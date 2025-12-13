---
title: 'Azure Update Manager Reality Check: Why 77% of Your VMs Are Unsupported'
date: 2025-09-24
summary: 'What Azure Update Manager really looks like in an enterprise: agent confusion,
  SCCM overlap, and how to make patching governance work.'
tags:
- Azure
- Azure Governance
- Azure Update Manager
- Governance
- KQL
- Monitoring
- Operations
- Patching
- Update Management
- Update Manager
- VM Management
cover: static/images/hero/azure-update-manager.png
hub: governance
---
# Azure Update Manager Reality Check: Why 77% of Your VMs Are Unsupported

When I first opened Azure Update Manager, I nearly had a heart attack. The dashboard cheerfully informed me that **1,791 virtual machines** needed attention. As someone responsible for keeping our Azure environment secure and compliant, seeing that number felt like staring down an impossible task.

Here's what I wish someone had told me on day one: **that number is completely misleading**.

After digging deep into our environment, running queries, and actually understanding what Azure Update Manager can and can't handle, I discovered the uncomfortable truth: **only 348 of those 1,791 VMs should actually be managed by Azure Update Manager**. That's 77% of our environment that shouldn't be there in the first place.

If you're facing a similar shock when you open Azure Update Manager, this post will save you weeks of confusion and help you focus on what actually matters.

## The Problem: Azure Update Manager Shows Everything

Azure Update Manager has a dirty little secret: it displays every single VM it can see, regardless of whether it should manage that VM or not. It doesn't understand that your environment is complex. It doesn't know about your Citrix VDI infrastructure, your Databricks clusters, or your security appliances that should never be touched by automated updates.

![Azure Update Manager Dashboard showing 1,791 VMs](/static/images/azure-update-manager-before.png)

Looking at this dashboard, my first instinct was panic. How could we possibly manage updates for nearly 1,800 virtual machines? Where do we even start?

The answer: we don't. Because most of these VMs are being managed by other tools, are specialized appliances, or simply aren't suitable for Azure Update Manager.

## The Reality: Most VMs Have Better Update Methods

Here's the breakdown of our "1,791 VMs that need updates":

| Platform Type | Count | Update Method | Responsible Team |
|---------------|-------|---------------|------------------|
| **Citrix VDI** | ~900 VMs | Intune | Citrix Team |
| **Azure Databricks** | ~170 VMs | Azure Databricks Solution | Databricks Team |
| **Windows Desktop OS** | 44 VMs | Intune | Desktop Team |
| **Security Appliances** | 46 VMs | Vendor Updates | Security Team |
| **Network Appliances** | 20 VMs | Vendor Updates | Network Team |
| **Other Appliances** | 7 VMs | Vendor Updates | Various Teams |
| **TOTAL UNSUPPORTED** | **~1,187 VMs** | **Various Methods** | **Multiple Teams** |

**The real number of VMs that should use Azure Update Manager? 348.**

That's a 77% reduction from what the dashboard initially showed us. Suddenly, the task went from "impossible" to "manageable."

## Why This Happens: Azure Update Manager Doesn't Understand Context

Azure Update Manager is designed to be simple: "Hey, there are VMs here, they probably need updates!" But enterprise environments are anything but simple.

**Citrix VDI Systems (900 VMs):** These are managed through Intune with carefully orchestrated update schedules that coordinate with user sessions. Azure Update Manager would break this process.

**Azure Databricks (170 VMs):** These are ephemeral compute clusters managed by the Databricks service itself. They get updated as part of the cluster lifecycle, not through traditional patching.

**Security Appliances (46 VMs):** Firewalls, intrusion detection systems, and other security tools require vendor-specific update procedures. One wrong automatic update could take down your entire network security posture.

**Desktop VMs (44 VMs):** Windows 10/11 virtual desktops are managed through Intune with different policies than servers. They need user-focused update schedules, not server maintenance windows.

**The lesson:** Just because Azure Update Manager can see a VM doesn't mean it should manage that VM.

## The Solution: KQL Queries to Find Your Real Targets

Instead of trying to manage all 1,791 VMs, I used Azure Resource Graph queries to identify which systems should actually be excluded from Azure Update Manager.

### Query 1: Identify Unsupported Systems

This query finds all the VMs that should be managed by other tools:

```kql
Resources
| where type == "microsoft.compute/virtualmachines"
| extend publisher = tostring(properties.storageProfile.imageReference.publisher)
| extend rgName = tostring(resourceGroup)
| where publisher in ("AzureDatabricks", "tenable", "paloaltonetworks", "MicrosoftWindowsDesktop") or
        subscriptionDisplayName contains "Citrix" or
        rgName contains "citrix" or
        rgName contains "databricks"
| project VMName = name, Publisher = publisher, Subscription = subscriptionDisplayName, ResourceGroup = rgName
| order by Subscription, ResourceGroup, VMName
```

This query identified our 1,187 unsupported systems by looking for:
- **Publisher patterns**: Databricks VMs, security appliances, Windows Desktop images
- **Subscription patterns**: Anything with "Citrix" in the subscription name
- **Resource group patterns**: Groups containing "citrix" or "databricks"

### Query 2: Count Unsupported Systems by Type

To understand the scope of what we're excluding:

```kql
Resources
| where type == "microsoft.compute/virtualmachines"
| extend publisher = tostring(properties.storageProfile.imageReference.publisher)
| extend rgName = tostring(resourceGroup)
| where publisher in ("AzureDatabricks", "tenable", "paloaltonetworks", "MicrosoftWindowsDesktop") or
        subscriptionDisplayName contains "Citrix" or
        rgName contains "citrix" or
        rgName contains "databricks"
| summarize VMCount = count(), VMNames = make_list(name) by publisher, subscriptionDisplayName, rgName
| order by VMCount desc
```

This showed us exactly where our unsupported VMs were concentrated and helped validate our filtering logic.

## The Filter Effect: From Chaos to Clarity

After applying these filters in Azure Update Manager (by excluding the problematic resource groups and subscriptions), the dashboard transformation was dramatic:

**Before filtering:** 1,791 VMs  
**After filtering:** 348 VMs

![Azure Update Manager Dashboard after filtering](/static/images/azure-update-manager-after.png)

Suddenly, Azure Update Manager became a useful tool instead of an overwhelming problem. We went from "How do we handle 1,800 VMs?" to "Here are the 348 VMs we actually need to focus on."

## The Business Impact: Focus on What Matters

This filtering approach delivered immediate business value:

**Risk Reduction:** We eliminated the risk of accidentally updating critical appliances or breaking carefully managed VDI environments.

**Resource Optimization:** Our team could focus on 348 VMs instead of trying to understand 1,791 different systems.

**Clear Accountability:** Each system type has a clear owner and update methodology. No more confusion about who's responsible for what.

**Realistic Planning:** Update schedules and maintenance windows became manageable when scoped to the right systems.

## Key Takeaways for Your Environment

**Don't trust the initial numbers:** Azure Update Manager will show you every VM it can see. Most of them probably shouldn't be there.

**Understand your ecosystem:** Map out which tools are already managing updates for different system types. Don't create duplicate or conflicting processes.

**Use filtering aggressively:** Azure Update Manager works best when it's focused on systems that actually belong there.

**Document your exclusions:** Keep track of why certain VMs are excluded so future team members understand the decisions.

## What's Next: Making the 348 VMs Actually Automated

Having identified our real target VMs is just the first step. In my next post, I'll show you why those 348 VMs still aren't being updated automatically, even with Azure Update Manager policies in place, and the missing piece that most Azure documentation doesn't tell you about.

The short version: policies configure VMs for automation, but they don't actually schedule when updates happen. That requires maintenance configurations, and there's a gap between the two that catches most administrators off guard.

---

**Want to audit your own environment?** Copy the KQL queries above and run them in Azure Resource Graph Explorer. You might be surprised by how many of your "problem VMs" are actually being managed perfectly well by other tools.

*Next in this series: "The Azure Update Manager Automation Gap (And How to Fix It)"*