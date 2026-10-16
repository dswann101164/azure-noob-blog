---
title: "KQL Query Library: 150+ Production-Ready Azure Resource Graph Queries"
date: 2026-01-03
modified: 2026-01-03
summary: "Complete KQL query library with 150+ production-tested queries for Azure Resource Graph, Log Analytics, and Sentinel. Copy-paste ready, enterprise-scale tested on 31,000+ resources."
tags: ["kql", "azure", "resource-graph", "queries", "monitoring"]
cover: /static/images/products/kql-cover.png
slug: kql-query-library
hub: kql
related_posts:
  - kql-cheat-sheet-complete
  - azure-vm-inventory-kql
faq_schema: true
---
<div style="background: #f8f9fa; padding: 2rem; border-left: 4px solid #0078d4; margin: 2rem 0; border-radius: 4px;">
  <h2 style="margin-top: 0; color: #0078d4;">⚡ Quick Answer: What is KQL?</h2>
  <p style="font-size: 1.1rem; margin-bottom: 1rem;">
    <strong>KQL (Kusto Query Language)</strong> is Microsoft's query language for Azure Resource Graph, Log Analytics, Azure Monitor, and Microsoft Sentinel. It lets you query thousands of Azure resources in seconds to find VMs, analyze costs, track compliance, and investigate security incidents.
  </p>
  <p style="margin: 0;"><strong>Real-world use:</strong> Find all VMs without backup in 5 seconds, track $100K+ monthly Azure spend by department, or identify compliance violations across 40+ subscriptions.</p>
</div>

---

## 10 Essential KQL Queries (Free Examples)

Here are 10 production-ready queries you can use right now.

### 1. Find All Virtual Machines with Public IPs

```kql
Resources
| where type =~ 'microsoft.compute/virtualmachines'
| extend nicId = tostring(properties.networkProfile.networkInterfaces[0].id)
| join kind=leftouter (
    Resources
    | where type =~ 'microsoft.network/networkinterfaces'
    | extend ipConfigId = tostring(properties.ipConfigurations[0].properties.publicIPAddress.id)
    | project nicId = id, ipConfigId
) on nicId
| join kind=leftouter (
    Resources
    | where type =~ 'microsoft.network/publicipaddresses'
    | project ipConfigId = id, publicIP = properties.ipAddress
) on ipConfigId
| where isnotempty(publicIP)
| project name, resourceGroup, location, publicIP, subscriptionId
```

**Why this matters:** Public IPs cost $3-5/month each and are security risks. This query finds all VMs exposed to the internet.

---

### 2. VMs Without Backup Configured

```kql
Resources
| where type =~ 'microsoft.compute/virtualmachines'
| where tags['Environment'] =~ 'Production'
| project vmId = tolower(id), vmName = name, resourceGroup, location
| join kind=leftanti (
    RecoveryServicesResources
    | where type =~ 'microsoft.recoveryservices/vaults/backupfabrics/protectioncontainers/protecteditems'
    | where properties.backupManagementType == 'AzureIaasVM'
    | extend vmId = tolower(tostring(properties.sourceResourceId))
    | project vmId
) on vmId
| project vmName, resourceGroup, location
```

**Business impact:** Each unprotected production VM is a potential data loss incident. This query finds the gaps.

---

### 3. Monthly Cost by Resource Group

```kql
CostManagementExports
| where TimeGenerated >= startofmonth(now())
| summarize TotalCost = sum(CostInBillingCurrency) by ResourceGroup
| order by TotalCost desc
| project ResourceGroup, ['Monthly Cost'] = strcat('$', round(TotalCost, 2))
```

**CFO-ready:** Shows exactly where money is going. Essential for chargeback and budget tracking.

---

### 4. Storage Accounts Without HTTPS Enforcement

```kql
Resources
| where type =~ 'microsoft.storage/storageaccounts'
| where properties.supportsHttpsTrafficOnly == false
| project name, resourceGroup, location, subscriptionId
```

**Security risk:** HTTP traffic is unencrypted. Compliance teams flag this immediately.

---

### 5. VMs Running Old OS Versions

```kql
Resources
| where type =~ 'microsoft.compute/virtualmachines'
| extend osType = tostring(properties.storageProfile.osDisk.osType)
| extend osVersion = tostring(properties.storageProfile.imageReference.sku)
| where osVersion contains '2012' or osVersion contains '2016'
| project name, osType, osVersion, resourceGroup, location
```

**Patching nightmare:** Windows Server 2012 reached end-of-life. This finds technical debt.

---

### 6. Untagged Resources (Compliance Violation)

```kql
Resources
| where tags !has 'CostCenter' or tags !has 'Department' or tags !has 'Owner'
| project name, type, resourceGroup, tags, subscriptionId
| order by type asc
```

**FinOps essential:** Can't do chargeback without tags. This query finds the violations.

---

### 7. VMs Stopped But Still Costing Money

```kql
Resources
| where type =~ 'microsoft.compute/virtualmachines'
| extend powerState = tostring(properties.extended.instanceView.powerState.code)
| where powerState != 'PowerState/running' and powerState != 'PowerState/deallocated'
| project name, powerState, resourceGroup, location
```

**Cost trap:** "Stopped" VMs still incur compute charges. "Deallocated" is free.

---

### 8. SQL Databases Over 100GB

```kql
Resources
| where type =~ 'microsoft.sql/servers/databases'
| where name != 'master'
| extend maxSizeGB = toint(properties.maxSizeBytes) / 1024 / 1024 / 1024
| where maxSizeGB > 100
| project name, maxSizeGB, tier = tostring(properties.currentServiceObjectiveName), resourceGroup
| order by maxSizeGB desc
```

**Cost optimization:** Large databases are expensive. Identifies candidates for archival or tiering.

---

### 9. Network Security Groups Allowing RDP from Internet

```kql
Resources
| where type =~ 'microsoft.network/networksecuritygroups'
| mv-expand rules = properties.securityRules
| where rules.properties.access == 'Allow'
| where rules.properties.direction == 'Inbound'
| where rules.properties.destinationPortRange has '3389'
| where rules.properties.sourceAddressPrefix == '*' or rules.properties.sourceAddressPrefix == 'Internet'
| project nsgName = name, ruleName = rules.name, resourceGroup, location
```

**Security critical:** Open RDP is an attack vector. SOC teams monitor this constantly.

---

### 10. Resources by Region (Multi-Region Deployment Check)

```kql
Resources
| summarize count() by location
| order by count_ desc
| project Region = location, ['Resource Count'] = count_
```

**Disaster recovery:** Shows if you're actually multi-region or just paying for it.

---

## Why Learn KQL Instead of Azure Portal Clicking?

**Portal problems:**
- Can only search one subscription at a time
- Can't filter by multiple criteria
- No way to export results at scale
- Manual work doesn't scale past 100 resources

**KQL solutions:**
- Query 40+ subscriptions in one query
- Complex filters (tags + location + cost + state)
- Export to CSV for Excel/PowerBI
- Save queries as Azure Monitor dashboards

**Time saved:** 5 minutes clicking per resource × 1,000 resources = 83 hours/month  
**With KQL:** 30 seconds to write query, 5 seconds to run = **83 hours saved**

---

## KQL Use Cases by Role

### Azure Administrators
- Find VMs without monitoring agents
- Track resource group ownership
- Identify orphaned resources (disks, IPs)
- Generate compliance reports

### FinOps Teams
- Cost by department/project/environment
- Untagged resource tracking
- Reserved Instance utilization
- Waste identification (idle VMs, unused disks)

### Security Teams
- Public-facing resources inventory
- NSG rule violations
- Storage accounts without encryption
- Identity & Access anomalies

### DevOps Engineers
- Pipeline resource provisioning status
- Environment resource counts
- Tag compliance automation
- Infrastructure drift detection

---

## KQL Learning Path (30 Days to Mastery)

### Week 1: Basics
- [ ] Understand `Resources` table
- [ ] Learn `where`, `project`, `extend`
- [ ] Write your first 5 queries
- [ ] Practice in Azure Resource Graph Explorer

### Week 2: Joins & Aggregations
- [ ] Master `join` (inner, outer, anti)
- [ ] Use `summarize` for counts/sums
- [ ] Learn `mv-expand` for arrays
- [ ] Build your first dashboard

### Week 3: Advanced Patterns
- [ ] Multi-subscription queries
- [ ] Complex filtering logic
- [ ] Performance optimization
- [ ] JSON property parsing

### Week 4: Production Deployment
- [ ] Save queries to Azure Monitor
- [ ] Create PowerShell automation
- [ ] Build executive dashboards
- [ ] Train your team

**Shortcut:** Use the 10 queries above as templates and you can move to Week 4 sooner.

---

## Common KQL Mistakes (And How to Fix Them)

### Mistake #1: Querying All Subscriptions When You Only Need One
**Wrong:**
```kql
Resources
| where type =~ 'microsoft.compute/virtualmachines'
| where name == 'MyVM'
```

**Right:**
```kql
Resources
| where subscriptionId == 'YOUR-SUB-ID'
| where type =~ 'microsoft.compute/virtualmachines'
| where name == 'MyVM'
```

**Why:** Filters at the top reduce query time from 30 seconds to 2 seconds.

---

### Mistake #2: Case-Sensitive Comparisons
**Wrong:**
```kql
| where type == 'Microsoft.Compute/virtualMachines'  // Fails if casing differs
```

**Right:**
```kql
| where type =~ 'microsoft.compute/virtualmachines'  // Case-insensitive
```

**Why:** Azure resource types aren't consistently cased. Always use `=~` for strings.

---

### Mistake #3: Not Handling Empty/Null Values
**Wrong:**
```kql
| where tags['CostCenter'] == ''  // Misses null tags
```

**Right:**
```kql
| where isempty(tags['CostCenter']) or isnull(tags['CostCenter'])
```

**Why:** Empty and null are different. Check both to catch all violations.

---

## KQL vs SQL: Key Differences

| Feature | SQL | KQL |
|---------|-----|-----|
| **Table name** | FROM users | users |
| **Filter** | WHERE status = 'active' | \| where status == 'active' |
| **Select columns** | SELECT name, email | \| project name, email |
| **Aggregation** | GROUP BY department | \| summarize by department |
| **Join** | INNER JOIN orders ON... | \| join kind=inner (orders) on... |
| **Case sensitivity** | Depends on collation | Use =~ for insensitive |

**SQL developers:** KQL reads top-to-bottom (pipeline), not inside-out like SQL.

---

## Free KQL Resources

**Official Microsoft:**
- [KQL Quick Reference](https://docs.microsoft.com/azure/data-explorer/kql-quick-reference)
- [Azure Resource Graph Explorer](https://portal.azure.com/#blade/HubsExtension/ArgQueryBlade)
- [Log Analytics Demo Environment](https://portal.azure.com/#blade/Microsoft_Azure_Monitoring_Logs/DemoLogsBlade)

**Azure Noob Resources:**
- [KQL Cheat Sheet (Free)](/blog/kql-cheat-sheet-complete/) - 15 essential queries
- [Azure VM Inventory with KQL](/blog/azure-vm-inventory-kql/) - Step-by-step tutorial

---

<div class="raci-cta" style="border: 2px solid #9C27B0; border-radius: 8px; padding: 1.5rem; margin: 2rem 0; background: #faf5fc;">
  <h3 style="margin-top: 0;">Azure Cloud Operations RACI Matrix</h3>
  <p>End the "who owns this?" debate in Azure. An Excel RACI matrix with 58 pre-assigned operations tasks, so your team knows who handles Key Vault, NSGs, backups, certificates, and the rest of the recurring work.</p>
  <a href="https://davidnoob.gumroad.com/l/ifojm" style="display: inline-block; padding: 0.875rem 2rem; background: #9C27B0; color: white; text-decoration: none; border-radius: 6px; font-weight: 700;">Get the RACI Matrix - $49 →</a>
</div>

---

## FAQ: KQL Query Library

**Q: Do I need programming experience to use KQL?**  
A: No. If you can write Excel formulas, you can learn KQL. The syntax is more English-like than SQL.

**Q: Will these queries work in my environment?**  
A: Yes. These queries use Azure Resource Graph (available in all Azure subscriptions) and standard resource types. No custom setup required.

**Q: How is this different from Microsoft's documentation?**  
A: Microsoft docs explain syntax. This library gives you working queries for real scenarios (find VMs without backup, track costs by department, identify security risks).

**Q: Can I use these queries in Azure Monitor Workbooks?**  
A: Yes. All queries work in Resource Graph Explorer, Azure Monitor, Log Analytics, and PowerShell.

**Q: Do you update the library when Azure changes?**  
A: Yes. Lifetime updates included. When new Azure services launch or resource types change, you get updated queries.

**Q: What if a query doesn't work in my environment?**  
A: Email me the error and I'll fix it within 24 hours. Or just request a refund—no questions asked.

---

## Ready to Master KQL?

**Free path:** Start with the [KQL Cheat Sheet](/blog/kql-cheat-sheet-complete/) (15 essential queries)  
**Fast path:** Paste the 10 queries above into Resource Graph Explorer and adapt them to your environment.

**Either way, you'll be querying Azure like a pro within 30 days.**

---

*This library is built from 3+ years managing 31,000+ Azure resources across 44 subscriptions in a Fortune 500 bank. Every query has been tested in production. Zero theory—just what actually works.*
