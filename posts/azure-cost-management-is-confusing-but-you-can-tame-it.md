---
title: "Azure Cost Management is Confusing (But You Can Tame It)"
slug: azure-cost-management-is-confusing-but-you-can-tame-it
date: 2025-09-15
summary: "Azure bills are messy, dashboards don't always add up, and tags are a nightmare. Here's how I'm making sense of it — and how you can too."
tags: ["Azure", "FinOps", "Cost Management", "Governance"]
cover: "static/images/hero/azure-cost-reporting.png"
---

## What problem are we solving?

If you've ever opened the Azure Cost Management blade and thought:  
*"Why doesn't this number match the bill I just got?"* — you're not alone.  

Between **EA vs. CSP billing**, **reserved instances**, **mis-tagged resources**, and **the 36 different cost reports Azure offers**, it feels like the system is designed to confuse you. I've burned hours (days) reconciling numbers that *should* be simple.  

The problem: cloud spend is too important to ignore, but Azure doesn't make it easy.

---

## Subscription vs. Resource Group scope

This trips up almost everyone:  

- **Billing actually happens at the subscription level.**  
  Your invoice is tied to subscriptions — period.  
- **Resource groups don't generate invoices.**  
  They're just a logical container inside a subscription.  
- **Cost reports at the resource group level are just slices.**  
  They're helpful for chargeback/showback, but they will never perfectly match what you see at the subscription scope.  

👉 **Rule of thumb:** Always reconcile subscription totals first. Use resource group reports for allocation, not for truth-in-billing.

---

## Tags: the only way to get sane reporting

As I wrote in [my earlier post on tags and governance](link-to-post), if your tags are junk, your cost reports are junk.  

Here's my go-to tagging scheme:

- `Application` — what workload/service this belongs to  
- `Cost Center` — which budget/code pays for it  
- `Owner` — the person or team responsible  
- `Environment` — `Prod`, `Dev`, `Test`, etc.  
- `Type` — is it a `Server`, `Appliance`, or `Desktop`  

When these are applied consistently, I can slice and dice costs in ways finance actually cares about.  
When they're missing? I may as well be reading hieroglyphics.

---

## The Azure Cost Management connector

This is where things start to get powerful:  

- The **Azure Cost Management connector** pulls cost data into **Power BI**.  
- It gives you the same underlying data that drives the portal — but you can automate, transform, and visualize it however you like.  
- You can connect at different scopes: subscription, management group, or billing account.  

Why use it?  
- Automate **monthly chargeback reports**  
- Blend Azure data with **on-prem costs** or other clouds  
- Fix gaps in the portal UI with your own dashboards  

---

### What you actually get

Here's what the connector pulls into Power BI:

![Azure Cost Management Connector in Power BI](/static/images/hero/azure-cost-connector.png)

You don't just get one dataset — you get multiple tables like:

- **Pricesheet** — contracted rates  
- **RI Transactions / Usage / Recommendations**  
- **Usage Details** — granular meter-by-meter usage  
- **Amortized Usage** — spreads RI costs across benefiting resources  

And the connector doesn't just give you raw tables — it wires them up into a **data model** automatically:

![Azure Cost Management Connector Data Model](/static/images/hero/azure-cost-model.png)

- **Subscriptions** → filter and group correctly  
- **Resources** → names, groups, and tags  
- **Usage Details / Amortized Usage** → raw vs. RI-adjusted spend  
- **Pricesheet** → actual contracted rates  
- **Calendar** → month/quarter/year rollups  

This saves hours of modeling work. Instead of manually joining CSVs, you start with a star schema ready for dashboards.

---

### How much data should you pull?

By default, the connector suggests **3 months of data**. That's not random — the files are **huge** even at 3 months, and refreshes get slow.  

My **leadership asked me to carry 13 months** for trending and forecasting. Sounds good in theory, but in practice I hit constant **refresh failures**. Even Microsoft support couldn't solve it.  

The fix:  
- **Premium workspace required.** Standard Power BI just couldn't handle the volume. Once I moved to a premium workspace, refreshes became reliable again.  

👉 Lesson learned: leadership will always want more history, but you have to balance that against technical limits. Start small, scale if you have capacity.

---

### A note on Chris Bowman's Cost Board

When I explored Chris Bowman's [Azure Cost Reporting board](https://github.com/ChrisBowman/azure-cost-reporting), one "gotcha" for me:  
- His **Calendar** was a *calculated table* built in DAX.  
- At first, I couldn't find much DAX, which left me scratching my head.  

That tripped me up until I realized I needed my own calendar + custom DAX to slice by the tags I care about (`Application`, `Cost Center`, `Owner`, `Environment`, `Type`).  

---

### Why tags matter (the hard way)

As soon as I put those tags into slicers, I saw just how messy things were:  

![Blank tags in Application slicer](/static/images/hero/azure-tags-blank.png)

- `(Blank)` values eating up thousands of dollars in costs  
- Raw, inconsistent tag strings nobody could actually use  
- A few clean ones (`Active Directory`, `APIM-Dev`) lost in the noise  

And when a cost shows up as **blank** in a board-level report, leadership doesn't shrug — they ask *who owns this, why isn't it tagged, and why are we paying for it?*  

That single exercise turned cost reporting into a governance spotlight.

---

### Cleaning messy tags with DAX

This is where cost, meter category, and tags collide.  

I created a calculated column to **extract a clean Application name** from messy tag strings (Rubrik, Citrix, Databricks, etc.), so I could finally answer the leadership question:  
*"How much does that app cost me a day?"*

![DAX tag extraction demo](/static/images/hero/azure-dax-extract.png)

**Calculated column on `Resources`:**
```dax
Tags.Application_clean =
VAR Key1     = "Application="
VAR Key2     = "ApplicationId="
VAR Src      = Resources[Tags]
VAR p1       = FIND(Key1, Src, 1, 0)
VAR p2       = FIND(Key2, Src, 1, 0)
VAR UseKey   = IF(p1 > 0, Key1, IF(p2 > 0, Key2, BLANK()))
VAR StartPos = IF(ISBLANK(UseKey), 0, FIND(UseKey, Src, 1, 0) + LEN(UseKey))
VAR EndSemi  = FIND(";", Src, StartPos, LEN(Src) + 1)
VAR EndComma = FIND(",", Src, StartPos, LEN(Src) + 1)
VAR EndPos   = MIN(EndSemi, EndComma)
VAR RawValue = IF(StartPos > 0, MID(Src, StartPos, EndPos - StartPos), BLANK())
RETURN
