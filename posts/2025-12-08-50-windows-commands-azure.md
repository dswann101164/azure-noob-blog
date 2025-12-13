---
title: "50 Windows Commands for Azure VMs (PowerShell + Active Directory)"
date: 2025-12-08
summary: "The essential Windows commands every Azure administrator needs—from PowerShell basics to Active Directory domain join and Group Policy troubleshooting in enterprise environments."
tags: ["azure", "windows", "powershell", "active-directory", "group-policy", "troubleshooting"]
cover: "/static/images/hero/windows-commands-azure.png"
hub: ai
---
Whether you deploy Azure Windows VMs through the Portal, PowerShell, ARM templates, or Terraform—eventually you'll RDP in to troubleshoot something. The deployment succeeded, the Portal shows healthy, but users can't authenticate with domain credentials, Group Policy won't apply, or the domain trust is broken.


This guide is part of our [AI-Assisted Azure Operations hub](/hub/ai/) exploring how AI tools transform cloud administration and productivity workflows.

This is when you need actual Windows commands.

This guide covers the 50 PowerShell and CMD commands that bridge the gap between successful deployment and operational readiness. These are the commands I use daily managing Windows Server infrastructure in a regulated banking environment.

## Who This is For

- Azure administrators managing Windows Server VMs
- Enterprise environments with Active Directory requirements
- Anyone troubleshooting Group Policy, domain trust, or authentication issues
- Operations teams bridging traditional infrastructure and Azure

## Table of Contents

1. [Azure-Specific Basics](#azure-basics)
2. [System Administration](#system-admin)
3. [Active Directory & Domain Join](#active-directory)
4. [Group Policy Troubleshooting](#group-policy)
5. [Networking](#networking)
6. [Disk Operations](#disk-operations)
7. [Security & Event Logs](#security-logs)
8. [Azure PowerShell](#azure-powershell)
9. [Serial Console (SAC)](#serial-console)
10. [Quick Reference](#quick-reference)

---

## <a name="azure-basics"></a>Part 1: Azure-Specific Basics

### Azure VM Agent (Windows)

The Azure VM Agent enables extensions, monitoring, and automation. When Custom Script Extensions fail or Azure Automation won't work, start here:

```powershell
# Check VM Agent service status
Get-Service WindowsAzureGuestAgent

# View VM Agent logs
Get-Content "C:\WindowsAzure\Logs\WaAppAgent.log" -Tail 50

# Check which extensions are installed
Get-ChildItem "C:\Packages\Plugins" | Select-Object Name, LastWriteTime

# View specific extension status
Get-ChildItem "C:\Packages\Plugins\Microsoft.Compute.CustomScriptExtension"

# Check extension logs
Get-Content "C:\WindowsAzure\Logs\Plugins\Microsoft.Compute.CustomScriptExtension\*\CommandExecution.log"
```

**Common issue:** "Custom Script Extension shows succeeded in Portal but script didn't actually run."

Check the actual execution logs:

```powershell
# View extension execution output
Get-Content "C:\Packages\Plugins\Microsoft.Compute.CustomScriptExtension\*\Status\*.status" | ConvertFrom-Json | Select-Object -ExpandProperty status

# Check for errors
Get-Content "C:\Packages\Plugins\Microsoft.Compute.CustomScriptExtension\*\RuntimeSettings\*.settings" | ConvertFrom-Json
```

### Azure Instance Metadata Service (IMDS)

Query VM metadata and managed identity tokens:

```powershell
# Get VM metadata
$metadata = Invoke-RestMethod -Headers @{"Metadata"="true"} -Uri "http://169.254.169.254/metadata/instance?api-version=2021-02-01"
$metadata | ConvertTo-Json -Depth 10

# Get specific values
$metadata.compute.vmId
$metadata.compute.location
$metadata.compute.resourceGroupName

# Get managed identity token
$token = Invoke-RestMethod -Headers @{"Metadata"="true"} -Uri "http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://management.azure.com/"
$token.access_token

# Check if VM has managed identity
$metadata.compute.identity
```

### Run Command Execution Status

When you deploy scripts via Azure Run Command:

```powershell
# List all Run Commands on this VM (requires Az PowerShell module)
Get-AzVMRunCommand -ResourceGroupName "myRG" -VMName "myVM"

# View Run Command output
Get-AzVMRunCommand -ResourceGroupName "myRG" -VMName "myVM" -RunCommandName "myCommand" -Expand instanceView

# Check Run Command logs locally
Get-ChildItem "C:\Packages\Plugins\Microsoft.CPlat.Core.RunCommandWindows" -Recurse
```

> **💼 Enterprise Callout: Active Directory Domain Join**
> 
> If you need to join Azure VMs to Active Directory for centralized authentication:
> ```powershell
> # Quick test if domain join succeeded
> Test-ComputerSecureChannel
> Get-ADComputer $env:COMPUTERNAME
> ```
> 
> [Jump to full Active Directory guide →](#active-directory)

---

## <a name="system-admin"></a>Part 2: System Administration

### Process & Performance Monitoring

```powershell
# List running processes sorted by CPU
Get-Process | Sort-Object CPU -Descending | Select-Object -First 10

# List processes by memory usage
Get-Process | Sort-Object WS -Descending | Select-Object -First 10 Name, @{N='Memory(MB)';E={[math]::Round($_.WS/1MB,2)}}

# Monitor CPU usage
Get-Counter '\Processor(_Total)\% Processor Time' -SampleInterval 2 -MaxSamples 5

# Check memory usage
Get-CimInstance Win32_OperatingSystem | Select-Object @{N='TotalMemory(GB)';E={[math]::Round($_.TotalVisibleMemorySize/1MB,2)}}, @{N='FreeMemory(GB)';E={[math]::Round($_.FreePhysicalMemory/1MB,2)}}

# System uptime
(Get-Date) - (Get-CimInstance Win32_OperatingSystem).LastBootUpTime
```

### Service Management

```powershell
# Check service status
Get-Service | Where-Object {$_.Status -eq "Running"} | Select-Object Name, DisplayName, StartType

# Check specific services
Get-Service -Name "NTDS", "DNS", "W32Time", "Netlogon"

# Start/stop/restart service
Start-Service -Name "Spooler"
Stop-Service -Name "Spooler"
Restart-Service -Name "Spooler"

# Set service startup type
Set-Service -Name "Spooler" -StartupType Automatic

# Check service dependencies
Get-Service -Name "NTDS" -DependentServices
Get-Service -Name "NTDS" -RequiredServices
```

### Event Log Monitoring

```powershell
# View recent system errors
Get-EventLog -LogName System -EntryType Error -Newest 20

# View application errors
Get-EventLog -LogName Application -EntryType Error -Newest 20

# Security log - failed logon attempts
Get-EventLog -LogName Security -InstanceId 4625 -Newest 50

# Security log - successful logons
Get-EventLog -LogName Security -InstanceId 4624 -Newest 50

# Filter by time
$startTime = (Get-Date).AddHours(-1)
Get-WinEvent -FilterHashtable @{LogName='System'; Level=2; StartTime=$startTime}

# Search for specific text in event logs
Get-EventLog -LogName System | Where-Object {$_.Message -like "*failed*"}

# Export events to CSV
Get-EventLog -LogName System -EntryType Error -Newest 100 | Export-Csv C:\Temp\SystemErrors.csv -NoTypeInformation
```

### User & Permission Management

```powershell
# List local users
Get-LocalUser

# Create local user
New-LocalUser -Name "serviceaccount" -Password (ConvertTo-SecureString "P@ssw0rd" -AsPlainText -Force) -FullName "Service Account"

# Add user to local administrators
Add-LocalGroupMember -Group "Administrators" -Member "DOMAIN\AdminUser"

# List members of local group
Get-LocalGroupMember -Group "Administrators"

# Check current user
whoami
whoami /groups

# Check user's group memberships
net user username /domain
```

---

## <a name="active-directory"></a>Part 3: Active Directory & Domain Join

> **Note:** This section covers traditional Active Directory Domain Controllers, not Azure AD Domain Services. Most enterprises run traditional AD in Azure for hybrid scenarios.

### Prerequisites for Domain Join

Before joining a Windows VM to Active Directory:

1. **DNS must point to domain controller** (not Azure DNS or 8.8.8.8)
2. **Network connectivity to DC** (ports 53, 88, 135, 389, 445, 636)
3. **Time sync within 5 minutes** (Kerberos requirement)
4. **Account with domain join privileges**

### Required Ports

| Port | Protocol | Service | Required |
|------|----------|---------|----------|
| 53 | TCP/UDP | DNS | Yes |
| 88 | TCP/UDP | Kerberos | Yes |
| 135 | TCP | RPC Endpoint Mapper | Yes |
| 389 | TCP/UDP | LDAP | Yes |
| 445 | TCP | SMB/CIFS | Yes |
| 464 | TCP/UDP | Kerberos Password Change | Yes |
| 636 | TCP | LDAPS | Recommended |
| 3268 | TCP | Global Catalog | Recommended |
| 3269 | TCP | Global Catalog SSL | Recommended |

### Domain Join Process

#### Step 1: Configure DNS

**Critical:** VM must use domain controller as DNS server.

```powershell
# Check current DNS configuration
Get-DnsClientServerAddress

# Set DNS to domain controller (temporary - testing only)
Set-DnsClientServerAddress -InterfaceIndex (Get-NetAdapter).ifIndex -ServerAddresses "10.0.0.4","10.0.0.5"

# Verify DNS resolution
Resolve-DnsName DC01.CONTOSO.COM
Resolve-DnsName CONTOSO.COM
nslookup _ldap._tcp.dc._msdcs.CONTOSO.COM

# Test DNS connectivity
Test-NetConnection DC01.CONTOSO.COM -Port 53
```

**Note:** For permanent DNS changes in Azure, configure at the VNet level in Azure Portal, not on the VM itself.

#### Step 2: Configure Time Sync

**This is critical.** Kerberos authentication fails if time difference exceeds 5 minutes.

```powershell
# Check time sync status
w32tm /query /status
w32tm /query /source

# Configure time sync to domain controller
w32tm /config /manualpeerlist:"DC01.CONTOSO.COM" /syncfromflags:manual /reliable:yes /update

# Force time sync
w32tm /resync /force

# Verify time difference
w32tm /stripchart /computer:DC01.CONTOSO.COM /samples:5 /dataonly
```

#### Step 3: Test Connectivity to Domain Controller

```powershell
# Ping domain controller
Test-NetConnection DC01.CONTOSO.COM

# Test required ports
Test-NetConnection DC01.CONTOSO.COM -Port 53   # DNS
Test-NetConnection DC01.CONTOSO.COM -Port 88   # Kerberos
Test-NetConnection DC01.CONTOSO.COM -Port 389  # LDAP
Test-NetConnection DC01.CONTOSO.COM -Port 445  # SMB
Test-NetConnection DC01.CONTOSO.COM -Port 636  # LDAPS

# Test LDAP connectivity
nltest /dsgetdc:CONTOSO.COM

# Check domain controller availability
nltest /dclist:CONTOSO.COM
```

#### Step 4: Join Domain

```powershell
# Join domain (interactive - prompts for credentials)
Add-Computer -DomainName CONTOSO.COM -Restart

# Join domain with specific credentials
$credential = Get-Credential
Add-Computer -DomainName CONTOSO.COM -Credential $credential -Restart

# Join domain with specific OU
Add-Computer -DomainName CONTOSO.COM -OUPath "OU=Servers,OU=Azure,DC=CONTOSO,DC=COM" -Credential $credential -Restart

# Join domain without restart
Add-Computer -DomainName CONTOSO.COM -Credential $credential
```

#### Step 5: Verify Domain Join

```powershell
# Check computer's domain
(Get-WmiObject Win32_ComputerSystem).Domain

# Test secure channel to domain
Test-ComputerSecureChannel

# Verify computer account in AD
Get-ADComputer $env:COMPUTERNAME

# Check domain controller connection
nltest /sc_query:CONTOSO.COM

# List domain controllers
nltest /dclist:CONTOSO.COM
```

### Troubleshooting Domain Join

#### Test Secure Channel

```powershell
# Test domain trust
Test-ComputerSecureChannel

# Repair broken trust
Test-ComputerSecureChannel -Repair -Credential (Get-Credential)

# Force password reset for computer account
Reset-ComputerMachinePassword -Credential (Get-Credential)
```

#### Domain Join Errors

**Error: "The specified domain either does not exist or could not be contacted"**

```powershell
# Check DNS configuration
Get-DnsClientServerAddress
Resolve-DnsName CONTOSO.COM
nslookup _ldap._tcp.dc._msdcs.CONTOSO.COM

# Test DC connectivity
Test-NetConnection DC01.CONTOSO.COM -Port 389
nltest /dsgetdc:CONTOSO.COM
```

**Error: "The trust relationship between this workstation and the primary domain failed"**

```powershell
# Check secure channel
Test-ComputerSecureChannel

# Repair trust
Test-ComputerSecureChannel -Repair -Credential (Get-Credential)

# If repair fails, rejoin domain
Remove-Computer -UnjoinDomainCredential (Get-Credential) -WorkgroupName WORKGROUP -Restart
# After restart:
Add-Computer -DomainName CONTOSO.COM -Credential (Get-Credential) -Restart
```

**Error: "The clock skew is too great"**

```powershell
# Check time on local machine
Get-Date

# Check time on DC (run on DC or use WMI)
w32tm /stripchart /computer:DC01.CONTOSO.COM /samples:1 /dataonly

# Sync time immediately
w32tm /resync /force

# Configure continuous sync
w32tm /config /manualpeerlist:"DC01.CONTOSO.COM" /syncfromflags:manual /reliable:yes /update
```

### Active Directory Queries

```powershell
# Import AD module (if not already loaded)
Import-Module ActiveDirectory

# Find computer in AD
Get-ADComputer $env:COMPUTERNAME -Properties *

# Find user account
Get-ADUser -Filter {SamAccountName -eq "john.doe"} -Properties *

# List all computers in specific OU
Get-ADComputer -Filter * -SearchBase "OU=Servers,OU=Azure,DC=CONTOSO,DC=COM"

# List all domain controllers
Get-ADDomainController -Filter *

# Check AD replication status
Get-ADReplicationFailure -Scope Domain

# Find all domain admins
Get-ADGroupMember "Domain Admins"
```

---

## <a name="group-policy"></a>Part 4: Group Policy Troubleshooting

Group Policy is critical in regulated environments. When GP won't apply to Azure VMs, use these commands:

### Force Group Policy Update

```powershell
# Force GP update
gpupdate /force

# Force GP update with logging
gpupdate /force /wait:0

# Update computer policy only
gpupdate /target:computer /force

# Update user policy only
gpupdate /target:user /force
```

### Check Group Policy Results

```powershell
# Show currently applied policies (summary)
gpresult /r

# Show detailed results
gpresult /v

# Generate HTML report
gpresult /h C:\Temp\GPReport.html

# Show only computer policies
gpresult /r /scope:computer

# Show only user policies
gpresult /r /scope:user
```

### PowerShell Group Policy Commands

```powershell
# Get Resultant Set of Policy
Get-GPResultantSetOfPolicy -ReportType Html -Path C:\Temp\RSoP.html

# List all GPOs in domain
Get-GPO -All | Select-Object DisplayName, GpoStatus, ModificationTime

# Check specific GPO
Get-GPO -Name "Azure VM Security Policy"

# Find GPOs linked to specific OU
Get-GPInheritance -Target "OU=Servers,OU=Azure,DC=CONTOSO,DC=COM"

# Test if GPO applies to computer
Get-GPOReport -Name "Azure VM Security Policy" -ReportType Html -Path C:\Temp\GPO.html
```

### Group Policy Event Logs

```powershell
# Check GP application events
Get-EventLog -LogName System -Source "Microsoft-Windows-GroupPolicy" -Newest 50

# Filter for errors only
Get-EventLog -LogName System -Source "Microsoft-Windows-GroupPolicy" -EntryType Error -Newest 20

# Check GP processing time
Get-WinEvent -FilterHashtable @{LogName='System'; ProviderName='Microsoft-Windows-GroupPolicy'} -MaxEvents 10

# Search for specific GP issues
Get-EventLog -LogName System | Where-Object {$_.Message -like "*Group Policy*" -and $_.EntryType -eq "Error"}
```

### Common Group Policy Issues

**Issue: "Group Policy not applying to Azure VM"**

```powershell
# Check domain membership
(Get-WmiObject Win32_ComputerSystem).Domain

# Test secure channel
Test-ComputerSecureChannel

# Check DNS (must point to DC)
Get-DnsClientServerAddress

# Test DC connectivity
Test-NetConnection DC01.CONTOSO.COM -Port 389

# Force GP refresh
gpupdate /force

# Check if computer is in correct OU
Get-ADComputer $env:COMPUTERNAME | Select-Object DistinguishedName
```

**Issue: "GP applies on-premises but not in Azure"**

```powershell
# Check site assignment (Azure VMs often in "Default-First-Site-Name")
nltest /dsgetsite

# Verify network connectivity to DC
nltest /sc_query:CONTOSO.COM

# Check if WMI filters blocking GPO
Get-GPOReport -Name "PolicyName" -ReportType Xml | Select-String "WmiFilter"

# Check GP event logs for details
Get-EventLog -LogName System -Source "Microsoft-Windows-GroupPolicy" -Newest 20
```

---

## <a name="networking"></a>Part 5: Networking

### Connectivity Testing

```powershell
# Test basic connectivity
Test-NetConnection 8.8.8.8
Test-Connection 8.8.8.8 -Count 4

# Test specific port
Test-NetConnection DC01.CONTOSO.COM -Port 389
Test-NetConnection azure.microsoft.com -Port 443

# Trace route
Test-NetConnection DC01.CONTOSO.COM -TraceRoute

# DNS resolution
Resolve-DnsName DC01.CONTOSO.COM
Resolve-DnsName azure.microsoft.com

# Check DNS configuration
Get-DnsClientServerAddress

# Test DNS server response
nslookup CONTOSO.COM
nslookup -type=SRV _ldap._tcp.dc._msdcs.CONTOSO.COM
```

### Network Configuration

```powershell
# Show network adapters
Get-NetAdapter | Select-Object Name, Status, LinkSpeed, MacAddress

# Show IP configuration
Get-NetIPAddress

# Show routing table
Get-NetRoute

# Show active connections
Get-NetTCPConnection | Where-Object {$_.State -eq "Established"}

# Show listening ports
Get-NetTCPConnection | Where-Object {$_.State -eq "Listen"} | Select-Object LocalPort, LocalAddress

# Legacy ipconfig
ipconfig /all
ipconfig /displaydns
ipconfig /flushdns
```

### Firewall Management

```powershell
# Check firewall status
Get-NetFirewallProfile | Select-Object Name, Enabled

# List all firewall rules
Get-NetFirewallRule | Where-Object {$_.Enabled -eq $true}

# Check specific rule
Get-NetFirewallRule -DisplayName "Remote Desktop*"

# Create new firewall rule
New-NetFirewallRule -DisplayName "Allow RDP" -Direction Inbound -Protocol TCP -LocalPort 3389 -Action Allow

# Enable/disable firewall
Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True

# Disable firewall temporarily (testing only!)
Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled False
```

### Network Troubleshooting

```powershell
# Test port connectivity (legacy)
telnet DC01.CONTOSO.COM 389

# Modern port test
Test-NetConnection DC01.CONTOSO.COM -Port 389 -InformationLevel Detailed

# Check ARP table
Get-NetNeighbor

# Check DNS cache
Get-DnsClientCache

# Check hosts file
Get-Content C:\Windows\System32\drivers\etc\hosts

# Network statistics
netstat -ano
netstat -s
```

---

## <a name="disk-operations"></a>Part 6: Disk Operations

When you attach a managed disk via Portal or PowerShell, it shows as "attached" but isn't initialized or formatted.

### Check Available Disks

```powershell
# List all disks
Get-Disk

# Show disk details
Get-Disk | Select-Object Number, FriendlyName, Size, PartitionStyle, OperationalStatus

# Check for offline disks
Get-Disk | Where-Object {$_.OperationalStatus -eq "Offline"}

# Show volumes
Get-Volume

# Show partition information
Get-Partition
```

### Initialize and Format Disk

```powershell
# Initialize disk (replace 2 with your disk number)
Initialize-Disk -Number 2 -PartitionStyle GPT

# Create partition using maximum size
New-Partition -DiskNumber 2 -UseMaximumSize -AssignDriveLetter

# Format volume
Format-Volume -DriveLetter F -FileSystem NTFS -NewFileSystemLabel "Data" -Confirm:$false

# Complete process in one script
$diskNumber = 2
Initialize-Disk -Number $diskNumber -PartitionStyle GPT
$partition = New-Partition -DiskNumber $diskNumber -UseMaximumSize -AssignDriveLetter
Format-Volume -Partition $partition -FileSystem NTFS -NewFileSystemLabel "Data" -Confirm:$false
```

### Disk Management

```powershell
# Bring disk online
Set-Disk -Number 2 -IsOffline $false

# Set disk to read-write
Set-Disk -Number 2 -IsReadOnly $false

# Extend volume (if space available)
$partition = Get-Partition -DriveLetter F
$maxSize = (Get-PartitionSupportedSize -DriveLetter F).SizeMax
Resize-Partition -DriveLetter F -Size $maxSize

# Check disk health
Get-PhysicalDisk | Select-Object FriendlyName, HealthStatus, OperationalStatus

# Check for disk errors (Windows built-in)
chkdsk C: /scan
```

---

## <a name="security-logs"></a>Part 7: Security & Event Logs

### Security Event Log

```powershell
# Failed logon attempts (Event ID 4625)
Get-EventLog -LogName Security -InstanceId 4625 -Newest 50 | Format-Table TimeGenerated, Message -AutoSize

# Successful logons (Event ID 4624)
Get-EventLog -LogName Security -InstanceId 4624 -Newest 50

# Account lockouts (Event ID 4740)
Get-EventLog -LogName Security -InstanceId 4740

# Special privilege logons (Event ID 4672)
Get-EventLog -LogName Security -InstanceId 4672 -Newest 20

# Audit policy changes (Event ID 4719)
Get-EventLog -LogName Security -InstanceId 4719

# User account created (Event ID 4720)
Get-EventLog -LogName Security -InstanceId 4720
```

### System Event Log

```powershell
# System errors
Get-EventLog -LogName System -EntryType Error -Newest 50

# System warnings
Get-EventLog -LogName System -EntryType Warning -Newest 50

# Service start/stop events
Get-EventLog -LogName System | Where-Object {$_.Message -like "*service*"}

# Recent reboots
Get-EventLog -LogName System -Source "User32" -Newest 10

# Filter by time
$startTime = (Get-Date).AddHours(-24)
Get-WinEvent -FilterHashtable @{LogName='System'; Level=2; StartTime=$startTime}
```

### Application Event Log

```powershell
# Application errors
Get-EventLog -LogName Application -EntryType Error -Newest 50

# Application crashes
Get-EventLog -LogName Application -Source "Application Error" -Newest 20

# Application hangs
Get-EventLog -LogName Application -Source "Application Hang" -Newest 20
```

### Azure-Specific Logs

```powershell
# Windows Azure Guest Agent logs
Get-Content "C:\WindowsAzure\Logs\WaAppAgent.log" -Tail 50

# Extension logs
Get-ChildItem "C:\WindowsAzure\Logs\Plugins\" -Recurse -Filter "*.log"

# Custom Script Extension logs
Get-Content "C:\Packages\Plugins\Microsoft.Compute.CustomScriptExtension\*\Status\*.status"
```

### Audit Current Security Settings

```powershell
# Check local security policy
secedit /export /cfg C:\Temp\secpol.cfg

# Check audit policy
auditpol /get /category:*

# Check user rights assignment
whoami /priv

# Check if BitLocker is enabled
Get-BitLockerVolume

# Check Windows Defender status
Get-MpComputerStatus
```

---

## <a name="azure-powershell"></a>Part 8: Azure PowerShell Commands

### Installation & Authentication

```powershell
# Install Azure PowerShell module
Install-Module -Name Az -Repository PSGallery -Force

# Import module
Import-Module Az

# Login to Azure
Connect-AzAccount

# Login with managed identity (from Azure VM)
Connect-AzAccount -Identity

# Check current context
Get-AzContext

# List all subscriptions
Get-AzSubscription

# Switch subscription
Set-AzContext -SubscriptionId "subscription-id"
```

### VM Management

```powershell
# List all VMs in subscription
Get-AzVM | Select-Object Name, ResourceGroupName, Location

# List VMs in specific resource group
Get-AzVM -ResourceGroupName "myRG"

# Get VM details
Get-AzVM -ResourceGroupName "myRG" -Name "myVM"

# Get VM status
Get-AzVM -ResourceGroupName "myRG" -Name "myVM" -Status

# Start VM
Start-AzVM -ResourceGroupName "myRG" -Name "myVM"

# Stop VM (deallocate)
Stop-AzVM -ResourceGroupName "myRG" -Name "myVM" -Force

# Restart VM
Restart-AzVM -ResourceGroupName "myRG" -Name "myVM"
```

### Network & Disk Operations

```powershell
# List NSG rules
Get-AzNetworkSecurityGroup -ResourceGroupName "myRG" | Get-AzNetworkSecurityRuleConfig

# List virtual networks
Get-AzVirtualNetwork

# List public IP addresses
Get-AzPublicIpAddress | Select-Object Name, ResourceGroupName, IpAddress

# List network interfaces
Get-AzNetworkInterface | Select-Object Name, ResourceGroupName, IpConfigurations

# List managed disks
Get-AzDisk | Select-Object Name, ResourceGroupName, DiskSizeGB, DiskState

# Get disk details
Get-AzDisk -ResourceGroupName "myRG" -Name "myDisk"
```

---

## <a name="serial-console"></a>Part 9: Serial Console (Special Admin Console)

When RDP fails, use Azure Serial Console. It's a text-based console that gives you CMD access even when networking is broken.

### Accessing Serial Console

1. Azure Portal → VM → Help → Serial Console
2. Press Enter to get CMD prompt
3. You're now in a CMD window with SYSTEM privileges

### Essential Serial Console Commands

**Note:** Serial Console uses CMD, not PowerShell. Screen is limited to 80x24 characters.

```cmd
REM Check network configuration
ipconfig /all

REM Test connectivity
ping 8.8.8.8
ping DC01.CONTOSO.COM

REM Check firewall status
netsh advfirewall show allprofiles

REM Temporarily disable firewall (testing only!)
netsh advfirewall set allprofiles state off

REM Re-enable firewall
netsh advfirewall set allprofiles state on

REM Check RDP service
sc query TermService
sc start TermService

REM Check RDP port
netstat -ano | findstr :3389

REM Enable RDP via registry
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server" /v fDenyTSConnections /t REG_DWORD /d 0 /f

REM Check DNS settings
ipconfig /displaydns
ipconfig /flushdns

REM Check routes
route print

REM Check services
sc query
sc query NTDS
sc query DNS

REM View event logs (limited)
wevtutil qe System /c:20 /rd:true /f:text

REM Check disk status
wmic diskdrive list brief
wmic logicaldisk get name,freespace,size
```

### PowerShell from Serial Console

You can launch PowerShell from SAC:

```cmd
REM Start PowerShell
powershell

REM Now you're in PowerShell with all commands available
Get-Service
Get-EventLog -LogName System -Newest 10
Test-ComputerSecureChannel
```

### Common Serial Console Scenarios

**Scenario 1: RDP Not Working After Update**

```cmd
REM Check RDP service status
sc query TermService

REM If stopped, start it
sc start TermService

REM Check if RDP is enabled
reg query "HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server" /v fDenyTSConnections

REM Enable RDP
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server" /v fDenyTSConnections /t REG_DWORD /d 0 /f

REM Check firewall
netsh advfirewall show allprofiles

REM Check what's listening on port 3389
netstat -ano | findstr :3389
```

**Scenario 2: VM Not Joining Domain**

```cmd
REM Check DNS configuration
ipconfig /all

REM Test DC connectivity
ping DC01.CONTOSO.COM
telnet DC01.CONTOSO.COM 389

REM Check domain membership
wmic computersystem get domain

REM Try to join domain (if networked)
powershell
Add-Computer -DomainName CONTOSO.COM -Credential (Get-Credential) -Restart
```

---

## <a name="quick-reference"></a>Quick Reference Table

| Category | Command | What It Does |
|----------|---------|--------------|
| **VM Agent** | `Get-Service WindowsAzureGuestAgent` | Check Azure agent |
| | `Get-Content C:\WindowsAzure\Logs\WaAppAgent.log` | View agent logs |
| **Extensions** | `Get-ChildItem C:\Packages\Plugins` | List extensions |
| | `Get-Content C:\WindowsAzure\Logs\Plugins\...\CommandExecution.log` | View execution logs |
| **IMDS** | `Invoke-RestMethod -Headers @{"Metadata"="true"} -Uri http://169.254...` | Get metadata |
| **Domain Join** | `Add-Computer -DomainName CONTOSO.COM` | Join AD domain |
| | `Test-ComputerSecureChannel` | Test domain trust |
| | `Test-ComputerSecureChannel -Repair` | Repair trust |
| **Group Policy** | `gpupdate /force` | Force GP refresh |
| | `gpresult /r` | Show applied policies |
| | `gpresult /h report.html` | Generate GP report |
| **AD Queries** | `Get-ADComputer $env:COMPUTERNAME` | Get computer object |
| | `Get-ADUser username` | Get user details |
| | `nltest /sc_query:CONTOSO.COM` | Check DC connection |
| **Network** | `Test-NetConnection -Port 389` | Test port connectivity |
| | `Resolve-DnsName DC01.CONTOSO.COM` | DNS lookup |
| | `Get-NetFirewallRule` | List firewall rules |
| **Disk** | `Get-Disk` | List disks |
| | `Initialize-Disk -Number 2` | Initialize disk |
| | `Format-Volume -DriveLetter F` | Format volume |
| **Event Logs** | `Get-EventLog -LogName Security -InstanceId 4625` | Failed logons |
| | `Get-EventLog -LogName System -EntryType Error` | System errors |
| **Azure PowerShell** | `Get-AzVM` | List VMs |
| | `Start-AzVM` / `Stop-AzVM` | Control VMs |
| **Serial Console** | `sc query TermService` | Check RDP service |
| | `ipconfig /all` | Network config |
| | `netsh advfirewall show allprofiles` | Firewall status |

---

## Domain Controller Management (Bonus)

If you're running Domain Controllers in Azure (many enterprises do):

### DC Health Checks

```powershell
# Check AD services
Get-Service NTDS, DNS, Kerberos, Netlogon, W32Time

# Check AD replication
repadmin /replsummary
repadmin /showrepl

# Check replication failures
Get-ADReplicationFailure -Scope Domain

# Force replication
repadmin /syncall /AdeP

# Check FSMO roles
netdom query fsmo

# Move FSMO role (if needed)
Move-ADDirectoryServerOperationMasterRole -Identity "DC02" -OperationMasterRole SchemaMaster
```

### DNS Diagnostics

```powershell
# Run dcdiag DNS tests
dcdiag /test:dns

# Full DC diagnostic
dcdiag /v

# Check DNS zones
Get-DnsServerZone

# Check DNS server settings
Get-DnsServer

# Test DNS recursion
Resolve-DnsName www.google.com -Server localhost
```

### Time Sync for DCs

```powershell
# Check time source (PDC Emulator should sync with external source)
w32tm /query /source
w32tm /query /status

# Configure PDC to sync with external time source
w32tm /config /manualpeerlist:"time.windows.com" /syncfromflags:manual /reliable:yes /update

# Restart time service
Restart-Service W32Time

# Force sync
w32tm /resync /force

# Check sync with other DCs
w32tm /monitor
```

---

## What Microsoft Doesn't Document Well

Microsoft's Azure Windows documentation assumes:

1. **Domain join always works** - It doesn't. DNS misconfiguration, time sync, and network issues are common.
2. **Group Policy "just applies"** - In hybrid scenarios with Azure VMs, GP often fails without clear errors.
3. **Serial Console is obvious** - It's not. Most admins don't know it exists or how to use it effectively.
4. **Traditional AD needs are met** - Azure AD Domain Services docs dominate, but enterprises run traditional AD.
5. **Extension troubleshooting is straightforward** - Exit codes and logs are poorly documented.

This guide fills those gaps with commands you'll actually use in production.

---

## Common Production Scenarios

### Scenario 1: "Domain trust failed after VM restart"

```powershell
# Check secure channel
Test-ComputerSecureChannel
# If returns False:

# Repair trust
Test-ComputerSecureChannel -Repair -Credential (Get-Credential CONTOSO\admin)

# If repair fails, check DNS and DC connectivity
Get-DnsClientServerAddress
Test-NetConnection DC01.CONTOSO.COM -Port 389

# Check event logs
Get-EventLog -LogName System -Source "Microsoft-Windows-GroupPolicy" -Newest 10
```

### Scenario 2: "Group Policy not applying to Azure VMs"

```powershell
# Force GP update
gpupdate /force

# Generate detailed report
gpresult /h C:\Temp\GPReport.html

# Check GP event logs
Get-EventLog -LogName System -Source "Microsoft-Windows-GroupPolicy" -EntryType Error

# Verify domain membership
(Get-WmiObject Win32_ComputerSystem).Domain

# Check OU placement
Get-ADComputer $env:COMPUTERNAME | Select-Object DistinguishedName

# Test secure channel
Test-ComputerSecureChannel

# Check site assignment
nltest /dsgetsite
```

### Scenario 3: "Can't RDP after Windows Update"

Use Serial Console:

```cmd
REM Check RDP service
sc query TermService
sc start TermService

REM Check firewall
netsh advfirewall show allprofiles
netsh advfirewall firewall show rule name="Remote Desktop"

REM Enable RDP
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server" /v fDenyTSConnections /t REG_DWORD /d 0 /f

REM Check what's listening
netstat -ano | findstr :3389

REM Check recent errors
powershell Get-EventLog -LogName System -EntryType Error -Newest 20
```

### Scenario 4: "New disk attached but not showing in Explorer"

```powershell
# Check if disk is visible
Get-Disk

# If disk shows as Offline or Raw:
Initialize-Disk -Number 2 -PartitionStyle GPT
New-Partition -DiskNumber 2 -UseMaximumSize -AssignDriveLetter
Format-Volume -DriveLetter F -FileSystem NTFS -NewFileSystemLabel "Data"

# Verify
Get-Volume
```

---

## Conclusion

These 50 commands cover 90% of Windows Server Azure administration tasks. Whether you manage 5 VMs or 5,000, these commands bridge the gap between successful deployment and operational reality.

**For most administrators:** Focus on Parts 1-6 for daily operations

**For enterprise environments:** Add Parts 3-4 (Active Directory + Group Policy) for domain-joined infrastructure

**For troubleshooting:** Part 9 (Serial Console) is critical when RDP fails

The key insight: Infrastructure-as-code deploys the VMs. These Windows commands fix the 20% that breaks after deployment.

---

## Download: Complete Command Reference

Want this as a searchable PDF cheat sheet?

**[Download: Azure Windows Command Reference (PDF)](#)**

Includes:
- All 50 commands with examples and Azure context
- Active Directory domain join checklist
- Group Policy troubleshooting flowchart
- Port reference table (AD, Azure services, RDP)
- Event log ID reference (4624, 4625, 4740, etc.)
- Serial Console quick reference card

Enter your email below and I'll send you the complete guide:

[Beehiiv email capture form]

---

## What's Next?

**Related posts:**
- [50 Linux Commands for Azure](/blog/50-linux-commands-azure/)
- [Azure VM Inventory with KQL](/blog/azure-vm-inventory-kql/)
- [Why Most Azure Migrations Fail](/blog/why-most-azure-migrations-fail/)

**Managing both Windows and Linux?** Check out our [Linux Commands for Azure guide](/blog/50-linux-commands-azure/) covering Ubuntu, RHEL, and Active Directory domain join from the Linux side.

**Questions?** Domain join issues, Group Policy problems, and trust relationship failures are some of the most frustrating Azure problems. If you hit an issue not covered here, reach out—I've probably seen it in a production banking environment.

---

*Updated December 2025 - Tested on Windows Server 2019, 2022, and Windows 10/11 in Azure production environments.*
