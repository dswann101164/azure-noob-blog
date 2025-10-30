---
title: "Azure Icons Reference - All 284 Icons Searchable"
date: 2025-10-29
summary: "Complete searchable reference of all Azure service icons with descriptions. Stop hunting through Microsoft's icon sets - everything in one interactive table."
tags: ["Azure", "Documentation", "Reference"]
cover: "/static/images/hero/azure-icons-reference.png"
---

# Azure Icons Reference - All 284 Icons Searchable

**The Problem:** You're building architecture diagrams, documentation, or presentations and need the right Azure icon. You know Microsoft publishes them somewhere. You spend 20 minutes clicking through GitHub repos, icon collections, and outdated documentation trying to find "that Storage Account icon" or "whatever that Kubernetes thing is called."

**The Solution:** All 284 Azure service icons in one searchable interactive table. See the icon, service name, and description. Filter, search, export. Done.

## What You Get

**[Interactive Table Reference](/static/azure-icons-table.html)** ← Open this now

- 284 Azure service icons with visual thumbnails
- Real-time search filtering
- Download filtered results to Excel or CSV
- Clean table format (Service Name | Description | Icon URL)
- Works offline after first load

**[Excel Spreadsheet Download](/static/files/Azure-Icons-Reference.xlsx)**

- Same 284 icons with direct SVG URLs
- Searchable by service name or description
- Enable filters, sort, analyze

## The Interactive Table

The HTML table shows all 284 icons in a clean format - just like Microsoft docs pages. Search instantly, see icon thumbnails, export your filtered results.

**[See it live →](/static/azure-icons-table.html)**

Press `Ctrl+K` to jump to search from anywhere.

## Why This Exists

I was documenting a migration architecture. Needed icons. Found [Ben Coleman's excellent Azure icon collection](https://code.benco.io/icon-collection/azure-icons/) - it's the de facto standard. But I wanted searchable metadata with visual thumbnails, not just a grid.

Built what I needed: scraped the collection, added service names and descriptions based on actual Azure service definitions, packaged it as both interactive HTML and Excel.

You're welcome to use it.

## Quick Icon Reference Table

Here's a sample of commonly-used services. Full list is in the interactive table.

| Icon | Service Name | Description |
|------|-------------|-------------|
| ![Virtual Machines](https://code.benco.io/icon-collection/azure-icons/Virtual-Machine.svg) | Virtual Machines | On-demand scalable computing resources with choice of OS |
| ![Storage Accounts](https://code.benco.io/icon-collection/azure-icons/Storage-Accounts.svg) | Storage Accounts | Cloud storage for objects, files, disks, queues, and tables |
| ![Azure Active Directory](https://code.benco.io/icon-collection/azure-icons/Azure-Active-Directory.svg) | Azure Active Directory | Cloud-based identity and access management service |
| ![Virtual Networks](https://code.benco.io/icon-collection/azure-icons/Virtual-Networks.svg) | Virtual Networks | Isolated private network in Azure for resource communication |
| ![Key Vaults](https://code.benco.io/icon-collection/azure-icons/Key-Vaults.svg) | Azure Key Vault | Secure storage for secrets, keys, and certificates with HSM support |
| ![App Services](https://code.benco.io/icon-collection/azure-icons/App-Services.svg) | App Services | HTTP-based platform for hosting web applications and REST APIs |
| ![Azure SQL Database](https://code.benco.io/icon-collection/azure-icons/SQL-Database.svg) | Azure SQL Database | Fully managed PaaS database engine with AI-powered features |
| ![Azure Kubernetes Service](https://code.benco.io/icon-collection/azure-icons/Kubernetes-Services.svg) | Azure Kubernetes Service | Managed Kubernetes container orchestration service |
| ![Azure Functions](https://code.benco.io/icon-collection/azure-icons/Function-Apps.svg) | Azure Functions | Serverless compute service for event-driven code |
| ![Azure Cosmos DB](https://code.benco.io/icon-collection/azure-icons/Azure-Cosmos-DB.svg) | Azure Cosmos DB | Globally distributed multi-model NoSQL database |
| ![Application Gateway](https://code.benco.io/icon-collection/azure-icons/Application-Gateways.svg) | Application Gateway | Layer 7 load balancer with WAF and SSL termination |
| ![Azure Firewall](https://code.benco.io/icon-collection/azure-icons/Firewalls.svg) | Azure Firewall | Managed cloud-based network security service |
| ![Load Balancers](https://code.benco.io/icon-collection/azure-icons/Load-Balancers.svg) | Azure Load Balancer | Layer 4 load balancer distributing traffic across VMs |
| ![Azure Monitor](https://code.benco.io/icon-collection/azure-icons/Monitor.svg) | Azure Monitor | Comprehensive monitoring solution for telemetry and analytics |
| ![Log Analytics](https://code.benco.io/icon-collection/azure-icons/Log-Analytics-Workspaces.svg) | Log Analytics Workspace | Centralized repository for log data and KQL queries |
| ![Application Insights](https://code.benco.io/icon-collection/azure-icons/Application-Insights.svg) | Application Insights | Application Performance Management (APM) service |
| ![Azure DevOps](https://code.benco.io/icon-collection/azure-icons/Azure-DevOps.svg) | Azure DevOps | Suite of development tools for CI/CD and project management |
| ![Recovery Services Vault](https://code.benco.io/icon-collection/azure-icons/Recovery-Services-Vaults.svg) | Recovery Services Vault | Backup and disaster recovery container |
| ![Azure Policy](https://code.benco.io/icon-collection/azure-icons/Policy.svg) | Azure Policy | Governance service for enforcing standards and compliance |
| ![Cost Management](https://code.benco.io/icon-collection/azure-icons/Cost-Management.svg) | Cost Management | FinOps platform for monitoring and optimizing cloud spending |

## How to Use It

### Option 1: Interactive Table (Fastest)

1. **Open the table**: [azure-icons-table.html](/static/azure-icons-table.html)
2. **Search**: Type "storage" or "key vault" or "network"
3. **Browse**: Scroll through all icons visually
4. **Export**: Click "Download Excel" or "Download CSV"

### Option 2: Excel Spreadsheet

1. **Download** the spreadsheet
2. **Filter** by any column (Service Name, Description, or Icon URL)
3. **Copy** the Icon URL for use in diagrams or documentation
4. **Search** using Excel's Ctrl+F

### Use Cases

**Architecture Diagrams**
- Visio: Insert → Pictures → From File → paste icon URL
- PowerPoint: Same - SVG scales perfectly
- Draw.io: Arrange → Insert → Image → paste URL

**Documentation**
- Markdown: `![Service Name](icon-url)`
- Confluence: Insert image from URL
- Internal wikis: Direct SVG links work everywhere

**Presentations**
- Copy/paste directly from URL
- SVG format = no pixelation at any size
- Consistent Microsoft branding

## Full Icon Categories Included

The reference covers every Azure service category:

- **Compute:** VMs, App Service, Functions, AKS, Batch
- **Storage:** Blob, Files, Disks, Data Lake, NetApp Files
- **Networking:** VNets, Load Balancers, Firewalls, ExpressRoute, Front Door
- **Databases:** SQL, Cosmos DB, PostgreSQL, MySQL, MariaDB
- **Identity:** Azure AD, B2C, Conditional Access, Roles
- **Security:** Key Vault, Sentinel, Security Center, DDoS Protection
- **Monitoring:** Monitor, Log Analytics, Application Insights, Workbooks
- **DevOps:** Azure DevOps, Pipelines, Repos, Artifacts
- **Integration:** Logic Apps, Service Bus, Event Grid, API Management
- **AI/ML:** Cognitive Services, Machine Learning, Bot Service
- **IoT:** IoT Hub, IoT Central, Digital Twins, Sphere
- **Hybrid:** Azure Arc, Stack, Stack Edge
- **Management:** Policy, Blueprints, Cost Management, Resource Groups
- **And 10+ more categories...**

## Icon Source Attribution

Icons sourced from [Ben Coleman's Azure Icon Collection](https://code.benco.io/icon-collection/azure-icons/) - the definitive open-source collection of official Microsoft Azure icons. Ben maintains these icons and keeps them updated with new Azure services.

If you need the raw icon files (not just URLs), visit his GitHub repo: [github.com/benc-uk/icon-collection](https://github.com/benc-uk/icon-collection)

## Icon Naming Conventions

Microsoft's icon naming is... inconsistent. Some observations from cataloging 284 icons:

**Classic vs. Modern**
- Services with "(Classic)" suffix are legacy (avoid in new designs)
- Example: "Virtual-Machines-(Classic).svg" vs "Virtual-Machine.svg"

**Service Renames**
- Azure Security Center → Microsoft Defender for Cloud (icon still says Security-Center)
- Windows Virtual Desktop → Azure Virtual Desktop (icon says Windows-Virtual-Desktop)
- SQL Data Warehouse → Azure Synapse Dedicated SQL Pool

**Missing Icons**
- Some preview services don't have official icons yet
- Very new services lag by 2-3 months
- Ben's collection is updated regularly but isn't instant

**File Naming vs Display Name**
- File: "Azure-Database-PostgreSQL-Server.svg"
- Service: "Azure Database for PostgreSQL"
- Be ready for slight variations

## Useful Icon Patterns

**Identifying Resource Types**

Most icons follow visual patterns:

- **Cylinders** = Databases (SQL, Cosmos DB, MySQL)
- **Cubes** = Compute (VMs, App Service, Functions)
- **Shields** = Security (Firewall, Key Vault, Sentinel)
- **Gears** = Management (Automation, Policy, Monitor)
- **Networks** = Networking (obvious)

**Colors**
- Blue = Core Azure services
- Green = Monitoring/healthy states
- Red/Orange = Alerts/security
- Purple = Data/analytics

## When Icon Names Don't Match Portal

You'll notice some icons have names that don't perfectly match what you see in the Azure Portal. Examples:

- **"App-Services"** → Shows as "App Service" in portal (no plural)
- **"Azure-AD-B2C"** → Official name is "Azure Active Directory B2C"
- **"HDInsight-Clusters"** → Portal calls it "Azure HDInsight"

Use the **Description** column to find the right icon. I wrote descriptions based on actual portal names and service definitions.

## Interactive Table Features

**What makes the HTML table great:**

1. **Visual Scanning**
   - See 20-30 icons at once
   - Quick visual identification
   - Familiar table format

2. **Fast Search**
   - Type-ahead filtering
   - Searches name AND description
   - Results update instantly

3. **One-Click Export**
   - Download Excel (.xls format)
   - Download CSV (.csv format)
   - Exports your current filtered view

4. **Professional Look**
   - Clean Microsoft-style design
   - Responsive (works on mobile)
   - Sticky header while scrolling

## Real-World Usage

**Where I Actually Use This**

1. **Migration Documentation**
   - Architecture diagrams for 44-subscription consolidation
   - Before/after infrastructure comparisons
   - Executive presentations with consistent branding

2. **Runbook Templates**
   - Standard operating procedures with service icons
   - Quick visual identification of resource types
   - Internal wiki documentation

3. **Cost Reporting**
   - FinOps dashboards showing service spending
   - Icons help business users recognize services
   - Better than text-only cost breakdowns

4. **Incident Response**
   - Visual service maps during outages
   - Quickly identify affected components
   - Clear stakeholder communication

## Download

**[Interactive Table Reference](/static/azure-icons-table.html)** ← Best option  
**[Excel Spreadsheet](/static/files/Azure-Icons-Reference.xlsx)** ← For data analysis

284 icons. Fully searchable. Direct URLs. No hunting through Microsoft docs.

## Credits

- **Icons:** [Ben Coleman's Azure Icon Collection](https://code.benco.io/icon-collection/azure-icons/)
- **Descriptions:** Written from Azure documentation and real-world usage
- **Table Format:** Custom HTML/JavaScript
- **Excel Generation:** Python openpyxl
- **Maintenance:** Ben Coleman updates the source icons regularly

If this saves you time, thank Ben. His collection is the foundation that makes this possible.

---

**Related Posts You Might Like:**
- [Azure Periodic Table Service Dictionary](/blog/azure-periodic-table-service-dictionary)
- [KQL Cheat Sheet](/blog/kql-cheat-sheet)
- [Azure Workbooks - Modernization Guide](/blog/azure-workbooks-modernization)
