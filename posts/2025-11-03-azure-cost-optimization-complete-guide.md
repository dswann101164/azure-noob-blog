---
title: 'Azure Cost Optimization 2025: The Complete Framework'
date: 2025-11-03
summary: A real-world guide to optimizing Azure costs using rightsizing, automation,
  cleanup, governance, tags, and financial accountability.
tags:
- Azure
- FinOps
- Cost Optimization
- Automation
- Governance
cover: /static/images/hero/azure-cost-optimization-guide.png
slug: azure-cost-optimization-complete-guide
hub: finops
related_posts:
  - azure-finops-complete-guide
  - azure-resource-tags-guide
  - azure-tag-governance-policy
  - cloud-migration-reality-check
  - azure-chargeback-tags-model
---

This isn't another "turn off unused VMs" guide.

This is the **complete framework** I've used to reduce Azure spend by 30-40% across multiple enterprisesâ€”without breaking production, without political fallout, and with Finance actually thanking me.

This guide is part of our [Azure FinOps hub](/hub/finops/) covering cost management, chargeback models, and tag governance at enterprise scale.

It's long. It's detailed. **Bookmark it**.

---

## Table of Contents
1. [The Framework Overview](#the-framework-overview)
2. [Phase 1: Establish Baseline](#phase-1-establish-baseline)
3. [Phase 2: Tag Everything](#phase-2-tag-everything)
4. [Phase 3: Context-Aware Analysis](#phase-3-context-aware-analysis)
5. [Phase 4: Optimization Execution](#phase-4-optimization-execution)
6. [Phase 5: Continuous Governance](#phase-5-continuous-governance)
7. [Stakeholder Management](#stakeholder-management)
8. [Common Pitfalls](#common-pitfalls)

---

## The Framework Overview

Real Azure cost optimization requires five phases:

| Phase | Focus | Timeline | Expected Impact |
|-------|-------|----------|-----------------|
| Baseline | Understand current state | Week 1-2 | 0% savings (data gathering) |
| Tagging | Add business context | Week 3-4 | 0% savings (foundation) |
| Analysis | Find optimization targets | Week 5-6 | 5-10% quick wins |
| Execution | Implement changes | Ongoing | 20-30% over 6 months |
| Governance | Prevent regression | Ongoing | Sustain savings |

**Critical Point**: Phases 1-2 produce zero savings but are mandatory. Skip them and you'll optimize the wrong things.

---

## Phase 1: Establish Baseline

Before you optimize anything, you need a complete picture of your Azure environment.

### Step 1: Total Spend by Service

```kql
// Get last 90 days of Azure spend by service
AzureCostManagementExports
| where TimeGenerated >= ago(90d)
| summarize TotalCost = sum(CostInBillingCurrency) by ServiceName
| order by TotalCost desc
| take 20
```

This tells you **where the money is actually going**. You'll likely find:
- **Compute**: 40-50% (VMs, App Services, AKS)
- **Storage**: 15-25% (Disks, Blob, File Shares)
- **Networking**: 10-15% (Bandwidth, Load Balancers, VPN)
- **Everything else**: 20-30%

### Step 2: Spend by Subscription

```kql
Resources
| summarize ResourceCount = count() by subscriptionId
| join kind=inner (
    AzureCostManagementExports
    | where TimeGenerated >= ago(30d)
    | summarize MonthlyCost = sum(CostInBillingCurrency) by SubscriptionId
) on $left.subscriptionId == $right.SubscriptionId
| project SubscriptionId = subscriptionId, ResourceCount, MonthlyCost
| order by MonthlyCost desc
```

Identifies **hot zones**â€”subscriptions with highest spend get optimization priority.

### Step 3: Resource Inventory

```kql
Resources
| where type in (
    "microsoft.compute/virtualmachines",
    "microsoft.storage/storageaccounts", 
    "microsoft.compute/disks",
    "microsoft.network/publicipaddresses"
)
| extend 
    ResourceType = tostring(split(type, '/')[1]),
    HasTags = iff(array_length(todynamic(tags)) > 0, "Yes", "No")
| summarize Count = count() by ResourceType, HasTags
| order by Count desc
```

Shows you:
- Total resource counts by type
- How many are **untagged** (the ones you can't analyze properly)

### Step 4: Unused Resource Scan

```kql
// Disks not attached to VMs
Resources
| where type == "microsoft.compute/disks"
| where properties.diskState == "Unattached"
| extend 
    DiskSizeGB = properties.diskSizeGB,
    SKU = properties.sku.name,
    EstimatedMonthlyCost = iff(properties.sku.name startswith "Premium", 
        properties.diskSizeGB * 0.135, 
        properties.diskSizeGB * 0.045)
| project name, resourceGroup, DiskSizeGB, SKU, EstimatedMonthlyCost
| order by EstimatedMonthlyCost desc
```

**Reality check**: This will find your real orphaned disksâ€”not the ones Azure Advisor flags (which are often DR/backup disks).

---

### 🔍 Find the "Zombie" Resources

These are resources that exist but show ZERO metrics for 30 days.

```kusto
// Find "Zombie" Resources (No metrics for 30 days)
// Note: Requires Metrics access
InsightsMetrics
| where TimeGenerated > ago(30d)
| summarize MaxVal = max(Val) by _ResourceId
| where MaxVal == 0
| project _ResourceId
```

---

## Phase 2: Tag Everything

Tags are the **only way** to add business context to Azure resources. Without them, you're optimizing blind.

### The Essential Tag Schema

Every resource needs these six tags (minimum):

```yaml
Environment: Production | UAT | Dev | DR
CostCenter: Finance | IT | Marketing | Sales
Owner: firstname.lastname@company.com
Application: SAP-ERP | CRM | WebPortal
Criticality: Tier1 | Tier2 | Tier3
EOL: YYYY-MM-DD (or "Permanent")
```

### Why These Tags Matter

**Environment**: Tells you which resources can be shut down nights/weekends  
**CostCenter**: Enables chargeback (makes cost someone else's problem)  
**Owner**: Who to ask "do we still need this?"  
**Application**: Groups related resources for impact analysis  
**Criticality**: Defines SLAs and optimization risk tolerance  
**EOL**: Identifies resources scheduled for decommission

### Bulk Tagging Strategy

**Option 1: PowerShell for Resource Groups**
```powershell
# Tag all resources in a resource group
$tags = @{
    "Environment" = "Production"
    "CostCenter" = "Finance"
    "Owner" = "jane.smith@company.com"
    "Application" = "SAP-ERP"
    "Criticality" = "Tier1"
    "EOL" = "Permanent"
}

Get-AzResource -ResourceGroupName "rg-sap-prod" | ForEach-Object {
    Update-AzTag -ResourceId $_.ResourceId -Tag $tags -Operation Merge
}
```

**Option 2: Azure Policy for Enforcement**
```json
{
  "mode": "Indexed",
  "policyRule": {
    "if": {
      "anyOf": [
        {"field": "tags['Environment']", "exists": "false"},
        {"field": "tags['Owner']", "exists": "false"},
        {"field": "tags['CostCenter']", "exists": "false"}
      ]
    },
    "then": {
      "effect": "deny"
    }
  }
}
```

This **prevents** new resources from being created without required tags.

### Tagging Existing Resources

```kql
// Find untagged resources by subscription
Resources
| where tags !has "Environment" or tags !has "Owner"
| summarize UntaggedCount = count() by subscriptionId, type
| order by UntaggedCount desc
```

**Reality**: You'll find hundreds (or thousands) of untagged resources. Prioritize:
1. Resources in high-spend subscriptions
2. Compute resources (VMs, App Services)
3. Storage with high costs

**Don't try to tag everything at once**â€”it's a 6-month project for large enterprises. For the complete tagging strategy including solving the 247 tag variations problem, see our [Azure tagging best practices guide](/blog/azure-resource-tags-guide/) and [tag governance policy implementation](/blog/azure-tag-governance-policy/).

---

## Phase 3: Context-Aware Analysis

Now that you have tags, you can analyze **by business context** instead of generic cloud metrics.

### Analysis 1: Cost by Application

```kql
Resources
| where tags contains "Application"
| extend Application = tostring(tags.Application)
| join kind=leftouter (
    AzureCostManagementExports
    | where TimeGenerated >= ago(30d)
    | summarize MonthlyCost = sum(CostInBillingCurrency) by ResourceId
) on ResourceId
| summarize TotalMonthlyCost = sum(MonthlyCost) by Application
| order by TotalMonthlyCost desc
```

Shows you **which applications cost the most**â€”not which subscriptions or resource types.

### Analysis 2: Dev/Test Overprovisioning

```kql
Resources
| where type == "microsoft.compute/virtualmachines"
| where tags.Environment in ("Dev", "UAT", "Test")
| extend 
    VMSize = properties.hardwareProfile.vmSize,
    IsOversized = iff(
        properties.hardwareProfile.vmSize contains "Standard_D8" or
        properties.hardwareProfile.vmSize contains "Standard_D16" or
        properties.hardwareProfile.vmSize contains "Standard_E",
        true, false
    )
| where IsOversized == true
| project name, resourceGroup, VMSize, Environment = tags.Environment, Owner = tags.Owner
```

**Dev/test environments** are the #1 source of waste in every enterprise I've seen. Nobody needs 16-core VMs for development. This connects directly to our broader [Azure FinOps implementation guide](/blog/azure-finops-complete-guide/) where we cover application-level cost visibility.

### Analysis 3: Resources Past EOL

```kql
Resources
| where tags contains "EOL"
| extend 
    EOLDate = todatetime(tags.EOL),
    DaysPastEOL = datetime_diff('day', now(), todatetime(tags.EOL))
| where DaysPastEOL > 0
| join kind=leftouter (
    AzureCostManagementExports
    | where TimeGenerated >= ago(30d)
    | summarize MonthlyCost = sum(CostInBillingCurrency) by ResourceId
) on ResourceId
| summarize 
    TotalResources = count(),
    TotalMonthlyCost = sum(MonthlyCost),
    ResourceList = make_list(name)
    by Owner = tags.Owner, Application = tags.Application
| order by TotalMonthlyCost desc
```

This finds resources **scheduled for decommission** but still running (and costing money).

### Analysis 4: 24/7 Dev Environments

```kql
Resources
| where type == "microsoft.compute/virtualmachines"
| where tags.Environment in ("Dev", "UAT")
| extend Owner = tags.Owner, Application = tags.Application
| join kind=leftouter (
    AzureCostManagementExports
    | where TimeGenerated >= ago(30d)
    | summarize MonthlyCost = sum(CostInBillingCurrency) by ResourceId
) on ResourceId
| summarize 
    VMCount = count(),
    MonthlyCost = sum(MonthlyCost),
    PotentialSavings = sum(MonthlyCost) * 0.65  // Assume 65% savings with auto-shutdown
    by Owner, Application
| where MonthlyCost > 1000
| order by PotentialSavings desc
```

**Dev/UAT VMs running 24/7** are burning money. Implement auto-shutdown schedules (nights/weekends) for **instant 65% savings**.

---

## Phase 4: Optimization Execution

Now you executeâ€”carefully, with business context.

### Quick Win 1: Delete Orphaned Disks

**Who to ask**: Check the `Owner` tag  
**Risk level**: Low (if you verify backup/DR context first)  
**Expected savings**: $500-$5,000/month depending on environment size

```powershell
# Find and review orphaned disks
$orphanedDisks = Get-AzDisk | Where-Object {$_.ManagedBy -eq $null}

foreach ($disk in $orphanedDisks) {
    Write-Host "Disk: $($disk.Name)"
    Write-Host "  Size: $($disk.DiskSizeGB) GB"
    Write-Host "  SKU: $($disk.Sku.Name)"
    Write-Host "  Owner: $($disk.Tags.Owner)"
    Write-Host "  Application: $($disk.Tags.Application)"
    Write-Host "---"
}

# After verification, delete (one at a time!)
# Remove-AzDisk -ResourceGroupName <rg> -DiskName <name> -Force
```

**NEVER bulk-delete**â€”verify each disk individually with the owner.

### Quick Win 2: Auto-Shutdown Dev/UAT VMs

```powershell
# Apply auto-shutdown to all Dev/UAT VMs
$vms = Get-AzVM | Where-Object {$_.Tags.Environment -in @("Dev", "UAT")}

foreach ($vm in $vms) {
    $properties = @{
        status = "Enabled"
        taskType = "ComputeVmShutdownTask"
        dailyRecurrence = @{
            time = "1900"  # 7 PM shutdown
        }
        timeZoneId = "Eastern Standard Time"
        notificationSettings = @{
            status = "Enabled"
            timeInMinutes = 30
            emailRecipient = $vm.Tags.Owner
        }
        targetResourceId = $vm.Id
    }
    
    New-AzResource `
        -ResourceId ("/subscriptions/{0}/resourceGroups/{1}/providers/Microsoft.DevTestLab/schedules/shutdown-computevm-{2}" -f $vm.Id.Split('/')[2], $vm.ResourceGroupName, $vm.Name) `
        -Properties $properties `
        -Force
}
```

This creates **auto-shutdown schedules** for all dev/UAT VMs with owner notifications.

**Expected savings**: 65% of dev/UAT compute costs (running 40 hours/week instead of 168 hours/week).

### Medium Win: Right-Size Production VMs

**This is where people get burned**â€”don't just blindly downsize.

**Process**:
1. **Identify candidates** (high-spec VMs with low utilization)
2. **Gather 30+ days of metrics** (not 7 daysâ€”that's too short)
3. **Check with the application owner** (understand usage patterns)
4. **Test in UAT first** (never right-size directly in production)
5. **Schedule during maintenance window** (not Tuesday at 2 PM)

```kql
// Find right-sizing candidates
Perf
| where TimeGenerated >= ago(30d)
| where ObjectName == "Processor" and CounterName == "% Processor Time"
| where InstanceName == "_Total"
| summarize 
    AvgCPU = avg(CounterValue),
    MaxCPU = max(CounterValue),
    P95CPU = percentile(CounterValue, 95)
    by Computer
| where P95CPU < 30  // 95th percentile under 30%
| join kind=inner (
    Resources
    | where type == "microsoft.compute/virtualmachines"
    | where tags.Environment == "Production"
    | extend 
        VMSize = properties.hardwareProfile.vmSize,
        Owner = tags.Owner,
        Application = tags.Application
    | project Computer = name, VMSize, Owner, Application
) on Computer
| project Computer, VMSize, AvgCPU, MaxCPU, P95CPU, Owner, Application
| order by P95CPU asc
```

**Red flags to watch for**:
- Batch processing workloads (CPU spikes at specific times)
- Month-end/quarter-end processing (need capacity for peak periods)
- Upcoming business growth (bad time to downsize)

### Big Win: Decommission Zombie Applications

**This is where real savings happen**â€”not optimization, elimination.

**Zombie app checklist**:
- [ ] No deployments in 6+ months
- [ ] No users in access logs
- [ ] Owner has left the company
- [ ] Nobody remembers what it does
- [ ] "Temporary" dev project from 2019

**Process**:
1. **Identify via tags and metrics**
2. **Email owner (use `Owner` tag)**
3. **Wait 2 weeks for response**
4. **Snapshot/backup everything**
5. **Shut down (don't delete) for 30 days**
6. **If nobody complains, delete**

```kql
// Find zombie app candidates
Resources
| where tags contains "Application"
| extend 
    Application = tostring(tags.Application),
    Owner = tostring(tags.Owner),
    LastDeployment = todatetime(tags.LastDeployment)
| where LastDeployment < ago(180d) or isempty(LastDeployment)
| join kind=leftouter (
    AzureCostManagementExports
    | where TimeGenerated >= ago(30d)
    | summarize MonthlyCost = sum(CostInBillingCurrency) by ResourceId
) on ResourceId
| summarize 
    ResourceCount = count(),
    TotalMonthlyCost = sum(MonthlyCost),
    Resources = make_list(name)
    by Application, Owner
| where ResourceCount > 3  // More than 3 resources = actual app
| order by TotalMonthlyCost desc
```

**Expected savings**: $10,000-$50,000/month per zombie application decommissioned. This decommissioning process should be part of your broader [Azure migration planning](/blog/cloud-migration-reality-check/), ensuring you're not just migrating technical debt to the cloud.

---

## Phase 5: Continuous Governance

Optimization is ongoingâ€”implement these to prevent cost regression.

### Governance 1: Monthly Cost Review Meetings

**Who**: Finance + IT + Application Owners  
**Frequency**: Monthly  
**Agenda**:
- Top 10 cost increases month-over-month
- New resources created (review for approval)
- Optimization wins achieved
- Next month's targets

**Make it data-driven**:
```kql
// Month-over-month cost changes by application
AzureCostManagementExports
| where TimeGenerated >= ago(60d)
| extend Month = startofmonth(TimeGenerated)
| extend Application = tostring(tags.Application)
| summarize MonthlyCost = sum(CostInBillingCurrency) by Month, Application
| order by Month desc, MonthlyCost desc
| serialize 
| extend PreviousMonthCost = prev(MonthlyCost, 1)
| extend CostChange = MonthlyCost - PreviousMonthCost
| extend PercentChange = round((CostChange / PreviousMonthCost) * 100, 2)
| where abs(PercentChange) > 20  // Flag changes > 20%
| project Application, Month, MonthlyCost, PreviousMonthCost, CostChange, PercentChange
```

### Governance 2: Azure Policy for Prevention

**Block untagged resources**:
```json
{
  "mode": "Indexed",
  "policyRule": {
    "if": {
      "anyOf": [
        {"field": "tags['Environment']", "exists": "false"},
        {"field": "tags['Owner']", "exists": "false"},
        {"field": "tags['CostCenter']", "exists": "false"}
      ]
    },
    "then": {
      "effect": "deny"
    }
  }
}
```

**Block oversized dev VMs**:
```json
{
  "mode": "Indexed",
  "policyRule": {
    "if": {
      "allOf": [
        {"field": "type", "equals": "Microsoft.Compute/virtualMachines"},
        {"field": "tags['Environment']", "in": ["Dev", "UAT", "Test"]},
        {"field": "Microsoft.Compute/virtualMachines/sku.name", "like": "Standard_D16*"}
      ]
    },
    "then": {
      "effect": "deny"
    }
  }
}
```

**Require auto-shutdown for dev/UAT**:
```json
{
  "mode": "Indexed",
  "policyRule": {
    "if": {
      "allOf": [
        {"field": "type", "equals": "Microsoft.Compute/virtualMachines"},
        {"field": "tags['Environment']", "in": ["Dev", "UAT"]}
      ]
    },
    "then": {
      "effect": "deployIfNotExists",
      "details": {
        "type": "Microsoft.DevTestLab/schedules",
        "roleDefinitionIds": ["/providers/Microsoft.Authorization/roleDefinitions/9980e02c-c2be-4d73-94e8-173b1dc7cf3c"],
        "deployment": {
          // Auto-shutdown deployment template
        }
      }
    }
  }
}
```

### Governance 3: Weekly Optimization Dashboard

Build a **Power BI dashboard** (or Azure Workbook) showing:
- Total Azure spend (this month vs. last month)
- Top 10 cost contributors by application
- Untagged resource count
- Orphaned disk count
- Dev/UAT VMs without auto-shutdown

**Make it visible**â€”email it to leadership weekly. Transparency drives action.

---

## Stakeholder Management

Cost optimization is 50% technical, 50% political. Here's how to navigate it.

### With Finance

**What they care about**: Predictability, chargeback, accountability  
**Your message**: "I can show you who's spending whatâ€”but I need tagging budget and time."  
**Win**: Get them to mandate tagging at the executive level

### With Application Owners

**What they care about**: Uptime, performance, not getting blamed  
**Your message**: "I'm here to help reduce *your* costsâ€”let's find waste together."  
**Win**: Frame optimization as *their* budget win, not IT's mandate

### With Leadership

**What they care about**: Big savings numbers, minimal risk  
**Your message**: "We can save 30% over 6 monthsâ€”here's the phased plan with risk mitigation."  
**Win**: Get executive sponsorship for decommissioning zombie apps

### With InfoSec/Compliance

**What they care about**: Not breaking audit requirements  
**Your message**: "Every change will be documented, tested, and reversible."  
**Win**: Get their sign-off on retention policies for deleted resources

---

## Common Pitfalls

### Pitfall 1: Optimizing Without Context
**Symptom**: Following Azure Advisor blindly  
**Result**: Breaking production, angry users, rolled-back changes  
**Fix**: Always check tags, ask owners, test in UAT first

### Pitfall 2: No Tagging Foundation
**Symptom**: Can't answer "who owns this resource?"  
**Result**: Paralysisâ€”too risky to change anything  
**Fix**: Stop all optimization until tagging is 80%+ complete

### Pitfall 3: One-Time Cleanup
**Symptom**: Big savings in Month 1, regression by Month 6  
**Result**: CFO asks "why are costs back up?"  
**Fix**: Implement governance policies and monthly reviews

### Pitfall 4: No Executive Sponsorship
**Symptom**: Application owners ignore your decommission requests  
**Result**: Zombie apps keep running indefinitely  
**Fix**: Get C-level mandate: "Owners have 30 days to respond or resources get shut down"

### Pitfall 5: Over-Optimizing Dev/Test
**Symptom**: Developers can't get work done, submit tickets constantly  
**Result**: Productivity loss exceeds cost savings  
**Fix**: Right-size dev environments but don't cripple them

---

## The 6-Month Roadmap

Here's the realistic timeline for meaningful cost reduction:

### Month 1-2: Foundation
- Complete resource inventory
- Establish tagging schema
- Begin tagging high-cost subscriptions
- Set up cost tracking dashboard

### Month 3-4: Quick Wins
- Delete orphaned disks
- Implement auto-shutdown for dev/UAT
- Right-size obvious oversized VMs
- Savings: **10-15%**

### Month 5-6: Strategic Optimization
- Decommission first zombie application
- Review and optimize reserved instances
- Implement cost governance policies
- Establish monthly review process
- Savings: **20-30%** cumulative

### Month 7+: Sustained Optimization
- Continuous improvement
- Quarterly architecture reviews
- New application cost approval process
- Savings: **30-40%** sustained

---

## Final Reality Check

**Azure cost optimization is not a sprintâ€”it's a marathon.**

You won't save 40% in Month 1. Anyone who promises that is lying.

What you *will* do:
- Build a foundation (tagging, inventory, governance)
- Capture quick wins (orphaned resources, auto-shutdown)
- Make strategic decisions (decommission zombies, right-size thoughtfully)
- Implement prevention (policies, reviews, accountability)

The enterprises I've worked with that succeeded had three things:
1. **Executive sponsorship** (CFO + CTO aligned)
2. **Business context** (tags, tags, tags)
3. **Patience** (6-month roadmap, not 2-week heroics)

Skip any of these and you'll either:
- Save nothing (no executive mandate)
- Break production (no business context)
- Create one-time savings that regress (no governance)

---

## Next Steps

**Week 1-2**: Run the baseline KQL queries in this guide  
**Week 3-4**: Define your tagging schema and get executive approval  
**Week 5-6**: Start tagging (high-cost subscriptions first)  
**Week 7-8**: Execute your first quick wins  
**Month 3+**: Build governance and keep optimizing

This isn't theory. This is the exact process I've used across multiple Azure environments.

It worksâ€”if you commit to the full framework, not just cherry-picking the easy parts.

**Good luck. You've got this.** ðŸš€

---

### 🛑 Optimization Requires Authority

You can identify waste, but can you delete it?
**[Download the Azure RACI Matrix](https://gumroad.com/l/raci-template?ref=cost-batch-guide)** to give your FinOps team the authority to decommission zombie resources.

<div class="downloads" style="text-align: center; margin-top: 2rem;">
  <a class="btn" href="https://gumroad.com/l/raci-template?ref=cost-batch-guide" style="font-size: 1.2em; padding: 15px 30px; background-color: #0078d4; color: white;">Get the Optimization RACI</a>
</div>

**Want the KQL queries from this guide in a ready-to-use format?** Check out my [Azure Cost Optimization KQL Library on GitHub](#)â€”all queries organized, tested, and ready to copy/paste.

---

## 🎯 Ready for Production-Ready Queries?

This guide covers the basics, but **scaling to 30,000+ resources requires battle-tested patterns.**

**The Complete KQL Query Library includes:**
- ✅ 48 copy-paste ready queries (VMs, networking, security, cost)
- ✅ Advanced joins (VMs → NICs → Disks → Subnets → Subscriptions)
- ✅ Enterprise-scale tested on 31,000+ resources
- ✅ Performance optimization for massive environments
- ✅ SQL to KQL translation guide
- ✅ Lifetime updates

**Launch price: $19** (regular $29)

[Get the Complete KQL Library →](https://davidnoob.gumroad.com/l/hooih)

---