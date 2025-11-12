---
title: "The Spreadsheet I Wish I Had in 2019: Before You Migrate Anything to Azure"
date: 2025-11-12
summary: "In 2019, leadership said 'we're going to the cloud.' Nobody asked how many applications we had. That one question would have saved millions. Here's the spreadsheet that forces the conversation before you start migrating."
tags: ["Azure", "Cloud Migration", "Governance", "Enterprise Reality", "CAF"]
cover: "/static/images/hero/cloud-migration-spreadsheet.png"
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
