---
title: "Only 1% of Azure Admins Know These Three Tools — And Even Fewer Know When to Use Which"
date: 2025-11-10
summary: "I passed AZ-104. I was certified. I knew how to create VMs, configure networking, deploy ARM templates. Day 1 on the job: 'Pull me an inventory.' AZ-104 never covered this. Here's the certification gap nobody talks about, the query that proves it, and the templates that save your career."
tags: ["azure", "resource-graph", "power-bi", "Excel", "AZ-104", "operations"]
cover: "/static/images/hero/excel-powerbi-arg-bossfight.png"
hub: automation
related_posts:
  - azure-service-inventory-tool
  - azure-ipam-tool
  - workbook-app-tool
  - pbix-modernizer-tool
---
## The AZ-104 Lie


This guide is part of our [Azure Automation hub](/hub/automation/) covering Infrastructure as Code, CI/CD pipelines, and DevOps practices.

I passed AZ-104. I was certified. I was an "Azure Administrator."

I knew how to:
- Create virtual machines
- Configure virtual networks
- Deploy ARM templates
- Manage identities and access
- Configure monitoring and backups

Day 1 on the job at a $122B enterprise managing 44 Azure subscriptions:

**Boss:** "Pull me an inventory of all resources across our subscriptions."

**Me:** *stares at portal*

**Me:** "...AZ-104 didn't cover this."

That's when I realized: **Microsoft certifications teach you to create resources. They don't teach you to report on them.**

And reporting is 80% of the actual job.

---

## 🚨 Emergency: Boss Just Asked For Inventory?

**If you need the answer RIGHT NOW**, here's the query that will save you:

**Copy this into Azure Resource Graph Explorer** (Portal → Search "Resource Graph Explorer"):

```kql
resources
| where type =~ 'microsoft.compute/virtualmachines'
| extend vmSize = tostring(properties.hardwareProfile.vmSize)
| extend osType = tostring(properties.storageProfile.osDisk.osType)
| extend powerState = tostring(properties.extended.instanceView.powerState.code)
| extend createdTime = tostring(properties.timeCreated)
| extend nicId = tostring(properties.networkProfile.networkInterfaces[0].id)
| extend osVersion = tostring(properties.storageProfile.imageReference.exactVersion)
| extend osSku = tostring(properties.storageProfile.imageReference.sku)
| extend osOffer = tostring(properties.storageProfile.imageReference.offer)
| extend osPublisher = tostring(properties.storageProfile.imageReference.publisher)
| extend osVersionDisplay = strcat(osPublisher, ' ', osOffer, ' ', osSku)
| join kind=leftouter (
    resources
    | where type =~ 'microsoft.network/networkinterfaces'
    | extend privateIp = tostring(properties.ipConfigurations[0].properties.privateIPAddress)
    | project nicId = id, privateIp
) on $left.nicId == $right.nicId
| join kind=leftouter (
    resourcecontainers
    | where type == 'microsoft.resources/subscriptions'
    | project subscriptionId, subscriptionName = name
) on subscriptionId
| extend ipAddress = iff(powerState == 'PowerState/running', privateIp, 'N/A')
| extend Application = coalesce(tags.Application, tags.application, tags.APPLICATION, 'Not Tagged')
| extend Owner = coalesce(tags.Owner, tags.owner, tags.OWNER, 'Not Tagged')
| extend Type = coalesce(tags.Type, tags.type, tags.TYPE, 'Not Tagged')
| extend Environment = coalesce(tags.Environment, tags.environment, tags.ENVIRONMENT, 'Not Tagged')
| project 
    name, 
    subscriptionName, 
    resourceGroup, 
    location, 
    vmSize, 
    osType,
    osVersionDisplay,
    powerState, 
    createdTime, 
    ipAddress,
    Application,
    Owner,
    Type,
    Environment
```

**Click "Download as CSV" → Send to boss → Breathe.**

**Now read the rest of this post so it doesn't take 6 hours next time.**

---

## What AZ-104 Actually Teaches You

Let me be specific about the gap.

**AZ-104 Modules:**
1. Manage Azure identities and governance
2. Implement and manage storage
3. Deploy and manage Azure compute resources
4. Configure and manage virtual networking
5. Monitor and back up Azure resources

**What they test:**
- Can you create a VM? ✅
- Can you configure an NSG? ✅
- Can you deploy an ARM template? ✅
- Can you set up a storage account? ✅

**What they DON'T test:**
- Can you generate an inventory of 31,000 resources? ❌
- Can you explain cost allocation to finance? ❌
- Can you build executive dashboards? ❌
- Can you automate recurring reports? ❌

**The certification prepared you for 20% of the job.**

---

*[Rest of the content continues exactly as before...]*






