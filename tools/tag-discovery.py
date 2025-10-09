"""
Azure Tag Discovery Script
Analyzes all resources across subscriptions to identify tag inconsistencies

This script discovers:
1. All unique tag keys (showing capitalization variations)
2. All unique values per tag key
3. Resources missing critical tags
4. Complete tag inventory for analysis

Usage:
    python tag-discovery.py

Output:
    - Console summary
    - tag-keys-report.csv (all tag keys and their usage)
    - tag-values-report.csv (all values for critical tags)
    - missing-tags-report.csv (resources missing critical tags)
    - full-inventory.csv (complete tag state of all resources)
"""

import os
from datetime import datetime
from azure.identity import DefaultAzureCredential
from azure.mgmt.resourcegraph import ResourceGraphClient
from azure.mgmt.resourcegraph.models import QueryRequest, QueryRequestOptions
from azure.mgmt.subscription import SubscriptionClient
import csv
from collections import defaultdict

# Critical tags we care about (add your specific tags here)
CRITICAL_TAGS = ['CostCenter', 'Environment', 'Owner', 'Department', 'Application']

def get_all_subscriptions(credential):
    """Get all subscription IDs the current account has access to"""
    subscription_client = SubscriptionClient(credential)
    subscriptions = []
    
    print("Discovering subscriptions...")
    for sub in subscription_client.subscriptions.list():
        subscriptions.append({
            'id': sub.subscription_id,
            'name': sub.display_name
        })
        print(f"  Found: {sub.display_name} ({sub.subscription_id})")
    
    print(f"\nTotal subscriptions: {len(subscriptions)}\n")
    return subscriptions

def run_resource_graph_query(client, query, subscription_ids):
    """Execute a Resource Graph query across subscriptions"""
    request = QueryRequest(
        subscriptions=subscription_ids,
        query=query,
        options=QueryRequestOptions(
            top=5000,  # Maximum results per page
            skip=0
        )
    )
    
    all_results = []
    response = client.resources(request)
    all_results.extend(response.data)
    
    # Handle pagination if there are more results
    while response.skip_token:
        request.options.skip_token = response.skip_token
        response = client.resources(request)
        all_results.extend(response.data)
    
    return all_results

def discover_all_tag_keys(client, subscription_ids):
    """Find all unique tag keys across all resources"""
    print("=" * 80)
    print("DISCOVERY 1: Finding all tag keys (including variations)")
    print("=" * 80)
    
    query = """
    Resources
    | where isnotempty(tags)
    | mvexpand tags
    | extend TagKey = tostring(bag_keys(tags)[0])
    | summarize 
        ResourceCount = count(),
        SubscriptionCount = dcount(subscriptionId),
        ResourceTypes = make_set(type)
        by TagKey
    | order by ResourceCount desc
    """
    
    results = run_resource_graph_query(client, query, subscription_ids)
    
    print(f"\nFound {len(results)} unique tag keys:\n")
    
    tag_key_data = []
    for row in results:
        tag_key = row.get('TagKey', 'Unknown')
        count = row.get('ResourceCount', 0)
        sub_count = row.get('SubscriptionCount', 0)
        
        tag_key_data.append({
            'TagKey': tag_key,
            'ResourceCount': count,
            'SubscriptionCount': sub_count,
            'ResourceTypes': ', '.join(row.get('ResourceTypes', []))[:200]  # Truncate for CSV
        })
        
        print(f"  {tag_key:40} | {count:6} resources | {sub_count:2} subscriptions")
    
    # Export to CSV
    with open('tag-keys-report.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['TagKey', 'ResourceCount', 'SubscriptionCount', 'ResourceTypes'])
        writer.writeheader()
        writer.writerows(tag_key_data)
    
    print(f"\n✓ Exported to: tag-keys-report.csv")
    return tag_key_data

def discover_tag_variations(tag_key_data):
    """Identify tag key variations (capitalization differences)"""
    print("\n" + "=" * 80)
    print("ANALYSIS: Tag Key Variations (Likely Same Tag, Different Capitalization)")
    print("=" * 80 + "\n")
    
    # Group by lowercase version to find variations
    variations = defaultdict(list)
    for tag in tag_key_data:
        key = tag['TagKey']
        key_lower = key.lower()
        variations[key_lower].append(key)
    
    # Find tags with multiple variations
    problems = []
    for key_lower, keys in variations.items():
        if len(keys) > 1:
            problems.append({
                'normalized': key_lower,
                'variations': keys,
                'count': len(keys)
            })
    
    if problems:
        print(f"Found {len(problems)} tag keys with capitalization variations:\n")
        for problem in sorted(problems, key=lambda x: x['count'], reverse=True):
            print(f"  {problem['normalized']}:")
            for variation in problem['variations']:
                print(f"    - {variation}")
            print()
    else:
        print("No obvious capitalization variations found (this is good!)\n")
    
    return problems

def discover_tag_values_for_key(client, subscription_ids, tag_key, variations=None):
    """Get all values for a specific tag key (including variations)"""
    print(f"\n{'=' * 80}")
    print(f"DISCOVERY 2: Values for '{tag_key}' tag")
    print("=" * 80)
    
    # Build the query to check multiple variations
    if variations:
        conditions = " or ".join([f"isnotempty(tags['{v}'])" for v in variations])
        coalesce_args = ", ".join([f"tostring(tags['{v}'])" for v in variations])
        query = f"""
        Resources
        | where {conditions}
        | extend TagValue = coalesce({coalesce_args})
        | where isnotempty(TagValue)
        | summarize 
            ResourceCount = count(),
            SubscriptionCount = dcount(subscriptionId),
            ResourceTypes = make_set(type)
            by TagValue
        | order by ResourceCount desc
        """
    else:
        query = f"""
        Resources
        | where isnotempty(tags['{tag_key}'])
        | extend TagValue = tostring(tags['{tag_key}'])
        | summarize 
            ResourceCount = count(),
            SubscriptionCount = dcount(subscriptionId),
            ResourceTypes = make_set(type)
            by TagValue
        | order by ResourceCount desc
        """
    
    results = run_resource_graph_query(client, query, subscription_ids)
    
    print(f"\nFound {len(results)} unique values:\n")
    
    for row in results[:50]:  # Show top 50
        value = row.get('TagValue', 'Unknown')
        count = row.get('ResourceCount', 0)
        print(f"  {value:40} | {count:6} resources")
    
    if len(results) > 50:
        print(f"\n  ... and {len(results) - 50} more values")
    
    return results

def discover_missing_tags(client, subscription_ids, critical_tags):
    """Find resources missing critical tags"""
    print(f"\n{'=' * 80}")
    print("DISCOVERY 3: Resources Missing Critical Tags")
    print("=" * 80)
    
    # Build dynamic query for all critical tags
    has_conditions = []
    missing_counts = []
    
    for tag in critical_tags:
        # Check common variations
        has_conditions.append(f"Has{tag} = isnotempty(tags['{tag}']) or isnotempty(tags['{tag.lower()}'])")
        missing_counts.append(f"Missing{tag} = countif(Has{tag} == false)")
    
    has_extend = ",\n        ".join(has_conditions)
    missing_summarize = ",\n        ".join(missing_counts)
    
    query = f"""
    Resources
    | extend 
        {has_extend}
    | summarize 
        {missing_summarize},
        TotalResources = count()
        by subscriptionId, resourceGroup
    | order by TotalResources desc
    """
    
    results = run_resource_graph_query(client, query, subscription_ids)
    
    print(f"\nResource groups with missing tags:\n")
    
    missing_data = []
    for row in results[:20]:  # Show top 20
        sub_id = row.get('subscriptionId', 'Unknown')[:8]
        rg = row.get('resourceGroup', 'Unknown')
        total = row.get('TotalResources', 0)
        
        print(f"  {rg:40} | Total: {total:4}")
        
        row_data = {
            'SubscriptionId': sub_id,
            'ResourceGroup': rg,
            'TotalResources': total
        }
        
        for tag in critical_tags:
            missing = row.get(f'Missing{tag}', 0)
            pct = (missing / total * 100) if total > 0 else 0
            row_data[f'Missing_{tag}'] = missing
            row_data[f'Missing_{tag}_Pct'] = f"{pct:.1f}%"
            if missing > 0:
                print(f"    - Missing {tag}: {missing} ({pct:.1f}%)")
        print()
        
        missing_data.append(row_data)
    
    # Export to CSV
    if missing_data:
        fieldnames = ['SubscriptionId', 'ResourceGroup', 'TotalResources']
        for tag in critical_tags:
            fieldnames.extend([f'Missing_{tag}', f'Missing_{tag}_Pct'])
        
        with open('missing-tags-report.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(missing_data)
        
        print(f"\n✓ Exported to: missing-tags-report.csv")
    
    return missing_data

def export_full_inventory(client, subscription_ids, critical_tags):
    """Export complete tag state for all resources"""
    print(f"\n{'=' * 80}")
    print("DISCOVERY 4: Full Tag Inventory (This may take a while...)")
    print("=" * 80 + "\n")
    
    # Build query to extract all critical tags
    tag_extracts = []
    for tag in critical_tags:
        # Check multiple variations
        tag_extracts.append(
            f"{tag}Raw = coalesce(tostring(tags['{tag}']), tostring(tags['{tag.lower()}']), 'MISSING')"
        )
    
    tag_extend = ",\n        ".join(tag_extracts)
    tag_project = ", ".join([f"{tag}Raw" for tag in critical_tags])
    
    query = f"""
    Resources
    | extend 
        {tag_extend}
    | project 
        ResourceId = id,
        ResourceName = name,
        ResourceType = type,
        SubscriptionId = subscriptionId,
        ResourceGroup = resourceGroup,
        Location = location,
        {tag_project}
    """
    
    results = run_resource_graph_query(client, query, subscription_ids)
    
    print(f"Found {len(results)} total resources")
    print(f"Exporting to full-inventory.csv...")
    
    # Export to CSV
    if results:
        fieldnames = ['ResourceId', 'ResourceName', 'ResourceType', 'SubscriptionId', 
                     'ResourceGroup', 'Location'] + [f"{tag}Raw" for tag in critical_tags]
        
        with open('full-inventory.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for row in results:
                writer.writerow(row)
        
        print(f"✓ Exported {len(results)} resources to: full-inventory.csv\n")
    
    return results

def generate_summary_report(tag_key_data, missing_data, full_inventory):
    """Generate a summary report of findings"""
    print("\n" + "=" * 80)
    print("SUMMARY REPORT")
    print("=" * 80 + "\n")
    
    print(f"Total Resources Analyzed: {len(full_inventory)}")
    print(f"Unique Tag Keys Found: {len(tag_key_data)}")
    print(f"Resource Groups Analyzed: {len(missing_data)}\n")
    
    # Calculate missing tag statistics
    print("Missing Tag Statistics:")
    for tag in CRITICAL_TAGS:
        total_missing = sum(row.get(f'Missing_{tag}', 0) for row in missing_data)
        total_resources = sum(row.get('TotalResources', 0) for row in missing_data)
        pct = (total_missing / total_resources * 100) if total_resources > 0 else 0
        print(f"  {tag:20} | {total_missing:6} missing ({pct:.1f}%)")
    
    print("\n" + "=" * 80)
    print("FILES GENERATED:")
    print("=" * 80)
    print("  1. tag-keys-report.csv      - All tag keys and usage")
    print("  2. missing-tags-report.csv  - Resources missing critical tags")
    print("  3. full-inventory.csv       - Complete tag state of all resources")
    print("\nNext Steps:")
    print("  1. Review tag-keys-report.csv for capitalization variations")
    print("  2. Review missing-tags-report.csv to identify worst resource groups")
    print("  3. Analyze full-inventory.csv to build normalization rules")
    print("=" * 80 + "\n")

def main():
    print("\n" + "=" * 80)
    print("AZURE TAG DISCOVERY TOOL")
    print("=" * 80)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Authenticate
    print("Authenticating to Azure...")
    credential = DefaultAzureCredential()
    
    # Get subscriptions
    subscriptions = get_all_subscriptions(credential)
    subscription_ids = [sub['id'] for sub in subscriptions]
    
    # Create Resource Graph client
    client = ResourceGraphClient(credential)
    
    # Run all discoveries
    tag_key_data = discover_all_tag_keys(client, subscription_ids)
    
    # Analyze for variations
    variations = discover_tag_variations(tag_key_data)
    
    # Discover values for critical tags
    print("\n" + "=" * 80)
    print("Analyzing values for critical tags...")
    print("=" * 80)
    
    for tag in CRITICAL_TAGS:
        # Find variations of this tag key
        tag_variations = [tag, tag.lower(), tag.upper()]
        # You could expand this based on what discover_all_tag_keys found
        discover_tag_values_for_key(client, subscription_ids, tag, tag_variations)
    
    # Find missing tags
    missing_data = discover_missing_tags(client, subscription_ids, CRITICAL_TAGS)
    
    # Export full inventory
    full_inventory = export_full_inventory(client, subscription_ids, CRITICAL_TAGS)
    
    # Generate summary
    generate_summary_report(tag_key_data, missing_data, full_inventory)
    
    print(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
