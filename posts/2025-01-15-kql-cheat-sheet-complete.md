---
title: 'KQL Cheat Sheet: Getting Started with Azure Resource Graph'
date: 2025-01-15
modified: 2025-12-24
summary: 'Essential KQL reference for Azure admins: 15 fundamental queries for VM inventory, resource discovery, and basic troubleshooting. Start learning Azure Resource Graph queries today.'
tags:
- Azure
- Cheat Sheet
- KQL
- Log Analytics
- Query Language
- Resource Graph
cover: /static/images/hero/kql-cheat-sheet.png
hub: governance
faq_schema: true
related_posts:
  - azure-resource-tags-guide
  - azure-tag-governance-policy
  - azure-policy-reality-check
---

# KQL Cheat Sheet: Getting Started with Azure Resource Graph

This guide is part of our [Azure Governance hub](/hub/governance/) covering policy enforcement, compliance frameworks, and enterprise controls.

> **Note:** No Azure certification teaches KQL for operational queries. The AZ-104 exam shows you two sample queries. That's it. No Resource Graph training. No joins. No performance optimization. Nothing about the queries you'll actually write daily.
>
> I wrote about this gap: [The Azure Role Microsoft Forgot to Certify](/blog/azure-reporting-role-microsoft-should-create/). Until Microsoft fixes this, here's the KQL guide you need.

---

## What is KQL?

Kusto Query Language (KQL) is the query language for Azure Resource Graph, Log Analytics, and Microsoft Sentinel. If you manage Azure resources, you need to know KQL.

This cheat sheet focuses on **Azure Resource Graph** - querying your Azure infrastructure metadata to inventory resources, check configurations, and troubleshoot issues.

## Getting Started

**Where to Run:** Azure Portal > Resource Graph Explorer (search "resource-graph" in the portal).

**Key Tables:**
- `Resources`: Contains all Azure resources (VMs, NICs, disks, storage, etc.)
- `ResourceContainers`: Contains subscriptions and resource groups

**Basic Query Structure:** Start with a table name, pipe (`|`) to operators like `where`, `join`, or `project`.

**Example:**
```kql
Resources
| where type == "microsoft.compute/virtualmachines"
| project name, location, resourceGroup
```

---

## Your First 3 Queries

### 1. List All Your VMs

```kql
Resources
| where type == "microsoft.compute/virtualmachines"
| project name, location, resourceGroup
```

**What it does:** Shows every VM across all your subscriptions.

---

### 2. Find VMs in a Specific Resource Group

```kql
Resources  
| where type == "microsoft.compute/virtualmachines"
| where resourceGroup == "Production-RG"
| project name, location
```

**What it does:** Filters to VMs in one resource group only.

---

### 3. Count VMs by Location

```kql
Resources
| where type == "microsoft.compute/virtualmachines" 
| summarize count() by location
```

**What it does:** Shows how many VMs you have in each Azure region.

---

## Core KQL Concepts

### Tables = Your Data Sources

Think of tables like Excel sheets - each contains different types of data:
- `Resources` = all your Azure resources
- `ResourceContainers` = subscriptions and resource groups

### Where = Your Filter

Like Excel filters - narrows down your data:
```kql
| where type == "microsoft.compute/virtualmachines"
| where location == "eastus"
```

**Always filter early for better performance.**

### Project = Your Columns

Selects which columns to display:
```kql
| project name, location, resourceGroup
```

Keeps output clean and focused.

### Summarize = Aggregations

Count, sum, or group your data:
```kql
| summarize count() by location
| summarize avg(properties.diskSizeGB) by resourceGroup
```

---

## 15 Essential Queries

### Query 1: List All VMs

```kql
Resources
| where type == "microsoft.compute/virtualmachines"
| project name, location, resourceGroup
```

---

### Query 2: List All Storage Accounts

```kql
Resources
| where type == "microsoft.storage/storageaccounts"
| project name, location, resourceGroup
```

---

### Query 3: Find Resources by Tag

```kql
Resources
| where tags["Environment"] == "Production"
| project name, type, resourceGroup
```

---

### Query 4: Count Resources by Type

```kql
Resources
| summarize count() by type
| order by count_ desc
```

---

### Query 5: List All Network Interfaces

```kql
Resources
| where type == "microsoft.network/networkinterfaces"
| project name, location, resourceGroup
```

---

### Query 6: Find Untagged Resources

```kql
Resources
| where type in ("microsoft.compute/virtualmachines", "microsoft.storage/storageaccounts")
| where isnull(tags) or array_length(bag_keys(tags)) == 0
| project name, type, resourceGroup
```

---

### Query 7: List All Managed Disks

```kql
Resources
| where type == "microsoft.compute/disks"
| project name, location, resourceGroup
```

---

### Query 8: Count Resources by Location

```kql
Resources
| summarize count() by location
| order by count_ desc
```

---

### Query 9: Find VMs with Specific OS

```kql
Resources
| where type == "microsoft.compute/virtualmachines"
| extend OSType = tostring(properties.storageProfile.osDisk.osType)
| where OSType == "Linux"
| project name, OSType, resourceGroup
```

---

### Query 10: List Public IP Addresses

```kql
Resources
| where type == "microsoft.network/publicipaddresses"
| project name, location, resourceGroup
```

---

### Query 11: Find Large Disks (>100GB)

```kql
Resources
| where type == "microsoft.compute/disks"
| extend DiskSizeGB = toint(properties.diskSizeGB)
| where DiskSizeGB > 100
| project name, DiskSizeGB, resourceGroup
```

---

### Query 12: List All Resource Groups

```kql
ResourceContainers
| where type == "microsoft.resources/resourcegroups"
| project name, location
```

---

### Query 13: Count VMs by Resource Group

```kql
Resources
| where type == "microsoft.compute/virtualmachines"
| summarize VMCount = count() by resourceGroup
| order by VMCount desc
```

---

### Query 14: Find Resources in Specific Subscription

```kql
Resources
| where subscriptionId == "your-subscription-id-here"
| summarize count() by type
```

---

### Query 15: Get VM with Network Details

```kql
Resources
| where type == "microsoft.compute/virtualmachines"
| extend NetworkInterfaceId = tostring(properties.networkProfile.networkInterfaces[0].id)
| project name, NetworkInterfaceId, resourceGroup
```

---

## What You've Learned

You now know how to:
- ✅ Query Azure Resource Graph
- ✅ Filter resources by type, location, tags
- ✅ Count and aggregate resources
- ✅ Find untagged resources
- ✅ Extract basic properties from resources

---

## 🚀 Want the Complete KQL Library?

This free guide covers the **fundamentals** - 15 essential queries to get started.

**Ready for production-level Azure administration?** 

### Get the Complete KQL Query Library ($29)

**What's included:**
- ✅ **48 production-tested queries** (vs 15 basic queries here)
- ✅ **Advanced joins** - Link VMs to NICs, disks, subnets, subscriptions
- ✅ **Performance optimization guide** - Query 31,000+ resources efficiently
- ✅ **SQL to KQL translation** - For SQL developers learning KQL
- ✅ **Case-insensitive tag handling** - Handles tag variations automatically
- ✅ **Power state detection** - Show IPs only for running VMs
- ✅ **Real production scenarios** - From managing enterprise-scale Azure
- ✅ **JSON query files** - Copy-paste ready for immediate use
- ✅ **Complete reference guide** - All queries organized by category
- ✅ **Troubleshooting guide** - Fix common KQL errors
- ✅ **Future updates included** - Get new queries as Azure evolves

**Used in production managing:**
- 44 Azure subscriptions
- 31,000+ resources
- Enterprise-scale environments

### Why Upgrade?

**This free guide teaches you KQL basics** → Get started in 30 minutes

**The complete library gives you production-ready queries** → Save 10+ hours/month

**Price: $29** (one-time purchase, instant download)

[Get the Complete KQL Library →](#)

*Money-back guarantee if it doesn't save you 2+ hours in the first week.*

---

## Additional Resources

- [KQL Quick Reference (Microsoft)](https://docs.microsoft.com/en-us/azure/data-explorer/kql-quick-reference)
- [Azure Resource Graph Documentation](https://docs.microsoft.com/en-us/azure/governance/resource-graph/)
- [More Azure insights at azure-noob.com](https://azure-noob.com)

---

### Azure Admin Starter Kit (Free Download)

Get my complete Azure admin toolkit: KQL cheat sheet, 50 Windows + 50 Linux commands, and an Azure RACI template in one free bundle.

[Get the Starter Kit →](/blog/starter-kit/)

---

*Want to learn more about Azure governance, cost management, and operations? Visit [azure-noob.com](https://azure-noob.com) for practical guides based on real enterprise experience.*
