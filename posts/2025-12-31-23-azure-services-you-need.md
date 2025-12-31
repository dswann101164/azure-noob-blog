---
title: "The 23 Azure Services You Actually Need to Know (Out of 200+)"
date: 2025-12-31
summary: "Azure lists 200+ services. You only need to deeply understand 23 of them. These services appear in every enterprise environment from 20 VMs to 30,000 resources. Master these first—ignore the other 180 until you actually need them."
tags: ["Azure", "Architecture", "Foundational"]
cover: "static/images/hero/azure-services-map.png"
---

**Short Answer:**
Azure lists 200+ services in the portal. In practice, every enterprise environment—whether running 20 VMs or 30,000 resources—relies on the same 23 foundational services. Master these 23 first. The other 180? Edge cases, regional variants, and marketing. You can safely ignore them until you actually need them.

---

If you've ever opened the Azure portal and thought "this feels like a city that grew without zoning laws," you're not wrong.

Microsoft keeps adding services. The portal keeps getting more cluttered. And Azure admins keep thinking they're behind because they don't understand Azure Purview, Azure Synapse, or whatever new SKU marketing launched this quarter.

Here's the truth nobody tells you:

**You don't need to know all of Azure to be effective.**

You need to know 23 services.

These 23 services appear in every real-world enterprise deployment. They form the foundation of every architecture. Everything else is optional until proven otherwise.

This post breaks them down by function, maps them to AWS and Google Cloud equivalents, and gives you permission to stop feeling guilty about ignoring the other 180 services.

## Why 23?

Because this is what actually shows up when you manage production Azure environments.

I manage 44 Azure subscriptions with 31,000+ resources across a regulated financial services environment. When I run inventory queries, when I troubleshoot outages, when I write documentation—these 23 services appear over and over.

The rest? Specialty tools for specific use cases. Important when you need them. Noise until you do.

## The Mental Model That Makes Azure Click

Before listing services, you need a framework that makes sense of how they relate.

**Think of Azure as a city:**

- **VNet** → Gated communities and roads
- **Compute** → Factories, offices, workers
- **Storage** → Warehouses and archives
- **Databases** → Filing cabinets and records offices
- **Monitoring & Security** → Surveillance, patrols, and alarms

Once you see Azure this way, architecture decisions stop being mysterious. You're not memorizing services—you're understanding how a city functions.

Now let's map the 23 services to this city.

---

## I. Compute Services – Where Work Actually Happens

Compute services are your labor force. They execute code, host applications, and process data.

### 1. Azure Virtual Machines (VMs)

**The foundation.** Choose your OS, size, disk, and networking. Most enterprise Azure spend is still VMs.

**Used for:** Legacy apps, domain controllers, anything you lifted-and-shifted

**AWS:** EC2 | **Google:** Compute Engine

**Reality check:** If you migrated to Azure, 70% of your workload landed here. Containerizing .NET Framework apps with SQL Server dependencies is a 12-month project, not a weekend task. Azure Migrate lied about complexity.

### 2. Azure Kubernetes Service (AKS)

Managed Kubernetes control plane for containerized workloads.

**Used for:** Microservices, platform engineering, scalable cloud-native apps

**AWS:** EKS | **Google:** GKE

**Reality check:** AKS doesn't remove complexity—it moves it. You still need to understand networking, storage classes, ingress controllers, and pod security. If you're managing 10 microservices or fewer, you probably don't need this yet.

### 3. Azure Functions

Event-driven, serverless compute.

**Used for:** Automation, webhooks, scheduled jobs, event processing

**AWS:** Lambda | **Google:** Cloud Functions

**Example workflow:** Blob uploaded → Function triggers → Image resized → Stored in CDN

**Reality check:** Cold start times make Functions unusable for latency-sensitive APIs. Great for async workflows. Terrible for user-facing requests that need sub-200ms response times.

### 4. Azure App Service

Platform-as-a-Service hosting for web apps and APIs.

**Used for:** Web applications without VM management

**AWS:** Elastic Beanstalk | **Google:** App Engine

**Reality check:** Works great until you need custom kernel modules, specific OS patches, or non-standard ports. Then you're back to VMs.

### 5. Azure Batch

Massively parallel compute jobs.

**Used for:** Rendering, simulations, HPC workloads, large-scale data processing

**AWS:** AWS Batch | **Google:** Dataflow

---

## II. Storage Services – The Warehouse District

Storage is where data lives. Not where logic runs.

### 6. Azure Blob Storage

Object storage for unstructured data.

**Stores:** Media files, PDFs, logs, backups, anything that isn't a database

**AWS:** S3 | **Google:** Cloud Storage

**Reality check:** Hot tier for frequent access, Cool tier for backups, Archive tier for compliance. Most teams overpay by keeping everything in Hot tier. Review access patterns quarterly.

### 7. Azure Data Lake Storage Gen2

Blob Storage optimized for big data analytics.

**Used for:** Raw data ingestion, data lake architectures, analytics pipelines

**AWS:** S3 (with specific configs) | **Google:** Cloud Storage

**Reality check:** Not a replacement for databases. This is for dumping raw CSV/JSON/Parquet files before transformation. If you have under 5TB of data, you probably don't need this yet.

### 8. Azure Files

Managed SMB/NFS file shares in the cloud.

**Used for:** Lifted file servers, shared application storage

**AWS:** EFS | **Google:** Filestore

**Reality check:** If you ran a Windows file server on-prem, this is its cloud cousin. Performance degrades over ExpressRoute with high latency. Test before migrating.

---

## III. Database Services – The Records Office

Databases are structured truth. Not just storage.

### 9. Azure SQL Database

Fully managed relational SQL database.

**Used for:** Application databases, modernized SQL Server workloads

**AWS:** RDS (SQL Server) | **Google:** Cloud SQL

**Reality check:** Still Microsoft SQL Server under the hood—just without patching at 2am. Some features from on-prem SQL Server don't exist in Azure SQL DB. Check compatibility before migration.

### 10. Azure Cosmos DB

Globally distributed NoSQL database.

**Used for:** Low-latency multi-region apps, globally distributed systems

**AWS:** DynamoDB | **Google:** Firestore/Datastore

**Reality check:** Global replication sounds great until you see the bill. A multi-region Cosmos DB deployment can cost 5x a single-region Azure SQL instance. Understand your actual latency requirements before committing.

---

## IV. Networking Services – Roads, Gates, and Bridges

Networking defines trust boundaries. Everything secure starts here.

### 11. Azure Virtual Network (VNet)

Your private network boundary. Security perimeter for all resources.

**AWS:** VPC | **Google:** VPC

**Reality check:** 80% of Azure connectivity tickets trace back to VNet peering, NSG rules, or route tables. Understand subnet design before deploying anything. Bad VNet architecture is expensive to fix later.

### 12. Azure Load Balancer

Layer 4 load balancing for VMs and internal services.

**AWS:** Network Load Balancer | **Google:** Network Load Balancing

**Reality check:** Use this for internal VM-to-VM traffic. For internet-facing HTTPS apps, use Application Gateway instead.

### 13. Azure Application Gateway

Layer 7 load balancer with WAF (Web Application Firewall).

**Used for:** Internet-facing web applications, SSL termination, path-based routing

**AWS:** Application Load Balancer | **Google:** Cloud Load Balancing

### 14. Azure ExpressRoute

Private dedicated connectivity between on-prem and Azure.

**Used for:** Enterprise hybrid cloud, low-latency requirements, regulatory compliance

**AWS:** Direct Connect | **Google:** Cloud Interconnect

**Reality check:** ExpressRoute + Private Endpoints + DNS = where most enterprise Azure networking problems come from. Budget 3-6 months for proper implementation.

### 15. Azure VPN Gateway

Encrypted connectivity between on-prem and Azure over the internet.

**Used for:** Smaller sites, branch offices, temporary connectivity

**AWS:** VPN Gateway | **Google:** Cloud VPN

**Reality check:** Cheaper than ExpressRoute but unpredictable latency. Don't use this for latency-sensitive applications.

---

## V. Identity & Access – The Security Checkpoint

### 16. Azure Active Directory (Entra ID)

Identity and access control for everything in Azure.

**Manages:** Users, groups, RBAC, conditional access, MFA

**AWS/Google:** IAM (but Entra ID is far more mature for enterprise identity)

**Reality check:** This isn't optional. Every security audit, every compliance framework, every zero-trust architecture starts here. Invest time understanding Entra ID RBAC roles vs Azure RBAC roles—they're different systems.

---

## VI. Management & Monitoring – The Control Center

These services answer: "What's happening in my environment right now?"

### 17. Azure Monitor

Centralized telemetry, metrics, logs, and alerts.

**Used for:** Performance monitoring, troubleshooting, alerting

**AWS:** CloudWatch | **Google:** Cloud Monitoring

**Reality check:** Azure Monitor is NOT optional at scale. When a distributed application breaks at 2am, this is how you debug it. Without proper logging and metrics, you're flying blind.

### 18. Azure Log Analytics

Query engine for Azure Monitor logs using KQL.

**Used for:** Searching logs, building dashboards, security investigations

**AWS:** CloudWatch Logs Insights | **Google:** Cloud Logging

**Reality check:** Learn KQL. It's the only way to query across 30,000 resources effectively. Every compliance audit asks for log queries. Start building a query library now.

### 19. Azure Policy

Governance as code. Enforce compliance rules automatically.

**Used for:** Tag enforcement, allowed regions, required encryption, compliance

**AWS:** Config + Organizations | **Google:** Organization Policy

**Reality check:** Don't deploy Policy until you understand what your environment looks like today. Auto-remediation can break production workloads if misconfigured.

### 20. Azure DevOps

End-to-end DevOps platform.

**Includes:** Git repos, CI/CD pipelines, work tracking, artifact management

**AWS:** CodeCommit + CodePipeline + CodeBuild | **Google:** Cloud Build

**Reality check:** If you're already on GitHub, you probably don't need Azure DevOps. But if you need on-prem agents, artifact feeds, and work tracking integrated—this is the best option in the Azure ecosystem.

---

## VII. AI & Analytics – The Intelligence Layer

### 21. Azure OpenAI Service

Hosted ChatGPT, GPT-4, and other OpenAI models.

**Used for:** Chatbots, content generation, document analysis, embeddings

**AWS:** Bedrock | **Google:** Vertex AI

**Reality check:** Token costs add up fast. A single poorly optimized RAG implementation can cost $10K/month. Understand pricing and implement caching before going to production.

### 22. Azure Cognitive Services

Prebuilt AI APIs for vision, speech, language, and search.

**Used for:** OCR, translation, sentiment analysis, speech-to-text

**AWS:** Rekognition, Transcribe, Comprehend | **Google:** Vision AI, Speech-to-Text

**Reality check:** Great for prototyping. Expensive at scale. If you're processing millions of documents monthly, custom models might be cheaper.

### 23. Azure Synapse Analytics

Enterprise data warehousing and big data analytics.

**Used for:** Data warehouse consolidation, large-scale analytics

**AWS:** Redshift | **Google:** BigQuery

**Reality check:** You're not ready for Synapse until you have 5TB+ data, dedicated data engineers, and a clear analytics strategy. Most companies try this too early.

---

## What About Everything Else?

**"But what about Azure Purview / Azure Arc / Azure Sentinel / [insert service]?"**

Those services matter—when you actually need them.

Here's when to explore beyond the 23:

### Azure Arc
**Learn it when:** You need to manage on-prem or multi-cloud resources from Azure  
**Not before:** You've fixed basic Azure governance (tagging, RBAC, cost management)

### Azure Sentinel
**Learn it when:** You need a cloud-native SIEM  
**Not before:** You have centralized logging and a security team to act on alerts

### Azure Purview
**Learn it when:** You need data cataloging across multiple data sources  
**Not before:** You have governance that teams actually follow

### Azure Data Factory
**Learn it when:** You need ETL pipelines and data orchestration  
**Not before:** You understand your data flow requirements

The pattern:

**Don't learn services because Microsoft is promoting them. Learn them when they solve a problem you already have.**

---

## How to Actually Use This List

**If you're new to Azure:**
Start with Compute, Storage, Networking, and Identity. Build something real. Deploy a web app. Break it. Fix it.

**If you manage production Azure:**
Audit your environment. I guarantee 95% of your resources use these 23 services. The remaining 5% are specialty tools or abandoned experiments.

**If you're studying for certifications:**
Microsoft exams test breadth. This list gives you depth. Master these 23 in production, then fill certification gaps as needed.

**If you're explaining Azure to leadership:**
Use the city analogy. "VNet is our gated community boundary. Monitor is our city operations center. Entra ID is the security checkpoint."

---

## Final Reality Check

Most Azure failures don't happen because someone chose the wrong service.

They happen because:
- No one understood how services relate
- No one owned boundaries  
- No one could explain the system simply

Cloud maturity starts when you can explain your architecture without needing a diagram.

These 23 services give you that foundation.

Master them first. Expand strategically. Stop feeling guilty about the other 180.
