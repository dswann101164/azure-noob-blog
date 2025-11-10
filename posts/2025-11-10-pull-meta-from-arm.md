---
title: "I'll Pull The Meta From ARM - What 6 Months of KQL Actually Looks Like"
date: 2025-11-10
summary: "I promised executives I'd query Azure Resource Manager for 'the answers.' They nodded. I got budget. Nobody asked what metadata actually exists in ARM. Here's the 35-line query I built to answer 'what VMs do we have' - and the 35 more I needed for everything else."
tags: ["Azure", "KQL", "Resource Graph", "FinOps", "Operations"]
cover: "/static/images/hero/pull-meta-from-arm.svg"
---

## The Meeting Where I Promised Magic

Last week I wrote about [corporate arrogance killing cloud projects](https://azure-noob.com/blog/buzzwords-meetings-confusion/). Today, I'm showing you the exact technical gap that caused one of those failures.

Here's what I said in that executive meeting:

> "I'll use KQL to pull the meta from the ARM and get the answers."

Everyone nodded. Leadership approved it. The project got budget. Meeting adjourned.

Here's what nobody asked:
- What metadata specifically?
- What format?
- What's included vs. what needs to be built?
- How long will this take?

Here's what I actually meant:
"I'll write some Azure Resource Graph queries for... something."

Here's what they heard:
"Quick report with all the answers coming soon."

Here's what I actually built:
Six months of KQL query development, three separate joins per resource type, custom tag normalization logic, and 36+ production queries to answer what should have been a simple question.

Welcome to the gap between "pull the meta from ARM" and production reality.

---

## What Executives See

When leadership looks at Azure, they see this:

![Azure Portal Resource List](/static/images/azure-portal-resources.png)

A clean list of resources. Names, types, locations. Simple.

They think: "The data's right there. How hard can a report be?"

---

## What "The Meta" Actually Looks Like

Here's the naive approach everyone imagines:

```kql
resources
| where type == 'microsoft.compute/virtualmachines'
```

Done, right?

**Wrong.**

Here's what that query actually returns:

```json
{
  "id": "/subscriptions/xxx/resourceGroups/prod/providers/Microsoft.Compute/virtualMachines/vm001",
  "name": "vm001",
  "type": "microsoft.compute/virtualmachines",
  "location": "eastus",
  "properties": {
    "hardwareProfile": {
      "vmSize": "Standard_D4s_v3"
    },
    "storageProfile": {
      "osDisk": {
        "osType": "Windows"
      },
      "imageReference": {
        "publisher": "MicrosoftWindowsServer",
        "offer": "WindowsServer",
        "sku": "2022-datacenter-azure-edition",
        "exactVersion": "20348.2227.231214"
      }
    },
    "networkProfile": {
      "networkInterfaces": [
        {
          "id": "/subscriptions/xxx/resourceGroups/prod/providers/Microsoft.Network/networkInterfaces/vm001-nic"
        }
      ]
    },
    "extended": {
      "instanceView": {
        "powerState": {
          "code": "PowerState/running"
        }
      }
    }
  },
  "tags": {
    "Application": "WebServer",
    "Owner": "TeamA"
  }
}
```

**What executives want:**
| Name | Size | OS | IP Address | Owner | Environment | Status |
|------|------|----|-----------:|------:|------------:|-------:|
| vm001 | D4s_v3 | Windows Server 2022 | 10.0.1.5 | TeamA | Production | Running |

**What ARM gives you:**
Nested JSON requiring extraction, joins, and conditional logic.

---

## The Real Query: 35 Lines to Get VM Inventory

Here's what "pulling the meta from ARM" actually looks like:

```kql
resources
| where type =~ 'microsoft.compute/virtualmachines'
| extend vmSize = tostring(properties.hardwareProfile.vmSize)
| extend osType = tostring(properties.storageProfile.osDisk.osType)
| extend powerState = tostring(properties.extended.instanceView.powerState.code)
| extend createdTime = tostring(properties.timeCreated)
| extend nicId = tostring(properties.networkProfile.networkInterfaces[0].id)
// Extract OS version information
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
// Extract specific tags (handles case variations)
| extend Application = coalesce(tags.Application, tags.application, tags.APPLICATION, 'Not Tagged')
| extend Owner = coalesce(tags.Owner, tags.owner, tags.OWNER, 'Not Tagged')
| extend Type = coalesce(tags.Type, tags.type, tags.TYPE, 'Not Tagged')
| extend Environment = coalesce(tags.Environment, tags.environment, tags.ENVIRONMENT, 'Not Tagged')
| project 
    id, 
    name, 
    subscriptionId, 
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

Let's break down what each section actually does.

---

## Breaking Down The Query

### Lines 1-7: Extract Nested Properties

```kql
| extend vmSize = tostring(properties.hardwareProfile.vmSize)
| extend osType = tostring(properties.storageProfile.osDisk.osType)
| extend powerState = tostring(properties.extended.instanceView.powerState.code)
```

**What executives think:** "The data's right there"

**Reality:** Every property is nested 3-4 levels deep in JSON. You need to know the exact path. One typo, you get nulls. No autocomplete. No schema documentation that matches production.

**Time investment:** 2 days figuring out where properties actually live vs. where Microsoft docs say they should be.

---

### Lines 8-12: Concatenate OS Version

```kql
| extend osVersion = tostring(properties.storageProfile.imageReference.exactVersion)
| extend osSku = tostring(properties.storageProfile.imageReference.sku)
| extend osOffer = tostring(properties.storageProfile.imageReference.offer)
| extend osPublisher = tostring(properties.storageProfile.imageReference.publisher)
| extend osVersionDisplay = strcat(osPublisher, ' ', osOffer, ' ', osSku)
```

**What executives want:** "Windows Server 2022"

**Reality:** OS version is split across 4 separate properties that need manual concatenation. And that's just for Marketplace images - custom images require completely different logic.

**Time investment:** 1 day handling all the edge cases (custom images, legacy formats, missing data).

---

### Lines 13-18: Join to Get IP Addresses

```kql
| join kind=leftouter (
    resources
    | where type =~ 'microsoft.network/networkinterfaces'
    | extend privateIp = tostring(properties.ipConfigurations[0].properties.privateIPAddress)
    | project nicId = id, privateIp
) on $left.nicId == $right.nicId
```

**What executives think:** "VMs have IP addresses"

**Reality:** IP addresses belong to Network Interface Cards (NICs), which are separate resources. VMs only store a reference ID to the NIC. You need a left outer join to another Resource Graph query. And this assumes one NIC per VM - multi-NIC VMs require array handling.

**Time investment:** 3 days mastering KQL joins, understanding NIC relationships, handling VMs with multiple NICs.

---

### Lines 19-23: Translate Subscription GUIDs

```kql
| join kind=leftouter (
    resourcecontainers
    | where type == 'microsoft.resources/subscriptions'
    | project subscriptionId, subscriptionName = name
) on subscriptionId
```

**What executives see:** Subscription names in the portal

**Reality:** ARM returns subscription GUIDs. Human-readable names require joining to `resourcecontainers` table. Another join. Another opportunity for performance issues at scale.

**Time investment:** 1 day learning about resourcecontainers vs resources tables.

---

### Lines 24-29: Handle Tag Chaos

```kql
| extend Application = coalesce(tags.Application, tags.application, tags.APPLICATION, 'Not Tagged')
| extend Owner = coalesce(tags.Owner, tags.owner, tags.OWNER, 'Not Tagged')
| extend Type = coalesce(tags.Type, tags.type, tags.TYPE, 'Not Tagged')
| extend Environment = coalesce(tags.Environment, tags.environment, tags.ENVIRONMENT, 'Not Tagged')
```

**What the tagging policy says:** `Application` tag required on all resources

**Reality in production:**
- Some resources: `Application`
- Other resources: `application` 
- Legacy resources: `APPLICATION`
- Half the resources: No tag at all

**Why this happens:**
- Portal is case-insensitive (hides the problem)
- ARM API is case-sensitive (causes the problem)
- Terraform defaults to lowercase
- PowerShell scripts use TitleCase
- Consultants used UPPERCASE
- Nobody noticed until you tried to query

**This one line represents:**
- Organizational tag standards that don't exist
- Years of inconsistent deployments
- No tag governance until recently
- 40% of resources still untagged
- Manual cleanup campaigns that never finish

**Time investment:** Ongoing. Forever. This is your life now.

---

## The Multiplication Problem

**Here's what breaks executives:**

This 35-line query? It's for **ONE resource type**.

To answer "What's in our Azure environment?" you need queries for:

1. **Virtual Machines** (35 lines)
2. **AKS Clusters** (40 lines - even more complex joins)
3. **Storage Accounts** (30 lines)
4. **Virtual Networks** (25 lines)
5. **Network Security Groups** (45 lines - need to expand rule arrays)
6. **SQL Databases** (35 lines)
7. **App Services** (30 lines)
8. **Key Vaults** (25 lines)
9. **Log Analytics Workspaces** (30 lines)
10. **Public IP Addresses** (20 lines)
11. **Load Balancers** (40 lines)
12. **Application Gateways** (45 lines)

**Each with:**
- Its own nested property structure
- Its own join requirements
- Its own missing data handling
- Its own edge cases

**Total investment:** 36+ production queries, 6 months of development, nights and weekends debugging edge cases.

---

## What's STILL Missing

Even with all these queries, you still don't have:

### ❌ Cost Data

Cost isn't in Resource Graph. It's in the Cost Management API. Separate authentication. Different query language. Different time delays (24-48 hours lag).

To get cost per resource:
1. Query Resource Graph for resources
2. Query Cost Management API for costs
3. Join the results in your application layer
4. Handle resources that exist but have no cost data yet
5. Handle costs for resources that were deleted
6. Handle Azure reservations that don't map to specific resources
7. Handle subscription-level services that can't be allocated

**Additional time:** 2 weeks building the cost allocation pipeline.

### ❌ Compliance Status

Azure Policy compliance isn't in Resource Graph. It's in the Policy API. Another separate call.

To get compliance per resource:
1. Query Resource Graph for resources
2. Query Policy API for compliance state
3. Query Policy API again for policy definitions
4. Join everything together
5. Handle policies that apply at management group level
6. Handle inheritance and exemptions
7. Translate policy definition IDs to human-readable names

**Additional time:** 1 week building compliance reporting.

### ❌ Relationships and Dependencies

ARM doesn't tell you:
- Which VMs depend on which NSGs
- Which App Services use which Key Vaults
- Which applications span which resource groups
- Which resources are related to the same business application

You have to infer this from:
- Naming conventions (if they exist)
- Tags (if they're consistent)
- Manual documentation (if it exists)
- Tribal knowledge (good luck)

**Additional time:** Ongoing manual documentation.

### ❌ Business Context

ARM definitely doesn't tell you:
- Which business owner is responsible
- Which budget this should charge to
- What the disaster recovery requirements are
- What the change control process is
- Whether this is even still needed

This requires:
- CMDB integration (if you have one)
- ServiceNow tickets (if they're up to date)
- Interviews with business owners (if you can find them)
- Archaeological digs through old emails

**Additional time:** Measured in years.

---

## The Reality Check

**What I said in the meeting:**
> "I'll use KQL to pull the meta from the ARM and get the answers."

**What I should have said:**
> "I can query Azure Resource Manager for basic resource properties. To answer your actual questions about cost allocation, compliance, and business ownership, I'll need to:
> - Build 36+ specialized KQL queries
> - Integrate with 3 separate Azure APIs
> - Implement tag governance across the organization
> - Create external documentation for business context
> - Budget 6 months for initial development plus ongoing maintenance
> 
> Would you like me to scope this properly, or should we start with a smaller proof-of-concept?"

**Why I didn't say that:**
Because admitting complexity sounds like I'm creating obstacles. Corporate culture rewards confident-sounding commitments, not honest assessments.

**The cost of that arrogance:**
- 6 months of weekend work
- Missed expectations about timeline
- Leadership frustrated about delays
- Me frustrated about unrealistic expectations
- Project technically successful but organizationally viewed as "took too long"

---

## The Complete KQL Toolkit

I've published all 36+ production queries to GitHub:

**[azure-inventory-workbook-enhanced](https://github.com/dswann101164/azure-inventory-workbook-enhanced/tree/main/powerbi%20starter/kql)**

**What's included:**

### Compute Resources:
- `01_Virtual_Machines_Details.kql` - Complete VM inventory with joins
- `02_VM_Status_Summary.kql` - Power state rollup
- `03_VM_by_SKU.kql` - Size analysis
- `09_AKS_Clusters_Details.kql` - Kubernetes cluster inventory
- `11_Azure_Arc_Servers_Details.kql` - Hybrid server inventory

### Networking:
- `19_Networking_Overview.kql` - Complete network topology
- `20_Virtual_Networks_Analysis.kql` - VNet configurations and peering
- `21_Load_Balancers_Details.kql` - Load balancer rules and backend pools

### Storage:
- `16_Storage_Overview.kql` - All storage resources
- `17_Storage_Accounts_Configuration.kql` - Detailed storage configs
- `18_Managed_Disks_Configuration.kql` - Disk inventory and orphaned disk detection

### PaaS Services:
- `13_App_Services_Details.kql` - App Service plans and apps
- `14_SQL_Servers_Details.kql` - SQL Server inventory
- `15_Database_Services_Details.kql` - All database types

### Governance & Cost:
- `29_Governance_Resources.kql` - Policies, locks, RBAC
- `31_Orphaned_Resources_Analysis.kql` - Unused resources costing money
- `32_Cost_Saving_Recommendations.kql` - Rightsizing opportunities

### Security:
- `27_Security_Recommendations_from_Advisor.kql` - Security hygiene
- `36_Security_Configuration_Issues.kql` - Common misconfigurations

**All queries include:**
- Handling for missing data
- Case-insensitive tag extraction
- Subscription name joins
- Comments explaining non-obvious logic
- Production-tested edge case handling

---

## Lessons Learned

After 6 months of building this, here's what I wish I'd known:

### 1. "Pull the meta" is not a 2-week project

**What executives hear:** "Quick data extraction"

**Reality:** 
- 2-3 months for initial query library
- 2-3 months for edge case handling
- Ongoing maintenance forever
- Scales with resource type diversity

Budget accordingly. Don't promise quick wins.

### 2. ARM is a resource API, not a reporting API

Azure Resource Manager's job:
- ✅ Create, read, update, delete resources
- ✅ Return raw resource properties
- ❌ Generate business reports
- ❌ Provide curated analytics
- ❌ Join data across services
- ❌ Interpret business context

If you promise "answers," you're building the reporting layer they thought already existed.

### 3. Tags solve problems you create later

**Early in cloud adoption:** "Tags are overhead, we'll add them later"

**18 months later:** "Why can't you tell me what this costs?"

The time to implement tag governance is before you have 31,000 resources. After that, you're doing archaeological cost allocation.

### 4. The joins are where beginners fail

Basic KQL is easy. What breaks people:
- Understanding which resources relate to which
- Knowing when you need leftouter vs inner joins
- Handling resources with 0, 1, or many relationships
- Performance optimization at scale

This isn't "pull the meta" - this is database query optimization.

### 5. Production data is never clean

Every query needs:
- Null handling for missing properties
- Case-insensitive tag matching
- Coalesce chains for schema variations
- Conditional logic for legacy formats
- Error handling for API changes

Budget 40% of development time for edge cases.

### 6. Documentation rots immediately

That VM query? Works great today. Tomorrow:
- Microsoft adds a new VM property
- Your org creates a new tag standard
- Someone deploys VMs in a new pattern
- ARM API changes schema slightly

Queries require maintenance. They're not "write once, run forever."

### 7. The real work is organizational, not technical

The hard part isn't writing KQL. It's:
- Getting agreement on tag taxonomy
- Enforcing tag governance
- Teaching teams to use tags correctly
- Documenting business context externally
- Maintaining data quality over time

Technology is easy. People are hard.

---

## What I'd Do Differently

If I could redo that meeting:

**Instead of:**
> "I'll use KQL to pull the meta from the ARM and get the answers."

**I'd say:**
> "Let me make sure I understand what you need. Can you show me an example of what success looks like?
>
> [They show me a spreadsheet]
>
> Okay, here's what's involved:
> - Resource data: 2 weeks to build base queries
> - IP addresses: Requires joins to network resources, 3 days
> - Cost allocation: Separate API, requires tag governance, 6 weeks
> - Business ownership: Not in Azure, needs external documentation, TBD
>
> I can have basic resource inventory in 2 weeks. Complete cost allocation with business context is a 4-month project.
>
> Which scope do you want me to start with?"

**Why this is better:**
- Forces them to articulate specific needs
- Sets realistic timeline expectations
- Breaks the work into phases
- Makes missing data explicit
- Gives them decision points

**Would they have liked this answer less?**
Yes.

**Would the project have gone better?**
Also yes.

---

## The Tools You Actually Need

Beyond the KQL queries, here's what you need for production Azure inventory:

### 1. Azure Resource Graph

**What it is:** Query interface for ARM resources

**What it's good for:**
- Resource configuration data
- Near real-time (5-minute delay max)
- 1,000 resources per query (pagination required)
- Fast performance even at scale

**What it's NOT:**
- Cost data
- Compliance status
- Application relationships
- Business context

### 2. Cost Management API

**What it is:** Separate API for cost and usage data

**What it's good for:**
- Actual costs per resource
- Usage patterns over time
- Reserved instance utilization
- Budget tracking

**What's painful:**
- 24-48 hour data lag
- Different authentication
- Different query language
- Separate rate limits

### 3. Azure Policy API

**What it is:** Compliance and governance state

**What it's good for:**
- Policy assignment status
- Compliance per resource
- Exemption tracking
- Remediation history

**What's annoying:**
- Yet another separate API
- Requires multiple calls to get full picture
- Policy definitions vs assignments vs compliance are separate queries

### 4. External Documentation

**What it is:** SharePoint/Confluence/OneNote/whatever you have

**What you'll track here:**
- Business owners
- Application relationships
- Disaster recovery requirements
- Change control processes
- Budget allocation
- Everything ARM doesn't know

**Why you need it:**
Because Azure doesn't know which VM belongs to which application, which team owns it, or whether anyone will care if you delete it.

### 5. Power BI or Similar

**What it is:** Visualization layer on top of all the queries

**Why you need it:**
- Executives want dashboards, not KQL results
- Needs to refresh automatically
- Requires scheduled data refresh
- Has its own authentication challenges

**Time investment:** Another 2-3 weeks building reports after the queries work.

---

## The GitHub Repository

Everything I've described is available in production-ready form:

**[azure-inventory-workbook-enhanced](https://github.com/dswann101164/azure-inventory-workbook-enhanced)**

**Repository structure:**
```
/powerbi starter/kql/
  ├── 01_Virtual_Machines_Details.kql
  ├── 02_VM_Status_Summary.kql
  ├── 09_AKS_Clusters_Details.kql
  ├── 16_Storage_Overview.kql
  ├── 19_Networking_Overview.kql
  ├── 31_Orphaned_Resources_Analysis.kql
  └── [30+ more production queries]
```

**Each query includes:**
- Full working code (copy-paste ready)
- Comments explaining complex logic
- Tag normalization handling
- Subscription name joins
- Null handling for missing data

**Based on:** Billy York's excellent [Azure Inventory Workbook](https://github.com/scautomation/Azure-Inventory-Workbook), enhanced for enterprise-scale environments where:
- Tag governance is aspirational
- Resources span 44 subscriptions
- Naming conventions are "suggestions"
- Legacy resources have zero documentation

**Clone it. Use it. Modify it for your environment.**

This is what "pulling the meta from ARM" actually looks like in production.

---

## The Bottom Line

**What executives think they're asking for:**
"Pull the data from Azure and make me a report"

**What you're actually building:**
- 36+ specialized queries
- Multi-API data integration
- Tag governance enforcement
- External documentation system
- Automated refresh pipeline
- Exception handling for every edge case
- Ongoing maintenance forever

**Timeline:**
- Executives expect: 2 weeks
- Reality: 6 months initial, ongoing maintenance

**The gap between these is where projects fail.**

---

## What's Next

In my next post, I'm tackling the other big promise that sounds simple but isn't:

**"Just use subscriptions for cost allocation"**

Spoiler: That only works if your subscriptions were architected as cost centers. If they're security boundaries (like mine), you need the resource-level tag taxonomy approach. Complete code, real examples, production-tested.

**Want this when I publish it?** [Subscribe here](https://azure-noob.com) or follow the [GitHub repo](https://github.com/dswann101164).

---

## Your Turn

What "simple" Azure request turned into a 6-month project in your environment?

What's the biggest gap between what executives think exists and what you actually had to build?

Drop a comment below - I'm collecting these for a follow-up on the most common "easy Azure tasks" that absolutely aren't.

---

**Related Posts:**
- [Buzzwords, Technical Terms, and the Meetings Where Nobody Understands Anything](https://azure-noob.com/blog/buzzwords-meetings-confusion/)
- [Azure Cost Allocation When Subscriptions Are Security Boundaries](https://azure-noob.com/blog/coming-soon/) (Coming soon)

---

*Written at 3:30 AM by someone who learned KQL the hard way so you don't have to.*
