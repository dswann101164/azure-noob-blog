---
title: "I Migrated My Own Azure Virtual Desktop to Windows 11 with 512GB Disk Space"
date: 2025-10-28
summary: "How I migrated from a cramped 127GB Windows 10 AVD to a spacious 512GB Windows 11 environment - including the gotchas nobody tells you about disk partitions, authentication, and user assignments."
tags: ["Azure", "AVD", "Windows 11", "Operations"]
cover: "/static/images/hero/avd-win11-migration.png"
---

I was running out of disk space on my Azure Virtual Desktop. 127GB total, only 18GB free. Time to migrate to Windows 11 with more breathing room.

This is the story of migrating my own daily driver AVD from Windows 10 to Windows 11, complete with all the mistakes, fixes, and lessons learned along the way.

## The Problem

My current AVD session host:
- **VM:** wvdsnvtestn-2.moonlab.local
- **OS:** Windows 10 Enterprise Multi-session
- **Size:** Standard D8s v5 (8 vCPU, 32GB RAM)
- **Disk:** 127GB total, **18GB free** (85% full)

Where did the space go?

```powershell
C:\Users:              17.11 GB  (profiles and local cache)
C:\Program Files:      15.73 GB  (64-bit apps)
C:\Program Files (x86): 12.45 GB  (32-bit apps)
C:\Windows:            ~40-50 GB (system files, WinSxS)
Page file:             ~8 GB     (based on 32GB RAM)
```

Nothing crazy. Just normal Windows bloat and standard tools. But 18GB free isn't enough headroom for an architect doing daily work.

**Time to migrate.**

## The Decision: New Pool vs In-Place Upgrade

With a Personal AVD pool, I had two options:

### Option 1: In-Place Upgrade Existing Pool
- Upgrade each VM from Win 10 to Win 11
- No infrastructure changes
- All-or-nothing approach
- No rollback if issues

### Option 2: Create New Pool (What I Chose)
- Build new Windows 11 pool alongside existing
- Test before committing
- Easy rollback (keep old pool running)
- Zero user impact during migration
- Run both pools in parallel

**I chose Option 2.** As the guinea pig for my own migration, I wanted a safety net.

## Building the New Pool

### Pool Configuration

Created a new host pool: `wvdhostpool1-win11`

```
Pool Settings:
- Type: Personal
- Assignment: Direct (match current setup)
- Location: East US
- Workspace: win11 (new workspace for clarity)
- Managed Identity: Enabled
- Diagnostics: Log Analytics (Sentinel)
```

**Why a new workspace?**

I could have added the new pool to the existing workspace, but separating them makes it clearer during migration:
- Old workspace = Win 10 VMs
- New workspace = Win 11 VMs

Users know exactly which desktop they're launching.

### Session Host Configuration

**This is where it gets interesting.**

```
VM Settings:
- Name prefix: win1101-
- Image: Windows 11 Enterprise Multi-session (25H2)
- VM size: Standard D8s v5 (8 vCPU, 32GB RAM)
- OS disk size: 512GB Standard SSD  ← THE KEY REQUIREMENT
- Network: vnet-prod-onprem2azure
- Subnet: snet-prod-onprem2azure-prod
- Security: Trusted launch, secure boot, vTPM, integrity monitoring
```

**Critical: Domain Join Settings**

The first time I tried to deploy, I missed this. The Azure portal has a setting buried in the VM configuration:

```
Specify domain or unit: YES  ← Must be set to Yes
Domain to join: moonlab.local
Domain join type: Active Directory
Domain admin credentials: (your account with join permissions)
```

If you skip this, the VM deploys but:
- ❌ Not domain joined
- ❌ AVD agent not installed automatically
- ❌ Not registered to host pool

**You have to delete it and start over.** Ask me how I know.

## The 512GB Disk Mystery

The deployment succeeded. I connected to the new Win 11 VM and checked disk space:

```powershell
PS C:\> Get-Volume | Select DriveLetter, @{Name="Size(GB)";Expression={[math]::Round($_.Size/1GB,2)}}, @{Name="Free(GB)";Expression={[math]::Round($_.SizeRemaining/1GB,2)}}

DriveLetter Size(GB) Free(GB)
----------- -------- --------
C             126.45    96.76
```

**Wait. What?**

The Azure portal clearly showed the disk as 512GB. But Windows only saw 127GB.

### The Gotcha: Unallocated Space

I checked the disk properties in the Azure portal:

**Disk size: 512 GiB** ✅

The disk WAS 512GB. But the partition was only 127GB. The remaining ~385GB was sitting there unallocated.

**This is a common gotcha with Azure VMs.** When you specify a larger disk size during deployment, Azure creates the disk at that size, but the partition inside Windows doesn't automatically expand to fill it.

### The Fix: Extend the Partition

**On the Win 11 VM:**

1. Open Computer Management: `compmgmt.msc`
2. Go to Storage → Disk Management
3. You'll see:
   - C: drive = 127GB (in use)
   - Unallocated space = ~385GB (grayed out)
4. Right-click C: drive → **Extend Volume**
5. Walk through the wizard (use all available space)
6. Done - C: drive now shows 512GB

**No downtime. No VM restart needed.**

After extending:

```powershell
PS C:\> Get-Volume | Select DriveLetter, @{Name="Size(GB)";Expression={[math]::Round($_.Size/1GB,2)}}, @{Name="Free(GB)";Expression={[math]::Round($_.SizeRemaining/1GB,2)}}

DriveLetter Size(GB) Free(GB)
----------- -------- --------
C             476.45   450.32
```

**Much better.** 450GB free vs 18GB before.

## Installing Apps: The Automated Way

I didn't want to manually click through installers. Here's the Chocolatey script I used:

```powershell
# Azure Architect AVD Setup Script
# Run as Administrator

Set-ExecutionPolicy Bypass -Scope Process -Force

# Install Chocolatey
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))

# Refresh environment
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# Install tools
choco install -y powershell-core
choco install -y vscode
choco install -y git
choco install -y azure-cli
choco install -y microsoftazurestorageexplorer
choco install -y azure-data-studio
choco install -y notepadplusplus
choco install -y 7zip
choco install -y googlechrome
choco install -y adobereader

# Install Azure PowerShell modules
Install-Module -Name Az -Repository PSGallery -Force -AllowClobber

Write-Host "Base tools installed. Office/Teams/Visio require manual installation." -ForegroundColor Green
```

**The script ran flawlessly.** All tools installed without interaction.

**Manual installs still needed:**
- Office (Microsoft 365 Apps)
- Teams (VDI-optimized version)
- Visio (requires specific licensing)

These can't be easily scripted due to licensing activation requirements at Synovus.

## The Authentication Puzzle

With the VM ready, I tried to connect from my home computer.

**Remote Desktop client → Subscribe to workspace:**

Entered: `dswann@moonlab.local`

**Error:** "We couldn't find any Workspaces."

### The Problem: Azure AD vs On-Premises AD

**Inside the corporate network (via WVD):**
- I authenticate with my on-premises AD account: `dswann@moonlab.local`
- Kerberos/NTLM to domain-joined machines

**From the internet (connecting to AVD):**
- I need to authenticate with my **Azure AD account**: `dswann@snvtest.com`
- Modern authentication/OAuth to Azure

**These are two different accounts.** AVD from the internet requires the Azure AD UPN, not the on-prem domain account.

### The Fix: Correct Account and Assignments

**Two assignments needed for Personal pools with Direct assignment:**

**1. Application Group Assignment**

This controls who can see and access the workspace.

```
Azure Portal → AVD → Workspaces → win11 → Application groups 
→ wvdhostpool1-win11-DAG → Assignments → Add

Add user: dswann@snvtest.com
```

**2. VM Assignment**

This controls which specific VM you're assigned to.

```
Azure Portal → AVD → Host pools → wvdhostpool1-win11 
→ Session hosts → win1101-0.moonlab.local → Assignment

Add user: dswann@snvtest.com
```

**Both are required.** Miss either one and you can't connect.

After adding both assignments, I waited 2-5 minutes for propagation, then:

**Remote Desktop client → Subscribe:**

Entered: `dswann@snvtest.com`

**Success.** The "win11" workspace appeared.

### MFA and Single Sign-On

**Interesting operational detail:**

When I first connected from home:
1. Authenticated to old Win 10 WVD with MFA (from internet)
2. From inside that session, connected to new Win 11 WVD
3. **No additional MFA prompt**

Why? Once I was on the corporate network (via the first AVD connection), Conditional Access saw subsequent connections as "on corporate network" and didn't require MFA again.

This is Azure AD single sign-on working as designed. If I'd connected directly to the Win 11 workspace from home (bypassing the old one), I would have hit MFA.

## What I Learned

### 1. Disk Size ≠ Partition Size

**Azure creates the disk at the size you specify, but the partition doesn't auto-expand.**

You must manually extend the partition in Disk Management. This is standard Windows behavior, but it catches people off guard because cloud VMs "should just work."

**Pro tip:** Check `Get-Volume` immediately after deployment to verify usable space matches expectations.

### 2. Domain Join is Critical

**The "Specify domain or unit" setting is easy to miss** in the portal during VM creation.

Without it:
- VM deploys successfully
- But not domain joined
- AVD agent doesn't install
- Not registered to host pool
- You have to delete and start over

**Always verify domain join configuration before clicking "Create".**

### 3. Two Different Accounts for AVD

**On corporate network:** Use on-premises AD account (`user@domain.local`)

**From internet:** Use Azure AD account (`user@company.com`)

These are separate identities. You need both:
- On-prem AD account for domain-joined VM access
- Azure AD account for AVD workspace discovery and authentication

### 4. Personal Pools Need Two Assignments

**Application group assignment:** Can you see the workspace?

**VM assignment:** Which VM do you get?

Both are required for Personal pools with Direct assignment. Pooled hosts only need app group assignment.

### 5. New Pool Strategy is Worth It

**Running both pools in parallel gave me:**
- Safety net (old VM still works)
- Time to test thoroughly
- Zero pressure ("I can always go back")
- Validation period before committing

The cost of running both (~$50/month extra for a few weeks) was worth the peace of mind.

## The Results

### Before (Win 10)
- 127GB disk
- 18GB free (85% full)
- Constant "low disk space" anxiety
- Had to clean up temp files weekly

### After (Win 11)
- 512GB disk
- 450GB free (12% used)
- Breathing room for years
- No more space management

### Performance
**Disk I/O feels faster** with Standard SSD at 512GB (P20 tier) vs 127GB (P10 tier). Higher IOPS and throughput at the larger size.

**Windows 11 differences noticed:**
- Slightly cleaner UI (centered taskbar, rounded corners)
- Same performance on identical VM size
- All tools work exactly the same
- Teams is still Teams (unfortunately)

## Cost Implications

**VM cost:** ~$350/month (Standard D8s v5)

**Disk cost:**
- 127GB Standard SSD (P10): ~$10/month
- 512GB Standard SSD (P20): ~$30/month
- **Delta: $20/month**

**The disk upgrade is <10% of total VM cost.** For an architect who lives in this environment daily, $20/month for 4x the space is a no-brainer.

## Would I Do Anything Differently?

**Not really.** The migration went smoothly once I:
1. Configured domain join correctly
2. Extended the disk partition
3. Set up both user assignments

**The new pool strategy was the right call.** Zero downtime, ability to test thoroughly, and easy rollback if needed.

**Only regret:** I didn't migrate sooner. I suffered with 18GB free for months before finally doing this.

## What's Next

**For me:**
- Test everything for a week
- Verify FSLogix profile consistency
- Confirm all apps work as expected
- Decommission old Win 10 pool after validation period

**For my team:**
- Document this process for other users
- Create standardized VM deployment template
- Build automation for app installation
- Plan broader Win 11 migration rollout

**For the Synovus-Pinnacle merger:**
- This migration pattern will scale to 300+ users
- Win 11 ready when Pinnacle users need AVD access
- Proven playbook for Personal pool migrations
- Documented all the gotchas

## The Bottom Line

**Migrating my own AVD to Windows 11 with 512GB disk space took about 3 hours of actual work:**
- 30 minutes: Create pool and deploy VM
- 30 minutes: Fix disk partition issue
- 30 minutes: Install apps
- 30 minutes: Configure authentication and assignments
- 60 minutes: Testing and validation

**Total cost: ~$20/month more for the larger disk**

**Result: 4x more disk space, modern OS, clean slate, and documented migration process for the team.**

If you're running out of space on your AVD, don't suffer. Migrate to a new pool with proper disk sizing. The new pool strategy gives you a safety net and the ability to test thoroughly before committing.

Your future self (and your team) will thank you.

---

*This post documents the actual migration of my production AVD environment at Synovus. All commands, scripts, and gotchas are from real experience. Your mileage may vary, but the patterns should apply to any Personal AVD pool migration.*
