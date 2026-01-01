---
title: 'KQL Cheat Sheet for Azure Migration Discovery: 48 Production-Tested Queries'
date: 2025-01-15
modified: 2025-12-28
summary: 'Complete KQL reference for Azure Resource Graph: 15 free fundamental queries + migration discovery section. Auto-fill 25 of 55 migration questions with KQL. Tested on 31,000+ resources across 44 subscriptions.'
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

---

> **📥 Want this as a PDF?** Download the free KQL cheat sheet PDF with all 15 essential queries formatted for printing and offline reference.
> 
> [Download Free KQL Cheat Sheet PDF →](/static/downloads/kql-query-library.pdf)

---

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

<div style="background: linear-gradient(135deg, #0078d4 0%, #005a9e 100%); padding: 2.5rem; border-radius: 8px; text-align: center; color: white; margin: 3rem 0;">
  <h2 style="color: white; margin-top: 0; font-size: 2rem;">🔒 Enterprise KQL Library: Migration Discovery Queries</h2>
  <p style="font-size: 1.15rem; margin: 1rem 0 1.5rem; line-height: 1.6;">
    The 15 queries above cover the <strong>fundamentals</strong>.<br>
    Ready for <strong>production-level migration discovery</strong>?
  </p>
  <p style="font-size: 1.1rem; margin-bottom: 2rem;">
    Join <strong>500+ Azure Architects</strong> and get the <strong>47-Query Enterprise Library</strong> in a searchable PDF + my weekly operations brief.
  </p>
  
  <form action="https://app.kit.com/forms/8896829/subscriptions" method="post" style="max-width: 450px; margin: 0 auto; display: flex; gap: 0.75rem; flex-wrap: wrap; justify-content: center;">
    <input type="email" 
           name="email_address" 
           placeholder="your@email.com" 
           required 
           style="flex: 1; min-width: 250px; padding: 1rem; border: none; border-radius: 6px; font-size: 1rem; color: #333;">
    <button type="submit" 
            style="padding: 1rem 2rem; background: white; color: #0078d4; border: none; border-radius: 6px; font-weight: 700; cursor: pointer; white-space: nowrap; font-size: 1rem;">
      Get Enterprise Library
    </button>
  </form>
  
  <p style="margin: 1.5rem 0 0; font-size: 0.9rem; opacity: 0.95;">
    ✔️ 47 production-tested queries • ✔️ Migration discovery workflows • ✔️ Advanced joins & aggregations<br>
    <span style="font-size: 0.85rem; opacity: 0.9;">Instant PDF delivery • No spam • Unsubscribe anytime</span>
  </p>
</div>

## 🚀 KQL for Migration Discovery (Preview)

**Before you touch Azure Migrate**, you need accurate inventory data. These queries answer the 55 questions in the [Azure Migration Assessment Pro](/products/) without guesswork.

<em style="opacity: 0.8;">Note: The complete migration discovery queries (15+ additional queries) are included in the Enterprise Library above. Below is a preview of what's included.</em>

### Critical Migration Questions KQL Can Answer:

**Infrastructure Discovery:**
```kql
// Question #10-12: Platform, OS, and Server Count
Resources
| where type =~ 'microsoft.compute/virtualmachines'
| extend osType = properties.storageProfile.osDisk.osType
| extend osVersion = properties.storageProfile.imageReference.sku
| summarize 
    TotalVMs = count(),
    Windows = countif(osType =~ 'Windows'),
    Linux = countif(osType =~ 'Linux')
    by osType, osVersion
| order by TotalVMs desc
```

**Dependency Mapping:**
```kql
// Question #15-16: Load Balancer Dependencies & Public Exposure
Resources
| where type =~ 'microsoft.network/loadbalancers'
| extend frontendConfig = properties.frontendIPConfigurations
| mvexpand frontendConfig
| extend 
    publicIP = frontendConfig.properties.publicIPAddress.id,
    privateIP = frontendConfig.properties.privateIPAddress
| project name, resourceGroup, 
    hasPublicIP = isnotnull(publicIP),
    privateIP, location
```

**Cost Discovery:**
```kql
// Question #43-44: Resource Count by Application
Resources
| where type =~ 'microsoft.compute/virtualmachines'
    or type =~ 'microsoft.storage/storageaccounts'
    or type =~ 'microsoft.network/virtualnetworks'
| extend appName = tostring(tags['Application'])
| where isnotempty(appName)
| summarize 
    VMs = countif(type =~ 'microsoft.compute/virtualmachines'),
    Storage = countif(type =~ 'microsoft.storage/storageaccounts'),
    TotalResources = count()
    by appName, resourceGroup
| order by TotalResources desc
```

### 🎯 The Migration Discovery Workflow:

1. **Run these queries** → Answers 25 of 55 migration questions
2. **Export to Excel** → Paste into [Migration Assessment Pro](/products/)
3. **Auto-fill confidence** → High (KQL-verified), not Low (guessed)
4. **Remaining 30 questions** → Manual discovery (app owners, licensing docs)

**Time saved:** 10-15 hours per application

### Want All 48 Migration Discovery Queries?

The [Complete KQL Query Library ($19)](https://davidnoob.gumroad.com/l/hooih) includes:
- ✅ **Dependency mapping queries** - Find load balancers, VNets, NSGs per app
- ✅ **Licensing audits** - SQL Server, Windows, Red Hat detection
- ✅ **Cost allocation** - Tag-based resource grouping for cost estimates
- ✅ **Security assessment** - Encryption status, public exposure, NSG rules

**Maps directly to the Migration Assessment Pro questionnaire.**

---

## 🚀 Want the Complete KQL Library?

This free guide covers the **fundamentals** - 15 essential queries to get started.

**Ready for production-level Azure administration?** 

### Get the Complete KQL Query Library ($19)

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

**Price: $19** (one-time purchase, instant download)

[Get the Complete KQL Library →](https://davidnoob.gumroad.com/l/hooih)

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
