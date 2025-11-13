---
title: "Building an Azure CMDB | Resource Inventory with Azure Resource Graph and KQL"
date: 2025-10-11
summary: "How to build a Configuration Management Database for Azure using Resource Graph and KQL queries. Track 31,000+ resources across 44 subscriptions with real-time accuracy. Why traditional CMDBs fail and Azure Resource Graph succeeds."
tags: ["Azure", "CMDB", "Resource Graph", "KQL", "Inventory"]
cover: "/static/images/hero/cmdb-wrong.png"
---

ServiceNow CMDB said we had 8,000 resources. I opened the report:

```
AZRPRDVM001 - Owner: [blank]
SRV-SQL-02 - Owner: John Smith (terminated 2021)
LEGACY_APP_SERVER - Owner: [blank]
WIN2019-TEMP - Owner: [blank]
```

**What the hell is this? Who owns this? What does it even DO?**

Nobody knew.

So I spent **three months** bridging the gap between systems that don't talk to each other:

**RVtools exports** from 3 VMware vCenters showing VMs exist, but:
- No notes about what they do
- Virtual desktops mixed in with servers (both domain-joined)
- No visibility to physical devices
- Just server names with zero context

**ManageEngine** to find what RVtools can't see:
- Physical servers (RVtools only knows virtual)
- Which of the 21 AD domains each device authenticates against
- Filter out actual servers from virtual desktops

**ServiceNow CMDB** with records that:
- Show terminated employees as owners
- Have blank fields everywhere
- Don't match the RVtools inventory
- Contain servers that were decommissioned years ago

**Excel cross-referencing** trying to manually:
- Match RVtools VM names to ServiceNow records
- Figure out what these servers actually DO
- Find who ACTUALLY owns them (not John who left in 2021)
- Separate physical servers from VMs from virtual desktops
- Map applications to infrastructure nobody documented

**Email archaeology** searching old tickets for any mention of these servers

**Meetings with application teams** asking "is this yours?" over and over

And AD cleanup across 21 domains? That's a whole other animal. Which domains are actually still in use? Which accounts are still active? Who knows.

All of this because of tech debt baked in from years of people coming and going. Nobody documented what servers do. Nobody updated the CMDB when things changed. The people who built these systems don't work here anymore.

**After 3 months, I had a spreadsheet I barely trusted.**

**Then we migrated to Azure. I ran one Resource Graph query. 31,000 accurate, tagged resources in 30 seconds.**

## The Gap That Kills You

The problem isn't just that your CMDB is wrong. It's that your on-premises infrastructure has NO SYSTEM that connects:
- What servers exist (RVtools shows this)
- What they're for (nobody documented this)
- Who owns them (owners left years ago)
- What applications run on them (undocumented)

**RVtools shows you VMs exist.** Great. But it doesn't tell you:
- Is `WIN2019-TEMP` a production SQL Server or someone's test VM from 2019?
- Does anyone still use `AZRPRDVM001`?
- What application runs on `LEGACY_APP_SERVER`?
- Who do I ask when it breaks?

**ServiceNow CMDB has records.** Great. But they're:
- Missing half the servers RVtools found
- Showing owners who were terminated 2-3 years ago
- Full of blank fields where documentation should be
- Outdated the moment someone makes a change and forgets to update it

**The gap between "I can see servers exist" and "I know what they do" takes 3 months to bridge manually.**

That's the tech debt that kills enterprise IT.

## Why Azure Arc Wouldn't Have Fixed This

Someone will say: "Why didn't you use Azure Arc to manage on-premises infrastructure?"

**Because Arc doesn't magically document your servers.**

Even if we had connected every on-premises VM to Azure Arc (we didn't), I'd still need to:
- **Tag them manually** - Arc doesn't know "this is Finance CRM owned by Sarah"
- **Figure out what they do** - Arc doesn't read undocumented applications
- **Find actual owners** - Arc doesn't update ServiceNow records showing terminated employees
- **Separate servers from desktops** - Arc would connect both, creating MORE noise

Arc gives you management capabilities. It doesn't fix years of missing documentation. You'd still spend 3 months figuring out what these servers are before you could tag them properly in Arc.

The problem isn't the tool. The problem is nobody documented anything for years.

## The Multi-Tool Nightmare

On-premises environments make this worse because you need MULTIPLE tools just to understand what exists:

**VMware vCenter / RVtools:**
- Shows virtual machines
- Includes both servers AND virtual desktops if they're domain-joined
- Has no knowledge of physical devices
- No documentation about what VMs actually do
- We had 3 separate vCenters with no consolidated view

**ManageEngine:**
- Shows physical servers (which RVtools can't see)
- Maps which of 21 Active Directory domains devices authenticate against
- Needed to separate actual servers from virtual desktops
- Tracks last login times (critical for figuring out if anyone uses these)

**ServiceNow CMDB:**
- Supposedly the "single source of truth"
- Server names with no context
- Terminated employee names as owners
- Blank fields everywhere
- Records for servers decommissioned years ago

**Active Directory:**
- 21 domains accumulated through mergers
- Which ones are actually still in use?
- Which accounts are still active?
- Nobody knows without querying each domain individually

**Excel:**
- Where you dump all the exports
- Try to manually correlate data between systems
- Spend weeks cross-referencing hoping to find patterns

You can't answer basic questions without running queries across multiple systems and manually correlating the results:

**"How many SQL Servers do we have?"**  
Let me check RVtools for VMs named SQL... and ManageEngine for physical SQL boxes... and ServiceNow to see what's documented... and hope they all match. They won't.

**"Who owns AZRPRDVM001?"**  
ServiceNow says John Smith. John left in 2021. Let me check emails mentioning this server... ask around in meetings... eventually find someone who THINKS they know...

**"What application runs on LEGACY_APP_SERVER?"**  
Great question. Nobody documented it. The person who built it left. Let me check what's connecting to it and work backwards...

**Three months of this.** That's what it takes to build an inventory for a merger consolidation when your CMDB is wrong and your infrastructure has years of undocumented tech debt.

## Why Every CMDB Is Wrong

Your Configuration Management Database goes out of date the moment it's created:

**The process everyone follows:**
1. IT creates a server
2. IT updates the CMDB (maybe)
3. IT makes changes to the server over time
4. IT forgets to update the CMDB
5. Application owner leaves the company
6. New person inherits the server, doesn't update CMDB
7. IT decommissions the server
8. IT forgets to update the CMDB

**The result:** Your CMDB contains:
- Servers that were decommissioned years ago
- Servers missing from the inventory entirely
- Owner fields pointing to terminated employees
- Blank fields where documentation should be
- No connection to what applications actually run on these servers

**The excuse:** "We're too busy fixing things to update documentation."

That excuse is valid. When you're fighting fires, documenting assets falls to the bottom of the priority list. The problem isn't that people are lazy—it's that manual CMDB updates require discipline that doesn't survive operational pressure.

And nobody has time to go back and fill in the gaps later.

## Why This Goes Undetected for Years

The CMDB accuracy problem persists because of a knowledge gap at multiple organizational levels.

**Leadership approved the CMDB investment** based on industry best practices. Consultants recommended it. Compliance frameworks required it. The business case was approved. The tool was purchased.

**But validating CMDB accuracy requires technical knowledge** that many senior leaders don't have direct experience with. Most executives came up through different technological eras—they understand business operations, financial systems, and strategic planning. But configuration management databases? That's specialized IT infrastructure knowledge.

**This creates a validation challenge.** Leadership knows to check financial reports, sales metrics, and customer satisfaction scores. They have decades of experience with those domains and know what "good" looks like.

But how do you validate a CMDB if you've never worked directly with one? What questions should you ask? What metrics indicate health? What does "95% accurate" actually mean in practice?

**The result:** Leadership approves the CMDB purchase, sees it deployed, checks the compliance box, and trusts that IT is maintaining it properly. They don't realize they should be asking:

- "Show me your accuracy metrics from last month"
- "What's your process for updating records when servers change?"
- "How do you verify that owner information stays current?"
- "When was the last time we audited the CMDB against actual infrastructure?"

**They don't ask these questions because nobody taught them these are the questions to ask.** It's not a failure of leadership—it's a systemic knowledge gap. Technical inventory management wasn't part of their career development.

**IT teams, for their part,** often don't communicate CMDB health proactively. When pressed for time, they focus on keeping systems running rather than maintaining documentation. And since leadership isn't asking about CMDB accuracy, there's no forcing function to prioritize it.

**The problem becomes visible only when:**
- A merger requires consolidated inventory
- A migration demands accurate asset counts
- An audit exposes gaps
- A security incident reveals unknown systems
- Leadership asks a question that requires accurate data

By that point, the CMDB has been wrong for years. Not because anyone intended it to be wrong, but because no one in a position to enforce accountability had the technical context to recognize the problem earlier.

**Cloud migration often solves this indirectly.** Azure Resource Graph provides inventory data that leadership can validate without deep technical knowledge:

"How many servers do we have?" → Run a query, get a number  
"What's our Windows Server 2012 exposure?" → Run a query, get a list  
"Who owns the Finance infrastructure?" → Filter by Application tag, see owners

The data becomes accessible to non-technical stakeholders. And when the system enforces tagging at creation, accuracy becomes automatic rather than requiring manual discipline.

## The Meeting That Exposes It

Leadership asks: "How many servers are running SQL Server?"

You check ServiceNow CMDB. It says 31 SQL Server instances.

Someone from the database team: "That can't be right. I manage at least 50."

Infrastructure manager: "What about the test environment servers?"

Application team: "Are we counting Azure or just on-premises?"

Nobody actually knows. Your CMDB—the single source of truth—is wrong. And everyone in the room knows it.

So someone (usually you) gets tasked with "figuring it out." Which means the three-month archaeology project:
- Export RVtools from 3 vCenters
- Export ManageEngine data for physical servers
- Export ServiceNow CMDB records
- Dump everything into Excel
- Manually correlate data across systems
- Email people asking "is this yours?"
- Build a spreadsheet you barely trust

## What Cloud Migration Forces

When you start a cloud migration, you need answers:

- What applications are running?
- What servers support those applications?
- Who owns these servers?
- What's production vs. development vs. test?
- Which servers are physical vs. virtual?
- What AD domain are they in?

You can't migrate what you don't know exists. You can't plan capacity for applications you forgot about. You can't contact owners who left the company three years ago.

**So you run discovery.**

And discovery exposes years of accumulated tech debt. All the documentation nobody maintained. All the servers nobody remembers building. All the applications running on infrastructure nobody can explain.

## The Discovery That Changed Everything

We were planning a merger consolidation. 44 Azure subscriptions. 21 Active Directory domains. Leadership wanted a migration plan.

After three months of RVtools exports, ManageEngine queries, ServiceNow archaeology, and Excel cross-referencing, my spreadsheet showed roughly 8,000 resources.

Then I ran this Azure Resource Graph query:

```kql
Resources
| where type =~ 'microsoft.compute/virtualmachines'
   or type =~ 'microsoft.sql/servers'
   or type =~ 'microsoft.storage/storageaccounts'
   or type =~ 'microsoft.network/virtualnetworks'
| summarize count() by type
```

**Result:** 31,000 resources.

My three-month spreadsheet wasn't even close. Off by a factor of four.

But here's what mattered: **Azure Resource Graph was accurate.** 

More importantly: **The resources in Azure had TAGS.**

```kql
Resources
| where isnotempty(tags['Application']) 
  and isnotempty(tags['Owner'])
| project name, tags['Application'], tags['Owner']
```

For the first time in years, I could answer:
- What is this? (Application tag)
- Who owns it? (Owner tag)
- What does it do? (documented in tags)

No RVtools export. No ManageEngine query. No ServiceNow cross-reference. No manual correlation.

**One query. 30 seconds. Accurate.**

## Resource Graph Doesn't Fix On-Premises (And That's The Point)

**Critical clarification:** Azure Resource Graph only works for resources IN Azure. It doesn't help with your on-premises discovery.

**You still need the 3-month archaeology project** to inventory on-prem infrastructure before migration:
- RVtools exports from multiple VMware vCenters
- ManageEngine queries for physical servers and AD domain mapping
- ServiceNow CMDB archaeology
- Excel cross-referencing
- Email searches and meetings to find owners
- Manual correlation across systems that don't talk to each other

**Azure Resource Graph cannot see:**
- VMware VMs (until they're migrated to Azure)
- Physical servers (until they're migrated or Arc-enabled)
- On-premises infrastructure of any kind
- Anything not in Azure's control plane

**The payoff comes AFTER migration, not during discovery:**

**On-premises inventory:**
- 3 months of manual work
- Multiple tools that don't integrate
- Manual correlation required
- Immediately out of date
- Must repeat for every major initiative

**Azure inventory (post-migration):**
- 30-second queries
- Single source of truth
- Automatically maintained
- Always current
- Never requires manual archaeology again

**You're not avoiding the discovery pain.** The 3-month project still happens. But it's the LAST TIME you have to do it.

**Going forward:**
- New resources created in Azure → Automatically tracked with enforced tags
- Changes to existing resources → Automatically updated in Resource Graph
- Resources decommissioned → Automatically removed from queries
- No manual CMDB maintenance required
- No RVtools exports needed
- No cross-referencing between systems

**The investment is front-loaded:** Spend 3 months getting accurate on-prem inventory for migration planning, properly tag everything during migration, then never do manual inventory work again.

That's why cloud migration fixes the CMDB problem. Not by avoiding the discovery work, but by ensuring you never have to repeat it.

## Azure Resource Graph: The CMDB That Works

Azure Resource Graph is fundamentally different because it doesn't rely on people maintaining documentation:

**Traditional CMDB (ServiceNow/etc.):**
- Someone creates a VM
- Someone (hopefully) updates CMDB
- Someone changes the VM
- Someone (probably) forgets to update CMDB
- Owner leaves the company
- CMDB still shows terminated employee as owner
- VM gets decommissioned
- CMDB contains ghost asset forever

**Azure Resource Graph:**
- Someone creates a VM → Resource Graph knows immediately
- Someone tags it with Application/Owner → Tags are part of the resource
- Someone changes the VM → Resource Graph updates automatically
- Someone decommissions the VM → Resource Graph removes it
- Someone queries Resource Graph → Gets current state with tags, always

**The difference:** Tags are part of the Azure resource itself. Not a separate documentation system trying to track things. The metadata lives with the resource.

When you enforce tagging at creation (via Azure Policy), every new resource gets documented properly from day one. No manual CMDB updates. No hoping people remember to document things.

## The Queries That Actually Work

Here's what you can answer with Azure Resource Graph that took me 3 months to answer on-premises:

**What do we own?**

```kql
Resources
| project name, type, resourceGroup, subscriptionId, 
  tags['Application'], tags['Owner']
| order by name asc
```

Accurate. Real-time. Cross-subscription. With context about what things ARE and who owns them.

**Which SQL Servers don't have backups configured?**

```kql
Resources
| where type =~ 'microsoft.sql/servers/databases'
| extend backupRetention = properties.retentionDays
| where backupRetention == 0 or isnull(backupRetention)
| project name, resourceGroup, subscriptionId
```

Your CMDB can't answer this. Even if it listed SQL Servers, it doesn't track configurations.

**What resources are missing required tags?**

```kql
Resources
| where isnull(tags['Application']) or isnull(tags['Owner'])
| project name, type, resourceGroup, subscriptionId
| summarize count() by type
```

This is how you enforce governance. Find resources created without proper documentation BEFORE they become mystery servers nobody understands.

**Who actually owns this?**

```kql
Resources
| where name contains 'AZRPRDVM001'
| project name, tags['Owner'], tags['Application']
```

Instant answer. No "John Smith (terminated 2021)." Actual current owner because tagging was enforced at creation.

**What's the full inventory across 44 subscriptions?**

```kql
Resources
| summarize count() by type, subscriptionId
| order by count_ desc
```

Try doing this on-premises. You'd need RVtools exports from 3 vCenters, ManageEngine exports, ServiceNow exports, and 3 months of manual correlation.

With Resource Graph: One query. 30 seconds. Always accurate.

## Why Leadership Suddenly Cares About Inventory

Once we had accurate Resource Graph data, leadership could ask questions they couldn't before:

**"How many servers are we actually running?"**  
Answer: 2,847 VMs across all subscriptions (my spreadsheet said 1,200)

**"What's our Azure spend per application?"**  
Answer: Here's the breakdown by Application tag

**"Which resources don't have proper cost allocation tags?"**  
Answer: 8,400 resources missing tags, here's the list

**"What's our Windows Server 2012 exposure for security patching?"**  
Answer: 193 instances, here's where they are (my spreadsheet showed 47)

**"Who owns the Finance CRM infrastructure?"**  
Answer: Sarah Johnson, here are her 47 tagged resources

For the first time, leadership had confidence in IT's answers. Not because I suddenly became better at documentation—because the system enforced documentation automatically.

No more three-month discovery projects. No more "let me check three different systems and get back to you." No more "the person who knew this left two years ago."

## The Security Benefit Nobody Talks About

An accurate inventory is a security control.

**You can't protect what you don't know exists.**

On-premises: "Are all our SQL Servers behind firewalls?"  
Let me check RVtools... and ManageEngine... and ServiceNow... and hope I found them all. I probably missed some.

Azure: "Are all our SQL Servers behind private endpoints?"

```kql
Resources
| where type =~ 'microsoft.sql/servers'
| extend privateEndpoint = properties.privateEndpointConnections
| where isnull(privateEndpoint) or array_length(privateEndpoint) == 0
| project name, resourceGroup, subscriptionId, tags['Owner']
```

Instant answer. Complete list. With owners to contact about fixing the gaps.

If your on-premises CMDB is missing 146 SQL Server instances (like mine was), your security team has no idea those servers exist, let alone whether they're properly secured.

Cloud migration forced us to fix this. Now security can run queries themselves and get real answers.

## The Cost Management Breakthrough

Accurate inventory enables accurate cost allocation.

On-premises: "How much does the Finance CRM application cost?"  
Well, let me find all the servers... check RVtools... verify with ServiceNow... figure out which ones are actually Finance... estimate costs... maybe get it right...

Azure: "How much does the Finance CRM application cost?"

```kql
Resources
| where tags['Application'] == 'Finance CRM'
| join kind=inner (
    ResourceContainers
    | where type =~ 'microsoft.resources/subscriptions'
    | project subscriptionId, subscriptionName = name
) on subscriptionId
| summarize ResourceCount = count() by subscriptionName
```

Then correlate with Azure Cost Management filtering by Application tag. Accurate costs. Real-time. No guessing.

## The Business Case Nobody Makes

When leadership asks "Why should we migrate to Azure?" everyone focuses on scalability, uptime, and innovation.

Nobody mentions: **"You'll finally have an accurate inventory."**

But that's one of the most valuable outcomes. Not the primary reason to migrate, but a massive operational benefit that solves a problem every enterprise has:

**You don't know what you own. And it's costing you months of manual work to find out.**

After cloud migration, you do know. And it stays accurate automatically because:
- Tags are enforced at resource creation (Azure Policy)
- Metadata lives with the resource, not in a separate CMDB
- Changes update automatically
- Decommissioned resources disappear from queries
- No manual documentation updates required

The three-month discovery projects end. The "let me get back to you" conversations stop. The spreadsheet archaeology becomes a query that runs in 30 seconds.

That's worth something. Probably more than anyone realizes.

## How to Actually Use This

If you're managing Azure resources, stop trying to maintain a separate CMDB. Use Azure Resource Graph as your inventory system:

**For discovery:**
```kql
Resources
| project name, type, resourceGroup, subscriptionId, 
  location, tags
| order by name asc
```

**For finding undocumented resources:**
```kql
Resources
| where isnull(tags['Application']) 
   or isnull(tags['Owner'])
   or isnull(tags['CostCenter'])
| project name, type, resourceGroup, subscriptionId
| summarize count() by type
```

**For security compliance:**
```kql
Resources
| where type =~ 'microsoft.compute/virtualmachines'
| extend osVersion = properties.storageProfile.imageReference.sku
| where osVersion contains '2012' or osVersion contains '2008'
| project name, resourceGroup, tags['Owner'], osVersion
```

**For cost allocation:**
```kql
Resources
| where isnotempty(tags['Application'])
| extend app = tostring(tags['Application'])
| summarize count() by app
| order by count_ desc
```

These queries answer questions that took me 3 months to answer on-premises. In 30 seconds. With accurate data. Every time.

## The Uncomfortable Truth

Your CMDB is wrong. It's been wrong for years. Everyone knows it's wrong.

The only reason it hasn't caused a bigger problem is that nobody's needed accurate inventory data badly enough to force a fix.

Until you need to do a merger consolidation. Or a migration. Or answer executive questions about infrastructure that actually require accurate numbers.

Then someone (probably you) gets three months of archaeology work:
- RVtools exports showing VMs with no context
- ManageEngine queries for physical servers and AD domains
- ServiceNow CMDB reports showing terminated employees as owners
- Excel cross-referencing trying to connect systems that don't talk
- Email archaeology searching for mentions of mystery servers
- Meetings asking "is this yours?" over and over

Cloud migration forces that fix. Not because of some architectural requirement, but because you literally cannot plan a migration without knowing what you're migrating.

So you discover what you actually own. You TAG it properly during migration. And then you realize: Azure Resource Graph maintains that inventory automatically going forward.

The CMDB problem you've had for a decade? Cloud migration solves it as a side effect.

That's not why you migrate to Azure. But it's one of the best reasons to stay there.

---

**Want the full KQL queries for resource inventory and compliance checks?** They're built into Azure Resource Graph Explorer. Start with the sample queries and adapt them to your tagging strategy.

This is how you answer "what do we own?" in 30 seconds instead of 3 months.

And this is why proper tagging during cloud migration matters more than anyone realizes.
