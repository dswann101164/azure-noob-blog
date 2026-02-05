---
title: "Azure Cost Optimization 2025: Hidden Costs & What Actually Works"
date: 2025-12-08
summary: "Azure Advisor says 'right-size your VMs.' Finance says 'why is our cloud bill still increasing?' Here's what actually reduces Azure costs in production: the tactics that work when reserved instances and Advisor recommendations aren't enough."
tags: ["azure", "cost-optimization", "finops", "cost-management", "azure-advisor", "governance"]
cover: "/static/images/hero/azure-cost-optimization-complete-guide.png"
hub: "finops"
related_posts:
  - azure-cost-reports-business-reality
  - azure-openai-pricing-real-costs
  - azure-chargeback-tags-model
  - tag-governance-247-variations
---

# Azure Cost Optimization: What Actually Works (Not Azure Advisor Recommendations)

## The Problem

Finance email at 8 AM: "Azure spend is up $47,000 this month. What are we doing about cost optimization?"

You open Azure Advisor. It says:
- "Right-size 3 underutilized VMs" (saves $240/month)
- "Delete 2 unattached disks" (saves $45/month)
- "Buy reserved instances" (saves $1,200/month)

You implement all of it. Next month: **Azure spend is still up $46,715.**

**Why?** Because Azure Advisor optimizes what you already have. It doesn't prevent the three things that actually drive cloud cost growth:

1. **Untracked resource sprawl** (departments spinning up resources with no visibility)
2. **Lack of cost allocation** (nobody knows who's spending what)
3. **Missing governance** (no automated controls to prevent waste)

Here's what actually works when Advisor recommendations aren't enough.

---

## What Microsoft Says About Cost Optimization

Microsoft's [Azure Cost Management documentation](https://learn.microsoft.com/en-us/azure/cost-management-billing/) focuses on:

**Visibility:**
- Cost analysis dashboards
- Budget alerts
- Export cost data

**Optimization:**
- Azure Advisor recommendations
- Reserved instances and savings plans
- Right-sizing VMs

**Governance:**
- Azure Policy for tagging
- Budgets and alerts

These tools are excellent for **measuring** and **reacting** to costs. They don't **prevent** the costs from happening in the first place.

**Example:** Azure Advisor tells you a VM has been idle for 30 days. Great! But why did it get created in the first place? Who approved it? What application needed it? When Advisor finds it idle, you've already spent $2,000 on something nobody uses.

**The gap:** Microsoft's cost tools assume you have governance in place. Most organizations don't.

Here's what to do BEFORE you even look at Advisor recommendations.

---

## The 3 Phases of Azure Cost Optimization

### **Phase 1: Know What You Have (Month 1)**
### **Phase 2: Know Who's Spending It (Month 2-3)**
### **Phase 3: Prevent Waste Automatically (Month 4+)**

Most organizations skip Phase 1 and 2 and jump straight to Phase 3 (buying reserved instances). Then they wonder why costs keep growing.

Let's fix that.

---

## Phase 1: Know What You Have

**Time investment:** 2-4 weeks  
**Cost impact:** Identifies 20-30% of resources that shouldn't exist

### The Problem

You can't optimize what you can't see. Azure Cost Management shows you **costs**. It doesn't show you:
- Which resources support which applications
- Who requested each resource
- Why resources were created
- Which resources are actually being used

**Real example:** Found 47 VMs running in a subscription. Only 12 had been accessed in the last 90 days. **Total waste:** $22,000/month.

**Why it happened:** Developers spin up test VMs, forget about them, move to new projects. No process to track or decommission them.

### What Actually Works: Resource Inventory with Business Context

**Step 1: Build the inventory KQL query**

```kql
Resources
| where type =~ 'microsoft.compute/virtualmachines'
| extend 
    vmSize = properties.hardwareProfile.vmSize,
    osType = properties.storageProfile.osDisk.osType,
    powerState = properties.extended.instanceView.powerState.code
| join kind=leftouter (
    ResourceContainers
    | where type == 'microsoft.resources/subscriptions'
    | project subscriptionId, subscriptionName = name
) on subscriptionId
| project 
    name,
    resourceGroup,
    subscriptionName,
    location,
    vmSize,
    osType,
    powerState,
    tags,
    id
| extend 
    Application = tostring(tags.Application),
    Owner = tostring(tags.Owner),
    CostCenter = tostring(tags.CostCenter),
    Environment = tostring(tags.Environment)
```

**This query shows:**
- VM name, size, location
- Power state (running/stopped)
- Business context from tags

**Step 2: Export to Excel, add these columns manually:**
- **Last Accessed:** When was this VM last logged into?
- **Purpose:** What does this VM do?
- **Application Owner:** Who approved this?
- **Decommission Date:** When can we delete it?

**Step 3: Meet with each application owner**

Don't send an email survey. **Schedule 15-minute meetings.** Go through each resource in their resource group. Ask:
- "Do you still need this?"
- "When was the last time anyone logged into it?"
- "What happens if we turn it off for a week?"

**Result from one organization:** 35% of VMs were "probably safe to delete" after these conversations.

### What to Do With the Results

**Immediate actions (Week 1-2):**
- Delete obviously unused resources (unattached disks, old snapshots, stopped VMs older than 90 days)
- **Savings:** Usually 5-10% of monthly spend

**Short-term actions (Week 3-4):**
- Schedule decommission dates for "probably safe to delete" resources
- Test shutdowns (turn off for 1 week, see if anyone complains)
- **Savings:** 15-20% of monthly spend

**Long-term actions (Month 2+):**
- Implement automated shutdown schedules (dev/test VMs off nights/weekends)
- Tag enforcement (can't create resources without Owner/CostCenter tags)
- **Savings:** 20-30% of monthly spend

---

## Phase 2: Know Who's Spending It

**Time investment:** 4-8 weeks  
**Cost impact:** Enables chargeback, creates accountability

### The Problem

Azure subscriptions aren't cost centers. Applications are.

**Scenario:** Finance asks "How much did the Payroll application cost us this month?"

**Azure Cost Management shows:** "Subscription XYZ cost $47,000."

**Finance:** "But three applications run in that subscription. How much was Payroll specifically?"

**You:** "Uh..."

**The gap:** Azure tracks costs by subscription, resource group, and tags. Applications span all three.

### What Actually Works: Tag-Based Cost Allocation

**Step 1: Define your cost allocation model**

**Option A: Chargeback (precise)**
- Every dollar allocated to a business unit
- Requires: Owner, CostCenter, Application tags on ALL resources
- Use case: Regulated industries, large enterprises, anywhere finance requires exact allocation

**Option B: Showback (approximate)**
- Show departments what they're spending
- Doesn't require perfect tagging
- Use case: Most organizations, especially early in cloud journey

**Start with showback. Move to chargeback later.**

**Step 2: Implement tag governance**

Use Azure Policy to require tags on new resources:

```json
{
  "mode": "Indexed",
  "policyRule": {
    "if": {
      "allOf": [
        {
          "field": "type",
          "equals": "Microsoft.Compute/virtualMachines"
        },
        {
          "anyOf": [
            {
              "field": "tags['CostCenter']",
              "exists": "false"
            },
            {
              "field": "tags['Owner']",
              "exists": "false"
            },
            {
              "field": "tags['Application']",
              "exists": "false"
            }
          ]
        }
      ]
    },
    "then": {
      "effect": "deny"
    }
  }
}
```

**This policy blocks VM creation unless CostCenter, Owner, and Application tags are present.**

**Critical:** Start with "audit" effect, not "deny". Give teams 30 days to fix existing resources before you block new ones.

**Step 3: Build cost allocation reports in Power BI**

Azure Cost Management exports cost data. Connect Power BI to it:

```dax
CostByApplication = 
CALCULATE(
    SUM('CostData'[Cost]),
    ALLEXCEPT('CostData', 'CostData'[Application])
)
```

**Report shows:**
- Cost by Application
- Cost by CostCenter
- Cost by Owner
- Drill-down to resource-level details

**Result:** Finance can now answer "How much did Payroll cost?" with real data.

### What to Do With the Results

**Immediate actions (Month 1):**
- Publish cost by application reports monthly
- Send to application owners
- **Impact:** Creates awareness (costs usually stabilize or decrease 5-10%)

**Short-term actions (Month 2-3):**
- Implement budgets per application
- Alert owners when they're at 80% of budget
- **Impact:** Prevents surprise overruns

**Long-term actions (Month 4+):**
- Chargeback model (IT charges business units for Azure spend)
- Application owners now have incentive to optimize
- **Impact:** 10-20% cost reduction as owners optimize their own resources

---

## Phase 3: Prevent Waste Automatically

**Time investment:** Ongoing  
**Cost impact:** Prevents 30-40% of future waste

### The Problem

Even with perfect visibility and cost allocation, costs still grow because:
- Developers forget to delete test resources
- VMs run 24/7 when they're only needed 8-5
- Storage accounts accumulate old data nobody needs
- Nobody notices small resource creep (5 VMs here, 3 storage accounts there)

**Manual optimization doesn't scale.** You need automation.

### What Actually Works: Automated Governance

**Tactic 1: Auto-shutdown schedules**

Dev/test VMs should not run nights and weekends.

**PowerShell automation:**

```powershell
# Tag VMs with shutdown schedule
Update-AzTag -ResourceId $vmId -Tag @{
    "AutoShutdown" = "Weeknights-7PM"
    "AutoStart" = "Weekdays-7AM"
} -Operation Merge

# Azure Automation runbook checks tags hourly, starts/stops VMs
```

**Savings:** 65% reduction in dev/test VM costs (VMs only run 40 hours/week instead of 168)

**Tactic 2: Storage lifecycle policies**

Old blobs cost money. Delete them automatically.

**Lifecycle policy:**

```json
{
  "rules": [
    {
      "enabled": true,
      "name": "delete-old-logs",
      "type": "Lifecycle",
      "definition": {
        "filters": {
          "blobTypes": ["blockBlob"],
          "prefixMatch": ["logs/"]
        },
        "actions": {
          "baseBlob": {
            "delete": {
              "daysAfterModificationGreaterThan": 90
            }
          }
        }
      }
    }
  ]
}
```

**Savings:** 30-50% reduction in storage costs (depends on data retention needs)

**Tactic 3: Orphaned resource cleanup**

Unattached disks, unused NICs, old snapshotsâ€”nobody notices them until the bill arrives.

**KQL query to find orphaned disks:**

```kql
Resources
| where type =~ 'microsoft.compute/disks'
| where properties.diskState =~ 'Unattached'
| extend diskSizeGB = properties.diskSizeGB
| extend sku = properties.sku.name
| project name, resourceGroup, diskSizeGB, sku, id
```

**Automate cleanup:** Azure Automation runbook deletes unattached disks older than 30 days (after confirming with owners).

**Savings:** $5-10K/month in mid-size environments

**Tactic 4: Right-sizing automation**

Azure Advisor says "right-size this VM." Great. Who's actually going to do it?

**Automation pattern:**
1. Weekly script pulls Advisor recommendations
2. Filters for high-confidence, low-risk changes (CPU <5% for 30 days)
3. Creates Azure DevOps ticket for VM owner
4. Auto-applies change if owner doesn't respond in 14 days

**Savings:** Actually implements 80% of Advisor recommendations (vs. 10% manual implementation rate)

### What to Do With the Results

**Month 1:**
- Implement auto-shutdown for dev/test VMs
- **Impact:** 15-25% reduction in VM costs

**Month 2:**
- Add storage lifecycle policies
- **Impact:** 10-20% reduction in storage costs

**Month 3:**
- Automate orphaned resource cleanup
- **Impact:** $5-15K/month in small waste elimination

**Month 4+:**
- Automate Advisor recommendation implementation
- **Impact:** Another 10-15% reduction from right-sizing

**Cumulative:** 30-40% reduction in Azure spend with minimal ongoing effort

---

## The Tools You Actually Need

**Forget expensive third-party cost optimization tools.** Here's what you need:

### **1. Azure Resource Graph (Free)**
For inventory and resource discovery

**Learn more:** [KQL Cheat Sheet](/blog/kql-cheat-sheet-complete/)

### **2. Power BI (Free with Office 365)**
For cost allocation reports and executive dashboards

**Learn more:** [Azure Cost Reports for Business Reality](/blog/azure-cost-reports-business-reality/)

### **3. Azure Policy (Free)**
For tag enforcement and governance

**Learn more:** [Azure Tag Governance Policy](/blog/azure-tag-governance-policy/)

### **4. Azure Automation (Nearly Free)**
For auto-shutdown, cleanup scripts, and Advisor automation

**Cost:** ~$5/month for typical automation workloads

### **5. Excel + 15-Minute Meetings (Free)**
For Phase 1 inventory and application owner conversations

**Total cost:** $5/month + your time

**Compare to:** Third-party tools ($10K-50K/year) that do the same thing

---

## What Doesn't Work (Don't Waste Time)

### **âŒ Reserved Instances Without Governance**

**Scenario:** You buy 3-year reserved instances. Savings: 40%.

**Problem:** Application gets decommissioned in Year 2. You're stuck paying for reserved capacity you don't need.

**Lesson:** Only buy reserved instances for workloads with:
- Stable usage patterns (proven 12+ months)
- Business commitment (not getting decommissioned)
- Tag governance (you can track what it's for)

### **âŒ Cost Optimization Without Tag Governance**

**Scenario:** You optimize costs by 20%. Finance asks "Which applications saved money?"

**Problem:** You can't answer because resources aren't tagged with application names.

**Lesson:** Phase 2 (cost allocation) enables Phase 3 (optimization). Don't skip it.

### **âŒ Relying on Advisor Recommendations Alone**

**Scenario:** Azure Advisor says "save $1,200/month with these 10 changes."

**Problem:** 9 of those recommendations are low-risk but also low-impact. The 10th is high-risk (resize production database) and nobody wants to do it.

**Lesson:** Advisor finds optimization opportunities. It doesn't implement them or assess risk. You need automation.

### **âŒ Sending Email Surveys About Resource Usage**

**Scenario:** You email 50 application owners: "Do you still need these VMs?"

**Responses:** 3 people reply. 47 ignore the email.

**Lesson:** Schedule 15-minute meetings. Walk through resources together. You'll get real answers.

---

## Real-World Results

**Organization A (Regional financial services company):**
- **Starting point:** $180K/month Azure spend, no tag governance
- **Phase 1 (Month 1-2):** Resource inventory identified $45K/month in unused VMs
- **Phase 2 (Month 3-4):** Tag enforcement + cost allocation reports
- **Phase 3 (Month 5-8):** Auto-shutdown, lifecycle policies, orphaned resource cleanup
- **Result:** $120K/month Azure spend (33% reduction), maintained for 12+ months

**Organization B (Healthcare SaaS company):**
- **Starting point:** $85K/month Azure spend, growing 15%/month
- **Phase 1 (Month 1):** Found 40% of storage was old backups nobody needed
- **Phase 2 (Month 2-3):** Tag governance stopped untracked resource sprawl
- **Phase 3 (Month 4+):** Auto-shutdown reduced dev/test costs by 60%
- **Result:** $62K/month Azure spend (27% reduction), growth stopped

**Pattern:** Most organizations find 20-40% optimization opportunity. Half of it comes from "delete stuff nobody's using." The other half comes from automation.

---

## The 90-Day Cost Optimization Plan

### **Month 1: Visibility**
- **Week 1-2:** Resource inventory (KQL queries, Excel export)
- **Week 3-4:** Application owner meetings (15 min each)
- **Result:** List of resources to delete, downsize, or keep

### **Month 2: Allocation**
- **Week 1-2:** Implement tag governance (Azure Policy with "audit" effect)
- **Week 3-4:** Build Power BI cost allocation reports
- **Result:** Finance can answer "How much did Application X cost?"

### **Month 3: Automation**
- **Week 1:** Auto-shutdown for dev/test VMs
- **Week 2:** Storage lifecycle policies
- **Week 3:** Orphaned resource cleanup automation
- **Week 4:** Advisor recommendation automation
- **Result:** Ongoing waste prevention without manual effort

**Expected outcome:** 25-35% cost reduction, sustained indefinitely

---

## Common Objections (And Responses)

### **"We don't have time for 15-minute meetings with every app owner."**

You don't have time NOT to. One meeting prevents $2,000/month in waste. That's $24,000/year. Worth 15 minutes?

### **"Our developers will complain about auto-shutdown breaking their workflows."**

Give them an opt-out tag. `"AutoShutdown" = "Never"` for resources that need 24/7 uptime. 95% of dev/test VMs don't need it.

### **"We tried tag governance before. Nobody followed it."**

Because you didn't enforce it. Move from "audit" to "deny" policy. Can't create resources without tags.

### **"Reserved instances are too risky. What if the workload changes?"**

Then don't buy 3-year commitments. Buy 1-year. Or use savings plans (more flexible). Or just optimize with automation first.

### **"Our organization is too complex for this simple approach."**

Your organization is exactly WHY this approach works. Simple, repeatable, automated. Complexity is the enemy of cost control.

---


---

## The Bottom Line

**Azure Advisor recommendations are necessary but not sufficient.**

**What Advisor does:**
- Finds optimization opportunities in existing resources
- Recommends reserved instances and right-sizing
- Identifies unused resources

**What Advisor doesn't do:**
- Stop new waste from being created
- Allocate costs to business units
- Implement recommendations automatically
- Prevent untracked resource sprawl

**The winning formula:**
1. **Know what you have** (inventory + business context)
2. **Know who's spending it** (tag governance + cost allocation)
3. **Prevent waste automatically** (auto-shutdown + lifecycle policies + cleanup scripts)

**Expected result:** 25-35% cost reduction, maintained indefinitely

**Time investment:** 90 days upfront, minimal ongoing effort

**Tools needed:** Azure Resource Graph + Power BI + Azure Policy + Azure Automation (total cost: ~$5/month)

---

## Related Resources

**Learn the tools for cost optimization:**
- [KQL Cheat Sheet](/blog/kql-cheat-sheet-complete/) - Query resources and costs
- [FinOps Hub](/hub/finops/) - Complete cost optimization guides
- [Azure Tag Governance](/blog/azure-tag-governance-policy/) - Enforce tagging for cost allocation
- [Azure Cost Reports for Business](/blog/azure-cost-reports-business-reality/) - Build Power BI dashboards

**Cost-related posts:**
- [Azure Chargeback Tags Model](/blog/azure-chargeback-tags-model/)
- [Azure OpenAI Pricing Reality](/blog/azure-openai-pricing-real-costs/)
- [Tag Governance: 247 Variations](/blog/tag-governance-247-variations/)

---

### ?? Find the Hidden Waste (Orphans)

Don't wait for Advisor. Run this query to find orphaned disks costing you money right now.

```kusto
// Find Orphaned Managed Disks (Not attached to any VM)
Resources
| where type =~ 'microsoft.compute/disks'
| where properties.diskState == 'Unattached'
| project name, resourceGroup, sku.name, diskSizeGB = properties.diskSizeGB
| sort by diskSizeGB desc
```

---

**Questions about cost optimization?** Let me know what you're struggling with. Email or comment below.

---

### ?? Optimization is a Role, Not a Task

Optimization works when someone's job description says "Cost Efficiency."
**[Download the Azure RACI Matrix](https://davidnoob.gumroad.com/l/ifojm?ref=cost-batch-optimization)** to define who owns the optimization lifecycle.

<div class="downloads" style="text-align: center; margin-top: 2rem;">
  <a class="btn" href="https://davidnoob.gumroad.com/l/ifojm?ref=cost-batch-optimization" style="font-size: 1.2em; padding: 15px 30px; background-color: #0078d4; color: white;">Get the FinOps RACI</a>
</div>

*Updated December 8, 2025*
