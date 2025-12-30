---
title: "Azure Governance Crisis Mode: The 90-Day Recovery Framework"
date: 2025-12-30
summary: "Your Azure environment is ungoverned: 12,000 untagged resources, $800K/month bill with no owner map, 47 subscriptions in chaos. You have 90 days and limited political capital. Here's the enterprise-tested triage sequence that prevents you from getting fired while building long-term governance."
tags: ["Azure", "Governance", "Crisis Management", "FinOps", "Cost Management", "Enterprise", "Recovery"]
cover: "/static/images/hero/azure-governance-crisis.png"
hub: governance
related_posts:
  - azure-governance-napkin-test
  - azure-cost-management-lie
  - azure-landing-zone-reality-check
  - azure-chargeback-tags-model
  - tag-governance-247-variations
---

**Monday morning. 9 AM. Conference room.**

CFO: "Azure costs $847K this month. That's 22% over budget. What are we paying for?"

You: *Opens Azure portal. 12,347 resources. 11,982 have zero tags. 47 subscriptions. No naming standards. No clear owners.*

CFO: "I need answers by Friday's board meeting."

**You have 90 days to turn chaos into governance.**

Not 12 months. Not "when the CAF rollout finishes." Not "after we hire consultants."

**90 days. Starting now.**

This is not a drill. This is the brownfield governance reality that 80% of Azure enterprises face.

---

## Why This Framework Exists

This guide is part of our [Azure Governance & FinOps Hub](/hub/governance/) covering the complete governance lifecycle from crisis through optimization.

Most Azure governance guides assume:
- ✅ Greenfield environment
- ✅ Executive support
- ✅ Dedicated governance team
- ✅ Time to "do it right"

**Your reality:**
- ❌ Brownfield chaos from 4 years of "just get it working"
- ❌ Finance threatening to cut cloud budget by 30%
- ❌ You're the only Azure architect for 31,000 resources
- ❌ The CFO wants results Friday, not in 18 months

**This is crisis mode governance.**

And it requires a completely different approach than the CAF documentation suggests.

---

## The 90-Day Triage Model

### Core Principle: Stopbleeds, Then Heal

You cannot fix everything in 90 days.

You CAN:
1. **Stop the bleeding** (zombie resources, orphaned subscriptions)
2. **Create visibility** (who owns what, what costs what)
3. **Establish authority** (RACI matrix, approval gates)
4. **Build momentum** (quick wins that prove governance works)

Then, after demonstrating value in 90 days, you get political capital for Phase 2 (optimization) and Phase 3 (long-term enforcement).

**But if you don't survive the first 90 days, there is no Phase 2.**

---

## Week 1-2: Baseline & Stopbleeds

**Goal:** Know what you have. Kill the obvious waste.

### Day 1-3: Emergency Triage Query

**Run this first:**

```kusto
Resources
| where type !in ("microsoft.insights/components", "microsoft.operationalinsights/workspaces")
| extend 
    HasTags = iif(array_length(todynamic(tags)) > 0, "Tagged", "Untagged"),
    IsRunning = iif(properties.powerState contains "running", "Running", "Stopped"),
    ResourceAge = datetime_diff('day', now(), todatetime(properties.timeCreated))
| summarize 
    ResourceCount = count(),
    EstimatedMonthlyCost = sum(todouble(properties.estimatedCost))
    by subscriptionId, resourceGroup, type, HasTags, IsRunning
| order by EstimatedMonthlyCost desc
| take 100
```

**This shows you:**
- Top 100 most expensive resource types
- How many are tagged vs untagged
- How many are running vs stopped
- Which subscriptions/resource groups own the cost

**Action:** Export to Excel. This is your "Triage Dashboard."

### Day 4-7: Find the Zombies

**Zombie resources:** Running for 90+ days with zero activity.

```kusto
Resources
| where type =~ "microsoft.compute/virtualmachines"
| extend PowerState = tostring(properties.extended.instanceView.powerState.code)
| where PowerState contains "running"
| join kind=leftouter (
    AzureActivity
    | where TimeGenerated > ago(90d)
    | where OperationNameValue contains "Microsoft.Compute"
    | summarize LastActivity = max(TimeGenerated) by ResourceId
) on $left.id == $right.ResourceId
| where isnull(LastActivity) or LastActivity < ago(90d)
| extend 
    EstimatedMonthlyCost = todouble(properties.hardwareProfile.vmSize) * 100  // rough estimate
| project 
    Name = name,
    ResourceGroup = resourceGroup,
    Subscription = subscriptionId,
    VMSize = tostring(properties.hardwareProfile.vmSize),
    LastActivity,
    EstimatedMonthlyCost
| order by EstimatedMonthlyCost desc
```

**This finds:**
- VMs running for 90+ days with no logins, no reboots, no configuration changes
- Likely cost: $20K-$200K/month depending on environment

**Action:** Create "Zombie Decommission List" with owners (or "Unknown" if no owner exists).

### Day 8-14: Emergency Stopbleeds

**Kill these immediately (with approval):**
1. **Stopped VMs still incurring storage costs** - Deallocate or delete
2. **Orphaned disks** (no attached VM) - Delete after 30-day grace period
3. **Empty resource groups** - Delete (they create noise)
4. **Duplicate resources** (dev/test leftovers) - Delete non-production duplicates
5. **Inactive storage accounts** (zero blob operations in 90 days) - Archive or delete

**Expected savings:** $50K-$150K/month

**Political capital gain:** CFO sees immediate $150K/month reduction = you get 60 more days.

---

## Week 3-6: Power Mapping (Who Owns What)

**Goal:** Create the ownership map. Even if imperfect.

### Week 3: Map Subscriptions to Business Units

**You need:**
- Subscription Name
- Business Unit Owner (name + email)
- Cost Center
- Purpose (Production, Development, Sandbox, etc.)

**How to find owners:**

```kusto
Resources
| summarize ResourceCount = count() by subscriptionId
| join kind=inner (
    ResourceContainers
    | where type == "microsoft.resources/subscriptions"
    | project subscriptionId, SubscriptionName = name, tags
) on subscriptionId
| extend 
    Owner = tostring(tags.Owner),
    CostCenter = tostring(tags.CostCenter),
    Environment = tostring(tags.Environment)
| project 
    SubscriptionName,
    ResourceCount,
    Owner = iif(isempty(Owner), "UNKNOWN", Owner),
    CostCenter = iif(isempty(CostCenter), "UNKNOWN", CostCenter),
    Environment = iif(isempty(Environment), "UNKNOWN", Environment)
| order by ResourceCount desc
```

**Action:** Create Excel with columns:
- Subscription Name
- Current Owner (from tags or manual research)
- Cost Center (Finance department will help here)
- Monthly Cost (from Azure Cost Management)
- Status (Owned, Orphaned, Decommission Candidate)

**Send this to Finance and each department head:** "This is what you own. Confirm or correct by Friday."

### Week 4-5: Build the RACI Matrix

**Don't build perfect governance. Build clear accountability.**

**Required roles (minimum viable):**
1. **Subscription Owner** - Approves budget, decommissions
2. **Resource Contributor** - Creates/modifies resources
3. **Cost Allocation Owner** - Tags resources for chargeback
4. **Security Approver** - Approves network/identity changes
5. **Tag Standard Approver** - Defines tagging schema

**Template:**

| Operation | Approver | Contributor | Informed | Notes |
|-----------|----------|-------------|----------|-------|
| Create subscription | CFO | IT Director | Finance | Requires cost center mapping |
| Delete resource | Subscription Owner | Resource Contributor | Finance | 30-day approval window |
| Modify tags | Cost Allocation Owner | Resource Contributor | Finance | Monthly cleanup cycle |
| Create network resource | Security Approver | Network Admin | IT Director | Requires architecture review |
| Decommission subscription | CFO | Subscription Owner | Finance, IT | 60-day notification |

**This is your command structure for the next 60 days.**

### Week 6: Assign Ownership to Top 20 Subscriptions

**Focus:** The 20 subscriptions representing 80% of cost.

**Action:**
1. Send email to each business unit: "You own these subscriptions. Confirm or deny."
2. If they confirm → They're now accountable in the RACI matrix
3. If they deny → Escalate to their VP with CFO copy
4. If no response after 2 weeks → Mark "Orphaned - Decommission Candidate"

**Expected outcome:** 15/20 subscriptions have clear owners by end of Week 6.

---

## Week 7-10: Tag Triage (80/20 Rule)

**Goal:** Tag the expensive stuff first. Ignore the rest.

### Week 7: Define Minimum Viable Tag Schema

**Don't create a 15-tag schema that nobody will follow.**

**Start with 3 tags:**
1. **CostCenter** (4 digits: matches Finance system)
2. **Environment** (Production, Development, Staging - pick 3)
3. **Owner** (email address of person accountable)

**That's it.**

### Week 8-9: Tag the Top 200 Resources by Cost

**Query:**

```kusto
Resources
| extend MonthlyCost = todouble(properties.estimatedCost) * 720  // rough monthly estimate
| order by MonthlyCost desc
| take 200
| project 
    ResourceId = id,
    Name = name,
    ResourceGroup = resourceGroup,
    Subscription = subscriptionId,
    Type = type,
    MonthlyCost,
    CurrentTags = tags
```

**Action:**
1. Export to Excel
2. Add columns: CostCenter, Environment, Owner
3. Send to subscription owners: "Fill these in by Friday"
4. Use Azure CLI to bulk-apply tags:

```bash
az tag create --resource-id $resourceId \
  --tags CostCenter=4200 Environment=Production Owner=john@company.com
```

**Expected outcome:** 200 resources (representing 60-70% of cost) are tagged correctly.

### Week 10: Create Tag Reporting Dashboard

**Now you can answer the CFO's question:**

```kusto
Resources
| extend 
    CostCenter = tostring(tags.CostCenter),
    Environment = tostring(tags.Environment),
    MonthlyCost = todouble(properties.estimatedCost) * 720
| where isnotempty(CostCenter)
| summarize TotalCost = sum(MonthlyCost) by CostCenter, Environment
| order by TotalCost desc
```

**This shows:** "$847K/month breaks down as: Finance (4200) = $240K, Sales (5100) = $180K, IT (6000) = $320K, Unknown = $107K."

**CFO's response:** "Good. Now reduce 'Unknown' to zero and charge each department."

---

## Week 11-12: Policy Lockdown (Prospective Only)

**Goal:** Prevent new chaos. Grandfather existing chaos.

### Week 11: Create Deny Policies for New Resources

**Azure Policy JSON:**

```json
{
  "mode": "Indexed",
  "policyRule": {
    "if": {
      "anyOf": [
        {
          "field": "tags['CostCenter']",
          "exists": "false"
        },
        {
          "field": "tags['Environment']",
          "exists": "false"
        },
        {
          "field": "tags['Owner']",
          "exists": "false"
        }
      ]
    },
    "then": {
      "effect": "deny"
    }
  }
}
```

**Apply to:** Management group for Production subscriptions only.

**Grandfather:** Existing resources exempt. Policy applies only to NEW resources created after Week 11.

### Week 12: Communicate the New Rules

**Email to all Azure contributors:**

> Subject: New Azure tagging requirements effective immediately
>
> Starting Monday, all NEW resources created in Production subscriptions require 3 tags:
> - CostCenter (4 digits - see Finance for your code)
> - Environment (Production, Development, or Staging)
> - Owner (your email address)
>
> Existing resources: No action required. We'll clean up tags during Q1 maintenance windows.
>
> Questions? Reply to this thread or join office hours Friday 2-3 PM.

**Expected pushback:** 20% will complain. Respond: "CFO mandate. Non-negotiable."

---

## Day 90: The Board Presentation

**CFO to you:** "Give me 5 slides for Friday's board meeting."

### Slide 1: Governance Crisis → Governance Baseline (90 Days)

**Before (Day 1):**
- 12,347 resources, 11,982 untagged (97%)
- $847K/month spend, no cost allocation
- 47 subscriptions, 38 with unknown owners (81%)
- Zero policy enforcement

**After (Day 90):**
- 12,120 resources (227 zombies deleted)
- 3,200 resources tagged (top 200 by cost + top 20 subscriptions)
- 32 subscriptions with clear owners (68%)
- Azure Policy enforcing tags on new Production resources

### Slide 2: Cost Impact

**Zombies killed:** $127K/month savings  
**Orphaned disks deleted:** $18K/month savings  
**Unused storage accounts archived:** $9K/month savings  
**Total:** $154K/month = $1.85M/year

**ROI:** 3-month investment (your time + $0 tools) = $1.85M annual return

### Slide 3: Ownership Map

**Before:** 81% of subscriptions had "Unknown" owner  
**After:** 68% of subscriptions have confirmed business owners

**Remaining 32%:** Marked for decommission unless claimed by Q1 2026.

### Slide 4: Chargeback Readiness

**Before:** Finance could not allocate Azure costs to departments  
**After:** 70% of costs are tagged and allocated

**Next 90 days:** Implement monthly chargeback reports to department heads.

### Slide 5: Phase 2 Plan (Q1 2026)

**Optimization (90 days):**
- Reserved Instances for Production workloads (20-30% savings)
- Right-size oversized VMs (10-15% savings)
- Archive cold storage (5-10% savings)

**Expected additional savings:** $200K-$400K/year

---

## The Technical Magnet: Top 50 Untagged Resources by Cost

**Paste this into Azure Resource Graph Explorer:**

```kusto
Resources
| extend 
    HasCostCenterTag = iif(isnotempty(tostring(tags.CostCenter)), "Yes", "No"),
    HasEnvironmentTag = iif(isnotempty(tostring(tags.Environment)), "Yes", "No"),
    HasOwnerTag = iif(isnotempty(tostring(tags.Owner)), "Yes", "No"),
    MonthlyCost = todouble(properties.estimatedCost) * 720  // estimate
| where HasCostCenterTag == "No" or HasEnvironmentTag == "No" or HasOwnerTag == "No"
| order by MonthlyCost desc
| take 50
| project 
    ResourceName = name,
    ResourceGroup = resourceGroup,
    Subscription = subscriptionId,
    ResourceType = type,
    EstimatedMonthlyCost = MonthlyCost,
    MissingTags = strcat(
        iif(HasCostCenterTag == "No", "CostCenter ", ""),
        iif(HasEnvironmentTag == "No", "Environment ", ""),
        iif(HasOwnerTag == "No", "Owner", "")
    ),
    CurrentTags = tags
| order by EstimatedMonthlyCost desc
```

**Save this.** Run it weekly. Your "Top 50 Untagged" list should shrink every week.

**When it hits zero:** You've won.

---

## What Comes After Day 90?

You've stopped the bleeding. You've created visibility. You've proven governance works.

**Now you can do governance properly:**

**Phase 2 (Q1 2026): Optimization**
- Reserved Instances
- Right-sizing
- Hybrid Benefit
- Storage tiering
- [Complete Cost Optimization Guide](/blog/azure-cost-optimization-complete-guide/)

**Phase 3 (Q2 2026): Enforcement**
- Full tag governance policies
- Automated compliance scanning
- Monthly chargeback reports
- [Tag Governance That Actually Enforces](/blog/azure-tag-governance-policy/)

**Phase 4 (Q3 2026): Maturity**
- FinOps KPIs
- Continuous optimization
- Self-service governance
- [Azure FinOps Complete Framework](/blog/azure-finops-complete-guide/)

But none of that happens if you don't survive the first 90 days.

---

## Common Failure Modes (And How to Avoid Them)

### Failure #1: Trying to Fix Everything at Once

**Symptom:** You create a 47-page governance doc, schedule 12 workshops, propose a 6-month CAF rollout.

**Result:** Finance cuts budget before you finish planning.

**Fix:** 90-day triage. Kill waste first. Build governance second.

### Failure #2: Waiting for Executive Approval

**Symptom:** You schedule governance kickoff meetings with VPs, wait for strategy approval, draft charters.

**Result:** 6 weeks gone, zero zombies deleted, CFO loses patience.

**Fix:** Delete zombies on Day 1. Ask forgiveness, not permission. Show immediate ROI.

### Failure #3: Perfect Tags vs Good Enough Tags

**Symptom:** You debate 15-tag schema, semantic standards, taxonomy frameworks.

**Result:** 3 months of debate, zero tags applied.

**Fix:** Start with 3 tags (CostCenter, Environment, Owner). Expand later.

### Failure #4: Blaming "The Business"

**Symptom:** "Business units won't tag their resources. Governance is impossible without buy-in."

**Result:** CFO blames you, not the business units.

**Fix:** Tag the expensive stuff yourself. Prove the model works. Then mandate it.

### Failure #5: Treating This Like a Project

**Symptom:** You set up PMO tracking, write status reports, schedule phase gates.

**Result:** Governance dies after 6 months when "the project ends."

**Fix:** Treat governance as operations, not a project. RACI matrix = permanent org structure.

---

## The Authority Framework You Need

Reading this guide gives you the playbook.

**The RACI Matrix gives you the authority to execute it.**

Without clear ownership of:
- Who approves resource deletion (Subscription Owner)
- Who enforces tagging (Cost Allocation Owner)
- Who decides what to keep vs kill (CFO + Business Unit Head)

...you'll spend 90 days asking for permission instead of taking action.

---

### 🛑 Stop Operating in a Power Vacuum

Crisis governance requires command structure, not consensus.

**[Download the Azure RACI Matrix](https://davidnoob.gumroad.com/l/ifojm?ref=crisis-recovery)** with 58 Azure operations mapped to 5 roles.

**What's inside:**
- ✅ Pre-mapped accountability for 58 Azure operations
- ✅ Excel template (edit for your org structure)
- ✅ Role definitions (Approver vs Contributor vs Informed)
- ✅ Crisis mode modifications (faster approval cycles)
- ✅ Escalation paths for when stakeholders don't respond

**Price:** $29 (Launch special: $19 until Jan 31, 2026)

**Guarantee:** If this doesn't save you 10+ hours of "who has authority to delete this?" confusion in your first week, instant refund.

<div class="downloads" style="text-align: center; margin-top: 2rem; margin-bottom: 3rem;">
  <a class="btn" href="https://davidnoob.gumroad.com/l/ifojm?ref=crisis-recovery" style="font-size: 1.3em; padding: 18px 36px; background-color: #0078d4; color: white; border-radius: 6px; text-decoration: none;">Get the Crisis Command Structure</a>
  <p style="margin-top: 1rem; color: #666;">You have 90 days. Don't waste them debating who owns what.</p>
</div>

---

## The Bottom Line

**Perfect governance takes 18 months.**

**Surviving the next 90 days takes triage.**

Kill zombies. Map ownership. Tag the expensive stuff. Lock down new resources.

Then, when Finance sees $150K/month in savings and the CFO can finally explain the Azure bill, you get 6 more months to build real governance.

**But if you try to build perfect governance while the environment burns, you'll be replaced by someone who knows how to triage.**

This is crisis mode. Act like it.

---

## Related Posts

**The governance recovery sequence:**
1. **This post** - Crisis mode triage (Days 1-90)
2. [Azure Cost Optimization Complete Guide](/blog/azure-cost-optimization-complete-guide/) - Optimization (Days 91-180)
3. [Azure Tag Governance Policy](/blog/azure-tag-governance-policy/) - Enforcement (Days 181-270)
4. [Azure FinOps Complete Framework](/blog/azure-finops-complete-guide/) - Maturity (Days 271+)

**The strategic foundation:**
- [The Napkin Test: Why 90% of Azure Governance Fails](/blog/azure-governance-napkin-test/) - Defensibility before compliance
- [Azure Policy Doesn't Fix Bad Architecture](/blog/azure-policy-doesnt-fix-bad-architecture/) - Why enforcement alone fails
- [The Lie Azure Cost Management Tells Enterprises](/blog/azure-cost-management-lie/) - Why Microsoft's cost tools assume greenfield

**The execution playbook:**
- [Azure Costs: Track by Apps, Not Subscriptions](/blog/azure-costs-apps-not-subscriptions/) - Cost allocation reality
- [Tag Governance: 247 Variations of "Production"](/blog/tag-governance-247-variations/) - Semantic standardization
- [Azure Chargeback That Business Units Accept](/blog/azure-chargeback-tags-model/) - The 6 tags that work

---

### Azure Admin Starter Kit (Free Download)

Get my KQL cheat sheet, 50 Windows + 50 Linux commands, and an Azure RACI template in one free bundle.

[Get the Starter Kit →](/blog/starter-kit/)
