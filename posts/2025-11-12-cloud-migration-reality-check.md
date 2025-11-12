---
title: "The Spreadsheet I Wish I Had in 2019: Cloud Migration Reality Check"
date: 2025-11-12
summary: "Free Excel workbook with 54 readiness questions to inventory applications before Azure/CAF. Stop guessing, start migrating."
tags: ["Azure", "Cloud Migration", "Governance", "FinOps", "Reality Check"]
cover: "/static/images/hero/cloud-migration-spreadsheet.png"
---

## What problem are we solving?

In 2019, leadership said: *“We’re going to the cloud.”*

And that was it.  
No inventory, no ownership, no business case — just a deadline and an assumption that everything could move.

Every migration failure since then can be traced back to one question nobody could answer:

> **How many applications do we have?**

If you don’t know that, nothing else matters.  
You can’t plan, cost, secure, or govern what you don’t understand.

This post gives you the spreadsheet I wish I’d had that day — the one that would have stopped the chaos before it started.

---

## The idea

Instead of diving straight into Azure Migrate, CAF, or discovery tools, you start with a **readiness interview**.

Each question forces ownership, validation, and documentation before anyone touches the cloud.

The sheet is built to make leadership, app owners, and IT confront reality:

- Do we have the **installation media**?  
- Is the **vendor still in business**?  
- Who owns it — and who **pays for it**?  
- Does it have a **certificate**?  
- Is it **behind a load balancer**, or **public-facing**?  
- Can we even **reinstall** it?

Until those questions are answered, you’re not migrating — you’re gambling.

---

## Download the workbook

👉 **[Download Excel (.xlsx)](/static/downloads/Application_Questionnaire_Template_v2.xlsx)**  
👉 **[One-click Google Sheets template → Make a copy](https://bit.ly/cloud-readiness-template)** *(no sign-up required)*  
👉 **[Download CSV version](/static/downloads/Cloud_Migration_Readiness_Questionnaire_v2.csv)**  

The workbook includes a second **Dashboard** tab that auto-calculates:
- % of questions answered  
- % of high-confidence answers  
- Red-flag count  
- Critical-app total  

✅ Green = ready 🟡 Yellow = partial 🔴 Red = not ready

---

## Example preview

| # | Question | Example Answer | Confidence | Owner |
|---|-----------|----------------|-------------|--------|
| 1 | What is this application called internally? | CoreBanking | High | John Smith |
| 14 | Does this application use a certificate? If yes, where is it stored and when does it expire? | Yes — IIS cert expires Jan 2026 | Medium |  |
| 15 | Is this application behind a load balancer (Azure LB, F5, NSG, etc.)? | Yes, F5 VIP 10.10.5.21 | High |  |
| 16 | Is this application public-facing (accessible from the internet)? | No | High |  |
| 27 | Can this app be reinstalled from known media? | ISO stored on NAS01\\Software\\Apps | Low |  |

*Confidence scale: High = Verified · Medium = Believed · Low = Guess*

---

## Why it matters

This isn’t a technical checklist — it’s an **organizational mirror.**

It shows how ready your people, documentation, and processes actually are.

You’ll know you’re mature when:
- Every question has an owner.
- Every owner knows the answer.
- Every answer is validated, not assumed.

Until then, *you’re not migrating — you’re inventorying.*

---

## Next steps

1. Duplicate the Excel tab once per application.  
2. Fill it out collaboratively with business and IT.  
3. Only then, decide the **7R action** — Rehost, Refactor, Rearchitect, Rebuild, Replace, Retire, or Retain.  
4. Use the results to prioritize what’s actually ready versus what still needs discovery.

**👉 [Download the workbook now →](/static/downloads/Application_Questionnaire_Template_v2.xlsx)**  

This single exercise will save months of rework and six figures in migration waste.

---

## Closing thought

Before you build your first landing zone or VM, open the spreadsheet.

If you can’t fill out half of it, **you’re not ready yet — and that’s okay.**

Finding that out now means your migration will succeed later.

---

*Download the workbook. Ask the hard questions. Don’t migrate until you know what you own.*
