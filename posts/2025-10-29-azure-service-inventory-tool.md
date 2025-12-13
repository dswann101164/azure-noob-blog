---
title: 'Azure Service Inventory Tool: Which of the 397 Services Do You Actually Use?'
date: 2025-10-29
summary: 'A practical service inventory pattern for Azure: map resources to real business
  services, owners, and environments so governance and audits stop being guesswork.'
tags:
- Azure
- CMDB
- Governance
- Inventory
- Operations
- PowerShell
- Resource Graph
- Tools
cover: /static/images/hero/service-inventory-tool.svg
hub: automation
related_posts:
  - only-1-percent-know-these-tools
  - azure-ipam-tool
  - workbook-app-tool
  - azure-cost-optimization-what-actually-works
hub: governance
---
Microsoft says there are **397 Azure services**.

The [Azure Periodic Table](https://www.azureperiodictable.com/) displays them beautifully.

But here's what the periodic table doesn't tell you:
- Which services **you're** actually using
- How many of each service you have
- What they cost
- Who owns them
- Which ones are deprecated

After managing 31,000 resources across 44 subscriptions, I got tired of not knowing my actual service footprint.

So I built a tool to answer: **"Which of the 397 Azure services am I actually using?"**

Turns out: **38 services**. Out of 397.

This post shows you how to build the same tool for your environment.

## The Problem with the Periodic Table

The Azure Periodic Table is gorgeous. Great for:
- Learning what services exist
- Finding service descriptions
- Impressing executives in presentations

Terrible for:
- "What services does my organization use?"
- "How many App Service Plans do we have?"
- "Which services are we paying for?"
- "What's deprecated that we need to migrate off?"
- "Who owns Azure SQL in our environment?"

The periodic table shows all 397 services. I need to know which **38** I'm responsible for.

## What the Tool Does

This tool creates an **Azure Service Inventory** for your environment:

**Input:** Your Azure subscriptions

**Output:** Excel spreadsheet with:
- Every Azure service type you're using
- Count of each resource type
- Service category (Compute, Networking, Storage, etc.)
- Estimated cost tier
- Deprecated status
- Links to documentation
- Space for your team's notes

**Example Output:**

```
Service Type              Category    Count   Cost Tier   Deprecated
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Virtual Machines          Compute       156      High         No
Storage Accounts          Storage       423      Medium       No
Virtual Networks          Networking     44      Low          No
Network Interfaces        Networking    312      Free         No
Recovery Services Vault   Backup         12      Medium       No
Key Vault                 Security       18      Low          No
Log Analytics Workspace   Monitoring      8      Medium       No
Classic Storage Account   Storage         3      Medium       YES (migrate to v2)
```

**The Insight:** Out of 397 possible services, you're using 38. Focus on those.

## How It Works

### Step 1: Query Your Environment

Use Azure Resource Graph to get every resource type:

```kql
Resources
| summarize 
    Count = count(),
    Subscriptions = make_set(subscriptionId),
    ResourceGroups = make_set(resourceGroup)
  by type
| extend 
    Provider = split(type, '/')[0],
    ServiceType = split(type, '/')[1]
| project Provider, ServiceType, Count, Subscriptions, ResourceGroups
| order by Count desc
```

This returns every resource type in your environment with counts.

### Step 2: Enrich with Service Metadata

Match resource types against known Azure services:

- Service category (Compute, Networking, etc.)
- Cost tier (Free, Low, Medium, High)
- Deprecated status
- Documentation links
- Common use cases

### Step 3: Export to Excel

Create a searchable, sortable spreadsheet your team can use.

## The PowerShell Script

Here's the complete tool:

```powershell
<#
.SYNOPSIS
    Azure Service Inventory Tool
.DESCRIPTION
    Queries all subscriptions to determine which Azure services are actually in use.
    Creates an Excel-compatible CSV with service counts, categories, and metadata.
.EXAMPLE
    .\Get-AzureServiceInventory.ps1
    .\Get-AzureServiceInventory.ps1 -SubscriptionId "sub-id-here"
#>

param(
    [Parameter(Mandatory=$false)]
    [string]$SubscriptionId,
    
    [Parameter(Mandatory=$false)]
    [string]$OutputPath = ".\AzureServiceInventory.csv"
)

# Ensure Az.ResourceGraph module
if (-not (Get-Module -ListAvailable Az.ResourceGraph)) {
    Write-Host "Installing Az.ResourceGraph module..." -ForegroundColor Yellow
    Install-Module Az.ResourceGraph -Force -AllowClobber
}

Import-Module Az.ResourceGraph

# Check if logged in
$context = Get-AzContext
if (-not $context) {
    Write-Host "Not logged in to Azure. Running Connect-AzAccount..." -ForegroundColor Yellow
    Connect-AzAccount
}

Write-Host "`n🔍 Querying Azure Resource Graph for service inventory..." -ForegroundColor Cyan

# Build subscription scope
$subscriptionScope = if ($SubscriptionId) {
    @($SubscriptionId)
} else {
    (Get-AzSubscription | Where-Object {$_.State -eq 'Enabled'}).Id
}

Write-Host "📊 Scanning $($subscriptionScope.Count) subscription(s)..." -ForegroundColor Cyan

# Query all resource types
$query = @"
Resources
| summarize 
    Count = count(),
    SubscriptionCount = dcount(subscriptionId),
    Locations = make_set(location)
  by type
| extend 
    Provider = split(type, '/')[0],
    ServiceType = split(type, '/')[1]
| project Provider, ServiceType, Count, SubscriptionCount, Locations
| order by Count desc
"@

$results = Search-AzGraph -Query $query -Subscription $subscriptionScope -First 1000

Write-Host "✅ Found $($results.Count) distinct Azure service types in use`n" -ForegroundColor Green

# Service category mapping
$categoryMap = @{
    'Microsoft.Compute' = 'Compute'
    'Microsoft.Network' = 'Networking'
    'Microsoft.Storage' = 'Storage'
    'Microsoft.Web' = 'Web + Mobile'
    'Microsoft.Sql' = 'Databases'
    'Microsoft.DBforPostgreSQL' = 'Databases'
    'Microsoft.DBforMySQL' = 'Databases'
    'Microsoft.KeyVault' = 'Security'
    'Microsoft.ManagedIdentity' = 'Security'
    'Microsoft.Security' = 'Security'
    'Microsoft.OperationalInsights' = 'Monitoring'
    'Microsoft.Insights' = 'Monitoring'
    'Microsoft.Monitor' = 'Monitoring'
    'Microsoft.RecoveryServices' = 'Backup + DR'
    'Microsoft.Backup' = 'Backup + DR'
    'Microsoft.ContainerService' = 'Containers'
    'Microsoft.ContainerRegistry' = 'Containers'
    'Microsoft.Logic' = 'Integration'
    'Microsoft.ServiceBus' = 'Integration'
    'Microsoft.EventHub' = 'Integration'
    'Microsoft.Automation' = 'Management'
    'Microsoft.Resources' = 'Management'
    'Microsoft.Authorization' = 'Management'
}

# Cost tier estimation (rough)
$costTierMap = @{
    'virtualmachines' = 'High'
    'disks' = 'Medium'
    'snapshots' = 'Low'
    'storageaccounts' = 'Medium'
    'virtualnetworks' = 'Low'
    'networkinterfaces' = 'Free'
    'publicipaddresses' = 'Low'
    'loadbalancers' = 'Low'
    'applicationgateways' = 'High'
    'vaults' = 'Medium'  # Key Vault
    'servers' = 'High'   # SQL
    'workspaces' = 'Medium'  # Log Analytics
    'sites' = 'Medium'   # App Service
}

# Deprecated services
$deprecatedServices = @{
    'Microsoft.ClassicCompute/virtualMachines' = 'Migrate to Azure Resource Manager VMs'
    'Microsoft.ClassicStorage/storageAccounts' = 'Migrate to v2 Storage Accounts'
    'Microsoft.ClassicNetwork/virtualNetworks' = 'Migrate to ARM Virtual Networks'
}

# Build enriched inventory
$inventory = $results | ForEach-Object {
    $provider = $_.Provider
    $serviceType = $_.ServiceType
    $fullType = "$provider/$serviceType"
    
    $category = if ($categoryMap.ContainsKey($provider)) {
        $categoryMap[$provider]
    } else {
        'Other'
    }
    
    $costTier = if ($costTierMap.ContainsKey($serviceType.ToLower())) {
        $costTierMap[$serviceType.ToLower()]
    } else {
        'Unknown'
    }
    
    $deprecated = if ($deprecatedServices.ContainsKey($fullType)) {
        "YES - $($deprecatedServices[$fullType])"
    } else {
        'No'
    }
    
    $docsLink = "https://learn.microsoft.com/azure/?product=$($serviceType.ToLower())"
    
    [PSCustomObject]@{
        Provider = $provider
        ServiceType = $serviceType
        Category = $category
        Count = $_.Count
        SubscriptionCount = $_.SubscriptionCount
        Locations = ($_.Locations -join ', ')
        CostTier = $costTier
        Deprecated = $deprecated
        DocsLink = $docsLink
        Notes = ''  # For manual entry
        Owner = ''  # For manual entry
    }
}

# Export to CSV
$inventory | Export-Csv -Path $OutputPath -NoTypeInformation -Encoding UTF8

Write-Host "✅ Service inventory exported to: $OutputPath" -ForegroundColor Green
Write-Host "`n📊 Summary:" -ForegroundColor Cyan
Write-Host "   Total Services in Use: $($inventory.Count)" -ForegroundColor White
Write-Host "   Total Resources: $(($inventory | Measure-Object -Property Count -Sum).Sum)" -ForegroundColor White

# Category breakdown
$categoryBreakdown = $inventory | Group-Object Category | Sort-Object Count -Descending
Write-Host "`n📁 By Category:" -ForegroundColor Cyan
foreach ($cat in $categoryBreakdown) {
    Write-Host "   $($cat.Name): $($cat.Count) service types" -ForegroundColor White
}

# Check for deprecated services
$deprecatedCount = ($inventory | Where-Object {$_.Deprecated -ne 'No'}).Count
if ($deprecatedCount -gt 0) {
    Write-Host "`n⚠️  Warning: $deprecatedCount deprecated service(s) found!" -ForegroundColor Yellow
    $inventory | Where-Object {$_.Deprecated -ne 'No'} | ForEach-Object {
        Write-Host "   - $($_.ServiceType): $($_.Deprecated)" -ForegroundColor Yellow
    }
}

Write-Host "`n💡 Next Steps:" -ForegroundColor Cyan
Write-Host "   1. Open $OutputPath in Excel" -ForegroundColor White
Write-Host "   2. Add Owner and Notes columns for your team" -ForegroundColor White
Write-Host "   3. Filter by Category or CostTier" -ForegroundColor White
Write-Host "   4. Share with your team for service ownership mapping" -ForegroundColor White
Write-Host ""
```

### Running the Script

```powershell
# Run against all subscriptions
.\Get-AzureServiceInventory.ps1

# Run against specific subscription
.\Get-AzureServiceInventory.ps1 -SubscriptionId "your-sub-id"

# Custom output location
.\Get-AzureServiceInventory.ps1 -OutputPath "C:\Reports\ServiceInventory.csv"
```

### Output Example

The script creates a CSV with these columns:

| Provider | ServiceType | Category | Count | SubscriptionCount | Locations | CostTier | Deprecated | DocsLink | Notes | Owner |
|----------|-------------|----------|-------|-------------------|-----------|----------|------------|----------|-------|-------|
| Microsoft.Compute | virtualMachines | Compute | 156 | 12 | eastus, westus | High | No | [link] | | |
| Microsoft.Storage | storageAccounts | Storage | 423 | 18 | eastus, centralus | Medium | No | [link] | | |
| Microsoft.Network | virtualNetworks | Networking | 44 | 14 | eastus, westus | Low | No | [link] | | |

## What You Learn

Running this against my 44 subscriptions revealed:

### The 80/20 Rule Applies

**Top 10 services = 92% of all resources:**
1. Network Interfaces (8,234)
2. Disks (4,156)
3. Virtual Machines (3,890)
4. Public IP Addresses (2,341)
5. Storage Accounts (1,892)
6. Network Security Groups (847)
7. Virtual Networks (423)
8. Snapshots (312)
9. Key Vaults (287)
10. Recovery Services Vaults (156)

**Bottom 28 services = 8% of resources**

### We're Using 38 Services (Out of 397)

**Breakdown by category:**
- Compute: 8 service types
- Networking: 12 service types
- Storage: 4 service types
- Databases: 3 service types
- Monitoring: 4 service types
- Security: 3 service types
- Management: 2 service types
- Other: 2 service types

**The other 359 Azure services?** Marketing.

### We Have Deprecated Services

**3 classic services still in use:**
- Classic Storage Accounts: 12 instances
- Classic Virtual Networks: 3 instances

These need migration before they're force-retired.

### Multi-Subscription Sprawl is Real

Some services exist in **18 different subscriptions**:
- Storage Accounts
- Virtual Networks
- Log Analytics Workspaces

This complicates:
- Cost allocation
- Security policy
- Compliance auditing

The inventory makes this visible.

## How to Use This Tool

### 1. Service Rationalization

**Question:** "Do we really need 8 different monitoring solutions?"

**Inventory shows:**
- Log Analytics Workspaces: 8
- Application Insights: 12
- Monitor Diagnostic Settings: 156

**Decision:** Consolidate to 2 centralized Log Analytics workspaces.

### 2. Ownership Mapping

Open the CSV in Excel. Add Owner column:

```
ServiceType              Count   Owner
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Virtual Machines          156    Infrastructure Team
SQL Servers                23    Database Team
App Service Plans          45    Application Team
Storage Accounts          423    Unassigned ← Problem!
```

**Result:** 423 storage accounts with no owner. Time to fix that.

### 3. Cost Optimization Targets

Filter by CostTier = "High":

```
ServiceType          Count   CostTier   Monthly Cost (est)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Virtual Machines      156     High       $87,000
SQL Servers            23     High       $34,000
Application Gateways   12     High       $18,000
```

**Priority:** Focus cost optimization on VMs first (biggest impact).

### 4. Migration Planning (Merger Use Case)

We're merging 44 subscriptions down to 12.

**Inventory shows:**
- Company A uses: Azure Firewall
- Company B uses: Network Virtual Appliances

**Decision needed:** Standardize on one solution.

The inventory makes these conflicts visible **before** the migration.

### 5. Compliance & Audit

**Auditor:** "Show me all database services in scope."

**Excel filter:** Category = "Databases"

```
ServiceType                Count   Locations
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SQL Servers                 23     eastus, westus
PostgreSQL Servers          8      eastus
MySQL Servers               4      centralus
```

**Export:** Send filtered CSV to auditor. Done in 30 seconds.

## Advanced: Add Cost Data

The basic inventory shows *cost tier*. But you can add **actual cost**:

### Query Cost Management API

```powershell
# Add this to the script after building inventory
$costQuery = @"
{
  "type": "Usage",
  "timeframe": "MonthToDate",
  "dataset": {
    "granularity": "None",
    "aggregation": {
      "totalCost": {
        "name": "Cost",
        "function": "Sum"
      }
    },
    "grouping": [
      {
        "type": "Dimension",
        "name": "ResourceType"
      }
    ]
  }
}
"@

# Call Cost Management API for each subscription
# (Implementation left as exercise - requires Cost Management permissions)
```

**Result:** Add "ActualMonthlyCost" column to inventory.

## Why This Matters

Microsoft publishes 397 Azure services.

Most organizations use **30-50** of them.

But without an inventory, you don't know:
- Which services you have
- How many of each
- Who owns them
- What they cost
- What's deprecated

**This tool gives you that visibility in 2 minutes.**

It's not revolutionary. It's just **Resource Graph + Excel**.

But it answers questions you can't answer from the Azure Portal:
- "What's our Azure footprint?"
- "Which services are we responsible for?"
- "What should we focus on?"

## Real-World Use Cases

### Use Case 1: New Azure Admin Onboarding

**Problem:** New hire asks "What services do we use?"

**Old answer:** "Um, VMs, storage, networking... lots of stuff."

**New answer:** "Here's the inventory. We use 38 services. Focus on these 10."

### Use Case 2: M&A Due Diligence

**Problem:** Acquiring company. Need to understand their Azure environment.

**Old approach:** Manual discovery. Takes weeks.

**New approach:** Run the script. Inventory in 2 minutes.

### Use Case 3: Service Consolidation

**Problem:** 8 Log Analytics workspaces. Do we need all of them?

**Inventory shows:**
- 3 workspaces with >1000 resources
- 5 workspaces with <50 resources

**Decision:** Consolidate the 5 small ones.

### Use Case 4: Budget Planning

**CFO:** "What are we spending on Azure?"

**Inventory filtered by CostTier:**
- High: 12 service types
- Medium: 18 service types
- Low: 6 service types
- Free: 2 service types

**Budget focus:** The 12 high-cost services drive 80% of spend.

## Common Patterns You'll Find

After running this on multiple organizations:

### Pattern 1: The 80/20 Service Distribution

**80% of resources** = 10-15 service types (VMs, storage, networking basics)

**20% of resources** = 20-30 service types (databases, monitoring, security, etc.)

### Pattern 2: Zombie Services

Services with Count = 1-3 that nobody remembers creating:

```
ServiceType              Count   Owner
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Machine Learning Workspace  2     Unknown
Data Factory                1     Unknown
Container Registry          1     Unknown
```

**Investigation needed:** What are these? Can we delete them?

### Pattern 3: Multi-Subscription Sprawl

Same service type across 15+ subscriptions:

- Harder to secure consistently
- Harder to monitor
- Harder to optimize cost
- Harder to audit

**Strategy:** Consolidate where possible.

### Pattern 4: Classic Resource Debt

Classic resources still running:

```
ServiceType                      Count   Deprecated
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Classic Storage Accounts          12     YES
Classic Virtual Networks           3     YES
```

**Action required:** Migration project before force retirement.

## Limitations

This tool doesn't:

1. **Track service features** - Just that App Service exists, not which tiers/features
2. **Include resource properties** - Doesn't show VM sizes, storage tiers, etc.
3. **Calculate exact costs** - Estimates cost tier, not actual spend
4. **Track configuration** - Doesn't show settings, just existence
5. **Monitor health** - Doesn't show if services are broken

**What it does:** Give you a **service footprint** in 2 minutes.

For deeper analysis, use:
- Azure Advisor (recommendations)
- Cost Management (actual costs)
- Resource Graph Explorer (detailed queries)
- Azure Monitor (health/performance)

## Next Steps

### 1. Run the Script

```powershell
.\Get-AzureServiceInventory.ps1
```

### 2. Open in Excel

- Add filters
- Sort by Count
- Add Owner column
- Add Notes column

### 3. Share with Your Team

Use it for:
- Service ownership mapping
- Cost optimization planning
- Migration preparation
- Audit documentation
- New hire onboarding

### 4. Re-Run Quarterly

Track how your service footprint changes:
- New services added
- Old services retired
- Resource counts growing/shrinking

## The Bottom Line

Microsoft offers 397 Azure services.

You're probably using **30-50** of them.

But you don't know which ones without an inventory.

**This tool gives you that inventory in 2 minutes.**

It's not fancy. It's just Resource Graph + CSV.

But it answers questions the Azure Portal can't:
- "What's our service footprint?"
- "Where should we focus?"
- "What's deprecated?"
- "Who owns what?"

Run the script. Open the CSV. You'll know.

---

**Download the script:** [Get-AzureServiceInventory.ps1](/static/downloads/Get-AzureServiceInventory.ps1)

**Questions?** Leave a comment below.

**Want more operational tools?** Check out [azure-noob.com](https://azure-noob.com) for practical Azure automation.
