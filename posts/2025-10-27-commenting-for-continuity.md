---
title: "Commenting for Continuity: Why My Code Comments Don't Look Like Yours (On Purpose)"
date: 2025-10-27
summary: "Most guides say 'comment the why, not the what.' Azure admins need more: comments that double as runbooks, audit trails, and change-board briefs."
tags: ["azure", "devops", "kql", "powershell", "Terraform", "governance"]
cover: "/static/images/hero/code-architecture.svg"
hub: ai
---
## TL;DR


This guide is part of our [AI-Assisted Azure Operations hub](/hub/ai/) exploring how AI tools transform cloud administration and productivity workflows.

Typical "best practices" stop at readability. My commenting style is built for **continuity**—so an Azure admin, auditor, or on-call responder can reconstruct intent, verify outcomes, and roll back safely without tribal knowledge.

---

## The Problem with "Good Comments"

Every coding guide tells you the same thing:

1. **Comment the why, not the what**
2. **Avoid duplicating code**
3. **Keep it short**

All true—**but insufficient for cloud operations.**

In Azure, your comments must serve:
- **Change Advisory Board (CAB)** reviews
- **Audit responses** (SOC 2, PCI, HIPAA)
- **Incident recovery** (at 2 AM when the author is unreachable)
- **Knowledge transfer** (when you're the only one who knows how this works)

If a CAB member asks:
- "What changed?"
- "Why now?"
- "How do we verify success?"
- "How do we roll back?"

...your "why" comments won't cut it.

---

## My Model: Comments as Operational Memory

I use a **universal, lightweight schema** that works in PowerShell, KQL, Terraform, Bash, Python—any language.

```
TITLE | PURPOSE | CONTEXT | ASSUMPTIONS | INPUTS | OUTPUTS
RISKS & LIMITS | VERIFICATION | ROLLBACK | RUNBOOK/LINKS
OWNER | LAST UPDATED | CHANGELOG
```

These fields map **1:1 to what change boards, incident reviews, and future teammates need.**

Not every script needs all fields. But the schema is consistent, so anyone reading your code knows what to look for.

---

## Side-by-Side: Common Advice vs Continuity Model

| Situation | Typical Comment | Continuity Model (Mine) |
|-----------|----------------|------------------------|
| **PowerShell inventory script** | "Gets subscriptions and exports CSV." | **PURPOSE:** Tenant-wide inventory for audit.<br>**ASSUMPTIONS:** Reader on all subs.<br>**RISKS:** Throttling; retries 3x.<br>**VERIFICATION:** Expect N rows ≈ ARG count.<br>**ROLLBACK:** N/A (read-only). |
| **KQL detection query** | "Finds old agents." | **PURPOSE:** Identify VMs on MMA for migration.<br>**LIMITS:** Arc reports differ.<br>**VERIFICATION:** Spot-check in Portal → VM → Extensions.<br>**RUNBOOK:** ADR-015. |
| **Terraform hub VNet** | "Creates hub network." | **CONTEXT:** CAF landing zone; peered spokes.<br>**RISKS:** CIDR change forces replacement.<br>**ROLLBACK:** `terraform apply` previous planfile.<br>**OWNER/LAST UPDATED** included. |

The difference: **The continuity model answers questions before they're asked.**

---

## Concrete Examples

### PowerShell (Advanced Function Header)

```powershell
<#
TITLE: Resource Deletions (Last 90d)
PURPOSE: SOC 2 quarterly audit – who deleted what/when
CONTEXT: Activity Log via Log Analytics (control plane only)
ASSUMPTIONS: ≥90d retention; Reader on target subscriptions
INPUTS: $LookbackDays = 90
OUTPUTS: CSV with TimeGenerated, Caller, ResourceId
RISKS & LIMITS: 
  - Soft deletes not visible (e.g., Key Vault)
  - Guest UPNs appear as UUIDs
VERIFICATION: 
  - Pivot CorrelationId in Portal → Activity log to confirm operation
ROLLBACK: N/A (read-only query)
RUNBOOK/LINKS: RBK-DEL-001, ADR-004
OWNER: David Swann
LAST UPDATED: 2025-10-27
CHANGELOG:
  - 2025-10-27: Initial implementation
#>

function Get-AzureResourceDeletions {
    param(
        [int]$LookbackDays = 90
    )
    
    # Query implementation here...
}
```

**What this gives you:**
- **Auditor asks:** "How far back does this go?" → **ASSUMPTIONS**
- **Manager asks:** "What if something breaks?" → **RISKS & LIMITS**
- **On-call asks:** "How do I verify this worked?" → **VERIFICATION**

### KQL (Inline, Concise)

```kql
// TITLE: Agent Migration Readiness
// PURPOSE: Identify VMs still on MMA (14d grace period ending)
// LIMITS: Arc-enabled VMs may report differently
// VERIFY: Portal → VM → Extensions should show AMA (not MMA)

Heartbeat
| summarize lastSeen = max(TimeGenerated) by Computer, AgentVersion
| where lastSeen < ago(14d)
| where AgentVersion startswith "MMA"
| project Computer, AgentVersion, DaysSinceLastSeen = datetime_diff('day', now(), lastSeen)
| order by DaysSinceLastSeen desc
```

**What this gives you:**
- **Teammate asks:** "What's this query for?" → **PURPOSE**
- **You ask yourself 3 months later:** "Why 14 days?" → **PURPOSE** (grace period)
- **Verification fails:** → **VERIFY** tells you where to spot-check

### Terraform (Module Doc Block)

```hcl
/*
TITLE: Hub VNet Module
PURPOSE: Standard hub with shared services + routing to on-prem
CONTEXT: Aligns with CAF landing zone architecture; peered to spokes
ASSUMPTIONS:
  - azurerm provider >= 4.36
  - Remote state configured (state.tf)
  - Address space doesn't conflict with existing VNets
OUTPUTS: vnet_id, subnet_ids
RISKS & LIMITS:
  - CIDR changes force VNet replacement (destructive)
  - NSG rules managed separately (not in module)
VERIFICATION:
  - `terraform plan` should be stable with no input changes
  - Test connectivity from spoke VM to hub firewall
ROLLBACK:
  - Apply previous planfile: `terraform apply tfplan-[timestamp]`
  - Or checkout previous Git tag: `git checkout v1.2.0`
OWNER: D. Swann
LAST UPDATED: 2025-10-27
*/

resource "azurerm_virtual_network" "hub" {
  name                = var.vnet_name
  location            = var.location
  resource_group_name = var.resource_group_name
  address_space       = var.address_space
  
  # Configuration...
}
```

**What this gives you:**
- **CAB asks:** "What happens if we change the CIDR?" → **RISKS & LIMITS**
- **Incident responder asks:** "How do we roll back?" → **ROLLBACK**
- **New team member asks:** "Is this up to date?" → **LAST UPDATED**

---

## Why This Wins in Azure Operations

### 1. Traceability
**Owner, date, and changelog** reduce "who touched this?" hunts.

Instead of:
```powershell
# Fixed the query - DW
```

You get:
```powershell
# LAST UPDATED: 2025-10-27
# CHANGELOG:
#   - 2025-10-27: Added retry logic for throttling (D. Swann)
#   - 2025-09-15: Initial version (J. Smith)
```

### 2. Audit-Ready
**Purpose/assumptions/verification** map directly to CAB forms.

Your script header becomes your change request documentation:
- **Purpose** → Business justification
- **Risks & Limits** → Impact assessment
- **Verification** → Success criteria
- **Rollback** → Backout plan

### 3. Faster Handoffs
A responder can **verify and roll back without paging the author.**

At 2 AM, when a Terraform apply fails:
- **VERIFICATION** tells them what "success" looks like
- **ROLLBACK** gives them the exact command to undo
- **RUNBOOK/LINKS** points them to the full procedure

### 4. AI-Friendly
**Structured fields are parseable by copilots** to build docs or PR notes.

GitHub Copilot, ChatGPT, and other tools can extract:
- Purpose → README summary
- Inputs/Outputs → Parameter documentation
- Verification → Test cases

---

## VS Code: Make It One Keystroke

Add a **global snippet** (`crumbs`) so every file gets the same header in seconds.

**File:** `%APPDATA%\Code\User\snippets\global.code-snippets`

```json
{
  "Breadcrumb Header": {
    "prefix": "crumbs",
    "body": [
      "TITLE: ${1:Short title}",
      "PURPOSE: ${2:What this does and why}",
      "CONTEXT:",
      "  - ${3:Key constraints/decisions}",
      "ASSUMPTIONS:",
      "  - ${4:Environment, versions, data}",
      "INPUTS:",
      "  - ${5:name=, example=}",
      "OUTPUTS:",
      "  - ${6:files/returns/side effects}",
      "RISKS & LIMITS:",
      "  - ${7:Edge cases/gaps}",
      "VERIFICATION:",
      "  - ${8:Command or check to prove success}",
      "ROLLBACK:",
      "  - ${9:How to undo safely}",
      "RUNBOOK/LINKS:",
      "  - ${10:ADR-xxx / PR# / wiki}",
      "OWNER: ${11:Your Name}",
      "LAST UPDATED: ${12:YYYY-MM-DD}",
      "CHANGELOG:",
      "  - ${13:YYYY-MM-DD}: ${14:Initial} (${15:you})"
    ]
  }
}
```

**Usage:**
1. Open any file
2. Type `crumbs`
3. Hit Tab
4. Fill in the fields

**Result:** Every script, query, and module gets consistent documentation in 30 seconds.

---

## "But Won't This Be Too Verbose?"

**Only the header is verbose.**

Inline comments stay tight with tags like:
- `NOTE:` → Clarification
- `WHY:` → Business reason
- `CAVEAT:` → Edge case
- `VERIFY:` → Spot