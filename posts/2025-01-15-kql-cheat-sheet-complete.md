---
title: 'KQL Cheat Sheet: Complete Azure Log Analytics Query Guide (2025)'
date: 2025-01-15
modified: 2025-11-29
summary: 'A complete KQL cheat sheet for Azure admins: joins, summarize, extend, project,
  and real-world query patterns for Azure Resource Graph and Log Analytics.'
tags:
- Azure
- Cheat Sheet
- KQL
- Log Analytics
- Query Language
- Resource Graph
- Sentinel
cover: /static/images/hero/kql-cheat-sheet.png
---
# KQL Cheat Sheet for Azure Admins: Azure Resource Graph (VMs, NICs, Disks)

> **Note:** No Azure certification teaches KQL for operational queries. The AZ-104 exam shows you two sample queries. That's it. No Resource Graph training. No joins. No performance optimization. Nothing about the queries you'll actually write daily.
>
> I wrote about this gap: [The Azure Role Microsoft Forgot to Certify](/blog/azure-reporting-role-microsoft-should-create/). Until Microsoft fixes this, here's the KQL guide you need.

---

This Kusto Query Language (KQL) cheat sheet is designed for Azure administrators new to KQL, focusing on querying Azure resources like virtual machines (VMs), network interface cards (NICs), managed disks, and subscriptions using Azure Resource Graph in the Azure Portal (Resource Graph Explorer). 

Use this to inventory resources, check configurations, or troubleshoot VM-related issues. For more details, see the [KQL quick reference](https://docs.microsoft.com/en-us/azure/data-explorer/kql-quick-reference) and [Resource Graph query docs](https://docs.microsoft.com/en-us/azure/governance/resource-graph/).

## Getting Started

**Where to Run:** Azure Portal > Resource Graph Explorer (search "Resource Graph" in the portal).

**Key Tables:**
- `Resources`: Contains all Azure resources (VMs, NICs, disks, etc.)
- `ResourceContainers`: Contains subscriptions and resource groups

**Basic Query Structure:** Start with `Resources` or `ResourceContainers`, pipe (`|`) to operators like `where`, `join`, or `project`.

**Case Sensitivity:** Operators are case-insensitive; string comparisons (e.g., `has`) are case-sensitive unless using `_cs` (e.g., `has_cs`).

**Resource Graph Notes:** Queries resource metadata (not logs or metrics). No `TimeGenerated` field, unlike Log Analytics.

## Quick Start: Your First 3 Queries

**1. List all your VMs:**
```kql
Resources
| where type == "microsoft.compute/virtualmachines"
| project name, location, resourceGroup
```

**2. Find VMs in a specific resource group:**
```kql
Resources  
| where type == "microsoft.compute/virtualmachines"
| where resourceGroup == "MyResourceGroup"
| project name, location
```

**3. Show VM count by location:**
```kql
Resources
| where type == "microsoft.compute/virtualmachines" 
| summarize count() by location
```

## Core KQL Concepts

**Tables = Your Data Sources**
- Think of tables like Excel sheets - each contains different types of data
- `Resources` = all your Azure resources
- `ResourceContainers` = subscriptions and resource groups

**Where = Your Filter**
- Like Excel filters - narrows down your data
- Always filter early for better performance

**Project = Your Columns**
- Selects which columns to display
- Keeps output clean and focused

## Querying Resources

Use `Resources` to list VMs, NICs, disks, or other resources.

| What You Want | Example | Description |
|---------------|---------|-------------|
| List VMs | `Resources \| where type == "microsoft.compute/virtualmachines"` | All VMs across subscriptions |
| List NICs | `Resources \| where type == "microsoft.network/networkinterfaces"` | All network interfaces |
| List Disks | `Resources \| where type == "microsoft.compute/disks"` | All managed disks |
| Filter by Resource Group | `Resources \| where resourceGroup == "MyResourceGroup"` | Resources in a specific group |
| Filter by Tag | `Resources \| where tags["Environment"] == "Production"` | Resources with specific tag value |

**Example: List VMs in a specific resource group:**
```kql
Resources
| where type == "microsoft.compute/virtualmachines"
| where resourceGroup == "MyResourceGroup"
| project name, location, resourceGroup
```

## Joining Resources

Use `join` to correlate VMs with NICs, disks, or subscriptions. The `properties` column is JSON, so use `tostring` or `parse_json` to extract fields.

| What You Want | Example | Description |
|---------------|---------|-------------|
| VMs to NICs | `Resources \| where type == "microsoft.compute/virtualmachines" \| extend NICId = tostring(properties.networkProfile.networkInterfaces[0].id) \| join kind=leftouter (Resources \| where type == "microsoft.network/networkinterfaces") on $left.NICId == $right.id` | Links VMs to their NICs |
| VMs to Disks | `Resources \| where type == "microsoft.compute/virtualmachines" \| extend DiskId = tostring(properties.storageProfile.osDisk.managedDisk.id) \| join kind=leftouter (Resources \| where type == "microsoft.compute/disks") on $left.DiskId == $right.id` | Links VMs to OS disks |
| VMs to Subscriptions | `Resources \| where type == "microsoft.compute/virtualmachines" \| join kind=leftouter (ResourceContainers \| where type == "microsoft.resources/subscriptions") on subscriptionId` | Adds subscription names |

**Example: VMs with NIC and subscription details:**
```kql
Resources
| where type == "microsoft.compute/virtualmachines"
| extend NetworkInterfaceId = tostring(properties.networkProfile.networkInterfaces[0].id)
| join kind=leftouter (
    Resources
    | where type == "microsoft.network/networkinterfaces"
    | project NetworkInterfaceId = id, PrivateIP = tostring(properties.ipConfigurations[0].properties.privateIPAddress)
) on NetworkInterfaceId
| join kind=leftouter (
    ResourceContainers
    | where type == "microsoft.resources/subscriptions"
    | project subscriptionId, SubscriptionName = name
) on subscriptionId
| project VMName = name, PrivateIP, SubscriptionName, resourceGroup
```

## Extracting JSON Properties

Parse JSON fields from the `properties` column to get detailed resource information:

| Field | Example | Description |
|-------|---------|-------------|
| VM Computer Name | `extend VM_ComputerName = tostring(properties.osProfile.computerName)` | VM's internal name |
| NIC Private IP | `extend PrivateIP = tostring(properties.ipConfigurations[0].properties.privateIPAddress)` | NIC's private IP address |
| VNet/Subnet Name | `extend VNetName = split(tostring(properties.ipConfigurations[0].properties.subnet.id), "/")[8]` | Extract VNet from subnet ID |
| Disk Size | `extend DiskSizeGB = toint(properties.diskSizeGB)` | Disk size in GB |
| OS Type | `extend OSType = tostring(properties.storageProfile.osDisk.osType)` | OS (Windows/Linux) |

**Example: Get VM OS and disk details:**
```kql
Resources
| where type == "microsoft.compute/virtualmachines"
| extend OSType = tostring(properties.storageProfile.osDisk.osType),
         DiskSizeGB = toint(properties.storageProfile.osDisk.diskSizeGB)
| project VMName = name, OSType, DiskSizeGB, resourceGroup
```

## Custom Fields and Conditional Logic

Use `case()` to create custom fields and business logic:

| What You Want | Example | Description |
|---------------|---------|-------------|
| Custom OS Name | `extend DetailedOS = case(properties.storageProfile.osDisk.osType == "Windows", "Windows Server", properties.storageProfile.osDisk.osType == "Linux", "Linux", "Unknown")` | Categorize OS type |
| Tag Extraction | `extend Owner = tostring(tags["Owner"])` | Extract tag value |
| Update Strategy | `extend UpdateMethod = case(properties.storageProfile.osDisk.osType == "Windows", "Azure Update Manager", "Linux Package Manager")` | Define patching method |

**Example: VMs with OS details and tags:**
```kql
Resources
| where type == "microsoft.compute/virtualmachines"
| extend OSType = tostring(properties.storageProfile.osDisk.osType),
         DetailedOS = case(
             OSType == "Linux" and properties.storageProfile.imageReference.publisher == "Canonical", "Ubuntu Linux",
             OSType == "Windows" and properties.storageProfile.imageReference.offer contains "WindowsServer", "Windows Server",
             "Unknown"
         ),
         Environment = tostring(tags["Environment"])
| project VMName = name, DetailedOS, Environment, resourceGroup
```

## Disk Queries

Query disks directly or join with VMs to check configurations:

| What You Want | Example | Description |
|---------------|---------|-------------|
| List Disks | `Resources \| where type == "microsoft.compute/disks"` | All managed disks |
| Disks by VM | `Resources \| where type == "microsoft.compute/virtualmachines" \| extend DiskId = tostring(properties.storageProfile.osDisk.managedDisk.id) \| join kind=leftouter (Resources \| where type == "microsoft.compute/disks") on $left.DiskId == $right.id` | Links VMs to OS disks |
| Disk Size Filter | `Resources \| where type == "microsoft.compute/disks" \| extend DiskSizeGB = toint(properties.diskSizeGB) \| where DiskSizeGB > 100` | Disks larger than 100 GB |

**Example: VMs with OS disk sizes:**
```kql
Resources
| where type == "microsoft.compute/virtualmachines"
| extend DiskId = tostring(properties.storageProfile.osDisk.managedDisk.id)
| join kind=leftouter (
    Resources
    | where type == "microsoft.compute/disks"
    | project DiskId = id, DiskSizeGB = toint(properties.diskSizeGB)
) on DiskId
| project VMName = name, DiskSizeGB, resourceGroup
```

## Copy-Paste Ready Queries for Common Tasks

### 1. Complete VM Inventory
```kql
Resources
| where type == "microsoft.compute/virtualmachines"
| extend NetworkInterfaceId = tostring(properties.networkProfile.networkInterfaces[0].id),
         DiskId = tostring(properties.storageProfile.osDisk.managedDisk.id),
         OSType = tostring(properties.storageProfile.osDisk.osType),
         Environment = tostring(tags["Environment"])
| join kind=leftouter (
    Resources
    | where type == "microsoft.network/networkinterfaces"
    | project NetworkInterfaceId = id, PrivateIP = tostring(properties.ipConfigurations[0].properties.privateIPAddress)
) on NetworkInterfaceId
| join kind=leftouter (
    Resources
    | where type == "microsoft.compute/disks"
    | project DiskId = id, DiskSizeGB = toint(properties.diskSizeGB)
) on DiskId
| project VMName = name, PrivateIP, OSType, DiskSizeGB, Environment, resourceGroup
```

### 2. Cost Analysis: Resources by Type and Location
```kql
Resources
| summarize ResourceCount = count() by type, location
| order by ResourceCount desc
```

### 3. Security Audit: Find Untagged Resources
```kql
Resources
| where type in ("microsoft.compute/virtualmachines", "microsoft.storage/storageaccounts", "microsoft.network/networksecuritygroups")
| where isnull(tags) or array_length(bag_keys(tags)) == 0
| project name, type, resourceGroup, location
| order by type, name
```

### 4. VMs by Subscription and VNet
```kql
Resources
| where type == "microsoft.compute/virtualmachines"
| extend NetworkInterfaceId = tostring(properties.networkProfile.networkInterfaces[0].id)
| join kind=leftouter (
    Resources
    | where type == "microsoft.network/networkinterfaces"
    | extend VNetName = split(tostring(properties.ipConfigurations[0].properties.subnet.id), "/")[8]
    | project NetworkInterfaceId = id, VNetName
) on NetworkInterfaceId
| join kind=leftouter (
    ResourceContainers
    | where type == "microsoft.resources/subscriptions"
    | project subscriptionId, SubscriptionName = name
) on subscriptionId
| project VMName = name, VNetName, SubscriptionName, resourceGroup
```

### 5. Find Production VMs with Specific Tags
```kql
Resources
| where type == "microsoft.compute/virtualmachines"
| extend Environment = tostring(tags["Environment"]),
         Owner = tostring(tags["Owner"])
| where Environment == "Production"
| project VMName = name, Environment, Owner, resourceGroup
```

### 6. OS Distribution and Update Strategy
```kql
Resources
| where type == "microsoft.compute/virtualmachines"
| extend OSType = tostring(properties.storageProfile.osDisk.osType),
         OSProduct = tostring(properties.storageProfile.imageReference.offer),
         OSVersion = tostring(properties.storageProfile.imageReference.sku),
         DetailedOS = case(
             OSType == "Linux" and properties.storageProfile.imageReference.publisher == "Canonical", "Ubuntu Linux",
             OSType == "Linux" and properties.storageProfile.imageReference.publisher == "RedHat", "Red Hat Linux",
             OSType == "Windows" and OSProduct contains "WindowsServer" and OSVersion contains "2022", "Windows Server 2022",
             OSType == "Windows" and OSProduct contains "WindowsServer", "Windows Server - Other",
             "Unknown"
         ),
         UpdateMethod = case(
             OSType == "Windows" and OSProduct contains "WindowsServer", "Azure Update Manager",
             OSType == "Linux", "Linux Package Manager",
             "Manual"
         )
| project VMName = name, DetailedOS, UpdateMethod, resourceGroup
```

## Visualizing in Resource Graph

Resource Graph Explorer supports visualizations like tables or pie charts. Use `summarize` to prepare data:

| What You Want | Example | Description |
|---------------|---------|-------------|
| VMs by OS | `Resources \| where type == "microsoft.compute/virtualmachines" \| summarize count() by OSType = tostring(properties.storageProfile.osDisk.osType)` | Count VMs by Windows/Linux |
| Disks by Size | `Resources \| where type == "microsoft.compute/disks" \| summarize count() by DiskSizeGB = toint(properties.diskSizeGB)` | Count disks by size |

**Example: Chart VMs by OS type:**
```kql
Resources
| where type == "microsoft.compute/virtualmachines"
| summarize count() by OSType = tostring(properties.storageProfile.osDisk.osType)
```

In Resource Graph Explorer, select "Pie chart" in the portal to visualize.

## KQL Performance Optimization: Query Speed Matters at Scale

**When you're querying 31,000+ resources across 44 subscriptions, query performance matters.**

Here's what I learned managing enterprise-scale Azure environments.

### Why Query Performance Matters

**Slow query symptoms:**
- Query timeout errors in Resource Graph Explorer
- 30+ second wait times for results
- Portal becomes unresponsive
- Can't run queries during business hours (too slow)

**The cost of slow queries:**
- Wasted time (30 seconds × 50 queries/day = 25 minutes daily)
- Delayed incident response
- Frustrated stakeholders waiting for reports
- Can't use queries in automation (timeout kills scripts)

### Performance Rule #1: Filter Early, Filter Often

**Bad query (slow):**
```kql
Resources
| project name, type, location, resourceGroup, tags
| where type == "microsoft.compute/virtualmachines"
| where resourceGroup == "Production-RG"
```

**Why it's slow:** Projects ALL columns from ALL resources BEFORE filtering

**Good query (fast):**
```kql
Resources
| where type == "microsoft.compute/virtualmachines"
| where resourceGroup == "Production-RG"
| project name, location, tags
```

**Why it's fast:** Filters FIRST to reduce data, projects ONLY needed columns

**Performance improvement: 10-20x faster**

### Performance Rule #2: Project Only What You Need

**Bad query:**
```kql
Resources
| where type == "microsoft.compute/virtualmachines"
| extend AllProperties = parse_json(properties)
// Pulls entire properties JSON for every VM
```

**Good query:**
```kql
Resources
| where type == "microsoft.compute/virtualmachines"
| extend OSType = tostring(properties.storageProfile.osDisk.osType)
// Extracts only the specific field needed
```

**Why:** Parsing entire JSON objects is expensive. Extract only the fields you actually use.

### Performance Rule #3: Use `in` Instead of Multiple `or` Conditions

**Bad query:**
```kql
Resources
| where type == "microsoft.compute/virtualmachines" 
   or type == "microsoft.storage/storageaccounts"
   or type == "microsoft.network/networksecuritygroups"
   or type == "microsoft.sql/servers"
```

**Good query:**
```kql
Resources
| where type in ("microsoft.compute/virtualmachines", 
                 "microsoft.storage/storageaccounts",
                 "microsoft.network/networksecuritygroups",
                 "microsoft.sql/servers")
```

**Performance improvement: 3-5x faster** for multiple conditions

### Performance Rule #4: Limit Results During Testing

**Testing queries:**
```kql
Resources
| where type == "microsoft.compute/virtualmachines"
| take 10  // Test with 10 VMs first
| extend OSType = tostring(properties.storageProfile.osDisk.osType)
| project name, OSType
```

**Once query works, remove `take` for full results.**

**Why:** Testing on 10 rows is instant. Testing on 10,000 rows wastes time if query has errors.

### Performance Rule #5: Join Efficiently

**Bad join (slow):**
```kql
Resources
| where type == "microsoft.compute/virtualmachines"
| join (Resources) on $left.subscriptionId == $right.subscriptionId
// Joins to entire Resources table (millions of rows)
```

**Good join (fast):**
```kql
Resources
| where type == "microsoft.compute/virtualmachines"
| join kind=leftouter (
    Resources
    | where type == "microsoft.network/networkinterfaces"  // Filter BEFORE join
    | project NetworkInterfaceId = id, PrivateIP = tostring(properties.ipConfigurations[0].properties.privateIPAddress)
) on $left.NetworkInterfaceId == $right.NetworkInterfaceId
```

**Why:** Filter both sides of join to smallest dataset possible BEFORE joining.

### Real-World Performance Example

**Scenario:** Get all VMs with their private IPs across 44 subscriptions

**Bad query (45 seconds):**
```kql
Resources
| join (Resources | where type == "microsoft.network/networkinterfaces") on $left.id == $right.properties.virtualMachine.id
| where type == "microsoft.compute/virtualmachines"
| project name, PrivateIP = tostring(properties.ipConfigurations[0].properties.privateIPAddress)
```

**Good query (3 seconds):**
```kql
Resources
| where type == "microsoft.compute/virtualmachines"
| extend NetworkInterfaceId = tostring(properties.networkProfile.networkInterfaces[0].id)
| join kind=leftouter (
    Resources
    | where type == "microsoft.network/networkinterfaces"
    | project NetworkInterfaceId = id, PrivateIP = tostring(properties.ipConfigurations[0].properties.privateIPAddress)
) on NetworkInterfaceId
| project VMName = name, PrivateIP
```

**Performance improvement: 15x faster**

**Why the difference:**
1. Filter VMs first (reduces dataset)
2. Filter NICs before join (reduces join size)
3. Project only needed columns (reduces memory)
4. Use efficient join key (NetworkInterfaceId)

---

## KQL vs SQL: Translation Guide for SQL Developers

**Coming from SQL? Here's how KQL compares.**

Many Azure admins know SQL but not KQL. This translation guide helps you leverage existing knowledge.

### Basic Syntax Comparison

| Task | SQL | KQL |
|------|-----|-----|
| Select all | `SELECT * FROM VMs` | `Resources \| where type == "microsoft.compute/virtualmachines"` |
| Filter rows | `WHERE location = 'eastus'` | `\| where location == "eastus"` |
| Select columns | `SELECT name, location` | `\| project name, location` |
| Count rows | `SELECT COUNT(*) FROM VMs` | `Resources \| where type == "microsoft.compute/virtualmachines" \| count` |
| Group by | `GROUP BY location` | `\| summarize count() by location` |
| Order results | `ORDER BY name` | `\| order by name` |
| Limit results | `LIMIT 10` | `\| take 10` |

### Key Conceptual Differences

**SQL thinks in tables. KQL thinks in pipelines.**

**SQL:**
```sql
SELECT v.name, v.location, n.privateIP
FROM VMs v
LEFT JOIN NICs n ON v.NetworkInterfaceId = n.id
WHERE v.location = 'eastus'
ORDER BY v.name
```

**KQL equivalent:**
```kql
Resources
| where type == "microsoft.compute/virtualmachines"
| where location == "eastus"
| extend NetworkInterfaceId = tostring(properties.networkProfile.networkInterfaces[0].id)
| join kind=leftouter (
    Resources
    | where type == "microsoft.network/networkinterfaces"
    | project NetworkInterfaceId = id, PrivateIP = tostring(properties.ipConfigurations[0].properties.privateIPAddress)
) on NetworkInterfaceId
| order by name
| project name, location, PrivateIP
```

**Differences:**
- KQL uses pipes (`|`) to chain operations sequentially
- SQL uses JOIN at clause level, KQL uses `join` as an operator
- KQL requires `extend` to create new columns before using them
- SQL's `SELECT` combines column selection and calculation; KQL separates (`project` vs `extend`)

### Aggregation Translation

**SQL:**
```sql
SELECT location, COUNT(*) as VMCount
FROM VMs
GROUP BY location
HAVING COUNT(*) > 10
ORDER BY VMCount DESC
```

**KQL:**
```kql
Resources
| where type == "microsoft.compute/virtualmachines"
| summarize VMCount = count() by location
| where VMCount > 10
| order by VMCount desc
```

**Key difference:** KQL's `summarize` combines `GROUP BY` and aggregation. `HAVING` becomes a `where` after `summarize`.

### Subquery Translation

**SQL:**
```sql
SELECT *
FROM VMs
WHERE location IN (
    SELECT location 
    FROM VMs 
    GROUP BY location 
    HAVING COUNT(*) > 5
)
```

**KQL:**
```kql
let LocationsWithManyVMs = Resources
    | where type == "microsoft.compute/virtualmachines"
    | summarize VMCount = count() by location
    | where VMCount > 5
    | project location;
Resources
| where type == "microsoft.compute/virtualmachines"
| where location in (LocationsWithManyVMs)
```

**Key difference:** KQL uses `let` to define reusable subqueries. Think of it like SQL CTEs (Common Table Expressions).

### String Operations

| Task | SQL | KQL |
|------|-----|-----|
| Contains | `WHERE name LIKE '%prod%'` | `\| where name contains "prod"` |
| Starts with | `WHERE name LIKE 'vm-%'` | `\| where name startswith "vm-"` |
| Ends with | `WHERE name LIKE '%-prod'` | `\| where name endswith "-prod"` |
| Case insensitive | `WHERE LOWER(name) = 'vmname'` | `\| where name =~ "vmname"` |
| Concat | `CONCAT(name, '-', location)` | `strcat(name, "-", location)` or `name + "-" + location` |
| Substring | `SUBSTRING(name, 1, 5)` | `substring(name, 0, 5)` |

### Date/Time Operations (Log Analytics)

**Note:** Resource Graph doesn't have time-based data. These examples are for Log Analytics queries.

| Task | SQL | KQL |
|------|-----|-----|
| Last 24 hours | `WHERE timestamp > NOW() - INTERVAL 1 DAY` | `\| where TimeGenerated > ago(24h)` |
| Between dates | `WHERE timestamp BETWEEN '2024-01-01' AND '2024-01-31'` | `\| where TimeGenerated between (datetime(2024-01-01) .. datetime(2024-01-31))` |
| Date part | `EXTRACT(HOUR FROM timestamp)` | `format_datetime(TimeGenerated, 'HH')` or `bin(TimeGenerated, 1h)` |

### Common KQL Functions SQL Developers Should Know

**Case statements:**
```kql
// SQL: CASE WHEN ... THEN ... ELSE ... END
| extend OSCategory = case(
    OSType == "Windows", "Microsoft",
    OSType == "Linux", "Open Source",
    "Unknown"
)
```

**Coalesce (NULL handling):**
```kql
// SQL: COALESCE(column1, column2, 'default')
| extend Owner = coalesce(tags["Owner"], tags["CreatedBy"], "Unassigned")
```

**String splitting:**
```kql
// SQL: SPLIT_PART or STRING_SPLIT
| extend VNetName = split(SubnetId, "/")[8]  // Get 8th element from path
```

**Array operations:**
```kql
// Get first element
| extend FirstNIC = properties.networkProfile.networkInterfaces[0].id

// Array length
| extend NICCount = array_length(properties.networkProfile.networkInterfaces)
```

### Common SQL Patterns → KQL

**Get top N:**
```kql
// SQL: SELECT TOP 10 * FROM VMs ORDER BY DiskSizeGB DESC
Resources
| where type == "microsoft.compute/virtualmachines"
| extend DiskSizeGB = toint(properties.storageProfile.osDisk.diskSizeGB)
| top 10 by DiskSizeGB desc
```

**Distinct values:**
```kql
// SQL: SELECT DISTINCT location FROM VMs
Resources
| where type == "microsoft.compute/virtualmachines"
| distinct location
```

**Count distinct:**
```kql
// SQL: SELECT COUNT(DISTINCT location) FROM VMs
Resources
| where type == "microsoft.compute/virtualmachines"
| summarize UniqueLocations = dcount(location)
```

---

## Advanced KQL Techniques for Azure Resource Graph

**Beyond basics: techniques for complex queries.**

### Dynamic Columns and Arrays

**Problem:** You need to work with arrays in JSON properties.

**Extract all NICs from a VM (not just first):**
```kql
Resources
| where type == "microsoft.compute/virtualmachines"
| mv-expand NIC = properties.networkProfile.networkInterfaces
| extend NetworkInterfaceId = tostring(NIC.id)
| join kind=leftouter (
    Resources
    | where type == "microsoft.network/networkinterfaces"
    | project NetworkInterfaceId = id, PrivateIP = tostring(properties.ipConfigurations[0].properties.privateIPAddress)
) on NetworkInterfaceId
| summarize NICs = make_list(PrivateIP) by VMName = name
| project VMName, AllPrivateIPs = NICs
```

**What `mv-expand` does:** Expands arrays into separate rows (like SQL's UNNEST or CROSS APPLY).

### Working with Tags at Scale

**Find resources missing critical tags:**
```kql
Resources
| where type in ("microsoft.compute/virtualmachines", "microsoft.storage/storageaccounts")
| extend HasEnvironmentTag = isnotnull(tags["Environment"]),
         HasOwnerTag = isnotnull(tags["Owner"]),
         HasCostCenterTag = isnotnull(tags["CostCenter"])
| where HasEnvironmentTag == false or HasOwnerTag == false or HasCostCenterTag == false
| extend MissingTags = strcat(
    iff(HasEnvironmentTag == false, "Environment ", ""),
    iff(HasOwnerTag == false, "Owner ", ""),
    iff(HasCostCenterTag == false, "CostCenter", "")
)
| project name, type, resourceGroup, MissingTags
| order by type, name
```

**Result:** Clear report showing exactly which tags are missing per resource.

### Complex JSON Parsing

**Extract nested properties:**
```kql
Resources
| where type == "microsoft.compute/virtualmachines"
| extend ImagePublisher = tostring(properties.storageProfile.imageReference.publisher),
         ImageOffer = tostring(properties.storageProfile.imageReference.offer),
         ImageSku = tostring(properties.storageProfile.imageReference.sku),
         ImageVersion = tostring(properties.storageProfile.imageReference.version),
         FullImageString = strcat(ImagePublisher, ":", ImageOffer, ":", ImageSku, ":", ImageVersion)
| summarize VMCount = count() by FullImageString
| order by VMCount desc
```

**Use case:** Understand image distribution across your environment.

### Cross-Subscription Resource Relationships

**Find VMs connected to VNets in different subscriptions:**
```kql
Resources
| where type == "microsoft.compute/virtualmachines"
| extend NetworkInterfaceId = tostring(properties.networkProfile.networkInterfaces[0].id)
| join kind=leftouter (
    Resources
    | where type == "microsoft.network/networkinterfaces"
    | extend SubnetId = tostring(properties.ipConfigurations[0].properties.subnet.id)
    | extend VNetSubscription = split(SubnetId, "/")[2]
    | project NetworkInterfaceId = id, VNetSubscription, NICSubscription = subscriptionId
) on NetworkInterfaceId
| where VNetSubscription != NICSubscription  // Cross-subscription connection
| project VMName = name, VMSubscription = subscriptionId, VNetSubscription, resourceGroup
```

**Why this matters:** Cross-subscription networking creates security and cost allocation complexity.

### Bulk Compliance Checking

**Check for specific security configurations across all VMs:**
```kql
Resources
| where type == "microsoft.compute/virtualmachines"
| extend BootDiagEnabled = tobool(properties.diagnosticsProfile.bootDiagnostics.enabled),
         ManagedDisk = isnotnull(properties.storageProfile.osDisk.managedDisk),
         VMAgent = properties.osProfile.windowsConfiguration.provisionVMAgent,
         SecurityType = tostring(properties.securityProfile.securityType)
| extend ComplianceScore = 
    iff(BootDiagEnabled, 25, 0) +
    iff(ManagedDisk, 25, 0) +
    iff(VMAgent == true, 25, 0) +
    iff(SecurityType == "TrustedLaunch", 25, 0)
| extend ComplianceStatus = case(
    ComplianceScore >= 75, "Compliant",
    ComplianceScore >= 50, "Partial",
    "Non-Compliant"
)
| project VMName = name, ComplianceScore, ComplianceStatus, resourceGroup
| order by ComplianceScore asc
```

**Result:** Quantitative compliance scoring for prioritizing remediation.

---

## Microsoft Sentinel KQL Examples

**KQL for security operations in Sentinel.**

Microsoft Sentinel uses KQL for security queries. Here are common patterns for Azure admins working with Sentinel.

### Failed Sign-In Attempts

**Find repeated failed sign-ins from same user:**
```kql
SigninLogs
| where TimeGenerated > ago(24h)
| where ResultType != "0"  // 0 = success
| summarize FailedAttempts = count(), 
            IPAddresses = make_set(IPAddress),
            Locations = make_set(Location)
            by UserPrincipalName
| where FailedAttempts > 5
| order by FailedAttempts desc
```

**Use case:** Detect brute force attacks or compromised credentials.

### Azure Activity Log Security Events

**Track who deleted Azure resources:**
```kql
AzureActivity
| where TimeGenerated > ago(7d)
| where OperationNameValue endswith "/delete"
| where ActivityStatusValue == "Success"
| project TimeGenerated, Caller, OperationNameValue, ResourceId, ResourceGroup
| order by TimeGenerated desc
```

**Use case:** Security audit trail for resource deletions.

### VM Creation and Modification Tracking

**Monitor VM deployments:**
```kql
AzureActivity
| where TimeGenerated > ago(30d)
| where ResourceProviderValue == "Microsoft.Compute"
| where OperationNameValue has "virtualMachines/write"
| extend VMName = tostring(parse_json(Properties).resource)
| project TimeGenerated, Caller, VMName, ResourceGroup, SubscriptionId
| order by TimeGenerated desc
```

**Use case:** Track who's creating VMs (cost control + security).

### Detecting Unusual Azure Portal Access

**Find logins from new countries:**
```kql
let UserLocations = SigninLogs
    | where TimeGenerated > ago(90d)
    | summarize KnownCountries = make_set(LocationDetails.countryOrRegion) by UserPrincipalName;
SigninLogs
| where TimeGenerated > ago(24h)
| extend Country = tostring(LocationDetails.countryOrRegion)
| join kind=leftouter (UserLocations) on UserPrincipalName
| where Country !in (KnownCountries)  // New country
| project TimeGenerated, UserPrincipalName, Country, IPAddress, ResultType
```

**Use case:** Detect compromised accounts accessed from unusual locations.

### High-Privilege Azure Role Assignments

**Track who's assigning Owner/Contributor roles:**
```kql
AzureActivity
| where TimeGenerated > ago(30d)
| where OperationNameValue == "Microsoft.Authorization/roleAssignments/write"
| extend RoleDefinition = tostring(parse_json(Properties).roleDefinitionId)
| where RoleDefinition has "Owner" or RoleDefinition has "Contributor"
| project TimeGenerated, Caller, ResourceId, ResourceGroup, SubscriptionId
| order by TimeGenerated desc
```

**Use case:** Security monitoring of privilege escalation.

### Sentinel Watchlist Integration

**Check if IPs are in threat watchlist:**
```kql
let ThreatIPs = _GetWatchlist("KnownBadIPs")
    | project IPAddress = SearchKey;
SigninLogs
| where TimeGenerated > ago(24h)
| where IPAddress in (ThreatIPs)
| project TimeGenerated, UserPrincipalName, IPAddress, Location, ResultType
```

**Use case:** Correlate Azure activity with threat intelligence.

---

## Troubleshooting Common Errors

**Query timeout:** Add `| take 100` to limit results while testing

**JSON parsing errors:** Use `tostring()` consistently when extracting from `properties`

**Join failures:** Verify the join keys match exactly (case-sensitive)

**Empty results:** Check resource type spelling: `"microsoft.compute/virtualmachines"` (all lowercase)

**"The request had some invalid properties" error:**
- Usually caused by trying to access properties that don't exist
- Use `isnotnull()` or `coalesce()` to handle missing properties
- Example: `| extend OSType = coalesce(tostring(properties.storageProfile.osDisk.osType), "Unknown")`

**"Query execution exceeded the maximum allowed time" error:**
- Query is too complex or dataset too large
- Apply filters earlier in the query
- Reduce the number of joins
- Break complex queries into smaller steps with `let` statements

**"Mv-expand operator: argument 'ColumnName' is not an array" error:**
- Trying to expand a non-array field
- Verify the property is actually an array using `array_length()`
- Example check: `| where array_length(properties.networkProfile.networkInterfaces) > 0`

**"Column 'propertyName' not found" error:**
- Property doesn't exist on all resources being queried
- Filter to specific resource types first
- Use `has` instead of exact property paths for safer queries

## Tips for Beginners

- **Run Queries:** Use Azure Portal > Resource Graph Explorer for quick access
- **Parse JSON:** Use `tostring` or `parse_json` for properties and tags
- **Test Small:** Add `take 10` to preview results
- **Schema:** Check table/column details in Resource Graph Explorer's left pane
- **Performance:** Filter early with `where type == ...` to reduce data
- **Limitations:** Resource Graph is for metadata only. For metrics (e.g., CPU, disk IOPS), use Log Analytics (`AzureMetrics`)
- **Save queries:** Use Resource Graph Explorer's "Save" button to build a personal query library
- **Shared queries:** Create shared queries in Azure for team collaboration
- **Export results:** Use "Download as CSV" for Excel analysis or reporting

---

## Download PDF Version

Want this cheat sheet as a PDF for easy reference? Get 45+ production-ready KQL queries including advanced joins, performance optimization, and automation templates.

<div style="max-width: 600px; margin: 2rem auto; padding: 2rem; background: linear-gradient(135deg, #7c3aed 0%, #5b21b6 100%); border-radius: 12px; text-align: center; color: white; box-shadow: 0 8px 24px rgba(124, 58, 237, 0.3);">
  <h3 style="margin: 0 0 1rem; font-size: 1.5rem; color: white;">📥 Get the Complete KQL Query Library</h3>
  <p style="margin: 0 0 1.5rem; font-size: 1rem; opacity: 0.95;">
    Resource Graph, Log Analytics, Cost Management queries + automation templates
  </p>
  <form action="https://magic.beehiiv.com/v1/3827b09b-c887-4929-a724-f6c97cef1c94" method="GET" style="max-width: 500px; margin: 0 auto; display: flex; gap: 0.5rem; flex-wrap: wrap; justify-content: center;">
    <input type="email" name="email" placeholder="your@email.com" required style="flex: 1; min-width: 250px; padding: 0.75rem 1rem; border: 2px solid rgba(255,255,255,0.3); border-radius: 6px; font-size: 1rem; background: rgba(255,255,255,0.9);">
    <input type="hidden" name="utm_source" value="azure-noob-blog">
    <input type="hidden" name="utm_medium" value="lead-magnet">
    <input type="hidden" name="utm_campaign" value="kql-query-library">
    <button type="submit" style="padding: 0.75rem 1.5rem; background: white; color: #7c3aed; border: none; border-radius: 6px; font-size: 1rem; font-weight: 700; cursor: pointer; white-space: nowrap;">Get Free Download</button>
  </form>
  <p style="margin: 1rem 0 0; font-size: 0.85rem; opacity: 0.8;">
    Instant delivery. Unsubscribe anytime.
  </p>
</div>

---

**Questions about KQL or need help with a specific query?** Find more Azure insights at [azure-noob.com](https://azure-noob.com).

*KQL Cheat Sheet v2.0 - Updated with performance optimization, SQL translation guide, and Sentinel examples*
