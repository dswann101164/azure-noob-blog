---
title: "The Azure Role Microsoft Forgot to Certify: Why There's No Exam for Workbooks, KQL, Power BI, and AI"
date: 2025-12-07
summary: "Microsoft certifies Azure Administrators, Developers, and Data Engineers. But there's no certification for the role 80% of Azure admins actually perform: building Workbooks, writing KQL queries, creating Power BI dashboards, and leveraging AI for operations. Here's the exam that should exist."
tags: ["Azure", "Certification", "Career", "Workbooks", "KQL", "Power BI", "AI", "Azure Monitor", "FinOps"]
cover: "/static/images/hero/azure-reporting-role-gap.png"
hub: "monitoring"
related_posts:
  - kql-cheat-sheet-complete
  - modernizing-azure-workbooks
  - azure-dashboards-cloud-noc
  - chris-bowman-dashboard
---

# The Azure Role Microsoft Forgot to Certify: Why There's No Exam for Workbooks, KQL, Power BI, and AI

**I spend 60% of my time as an "Azure Administrator" doing work that no Azure certification teaches.**

Not infrastructure deployment. Not identity management. Not networking.

**Building reports. Writing queries. Creating dashboards. Answering business questions with data.**

Yet when I look at Microsoft's Azure certification paths, **this role doesn't exist.**

## The Azure Certification Path (What Exists Today)

Microsoft offers certifications for:

**Infrastructure & Operations:**
- **AZ-104:** Azure Administrator Associate
- **AZ-305:** Azure Solutions Architect Expert
- **AZ-500:** Azure Security Engineer Associate

**Development:**
- **AZ-204:** Azure Developer Associate
- **AZ-400:** DevOps Engineer Expert

**Data & AI:**
- **DP-900:** Azure Data Fundamentals
- **DP-203:** Azure Data Engineer Associate
- **AI-102:** Azure AI Engineer Associate
- **PL-300:** Power BI Data Analyst Associate

**The problem:** None of these certifications cover the role most Azure admins actually perform.

## The Role That Doesn't Have a Certification

**If you're an Azure Administrator in an enterprise, here's what you actually do:**

### Monday Morning: Finance Calls
> "Azure spend is up $47,000 this month. Explain why."

**Tools I use:**
- Azure Workbooks (not covered in any Azure cert)
- KQL queries joining cost data across 44 subscriptions (AZ-104 barely mentions KQL)
- Power BI dashboard showing cost by business unit (not mentioned in AZ-104)

**Which certification teaches this?**
- AZ-104? Teaches you how to set cost alerts. Doesn't teach you how to build cost reports.
- PL-300 (Power BI)? Teaches Power BI, but doesn't cover Azure-specific data sources like Resource Graph or Cost Management.
- DP-203 (Data Engineer)? Way too advanced. I don't need to build data pipelines. I need to query Azure data.

**Answer: None of them.**

### Tuesday: Security Compliance Report
> "SOC2 audit needs a report showing all resources without required tags."

**Tools I use:**
- Azure Resource Graph (mentioned in AZ-104, but not taught in depth)
- KQL query scanning 31,000 resources (no certification teaches KQL for Resource Graph)
- Azure Workbook displaying compliance status (no certification teaches Workbook design)

**Which certification teaches this?**
- AZ-104? Mentions Resource Graph exists. Doesn't teach you how to write queries.
- AZ-500 (Security)? Focuses on security configuration, not compliance reporting.
- DP-203 (Data Engineer)? Teaches data engineering, not operational queries.

**Answer: None of them.**

### Wednesday: Application Performance Dashboard
> "Build a dashboard showing which VMs we can safely shut down overnight to save costs."

**Tools I use:**
- Azure Monitor Logs (AZ-104 teaches basic alerts only)
- KQL queries analyzing 30 days of CPU/memory metrics (not taught)
- Azure Workbook with interactive filters (not taught)
- Azure Advisor recommendations integrated into Workbook (integration not taught)

**Which certification teaches this?**
- AZ-104? Teaches you how to configure Azure Monitor. Doesn't teach you how to analyze the data.
- AZ-305 (Architect)? Focuses on solution design, not operational reporting.

**Answer: None of them.**

### Thursday: Executive Dashboard
> "Leadership wants one dashboard showing everything wrong with our Azure environment."

**Tools I use:**
- Power BI connecting to multiple Azure data sources (not covered in any Azure cert)
- KQL queries from Resource Graph, Log Analytics, and Cost Management (not taught together)
- DAX measures for custom calculations (PL-300 teaches this, but not for Azure data)
- Azure AI to generate natural language insights (no cert teaches AI in operational workflows)

**Which certification teaches this?**
- AZ-104? Doesn't mention Power BI.
- PL-300 (Power BI)? Doesn't cover Azure-specific data sources or KQL.
- AI-102? Focuses on building AI solutions, not using AI for operations.

**Answer: None of them.**

### Friday: Vulnerability Remediation Report
> "Security scan found 285 VMs with high-severity vulnerabilities. Which patches fix which issues?"

**Tools I use:**
- Azure Resource Graph to query VM inventory (mentioned in AZ-104, not taught)
- KQL to join vulnerability scan results with Update Manager compliance (not taught)
- Azure Workbook showing patch status by application owner (not taught)
- Azure OpenAI to summarize findings for non-technical leadership (not taught anywhere)

**Which certification teaches this?**
- AZ-500 (Security)? Teaches security configuration, not vulnerability reporting.
- AZ-104? Mentions Update Manager. Doesn't teach data analysis.

**Answer: None of them.**

## The Pattern: Infrastructure Configuration ≠ Operational Reporting

**Every Azure certification focuses on:**
- How to **configure** Azure services
- How to **deploy** infrastructure
- How to **secure** environments
- How to **architect** solutions

**None of them focus on:**
- How to **query** Azure data at scale
- How to **build** operational dashboards
- How to **create** business reports
- How to **leverage AI** for operational insights

**Yet this is what Azure administrators spend most of their time doing.**

## The Certification That Should Exist

Microsoft should create: **AZ-XXX: Azure Operations and Analytics Associate**

**Target audience:**
- Azure Administrators who need to report on infrastructure
- Cloud FinOps practitioners building cost dashboards
- Cloud NOC teams creating operational Workbooks
- Security teams building compliance reports

**Prerequisites:**
- AZ-900 (Azure Fundamentals) OR
- 6+ months Azure administration experience

**Exam domains:**

### 1. Azure Workbooks (25%)
**Skills measured:**
- Design interactive dashboards for operations, cost, security
- Combine data from Azure Monitor, Resource Graph, Log Analytics
- Create Workbooks for specific audiences (NOC, FinOps, executives)
- Implement parameters and filters for user interaction
- Share and deploy Workbooks across environments

**Sample task:**
> Build an Azure Workbook showing all VMs without backup configured, grouped by subscription and application owner, with drill-down to VM details.

**Current certification coverage:** Zero

### 2. KQL for Azure Operations (30%)
**Skills measured:**
- Query Azure Resource Graph for inventory and compliance
- Query Azure Monitor Logs for performance analysis
- Join data across Resource Graph, Logs, and Cost Management
- Optimize queries for large-scale environments (10K+ resources)
- Build reusable query functions and parameters

**Sample task:**
> Write a KQL query that shows all storage accounts without lifecycle management policies, joins with cost data to show monthly spend, and filters to accounts costing more than $100/month.

**Current certification coverage:**
- AZ-104: One or two sample queries
- DP-203: Advanced KQL, but focused on data engineering not operations

### 3. Power BI Integration with Azure (25%)
**Skills measured:**
- Connect Power BI to Azure Resource Graph
- Import Azure Cost Management data
- Create measures with DAX for Azure-specific calculations
- Design executive dashboards for cost, compliance, performance
- Implement chargeback models with tags and cost allocation

**Sample task:**
> Build a Power BI dashboard showing Azure costs by business unit, with drill-down to subscription and resource group, including month-over-month variance and forecast.

**Current certification coverage:**
- PL-300: Power BI skills, but doesn't cover Azure data sources
- AZ-104: Power BI never mentioned

### 4. AI for Azure Operations (20%)
**Skills measured:**
- Use Copilot for Azure for optimization recommendations
- Leverage Azure Monitor's AI-powered anomaly detection
- Build automation scripts with Azure OpenAI
- Implement AI-driven cost forecasting
- Create natural language reports from Azure data

**Sample task:**
> Use Azure OpenAI to generate a KQL query that identifies underutilized VMs, then create a natural language summary of findings for non-technical stakeholders.

**Current certification coverage:**
- AI-102: Building AI solutions, not using AI for operations
- No Azure cert covers AI in administrative workflows

## Why Each Existing Certification Doesn't Cover This

Let me be specific about why existing certs fall short:

### AZ-104 (Azure Administrator Associate)

**What it covers well:**
- VM deployment and configuration ✅
- Virtual networking and NSGs ✅
- Azure AD and RBAC ✅
- Backup and disaster recovery ✅
- Basic Azure Monitor alerts ✅

**What it misses completely:**
- Azure Workbooks design and implementation ❌
- KQL query writing beyond basic examples ❌
- Power BI integration ❌
- AI tools for operations ❌
- Operational reporting at scale ❌

**Hands-on Workbook labs:** 0  
**KQL query challenges:** 0  
**Power BI integration:** Not mentioned  
**AI operations:** Not mentioned  

**Gap:** 80% of what I do daily as an "Azure Administrator"

### AZ-305 (Azure Solutions Architect Expert)

**What it covers well:**
- Solution design and architecture ✅
- Cost optimization strategies ✅
- Governance and compliance design ✅

**What it misses:**
- Actually building the cost reports ❌
- Actually writing the compliance queries ❌
- Operational dashboard implementation ❌

**Gap:** Focuses on design, not implementation of reporting

### AZ-500 (Azure Security Engineer Associate)

**What it covers well:**
- Security configuration ✅
- Microsoft Defender setup ✅
- Sentinel deployment ✅

**What it misses:**
- Building security compliance dashboards ❌
- KQL for security reporting ❌
- Executive security scorecards ❌

**Gap:** Configures security, doesn't report on it

### PL-300 (Power BI Data Analyst Associate)

**What it covers well:**
- Power BI dashboard design ✅
- DAX measures and calculations ✅
- Data modeling ✅

**What it misses:**
- Azure Resource Graph as a data source ❌
- Azure Cost Management integration ❌
- KQL for Azure Monitor data ❌
- Azure-specific use cases ❌

**Gap:** Generic Power BI, not Azure-specific

### DP-203 (Azure Data Engineer Associate)

**What it covers well:**
- Data pipeline design ✅
- Advanced KQL ✅
- Data Lake and Synapse ✅

**What it misses:**
- Way too advanced for operational queries ❌
- Focused on data engineering, not operations ❌

**Gap:** I don't need to build data pipelines. I need to query Azure data.

### AI-102 (Azure AI Engineer Associate)

**What it covers well:**
- Building AI solutions ✅
- Cognitive Services ✅
- Azure OpenAI deployment ✅

**What it misses:**
- Using AI for operational automation ❌
- AI in administrative workflows ❌
- Copilot for Azure ❌

**Gap:** Building AI solutions ≠ using AI as an admin

## The Exact Skills Missing from All Certifications

Here's what **no Azure certification** currently teaches:

### Azure Workbooks (100% Gap)

**Skills needed:**
- Workbook JSON structure and authoring
- Data source integration (Monitor, Resource Graph, Logs)
- Parameter design for user interaction
- Conditional formatting and visualizations
- Workbook sharing and deployment strategies

**Current coverage across ALL Azure certs:** Zero hands-on labs

**Real-world usage:** I've built 12 production Workbooks used daily by 50+ people

### KQL for Operations (90% Gap)

**Skills needed:**
- Resource Graph schema and relationships
- Join strategies across data sources
- Performance optimization for 10K+ resource queries
- Time-series analysis for metrics
- Building reusable query functions

**Current coverage:**
- AZ-104: Maybe 2 sample queries
- DP-203: Advanced KQL, but data engineering focus

**Real-world usage:** I write 10-20 KQL queries per week

### Power BI + Azure Integration (85% Gap)

**Skills needed:**
- Connecting to Resource Graph API
- Azure Cost Management connector
- KQL queries as Power BI data sources
- DAX for Azure-specific calculations (cost per tag, etc.)
- Refresh strategies for Azure data

**Current coverage:**
- PL-300: Generic Power BI
- AZ-104/305: Never mentioned

**Real-world usage:** Every Azure FinOps initiative requires Power BI

### AI in Operations (100% Gap)

**Skills needed:**
- Copilot for Azure usage patterns
- Azure OpenAI for automation scripts
- AI-powered anomaly detection in Monitor
- Natural language reporting from Azure data
- AI-driven cost forecasting

**Current coverage:** Zero across all Azure operational certs

**Real-world usage:** I use Azure OpenAI weekly for query generation and report writing

## Real-World Impact of This Gap

### For New Azure Admins

You pass AZ-104. You get hired. Day 1:

**Manager:** "Build a dashboard showing our Azure costs by application."

**You:** "AZ-104 didn't teach me Power BI, KQL, or how to query cost data."

**Manager:** "Figure it out."

**Result:** 3-6 months of trial and error learning tools the certification should have taught.

### For Employers

**Job posting:** "Azure Administrator - Must have AZ-104 and ability to build operational dashboards and cost reports."

**Reality:** AZ-104 teaches neither.

**Result:** Either hire someone overqualified (data engineer) or accept a learning curve.

### For Microsoft

Microsoft builds incredible reporting tools:
- Azure Workbooks
- Azure Resource Graph
- Azure Monitor
- Power BI
- Copilot for Azure
- Azure OpenAI

Microsoft certifies Azure professionals who don't know how to use them.

**This is a missed opportunity.**

## What Should Change

### Option 1: Expand AZ-104

Add these modules to Azure Administrator Associate:

**New Module 1: Operational Reporting**
- Azure Workbooks design (10% of exam)
- KQL for Resource Graph and Monitor (15% of exam)
- 3-5 hands-on Workbook labs

**New Module 2: Business Intelligence**
- Power BI basics for Azure data (5% of exam)
- Connecting to Cost Management and Resource Graph
- 1-2 hands-on dashboard labs

**Problem:** This makes AZ-104 too large

### Option 2: Create New Certification (Better)

**AZ-XXX: Azure Operations and Analytics Associate**

**Prerequisites:** AZ-900 or AZ-104

**Target:** Azure admins who build reports and dashboards

**Exam breakdown:**
- 25% Azure Workbooks
- 30% KQL for operations
- 25% Power BI integration
- 20% AI in operations

**Benefits:**
- Focuses on specific skill gap
- Doesn't bloat existing certs
- Creates career path for reporting-focused admins

### Option 3: Enhance Existing Certs

**PL-300 (Power BI):**
- Add Azure Resource Graph module
- Add Azure Cost Management connector
- Add Azure-specific dashboard examples

**AZ-104 (Azure Admin):**
- Double KQL coverage
- Add 2-3 Workbook labs
- Mention Power BI exists

**Problem:** Still fragmented across multiple certs

## Until Microsoft Fixes This

**If you're an Azure admin who needs these skills:**

### Learn Azure Workbooks
- **Start:** Azure Monitor Workbook gallery templates
- **Practice:** Clone existing Workbooks, modify them
- **Build:** One compliance dashboard (resources without tags)
- **Time:** 1-2 weeks to basic proficiency

**Resources:**
- [Modernizing Azure Workbooks](/blog/modernizing-azure-workbooks/)
- [Azure Dashboards for Cloud NOC](/blog/azure-dashboards-cloud-noc/)

### Learn KQL
- **Start:** Azure Resource Graph queries for inventory
- **Practice:** Write queries for common admin tasks
- **Build:** Query library for reusable patterns
- **Time:** 2-3 weeks to operational proficiency

**Resources:**
- [KQL Cheat Sheet](/blog/kql-cheat-sheet-complete/)
- [Azure VM Inventory with KQL](/blog/azure-vm-inventory-kql/)

### Learn Power BI + Azure
- **Start:** Connect Power BI to Azure Cost Management
- **Practice:** Build one cost dashboard by subscription
- **Build:** Add Resource Graph data for inventory
- **Time:** 2-4 weeks for Azure integration

**Resources:**
- [Azure Cost Reports for Business Reality](/blog/azure-cost-reports-business-reality/)
- [Chris Bowman Dashboard Model](/blog/chris-bowman-dashboard/)

### Learn AI for Operations
- **Start:** Use Copilot for Azure for optimization suggestions
- **Practice:** Azure OpenAI for KQL query generation
- **Build:** Automation script that summarizes Azure data
- **Time:** 1-2 weeks to experiment

**Resources:**
- [AI for Azure Admins Gap](/blog/ai-azure-admins-gap/)

## The Bottom Line

**Microsoft has certifications for:**
- Building infrastructure (AZ-104)
- Designing solutions (AZ-305)
- Securing environments (AZ-500)
- Building AI (AI-102)
- Analyzing data (DP-203)
- Creating BI reports (PL-300)

**Microsoft has NO certification for:**
- Building operational dashboards with Workbooks
- Writing KQL queries for Azure operations
- Creating Power BI reports from Azure data
- Using AI for administrative workflows

**Yet this is what most Azure administrators actually do 60-80% of the time.**

The role exists. The tools exist. The job postings exist.

**Only the certification is missing.**

---

## Related Resources

**Learn the skills Microsoft doesn't certify:**
- [KQL Mastery Hub](/hub/kql/) - Production KQL queries
- [Monitoring & Dashboards Hub](/hub/monitoring/) - Workbook patterns
- [FinOps Hub](/hub/finops/) - Power BI cost reporting

**Certification discussion:**
- [Why I'm Not Renewing Azure Certifications](/blog/not-renewing-azure-certs-choosing-ai-102/)
- [Azure Tool Selection for Noobs](/blog/azure-tool-selection-noobs/)

---

**Do you spend more time building reports than deploying infrastructure? Let me know in the comments what certifications you think would actually help Azure admins.**

*Updated December 7, 2025*
