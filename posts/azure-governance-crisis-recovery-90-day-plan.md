---
title: "Azure Governance Crisis Mode: The 90-Day Recovery Framework (2025)"
date: 2025-12-30
summary: "Your environment is on fire. You have 3 months to fix it before the renewal audit. Here is the triage sequence for Brownfield Recovery."
tags: ["Azure", "Governance", "Crisis Management", "FinOps", "Recovery"]
hub: "governance"
layout: "Post"
---

Your environment is on fire. You have 3 months. Maybe an audit is coming, or maybe the CFO finally looked at the bill.

You don't need a "Center of Excellence" right now. You need triage.

This is the 90-day recovery framework for bringing a chaotic Azure brownfield back from the brink.

---

## Days 1-30: Stop the Bleeding (Triage)

The goal here isn't perfection; it's visibility. You can't kill what you can't see.

### Technical Magnet: The Triage KQL

Run this query immediately. It identifies your "Bleeders" — the most expensive resources that have no localized accountability (missing Owner or CostCenter tags).

```kusto
// Top 20 Most Expensive "Orphan" Resources
Usage
| where TimeGenerated > ago(30d)
| where Tags !has "Owner" or Tags !has "CostCenter"
| summarize TotalCost = sum(Cost) by ResourceId, ResourceGroup
| top 20 by TotalCost desc
| project ResourceId, TotalCost, ResourceGroup
```

*Don't try to tag everything yet. Just tag these 20. Call the people. Ask "Is this yours?"*

---

## Days 31-60: The Structural Firewall

Once you've identified the worst offenders, you need to stop new ones from entering the building.

1.  **Freeze Permissions:** Stop handing out 'Contributor' access to subscriptions.
2.  **Deploy Deny Policies:** Block creation of resources without 'CostCenter' in your production scopes.

---

## Days 61-90: The Kill List

Now you have visibility and a firewall. It's time to delete.

*   Decommission zombie resources found in Triage.
*   Right-size the "Safety Buffer" VMs that devs oversized "just in case."

---

## The Crisis RACI

Recovery is political. You will be turning off servers that people claim are critical (but haven't been logged into for 6 months).

**[Download the Azure RACI Matrix](https://gumroad.com/l/raci-template?ref=cost-recovery-crisis)** to define the 'Crisis Manager' role who has the authority to pull the plug.

<div class="downloads" style="text-align: center; margin-top: 2rem;">
  <a class="btn" href="https://gumroad.com/l/raci-template?ref=cost-recovery-crisis" style="font-size: 1.2em; padding: 15px 30px; background-color: #0078d4; color: white;">Get the Crisis RACI</a>
  <div class="preview-block" style="margin-top: 10px; font-size: 0.9em; color: #555;">
     <span>✅ Roles Included</span> • <span>💲 Price: $29</span> • <span>📊 Excel Format</span>
  </div>
</div>
