---
title: "Why Your Automation Fails on Fresh Azure VMs (And How I Fixed It)"
date: 2025-09-29
summary: "Three hours debugging certificate errors on fresh marketplace VMs. The culprit? Microsoft's own infrastructure serving outdated dependencies."
tags: ["Azure", "PowerShell", "Automation", "DevOps", "Troubleshooting"]
cover: "/static/images/hero/azure-automation-debugging.png"
---

I built a PowerShell script to automate Azure admin workstation setup. Tested on my VM - worked perfectly. Deployed a fresh Windows 11 Enterprise N from Azure marketplace to document the process - total failure. Every package install failed with cryptic certificate errors.

Three hours later, I discovered why Microsoft's package manager doesn't work on Microsoft's marketplace images.

## The Certificate Validation Error

Fresh Windows 11 Enterprise N VMs fail every winget package install:

```
0x8a15005e : The server certificate did not match any of the expected values.
```

PowerShell 7? Failed. VS Code? Failed. Git, Python, Azure CLI - all failed.

## The Debugging Rabbit Hole

**First attempt: Run Windows Update**

Maybe the VM just needs updates? I wrote a script using PSWindowsUpdate module, waited 90 minutes for patches and reboot.

```powershell
Get-AppxPackage -Name "Microsoft.VCLibs.140.00.UWPDesktop" | Select-Object Version
# Version: 14.0.30704.0
```

Still the old version. Windows Update doesn't include framework updates.

**Second attempt: Manual dependency updates**

Winget requires VCLibs.140.00.UWPDesktop version 14.0.33728.0+ to work properly. Downloaded from Microsoft's official URLs:

```powershell
Invoke-WebRequest -Uri "https://aka.ms/Microsoft.VCLibs.x64.14.00.Desktop.appx"
Add-AppxPackage -Path $downloaded
```

Installed version: 14.0.33321.0

Still too old. Microsoft's download URL doesn't provide the version their software requires.

**The dependency trap:**

- Fresh marketplace VMs ship with winget v1.19 (certificate validation broken)
- Updating to winget v1.26 requires App Installer v1.26
- App Installer v1.26 requires VCLibs 14.0.33728.0+
- Microsoft's URLs only provide VCLibs 14.0.33321.0
- Windows Update doesn't include these frameworks

Stuck in a loop with no Microsoft-provided solution.

## The Working Solution: Chocolatey

Chocolatey doesn't depend on AppX frameworks. It just works.

Rewrote the script using Chocolatey instead of winget. Tested on a fresh marketplace VM:

```
14/14 packages installed successfully
0 failures
```

## Deployment Timeline

From Azure Portal to fully configured workstation: **30-60 minutes**

- Deploy Windows 11 VM: 5-10 min
- Download script: 2 min
- Chocolatey installs everything: 20-40 min
- Reboot and verify: 5 min

**What gets installed:**
- Dev tools: PowerShell 7, VS Code, Git, Python, Node.js
- Azure tools: Azure CLI, Storage Explorer, Terraform, Bicep
- Utilities: Windows Terminal, Docker Desktop, Postman, 7-Zip, Notepad++

Plus desktop shortcuts for the key applications.

## Usage

One command on any fresh Azure VM:

```powershell
# Download and run
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/dswann101164/azure-admin-workstation-setup/main/Setup-AzureAdminWorkstation-Chocolatey.ps1" -OutFile "Setup.ps1"

.\Setup.ps1 -NoPrompts
```

Source code and documentation: [github.com/dswann101164/azure-admin-workstation-setup](https://github.com/dswann101164/azure-admin-workstation-setup)

## Key Takeaways

**Test on actual fresh VMs.** Your dev machine that's been running for weeks has accumulated updates that fresh marketplace images don't have.

**Marketplace images are outdated.** Windows 11 Enterprise N ships with 9-month-old package managers and frameworks.

**Microsoft's infrastructure has gaps.** Their download URLs serve versions too old for their own software requirements.

**Chocolatey avoids the problem entirely.** No AppX dependencies, no certificate validation issues, no version mismatches.

The irony: Microsoft's package manager doesn't work on Microsoft's marketplace images because Microsoft's download infrastructure is outdated.

Save yourself three hours - use Chocolatey for Azure VM automation.

---

*Tested on Windows 11 Enterprise N (22H2) from Azure Marketplace - September 2025*