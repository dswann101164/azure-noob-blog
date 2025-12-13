---
title: "50 Linux Commands for Azure (However You Deploy)"
date: 2025-12-08
summary: "The essential Linux commands every Azure administrator needs—whether you use the Portal, PowerShell, or IaC. Includes Active Directory domain join for enterprise environments."
tags: ["azure", "linux", "operations", "active-directory", "troubleshooting", "commands"]
cover: "/static/images/hero/linux-commands-azure.png"
hub: ai
---
Whether you deploy Azure VMs through the Portal, PowerShell, ARM templates, or Terraform—eventually you'll SSH in to troubleshoot something. The deployment succeeded, the Portal shows green checkmarks, but users can't authenticate, disks aren't mounted, or network connectivity mysteriously stopped working.


This guide is part of our [AI-Assisted Azure Operations hub](/hub/ai/) exploring how AI tools transform cloud administration and productivity workflows.

This is when you need actual Linux commands.

This guide covers the 50 commands that bridge the gap between successful deployment and operational readiness. These are the commands I use daily managing Azure infrastructure in a regulated banking environment.

## Who This is For

- Azure administrators managing Linux VMs
- Anyone who's ever seen "Deployment succeeded" but things don't work
- Enterprise environments with Active Directory requirements
- Operations teams bridging cloud and traditional infrastructure

## Table of Contents

1. [Azure-Specific Basics](#azure-basics)
2. [System Administration](#system-admin)
3. [Networking](#networking)
4. [File Operations](#file-operations)
5. [Azure Disk Operations](#disk-operations)
6. [Security & Logs](#security-logs)
7. [Azure CLI](#azure-cli)
8. [Active Directory Domain Join](#active-directory) (Enterprise)
9. [Quick Reference](#quick-reference)

---

## <a name="azure-basics"></a>Part 1: Azure-Specific Basics

### Azure VM Agent & Extensions

The Azure VM Agent enables extensions, monitoring, and management. When extensions won't install or Azure automation fails, start here:

```bash
# Check agent status
sudo systemctl status walinuxagent

# View agent logs
sudo tail -f /var/log/waagent.log

# Restart agent
sudo systemctl restart walinuxagent

# Check which extensions are installed
sudo ls -la /var/lib/waagent/
```

**Common issue:** "Custom Script Extension shows as succeeded but my script didn't run."

Check the actual extension logs:

```bash
# View extension handler logs
sudo cat /var/log/azure/custom-script/handler.log

# Check extension status files
sudo cat /var/lib/waagent/Microsoft.Azure.Extensions.CustomScript*/status/*.status

# Look for exit codes
sudo cat /var/lib/waagent/Microsoft.Azure.Extensions.CustomScript*/status/*.status | grep exitCode
```

### Azure Instance Metadata Service (IMDS)

Query VM metadata and managed identity tokens:

```bash
# Get VM metadata
curl -H "Metadata:true" "http://169.254.169.254/metadata/instance?api-version=2021-02-01" | jq

# Get managed identity token
curl -H "Metadata:true" \
  "http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://management.azure.com/"

# Check if VM has managed identity
curl -H "Metadata:true" "http://169.254.169.254/metadata/instance/compute/identity?api-version=2021-02-01"
```

### cloud-init Troubleshooting

If you used custom_data for VM initialization:

```bash
# Check cloud-init logs
sudo tail -f /var/log/cloud-init-output.log
sudo cat /var/log/cloud-init.log

# Check cloud-init status
sudo cloud-init status

# Re-run cloud-init (testing only!)
sudo cloud-init clean
sudo cloud-init init
```

> **💼 Enterprise Callout: Active Directory Domain Join**
> 
> If you need to join Azure VMs to Active Directory for centralized authentication:
> ```bash
> # Quick test if domain join succeeded
> sudo realm list
> getent passwd username@DOMAIN.COM
> ```
> 
> [Jump to full Active Directory guide →](#active-directory)

---

## <a name="system-admin"></a>Part 2: System Administration

### Process & Performance Monitoring

```bash
# Real-time process monitoring
top
htop  # Install with: apt install htop

# List all processes
ps aux
ps -ef

# Check specific service status
sudo systemctl status sshd
sudo systemctl status azuremonitoragent

# View service logs
sudo journalctl -u sshd
sudo journalctl -u walinuxagent --since "1 hour ago"

# Follow logs in real-time
sudo journalctl -u sshd -f
```

### System Resource Checks

```bash
# Disk usage
df -h
du -sh /var/log/*

# Memory usage
free -h
vmstat 1 5

# System uptime and load
uptime

# CPU information
lscpu
cat /proc/cpuinfo

# Check for high CPU processes
top -b -n 1 | head -20
```

### User & Permission Management

```bash
# Execute as root
sudo systemctl restart sshd

# Change file permissions
chmod 755 script.sh
chmod 600 /etc/sssd/sssd.conf

# Change file ownership
sudo chown azureuser:azureuser /datadisk
sudo chown -R www-data:www-data /var/www/html

# Add user
sudo useradd -m -s /bin/bash newuser

# Modify user
sudo usermod -aG sudo newuser

# Set/change password
sudo passwd newuser

# Check user info
id username
groups username
```

---

## <a name="networking"></a>Part 3: Networking

### Connectivity Testing

```bash
# Test basic connectivity
ping 8.8.8.8
ping DC01.CONTOSO.COM

# HTTP requests
curl https://azure.microsoft.com
wget https://example.com/file.tar.gz

# Test specific port
nc -zv 10.0.0.4 22
telnet 10.0.0.4 389

# Trace network route
traceroute azure.microsoft.com

# DNS lookup
nslookup DC01.CONTOSO.COM
dig DC01.CONTOSO.COM

# Check DNS configuration
cat /etc/resolv.conf
```

### Network Status & Configuration

```bash
# Show network interfaces (modern)
ip addr show
ip link show

# Show routing table
ip route show

# Show listening ports and connections
ss -tulpn
ss -tulpn | grep LISTEN

# Legacy netstat (if installed)
netstat -tulpn
netstat -an | grep ESTABLISHED
```

### Firewall Management

```bash
# Ubuntu/Debian - UFW
sudo ufw status
sudo ufw allow 22/tcp
sudo ufw enable

# RHEL/CentOS - firewalld
sudo firewall-cmd --list-all
sudo firewall-cmd --add-port=80/tcp --permanent
sudo firewall-cmd --reload

# iptables (legacy but still used)
sudo iptables -L -n -v
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
```

**Important:** Azure NSG rules take precedence over VM-level firewalls. If you can't connect, check both.

---

## <a name="file-operations"></a>Part 4: File Operations

### Navigation & Viewing

```bash
# List files with details
ls -la
ls -lh  # Human-readable sizes
ls -lt  # Sort by time

# Change directory
cd /var/log
cd ~  # Home directory
cd -  # Previous directory

# Show current directory
pwd

# View files
cat /etc/hosts
less /var/log/syslog
more /etc/fstab

# View file with line numbers
cat -n /etc/ssh/sshd_config

# Follow log file in real-time
tail -f /var/log/syslog
tail -f /var/log/auth.log

# View first/last lines
head -20 /var/log/syslog
tail -50 /var/log/syslog
```

### Searching

```bash
# Find files
find /var/log -name "*.log"
find /home -type f -mtime -7  # Modified in last 7 days
find / -name "waagent.log" 2>/dev/null

# Search text in files
grep "error" /var/log/syslog
grep -r "Failed" /var/log/
grep -i "authentication failure" /var/log/auth.log

# Search with context
grep -A 5 -B 5 "error" logfile.txt
```

### File Management

```bash
# Copy files
cp file1.txt file2.txt
cp -r /source/dir /destination/dir

# Move/rename
mv oldname.txt newname.txt
mv /tmp/file.txt /home/user/

# Delete files
rm file.txt
rm -rf /tmp/olddata/  # Careful with -rf!

# Create empty file
touch newfile.txt

# Create directory
mkdir /datadisk/backups
mkdir -p /data/app/logs  # Create parent dirs
```

### Archive Operations

```bash
# Create tar archive
tar -czf backup.tar.gz /var/www/html/

# Extract tar archive
tar -xzf backup.tar.gz
tar -xzf backup.tar.gz -C /destination/

# List tar contents
tar -tzf backup.tar.gz

# Zip/unzip
zip -r archive.zip /path/to/dir
unzip archive.zip
```

---

## <a name="disk-operations"></a>Part 5: Azure Disk Operations

When you attach a managed disk via Portal, PowerShell, or IaC, it shows as "attached" but isn't mounted. Here's how to make it usable:

### Check Attached Disks

```bash
# List block devices
lsblk

# Show all disks and partitions
sudo fdisk -l

# Show disk UUIDs
sudo blkid
```

### Partition, Format, and Mount

```bash
# Partition the disk (interactive)
sudo fdisk /dev/sdc
# Commands: n (new), p (primary), 1 (partition number), enter, enter, w (write)

# Format with ext4
sudo mkfs.ext4 /dev/sdc1

# Create mount point
sudo mkdir /datadisk

# Mount temporarily
sudo mount /dev/sdc1 /datadisk

# Verify mount
df -h
mount | grep sdc
```

### Make Mount Permanent

```bash
# Get UUID
sudo blkid /dev/sdc1
# Output: /dev/sdc1: UUID="abc123..." TYPE="ext4"

# Add to fstab
echo "UUID=abc123-def456 /datadisk ext4 defaults,nofail 0 0" | sudo tee -a /etc/fstab

# Test fstab (doesn't actually mount)
sudo findmnt --verify

# Test mount all
sudo mount -a

# Verify
df -h | grep datadisk
```

**Important:** Always use `nofail` option in fstab for data disks. Otherwise, if the disk fails to mount, the VM won't boot.

---

## <a name="security-logs"></a>Part 6: Security & Logs

### Log Files

```bash
# System logs
sudo tail -f /var/log/syslog        # Ubuntu/Debian
sudo tail -f /var/log/messages      # RHEL/CentOS

# Authentication logs
sudo tail -f /var/log/auth.log      # Ubuntu/Debian
sudo tail -f /var/log/secure        # RHEL/CentOS

# Azure-specific logs
sudo tail -f /var/log/waagent.log
sudo tail -f /var/log/azure/custom-script/handler.log

# Kernel logs
dmesg
dmesg | grep -i error

# Boot logs
sudo journalctl -b
```

### Security Checks

```bash
# Check login history
last
last -a  # Show hostname
lastb    # Failed login attempts

# Currently logged in users
who
w

# Check sudo permissions
sudo -l

# View failed authentication attempts
sudo grep "Failed password" /var/log/auth.log
sudo grep "authentication failure" /var/log/auth.log | tail -20

# Check for suspicious activity
sudo grep "session opened" /var/log/auth.log | grep -v "azureuser"
```

---

## <a name="azure-cli"></a>Part 7: Azure CLI Commands

Install Azure CLI:

```bash
# Ubuntu/Debian
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# RHEL/CentOS
sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc
sudo sh -c 'echo -e "[azure-cli]\nname=Azure CLI\nbaseurl=https://packages.microsoft.com/yumrepos/azure-cli\nenabled=1\ngpgcheck=1\ngpgkey=https://packages.microsoft.com/keys/microsoft.asc" > /etc/yum.repos.d/azure-cli.repo'
sudo yum install azure-cli
```

Common operations:

```bash
# Login
az login
az login --identity  # Using managed identity

# Show current subscription
az account show

# List subscriptions
az account list --output table

# Switch subscription
az account set --subscription "Production"

# List VMs
az vm list --output table
az vm list --resource-group myRG --output table

# VM operations
az vm start --resource-group myRG --name myVM
az vm stop --resource-group myRG --name myVM
az vm restart --resource-group myRG --name myVM
az vm deallocate --resource-group myRG --name myVM

# Show VM details
az vm show --resource-group myRG --name myVM
az vm get-instance-view --resource-group myRG --name myVM

# Network operations
az network nsg rule list --resource-group myRG --nsg-name myNSG --output table
az network vnet list --output table
az network nic list --output table

# Disk operations
az disk list --output table
az disk show --resource-group myRG --name myDisk
```

---

## <a name="active-directory"></a>Part 8: Active Directory Domain Join (Enterprise Deep-Dive)

> **Note:** This section is optional. Skip if you don't need Active Directory integration.

### When You Need This

- Centralized user authentication across hybrid infrastructure
- Group Policy management for compliance
- Enterprise SSO requirements
- Regulated environments (banking, healthcare, government)

Most Azure documentation focuses on Azure AD Domain Services (AADDS). This guide covers joining to **traditional Active Directory Domain Controllers**, which is what most enterprises actually run.

### Prerequisites

Before attempting domain join:

1. **Network connectivity** - VM must reach domain controller
2. **DNS** - Must point to DC (not Azure DNS or 8.8.8.8)
3. **Time sync** - Must be within 5 minutes of DC (Kerberos requirement)
4. **Ports open** - 53, 88, 389, 445, 636 (minimum)
5. **Admin credentials** - Account with domain join privileges

### Required Ports

| Port | Protocol | Service | Required |
|------|----------|---------|----------|
| 53 | TCP/UDP | DNS | Yes |
| 88 | TCP/UDP | Kerberos | Yes |
| 135 | TCP | RPC | Yes |
| 389 | TCP/UDP | LDAP | Yes |
| 445 | TCP | SMB | Yes |
| 464 | TCP/UDP | Kerberos Password | Yes |
| 636 | TCP | LDAPS | Recommended |
| 3268 | TCP | Global Catalog | Recommended |
| 3269 | TCP | Global Catalog SSL | Recommended |

### Installation (Ubuntu/Debian)

```bash
# Update package list
sudo apt update

# Install required packages
sudo apt install -y realmd sssd sssd-tools libnss-sss libpam-sss \
  adcli samba-common-bin packagekit krb5-user

# During install, you'll be prompted for Kerberos realm (DOMAIN.COM in uppercase)
```

### Installation (RHEL/CentOS)

```bash
# Install packages
sudo yum install -y realmd sssd oddjob oddjob-mkhomedir adcli \
  samba-common samba-common-tools krb5-workstation

# Enable and start services
sudo systemctl enable sssd
sudo systemctl start sssd
```

### Domain Join Process

#### Step 1: Configure DNS

**Critical:** VM must use domain controller as DNS server, not Azure DNS or public DNS.

```bash
# Check current DNS
cat /etc/resolv.conf

# Configure DNS (temporary - for testing)
echo "nameserver 10.0.0.4" | sudo tee /etc/resolv.conf
echo "search CONTOSO.COM" | sudo tee -a /etc/resolv.conf

# Make permanent (Ubuntu/Debian with netplan)
sudo nano /etc/netplan/50-cloud-init.yaml

# Add under ethernet section:
#   nameservers:
#     addresses: [10.0.0.4, 10.0.0.5]
#     search: [CONTOSO.COM]

sudo netplan apply

# Make permanent (RHEL/CentOS)
sudo nmcli con mod "System eth0" ipv4.dns "10.0.0.4 10.0.0.5"
sudo nmcli con mod "System eth0" ipv4.dns-search "CONTOSO.COM"
sudo nmcli con up "System eth0"

# Verify DNS resolution
nslookup DC01.CONTOSO.COM
nslookup CONTOSO.COM
nslookup _ldap._tcp.dc._msdcs.CONTOSO.COM
```

#### Step 2: Configure Time Sync

**This is critical.** Kerberos authentication fails if time difference exceeds 5 minutes.

```bash
# Check current time and timezone
timedatectl status

# Enable NTP
sudo timedatectl set-ntp true

# Sync immediately with domain controller
sudo ntpdate DC01.CONTOSO.COM

# Or use chrony (RHEL 8+)
sudo systemctl enable chronyd
sudo systemctl start chronyd

# Add DC as time source
echo "server DC01.CONTOSO.COM iburst" | sudo tee -a /etc/chrony.conf
sudo systemctl restart chronyd

# Verify sync
chronyc sources
```

#### Step 3: Discover Domain

```bash
# Discover domain
sudo realm discover CONTOSO.COM

# Expected output:
# contoso.com
#   type: kerberos
#   realm-name: CONTOSO.COM
#   domain-name: contoso.com
#   configured: no
#   server-software: active-directory
#   client-software: sssd
```

If discovery fails:

```bash
# Check DNS resolution
nslookup _ldap._tcp.dc._msdcs.CONTOSO.COM

# Check DC connectivity
ping DC01.CONTOSO.COM
nc -zv DC01.CONTOSO.COM 389
```

#### Step 4: Join Domain

```bash
# Join domain (interactive - will prompt for password)
sudo realm join --user=administrator CONTOSO.COM

# Or specify password on command line (scripting)
echo 'P@ssw0rd' | sudo realm join --user=administrator CONTOSO.COM --stdin

# Join with specific OU (optional)
sudo realm join --user=administrator --computer-ou="OU=Servers,OU=Azure,DC=CONTOSO,DC=COM" CONTOSO.COM

# Verify join
sudo realm list
```

Expected output:

```
contoso.com
  type: kerberos
  realm-name: CONTOSO.COM
  domain-name: contoso.com
  configured: kerberos-member
  server-software: active-directory
  client-software: sssd
  required-package: sssd-tools
  required-package: sssd
  required-package: libnss-sss
  required-package: libpam-sss
  required-package: adcli
  required-package: samba-common-bin
  login-formats: %U@contoso.com
  login-policy: allow-realm-logins
```

#### Step 5: Configure SSSD

```bash
# Edit SSSD configuration
sudo nano /etc/sssd/sssd.conf

# Recommended settings:
# [sssd]
# domains = CONTOSO.COM
# config_file_version = 2
# services = nss, pam
# 
# [domain/CONTOSO.COM]
# default_shell = /bin/bash
# krb5_store_password_if_offline = True
# cache_credentials = True
# krb5_realm = CONTOSO.COM
# realmd_tags = manages-system joined-with-adcli
# id_provider = ad
# fallback_homedir = /home/%u
# ad_domain = contoso.com
# use_fully_qualified_names = False
# ldap_id_mapping = True
# access_provider = ad

# Set correct permissions
sudo chmod 600 /etc/sssd/sssd.conf
sudo chown root:root /etc/sssd/sssd.conf

# Restart SSSD
sudo systemctl restart sssd
sudo systemctl status sssd
```

Key settings explained:

- `use_fully_qualified_names = False` - Allow login as "john" instead of "john@contoso.com"
- `fallback_homedir = /home/%u` - Create home directory in /home/username
- `ldap_id_mapping = True` - Automatically map AD SIDs to Unix UIDs/GIDs
- `cache_credentials = True` - Allow offline authentication

#### Step 6: Configure Home Directory Creation

```bash
# Enable automatic home directory creation
sudo pam-auth-update --enable mkhomedir

# Or manually add to PAM configuration
echo "session required pam_mkhomedir.so skel=/etc/skel/ umask=0077" | \
  sudo tee -a /etc/pam.d/common-session

# For RHEL/CentOS
sudo authconfig --enablemkhomedir --update
```

#### Step 7: Configure Sudo Access

```bash
# Add domain admins to sudoers
echo "%domain\ admins ALL=(ALL:ALL) ALL" | sudo tee /etc/sudoers.d/domain_admins

# Or specific group
echo "%azure-admins ALL=(ALL:ALL) ALL" | sudo tee /etc/sudoers.d/azure_admins

# Set correct permissions
sudo chmod 0440 /etc/sudoers.d/domain_admins

# Test syntax
sudo visudo -c
```

#### Step 8: Configure SSH

Allow password authentication for domain users:

```bash
# Edit SSH config
sudo nano /etc/ssh/sshd_config

# Ensure these settings:
PasswordAuthentication yes
ChallengeResponseAuthentication yes
UsePAM yes

# Ubuntu 22.04+ also check:
sudo nano /etc/ssh/sshd_config.d/50-cloud-init.conf

# Restart SSH
sudo systemctl restart sshd
```

### Verification & Testing

#### Test User Lookup

```bash
# Test user lookup via SSSD
getent passwd john@CONTOSO.COM
getent passwd john  # If use_fully_qualified_names = False

# Expected output:
# john:*:1450401106:1450400513:John Smith:/home/john:/bin/bash

# Test group lookup
getent group "domain admins"
getent group "domain users"

# Check user details
id john@CONTOSO.COM
groups john@CONTOSO.COM
```

#### Test Kerberos Authentication

```bash
# Get Kerberos ticket
kinit john@CONTOSO.COM
# Enter password when prompted

# List tickets
klist

# Expected output:
# Ticket cache: FILE:/tmp/krb5cc_1000
# Default principal: john@CONTOSO.COM
# 
# Valid starting     Expires            Service principal
# 12/08/25 10:00:00  12/08/25 20:00:00  krbtgt/CONTOSO.COM@CONTOSO.COM

# Destroy ticket (logout)
kdestroy
```

#### Test SSH Login

```bash
# From another machine, SSH with domain credentials
ssh john@CONTOSO.COM@vm-hostname.contoso.com

# Or if use_fully_qualified_names = False
ssh john@vm-hostname.contoso.com

# First login will create home directory
```

### Troubleshooting Commands

#### Check SSSD Status

```bash
# Service status
sudo systemctl status sssd
sudo systemctl status sssd-kcm
sudo systemctl status sssd-nss
sudo systemctl status sssd-pam

# Check domain status
sudo sssctl domain-status CONTOSO.COM

# Check online/offline status
sudo sssctl domain-status CONTOSO.COM | grep "Online status"
```

#### View Logs

```bash
# Main SSSD log
sudo tail -f /var/log/sssd/sssd.log

# Domain-specific log
sudo tail -f /var/log/sssd/sssd_CONTOSO.COM.log

# Kerberos logs
sudo tail -f /var/log/krb5libs.log

# PAM authentication log
sudo tail -f /var/log/auth.log | grep pam
```

#### Clear Cache & Restart

```bash
# Clear SSSD cache
sudo sss_cache -E

# Restart SSSD
sudo systemctl restart sssd

# Verify cache cleared
sudo sssctl cache-expire -E
```

#### Test Connectivity to DC

```bash
# Ping DC
ping DC01.CONTOSO.COM

# Test required ports
nc -zv DC01.CONTOSO.COM 53    # DNS
nc -zv DC01.CONTOSO.COM 88    # Kerberos
nc -zv DC01.CONTOSO.COM 389   # LDAP
nc -zv DC01.CONTOSO.COM 445   # SMB
nc -zv DC01.CONTOSO.COM 636   # LDAPS

# Test LDAP directly
ldapsearch -x -H ldap://DC01.CONTOSO.COM -b "DC=CONTOSO,DC=COM"
```

#### Debug Kerberos

```bash
# Enable Kerberos tracing
export KRB5_TRACE=/dev/stdout
kinit john@CONTOSO.COM

# Check Kerberos config
cat /etc/krb5.conf

# Test DNS SRV records
nslookup -type=SRV _kerberos._tcp.CONTOSO.COM
nslookup -type=SRV _ldap._tcp.CONTOSO.COM
```

#### Check User Authentication Attempts

```bash
# View all authentication attempts
sudo grep "authentication" /var/log/auth.log

# View failed attempts
sudo grep "authentication failure" /var/log/auth.log

# View successful logins
sudo grep "session opened" /var/log/auth.log

# Check SSSD authentication
sudo grep "pam_sss" /var/log/auth.log
```

### Common Errors & Solutions

#### Error: "Couldn't join realm: Failed to enroll machine"

**Cause:** DNS not configured correctly

**Solution:**
```bash
# Verify DNS points to DC
cat /etc/resolv.conf

# Test DNS resolution
nslookup DC01.CONTOSO.COM
nslookup _ldap._tcp.dc._msdcs.CONTOSO.COM

# Fix DNS
echo "nameserver 10.0.0.4" | sudo tee /etc/resolv.conf
```

#### Error: "realm: Couldn't join realm: Insufficient permissions"

**Cause:** User account doesn't have domain join privileges or wrong password

**Solution:**
```bash
# Verify account can join domain (run on DC or admin workstation)
Get-ADUser administrator -Properties msDS-AllowedToActOnBehalfOfOtherIdentity

# Try with domain admin account
sudo realm join --user=domainadmin CONTOSO.COM
```

#### Error: "No such file or directory" when trying to SSH

**Cause:** Home directory not created automatically

**Solution:**
```bash
# Enable home directory creation
sudo pam-auth-update --enable mkhomedir

# Or manually create
sudo mkdir /home/john
sudo chown john:domain\ users /home/john
```

#### Error: "Permission denied (publickey,password)"

**Cause:** Password authentication disabled in SSH

**Solution:**
```bash
# Check SSH config
sudo grep PasswordAuthentication /etc/ssh/sshd_config
sudo grep PasswordAuthentication /etc/ssh/sshd_config.d/*.conf

# Enable password auth
sudo sed -i 's/PasswordAuthentication no/PasswordAuthentication yes/' /etc/ssh/sshd_config
sudo systemctl restart sshd
```

#### Error: "Clock skew too great" (Kerberos)

**Cause:** Time difference between VM and DC exceeds 5 minutes

**Solution:**
```bash
# Check time on both systems
date
timedatectl

# Sync time immediately
sudo timedatectl set-ntp true
sudo ntpdate DC01.CONTOSO.COM

# Verify sync
timedatectl status

# Configure permanent sync
echo "server DC01.CONTOSO.COM iburst" | sudo tee -a /etc/chrony.conf
sudo systemctl restart chronyd
```

#### Error: "getent passwd username" returns nothing

**Cause:** SSSD not properly configured or domain not accessible

**Solution:**
```bash
# Check SSSD status
sudo systemctl status sssd
sudo sssctl domain-status CONTOSO.COM

# Check SSSD logs
sudo tail -50 /var/log/sssd/sssd_CONTOSO.COM.log

# Clear cache and restart
sudo sss_cache -E
sudo systemctl restart sssd

# Test after restart
sleep 5
getent passwd username
```

### Leave Domain

If you need to unjoin the domain:

```bash
# Leave domain
sudo realm leave CONTOSO.COM

# Verify
sudo realm list

# Clean up (optional)
sudo apt remove realmd sssd sssd-tools
sudo rm -rf /var/lib/sss/
sudo rm /etc/sssd/sssd.conf
```

### Automation Script

Complete domain join script for Ubuntu:

```bash
#!/bin/bash
# domain-join.sh - Automated domain join for Azure VMs

DOMAIN="CONTOSO.COM"
DC_IP="10.0.0.4"
ADMIN_USER="administrator"

echo "=== Installing packages ==="
sudo apt update
sudo DEBIAN_FRONTEND=noninteractive apt install -y realmd sssd sssd-tools \
  libnss-sss libpam-sss adcli samba-common-bin krb5-user

echo "=== Configuring DNS ==="
sudo sed -i "s/nameserver .*/nameserver $DC_IP/" /etc/resolv.conf
echo "search $DOMAIN" | sudo tee -a /etc/resolv.conf

echo "=== Syncing time ==="
sudo timedatectl set-ntp true
sleep 2

echo "=== Discovering domain ==="
sudo realm discover $DOMAIN

echo "=== Joining domain ==="
echo "Enter password for $ADMIN_USER@$DOMAIN:"
sudo realm join --user=$ADMIN_USER $DOMAIN

echo "=== Configuring SSSD ==="
sudo sed -i 's/use_fully_qualified_names = True/use_fully_qualified_names = False/g' /etc/sssd/sssd.conf
sudo sed -i '/\[domain/a fallback_homedir = /home/%u' /etc/sssd/sssd.conf
sudo chmod 600 /etc/sssd/sssd.conf

echo "=== Enabling home directory creation ==="
sudo pam-auth-update --enable mkhomedir

echo "=== Configuring sudo ==="
echo "%domain\ admins ALL=(ALL:ALL) ALL" | sudo tee /etc/sudoers.d/domain_admins
sudo chmod 0440 /etc/sudoers.d/domain_admins

echo "=== Restarting services ==="
sudo systemctl restart sssd

echo "=== Verifying join ==="
sudo realm list
echo ""
echo "Test with: getent passwd username@$DOMAIN"
echo "SSH test: ssh username@$DOMAIN@$(hostname)"
```

---

## <a name="quick-reference"></a>Quick Reference Table

| Category | Command | What It Does |
|----------|---------|--------------|
| **Azure VM Agent** | `systemctl status walinuxagent` | Check Azure agent status |
| | `tail -f /var/log/waagent.log` | View agent logs |
| **Extensions** | `ls /var/lib/waagent/` | List installed extensions |
| | `cat /var/log/azure/custom-script/handler.log` | Debug custom scripts |
| **IMDS** | `curl -H "Metadata:true" http://169.254...` | Get VM metadata |
| **cloud-init** | `tail -f /var/log/cloud-init-output.log` | Check init logs |
| **Processes** | `top` / `htop` | Monitor processes |
| | `ps aux` | List all processes |
| | `systemctl status servicename` | Check service |
| **Resources** | `df -h` | Disk usage |
| | `free -h` | Memory usage |
| | `uptime` | System load |
| **Network** | `ss -tulpn` | Listening ports |
| | `ping` / `nc -zv` | Test connectivity |
| | `nslookup` / `dig` | DNS lookup |
| **Files** | `ls -la` | List files |
| | `tail -f /var/log/syslog` | Follow logs |
| | `grep "error" logfile` | Search logs |
| **Disks** | `lsblk` | List disks |
| | `fdisk -l` | Partition info |
| | `mount` / `blkid` | Mount operations |
| **Security** | `last` | Login history |
| | `who` / `w` | Current users |
| | `sudo -l` | Check privileges |
| **Azure CLI** | `az vm list` | List VMs |
| | `az vm start/stop` | Control VMs |
| **AD Join** | `realm join DOMAIN.COM` | Join AD domain |
| | `realm list` | Check join status |
| | `getent passwd user@DOMAIN.COM` | Test user lookup |
| | `kinit user@DOMAIN.COM` | Get Kerberos ticket |
| | `sssctl domain-status DOMAIN.COM` | Check SSSD status |

---

## Pro Tips

### Serial Console Essentials

When SSH is broken, use Azure Serial Console with these commands:

```bash
# Check SSH status
sudo systemctl status sshd
sudo systemctl restart sshd

# Check network
ip addr show
ip route show

# View recent errors
sudo journalctl -xe | tail -50
sudo tail -50 /var/log/syslog
```

### Azure Monitor Agent

```bash
# Check AMA status
systemctl status azuremonitoragent

# View AMA logs
journalctl -u azuremonitoragent -f

# Restart AMA
sudo systemctl restart azuremonitoragent
```

### Time Sync (Critical for AD)

```bash
# Check time status
timedatectl status

# Enable NTP
sudo timedatectl set-ntp true

# Sync immediately
sudo ntpdate DC01.CONTOSO.COM

# Check NTP servers (chrony)
chronyc sources
```

### Quick Health Check Script

```bash
#!/bin/bash
echo "=== System Health Check ==="
echo ""
echo "Uptime & Load:"
uptime
echo ""
echo "Memory:"
free -h
echo ""
echo "Disk:"
df -h | grep -v tmpfs
echo ""
echo "Azure Agent:"
systemctl status walinuxagent --no-pager | head -3
echo ""
echo "Network:"
ip addr show | grep -E "inet |^[0-9]:"
echo ""
echo "Recent Errors:"
sudo grep -i error /var/log/syslog | tail -5
```

---

## What's Missing from Microsoft's Docs

Microsoft's Azure Linux documentation assumes you already know:

1. **Linux basics** - They jump straight to Azure-specific tools
2. **Troubleshooting workflow** - Documentation shows happy path only
3. **Active Directory complexity** - AADDS docs don't cover traditional AD
4. **Time sync criticality** - Rarely mentioned but breaks Kerberos auth
5. **Extension debugging** - Exit codes and logs are poorly documented
6. **Network troubleshooting** - NSG vs OS firewall vs app-level blocking
7. **Serial Console workflow** - Only mentioned when SSH fails completely

This guide fills those gaps with commands you'll actually use.

---

## Conclusion

These 50 commands cover 90% of Azure Linux administration tasks. Whether you manage 5 VMs or 5,000, these commands bridge the gap between successful deployment and operational reality.

**For most administrators:** Focus on Parts 1-6 for daily operations

**For enterprise environments:** Add Part 8 (Active Directory) for centralized authentication

**For automation:** Wrap these commands in scripts, Ansible playbooks, or deploy via Custom Script Extensions

The key insight: Infrastructure-as-code gets you 80% there. These Linux commands handle the remaining 20%.

---

## Download: Complete Command Reference

Want this as a searchable PDF cheat sheet?

**[Download: Azure Linux Command Reference (PDF)](#)**

Includes:
- All 50 commands with examples and Azure context
- Active Directory domain join checklist and troubleshooting flowchart
- Port reference table (Azure services, AD, common applications)
- Common error messages and solutions
- One-page quick reference card

Enter your email below and I'll send you the complete guide:

[Beehiiv email capture form]

---

## What's Next?

**Related posts:**
- [Azure VM Inventory with KQL](/blog/azure-vm-inventory-kql/)
- [Why Most Azure Migrations Fail](/blog/why-most-azure-migrations-fail/)
- [Azure Cost Optimization - What Actually Works](/blog/azure-cost-optimization-what-actually-works/)

**Questions?** The hardest part of Azure Linux management is often the stuff Microsoft doesn't document. If you hit an issue not covered here, reach out—I've probably seen it before in a production banking environment.

---

*Updated December 2025 - Tested on Ubuntu 22.04 LTS and RHEL 9.x in Azure production environments.*
