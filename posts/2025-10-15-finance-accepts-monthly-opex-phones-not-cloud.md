---
title: "Finance Accepts Monthly OpEx for Phones. Why Not Cloud?"
date: 2025-10-15
summary: "Nobody questions paying Verizon instead of building cell towers. Apps on your phone = value. The network = enabler. Finance gets it. So why do they question the same model for Azure?"
tags: ["azure", "FinOps", "Leadership", "ROI", "OpEx"]
cover: "static/images/hero/phone-azure-same-thing.png"
hub: governance
related_posts:
  - azure-resource-tags-guide
  - azure-tag-governance-policy
  - azure-policy-reality-check
---
# Finance Accepts Monthly OpEx for Phones. Why Not Cloud?


This guide is part of our [Azure Governance hub](/hub/governance/) covering policy enforcement, compliance frameworks, and enterprise controls.

I was in a budget meeting when the CFO asked: "Why are we paying Microsoft monthly for Azure? Can't we just own the servers?"

I pulled out my phone and set it on the table.

"How much does Verizon charge you per month?" I asked.

"About $120," she said.

"Ever think about building your own cell towers instead?"

She laughed. "That would be ridiculous."

"Why?"

"Because... it's obviously cheaper to pay monthly for service than build and maintain cellular infrastructure."

**I pointed at the Azure budget on her screen.**

"It's the same thing."

## The Question Finance Never Asks

**Nobody in Finance has ever said:**

"What's the ROI of paying Verizon $120/month versus building our own cellular network?"

**Because everyone instinctively understands:**
- Building cell towers: $Millions in capital
- Maintaining towers: Ongoing operational cost
- Geographic coverage: Need towers everywhere
- Technology upgrades: 3G → 4G → 5G requires infrastructure replacement
- Regulatory compliance: FCC licensing, spectrum auctions
- Disaster recovery: Redundant infrastructure
- 24/7 operations: Staff, monitoring, maintenance

**Versus:**
- Pay Verizon: $120/month
- It just works
- Coverage everywhere
- Automatic upgrades
- Someone else's problem

**The calculation is so obvious that Finance never even asks the question.**

## The Question Finance Always Asks

But with Azure, the same CFO asks:

"What's the ROI of paying Microsoft monthly versus owning our own servers?"

**Why is this different?**

It's not. It's the exact same economic model:

**Building data centers:**
- $Millions in capital (building, power, cooling)
- Ongoing operational cost (utilities, staff, maintenance)
- Geographic redundancy (multiple locations for DR)
- Technology refresh (servers replaced every 3-5 years)
- Compliance and security (certifications, audits, physical security)
- 24/7 operations (monitoring, incident response)

**Versus:**
- Pay Microsoft: Monthly based on usage
- It just works
- Global infrastructure
- Automatic upgrades
- Microsoft's problem

**The calculation is identical to the cell phone decision. But Finance treats them completely differently.**

## Why Finance Gets One But Questions The Other

**Cell phones are personal.** Everyone in Finance carries one. They understand the value proposition intuitively because they experience it daily.

**Data centers are abstract.** Most Finance people have never visited a data center. They don't see the complexity. They just see "servers" and assume they're like buying office furniture - a one-time capital expense.

**The mental model is wrong.**

Finance thinks:
- Cell phone service = Ongoing utility (like electricity)
- Data center = Capital asset (like a building)

**The reality:**
- Cell phone service = Infrastructure as a Service
- Azure = Infrastructure as a Service

**They're the same category. Just different scales.**

## The Apps Are The Value (Both Times)

Here's what Finance actually understands about cell phones:

**The phone itself isn't valuable.**

A $1,000 iPhone without service and apps is a paperweight. An expensive, pretty paperweight, but useless for business.

**The apps are the value:**
- Email (business communication)
- Slack (team collaboration)  
- Salesforce mobile (CRM on the go)
- Banking apps (financial management)
- Calendar (scheduling)
- GPS (logistics, travel)

**The cellular network is the enabler** that makes those applications work.

Finance doesn't question paying $120/month for cellular service because they understand the business value of the applications that run on it.

## Azure Is The Same Model

**Azure itself isn't valuable.**

Virtual machines sitting idle in a data center are just consuming electricity. Expensive electricity, but producing zero business value.

**The applications are the value:**
- ERP (business operations)
- CRM (customer relationships)
- Customer portals (revenue generation)
- HR systems (workforce management)
- Finance applications (compliance, reporting)

**The Azure platform is the enabler** that makes those applications work.

**So why does Finance question paying monthly for Azure but not for Verizon?**

## The Double Standard

**Finance doesn't ask:**
- "Can we quantify the ROI of cell service versus building towers?"
- "What's our cell phone OpEx compared to owning infrastructure?"
- "How much would we save if we built our own cellular network?"

**Because the answer is obvious:** Building cellular infrastructure is insane for a business that isn't in the telecom industry.

**But Finance does ask:**
- "Can we quantify the ROI of Azure versus owning servers?"
- "What's our cloud OpEx compared to capital investment in data centers?"
- "How much would we save if we bought our own hardware?"

**And IT has to justify why the obvious answer isn't obvious.**

## The Real Question Finance Should Ask

**Not:** "What's the ROI of Azure versus on-premises?"

**Instead:** "What applications run our business, and what's the best platform for them?"

**For cell phones, Finance already asked this:**

"What applications do our employees need to do their jobs effectively?"
- Email, Slack, Salesforce, banking, calendar, GPS

"What platform enables those applications?"
- Cellular service from Verizon/AT&T/T-Mobile

"What's the best way to provide that platform?"
- Pay monthly for service (obviously not building towers)

**For Azure, Finance should ask the same questions:**

"What applications run our business?"
- ERP, CRM, customer portals, HR systems, finance applications

"What platform enables those applications?"
- Cloud infrastructure (compute, storage, networking)

"What's the best way to provide that platform?"
- Pay monthly for Azure (obviously not building data centers)

**The answer is the same. The logic is identical. The economics are parallel.**

## What Happens Without The Platform

**Cell phone without service:**

You have a $1,000 device that:
- Can't make calls
- Can't send messages  
- Can't run email
- Can't access Slack
- Can't use Salesforce
- Can't navigate with GPS

**Business impact:** Employees can't communicate, collaborate, or access business applications. Operations grind to a halt.

**Azure without infrastructure:**

You have applications that:
- Can't serve customers
- Can't process orders
- Can't manage inventory
- Can't track finances
- Can't support operations

**Business impact:** The business stops functioning.

**In both cases, the platform is essential because the applications are essential.**

Finance understands this for cell phones. They need to understand it for Azure.

## The OpEx Model Finance Already Accepts

**Finance doesn't blink at monthly payments for:**

**Cell service:** $120/month per person
- 1,000 employees = $120,000/month = $1.44M/year
- Nobody asks for ROI
- Nobody questions why we don't build towers
- Accepted as necessary business expense

**Internet connectivity:** $5,000+/month for enterprise circuits
- Multi-location WAN = $50K+/month
- Nobody asks why we don't lay our own fiber
- Accepted as necessary infrastructure

**SaaS applications:** $Thousands/month
- Office 365, Salesforce, Workday, etc.
- Nobody asks why we don't host email ourselves
- Accepted as modern way to consume software

**But Azure VMs:** "Why are we paying monthly for infrastructure?"

**The cognitive dissonance is astounding.**

## The Argument That Wins

Next time Finance questions Azure's monthly costs, try this:

**Finance:** "Why are we paying monthly for cloud infrastructure?"

**You:** "Same reason we pay monthly for cell service. We need a platform to run business applications, and it's cheaper to rent than build."

**Finance:** "But we could own servers for less."

**You:** "Could we own cell towers for less than paying Verizon?"

**Finance:** "That's different."

**You:** "How? In both cases:
- We're paying monthly for infrastructure
- Someone else maintains it
- We get automatic upgrades
- We avoid capital investment
- We get geographic redundancy
- The platform enables business applications"

**Finance:** "..."

**You:** "You understand why paying Verizon makes sense. Azure is the same model, just for business applications instead of personal ones."

**If they still push back:**

"Would you rather explain to the board why email is down because our cell service contract wasn't renewed, or why customer orders aren't processing because we tried to save money running our own data center?"

## The Apps ARE The Business

**Here's what Finance needs to understand:**

The business doesn't run on Azure. The business runs on:
- ERP (SAP, Oracle, Dynamics)
- CRM (Salesforce, Dynamics)
- Customer portals
- E-commerce platforms
- Finance and HR systems

**Azure is just where those applications live.**

Just like:
- Business communication doesn't run on Verizon
- It runs on email, Slack, Teams
- **Verizon is just where those applications work**

**In both cases:**
- Applications = Value
- Platform = Enabler

**Finance accepts monthly payment for the cellular platform because they understand the value of mobile applications.**

**Finance should accept monthly payment for the cloud platform because business applications have the same value equation.**

## The Comparison Finance Can't Argue With

| Decision | Build It Yourself | Pay Monthly | Finance Chooses |
|----------|------------------|-------------|-----------------|
| **Cell Service** | Build towers, spectrum licensing, FCC compliance, maintain network | Pay Verizon $120/month | Pay Monthly ✅ |
| **Internet** | Lay fiber, maintain infrastructure, BGP routing | Pay ISP $5K/month | Pay Monthly ✅ |
| **Email** | Run Exchange servers, storage, backups, security | Pay Microsoft for Office 365 | Pay Monthly ✅ |
| **Cloud Infrastructure** | Build data centers, buy servers, hire staff, maintain everything | Pay Azure monthly | ??? 🤔 |

**Three out of four decisions, Finance immediately chooses monthly OpEx.**

**The fourth decision is identical in every way that matters.**

**Why is it treated differently?**

## The Real Reason For The Double Standard

**Familiarity.**

Finance uses cell phones every day. They experience the value. They understand why paying monthly makes sense.

Finance doesn't interact with data centers. They're abstract. So Finance defaults to treating them like capital assets - buildings, furniture, equipment.

**The solution:** Help Finance understand that Azure is cellular service for business applications.

**Not:** "Trust me, cloud is better"

**Instead:** "You already made this exact decision with cell phones. Azure is the same model."

## The Bottom Line

**Finance accepts paying Verizon instead of building cell towers because:**
- Apps on phones deliver business value
- Cellular network enables those apps
- Monthly OpEx is obviously cheaper than building infrastructure
- Everyone understands this intuitively

**Finance should accept paying Microsoft instead of building data centers because:**
- Apps in Azure deliver business value  
- Cloud platform enables those apps
- Monthly OpEx is obviously cheaper than building infrastructure
- **It's the exact same logic**

**The apps are the value. The platform is the enabler.**

**Finance gets this for cell phones. They need to get it for cloud.**

Next time Finance questions your Azure budget, put your phone on the table and ask:

**"Why do we pay Verizon instead of building cell towers?"**

Let them explain it to you.

Then say:

**"Azure is the same thing."**

---

*For more on why Finance's ROI calculations miss the point, read [Why Your Azure Migration ROI Calculation Is Wrong](/blog/azure-migration-roi-wrong/) - Finance compares server costs while missing the procurement revolution.*

*Or see [Azure Costs: Apps Not Subscriptions](/blog/azure-costs-apps-not-subscriptions/) - count your applications first, then design subscriptions around teams.*
