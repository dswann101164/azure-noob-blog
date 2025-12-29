---
title: Azure Chargeback Tags 2025: The 6 Tags That Actually Work
date: 2025-10-16
summary: A chargeback/showback model built on tags that finance, app owners, and cloud
  teams can all live with—without 47 competing cost spreadsheets.
tags:
- Azure
- Chargeback
- FinOps
- Governance
- Showback
- Tags
cover: /static/images/hero/azure-chargeback-model.png
slug: azure-chargeback-tags-model


related_posts:
  - azure-costs-apps-not-subscriptions
  - azure-resource-tags-guide
  - tag-governance-247-variations
  - azure-finops-complete-guide

---

This guide is part of our [Azure FinOps hub](/hub/finops/) covering cost management, chargeback models, and financial operations at enterprise scale.
## The story (from the trenches)

When Finance first asked for a chargeback report by Line of Business, I thought our tags would make it easy.
Every resource had `Owner`, `Application`, and `CostCenter` — what could go wrong?
Everything, it turns out.

Our tags told us *who ran the resource*, not *who paid for it.*
So I rebuilt the model from the ground up using six simple tags that finally made Azure Policy, FinOps, and security data line up.

```yaml
Owner: Data
Application: Platform Services
CostCenter: 200-1234
Type: Server
DomainJoined: Yes
ChargebackType: Shared
```

It looked clean, but it told the wrong story — who operates it, not who funds it.

---

## The minimal tag set that actually works

| Tag | Example | Why it matters |
|---|---|---|
| **Owner** | `Data` | Operational custodian. Who runs/fixes the thing. |
| **Application** | `Platform Services` | Workload identity for slicing costs and incidents. |
| **CostCenter** | `200-1234` | The **Line of Business** that funds/consumes it. Drives showback/chargeback. |
| **Type** | `Server` / `Desktop` / `Appliance` | Inventory posture & lifecycle (patching, backup, decomm). |
| **DomainJoined** | `Yes` / `No` | Security & compliance signal (identity plane, GPO reach, break-glass lists). |
| **ChargebackType** | `Shared` / `Direct` | Flags resources that need split or direct billing. |

> **Key idea:** `Owner` is **not** the payer. `CostCenter` is the money tag. `Application` is the bridge between Ops (Owner) and Finance (CostCenter). `Type` and `DomainJoined` make your inventory and patching views accurate.

---

## Shared services: how we made chargeback fair

Shared platforms (databases, monitoring, identity, logging) don’t map to a single payer. We used **ChargebackType=Shared** to mark them and **cost allocation rules** to split costs fairly among consuming CostCenters.

**Example split (concept):**

| Source (tag) | Target CostCenter | Allocation % |
|---|---|---|
| `ChargebackType=Shared` for Application=Platform Services | `200-1234` | 40% |
| " | `300-5678` | 30% |
| " | `400-6789` | 30% |

> Start with **showback** (no internal billing) for a few cycles to build trust. Move to **chargeback** once your tag coverage is stable.

---

## Queries you’ll use every week

### 1) Find resources missing critical tags
```kql
Resources
| extend Owner=tostring(tags.Owner), App=tostring(tags.Application), CC=tostring(tags.CostCenter), Type=tostring(tags.Type), DJ=tostring(tags['DomainJoined'])
| where isempty(Owner) or isempty(App) or isempty(CC) or isempty(Type) or isempty(DJ)
| project subscriptionId, resourceGroup, name, type, Owner, App, CC, Type, DJ
| order by subscriptionId, resourceGroup, name
```

### 2) Showback view by Line of Business (CostCenter) and Application
```kql
CostByResource
| summarize CostUSD=sum(AmortizedCost) by CostCenter, Application, bin(UsageDate, 1d)
| order by UsageDate asc
```

### 3) Patch & compliance slice by Type and DomainJoined
```kql
Resources
| where type =~ 'microsoft.compute/virtualmachines'
| extend Type=tostring(tags.Type), DJ=tostring(tags['DomainJoined'])
| summarize CountVMs=count() by Type, DJ
```

### 4) Owner ≠ Payer sanity check
```kql
Resources
| extend Owner=tostring(tags.Owner), App=tostring(tags.Application), CC=tostring(tags.CostCenter)
| summarize Resources=count() by Owner, CC
| order by Owner, CC
```

---

## Azure Policy: deny on missing tags (with friendly remediation)

Require the six tags on create. Deny if missing; pair with an initiative that adds a **Modify** policy for auto-append in well-known RGs.

```json
{
  "properties": {
    "displayName": "Require core tags on resources",
    "policyRule": {
      "if": {
        "anyOf": [
          { "field": "tags['Owner']", "exists": false },
          { "field": "tags['Application']", "exists": false },
          { "field": "tags['CostCenter']", "exists": false },
          { "field": "tags['Type']", "exists": false },
          { "field": "tags['DomainJoined']", "exists": false },
          { "field": "tags['ChargebackType']", "exists": false }
        ]
      },
      "then": { "effect": "deny" }
    }
  }
}
```

> Tip: keep tag names **exact** (`DomainJoined`, not `Is Domain Joined`). If you’re already live with variants, standardize and migrate with a one-time script.

---

## PowerShell: weekly tag health & nudge

```powershell
Connect-AzAccount

$query = @"
Resources
| extend Owner=tostring(tags.Owner), App=tostring(tags.Application), CC=tostring(tags.CostCenter), Type=tostring(tags.Type), DJ=tostring(tags['DomainJoined']), CB=tostring(tags.ChargebackType)
| where isempty(Owner) or isempty(App) or isempty(CC) or isempty(Type) or isempty(DJ) or isempty(CB)
| project subscriptionId, resourceGroup, name, type, Owner, App, CC, Type, DJ, CB
"@

$subs = (Get-AzSubscription).Id
$arg  = @{ Query = $query; Subscriptions = $subs }
$result = Search-AzGraph @arg
$result | Export-Csv -NoTypeInformation -Path "Tag-Remediation-MissingCoreTags.csv"
```

---

## Operating model that stuck

1. **Designate tag owners**: each Application has a named owner responsible for fixing missing tags.
2. **Showback first**: publish CostCenter/Application dashboards monthly; fix gaps.
3. **Promote to chargeback**: once untagged cost <2%, switch Finance to these numbers.
4. **Hold the line**: deny on create, auto-append only in controlled landing zones.

---

## TL;DR
- `Owner` tells us who runs it. `CostCenter` tells us who pays. `Application` ties the story together.
- Add `Type`, `DomainJoined`, and `ChargebackType` to unlock patching, inventory, and FinOps accuracy.
- Mark shared services and split fairly. Start with showback, then charge back.

This six-tag model is the smallest practical set that made our governance, security, and FinOps reporting finally agree with each other — and with Finance.

---

### 🔍 Audit Your "Big 6" Compliance

Are you actually tagging? Or just talking about it?

```kusto
// Audit the "Big 6" Tags
Resources
| extend hasOwner = iif(tags has "Owner", 1, 0)
| extend hasApp = iif(tags has "Application", 1, 0)
| extend hasCC = iif(tags has "CostCenter", 1, 0)
| summarize ComplianceScore = (sum(hasOwner) + sum(hasApp) + sum(hasCC)) * 100.0 / (count() * 3)
```

---

### 🛑 Chargeback Governance

Tags are only useful if they trigger a bill.
**[Download the Azure RACI Matrix](https://gumroad.com/l/raci-template?ref=cost-batch-chargeback)** to link Tag Compliance to Financial Accountability.

<div class="downloads" style="text-align: center; margin-top: 2rem;">
  <a class="btn" href="https://gumroad.com/l/raci-template?ref=cost-batch-chargeback" style="font-size: 1.2em; padding: 15px 30px; background-color: #0078d4; color: white;">Get the Chargeback RACI</a>
</div>
