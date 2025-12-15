---
title: Azure Dashboards Are Your Cloud NOC (And Nobody Told You)
date: 2025-10-03
summary: How to design Azure dashboards for a Cloud NOC team that actually answer
  questions instead of dumping metrics on a big screen.
tags:
- Azure
- Azure Monitor
- Cloud NOC
- Dashboards
- Governance
- Monitoring
- Operations
- Workbooks
cover: static/images/hero/cloud-noc.png
hub: governance
related_posts:
  - azure-resource-tags-guide
  - azure-tag-governance-policy
  - azure-policy-reality-check
cover: "/static/images/hero/azure-dashboards-cloud-noc.png"
---

This guide is part of our [Azure Governance hub](/hub/governance/) covering policy enforcement, compliance frameworks, and enterprise controls.
## The Problem Nobody Explains

You land in a new Azure admin role. You inherit an environment. Your boss asks you three simple questions:

- "What's running?"
- "Are we patched?"
- "What's this costing us?"

And you have no idea where to start.

Somebody tells you "use Azure Workbooks" or "build a dashboard." You Google it. You find Microsoft docs. You see KQL queries and JSON syntax and parameter configuration screens.

But nobody told you **why** you're doing this. What problem does a workbook solve? What's a dashboard for? Why does this tool exist?

You're being told to use the quadratic formula without understanding what it means to solve for X.

## The Algebra Problem

Remember learning algebra? You're told "solve for X" but nobody explains WHY you're doing it.

The teacher says: "Use the quadratic formula."
You ask: "But what am I solving?"
The teacher: "Just plug in the numbers."

Azure admins face the same problem:

The docs say: "Use Azure Workbooks."
You ask: "But what problem am I solving?"
The docs: "Here's the KQL syntax."

**Here's what nobody tells you:**

Workbooks and dashboards aren't mysterious Azure tools. They're just **saved transformations of raw data into organized information**. That's it.

Azure generates data constantly - metrics, logs, resource properties, configuration states. But raw data isn't useful. **Information** is useful.

Without workbooks/dashboards: You manually query data every time you need an answer.
- "How many VMs are running?" → Click through the portal
- "How many are Windows vs Linux?" → Do it again
- "Which ones have high CPU?" → Do it again

With workbooks/dashboards: You've saved those queries as reusable views.
- "How many VMs are running?" → One click
- "How many are Windows vs Linux?" → One click
- "Which ones have high CPU?" → One click

**You're not learning a new concept. You're learning to stop repeating yourself.**

## What Leadership Actually Understands: The NOC

Here's where it clicks.

Your leadership already understands this concept. They just don't know it applies to Azure.

**They understand Network Operations Centers (NOCs):**

- Big screens on the wall
- Red/yellow/green status lights
- One glance tells you if something's broken
- Drill down when you see red
- 24/7 monitoring from a centralized location

Every executive who's walked past the IT department has seen a NOC. They know what it does.

**Your translation:**

"We're building a cloud NOC. Instead of monitoring network switches and routers, we're monitoring Azure infrastructure across [insert your number] subscriptions."

**They get it instantly.**

The NOC parallel:

| Traditional NOC | Cloud NOC (Azure Dashboard/Workbook) |
|-----------------|--------------------------------------|
| Shows all network devices | Shows all cloud resources |
| Real-time status (up/down/degraded) | Real-time status (running/stopped/at-risk) |
| Alerts when something breaks | Alerts when something breaks |
| One person monitoring, whole team knows status | Leadership gets same visibility |

**Azure dashboards and workbooks ARE a NOC for cloud infrastructure.** That's the entire concept.

If you understand NOC, you understand dashboards.

## Your Cloud NOC: What It Actually Is

Now that you understand the NOC concept, here's how Azure implements it:

**Azure Workbooks = Your NOC Screen**
- Interactive dashboards that display infrastructure health
- Combine data from multiple sources
- Parameters let you filter (click subscription → see only those resources)
- Real-time queries that update automatically

**Azure Dashboards = Your Quick-Glance View**
- Pinned tiles showing key metrics
- Auto-refresh every 5 minutes (metrics) or hourly (logs)
- Simpler than workbooks, but less interactive
- Good for "what's on fire RIGHT NOW"

**Think of it this way:**

- **Dashboard** = The big wall screen in the NOC (high-level status)
- **Workbook** = The detailed console where you drill down and investigate

Both are just different views into your cloud infrastructure. Pick the one that fits your audience:
- **Leadership wants dashboards** (quick status check)
- **Admins want workbooks** (deep investigation)

You'll probably use both.

---

## The Foundation Nobody Teaches: Two Data Sources

Here's where new admins get confused: **What data goes where?**

You build a workbook. You see options for "Logs" and "Azure Resource Graph." You don't know which one to use. So you guess. And you waste hours querying the wrong data source.

**Nobody explains the difference:**

### Resource Graph = Inventory (What Exists RIGHT NOW)

- Current state of every resource
- Properties, tags, locations, configurations
- "Show me all VMs that are running"
- "Which resources don't have tags?"
- "What's the size of each VM?"
- Updates in near real-time (within minutes)

**Think of it as:** Your asset inventory database.

### Log Analytics = History (What HAPPENED Over Time)

- Performance metrics, events, logs
- Trends, patterns, anomalies
- "Show me CPU usage over the last 30 days"
- "Which VMs rebooted unexpectedly?"
- "When did disk space drop below 10%?"
- Requires logs to be collected and shipped first

**Think of it as:** Your security camera footage and performance recorder.

### The Trap Most Admins Fall Into

They try to use Log Analytics for inventory questions: "How many VMs do we have?"

**This fails** because Log Analytics only knows about resources that are SENDING LOGS. If a VM isn't configured to send logs, it doesn't exist in Log Analytics.

Or they try to use Resource Graph for performance history: "Show me CPU over 30 days."

**This fails** because Resource Graph only knows the CURRENT state. It doesn't store historical performance data.

### When To Use Which

| Question | Data Source | Why |
|----------|-------------|-----|
| How many VMs exist? | Resource Graph | Current inventory |
| Which VMs are running? | Resource Graph | Current state |
| Which VMs lack tags? | Resource Graph | Current configuration |
| CPU usage over 30 days? | Log Analytics | Historical performance |
| Which VMs had errors yesterday? | Log Analytics | Historical events |
| Disk space trends? | Log Analytics | Time-series data |

### The Power Move: Combine Them

Your best workbooks use BOTH:

1. **Resource Graph** gives you the complete inventory
2. **Log Analytics** shows you what's happening on those resources

Example: "Show me all VMs (Resource Graph) and highlight which ones have high CPU in the last hour (Log Analytics)."

That's your cloud NOC. Complete visibility.

## The 44 Subscription Problem

In my production environment, I manage 44 Azure subscriptions for a regional bank. We're merging with another bank in Q1 2026, so that number's about to grow.

**Without a cloud NOC, here's what answering basic questions looks like:**

Leadership: "How many VMs are unpatched?"
Me: *Opens portal, clicks first subscription, filters VMs, checks patch status, exports to Excel. Repeats 43 more times. Three days later...*

Leadership: "How many Windows Server 2012 VMs do we still have?"
Me: *Starts clicking through 44 subscriptions again...*

**This doesn't scale. You can't manually check 44 subscriptions.**

### What You Need: Cross-Subscription Visibility

Resource Graph solves this with ONE query across ALL subscriptions:

```kql
Resources
| where type == "microsoft.compute/virtualmachines"
| summarize count() by tostring(properties.storageProfile.osDisk.osType)
```

Result: 712 VMs total, 445 Windows, 267 Linux.

One query. 30 seconds. Every subscription.

### The Three Questions Leadership Actually Cares About

When I built our cloud NOC, I focused on three things:

**1. Control: "Do we even know what's running?"**
- VM inventory across all subscriptions
- Resources without required tags
- Orphaned resources (no owner, no cost center)

**2. Risk: "What's not patched? What's exposed?"**
- VMs not sending logs (blind spots)
- Unpatched systems by severity
- Public-facing resources

**3. Cost: "Where's the money going?"**
- Largest resources by cost
- Stopped-but-not-deallocated VMs (still charging)
- Resources in wrong regions (higher cost)

### How To Build This Without Dying

You don't build 44 dashboards. You build ONE workbook with subscription parameters.

The user picks a subscription from a dropdown, and the entire workbook filters to show only that subscription's data. Or they select "All Subscriptions" and see everything.

**This is the cloud NOC approach.**

One screen. All subscriptions. Real-time data. Leadership gets answers in 30 seconds instead of waiting 3 days for you to click through portals.

## How To Explain This To Leadership

Here's your 5-minute pitch. I've used this exact script with my executive team.

**Don't say this:**
"We need to implement Azure Monitor Workbooks with Resource Graph and Log Analytics integration for cross-subscription visibility and KQL-based alerting."

**Say this:**

"Right now, we're blind across 44 Azure subscriptions. When you ask me a simple question like 'How many VMs are unpatched?' I spend 3 days clicking through portals.

I'm building a cloud NOC - the same concept as our traditional network operations center, but for cloud infrastructure.

**Here's what you'll get:**

One dashboard that shows:
- What we have (complete inventory)
- What's at risk (unpatched systems, security issues)
- What's costing us money (waste, oversized resources)

It updates automatically. You'll have answers in 30 seconds instead of waiting days.

**Plus, we get alerts** - just like the NOC. If VM count drops unexpectedly, if untagged resources exceed our threshold, if critical systems go offline - the system alerts us proactively instead of waiting for someone to notice.

Same NOC concept you already understand. Just moved to the cloud."

### What They'll Ask

**"How long to build it?"**
"Initial version with basic inventory and health checks: 2 weeks. Then we iterate based on what questions you need answered."

**"What does it cost?"**
"The tools are included with Azure at no additional cost. Just my time to build and maintain it."

**"Can I see it on my phone?"**
"Yes. Dashboards work on mobile. Workbooks work in any browser."

**"What about alerts?"**
"We set thresholds - like 'notify me if VM count changes by more than 10%' or 'alert if any critical system shows unhealthy.' Same as your traditional NOC alarm system."

### The Visual They Need

Show them this:

**Before (Now):**
- 44 separate subscriptions
- Manual checks
- 3 days to answer basic questions
- Reactive (find problems after they happen)

**After (Cloud NOC):**
- One unified view
- Automated monitoring
- 30 seconds to answer questions
- Proactive (alerts before users notice)

They'll approve it on the spot.

## What You Build First

Start simple. Don't try to build everything at once.

**Week 1: Basic Inventory Workbook**

One workbook. Three queries. Resource Graph only.

**Query 1: VM Inventory**
```kql
Resources
| where type == "microsoft.compute/virtualmachines"
| extend powerState = properties.extended.instanceView.powerState.code
| project name, resourceGroup, location, 
    osType = tostring(properties.storageProfile.osDisk.osType),
    vmSize = tostring(properties.hardwareProfile.vmSize),
    powerState
| order by name asc
```

Shows you every VM, its OS, size, and whether it's running.

**Query 2: Resources Without Required Tags**
```kql
Resources
| where tags !has "CostCenter" or tags !has "Owner"
| project name, type, resourceGroup, subscriptionId
| order by type asc
```

Finds governance violations immediately.

**Query 3: Stopped VMs Still Charging**
```kql
Resources
| where type == "microsoft.compute/virtualmachines"
| extend powerState = properties.extended.instanceView.powerState.code
| where powerState == "PowerState/stopped"
| project name, resourceGroup, location, vmSize = tostring(properties.hardwareProfile.vmSize)
```

These VMs are stopped but NOT deallocated - still charging you.

**That's it. Three queries. Your first cloud NOC.**

### Week 2: Add Parameters

Add a subscription dropdown so users can filter to one subscription or view all.

Add a resource group filter.

Add a location filter.

Now your workbook is interactive.

### Week 3: Add Alerts

Set up Resource Graph alerts for:

**Alert 1: VM Count Change**
Trigger when VM count changes by more than 10% (catches accidental deletions or unexpected deployments)

```kql
Resources
| where type == "microsoft.compute/virtualmachines"
| summarize VMCount = count()
```

Alert condition: VMCount decreased by more than 10% from baseline

**Alert 2: Untagged Resources**
Trigger when untagged resources exceed threshold

```kql
Resources
| where tags !has "CostCenter" or tags !has "Owner"
| summarize UntaggedCount = count()
```

Alert condition: UntaggedCount > 50

**Alert 3: Public-Facing VMs**
Trigger when any VM gets a public IP (potential security risk)

```kql
Resources
| where type == "microsoft.compute/virtualmachines"
| where isnotnull(properties.networkProfile.networkInterfaces)
| mv-expand nic = properties.networkProfile.networkInterfaces
| extend nicId = tostring(nic.id)
| join kind=inner (
    Resources
    | where type == "microsoft.network/networkinterfaces"
    | mv-expand ipconfig = properties.ipConfigurations
    | where isnotnull(ipconfig.properties.publicIPAddress)
) on $left.nicId == $right.id
| project vmName = name, publicIP = tostring(ipconfig.properties.publicIPAddress.id)
```

Alert condition: Any results returned (new public IP detected)

These three alerts catch 80% of common issues.

### Week 4: Add Log Analytics

Now add performance data for VMs that are sending logs:

**VM Performance Over Time**
```kql
Perf
| where TimeGenerated > ago(24h)
| where ObjectName == "Processor" and CounterName == "% Processor Time"
| summarize AvgCPU = avg(CounterValue) by Computer, bin(TimeGenerated, 1h)
| render timechart
```

**VMs Not Sending Logs (Blind Spots)**
```kql
// Get all VMs from Resource Graph
let AllVMs = Resources
| where type == "microsoft.compute/virtualmachines"
| project Computer = name;
// Get VMs with recent heartbeats in Log Analytics
let ActiveVMs = Heartbeat
| where TimeGenerated > ago(1h)
| distinct Computer;
// Find the difference
AllVMs
| join kind=leftanti ActiveVMs on Computer
```

This shows you VMs that exist but aren't sending data - your blind spots.

### What Success Looks Like

After 4 weeks:
- Leadership can open one workbook and answer their own questions
- You get alerted to problems before users notice
- You're not manually clicking through 44 subscriptions
- You've built a cloud NOC

Then you iterate based on what questions keep coming up.

## The Bottom Line

Azure dashboards and workbooks aren't mysterious tools. They're your cloud NOC.

**The foundation:**
- **Resource Graph** = Inventory (what exists right now)
- **Log Analytics** = History (what happened over time)
- **Workbooks** = Your NOC screen (interactive investigation)
- **Dashboards** = Your wall display (quick status check)
- **Alerts** = Your alarm system (proactive notification)

**The business translation:**
Leadership already understands NOCs. You're just moving the concept to the cloud.

**The practical approach:**
Start with basic inventory queries. Add parameters for interactivity. Set up alerts for common issues. Layer in performance data from Log Analytics.

Four weeks. One workbook. Complete visibility across all your subscriptions.

**What most admins miss:**
They jump straight into building complex workbooks without understanding WHY they exist or WHAT PROBLEM they solve. Now you know both.

You're not learning a new concept. You're building a cloud NOC using tools that already exist in Azure.

**Next steps:**
1. Open Azure Monitor → Workbooks
2. Create a new workbook
3. Add your first Resource Graph query (VM inventory)
4. Save it
5. Show your boss

That's your cloud NOC. Now build it.

---

**Resources:**
- [Azure Resource Graph documentation](https://learn.microsoft.com/en-us/azure/governance/resource-graph/)
- [Azure Monitor Workbooks overview](https://learn.microsoft.com/en-us/azure/azure-monitor/visualize/workbooks-overview)
- [Create alerts with Resource Graph](https://learn.microsoft.com/en-us/azure/governance/resource-graph/alerts-query-quickstart)
- [My KQL Cheat Sheet](https://azure-noob.com/blog/kql-cheat-sheet/) - for when you're ready to write more complex queries

**Got questions?** Drop them in the comments. If you're struggling to explain this to your leadership, you're not alone - and now you have the translation.