---
title: "Software Rationalization: The Step Zero That Works in a DevOps World"
date: 2025-11-04
summary: "Before you migrate, modernize, or even look at the cloud â€” you must know what you own, what it costs, and whether it should exist. This is not a migration step. It's a business survival step."
tags: ["Rationalization", "FinOps", "devops", "azure", "governance", "Architecture", "Security", "Cost Allocation"]
cover: "/static/images/hero/rationalization-devops.png"
hub: governance
related_posts:
  - terraform-azure-devops-cicd-series-index
  - if-you-cant-code-your-architecture
  - cloud-migration-reality-check
---
## The One Question No One Can Answer


This guide is part of our [Azure Governance hub](/hub/governance/) covering policy enforcement, compliance frameworks, and enterprise controls.

> **"How many applications do we have â€” and how much do they *actually* cost us?"**

Ask any enterprise.  
You'll get the same four answers:

1. "Depends on who you ask."  
2. "We think around 400."  
3. "Maybe 700, counting Excel."  
4. "We don't know â€” and the bill is split across 47 subscriptions."

That last one?  
**That's the killer.**

---

## This Is Not an Azure Problem

**This is a *portfolio hygiene* problem.**

Azure just makes it **visible** â€” with **itemized, unmergeable, soul-crushing invoices**.

You don't rationalize *for* Azure.  
You rationalize to decide **if Azure (or any platform) deserves your app**.

---

## Step Zero: Rationalization â€” *Before Strategy, Before Budget, Before Cloud*

**Software rationalization** is the disciplined process of deciding what to:

| Decision | Meaning |
|--------|--------|
| **Retire** | It's dead. Kill it. |
| **Replace** | Buy > build. SaaS wins. |
| **Retain** | Keep on-prem. Cheaper. Safer. |
| **Replatform** | Minor lift to PaaS. |
| **Refactor** | Full rewrite. Future-proof. |
| **Rehost** | Lift-and-shift. *Only if you must.* |
| **Relocate** | Move hosting. Hybrid/DR. |

> **These are *outcomes*, not options.**  
> You earn them **after discovery**, not before.

---

## The DevOps Reality: Subscriptions Are *Security Zones*, Not App Silos

Microsoft says:  
> "One subscription per workload."

**That's a lie in a DevOps world.**

### Truth Table: One App, Many Subscriptions

| App | Environment | Subscription | Security Zone | Policy |
|-----|-------------|--------------|---------------|--------|
| ERP | Dev | `sub-dev-finance` | Low | Open egress |
| ERP | Test | `sub-test-finance` | Medium | Audit only |
| ERP | Prod | `sub-prod-pci` | High | No public IP, WAF, NSG |

**Same app. Same code. Same owner. Three subscriptions.**

### The Bill Breaks Here:
- **Cost Management** can't auto-roll-up by app
- **Showback** fails: "Prod = $50k, Dev = $2k" â†’ no context
- **Rationalization** fails: You can't retire "ERP" when its cost is shredded

---

## Step 0.5: Design a *Billing Architecture* That Survives DevOps

> **Your technical architecture must map 1:1 to your financial accountability model.**

### Required: The `AppID` â€” Your Atomic Unit of Truth

```yaml
# Mandatory tags on EVERY resource
AppID: ERP-001
Environment: Prod
CostCenter: FIN-1001
Owner: erp-team@contoso.com
SecurityZone: PCI
WorkloadTier: Mission-Critical
SunsetDate: 2027-12-31  # if applicable
```

### Enforce with Azure Policy

```json
{
  "if": {
    "field": "tags['AppID']",
    "exists": false
  },
  "then": {
    "effect": "deny"
  }
}
```

---

## The 7 R's â€” Reframed for DevOps + Multi-Subscription Reality

| R | Decision | DevOps Impact | Billing Impact | Execution |
|---|--------|---------------|----------------|-----------|
| **Retire** | Decommission | Delete from **all** envs | 100% savings | Runbook: `az resource delete` |
| **Replace** | SaaS | Kill custom code | Per-seat cost | Decommission + license |
| **Retain** | Keep on-prem | No cloud tax | Audit annually | Tag: `CloudEligible: No` |
| **Replatform** | PaaS | One pipeline â†’ N subs | Predictable | Bicep/ARM per env |
| **Refactor** | Containers/AKS | GitOps | Lower TCO | Feature flags |
| **Rehost** | IaaS VM | IaC deploy | +40% vs PaaS | **Require sunset plan** |
| **Relocate** | Hybrid/DR | ASR | Temp only | Tag: `Temporary: true` |

---

## Architecture Sins That Break FinOps (And How to Fix Them)

| Sin | Symptom | Fix |
|-----|---------|-----|
| **Monolithic RG** | 200 resources in one RG | Split: `RG-{CostCenter}-{AppID}-{Env}` |
| **Shared Storage** | 50 apps â†’ 1 account | One per `AppID` or `CostCenter` |
| **Global Log Workspace** | All logs â†’ one bill | One per `SecurityZone` + retention caps |
| **Mixed App Service Plan** | Dev + Prod in one plan | One plan per `WorkloadTier` |

---

## The Rationalization Playbook: From Chaos to Decisions

### Phase 0: Discover (Week 1)

```kql
// Azure Resource Graph: Find untagged orphans
Resources
| where isnull(tags['AppID'])
| summarize count() by subscriptionId, resourceGroup
| order by count_ desc
```

### Phase 1: Tag & Enforce (Week 2)
- Auto-tag via **Azure Automation**
- Block untagged deploys with **Azure Policy**

### Phase 2: Aggregate by `AppID` (Week 3)

```kql
// Cost Management: Roll up by AppID
where Tags.AppID != ""
| summarize TotalCost = sum(PreTaxCost) by Tags.AppID, Tags.Environment
| order by TotalCost desc
```

### Phase 3: Decide (Monthly)

| AppID | Total Cost | Owner | 7 R's | Justification |
|-------|------------|-------|-------|---------------|
| ERP-001 | $78,432 | Finance | **Retire** | SaaS alternative 60% cheaper |
| CRM-014 | $45,201 | Sales | **Replatform** | Move to App Service |
| Legacy-042 | $12,500 | IT | **Retain** | Compliance requirement |

### Phase 4: Execute (Automated)

```powershell
# Retire an application across all subscriptions
$appId = "ERP-001"

# Find all resources
$resources = az resource list --tag AppID=$appId --query [].id -o tsv

# Delete (with confirmation)
az resource delete --ids $resources
```

---

## FinOps KPIs That Actually Matter

| KPI | Formula | Target |
|-----|--------|--------|
| **Waste %** | `(Untagged + Retired-but-Running) / Total Spend` | < 5% |
| **Showback Accuracy** | `% of cost allocated to a business unit` | > 95% |
| **AppID Coverage** | `% of resources with AppID tag` | 100% |
| **Sunset Compliance** | `% of Rehost with SunsetDate < 12 mo` | 100% |

---

## Real Numbers: What Success Looks Like

### Typical Enterprise Before Rationalization:
- **800+** "applications" (nobody agrees on the count)
- **$2.5M** annual cloud spend
- **25%** untagged resources
- **0%** showback accuracy
- **6 weeks** to answer "what does App X cost?"

### After 18-Month Rationalization:
- **400** rationalized applications (400 retired/replaced)
- **$1.7M** annual cloud spend (**32% reduction**)
- **98%** AppID coverage
- **95%** showback accuracy
- **Real-time** cost visibility

**Results:**
- **Retired**: 280 apps (zombie VMs, forgotten POCs)
- **Replaced**: 120 apps (moved to SaaS - 50%+ cheaper)
- **Replatformed**: 95 apps (IaaS â†’ PaaS)
- **Savings**: $800K/year

---

## Well-Architected Framework + FinOps + DevOps = Your Operating Model

| WAF Pillar | Rationalization Check | Tool |
|-----------|-----------------------|------|
| **Cost Optimization** | Justified spend? | Cost Management + AppID roll-up |
| **Operational Excellence** | Clear owners + SLAs? | Azure Monitor + PagerDuty |
| **Reliability** | RTO/RPO requirements met? | Site Recovery |
| **Performance Efficiency** | Right-sized resources? | Azure Advisor |
| **Security** | Compliance validated? | Defender for Cloud |

> **Run this assessment monthly. Automate with Azure DevOps.**

---

## The Manifesto: Print This and Nail It to Your CCoE Door

> **"We don't migrate applications.**  
> **We rationalize *decisions* â€” by `AppID`, across security zones, with full cost visibility.**
>  
> **Subscriptions are for security.**  
> **`AppID` is for truth.**  
> **Everything else is noise."**

---

## Implementation Roadmap

### Month 1: Foundation
- [ ] Define tagging standard (AppID, CostCenter, Owner)
- [ ] Deploy Azure Policy to enforce tags
- [ ] Auto-tag existing resources (best effort)
- [ ] Set up Cost Management exports

### Month 2: Discovery
- [ ] Run Resource Graph queries to find orphans
- [ ] Build Power BI dashboard for AppID costs
- [ ] Interview app owners (validate AppID mapping)
- [ ] Document the "unknown" bucket (< 5% target)

### Month 3: Decisions
- [ ] Score each AppID against 7 R's framework
- [ ] Present findings to leadership
- [ ] Get approval for retirements
- [ ] Plan replatforming roadmap

### Month 4+: Execute
- [ ] Automate retirements (dev â†’ test â†’ prod)
- [ ] Migrate apps to PaaS/SaaS
- [ ] Track savings monthly
- [ ] Celebrate wins (and share numbers)

---

## Resources & Tools

| Tool | Purpose | Link |
|------|--------|------|
| **Azure Resource Graph** | Discovery queries | [Portal](https://portal.azure.com/#view/HubsExtension/ArgQueryBlade) |
| **Cost Management** | AppID cost roll-up | [Docs](https://learn.microsoft.com/en-us/azure/cost-management-billing/) |
| **Azure Policy** | Tag enforcement | [GitHub](https://github.com/Azure/azure-policy) |
| **Power BI** | Cost dashboards | [Templates](https://powerbi.microsoft.com/en-us/templates/) |
| **Well-Architected** | Assessment tool | [Portal](https://learn.microsoft.com/en-us/assessments/) |

---

## âœ… NOW AVAILABLE: The Azure Rationalization Toolkit

**Open-source, production-ready, tested at enterprise scale.**

ðŸ‘‰ **[Get the toolkit on GitHub](https://github.com/dswann101164/azure-rationalization-toolkit)**

**What's included:**
- âœ… Azure Policy definitions (ready to deploy)
- âœ… KQL queries (copy-paste into Resource Graph)
- âœ… PowerShell automation scripts
- âœ… Complete documentation with examples
- âœ… Zero setup required â€” just copy/paste queries

**Tested at scale:**
- 44 subscriptions
- 31,000+ resources
- 13+ months cost history
- Sub-3-second queries

All queries are ready to use in Azure Resource Graph Explorer today.

---

## Final Thoughts

Rationalization isn't a cloud project.  
It's a **truth-finding mission**.

You can't optimize what you don't measure.  
You can't retire what you can't find.  
You can't justify spend you can't attribute.

**AppID is your North Star.**  
Everything else is implementation detail.

Start there.  
The rest will follow.

---

*Next post: Building the AppID enforcement pipeline with Azure Policy + GitHub Actions.*

*All code and dashboards will be available in my [GitHub repo](https://github.com/dswann101164).*
