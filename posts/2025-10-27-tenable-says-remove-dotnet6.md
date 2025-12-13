---
title: "Security Found .NET 6 on 47 VMs. Now I'm Supposed to Remove It. Here's Why That's Impossible."
date: 2025-10-27
summary: "Tenable finds a vulnerability. Security creates a ticket. Change management wants approval. App teams say not my problem. Infrastructure doesn't own the apps. Welcome to the operational reality nobody talks about."
tags: ["azure", "Security", "operations", "Change Management"]
cover: "/static/images/hero/azure-support-ticket.svg"
hub: governance
---
## The Ticket


This guide is part of our [Azure Governance hub](/hub/governance/) covering policy enforcement, compliance frameworks, and enterprise controls.

```
Subject: Azure Admin - Remove .NET 6.0 from 47 Virtual Machines
Priority: High
Due Date: 30 days from scan date
Affected Resources: 47 VMs across 44 subscriptions

Description:
Tenable vulnerability scan identified .NET 6.0 installed on 47 Azure VMs.
.NET 6 reached end-of-support November 12, 2024.

Action Required:
Remove .NET 6.0 from all affected virtual machines.
Update to .NET 8 or later if applications require .NET runtime.

Assigned To: Azure Infrastructure Team
```

And just like that, you're responsible for removing software from 47 production servers across your entire Azure estate.

**Without knowing:**
- What applications run on these VMs
- Who owns those applications  
- Whether removing .NET 6 will break anything
- Whether you have permission to touch these VMs
- How to even DO this at scale

Welcome to enterprise cloud operations.

---

## The Scale Problem

Let's be clear: **You cannot manually RDP into 47 VMs.**

That's 10+ hours of:
1. Finding each VM in the portal (across 44 subscriptions)
2. Connecting via Bastion or RDP
3. Opening Programs and Features
4. Uninstalling .NET 6
5. Rebooting
6. Verifying removal
7. Documenting completion

And that assumes:
- You have local admin rights on all 47 VMs (you probably don't)
- The uninstall doesn't break anything (it will)
- Nobody complains when their app stops working (they will)

So let's try automation.

---

## The Automation Reality

### Step 1: Find All .NET 6 Installations

First, let's use Azure Resource Graph to find which VMs Tenable is complaining about:

```kql
resources
| where type == "microsoft.compute/virtualmachines"
| extend vmName = name
| extend subscription = subscriptionId
| extend resourceGroup = resourceGroup
| project vmName, subscription, resourceGroup, location
```

But wait—**Resource Graph doesn't tell you what SOFTWARE is installed.**

Tenable knows. Azure doesn't.

You need to either:
1. Pull the Tenable report and cross-reference VM names
2. Use Azure Update Manager to inventory installed software
3. Query each VM individually with PowerShell

Let's try option 3:

```powershell
# Connect to Azure
Connect-AzAccount

# Get all VMs across all subscriptions
$subscriptions = Get-AzSubscription
$results = @()

foreach ($sub in $subscriptions) {
    Set-AzContext -SubscriptionId $sub.Id
    
    $vms = Get-AzVM
    
    foreach ($vm in $vms) {
        Write-Host "Checking $($vm.Name)..."
        
        # Run command to check for .NET 6
        $result = Invoke-AzVMRunCommand `
            -ResourceGroupName $vm.ResourceGroupName `
            -VMName $vm.Name `
            -CommandId 'RunPowerShellScript' `
            -ScriptString @'
                $dotnetVersions = Get-ChildItem "C:\Program Files\dotnet\shared\Microsoft.NETCore.App" -Directory -ErrorAction SilentlyContinue
                $dotnet6 = $dotnetVersions | Where-Object { $_.Name -like "6.*" }
                
                if ($dotnet6) {
                    Write-Output "FOUND: $($dotnet6.Name)"
                } else {
                    Write-Output "NOT FOUND"
                }
'@
        
        $output = $result.Value[0].Message
        
        if ($output -like "*FOUND*") {
            $results += [PSCustomObject]@{
                VMName = $vm.Name
                ResourceGroup = $vm.ResourceGroupName
                Subscription = $sub.Name
                DotNetVersion = $output.Replace("FOUND: ", "")
            }
        }
    }
}

# Export results
$results | Export-Csv "dotnet6-inventory.csv" -NoTypeInformation
```

**Time to run this across 47 VMs:** 30-45 minutes (Invoke-AzVMRunCommand is SLOW)

**Results:** A CSV with confirmed .NET 6 installations.

---

### Step 2: Remove .NET 6 at Scale

Now let's try to REMOVE it:

```powershell
# Import the inventory
$vmsToFix = Import-Csv "dotnet6-inventory.csv"

foreach ($vm in $vmsToFix) {
    Write-Host "Removing .NET 6 from $($vm.VMName)..."
    
    Set-AzContext -SubscriptionId (Get-AzSubscription -SubscriptionName $vm.Subscription).Id
    
    $result = Invoke-AzVMRunCommand `
        -ResourceGroupName $vm.ResourceGroup `
        -VMName $vm.VMName `
        -CommandId 'RunPowerShellScript' `
        -ScriptString @'
            # Find .NET 6 uninstaller
            $uninstallKeys = Get-ChildItem "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
            $dotnet6 = $uninstallKeys | ForEach-Object {
                Get-ItemProperty $_.PSPath
            } | Where-Object {
                $_.DisplayName -like "*Microsoft .NET Runtime - 6.*" -or
                $_.DisplayName -like "*Microsoft ASP.NET Core 6.*"
            }
            
            foreach ($app in $dotnet6) {
                Write-Output "Uninstalling: $($app.DisplayName)"
                
                $uninstallString = $app.UninstallString
                if ($uninstallString) {
                    # Execute uninstall (silent mode)
                    Start-Process $uninstallString -ArgumentList "/quiet /norestart" -Wait
                }
            }
            
            Write-Output "Uninstall complete."
'@
    
    Write-Output $result.Value[0].Message
}
```

---

## Here's Where It Falls Apart

### Problem 1: You Don't Know What Will Break

Removing .NET 6 might:
- Break a .NET 6 application (obviously)
- Break a .NET 8 app that ALSO has .NET 6 binaries
- Break Windows services that depend on .NET 6
- Break monitoring agents, backup software, or management tools

**You don't know** because **you don't own these applications.**

### Problem 2: Change Management

Your change management process requires:
1. **Change request submission** (CAB approval needed)
2. **Business owner approval** (who is that?)
3. **Rollback plan** (how do you rollback 47 VMs?)
4. **Testing plan** (test what? in which environments?)

**The question nobody answers:**
- Do I submit ONE change request for 47 VMs?
- Or 47 separate change requests?

If one change request:
- CAB says "too broad, break it down"

If 47 change requests:
- You spend 20 hours writing change requests instead of fixing the problem

### Problem 3: Application Ownership

You're the **Azure Infrastructure Team**.

You manage:
- Virtual machine provisioning
- Networking and firewalls
- Backup and disaster recovery
- Monitoring and alerting

You **do not manage:**
- Application code
- Application dependencies
- Application testing
- Application deployment

**But the security ticket is assigned to you.**

Why? Because:
- Security found it on Azure VMs
- Azure VMs are owned by "Azure team"
- Therefore, Azure team fixes it

This logic makes sense to **nobody who actually does this work.**

---

## The Missing Process

Here's what SHOULD exist but doesn't:

### 1. RACI Matrix for Security Remediation

| Task | Responsible | Accountable | Consulted | Informed |
|------|-------------|-------------|-----------|----------|
| Vulnerability Scanning | Security Team | CISO | Infrastructure | All |
| Ticket Creation | Security Team | Security Manager | Infrastructure | App Teams |
| **Software Removal (OS-level)** | **Infrastructure** | **Infrastructure Manager** | **App Teams** | **Security** |
| **Software Removal (App-level)** | **App Teams** | **App Owner** | **Infrastructure** | **Security** |
| Testing After Removal | App Teams | App Owner | Infrastructure | Security |
| Change Approval | App Owner | CAB | Infrastructure | Security |
| Rollback Execution | Infrastructure | Infrastructure Manager | App Teams | Security |

**The problem:** Your organization doesn't have this defined.

So the ticket lands on Infrastructure by default.

### 2. Application Inventory (CMDB)

You need to know:
- Which VMs run which applications
- Who owns those applications
- Contact info for app owners
- Testing environments for each app

**The reality:** This data doesn't exist, or it's in a SharePoint that hasn't been updated since 2019.

### 3. Patching vs Remediation SLA

Your organization probably has:
- **OS patching SLA:** 30 days for critical, 60 days for high
- **Security vulnerability SLA:** 30 days from scan date

But NO definition of:
- Who does the remediation work
- How remediation is prioritized against other work
- What "remediation" means for third-party software

---

## The Real Answer

Here's what you SHOULD do (but probably can't):

### 1. Reassign the Ticket

```
To: Security Team Manager
CC: Application Services Director

Subject: Re-assignment - .NET 6 Removal Ticket

This ticket has been assigned to Azure Infrastructure, but the work
described is APPLICATION-level remediation, not infrastructure patching.

Azure Infrastructure manages:
- VM provisioning and decommissioning
- OS patching (Windows Update)
- Backup and DR

Azure Infrastructure does NOT manage:
- Application dependencies (including .NET runtime)
- Application code deployment
- Application testing

Request:
1. Identify application owners for each affected VM (see attached list)
2. Re-assign ticket to application teams
3. Infrastructure will provide VM access and change management support

Alternatively:
- Define a RACI matrix for security remediation work
- We'll follow the defined process going forward
```

### 2. Build the Missing Inventory

If they won't reassign it, at least BUILD the data you need:

```powershell
# Create application inventory from Azure tags
$inventory = @()

foreach ($sub in $subscriptions) {
    Set-AzContext -SubscriptionId $sub.Id
    $vms = Get-AzVM
    
    foreach ($vm in $vms) {
        $tags = (Get-AzResource -ResourceId $vm.Id).Tags
        
        $inventory += [PSCustomObject]@{
            VMName = $vm.Name
            Subscription = $sub.Name
            ResourceGroup = $vm.ResourceGroupName
            ApplicationName = $tags['Application']
            ApplicationOwner = $tags['Owner']
            Environment = $tags['Environment']
            CostCenter = $tags['CostCenter']
        }
    }
}

$inventory | Export-Csv "vm-application-inventory.csv" -NoTypeInformation
```

**Problem:** Your tags are probably wrong, incomplete, or missing.

See: [Azure Resource Tags Are Wrong and Nobody Cares](/blog/2025-09-xx-azure-tags-are-wrong)

### 3. Have the Hard Conversation

This requires a meeting with:
- Security leadership
- Application services leadership  
- Your manager

Agenda:
1. **Operational boundaries:** Who owns application-level remediation?
2. **Process definition:** How do security findings become work assignments?
3. **RACI creation:** Let's define this once, not per-ticket

**The outcome you want:**
- Clear ownership boundaries
- Security findings routed to correct teams
- Change management process that scales

**The outcome you'll probably get:**
- "We'll discuss this later"
- Ticket stays assigned to you
- You remove .NET 6 from 47 VMs manually

---

## What I Actually Did

Here's what I do in practice:

### 1. Document the Scope

```markdown
# .NET 6 Removal - Scope Documentation

## Total VMs: 47
## Subscriptions: 44
## Estimated Effort:
- Inventory: 4 hours
- Change requests: 8 hours  
- Execution: 12 hours
- Testing support: 16 hours (with app teams)
- **Total: 40 hours (1 full work week)**

## Risks:
1. Application breakage (unknown impact)
2. Rollback complexity (no automated rollback)
3. Resource contention (only 2 Azure admins for 44 subscriptions)

## Dependencies:
1. Application owner identification (Security team)
2. Application owner approval (Change management)
3. Testing environment access (App teams)
```

### 2. Push Back with Data

```
To: Security Team Manager
CC: My Manager

Subject: .NET 6 Removal - Resource Requirements

This work requires 40 hours of dedicated effort across a 2-week window.

Current Azure team capacity:
- Pinnacle merger work: 60% of capacity
- BAU operations: 30% of capacity  
- Available: 10% of capacity

Request:
1. Approve 40-hour project allocation
2. Pause other non-critical work
3. Provide application owner contacts

OR

Re-assign to application teams with infrastructure support role defined.
```

### 3. Do the Minimum Viable Remediation

If I can't reassign it:

1. **Inventory:** Use the PowerShell script above
2. **Categorize:** Group VMs by subscription and tag data
3. **Find owners:** Use tags, ask around, check with app teams
4. **Create ONE change request** per subscription (not per VM)
5. **Get app owner approval** (email trail for CYA)
6. **Remove .NET 6** with monitoring enabled
7. **Document failures** and escalate to app teams

**Result:** Some VMs get fixed, some break, some never get approval.

The security ticket closes after 60 days whether the work is done or not.

---

## The Uncomfortable Truth

**Security scanners CREATE work, but organizations don't define WHO does that work.**

Tenable/Qualys/Rapid7 will find:
- Outdated software
- Missing patches  
- Configuration drift
- Certificate expirations

And then someone has to:
- Investigate each finding
- Determine risk and priority
- Plan remediation
- Execute changes
- Verify results

**That work has to be ASSIGNED to someone with:**
- Appropriate access
- Domain knowledge
- Time to do the work
- Authority to make changes

In mature organizations, this is **defined in a RACI matrix**.

In your organization, it's assigned to whoever touches the asset last.

And if you're the Azure admin, that's you.

---

## What Actually Needs to Happen

1. **Define operational boundaries BEFORE scanning.**
   - What findings go to infrastructure?
   - What findings go to application teams?
   - What findings require collaboration?

2. **Build an accurate CMDB.**
   - Azure tags with application owner
   - CMDB entries for every VM
   - Contact information that's actually current

3. **Create a security remediation RACI.**
   - Who investigates findings?
   - Who plans remediation?
   - Who executes changes?
   - Who verifies results?

4. **Staff appropriately.**
   - Security remediation is WORK
   - It requires time, tools, and expertise
   - You can't bolt it onto existing full-time workloads

5. **Integrate with change management.**
   - One change request per application (not per VM)
   - Application owner approval is required
   - Infrastructure provides support, not ownership

---

## The Post-Mortem

Six weeks after the ticket was created:

- **VMs remediated:** 23 of 47
- **Applications broken:** 4
- **Rollbacks required:** 4  
- **App owner approvals received:** 8 of 47
- **Tickets re-assigned to app teams:** 15
- **Tickets closed due to timeout:** 9

**Total time spent:** 52 hours (more than the estimate)

**Lessons learned:**
1. We still don't have a RACI for security remediation
2. We still don't have an accurate CMDB
3. The next Tenable scan will create 40+ more tickets

And the cycle continues.

---

## The Real Solution

Stop assigning infrastructure-level tickets for application-level problems.

**Create a process:**

1. **Security findings route through a triage team**
   - Is this OS-level? → Infrastructure
   - Is this app-level? → Application teams
   - Is this config? → Security team

2. **Tickets include required context:**
   - Application name
   - Application owner (with contact info)
   - Testing requirements
   - Rollback plan

3. **Infrastructure provides support, not ownership:**
   - "We'll execute the changes after app owner approval"
   - Not: "We'll figure out who owns this and do everything"

4. **Leadership backs this up:**
   - When security escalates
   - When deadlines slip
   - When someone tries to reassign the work back to you

---

## Until Then

You'll keep getting tickets that say:

```
Subject: Azure Admin - Remove [software] from [number] VMs
Due Date: 30 days
Assigned To: You
```

And you'll keep fighting the same battle:

- This isn't my job
- I don't have context
- I don't own these applications
- We don't have a process for this

Welcome to enterprise cloud operations.

**Next time someone asks "why is cloud so hard?"**

Show them this post.

---

## Resources

**PowerShell Scripts:**
- [Find .NET installations across Azure VMs](https://github.com/azure-noob/scripts/dotnet-inventory)
- [Remove software at scale with RunCommand](https://github.com/azure-noob/scripts/vm-software-removal)

**Process Templates:**
- [Security Remediation RACI Matrix](https://github.com/azure-noob/templates/security-raci)
- [Application Inventory Template](https://github.com/azure-noob/templates/app-inventory)

**Related Posts:**
- [IT Roles & Responsibilities Matrix](/blog/2025-09-xx-it-roles-raci)
- [Azure Resource Tags Are Wrong and Nobody Cares](/blog/2025-09-xx-azure-tags)
- [Your CMDB Is Wrong (And Cloud Migration Will Prove It)](/blog/2025-10-xx-cmdb-is-wrong)

---

*Have a security remediation nightmare story? Email me at [email] or drop a comment below. We're all fighting this battle.*
