---
title: "Why Most Azure Migrations Fail: The Pre-Migration Reality Check Microsoft Won't Tell You"
date: 2025-11-12
modified: 2025-12-06
summary: "60% of Azure migrations exceed budget by 2x because teams skip one critical step: knowing what they have. Real lessons from enterprise migrations: the spreadsheet that prevents $2M budget overruns, timeline disasters, and post-migration chaos."
tags: ["azure", "Cloud Migration", "governance", "Enterprise Reality", "caf", "Migration Strategy", "Checklist", "Azure Migrate", "Migration Planning"]
cover: "/static/images/hero/cloud-migration-spreadsheet.png"
hub: "governance"
related_posts:
  - azure-migration-roi-wrong
  - azure-migrate-enterprise-hybrid
  - azure-migration-yard-sale-rolloff
  - application-migration-checklist-azure
---

# The Spreadsheet I Wish I Had in 2019: Before You Migrate Anything to Azure

## The Meeting

2019. Conference room. Leadership announces: **"We're going to the cloud."**

Someone from finance asks: "What will it cost?"

Leadership: "Less than what we spend now."

Someone from IT asks: "Which applications are we migrating?"

Leadership: "All of them."

Someone asks: "How many applications do we have?"

Silence.

Nobody knows.

**That's the moment this spreadsheet should have appeared on the projector.**

Not Azure Migrate. Not CAF documentation. Not consultant engagement proposals.

A simple spreadsheet with 55 questions that nobody could answer.

---

## What Azure Migrate Can't Prevent

Microsoft's [Azure Migrate service](https://learn.microsoft.com/en-us/azure/migrate/) provides excellent tools for discovery, assessment, and migration execution. The [assessment capabilities](https://learn.microsoft.com/en-us/azure/migrate/concepts-assessment-calculation) calculate Azure costs based on current server specifications and usage patterns. The [migration tools](https://learn.microsoft.com/en-us/azure/migrate/tutorial-migrate-physical-virtual-machines) handle the actual VM movement with minimal downtime.

What Azure Migrate can't do: **prevent the migration from failing before you ever use the tool.**

The #1 cause of migration failures isn't technical. It's organizational.

Leadership says "migrate all of them" before anyone has answered:
- How many applications do we have?
- Which servers support which applications?
- Who approved each workload for migration?
- What are the dependencies between systems?
- Which applications are actually still used?

**Azure Migrate assumes you already know these answers.** The [migration best practices](https://learn.microsoft.com/en-us/azure/migrate/best-practices-assessment) assume you have an application inventory, dependency maps, and business ownership documented.

Most organizations don't.

That's why 60% of Azure migrations exceed budget by 2x and timelines double.

Here's the pre-migration checklist that prevents this disaster.

---

## What Actually Happened

Without that forcing function, here's what we did:

**Month 1-3:** Azure training, CAF reading, subscription design debates

**Month 4-6:** Azure Migrate deployment, discovered we had 31,000+ resources nobody inventoried

**Month 7-9:** Started migrating "easy" applications we understood

**Month 10:** First migration failure - lost vendor contact, no installation media, license key in email from 2014

**Month 12:** Discovered 40% of applications had no documented owner

**Month 15:** CFO asks for cloud cost by department - we can't answer because subscriptions are security boundaries, not cost centers

**Month 18:** Consultant engagement to "fix" our migration strategy (aka do the inventory we should have done on day one)

**Cost:** Millions in wasted Azure spend, consulting fees, and staff time

**Root cause:** We started migrating before we knew what we owned.

---

## The Question That Changes Everything

**Before Azure Migrate. Before CAF. Before consultants.**

Ask this:

> **How many applications do we have?**

If you can't answer definitively, **stop.**

Don't design landing zones. Don't architect hub-and-spoke networks. Don't debate subscription naming conventions.

**Do an application inventory first.**

Because if you don't know how many applications you have, you also don't know:
- Who owns them
- Who maintains them
- If the vendor still exists
- Where the license keys are
- If anyone knows how they work
- Whether you should even migrate them

**This isn't a technical problem. It's an organizational maturity problem.**

---

## The Spreadsheet

I created the forcing function I wish I'd had in 2019.

**55 questions across 8 categories:**
1. Identity & Ownership (7 questions)
2. Vendor & Support (6 questions)
3. Technical Architecture (8 questions)
4. Licensing & Support Contracts (5 questions)
5. Business Value & Risk (4 questions)
6. Migration Planning (6 questions)
7. Compliance & Governance (5 questions)
8. Cost & Operations (9 questions)
9. Rationalization & Lifecycle (5 questions)

**Every question exposes institutional knowledge gaps that kill migrations.**

---

## Download

👉 **[Download Excel (.xlsx)](/static/downloads/Application_Questionnaire_Template_v2.xlsx)**  
👉 **[Download CSV version](/static/downloads/Application_Questionnaire_Template_v2.csv)**  

**Usage:**
- One spreadsheet per application
- Fill it out collaboratively (business + IT)
- If you can't answer 50% with high confidence → not ready to migrate yet
- If vendor contact person left 3 years ago → discovery work needed
- If "we think it's on ServerXYZ but not sure" → you're guessing

---

## The 55 Questions (And Why They Matter)

### Category 1: Identity & Ownership (Questions 1-7)

**These questions expose: Who's responsible when it breaks?**

1. What is this application called internally?
2. Which environment is it in (Prod/Dev/QA/DR)?
3. Which business unit or department owns this application?
4. How critical is this application to business operations (High/Medium/Low)?
5. Who is accountable for the business outcome if this app fails?
6. Who maintains the app day-to-day or handles incidents?
7. Which support queue or team handles this app?

**Why this matters:**

If you can't answer Question 5 ("Who's accountable if this fails?"), **you're about to migrate an application with no business owner.**

That means:
- Nobody to approve downtime windows
- Nobody to test post-migration
- Nobody to blame when it breaks in Azure (so IT gets blamed by default)
- Nobody who cares if you shut it down to save money

**Real example from my environment:**

Found an application consuming $2,400/month in Azure. Asked who owned it. Got three different answers. Traced it back - the business owner left the company in 2021. Application was still running. Nobody knew if anyone used it.

**If you can't answer "who's accountable," that application probably shouldn't migrate.**

---

### Category 2: Vendor & Support (Questions 8-9)

**These questions expose: Can we get help when it breaks?**

8. What is the software vendor or provider name?
9. Who do we contact for vendor support (email/phone)?

**Why this matters:**

Post-migration, the application breaks. You call the vendor. Their response: "Who are you? We don't have an active support contract with your company."

**Real example:**

Migrated a critical reporting application to Azure. Week 2, database connection fails. Called vendor for support. Vendor contact was Steve, who retired in 2018. New vendor contact had no record of our license. Support contract was signed in 2015 under a company name we no longer use (pre-merger).

Took 6 weeks to re-establish vendor relationship and get support. Application was down the entire time.

**If the person who maintains the vendor relationship left the company, you need to rebuild that relationship BEFORE migrating.**

---

### Category 3: Technical Architecture (Questions 10-17)

**These questions expose: Do we actually understand how this works?**

10. Is it on-prem, VM, SaaS, container, or hybrid?
11. Which OS, database, or runtime platform does it use?
12. What other apps, services, or databases does it depend on?
13. How do users authenticate (AD, local, custom)?
14. Does this application use a certificate? If yes, where is it stored and when does it expire?
15. Is this application behind a load balancer (Azure LB, F5, NSG, etc.)?
16. Is this application public-facing (accessible from the internet)?
17. Where is the installer or image stored?

**Why this matters:**

Question 12 ("What does it depend on?") is the migration killer.

Application A depends on Database B. Database B is shared by Applications C, D, and E. You can't migrate A without migrating B. But you can't migrate B until you migrate C, D, and E. Except E depends on Application F which you don't own.

**You just discovered your "simple" migration requires coordination across 6 applications and 3 business units.**

**Certificate story (Question 14):**

Migrated application to Azure. Worked great for 8 months. Then mysteriously stopped working. Nobody could figure it out.

Turns out: Certificate expired. Certificate was installed 6 years ago by someone who left. Nobody knew where the certificate request files were stored. Nobody knew the certificate password. Certificate was tied to a domain that was decommissioned in a merger.

Took 2 weeks to get new certificate issued and installed.

**If you don't know where certificates are and when they expire, expect surprises in Azure.**

---

### Category 4: Licensing & Support Contracts (Questions 18-22)

**These questions expose: Are we even allowed to run this in Azure?**

18. How is it licensed (per core, per user, subscription)?
19. Where is the license or agreement reference stored?
20. When does the vendor support contract expire?
21. Is the vendor still active and reachable?
22. Is this version still officially supported?

**Why this matters:**

Not all software licenses allow cloud hosting. Some licenses are tied to physical servers. Some licenses allow Azure but cost 3x more than on-premises.

**Real example:**

Migrated application to Azure. Vendor audit 6 months later: "Your license is for physical servers only. Running in Azure requires Enterprise Cloud License at $50K/year."

Nobody checked the license agreement before migration.

**Question 21 ("Is the vendor still active?") is brutal but necessary:**

We found applications from vendors who went out of business. Applications from vendors acquired by companies who discontinued the product. Applications from vendors who exist but no longer support this version.

**If the vendor is gone, you're on your own. That changes the migration decision.**

---

### Category 5: Business Value & Risk (Questions 23-26)

**These questions expose: Should we even migrate this?**

23. What business process does this application serve?
24. What happens if this app becomes unavailable?
25. What are the main issues or risks with this app?
26. Why are we migrating this app (cost, performance, compliance)?

**Why this matters:**

Question 23 ("What business process?") forces the business case conversation.

Sometimes the answer is: "We're not sure. We think HR uses it for something."

**That's your signal: This application is a retirement candidate, not a migration candidate.**

**Question 24 ("What happens if it's unavailable?") reveals truth:**

If the answer is "Nothing critical" or "We're not sure," **why are you spending money to migrate it?**

Test: Turn it off for a weekend. If nobody notices, retire it.

**Real example:**

Found 12 applications consuming $18K/month in Azure. Turned them off as a "maintenance window." Waited 2 weeks.

Zero complaints. Zero tickets.

Deleted them. Saved $216K/year.

**Not every application deserves migration. Some deserve deletion.**

---

### Category 6: Migration Planning (Questions 27-32)

**These questions expose: Are we actually ready?**

27. Which Azure service fits best (VM, App Service, SQL MI)?
28. Do we have updated documentation for this app?
29. Has ownership been verified recently?
30. Are all dependencies identified and documented?
31. Can this app be reinstalled from known media?
32. What is its readiness status (Green/Yellow/Red)?

**Why this matters:**

Question 31 ("Can it be reinstalled?") is the disaster recovery test.

If you can't reinstall the application from known media on-premises, **you definitely can't rebuild it in Azure when something goes wrong.**

**Real story:**

Application in Azure crashed. Needed to rebuild. Asked for installation media.

Answer: "We installed it in 2012. The ISO was on a file server that was decommissioned in 2017."

Spent 3 weeks trying to reconstruct the install. Eventually rebuilt from Azure Backup, but we were lucky.

**If you can't answer "where's the installer," you're not ready to migrate.**

---

### Category 7: Compliance & Governance (Questions 33-37)

**These questions expose: Will this pass audit?**

33. What type of data does it handle (Public/Internal/Confidential)?
34. Which compliance frameworks apply (PCI, HIPAA, SOX)?
35. Does it follow enterprise tagging standards?
36. What is its backup or DR tier level?
37. How many years of data retention are required?

**Why this matters:**

Question 34 ("Which compliance frameworks?") changes everything about where and how you migrate.

PCI data? Can't use certain Azure regions. Must use specific network configurations. Extra logging required.

HIPAA? BAA agreements with Microsoft. Specific encryption requirements. Audit logging mandatory.

**If you migrate before answering this, you fail your next audit.**

**Tagging (Question 35) is the cost allocation killer:**

Migrated 500 VMs to Azure. CFO wants cost by department. You need tags.

But you didn't tag during migration. Now you have to:
- Identify which department owns each VM (nobody remembers)
- Apply tags retroactively (manual work)
- Handle exceptions (PaaS services that auto-create resources without tags)

**Should have tagged during migration. Can't fix it easily afterward.**

---

### Category 8: Cost & Operations (Questions 38-41)

**These questions expose: Can we actually afford this?**

38. Which cost center or charge code funds this app?
39. What will it cost monthly in Azure?
40. What does it currently cost to host?
41. Can it be optimized, consolidated, or retired?

**Why this matters:**

Question 39 vs. 40 (Azure cost vs. current cost) is where migration ROI dies.

On-prem: $800/month (amortized hardware, shared infrastructure)  
Azure: $2,400/month (VM + storage + backup + bandwidth + PaaS services)

**Cloud doesn't automatically save money.** Sometimes it costs 3x more.

**Real example:**

Migrated application to Azure. Cost $4,200/month. Business owner shocked. "I thought cloud was supposed to be cheaper?"

Current cost on-prem: $1,100/month.

**If we'd answered Questions 39 & 40 before migrating, we would have killed this migration.**

---

## Azure Migration Cost Reality: What the Spreadsheet Reveals

**The question everyone asks: "What will Azure migration cost?"**

**The honest answer: "More than leadership expects, less than doing nothing."**

Here's what your spreadsheet reveals about actual Azure migration costs that sales presentations never mention.

### The Three Cost Categories Nobody Budgets For

**1. Migration Execution Costs (One-Time)**

What leadership budgets:
- Azure Migrate licensing: $0 (free tool)
- Network bandwidth: Included in current costs
- Staff time: "They're already employees"

**What it actually costs:**

```
Discovery phase: 3-6 months × $15K/month consulting = $45-90K
Assessment tools: Azure Migrate + dependency mapping = $0-5K
Migration tooling: Azure Site Recovery, migration services = $0-15K
Network acceleration: ExpressRoute setup or increased bandwidth = $10-50K
Staff overtime/contractors: Weekend migrations, rollbacks = $20-50K
Training: Azure certifications, vendor training = $5-15K
Consultant fees: When internal team gets stuck = $50-200K

Total migration execution: $130K - $425K (for 50-100 applications)
Per-application cost: $1,300 - $4,250 each
```

**The spreadsheet forces this conversation on Day 1, not Month 12.**

**2. Post-Migration Azure Costs (Recurring Monthly)**

Leadership expectations based on sales pitch:
```
Current on-prem: $50K/month
Azure promise: 30% savings
Expected Azure cost: $35K/month
```

**Actual Azure costs after migration:**

```
Compute (VMs right-sized up): $28K/month
Storage (3x redundancy, premium for databases): $12K/month
Networking (ExpressRoute, VPN, bandwidth): $8K/month
Backup & DR (Azure Site Recovery, snapshots): $6K/month
Security (Defender, Key Vault, firewalls): $4K/month
Monitoring (Log Analytics, Application Insights): $3K/month
PaaS migrations (SQL MI, App Service): $15K/month

Actual Azure monthly: $76K/month
vs. Current on-prem: $50K/month
Increase: +52% ($26K/month more)
```

**Why the increase?**

- On-prem costs were amortized (hardware paid off)
- Azure charges for redundancy you got "free" on-prem
- Bandwidth charges that didn't exist on-prem
- Premium storage for performance parity
- Backup costs now explicit (were "free" on SAN)

**Question 39 vs. 40 from the spreadsheet prevents this surprise.**

**3. Hidden Operational Costs (Ongoing)**

Costs that appear 6-12 months post-migration:

```
License true-ups: Vendor audits reveal under-licensing = $50-200K
Failed migrations redo: Applications that don't work, rebuild = $25-100K
Performance fixes: Right-sizing, premium storage upgrades = $10-50K/year
Compliance gaps: Encryption, logging, audit requirements = $15-40K
Training updates: Continuous Azure training as services change = $10-30K/year
Consultant retainer: For issues internal team can't solve = $60-150K/year

Hidden first-year costs: $170K - $570K
```

**Total Cost of Migration Example:**

```
Pre-migration assessment (using spreadsheet): $15K consulting
Migration execution: $300K
First year Azure operations: $912K (76K × 12)
Hidden costs first year: $370K

Total Year 1: $1,597K
vs. On-prem Year 1: $600K (50K × 12)

Cloud migration cost increase: +$997K first year
Break-even: Year 3-4 (if you optimize aggressively)
```

**The spreadsheet doesn't prevent these costs. It makes them visible BEFORE you commit.**

### Azure Migrate Tool Cost vs. This Spreadsheet Approach

**Azure Migrate (Microsoft's free tool):**

What it does well:
- Discovers VMs and dependencies automatically
- Performance baseline data collection
- Right-sizing recommendations
- Cost estimates based on VM metrics

**What it doesn't do:**

- ❌ Can't tell you if the business owner left the company
- ❌ Can't tell you where the installer ISO is stored
- ❌ Can't tell you if the vendor still exists
- ❌ Can't tell you if license allows cloud hosting
- ❌ Can't tell you if anyone actually uses the application
- ❌ Can't tell you what the long-term plan is

**Azure Migrate discovers resources. This spreadsheet discovers organizational readiness.**

**You need both.**

```
Week 1-4: Deploy Azure Migrate (technical discovery)
Week 5-12: Fill out spreadsheet per application (business discovery)
Week 13+: Decide what to migrate based on BOTH datasets
```

**Cost comparison:**

```
Azure Migrate only:
- Cost: $0 (free tool)
- Result: Accurate technical inventory, inaccurate business understanding
- Risk: Migrate wrong applications, miss retirement candidates
- Wasted spend: $500K - $2M on migrations that shouldn't happen

Azure Migrate + Spreadsheet:
- Cost: $15K (consulting to facilitate spreadsheet completion)
- Result: Accurate technical + business inventory
- Risk: Only migrate what makes business sense
- Savings: $500K - $2M avoided waste

ROI: 33x to 133x return on spreadsheet investment
```

**The spreadsheet is the cheapest insurance policy in your Azure migration.**

---

### Category 9: Rationalization & Lifecycle (Questions 42-52)

**These questions expose: What's the actual plan?**

42. What is its migration priority (High/Med/Low)?
43. How many servers/VMs are part of this app?
44. Which databases are associated with this app?
45. Is there an existing monitoring dashboard or link?
46. How often does it generate incidents (monthly avg)?
47. Are there legacy or unsupported components?
48. What's the rationalization plan (Rehost, Refactor, etc.)?
49. Has leadership approved migration or disposition?
50. When was it last validated as still needed?
51. What is the long-term plan (SaaS replacement, retire)?
52. When should it be re-evaluated (6mo/12mo)?

**Why this matters:**

Question 48 ("Rationalization plan") forces the 7R decision BEFORE migration:
- **Rehost** (lift-and-shift to IaaS)
- **Refactor** (small code changes for PaaS)
- **Rearchitect** (significant redesign)
- **Rebuild** (rewrite from scratch)
- **Replace** (buy SaaS alternative)
- **Retire** (delete it)
- **Retain** (keep on-prem)

**Most organizations default to Rehost (lift-and-shift) because they don't understand the application well enough to choose anything else.**

But Rehost is often the most expensive option.

**Question 51 ("Long-term plan?") changes the migration decision:**

If the answer is "Replace with Salesforce in 18 months," **don't migrate it to Azure.**

Keep it on-prem for 18 months, then turn it off when Salesforce goes live.

**We migrated applications with 12-month retirement dates. Wasted money on migrations that should never have happened.**

---

## The Red Flags

**As you fill out the spreadsheet, watch for these danger signs:**

🚩 **"I think it's owned by..."** → Ownership not validated  
🚩 **"The person who knew this left in 2020"** → Institutional knowledge loss  
🚩 **"We're not sure where the installer is"** → Can't rebuild if it breaks  
🚩 **"The vendor might still support it"** → Licensing risk  
🚩 **"Low confidence" on multiple answers** → Not ready to migrate  
🚩 **"We'll figure it out after migration"** → Recipe for disaster  
🚩 **Can't answer Questions 5, 9, 17, or 31** → STOP. Do discovery first.

**Each red flag adds risk. Three or more red flags = don't migrate yet.**

---

## How to Use This Spreadsheet

**Step 1: Leadership announces "we're going to the cloud"**

Stop. Don't start designing Azure architecture.

**Step 2: Open the spreadsheet**

Project it in the conference room.

**Step 3: Ask: "How many applications do we have?"**

If nobody knows → Discovery project comes before migration project.

**Step 4: For each application, fill out the questionnaire**

- Business owner answers business questions (1-7, 23-26, 38-41)
- IT answers technical questions (10-17, 27-32, 42-47)
- Compliance answers governance questions (33-37)
- Everyone collaborates on vendor/licensing (8-9, 18-22)

**Step 5: Count the red flags**

- 0-2 red flags: Probably ready to migrate
- 3-5 red flags: Need discovery work first
- 6+ red flags: Not ready, might be retirement candidate

**Step 6: Only then, decide the 7R action**

Rehost, Refactor, Rearchitect, Rebuild, Replace, Retire, or Retain.

**Step 7: Prioritize based on readiness, not executive preference**

Migrate applications with **high business value + low red flags** first.

Don't migrate applications with **low business value + high red flags**. Retire them instead.

---

## Azure Cloud Migration Strategy: The Right Sequence

**Microsoft's CAF documentation starts with landing zones and governance.**

**That's backwards.**

**Here's the actual sequence that prevents migration failure:**

### Phase 1: Discovery (Months 1-3)

**Goal:** Know what you own before deciding what to migrate.

**Activities:**
1. Deploy Azure Migrate for technical discovery
2. Deploy spreadsheet for organizational discovery
3. Identify application owners (or lack thereof)
4. Document dependencies across applications
5. Classify applications by criticality and readiness

**Deliverables:**
- Complete application inventory with owners
- Dependency maps showing migration complexity
- Red flag count per application
- Preliminary retirement candidate list

**Exit criteria:** Can answer "How many applications do we have?" with confidence

### Phase 2: Rationalization (Months 3-4)

**Goal:** Decide the 7R action for every application BEFORE designing Azure architecture.

**The 7Rs with spreadsheet guidance:**

**Rehost (Lift-and-Shift):**
- Spreadsheet shows: Green status, simple architecture, no compliance issues
- Best for: Applications with short remaining life (2-4 years)
- Azure target: IaaS VMs
- Cost: Moderate (highest Azure spend, lowest migration effort)

**Refactor (Minor Changes for PaaS):**
- Spreadsheet shows: Modern architecture, documented dependencies, active vendor
- Best for: Applications worth investing in
- Azure target: App Service, SQL Database, Container Apps
- Cost: Moderate (lower Azure spend, moderate migration effort)

**Rearchitect (Significant Redesign):**
- Spreadsheet shows: Core business app, high value, legacy architecture
- Best for: Strategic applications, 5+ year lifespan
- Azure target: Microservices, serverless, PaaS
- Cost: High (lowest Azure spend long-term, highest migration effort)

**Rebuild (Rewrite from Scratch):**
- Spreadsheet shows: No vendor support, no installation media, critical business value
- Best for: Applications you can't live without but can't migrate
- Azure target: Modern stack (React, .NET Core, PostgreSQL)
- Cost: Highest (migration effort = new development)

**Replace (Buy SaaS Alternative):**
- Spreadsheet shows: Generic business function, vendor exists, high maintenance cost
- Best for: Commodity applications (email, CRM, HR)
- Azure target: SaaS product (Salesforce, Workday, M365)
- Cost: Moderate (no migration effort, subscription fees)

**Retire (Delete It):**
- Spreadsheet shows: No owner, no business value, can't answer basic questions
- Best for: 20-40% of your application portfolio
- Azure target: None (decommission)
- Cost: Lowest (savings from deletion)

**Retain (Keep On-Premises):**
- Spreadsheet shows: Compliance restriction, vendor limitation, hardware dependency
- Best for: Regulated workloads, specialized hardware
- Azure target: None (stays on-prem or hybrid)
- Cost: Zero migration (status quo)

**Typical distribution after spreadsheet completion:**

```
50-60% → Rehost (lift-and-shift to Azure VMs)
10-15% → Refactor (PaaS migration)
5-10% → Rearchitect (strategic redesign)
2-5% → Rebuild (complete rewrite)
10-15% → Replace (buy SaaS)
20-40% → Retire (delete)
5-10% → Retain (keep on-prem)
```

**Notice: 20-40% retirement rate is normal and healthy.**

**The spreadsheet reveals retirement candidates that executive mandates hide.**

### Phase 3: Planning (Months 4-6)

**Goal:** Design Azure architecture for the applications that survived rationalization.

**Now you can design landing zones because you know:**
- How many subscriptions you need (based on apps migrating)
- Which compliance requirements apply (from spreadsheet)
- Network requirements (based on dependency maps)
- Cost center allocation (from business owner data)
- Governance policies needed (based on data classification)

**Architecture decisions driven by spreadsheet data:**

```
Compliance requirements (Question 34) → Azure region selection
Data classification (Question 33) → Network isolation design
Business criticality (Question 4) → SLA and redundancy levels
Dependencies (Question 12) → Migration wave grouping
Cost centers (Question 38) → Subscription structure
```

**This is when you read CAF documentation - after you know what you're building for.**

### Phase 4: Pilot (Months 6-9)

**Goal:** Validate approach with low-risk applications.

**Pilot selection criteria from spreadsheet:**

Choose applications with:
- ✅ Green readiness status (low red flag count)
- ✅ Low business criticality (failure won't kill company)
- ✅ Simple architecture (few dependencies)
- ✅ Active vendor support (can get help if needed)
- ✅ Documented owner (someone to test and approve)

**Don't choose:**
- ❌ Most critical application (too risky for pilot)
- ❌ Most complex application (too many variables)
- ❌ Application with vendor issues (will confuse pilot results)
- ❌ Application with no owner (can't validate success)

**Pilot success metrics:**

- Migration completed within time estimate (±20%)
- Application works in Azure (full functionality)
- Performance acceptable (meets SLAs)
- Cost within estimate (±30%)
- Business owner satisfied (would migrate more)

**If pilot fails, fix issues before scaling. Don't blame Azure - blame incomplete discovery.**

### Phase 5: Migration Waves (Months 9-24)

**Goal:** Systematic migration in prioritized groups.

**Wave planning based on spreadsheet:**

**Wave 1 (Months 9-12): Quick Wins**
- Applications: High value + low risk (green status + simple)
- Goal: Build momentum and confidence
- Typical: 10-20 applications

**Wave 2 (Months 12-18): Strategic Applications**
- Applications: High value + moderate risk (yellow status)
- Goal: Migrate core business applications
- Typical: 20-40 applications

**Wave 3 (Months 18-24): Complex Migrations**
- Applications: High value + high risk (red flags but necessary)
- Goal: Tackle difficult migrations with lessons learned
- Typical: 10-30 applications

**Wave 4 (Months 24-36): Long Tail**
- Applications: Low value + low risk (keep if cheap to migrate)
- Goal: Finish remaining migrations
- Typical: 20-50 applications

**Total migrated: 60-140 applications over 3 years**

**Not migrated (retired): 40-80 applications discovered through spreadsheet**

**Money saved from retirements: Often exceeds migration costs**

---

## The Conversation This Forces

**CFO:** "How much will Azure cost?"

**You:** "Can't answer yet. We don't know how many applications we're migrating."

**CFO:** "Well how many applications do we have?"

**You:** "That's what this spreadsheet helps us determine. Fill out these 55 questions for each application, then we can estimate cost."

**CFO:** "That sounds like it will take months."

**You:** "Yes. And if we skip it, the migration will cost 3x more and take twice as long. Choose."

**This spreadsheet gives you the forcing function to have that conversation on day one, not year two.**

---

## What Success Looks Like

**Mature organization (ready to migrate):**

Every application has:
- ✅ Documented business owner with accountability
- ✅ Current vendor contact information
- ✅ Known installation media location
- ✅ Valid support contracts
- ✅ Documented dependencies
- ✅ Cost center assignment
- ✅ Compliance classification
- ✅ Rationalization decision (7R)
- ✅ Leadership approval

**Every question answered with HIGH confidence.**

**Immature organization (not ready):**

Applications have:
- ❌ "I think Bob owned this but he left"
- ❌ "Vendor contact in email from 2015"
- ❌ "Install media on a server we decommissioned"
- ❌ "Support contract maybe expired?"
- ❌ "Not sure what it depends on"
- ❌ "Cost center TBD"
- ❌ "Probably not HIPAA data?"
- ❌ "Leadership said migrate everything"

**Most questions answered with LOW confidence or not at all.**

**If you're the second organization, this spreadsheet saves you from expensive migration failure.**

---

## Common Azure Migration Mistakes This Spreadsheet Prevents

**Mistake #1: Migrating Applications Nobody Uses**

**How it happens:**

Executive mandate: "Migrate everything to Azure by Q4."

IT response: "Okay, here's the server list from VMware. We'll migrate all of them."

Nobody asks: "Does anyone actually use ServerXYZ-2014?"

**The cost:**

Migrated application consuming $1,800/month in Azure. Ran for 18 months before someone asked "What is this?"

Investigation revealed: Application was replaced by SaaS product in 2020. Old server still running. Nobody shut it off.

**Cost of not asking: $32,400 wasted ($1,800 × 18 months)**

**How spreadsheet prevents this:**

Question 23: "What business process does this application serve?"  
Question 50: "When was it last validated as still needed?"

If you can't answer both with confidence → Retirement candidate, not migration candidate.

---

**Mistake #2: Ignoring Vendor Licensing Restrictions**

**How it happens:**

You migrate application to Azure. Works great. Six months later, vendor audit letter arrives: "Your license doesn't permit cloud hosting. Please purchase Cloud License at $75K/year or cease Azure usage within 30 days."

**How common is this:**

Happens with:
- Oracle databases (license per core changes in cloud)
- SQL Server (need Azure Hybrid Benefit setup correctly)
- Third-party applications with "on-premises only" licenses
- Vendor products with separate cloud SKUs

**The cost:**

Emergency license purchase: $75K  
Or emergency migration back to on-prem: $50K + downtime  
Or cease business process: Unacceptable

**How spreadsheet prevents this:**

Question 18: "How is it licensed?"  
Question 21: "Is the vendor still active and reachable?"  
Question 22: "Is this version still officially supported?"

**Action:** Contact vendor BEFORE migration. Get cloud licensing terms in writing.

For a deep dive into the most common licensing mistake that causes $50K+ audit penalties, read: [The $50K Licensing Mistake Noobs Make](/blog/azure-hybrid-benefit-licensing-mistake/)

---

**Mistake #3: Dependency Hell**

**How it happens:**

You migrate Application A to Azure. It breaks. Investigation reveals Application A depends on Database B which is still on-premises and requires 1ms latency that doesn't work across ExpressRoute.

Now you need to migrate Database B. But Database B supports Applications C, D, E, and F - all of which need testing if you migrate the database.

**Your "simple" Application A migration just became 6 applications.**

**The cost:**

Planned migration budget: $25K (one app)  
Actual migration cost: $180K (six apps + coordination + testing)

Budget overrun: 7.2x planned cost

**How spreadsheet prevents this:**

Question 12: "What other apps, services, or databases does it depend on?"  
Question 30: "Are all dependencies identified and documented?"

**If you can't map full dependency chain, you're not ready to migrate.**

Use Azure Migrate dependency mapping + manual verification through interviews.

---

**Mistake #4: Lost Installation Media**

**How it happens:**

Application breaks in Azure. Needs rebuild. Ask for installation media.

Answer: "We don't have it. Original installer was on Bob's laptop. Bob left in 2019."

Recovery options:
1. Try to restore from Azure Backup (might work)
2. Contact vendor for new installer (might not match configuration)
3. Rebuild from documentation (if it exists)
4. Give up and find SaaS replacement (expensive surprise)

**The cost:**

3 weeks of senior engineer time trying to rebuild: $30K  
Consultant engagement to help: $20K  
Emergency SaaS replacement: $50K implementation + $2K/month  
Business impact from downtime: Incalculable

**Total unexpected cost: $100K+**

**How spreadsheet prevents this:**

Question 17: "Where is the installer or image stored?"  
Question 31: "Can this app be reinstalled from known media?"

**If answer is "No" or "We think so but not sure" → Fix this BEFORE migrating.**

---

**Mistake #5: No Business Owner = No Accountability**

**How it happens:**

You migrate application to Azure. Post-migration validation needed. Who tests it?

Try to find business owner. Original owner left in 2020. Department reorganized twice since then. Nobody knows who owns this application now.

Application is running in Azure. Consuming $2,200/month. Nobody responsible. Nobody testing. Nobody knows if it works correctly.

**The cost:**

Application runs for 2 years in Azure: $52,800  
Nobody validates it works correctly  
Internal audit flags: "No owner documented for 47 applications"  
Consultant engagement to identify owners: $45K  
Cleanup project to retire orphaned apps: $80K

**Total waste: $177,800**

**How spreadsheet prevents this:**

Question 5: "Who is accountable for the business outcome if this app fails?"  
Question 29: "Has ownership been verified recently?"

**If you can't identify current owner with contact information → Don't migrate until you do.**

---

**Mistake #6: Certificate Expiration Surprise**

**How it happens:**

Application works in Azure for 11 months. Month 12, it stops working. Nobody knows why.

After days of troubleshooting: Certificate expired. Certificate was installed 4 years ago by contractor who left. Nobody knew certificate existed. Nobody monitored expiration.

Certificate renewal requires:
- Finding original certificate request files (lost)
- Getting new certificate issued (2 week process)
- Installing without breaking production (risky)

**The cost:**

Application downtime: 12 days  
Emergency contractor to rebuild certificate: $15K  
Business impact from outage: $50K+

**How spreadsheet prevents this:**

Question 14: "Does this application use a certificate? If yes, where is it stored and when does it expire?"

**Document ALL certificates BEFORE migration. Set up expiration monitoring.**

---

**Mistake #7: Compliance Violations**

**How it happens:**

You migrate application to Azure. Works great. 6 months later, compliance audit.

Auditor question: "This application processes PCI cardholder data. Where's your Azure PCI attestation?"

Your answer: "We didn't know it processed PCI data."

Audit finding: **Non-compliance. Remediate within 30 days or lose ability to process cards.**

**The cost:**

Emergency PCI remediation:
- Move application to compliant Azure region: $25K
- Implement required logging: $15K
- Network isolation fixes: $35K
- Audit validation: $20K

Total unbudgeted cost: $95K

**How spreadsheet prevents this:**

Question 33: "What type of data does it handle?"  
Question 34: "Which compliance frameworks apply?"

**If answer includes PCI, HIPAA, SOX, etc. → Architecture changes BEFORE migration.**

---

**The Pattern:**

Every mistake has the same root cause: **Incomplete discovery before migration.**

The spreadsheet forces complete discovery before you spend money.

**Better to discover problems during spreadsheet completion (cost: $0) than during Azure migration (cost: $$$$$).**

---

## The Bottom Line

**Before Azure Migrate. Before CAF. Before consultants. Before landing zones.**

**Answer this spreadsheet for every application.**

If you can't answer 50% of the questions with high confidence, **you're not ready to migrate yet.**

That's not failure. **That's clarity.**

Discovering you're not ready on day one costs nothing.

Discovering you're not ready in month 18 after spending millions? That's expensive.

**This spreadsheet is the forcing function I wish I'd had in 2019.**

You have it now. Use it.

---

## Download Again (In Case You Missed It)

👉 **[Download Excel (.xlsx)](/static/downloads/Application_Questionnaire_Template_v2.xlsx)**  
👉 **[Download CSV version](/static/downloads/Application_Questionnaire_Template_v2.csv)**  

**Fill it out. Get red flags. Do discovery work.**

**Then migrate what's ready. Retire what's not.**

Stop guessing. Start knowing.

---

## What Comes After This Spreadsheet

**Once you have answers to these 55 questions for each application:**

1. **Prioritize migrations** (high value + low risk first)
2. **Identify retirement candidates** (low value + high risk)
3. **Calculate actual Azure costs** (now that you know what you're migrating)
4. **Build your landing zones** (now that you know what lands in them)
5. **Design governance** (now that you know what you're governing)
6. **Start migrating** (with realistic expectations and timelines)

**Microsoft's CAF documentation assumes you already did this work.**

**Most organizations skip it and wonder why migrations fail.**

Don't skip it.

---

**Want more operational reality checks?** Subscribe below for Azure content that addresses the problems Microsoft's documentation ignores.

*The spreadsheet that should have been in CAF documentation - but isn't.*
