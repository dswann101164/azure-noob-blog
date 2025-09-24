---
title: "KQL Cheat Sheet for Azure Admins: Complete Resource Graph Guide"
date: 2025-09-23
summary: "Master Azure Resource Graph with this comprehensive KQL cheat sheet. Query VMs, NICs, disks, and more with practical examples and copy-paste queries."
tags: ["Azure", "KQL", "Resource Graph", "PowerShell"]
cover: "/static/images/hero/kql-cheat-sheet.png"
---

# KQL Cheat Sheet for Azure Admins: Azure Resource Graph (VMs, NICs, Disks)

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

## Troubleshooting Common Errors

**Query timeout:** Add `| take 100` to limit results while testing
**JSON parsing errors:** Use `tostring()` consistently when extracting from `properties`
**Join failures:** Verify the join keys match exactly (case-sensitive)
**Empty results:** Check resource type spelling: `"microsoft.compute/virtualmachines"` (all lowercase)

## Tips for Beginners

- **Run Queries:** Use Azure Portal > Resource Graph Explorer for quick access
- **Parse JSON:** Use `tostring` or `parse_json` for properties and tags
- **Test Small:** Add `take 10` to preview results
- **Schema:** Check table/column details in Resource Graph Explorer's left pane
- **Performance:** Filter early with `where type == ...` to reduce data
- **Limitations:** Resource Graph is for metadata only. For metrics (e.g., CPU, disk IOPS), use Log Analytics (`AzureMetrics`)

---

## Download PDF Version

Want this cheat sheet as a PDF for easy reference? Enter your email below and I'll send you the complete guide plus bonus queries for security auditing and cost optimization.

<form name="kql-cheat-sheet" method="POST" netlify data-netlify="true" action="/thank-you/">
  
  <div style="margin-bottom: 15px;">
    <label style="display: block; margin-bottom: 5px; font-weight: bold;">Email Address:</label>
    <input type="email" name="email" required style="width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px;">
  </div>
  
  <div style="margin-bottom: 15px;">
    <label style="display: block; margin-bottom: 5px; font-weight: bold;">Name (optional):</label>
    <input type="text" name="name" style="width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px;">
  </div>
  
  <div style="margin-bottom: 15px;">
    <label style="display: block; margin-bottom: 5px; font-weight: bold;">What's your biggest Azure challenge?</label>
    <select name="challenge" style="width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px;">
      <option value="">Select one...</option>
      <option value="cost-management">Cost management and optimization</option>
      <option value="resource-inventory">Resource inventory and governance</option>
      <option value="security-compliance">Security and compliance</option>
      <option value="automation">Automation and scripting</option>
      <option value="other">Other</option>
    </select>
  </div>
  
  <button type="submit" style="background: #0066cc; color: white; padding: 12px 24px; border: none; border-radius: 4px; cursor: pointer; font-size: 16px;">
    📧 Send Me the PDF + Bonus Queries
  </button>
</form>

---

**Questions about KQL or need help with a specific query?** Email me at [your-email] or find more Azure insights at [azure-noob.com](https://azure-noob.com).

*KQL Cheat Sheet v1.0 - More Azure tutorials and guides available at azure-noob.com*