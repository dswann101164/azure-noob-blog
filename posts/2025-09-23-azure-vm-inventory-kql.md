---
title: "From Raw Data to Actionable Insights: Mastering Azure VM Inventory with KQL"
date: 2025-09-23
summary: "Build a single KQL query that inventories every VM, cleans up OS details, and assigns the right patching workflow—Intune, Azure Update Manager, or Linux package managers."
tags: ["Azure", "KQL", "Update Management", "Intune", "VM Inventory"]
cover: "/static/images/hero/azure-vm-inventory-kql.png"
---

## What problem are we solving?

As an Azure administrator, your environment is a sprawling landscape of Windows Servers, Linux boxes, and Windows clients. The challenge: **Which ones are patched by Azure Update Manager and which fall under Intune?**  
Without a unified view, you risk compliance gaps and manual guesswork. This post shows how a single KQL query can deliver clarity and save hours of troubleshooting.

---

## Why I Wrote This Query

I built this query to **prepare my environment for Azure Update Manager (AUM)**.  
AUM is powerful for managing Windows Server patching, but it does **not support Windows 10/11 clients or Databricks VMs**. That means I needed a way to:

- Inventory *every* VM across subscriptions  
- Clearly separate the workloads AUM can handle (Windows Server)  
- Automatically flag those that must be handled by **Intune** (Windows clients)  
- Exclude or classify special cases like **Databricks** and Linux workloads  

By setting this foundation, I could confidently plan patching strategy across the tenant and avoid surprises when adopting AUM.

---

## The Goal: A Unified VM Report

Our objective is to write one query that:

- Gathers all Azure VMs  
- Enriches with networking and subscription context  
- Classifies OS types into clean names  
- Assigns the correct patching workflow (Intune, AUM, or Linux PM)  
- Surfaces useful metadata like Owner, CostCenter, Application  

---

## Breaking Down the Query

### Step 1: Gather Core Ingredients
- Start with all VMs from `Resources`
- Join to NICs for `PrivateIP` and `SubnetId`

### Step 2: Add Human-Readable Context
- Join subscription IDs to `SubscriptionName`

### Step 3: Extend with New Insights
- Parse `VNetName` and `SubnetName`
- Extract OS details (`OSType`, `OSPublisher`, `OSVersion`)
- Add `PowerState`, `CreatedBy`, `CreatedTime`

### Step 4: Apply Logic with `case`
- Build **DetailedOS** (Ubuntu Linux, Windows Server 2022, Windows 11, etc.)
- Assign **RemediationWorkflow**:
  - Windows 10/11 → Intune  
  - Windows Server → Azure Update Manager  
  - Linux → Native package manager  
  - Databricks / others → Investigation  
- Add **AzureUpdateManagerSupported** for clarity

### Step 5: Project a Clean Report
- Select core IDs (`VMName`, `DNSName`, `PrivateIP`)
- Include tags (`Owner`, `CostCenter`, `Application`)
- Keep only the columns you need

### Step 6: Order for Readability
- Sort by `RemediationWorkflow`, then `ResourceGroup`, then `VMName`

---

## The Complete Query

```kusto

Resources
| where type == "microsoft.compute/virtualmachines"
| extend NetworkInterfaceId = tostring(properties.networkProfile.networkInterfaces[0].id)
| join kind=leftouter (
    Resources
    | where type == "microsoft.network/networkinterfaces"
    | project
        NetworkInterfaceId = id,
        PrivateIP = tostring(properties.ipConfigurations[0].properties.privateIPAddress),
        SubnetId = tostring(properties.ipConfigurations[0].properties.subnet.id)
) on NetworkInterfaceId
| join kind=leftouter (
    ResourceContainers
    | where type == "microsoft.resources/subscriptions"
    | project subscriptionId, SubscriptionName = name
) on subscriptionId
| extend
    VNetName = tostring(split(SubnetId, "/")[8]),
    SubnetName = tostring(split(SubnetId, "/")[10]),
    OSType      = tostring(properties.storageProfile.osDisk.osType),
    OSPublisher = tostring(properties.storageProfile.imageReference.publisher),
    OSProduct   = tostring(properties.storageProfile.imageReference.offer),
    OSVersion   = tostring(properties.storageProfile.imageReference.sku),
    PowerState  = tostring(properties.extended.instanceView.powerState.displayStatus),
    CreatedTime = todatetime(properties.timeCreated),
    CreatedBy   = tostring(properties.createdBy.userPrincipalName)
| extend
    DetailedOS = case(
        OSType == "Linux" and OSPublisher == "Canonical", "Ubuntu Linux",
        OSType == "Linux" and OSPublisher == "RedHat", "Red Hat Linux",
        OSType == "Linux", strcat("Linux - ", OSPublisher),
        OSProduct contains "WindowsServer" and OSVersion contains "2022", "Windows Server 2022",
        OSProduct contains "WindowsServer" and OSVersion contains "2019", "Windows Server 2019",
        OSProduct contains "WindowsServer" and OSVersion contains "2016", "Windows Server 2016",
        OSProduct contains "WindowsServer", strcat("Windows Server - ", OSVersion),
        OSProduct contains "Windows-10" or OSProduct contains "windows-10", strcat("Windows 10 - ", OSVersion),
        OSProduct contains "Windows-11" or OSProduct contains "windows-11", strcat("Windows 11 - ", OSVersion),
        OSProduct contains "Databricks", "Azure Databricks VM",
        OSType == "Windows", strcat("Windows - ", OSProduct),
        "Unknown"
    ),
    RemediationWorkflow = case(
        OSProduct contains "Windows-10" or OSProduct contains "windows-10", "Updated by Intune",
        OSProduct contains "Windows-11" or OSProduct contains "windows-11", "Updated by Intune",
        OSProduct contains "WindowsServer", "Azure Update Manager",
        OSProduct contains "Databricks", "Excluded - Databricks",
        OSType == "Linux", "Linux Package Manager",
        OSType == "Windows", "Investigation Required - Windows",
        "Investigation Required"
    ),
    AzureUpdateManagerSupported = case(
        OSProduct contains "WindowsServer", "Yes",
        OSProduct contains "Windows-10" or OSProduct contains "windows-10", "No - Win10 client",
        OSProduct contains "Windows-11" or OSProduct contains "windows-11", "No - Win11 client",
        OSProduct contains "Databricks", "No - Databricks VM",
        OSType == "Linux", "No - Linux",
        OSType == "Windows", "No - Other Windows Client",
        "Unknown"
    )
| project
    VMName = name,
    DNSName = strcat(name, ".snv.net"),
    PrivateIP,
    ResourceGroup = resourceGroup,
    SubscriptionName,
    SubscriptionId = subscriptionId,
    Location = location,
    VNetName,
    SubnetName,
    OSType,
    OSPublisher,
    OSProduct,
    OSVersion,
    DetailedOS,
    PowerState,
    CreatedTime,
    CreatedBy,
    RemediationWorkflow,
    AzureUpdateManagerSupported,
    VMSize = tostring(properties.hardwareProfile.vmSize),
    CostCenter = tostring(tags["CostCenter"]),
    Owner = tostring(tags["Owner"]),
    Environment = tostring(tags["Environment"]),
    Department = tostring(tags["Department"]),
    Application = tostring(tags["Application"]),
    AllTags = tags
| order by RemediationWorkflow, ResourceGroup, VMName asc

## Why This Matters
By using KQL this way, you move from reactive troubleshooting to proactive governance.
This query:
- Eliminates manual patch-tracking  
- Makes AUM adoption smooth by pre-classifying unsupported systems  
- Provides clarity on Intune vs. AUM vs. Linux responsibilities  
- Surfaces Databricks as out-of-scope for AUM  
- Serves as a foundation for dashboards and alerts 