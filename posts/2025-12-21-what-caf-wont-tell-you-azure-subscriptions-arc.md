---
title: "What the CAF Won't Tell You About Azure Subscriptions (And Why Azure Arc Makes It Worse)"
date: 2025-12-21
summary: "Microsoft's Cloud Adoption Framework teaches subscriptions as a scale unit. In regulated enterprises, subscriptions are security boundaries. That's not an advanced topic—it's the foundation. Azure Arc amplifies this problem by extending broken subscription models to on-prem infrastructure."
tags: ["azure", "governance", "azure-arc", "caf", "subscriptions", "architecture"]
cover: "/static/images/hero/azure-subscriptions-caf-reality.png"
hub: governance
related_posts:
  - azure-arc-enterprise-scale-problems
  - azure-subscriptions-security-billing-boundary
  - azure-governance-napkin-test
---

**Short Answer:** The Cloud Adoption Framework positions Azure subscriptions as "scale units" for organizing resources. In regulated enterprises (banking, healthcare, government), subscriptions function as security boundaries enforced by compliance requirements—not organizational preferences. Microsoft's guidance optimizes for resource sharing and central management. Enterprise reality demands isolation, accurate billing, and audit trails. Azure Arc extends this architectural tension to on-prem infrastructure, forcing you to reconcile Azure's subscription model with VMware inventories, Active Directory domains, and air-gapped networks.

This guide is part of our [Azure Governance hub](/hub/governance/) covering enterprise governance strategies, compliance automation, and architectural reality at scale.

I manage 44 Azure subscriptions and 850+ Azure Arc-enabled VMware VMs. When architects ask "How should we structure our subscriptions?" I tell them the answer Microsoft won't: **Your compliance requirements already decided for you.**

Here's what the CAF doesn't say about subscriptions, why it matters, and how Azure Arc makes the problem impossible to ignore.

---

## What the CAF Says About Subscriptions

**Microsoft's Cloud Adoption Framework teaches subscriptions as:**

### "Scale Units for Resource Organization"

From the CAF:
> "Subscriptions serve as a scale unit for component workloads, which allows for platform development across several stages of maturity."

**Translation:** Think of subscriptions like folders. Put related resources in the same subscription to make management easier.

### "Use Management Groups for Governance"

CAF guidance:
> "Management groups provide a governance scope above subscriptions. You organize subscriptions into management groups; the governance conditions you apply cascade by inheritance to all associated subscriptions."

**Translation:** Don't create multiple subscriptions for governance. Use one big subscription and apply policies from above.

### "Use Tags for Cost Allocation"

CAF pattern:
> "Apply cost center tags to resources for chargeback and showback reporting."

**Translation:** Billing can span subscriptions. Just tag everything properly and cost reports will work.

---

## What the CAF Doesn't Say (Enterprise Reality)

### In Regulated Industries, Subscriptions ARE Security Boundaries

**Why this matters:**

In banking, healthcare, and government environments, security controls aren't organizational preferences—they're compliance requirements enforced by auditors, regulators, and security teams.

**Actual enterprise pattern:**

```
Subscription 1: Production workloads (PCI-DSS scope)
├── Network: Isolated VNet, no internet egress
├── RBAC: Production team only (no developers)
├── Audit: All activity logs shipped to SIEM
└── Compliance: SOC 2, PCI-DSS, HIPAA

Subscription 2: Development workloads (non-production)
├── Network: Internet-connected (developers need GitHub)
├── RBAC: Developers have Contributor access
├── Audit: Activity logs retained 90 days
└── Compliance: None (testing environment)
```

**These cannot be the same subscription.**

Not because of "organization," but because:
- Different security controls (SIEM vs. basic logging)
- Different network policies (isolated vs. internet-connected)
- Different RBAC requirements (restricted vs. open)
- Different compliance scope (audited vs. non-audited)

**The CAF's recommendation?**
> "Use Azure Policy to enforce different controls within the same subscription."

**The regulatory reality?**
> "Auditors want physical separation. Policy can be changed. Subscriptions can't be merged after the fact."

---

## The Billing Boundary Problem

### Tags Drift. Subscriptions Don't.

**Microsoft's cost allocation guidance:**

1. Apply `CostCenter` tag to all resources
2. Run Cost Management reports grouped by tag
3. Chargeback departments based on tag values

**What actually happens:**

**Month 1:** 95% of resources tagged correctly
**Month 6:** 73% of resources tagged correctly
- Automation created resources without tags
- Developers forgot to tag manually-created VMs
- Someone deleted tags during troubleshooting
- ARM templates deployed without tag inheritance

**Month 12:** Finance asks for chargeback report
- "Engineering owes us $147K"
- Engineering: "We can't verify. 27% of resources aren't tagged."
- Finance: "Fix your tagging and we'll run the report again next quarter."

**Subscription-based chargeback:**

```
Subscription: Engineering-Production
Cost this month: $147,000
Owner: Engineering department
Chargeback: 100% accurate, no reconciliation needed
```

**No tags required. No drift. No argument.**

### The $500 Waste Problem

**In a shared subscription:**

Total monthly cost: $50,000
Waste (orphaned disks, stopped VMs): $500
Waste as % of bill: 1% (invisible)

**In an isolated subscription:**

Total monthly cost: $1,000
Waste: $500
Waste as % of bill: 50% (impossible to ignore)

**Which model incentivizes optimization?**

Microsoft's revenue model depends on shared subscriptions where waste is a rounding error.

**Enterprise cost control depends on isolated subscriptions where waste is obvious.**

---

## How Azure Arc Amplifies the Subscription Problem

### Arc Extends Azure's Model to On-Prem (Whether You Want It To)

**Azure Arc's value proposition:**
> "Manage on-prem servers with Azure governance—policies, updates, monitoring—all from the Azure portal."

**The architectural reality:**

When you Arc-enable a VMware VM, you're mapping it to:
- **Azure subscription** (billing container)
- **Azure resource group** (organizational container)
- **Azure region** (data residency)
- **Azure tags** (metadata)

**But the VM still lives in:**
- **VMware vCenter** (actual compute platform)
- **Active Directory domain** (authentication)
- **On-prem network** (VLAN/subnet)
- **Physical datacenter** (regulatory jurisdiction)

**You've created two sources of truth.**

### Problem 1: Subscription Choice Affects Governance Data

**Scenario:** You have 850 VMware VMs in 3 datacenters.

**Option A: One Shared Subscription**
```
Subscription: OnPrem-Infrastructure
├── Resource Group: DC1-VMs (300 VMs)
├── Resource Group: DC2-VMs (400 VMs)
└── Resource Group: DC3-VMs (150 VMs)
```

**Result:**
- All 850 VMs appear in Azure Resource Graph as one pool
- Cost reporting aggregates across all datacenters
- RBAC applies to all VMs (production + dev + test)
- Compliance reports show "OnPrem-Infrastructure" as single control domain

**Option B: Isolated Subscriptions**
```
Subscription: Production-OnPrem (PCI-DSS scope)
└── 120 VMs (payment processing servers)

Subscription: Development-OnPrem (non-production)
└── 200 VMs (test environments)

Subscription: Legacy-OnPrem (migration candidates)
└── 530 VMs (aging infrastructure)
```

**Result:**
- Azure Resource Graph queries require cross-subscription logic
- Cost reporting matches budget structure (Prod vs. Dev vs. Legacy)
- RBAC scoped correctly (DevOps can't touch Prod accidentally)
- Compliance reports align with audit scope

**Which model matches your actual governance needs?**

The CAF doesn't answer this. It assumes you'll figure it out after Arc deployment.

### Problem 2: Ghost Registrations Create Fake Compliance

**What happens when you delete a VM:**

**In VMware:**
- VM deleted from vCenter
- Compute/storage released
- Inventory updated immediately

**In Azure Arc:**
- Arc agent stops reporting
- Azure resource remains registered
- Compliance reports show "managed" (but it's a ghost)

**Real example from our environment:**

**Before cleanup:**
- Azure Resource Graph: 850 Arc-enabled servers
- VMware RVTools export: 543 actual VMs
- Ghost registrations: 307 (36% of "managed" inventory is fake)

**Impact on governance:**
- Azure Policy compliance: 94% (looks great!)
- Actual compliance: Unknown (307 VMs don't exist)
- Audit report: Useless (1/3 of data is fiction)

**Root cause:** Arc registration happens in a subscription. VM lifecycle happens in VMware. No built-in reconciliation.

### Problem 3: Subscription Sprawl vs. Inventory Accuracy

**Microsoft's Arc guidance:**
> "Arc-enable servers to extend Azure management to on-prem."

**Missing from guidance:**
> "Choose your subscription structure BEFORE enabling Arc, because moving 850 Arc resources between subscriptions later requires re-registration."

**Real migration scenario:**

You Arc-enabled 850 VMs into a shared subscription. Six months later, security team says:
> "Production servers must be in isolated subscriptions for SOC 2 compliance."

**Your options:**

**Option 1: Re-register all Arc servers**
- Remove Arc agent from 120 production VMs
- Re-enable Arc into new subscription
- Lose 6 months of compliance history
- Duration: 2-4 weeks
- Risk: High (manual process, potential downtime)

**Option 2: Accept non-compliance**
- Keep production VMs in shared subscription
- Document exception for auditors
- Hope they accept it
- Risk: Audit failure

**Option 3: Build custom reconciliation**
- Tag Arc resources with "actual subscription should be X"
- Maintain mapping in external system
- Reconcile during audit
- Risk: Drift between tags and reality

**If you designed subscription structure correctly from day 1:** None of this happens.

---

## The AWS Comparison (Why Azure Is 5 Years Behind)

### AWS Makes Multi-Account the Default

**AWS Control Tower (2019):**
> "Provision multiple AWS accounts automatically using account vending machine patterns."

**AWS best practice:**
- One account per application
- One account per environment (dev/test/prod)
- Centralized billing via AWS Organizations
- No tags required for cost allocation

**Azure Subscription Vending (2023):**
> "Automate subscription creation using templates."

**Still positioned as:** Advanced topic for large enterprises

**Still recommends:** Management groups and tags as primary organization

**Why the difference?**

AWS learned early that shared accounts create:
- Security boundary confusion
- Cost allocation nightmares
- RBAC complexity

Azure is teaching the same lesson. But the documentation hasn't caught up to reality.

---

## When Subscriptions Actually Matter

### Use Cases Where Subscription Isolation Is Non-Negotiable

**1. Regulatory Compliance (PCI-DSS, HIPAA, SOC 2)**

**Requirement:** Physical separation of production and non-production systems

**Azure Policy approach:**
```hcl
# Deny public IP addresses in production resource groups
# Allow public IP addresses in dev resource groups
```

**Auditor response:**
> "Policy can be disabled. Show me physical separation."

**Subscription approach:**
```
Production Subscription: No internet egress, isolated VNet
Development Subscription: Internet-connected
```

**Auditor response:**
> "Approved."

**2. Chargeback/Showback with Finance**

**Tag-based chargeback conversation:**

Finance: "Engineering owes $147K."
Engineering: "27% of resources aren't tagged. We can't validate."
Finance: "Fix your tags and we'll re-run the report."
Engineering: "That'll take 3 weeks."
Finance: "Invoice is due next week."

**Subscription-based chargeback:**

Finance: "Engineering subscription cost: $147K."
Engineering: "Verified. Here's payment."

**No reconciliation. No tag audits. No argument.**

**3. Multi-Tenant SaaS**

**Scenario:** You run a SaaS platform with 47 enterprise customers.

**Shared subscription model:**
```
Subscription: SaaS-Production
├── RG: Customer-A-Resources
├── RG: Customer-B-Resources
└── RG: Customer-C-Resources (... 44 more)
```

**Problem:** One customer's security breach affects everyone in the subscription.

**Isolated subscription model:**
```
Subscription: Customer-A-Production
Subscription: Customer-B-Production
Subscription: Customer-C-Production
```

**Result:** Breach containment. No blast radius across customers.

**4. Mergers & Acquisitions**

**Scenario:** Your company acquires another company. Their Azure infrastructure must remain separate for 18 months (regulatory requirement).

**Shared subscription:** Impossible to separate later
**Isolated subscription:** Already separated by design

---

## When Shared Subscriptions Work

**Not every organization needs subscription isolation.**

### Legitimate Use Cases for Shared Subscriptions

**1. Startups (< 50 resources)**
- Single team
- No chargeback requirements
- Learning phase

**2. Single-Product Companies**
- One application
- One team
- Simple RBAC

**3. Non-Production Environments**
- Sandboxes
- Learning labs
- Experimentation

**4. Proof-of-Concept Projects**
- Short-lived
- No compliance requirements
- Tear down after 90 days

**The decision criteria:**

If your answer to ANY of these is "yes," you need isolated subscriptions:
- Do you have chargeback/showback requirements?
- Do you have regulatory compliance (PCI, HIPAA, SOC 2)?
- Do you have multiple teams with different security needs?
- Do you have production + non-production workloads?
- Do you have customers that must be isolated?

---

## The Real First Step in Azure Architecture

### Not: "What Resource Groups Do We Need?"

### Instead: "What Are Our Boundaries?"

**Question 1: What are our billing boundaries?**
- Who gets charged?
- How accurate must chargeback be?
- Can we tolerate 15-25% tagging drift?

**Question 2: What are our security boundaries?**
- What must be physically separated?
- What compliance scopes exist?
- What are our blast radius limits?

**Question 3: Are billing and security boundaries the same?**

**If YES:**
- Use isolated subscriptions
- Each subscription = one cost center + one security domain
- No tags required for governance
- Example: Production subscription for Payment Processing app

**If NO:**
- You're going to build complexity to align them
- Shared subscriptions + extensive tagging
- Custom RBAC across resource groups
- Azure Policy to enforce separation
- External reconciliation tools

**Most enterprises discover:** Isolated subscriptions are simpler than forcing alignment.

---

## Azure Arc Adds Another Boundary Question

### "What Are Our Inventory Boundaries?"

**Azure assumes:** Your entire infrastructure is in Azure subscriptions

**Azure Arc reality:** Infrastructure spans:
- Azure subscriptions (cloud resources)
- VMware vCenter (on-prem VMs)
- Active Directory (authentication)
- Physical datacenters (regulatory jurisdiction)

**New question:** Do your Azure Arc subscriptions match your operational boundaries?

**Scenario 1: Geographic Separation**

You have datacenters in:
- US (PCI-DSS compliance required)
- EU (GDPR data residency required)
- APAC (air-gapped, no internet)

**Shared subscription:**
```
Subscription: Global-OnPrem-Infrastructure
├── US-DC1-VMs
├── EU-DC2-VMs
└── APAC-DC3-VMs
```

**Problem:** GDPR auditor asks "Where is EU data processed?"
**Answer:** "In a subscription that also contains US and APAC resources."
**Auditor:** "That's not data residency isolation."

**Isolated subscriptions:**
```
Subscription: US-OnPrem (PCI-DSS scope)
Subscription: EU-OnPrem (GDPR scope)
Subscription: APAC-OnPrem (air-gapped)
```

**Scenario 2: Lifecycle Separation**

Your on-prem VMs have different lifecycles:
- Production VMs (keep forever, PCI-DSS compliance)
- Migration candidates (moving to Azure in 12 months)
- Legacy VMs (decommission when replacement ready)

**Shared subscription:** All VMs look the same in Azure Resource Graph

**Isolated subscriptions:**
```
Subscription: Production-OnPrem (PCI-DSS, governed)
Subscription: Migration-Staging (temporary, unmanaged)
Subscription: Legacy-Deprecation (compliance exempt)
```

**Azure Policy, compliance reports, and governance now align with operational reality.**

---

## Why Microsoft Doesn't Say This

### Reason 1: Customer Diversity

Microsoft writes documentation for:
- 5-person startups (1 subscription is perfect)
- 500-person companies (10 subscriptions)
- 50,000-person enterprises (500+ subscriptions)

**The CAF can't recommend "one subscription per app" because:**
- Startups can't afford subscription sprawl
- Mid-size companies don't have headcount to manage it
- Enterprises are already doing it

**So Microsoft says:** "Subscriptions are scale units. Use management groups for governance."

This works for 60% of customers. It fails for the 40% in regulated industries.

### Reason 2: Complexity Sells

**Shared subscriptions require:**
- Hub-and-spoke networking
- Shared Azure Firewall
- Complex RBAC (resource-level permissions)
- Tag governance automation
- Cost allocation tools (third-party or custom)

**Isolated subscriptions require:**
- Simple networking (one VNet per subscription)
- Optional firewall (or none)
- Simple RBAC (subscription-level permissions)
- No tags needed (subscription = cost center)

**Which model generates more Azure consulting revenue?**

**Which model requires more Azure services?**

**Which model creates more support tickets?**

The complex one.

### Reason 3: Revenue Opacity

**Shared subscription ($50K/month):**
- Waste: $500 (orphaned disks, stopped VMs)
- Waste as % of bill: 1%
- Customer reaction: Doesn't notice

**Isolated subscription ($1K/month):**
- Waste: $500
- Waste as % of bill: 50%
- Customer reaction: Shuts down unused resources immediately

**Which model maximizes Azure revenue?**

Microsoft's incentive: Shared subscriptions hide waste.
Customer's incentive: Isolated subscriptions expose waste.

---

## What Enterprise Architects Actually Do

### They Ignore the CAF and Design for Reality

**Pattern I see repeatedly:**

**Phase 1: Follow the CAF (6 months)**
- Shared subscriptions
- Management groups for governance
- Extensive tagging strategy
- Azure Policy for compliance

**Phase 2: Hit Reality (Month 7-12)**
- Tags drift to 70% accuracy
- Finance rejects chargeback reports
- Auditor flags lack of security separation
- Team realizes RBAC is unmanageable

**Phase 3: Redesign with Isolated Subscriptions (Month 13-18)**
- Create subscription per application
- Migrate resources (painful)
- Simplify RBAC
- Stop fighting tag drift

**Phase 4: Wish They Started with Phase 3**

---

## The Azure Arc Lesson

### Arc Exposes What Was Always True

Before Arc, you could pretend subscriptions were "organizational preferences."

After Arc, you can't ignore:
- **Inventory reconciliation:** Azure says 850 VMs. VMware says 543. Which is real?
- **Lifecycle mismatches:** VM deleted in VMware. Arc resource still exists in Azure.
- **Governance fiction:** Compliance reports based on ghost registrations.

**Arc forces the question:** Do your Azure subscriptions reflect operational reality?

If no: Your Arc deployment will create more problems than it solves.

---

## The Cornerstone Truth

**Microsoft's CAF teaches:**
> "Subscriptions are scale units. Use management groups and tags for governance."

**Enterprise reality:**
> "In regulated industries, subscriptions are security boundaries. Design for that first. Everything else is commentary."

**Azure Arc reality:**
> "If your subscription structure doesn't match your operational boundaries, Arc will expose it immediately."

---

## What to Do About It

### Step 1: Audit Your Current State

**Questions to answer:**

1. How many subscriptions do you have?
2. What determines subscription boundaries today?
3. Do subscriptions match security requirements?
4. Do subscriptions match cost allocation needs?
5. If you have Arc: Do subscriptions match inventory boundaries?

### Step 2: Define Your Boundaries

**Billing boundaries:**
- Who gets charged?
- How accurate must chargeback be?
- Can finance tolerate tag drift?

**Security boundaries:**
- What must be physically separated?
- What compliance scopes exist?
- What are blast radius limits?

**Inventory boundaries (if using Arc):**
- Geographic separation (US/EU/APAC)?
- Lifecycle separation (prod/migration/legacy)?
- Vendor separation (Azure/VMware/AWS)?

### Step 3: Align Subscriptions with Reality

**If boundaries align:**
- Use isolated subscriptions
- One subscription = one cost center + one security domain
- Simplify RBAC, networking, governance

**If boundaries conflict:**
- Accept complexity
- Build tag governance
- Custom cost allocation
- External reconciliation

**Most enterprises discover:** Isolated subscriptions are simpler.

### Step 4: Before Enabling Arc

**Critical decision:** Choose subscription structure BEFORE Arc deployment.

Moving 850 Arc resources between subscriptions = 2-4 weeks of re-registration.

**Questions:**
1. Do production and non-production VMs need separate subscriptions?
2. Do different datacenters need separate subscriptions?
3. Do migration candidates and long-term infrastructure need separate subscriptions?

**Answer these first. Enable Arc second.**

---

## Common Questions

**Q: Isn't subscription sprawl unmanageable?**

**A:** Management groups exist for a reason. Organize subscriptions into hierarchies. Apply governance from above. But don't confuse "governance scope" with "isolation boundary."

**Q: What about shared services (ExpressRoute, Firewall)?**

**A:** Hub-and-spoke topology works. Central subscription for shared infrastructure. Spoke subscriptions for isolated workloads. Doesn't require putting production and dev in the same subscription.

**Q: Doesn't this increase cost?**

**A:** Isolated subscriptions expose waste, which reduces cost. Shared subscriptions hide waste, which increases cost. Net effect: Isolated subscriptions usually cost less.

**Q: Can we migrate from shared to isolated later?**

**A:** Yes. It's painful. Resource moves, RBAC rebuilds, networking changes. Better to design correctly from day 1.

**Q: What if the CAF says something different?**

**A:** The CAF is guidance, not gospel. It's written for broad audiences. Your compliance requirements are mandatory. When they conflict, compliance wins.

---

## The Bottom Line

**The Cloud Adoption Framework is corporate marketing.**

It's designed to sell Azure to every customer from startups to banks.

**Your compliance requirements are engineering reality.**

They're mandatory, audited, and don't care about Microsoft's messaging.

**Azure Arc is the truth-teller.**

It extends Azure's subscription model to on-prem infrastructure and immediately exposes misalignment.

**The lesson:**

Design your subscription structure for compliance first, operational boundaries second, and organizational preferences last.

Tags are metadata. Resource groups are deployment containers. Subscriptions are the foundation.

Don't build a cathedral on sand.

---

**Related Content:**

- [Azure Arc at Enterprise Scale](/hub/arc/) — Managing Arc deployment across VMware, compliance, and hybrid environments
- [Azure Subscriptions: Security Boundary or Billing Boundary?](/blog/azure-subscriptions-security-billing-boundary/) — Deep dive on subscription decision criteria
- [Azure Governance Napkin Test](/blog/azure-governance-napkin-test/) — Can you explain your governance model in 30 seconds?
