---
title: "Azure Subscriptions vs. Apps: The 2025 Cost Model Guide"
date: 2025-10-11
summary: Azure bills at the subscription level—but the business thinks in terms of
  applications. Here's how to realign cost models for reality.
tags:
- Azure
- FinOps
- Cost Allocation
- Application Mapping
- Governance
cover: /static/images/hero/azure-finops-apps-vs-subscriptions.png
slug: azure-costs-apps-not-subscriptions


related_posts:
  - azure-resource-tags-guide
  - azure-chargeback-tags-model
  - azure-finops-complete-guide

---

This guide is part of our [Azure FinOps hub](/hub/finops/) covering cost management, chargeback models, and financial operations at enterprise scale.
**You start with the billing stupidly. Understanding how many apps you have helps get you to where you want to be.**

Microsoft told us to use subscriptions as billing boundaries. Two years later, we're maintaining manual spreadsheets to allocate costs across 44 subscriptions and 31,000 resources. Here's what we wish we'd known on day one: **count your applications first.**

## The Cloud Adoption Framework Rabbit Hole

Open Microsoft's Cloud Adoption Framework and prepare for a journey through:
- Management group hierarchies with 6 levels of depth
- Policy inheritance patterns across subscription boundaries
- Landing zone archetypes (Corporate, Online, Sandbox)
- Subscription vending automation and democratization
- "Scale units" and "workload isolation patterns"

You'll spend three months in architecture meetings drawing diagrams. Your whiteboard will look like a family tree designed by someone who hates their family.

**Here's what CAF won't tell you:** None of that matters if you don't know how many applications you're running.

## What Microsoft Says

CAF documentation is technically correct:
- Subscriptions are units of management, billing, and scale
- Use subscriptions to separate environments (dev/test/prod)
- Use tags for cost allocation with application name, cost center, environment
- Establish a tagging strategy for chargeback and showback

**The problem?** It assumes you already know your application inventory. You don't. Nobody does. Not on day one.

## The Simple Answer

Before you drown in CAF documentation, answer these questions:

**How many applications does each team run?**
- Data team: 3 apps? 10 apps?
- Finance team: 5 apps? 30 apps?
- Infrastructure team: Just shared services? Or line-of-business apps too?

**Which applications cost actual money?**
- Production workloads with real users
- Revenue-generating systems
- Compliance-heavy applications that can't share infrastructure

**Which teams have 3 apps versus 30 apps?**
- This determines whether you need tags
- If Finance has 30 applications in one subscription, you need tag-based cost allocation
- If Data has 3 applications, subscription-level reporting might work

## The Design Pattern That Actually Works

**Match your subscriptions to your organizational teams:**

```
Data Team:
├── sub-data-prod
└── sub-data-dev

Infrastructure Team:
├── sub-infra-prod
└── sub-infra-dev

Finance Team:
├── sub-finance-prod
└── sub-finance-dev

Active Directory Team:
└── sub-identity-prod
```

**Then tag every resource by application:**

```yaml
Application: "CostReporting"      # Which app owns this resource
Environment: "Production"          # Prod/Dev/Test
Owner: "Finance"                   # Which team
CostCenter: "1234"                 # Chargeback code
```

**That's it.** 

Subscriptions = Team boundaries and RBAC isolation  
Tags = Cost boundaries and application tracking

Stop trying to make subscriptions do both jobs. That's where everyone gets stuck.

## The Journey You'll Take (If You Ignore This Advice)

**Month 1: "Let's follow Microsoft's advice"**
- Create subscription per department
- Seems simple and clean
- Matches the org chart perfectly

**Month 6: "Wait, this doesn't work"**
- Need security boundaries between prod and dev
- Can't give everyone subscription owner rights
- Cost reports show subscription totals, not application costs
- Finance asks "How much does the CostReporting app cost?" 
- You have no answer

**Month 12: "Everything is manual spreadsheets"**
- Cost allocation takes days of manual work
- Nobody trusts the numbers because they're estimates
- Leadership is frustrated: "We moved to cloud for better visibility"
- You're exporting CSVs and doing VLOOKUP formulas

**Month 18: "We need to count our apps"**
- Finally sit down and inventory all applications
- Realize which apps actually cost money
- Map applications to teams and DevOps projects
- Discover Finance has 30 apps, Data has 10, Infrastructure has 5
- **This is the work you should have done on Day 1**

**Month 24: "Finally, mature cost model"**
- Application-based tagging implemented
- Automated resource cost reporting via Azure Cost Management
- Manual allocation only for shared subscription services (networking, monitoring)
- Leadership gets accurate numbers without spreadsheets
- You can finally answer "How much does this app cost?"

## Why This Works

**Subscriptions as team boundaries:**
- Maps to your org chart
- Clear RBAC ownership (Data team owns Data subscriptions)
- Billing rolls up naturally (Finance team spending = Finance subscriptions)
- Avoids 100+ subscriptions (one per app would be insane)
- Prevents RBAC nightmare of shared subscriptions

**Tags as cost boundaries:**
- Tracks costs per application
- Works across subscriptions (app might use networking, monitoring)
- Enables accurate chargeback/showback
- Scales to hundreds of applications
- Answers "How much does this app cost?" in Cost Management

**You're not trying to force subscriptions to be both team boundaries AND cost boundaries.** That's the mistake everyone makes.

## The Day 1 Questions Nobody Asks

Before you create ANY subscriptions, answer:

1. **How many applications do you run?** (Not "how many teams")
2. **How many applications PER TEAM?** (Finance has 3 apps? 10 apps? 30 apps?)
3. **Which apps need production environments?** (Most? Some? Only revenue-generating?)
4. **Which apps share infrastructure?** (Database clusters, networking, security services?)
5. **Who deploys these apps?** (DevOps pipelines? Manual? Infrastructure team?)

**Then design subscriptions based on:**
- Security requirements (prod/dev separation)
- Networking requirements (private endpoints, ExpressRoute, firewall rules)
- Application count (can 100 apps share one subscription with good tagging?)
- Team ownership (who has admin rights to what?)

**NOT based on:**
- Department org chart alone
- "One subscription per team" as a default
- What sounds simple in a meeting

## The Mistakes to Avoid

**❌ One subscription per application**  
You'll have 100+ subscriptions. Management overhead will kill you. Subscription limits (980 VNets, 10 ExpressRoute circuits) will bite you.

**❌ One subscription per department**  
Then no team has admin rights. Everything goes through Infrastructure. Developers can't deploy. Innovation dies.

**❌ One giant subscription**  
RBAC becomes impossible. Cost tracking is a nightmare. Everyone can see everyone else's resources. Blast radius for mistakes is your entire estate.

**✅ Subscriptions = Teams. Tags = Apps.**

## The Tools That Help

Once you have this design, you need tools to manage it:

**Cost Reporting Workbooks:** Track spending per application across subscriptions. Azure Monitor Workbooks can aggregate costs by tag, showing you per-app spending even when resources span multiple subscriptions.

**Azure FinOps Toolkit:** Manages cost allocation at scale. When you have 31,000 resources across 44 subscriptions, you need automation. The toolkit helps enforce tagging, track costs, and generate reports.

**Resource Graph Queries:** Self-maintaining inventory. Query all resources by tag to see what applications exist, which teams own them, who's spending what. Your CMDB that actually stays current.

I'll cover these tools in detail in future posts. For now, understand: the tools only work if your subscription design makes sense.

## The Real Lesson

CAF gives you 50 pages of enterprise architecture patterns. Consultants will sell you months of design workshops. Microsoft assumes you're starting greenfield with perfect knowledge.

**Here's what actually matters:**

Before you create subscriptions, count your applications. Know how many each team owns. Understand which ones cost real money.

Then match subscriptions to your teams and tag by application.

The rest is details.

---

**Coming next:** How I enhanced Billy York's workbook to monitor 200+ Azure services (already published), and how we're using the Azure FinOps Toolkit to manage costs at 31k resources.

This is the foundation. Get it right on Day 1, or spend 18 months fixing it with spreadsheets.

I learned this managing 44 subscriptions and 31,000 resources through a merger consolidation. You can skip the pain.

---

### 🔍 Find the Unclaimed Apps

Run this query to find which resource groups are missing an application tag—these are your billing ghosts.

```kusto
// Find Resources WITHOUT an Application Tag
Resources
| where tags !has "Application"
| summarize Count=count(), EstimatedCost=sum(todouble(properties.billingDetails.resourceUsage)) by resourceGroup
| order by Count desc
```

---

*Want the KQL queries for resource inventory? Tag enforcement policies? Cost allocation workbooks? I'll share them in future posts. First, get your subscription design right.*

---

### 🛑 Apps Need Owners, Not Just Tags

Tagging apps is step one. Assigning a human responsible for the bill is step two.
**[Download the Azure RACI Matrix](https://davidnoob.gumroad.com/l/ifojm?ref=cost-batch-apps-model)** to define the 'Application Cost Owner' role.

<div class="downloads" style="text-align: center; margin-top: 2rem;">
  <a class="btn" href="https://davidnoob.gumroad.com/l/ifojm?ref=cost-batch-apps-model" style="font-size: 1.2em; padding: 15px 30px; background-color: #0078d4; color: white;">Get the FinOps RACI</a>
  <div class="preview-block" style="margin-top: 10px; font-size: 0.9em; color: #555;">
     <span>✅ Roles Included</span> • <span>💲 Price: $29</span> • <span>📊 Excel Format</span>
  </div>
</div>
