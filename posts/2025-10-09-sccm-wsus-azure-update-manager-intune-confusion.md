---
title: "Intune vs WSUS 2025: Which Patch Management Tool to Use"
date: 2025-10-09
modified: 2025-12-31
summary: "Intune vs WSUS comparison 2025: Intune for cloud-first organizations ($6/user), WSUS for on-prem (free but complex). Includes SCCM and Azure Update Manager comparison, migration guide, and FAQ."
tags: ["azure", "sccm", "wsus", "intune", "azure-update-manager", "patch-management", "operations"]
cover: "static/images/hero/patch-management-confusion.svg"
animated_hero: true
hub: governance
faq_schema: true
related_posts:
  - azure-resource-tags-guide
  - azure-tag-governance-policy
  - azure-policy-reality-check
---

## WSUS vs SCCM vs Intune: Which Should You Use in 2025?

**Short Answer (Pick One):**

**Use WSUS if:** You have on-premises servers only, need free patching, and don't require application deployment. WSUS handles Windows updates but nothing else. Best for small environments (under 500 devices) with no cloud migration plans.

**Use SCCM (Configuration Manager) if:** You manage enterprise servers that need both patching and application deployment. SCCM includes WSUS functionality plus software deployment, OS imaging, and compliance management. Required for complex on-premises or hybrid environments with 1,000+ servers.

**Use Intune if:** You manage Windows 10/11 endpoints (laptops, desktops) in a cloud-first organization. Intune costs $6-8 per device per month but eliminates on-premises infrastructure. Not designed for servers—use SCCM or Azure Update Manager instead.

**Use Azure Update Manager if:** You only need simple patch management for Azure VMs without application deployment. Free for Azure VMs, works for both Windows and Linux. Requires Azure Arc ($5/month per server) for on-premises machines.

**Most enterprises use a combination:** SCCM for on-prem servers with app deployment needs, Azure Update Manager for simple Azure VM patching, and Intune for cloud-connected endpoints.

---

## Intune vs WSUS vs SCCM vs Azure Update Manager: Comparison Table

Here's the comparison table Google wants to show as a featured snippet:

| Feature | WSUS | SCCM | Azure Update Manager | Intune |
|---------|------|------|---------------------|--------|
| **Best For** | Small on-prem environments | Enterprise servers | Azure VMs | Windows 10/11 endpoints |
| **Cost** | Free | License + infrastructure | Free (Azure VMs) | $6-8/device/month |
| **Application Deployment** | ❌ No | ✅ Yes | ❌ No | ✅ Yes (endpoints only) |
| **Patch Management** | ✅ Yes | ✅ Yes (via WSUS) | ✅ Yes | ✅ Yes |
| **Works On-Prem** | ✅ Yes | ✅ Yes | ⚠️ Requires Arc ($5/mo) | ❌ Cloud-first |
| **Works in Azure** | ⚠️ Manual setup | ✅ Yes | ✅ Yes | ✅ Yes (endpoints) |
| **Manages Servers** | ✅ Yes | ✅ Yes | ✅ Yes | ❌ Not designed for servers |
| **Infrastructure Required** | ✅ Yes (Windows Server) | ✅ Yes (SQL, sites, DPs) | ❌ No | ❌ No |
| **Complexity** | Low | High | Low | Medium |

**Short answer:** Use SCCM for servers needing app deployment, Azure Update Manager for simple Azure VM patching, Intune for Windows 10/11 desktops. WSUS is legacy - SCCM includes it anyway.

## The Problem: Microsoft Has 4 Patching Solutions

Managing a large enterprise environment with dozens of Azure subscriptions, hybrid infrastructure, and an active migration in progress, here's what Microsoft offers for patching:

**WSUS (Windows Server Update Services):**
- Free, built into Windows Server
- Manual patch approvals
- On-prem only
- What enterprises used before SCCM

**SCCM/Configuration Manager:**
- Enterprise systems management
- Application deployment, OS deployment, inventory
- On-prem infrastructure required
- **Requires WSUS for patching**

**Azure Update Manager:**
- Cloud-native patching for Azure VMs
- No infrastructure required
- Free (part of Azure platform)
- **Patching only - no app deployment**

**Intune:**
- Modern device management for endpoints
- Cloud-first, designed for Windows 10/11 workstations
- Co-management with ConfigMgr possible
- $6-8/device/month

**The question everyone asks:** "Which one should I use?"

**The answer nobody gives:** "All of them, depending on the workload."

## What Each Tool Actually Does

### WSUS: The Foundation You Can't Kill

**What Microsoft says:**
"Windows Server Update Services provides update management for Microsoft products."

**What it actually is:**
- Free Windows Server role
- Downloads updates from Microsoft
- Distributes to endpoints
- Manual approval workflow

**The critical detail nobody mentions:**
SCCM requires WSUS to function. SCCM doesn't patch by itself - it uses WSUS as the backend.

**This means:**
- If you have SCCM, you have WSUS (embedded)
- You can't "just use SCCM" without WSUS infrastructure
- WSUS exists whether you see it or not

**What WSUS does:**
- ✅ Patches Windows servers and desktops
- ✅ Patches Microsoft products (Office, SQL, etc.)
- ❌ No application deployment
- ❌ No third-party patching (without add-ons)
- ❌ Limited reporting
- ❌ Manual approval workflow

**When to use WSUS standalone:**
- Small environment (< 100 servers)
- Simple patching needs
- No budget for SCCM
- No complex app deployment requirements

**Reality check:**
Most enterprises outgrow WSUS quickly. It works, but it's manual and limited.

### SCCM: The Enterprise Kitchen Sink

**What Microsoft says:**
"Microsoft Endpoint Configuration Manager provides comprehensive management of servers, workstations, and mobile devices."

**What it actually is:**
- Full systems management platform
- Application deployment
- OS deployment and imaging
- Hardware/software inventory
- Compliance reporting
- **Uses WSUS for patching backend**

**The architecture:**
```
SCCM (management layer)
    ↓
WSUS (patching backend)
    ↓
Endpoints
```

**What SCCM does:**
- ✅ Application deployment (complex multi-tier apps)
- ✅ OS deployment and imaging
- ✅ Patch management (via integrated WSUS)
- ✅ Hardware/software inventory
- ✅ Compliance and reporting
- ✅ Works on-prem and Azure (with agent)
- ❌ Complex to maintain
- ❌ Requires SQL Server, distribution points, site servers
- ❌ Expensive (licensing + infrastructure)

**When to use SCCM:**
- Need application deployment (not just patching)
- Complex enterprise environment
- On-prem infrastructure still exists
- Multi-tier application deployments
- OS imaging requirements

**Reality check:**
SCCM is overkill if you only need patching. But if you need app deployment for servers, it's the only Microsoft option.

### Azure Update Manager: Cloud-Native Patching Only

**What Microsoft says:**
"Azure Update Manager is a unified service to help manage and govern updates for all your machines."

**What it actually is:**
- Cloud-native patching service
- Free for Azure VMs
- $5/month for Arc-enabled on-prem servers
- **Patching only - zero app deployment**

**What Azure Update Manager does:**
- ✅ Patch Azure VMs (Windows + Linux)
- ✅ Schedule patching with maintenance windows
- ✅ Compliance reporting in Azure Portal
- ✅ Free for Azure VMs
- ✅ No infrastructure to maintain
- ❌ **Cannot deploy applications**
- ❌ Cannot image/deploy OS
- ❌ On-prem servers require Azure Arc ($$$)
- ❌ No complex orchestration (patch server 1, then 2, then restart app)

**When to use Azure Update Manager:**
- Azure VMs that only need patching
- No complex app deployment requirements
- Want to avoid SCCM infrastructure in cloud
- Simple maintenance window needs

**When NOT to use it:**
- Need application deployment
- Complex patching dependencies
- On-prem servers (unless you want to pay for Arc)

**Reality check:**
Perfect for simple Azure VM patching. Useless if you need app deployment.

### Intune: Modern Management for Endpoints

**What Microsoft says:**
"Microsoft Intune is a cloud-based endpoint management solution."

**What it actually is:**
- Cloud-based device management
- Designed for Windows 10/11 workstations and mobile devices
- Application deployment included
- **NOT for servers**

**What Intune does:**
- ✅ Manage Windows 10/11 desktops/laptops
- ✅ Mobile device management (iOS, Android)
- ✅ Application deployment for endpoints
- ✅ Conditional access policies
- ✅ Cloud-native, no on-prem infrastructure
- ❌ **Not designed for Windows Server**
- ❌ Limited server management features
- ❌ Can't replace SCCM for server workloads

**When to use Intune:**
- Windows 10/11 workstations
- Laptops and mobile devices
- BYOD scenarios
- Cloud-first strategy

**When NOT to use it:**
- Windows Servers (use SCCM or Azure Update Manager)
- Complex server application deployment
- On-prem-heavy environment

**Reality check:**
Intune is the future for endpoints. It's NOT the future for servers.

## The Decision Matrix Microsoft Won't Publish

Here's what you actually need based on your workload:

| Your Workload | Tool to Use | Why | Cost |
|---------------|-------------|-----|------|
| **On-prem servers** | SCCM (includes WSUS) | Can't use Azure Update Manager without Arc | SCCM license + infrastructure |
| **Azure VMs that need apps** | SCCM (includes WSUS) | Only tool that deploys apps to servers | SCCM license + infrastructure |
| **Azure VMs that only need patches** | Azure Update Manager | Free, cloud-native, simpler | Free |
| **Windows 10/11 laptops/desktops** | Intune | Modern management, designed for endpoints | $6-8/device/month |
| **Hybrid environment during migration** | ALL OF THE ABOVE | Multi-year transition reality | Combined costs |

**The truth nobody tells you:**

You don't choose one tool. You use **multiple tools based on workload requirements.**

## What Sales Teams Actually Say (And What They're Not Telling You)

### Configuration Manager Sales Rep

**What they say:**
"Just keep using SCCM for everything, including Azure VMs."

**Why they say it:**
They sell Configuration Manager licenses and consulting services.

**What they're not telling you:**
- Azure Update Manager is free and simpler for Azure VMs that only need patching
- SCCM requires infrastructure (SQL Server, site servers, distribution points) even in Azure
- You're paying for features you might not need

**When they're right:**
If your Azure VMs need complex application deployment, SCCM is the only option.

**When they're wrong:**
If VMs only need patching, Azure Update Manager is simpler and free.

### Azure Architect

**What they say:**
"Use Azure Update Manager for everything, it's cloud-native."

**Why they say it:**
They want you using Azure-native services, looks good on their cloud migration metrics.

**What they're not telling you:**
- Azure Update Manager cannot deploy applications
- On-prem servers require Azure Arc ($5/server/month)
- Arc adds complexity for infrastructure that's not going away soon

**When they're right:**
If you're Azure-only with simple patching needs, Update Manager is perfect.

**When they're wrong:**
If you need app deployment or manage significant on-prem infrastructure.

### Modern Workplace Consultant

**What they say:**
"Move everything to Intune, retire SCCM."

**Why they say it:**
Intune is the future, cloud-first strategy, "modern management."

**What they're not telling you:**
- Intune is designed for endpoints (desktops, laptops), not servers
- Server management features are limited
- Can't replace SCCM for complex server workloads

**When they're right:**
For Windows 10/11 desktops and laptops, Intune is absolutely the future.

**When they're wrong:**
For Windows Servers or complex application deployments.

## The Real Enterprise Architecture

Here's what large environments actually run during migration:

**Current State (Hybrid Infrastructure):**
- SCCM managing all on-prem servers
- SCCM managing some Azure VMs (that need app deployment)
- Azure Update Manager starting to manage new Azure VMs (patching only)
- WSUS still running (embedded in SCCM infrastructure)
- Intune not deployed yet (future state for endpoints)

**Why this complexity exists:**
- On-prem datacenters not going away immediately (2-5 year timeline)
- Some Azure VMs need complex app deployment (SCCM required)
- Some Azure VMs only need patching (Update Manager simpler)
- Desktops/laptops modernization is separate project (Intune future)

**This is normal.** Multi-year enterprise migrations require multiple tools.

## The Domain Join Decision (And Who Owns Patching)

Here's the organizational mess nobody talks about: **Who decides if new Azure VMs are domain-joined?**

This isn't a technical question. It's a **political question** that determines which team owns patching.

### The Technical Reality

**SCCM and domain join:**
- SCCM works best with domain-joined machines
- **Can** manage workgroup (non-domain) machines, but with limitations:
  - Client push installation doesn't work
  - Automatic client approval doesn't work  
  - User-based application deployments don't work
  - More complex authentication to distribution points
- Most SCCM admins expect everything domain-joined

**Azure Update Manager and domain join:**
- Works with domain-joined Azure VMs ✅
- Works with Azure AD-joined VMs ✅
- Works with workgroup VMs ✅
- **Domain join doesn't matter** - uses Azure VM agent

**The decision:**
When you create a new Azure VM, do you domain-join it to legacy Active Directory?

### The Organizational Conflict

**Legacy AD/SCCM Model:**
- AD team = SCCM team = Infrastructure team
- Everything is domain-joined by default
- SCCM manages all patching
- Clear ownership: "SCCM team patches everything"
- 20+ years of this model

**Cloud-Native Model:**
- Azure team builds VMs
- Cloud-first approach = Azure AD-joined or workgroup
- No dependency on legacy AD
- Azure Update Manager for patching
- Different team, different tools

**The collision:**
You're running **both models simultaneously** during migration.

### The Question Nobody Answers

**Scenario:** Azure team creates 50 new VMs for application migration.

**Question 1:** Are these VMs domain-joined to legacy AD?

**If YES (domain-joined):**
- SCCM can manage them
- AD/SCCM team owns patching
- Requires network connectivity to on-prem domain controllers
- Perpetuates dependency on legacy infrastructure
- SCCM team: "Great, we'll add them to our collections"

**If NO (Azure AD-joined or workgroup):**
- SCCM has trouble managing them (or can't at all)
- Azure team owns patching via Update Manager
- Cloud-native, no AD dependency
- Legacy SCCM team: "Wait, who's patching these?"

**Question 2:** Who decides?

**Common answers (none good):**
- "Whatever the app team wants" (inconsistent, chaos)
- "Everything must be domain-joined" (Azure architect frustrated)
- "Cloud-native only, no domain join" (SCCM team bypassed)
- "We'll figure it out later" (spoiler: you won't)

### The Real Enterprise Scenario

**What actually happens:**

**Phase 1 (Current):**
- Some Azure VMs are domain-joined (legacy apps that require it)
- Some Azure VMs are Azure AD-joined (cloud-native apps)
- Some Azure VMs are workgroup (special cases)
- **Nobody has a clear policy**

**Who patches what:**
- Domain-joined VMs: SCCM team patches via SCCM
- Azure AD-joined VMs: Azure team patches via Update Manager
- Workgroup VMs: "Uh... who owns these?"

**The governance gap:**
- No clear decision framework
- Each app migration handled case-by-case
- Political battles between teams
- Leadership doesn't understand the question

**The meeting that happens:**
```
Azure Team: "We built 50 VMs for the finance app migration."

SCCM Team: "Are they domain-joined?"

Azure Team: "No, we used Azure AD join. They're cloud-native."

SCCM Team: "Then who's patching them?"

Azure Team: "We set up Azure Update Manager."

SCCM Team: "That's not our standard. Everything goes through SCCM."

Azure Team: "But they're not domain-joined. SCCM can't manage them easily."

SCCM Team: "Then domain-join them."

Azure Team: "That defeats the purpose of cloud-native architecture."

[Escalation to leadership]

Leadership: "Just... make it work? Can't you use both?"

[Everyone sighs]
```

### The Governance You Actually Need

**Decision framework that works:**

| Workload Type | Domain Join? | Patching Tool | Who Owns It |
|---------------|--------------|---------------|-------------|
| **Legacy apps requiring AD** | Domain-joined | SCCM | SCCM/AD Team |
| **Cloud-native apps** | Azure AD-joined | Azure Update Manager | Azure/Cloud Team |
| **Complex app deployment needs** | Domain-joined | SCCM | SCCM/AD Team |
| **Simple web/API servers** | Azure AD-joined or Workgroup | Azure Update Manager | Azure/Cloud Team |
| **On-prem servers** | Domain-joined | SCCM | SCCM/AD Team |

**Clear ownership:**
- SCCM team owns all domain-joined infrastructure
- Azure team owns all Azure AD-joined / workgroup infrastructure
- No overlap, no confusion
- Document the policy, enforce in governance

**What this requires:**
- Leadership decision on default approach
- Clear exceptions process
- Both teams trained on their tools
- Governance policy documented
- Tags on VMs to indicate patching ownership

### The Tag Strategy

**Use Azure tags to track ownership:**

```powershell
# When creating Azure VM, tag it
$tags = @{
    "PatchManagement" = "AzureUpdateManager"  # or "sccm"
    "PatchOwner" = "AzureTeam"  # or "SCCMTeam"
    "DomainJoin" = "AzureAD"  # or "LegacyAD" or "Workgroup"
}

New-AzVM -ResourceGroupName "rg-prod" `
    -Name "vm-app-001" `
    -Tag $tags `
    # ... other parameters
```

**Query ownership:**
```kusto
Resources
| where type == "microsoft.compute/virtualmachines"
| extend patchTool = tags["PatchManagement"]
| extend patchOwner = tags["PatchOwner"]
| extend domainJoin = tags["DomainJoin"]
| summarize Count = count() by patchTool, patchOwner
| order by Count desc
```

**This gives you visibility:**
- How many VMs each team owns
- What domain join strategy you're using
- Clear accountability

### Why MVPs Don't Talk About This

MVPs focus on **technical capabilities**, not **organizational politics**.

**They'll tell you:**
- "SCCM can manage workgroup machines" (technically true)
- "Azure Update Manager works with any join type" (technically true)
- "Use the best tool for the workload" (technically correct)

**They won't tell you:**
- How to decide domain join strategy across hundreds of VMs
- Who makes the decision when teams disagree
- How to handle the SCCM team that wants everything domain-joined
- How to handle the Azure team that wants cloud-native everything
- What governance policy actually looks like

**Because MVPs aren't dealing with:**
- Team politics and ownership battles
- Legacy AD teams protecting their territory  
- Cloud teams frustrated by legacy dependencies
- Leadership that doesn't understand the question
- Multi-year transitions with both models running simultaneously

**You are.** This is the operational reality.

### The Bottom Line on Domain Join

**Technical truth:**
Both SCCM and Azure Update Manager can work with various join types.

**Organizational truth:**
Domain join decision determines **which team owns patching**, which creates political friction during migration.

**What you need:**
- Clear decision framework (documented)
- Leadership buy-in on default approach
- Exceptions process for special cases
- Tags for tracking ownership
- Both teams trained on their respective tools
- Governance policy that everyone follows

**Stop pretending it's purely technical.** It's **organizational**, and that's why it's hard.

## The Hidden Dependency: SCCM Requires WSUS

**The misconception:**
"SCCM does patching, so I don't need WSUS."

**The reality:**
SCCM doesn't patch by itself. It uses WSUS as the backend update source.

**The architecture:**
```powershell
# SCCM architecture for patching
SCCM Site Server
    ↓
Software Update Point (SUP) role
    ↓
WSUS Server (backend)
    ↓
SCCM Clients get updates via WSUS
```

**What this means:**
- Installing SCCM requires installing/configuring WSUS
- WSUS downloads updates from Microsoft
- SCCM manages which updates get approved/deployed
- SCCM clients scan against WSUS for compliance
- You can't "just use SCCM" - WSUS is always there

**Verify WSUS is running:**
```powershell
# Check if WSUS role is installed
Get-WindowsFeature -Name UpdateServices

# Check WSUS service status
Get-Service -Name WsusService

# View WSUS content location
Get-WsusServer | Select-Object Name, PortNumber, ServerProtocolVersion
```

**The bottom line:**
If someone says "migrate from WSUS to SCCM," they don't understand the architecture. SCCM includes WSUS.

## Azure Update Manager: What It Can't Do

Microsoft's marketing makes Azure Update Manager sound comprehensive. Here's what it **cannot** do:

### Cannot Deploy Applications

**The scenario:**
You need to deploy a custom application to 50 Azure VMs.

**SCCM:** ✅ Can do this (application deployment feature)

**Azure Update Manager:** ❌ Cannot do this (patching only)

**Your options:**
- Use SCCM (requires infrastructure)
- Use Azure VM extensions (limited, no complex workflows)
- Manual deployment (doesn't scale)

### Cannot Image/Deploy Operating Systems

**The scenario:**
You need to deploy 20 new Windows Server VMs with custom configuration.

**SCCM:** ✅ Can do this (OS deployment feature)

**Azure Update Manager:** ❌ Cannot do this (patching only)

**Your options:**
- Use SCCM
- Use Azure VM Image Gallery
- Use Packer/custom images

### Cannot Manage On-Prem Without Azure Arc

**The scenario:**
You have 500 on-prem servers that need patching.

**SCCM:** ✅ Can manage them (designed for on-prem)

**Azure Update Manager:** ⚠️ Requires Azure Arc ($5/server/month)

**The math:**
- 500 servers × $5/month = $2,500/month = $30,000/year
- Just to enable patching via Update Manager
- SCCM is cheaper if you already have it

### Cannot Do Complex Orchestration

**The scenario:**
Patch server 1, then server 2, then restart application service on server 3, with 10-minute waits between each step.

**SCCM:** ✅ Can do this (orchestration groups, pre/post scripts)

**Azure Update Manager:** ❌ Cannot do this (basic maintenance windows only)

**Reality check:**
Azure Update Manager is **patching only**. If you need anything beyond "install updates and reboot," you need SCCM or custom automation.

## When You Can Actually Ditch SCCM

**Sales pitch:**
"Migrate to Azure Update Manager and Intune, retire SCCM."

**Reality check:**
You can retire SCCM when ALL of these are true:

✅ All on-prem servers migrated to Azure or decommissioned
✅ No Azure VMs require complex application deployment
✅ All desktops/laptops migrated to Intune
✅ No custom OS imaging requirements
✅ No complex orchestration needs

**Timeline for most enterprises:**
- Year 1: Start using Azure Update Manager for new Azure VMs
- Year 2-3: Continue hybrid (SCCM + Update Manager)
- Year 3-5: Decommission on-prem datacenters
- Year 5+: Finally retire SCCM infrastructure

**This is NOT a quick project.**

## The "Can't I Use Both SCCM and Azure Update Manager?" Question

**Short answer:** Technically yes, but not recommended without clear separation.

**The problem:**
Both SCCM and Azure Update Manager try to control the Windows Update Agent on the same server.

**What happens:**
- Conflicting policies
- Updates installed twice
- Unpredictable behavior
- Compliance reporting confusion

**Supported approach:**
- SCCM manages on-prem servers
- Azure Update Manager manages Azure-only VMs
- Clear boundaries, no overlap

**Microsoft's guidance:**
"Azure Update Manager and SCCM should not patch the same server simultaneously."

**What this means:**
Pick one tool per server. Don't try to use both.

## PowerShell: Check What's Managing Your VMs

**Check if VM is managed by SCCM:**
```powershell
# Check for SCCM client
$sccmClient = Get-WmiObject -Namespace "root\ccm" -Class SMS_Client -ErrorAction SilentlyContinue

if ($sccmClient) {
    Write-Host "✓ SCCM Client installed" -ForegroundColor Green
    
    # Get SCCM site code
    $siteCode = (Get-WmiObject -Namespace "root\ccm" -Class SMS_Authority).CurrentManagementPoint
    Write-Host "  Site Code: $siteCode"
    
    # Check last policy update
    $lastPolicy = (Get-WmiObject -Namespace "root\ccm" -Class CCM_PolicyAgent_Configuration).LastUpdateTime
    Write-Host "  Last Policy Update: $lastPolicy"
} else {
    Write-Host "✗ SCCM Client not installed" -ForegroundColor Yellow
}
```

**Check Windows Update source:**
```powershell
# Check if using WSUS
$wuServer = (Get-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate" -Name "WUServer" -ErrorAction SilentlyContinue).WUServer

if ($wuServer) {
    Write-Host "✓ WSUS configured" -ForegroundColor Green
    Write-Host "  WSUS Server: $wuServer"
} else {
    Write-Host "✓ Using Microsoft Update directly" -ForegroundColor Green
}
```

**Check if Azure Update Manager is enabled:**
```powershell
# Check for Azure VM agent
$azureAgent = Get-Service -Name "WindowsAzureGuestAgent" -ErrorAction SilentlyContinue

if ($azureAgent) {
    Write-Host "✓ Azure VM Agent installed" -ForegroundColor Green
    Write-Host "  Status: $($azureAgent.Status)"
}

# Check automatic update settings
$autoUpdate = (Get-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU" -Name "NoAutoUpdate" -ErrorAction SilentlyContinue).NoAutoUpdate

if ($autoUpdate -eq 1) {
    Write-Host "  Automatic updates: Disabled (likely managed by SCCM)" -ForegroundColor Yellow
} else {
    Write-Host "  Automatic updates: Enabled (likely Azure Update Manager)" -ForegroundColor Green
}
```

## KQL: Find VMs by Patch Management Tool

**Find Azure VMs without SCCM client:**
```kusto
Resources
| where type == "microsoft.compute/virtualmachines"
| extend vmId = tolower(id)
| extend powerState = properties.extended.instanceView.powerState.displayStatus
| where powerState == "VM running"
| project vmName = name, resourceGroup, location, vmId
// Add your logic to check for SCCM client via extensions or tags
| where tags["PatchManagement"] != "sccm"
| order by vmName asc
```

**Find VMs by update compliance:**
```kusto
// Query from Azure Update Manager
PatchAssessmentResources
| where type == "microsoft.compute/virtualmachines/patchassessmentresults"
| extend vmId = tolower(split(id, '/patchAssessmentResults')[0])
| extend osType = properties.osType
| extend criticalUpdates = properties.criticalAndSecurityPatchCount
| extend otherUpdates = properties.otherPatchCount
| extend lastAssessment = properties.lastModifiedDateTime
| where criticalUpdates > 0 or otherUpdates > 0
| project vmId, osType, criticalUpdates, otherUpdates, lastAssessment
| order by criticalUpdates desc, otherUpdates desc
```

**Find servers needing Azure Update Manager onboarding:**
```kusto
Resources
| where type == "microsoft.compute/virtualmachines"
| extend powerState = properties.extended.instanceView.powerState.displayStatus
| where powerState == "VM running"
| extend osType = properties.storageProfile.osDisk.osType
| extend patchMode = properties.osProfile.windowsConfiguration.patchSettings.patchMode
| where patchMode != "AutomaticByPlatform" // Not using Azure Update Manager
| project 
    vmName = name,
    resourceGroup,
    location,
    osType,
    currentPatchMode = patchMode,
    subscriptionId
| order by vmName asc
```

## The Real Cost Comparison

**Scenario: 500 servers that need patching**

### Option 1: SCCM (Already Deployed)

**Costs:**
- License: Included in EA (or ~$60/device)
- Infrastructure: SQL Server, site servers, distribution points (already deployed)
- Labor: Dedicated SCCM admin team
- Total: Infrastructure costs already sunk

**Capabilities:**
- ✅ Patching
- ✅ Application deployment
- ✅ OS imaging
- ✅ Complex orchestration

### Option 2: Azure Update Manager (Cloud-Only VMs)

**Costs:**
- License: Free for Azure VMs
- Infrastructure: None
- Labor: Minimal (configure policies)
- Total: **Free**

**Capabilities:**
- ✅ Patching
- ❌ Application deployment
- ❌ OS imaging
- ❌ Complex orchestration

### Option 3: Azure Update Manager + Arc (Hybrid)

**Costs:**
- License: Free for Azure VMs, $5/month for Arc-enabled on-prem
- On-prem: 300 servers × $5/month = $1,500/month = **$18,000/year**
- Infrastructure: None (cloud service)
- Labor: Arc deployment + maintenance
- Total: **$18,000/year + Arc deployment labor**

**Capabilities:**
- ✅ Patching (Azure + on-prem)
- ❌ Application deployment
- ❌ OS imaging
- ❌ Complex orchestration

### Option 4: Keep SCCM + Add Azure Update Manager

**Costs:**
- SCCM: Existing infrastructure costs
- Azure Update Manager: Free for Azure VMs
- Total: SCCM costs (already paid)

**Capabilities:**
- ✅ Patching (both tools)
- ✅ Application deployment (SCCM)
- ✅ OS imaging (SCCM)
- ✅ Complex orchestration (SCCM)

**Reality check:**
Option 4 is what most enterprises actually do during multi-year transitions.

## The Timeline Nobody Tells You

**Sales pitch:**
"Migrate to Azure Update Manager and retire SCCM in 6 months."

**Operational reality:**

### Year 1: Add Azure Update Manager
- Deploy Azure Update Manager policies
- Enable for NEW Azure VMs only
- SCCM still manages all on-prem + existing Azure VMs
- Team learns Azure Update Manager

### Year 2-3: Hybrid State
- Azure Update Manager manages growing number of Azure VMs
- SCCM manages shrinking on-prem infrastructure
- Complex apps still require SCCM (no replacement)
- Both tools running simultaneously

### Year 3-5: On-Prem Decommission
- Migrate remaining on-prem servers to Azure
- Some Azure VMs still need SCCM (app deployment)
- Most Azure VMs now on Update Manager
- On-prem datacenters shut down

### Year 5+: SCCM Retirement
- Last SCCM-managed servers migrated
- SCCM infrastructure decommissioned
- Azure Update Manager for servers
- Intune for endpoints

**This is NOT a fast migration.** Plan 3-5 years minimum for large enterprises.

## What About Intune Co-Management?

**Microsoft's compromise:**
"Use SCCM + Intune together with co-management!"

**What co-management is:**
- ConfigMgr manages some workloads (apps, updates)
- Intune manages other workloads (compliance, conditional access)
- Both agents on same device

**When it makes sense:**
- Gradual transition from SCCM to Intune
- Keep SCCM for complex apps
- Move simple workloads to Intune
- Multi-year migration strategy

**When it's complicated:**
- Two management systems to maintain
- Two sets of policies to configure
- Potential conflicts between SCCM and Intune
- Team needs training on both platforms

**Reality:**
Co-management is a **transition state**, not an end state. It buys you time during migration.

## The Question Leadership Asks

**"When can we decommission SCCM and save money?"**

**The answer they don't want to hear:**
"When we decommission the last on-prem server."

**Why:**
- SCCM infrastructure (SQL, site servers, DPs) costs money
- If you have **1 on-prem server** requiring SCCM, you need the whole stack
- Can't shut down SCCM until everything moves to cloud or Intune

**The financial reality:**
- SCCM infrastructure: $X/year
- Need it for 1 server or 1,000 servers (same infrastructure)
- Can't reduce costs until **complete** migration

**Timeline:**
- On-prem datacenter shutdown: 3-5 years
- SCCM retirement: After datacenter shutdown
- Cost savings: Not until Year 5+

**What you can do sooner:**
- Reduce SCCM complexity (fewer site servers, smaller SQL)
- Start using Azure Update Manager for new Azure VMs (free)
- Move endpoints to Intune (different project)

## The Bottom Line

Microsoft has 4 patching solutions because enterprises are complicated.

**The tools:**
- WSUS: Legacy, manual, free (embedded in SCCM)
- SCCM: Enterprise management, requires WSUS, expensive
- Azure Update Manager: Cloud-native, patching only, free
- Intune: Modern endpoints, cloud-based, subscription cost

**Sales teams will tell you:**
- "Use one solution for everything!"
- "Migrate immediately!"
- "Azure Update Manager replaces SCCM!"

**Operational reality:**
- You need **multiple tools** based on workload
- SCCM doesn't disappear until on-prem does
- Azure Update Manager is great for simple patching
- Intune is for endpoints, not servers
- Plan **3-5 years** for full transition

**Stop asking "which tool should I use?"**

**Start asking: "Which tool for THIS workload?"**

---

## Quick Reference: Decision Tree

```
Is this a Windows 10/11 desktop/laptop?
    ├─ YES → Use Intune
    └─ NO → Continue

Is this a Windows Server?
    ├─ YES → Continue
    └─ NO → Check OS-specific tools

Does this server need complex application deployment?
    ├─ YES → Use SCCM
    └─ NO → Continue

Is this server in Azure?
    ├─ YES → Use Azure Update Manager (free)
    └─ NO (on-prem) → Use SCCM or Arc + Update Manager ($$$)

Are you in a multi-year migration?
    └─ YES → Use ALL tools based on workload (normal)
```

---

## Resources

**Microsoft Official Docs:**
- [Azure Update Manager Overview](https://learn.microsoft.com/en-us/azure/update-manager/)
- [Configuration Manager Documentation](https://learn.microsoft.com/en-us/mem/configmgr/)
- [Intune Documentation](https://learn.microsoft.com/en-us/mem/intune/)
- [WSUS Documentation](https://learn.microsoft.com/en-us/windows-server/administration/windows-server-update-services/get-started/windows-server-update-services-wsus)

**Migration Guidance:**
- [Migrate from SCCM to Azure Update Manager](https://learn.microsoft.com/en-us/azure/update-manager/guidance-migration-azure)
- [Co-management with Intune](https://learn.microsoft.com/en-us/mem/configmgr/comanage/overview)

**Related Posts:**
- [Azure VM Automation Dependency Hell](/blog/azure-vm-automation-dependency-hell/) - Chocolatey vs winget automation challenges
- [PowerShell Scripts Break on Server 2025](/blog/azure-scripts-break-server-2025/) - ISE vs PowerShell 7 for Azure automation
- [The 3 Hour Debugging Rule](/blog/azure-debugging-ai-rule/) - When to stop debugging and open Microsoft support

---

## Frequently Asked Questions

### Can WSUS manage Windows 11 updates?

Yes, but with limitations. WSUS can deploy Windows 11 feature updates and security patches, but:
- ❌ Cannot enforce hardware requirements (TPM 2.0, Secure Boot)
- ❌ No support for Windows Update for Business policies
- ❌ Missing cloud-native telemetry and reporting
- ✅ Works for basic patching in stable environments

Microsoft recommends Intune for Windows 11 management because WSUS lacks modern device management capabilities (conditional access, compliance policies, autopilot).

### Do I need SCCM if I have Intune?

Depends on your infrastructure:

**You need SCCM if:**
- Managing on-premises servers (Server 2016, 2019, 2022)
- Deploying thick-client applications (legacy software with MSI/EXE installers)
- Operating system deployment (bare-metal imaging)
- Software distribution in air-gapped networks

**Intune alone works if:**
- 100% cloud-connected devices
- Windows 10/11 modern apps only
- No on-prem server management needed

**Hybrid reality:** Most enterprises run SCCM + Intune together with co-management until legacy infrastructure is fully retired (5-10 year timeline).

### What replaces WSUS in a cloud-first strategy?

**Microsoft's official replacement path:**
1. **Intune** - For Windows 10/11 desktops and laptops
2. **Azure Update Manager** - For Azure VMs and Arc-enabled servers
3. **Windows Update for Business** - Cloud policy engine for update rings

**Migration timeline:**
- Phase 1: Move Windows 10/11 devices to Intune (6-12 months)
- Phase 2: Arc-enable on-prem servers → Azure Update Manager (12-24 months)
- Phase 3: Retire WSUS servers (18-36 months)

**Reality:** Most enterprises keep WSUS running 3-5 years longer than planned because legacy applications break with modern management tools.

### Can Azure Update Manager manage on-premises servers?

Yes, through Azure Arc. Steps:
1. Install Azure Arc agent on on-prem VMs (VMware, Hyper-V, physical servers)
2. Register servers with Azure (creates Arc-enabled server resource)
3. Enable Azure Update Manager for Arc servers
4. Schedule patching through Azure portal

**Limitation:** Servers must have internet connectivity (direct or through proxy) to Azure Arc endpoints. Air-gapped networks require Azure Stack HCI or SCCM.

**Cost:** Azure Arc itself is free. Azure Update Manager charges per managed server (approximately $5-$10/server/month depending on monitoring features enabled).

For complete Azure Arc deployment patterns and enterprise-scale management, see our [Azure Arc hub](/hub/arc/).

### Is SCCM being discontinued?

No, but Microsoft is **"deprioritizing"** it. Current status:
- ✅ Still supported (support continues through 2027+)
- ✅ Security updates continue
- ⚠️ New features minimal (focus shifted to Intune)
- ⚠️ Renamed to "Configuration Manager" to de-emphasize "System Center"

**Microsoft's message:** "We're not killing SCCM, but we're not investing in it either. Migrate to Intune + Azure Update Manager for long-term support."

**Enterprise reality:** SCCM remains critical for 60-70% of large enterprises managing legacy infrastructure. Full migration to Intune takes 5-10 years in regulated industries.

### What's the cost difference between WSUS and Intune?

**WSUS:**
- License: $0 (included with Windows Server)
- Infrastructure: Server hardware/VM costs (~$2K-$5K/year)
- Labor: 0.5-1 FTE for management (~$50K-$100K/year)
- **Total Cost for 500 devices:** ~$50K-$100K/year

**Intune:**
- License: $6-$14/user/month (Microsoft 365 E3/E5)
- Infrastructure: $0 (cloud-hosted)
- Labor: 0.1-0.2 FTE for management (~$10K-$20K/year)
- **Total Cost for 500 devices:** ~$40K-$90K/year

**Verdict:** Intune is cost-comparable for organizations already on Microsoft 365 E3/E5. For companies on basic Office 365 plans, adding Intune increases costs significantly.

### Can I use WSUS and Intune together?

Yes, but it creates management confusion:
- **Co-management scenarios:** SCCM acts as bridge between WSUS and Intune
- **Split management:** WSUS for on-prem servers, Intune for cloud devices
- **Migration phase:** Gradually move device groups from WSUS → Intune

**Best practice:** Use SCCM as intermediary rather than running WSUS + Intune directly. SCCM provides unified reporting and prevents devices from receiving conflicting update policies.

**Common mistake:** Organizations enable both WSUS and Intune for the same devices, creating duplicate update deployments and patch conflicts.

For enterprise governance strategies around update management and compliance, see our [Azure Governance hub](/hub/governance/).

---

*Managing enterprise Azure patching strategy? This is the operational reality nobody documents. If this helped clarify the confusion, share it with your team - they're probably asking the same questions.*

*Updated December 22, 2025 with FAQ section and 2025 comparison guidance.*
