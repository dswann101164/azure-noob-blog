---
title: "The Complete Linux Cheat Sheet for Azure Admins"
date: 2025-11-03
summary: "Every Linux command you'll need as an Azure administratorâ€”organized by scenario, with Windows equivalents, and real Azure examples. Bookmark this. You'll reference it constantly."
tags: ["azure", "linux", "cloud-shell", "aks", "ubuntu", "reference"]
cover: "/static/images/hero/linux-cheat-sheet-azure.svg"
hub: automation
related_posts:
  - linux-commands-azure-admin-career
  - 50-linux-commands-azure
  - azure-osi-model-for-admins
---
This is the Linux reference guide for Azure administrators who learned on Windows.


This guide is part of our [Azure Automation hub](/hub/automation/) covering Infrastructure as Code, CI/CD pipelines, and DevOps practices.

It's organized by **what you're actually doing** (not alphabetically by command). Windows command equivalents included. Azure-specific examples throughout.

**Bookmark this page.** You'll come back to it constantly.

---

## Table of Contents

1. [Navigation & File Basics](#navigation--file-basics)
2. [Reading & Searching Files](#reading--searching-files)
3. [File Permissions & Ownership](#file-permissions--ownership)
4. [Process Management](#process-management)
5. [Service Management](#service-management)
6. [Disk & Storage](#disk--storage)
7. [Networking](#networking)
8. [User & Group Management](#user--group-management)
9. [Package Management](#package-management)
10. [Text Editing](#text-editing)
11. [System Information](#system-information)
12. [Azure-Specific Commands](#azure-specific-commands)
13. [Troubleshooting Patterns](#troubleshooting-patterns)

---

## Navigation & File Basics

### Where Am I? (pwd)

```bash
# Print working directory
pwd
# Output: /home/azureuser

# Windows equivalent: cd (with no arguments)
```

### List Files (ls)

```bash
# Basic listing
ls

# Detailed listing with permissions, owner, size, date
ls -l

# Include hidden files (. files)
ls -a

# Combination: detailed + hidden
ls -la

# Human-readable file sizes
ls -lh

# Sort by modification time (newest first)
ls -lt

# Sort by size
ls -lS

# Windows equivalent: dir, dir /a, dir /o:d
```

**Real Azure example:**

```bash
# List all files in Azure VM home directory
ls -lah ~/

# Output:
drwxr-xr-x  5 azureuser azureuser 4.0K Nov  3 10:30 .
drwxr-xr-x 12 root      root      4.0K Oct 15 08:22 ..
-rw-------  1 azureuser azureuser 1.2K Nov  3 09:15 .bash_history
drwx------  2 azureuser azureuser 4.0K Nov  2 14:30 .ssh
-rwxr-xr-x  1 azureuser azureuser 2.0K Nov  3 10:30 deploy.sh
```

### Change Directory (cd)

```bash
# Go to specific directory
cd /var/log

# Go up one level
cd ..

# Go to home directory (three ways)
cd
cd ~
cd /home/azureuser

# Go to previous directory
cd -

# Windows equivalent: cd (same syntax except for ~)
```

**Azure-specific paths:**

```bash
# Common Azure VM locations
cd /var/log                    # System logs
cd /etc                        # Configuration files
cd /var/www                    # Web applications (nginx/apache)
cd /opt                        # Third-party applications
cd /mnt                        # Mounted Azure disks
cd /usr/local/bin              # Custom scripts
```

### Create/Remove Directories (mkdir/rmdir/rm)

```bash
# Create directory
mkdir mydir

# Create nested directories
mkdir -p /path/to/nested/dir

# Remove empty directory
rmdir mydir

# Remove directory and contents (BE CAREFUL!)
rm -r mydir

# Remove with confirmation for each file
rm -ri mydir

# Force remove without confirmation (VERY DANGEROUS)
rm -rf mydir

# Windows equivalent: md, mkdir, rmdir, rd /s
```

### Copy/Move/Delete Files (cp/mv/rm)

```bash
# Copy file
cp source.txt destination.txt

# Copy directory recursively
cp -r source_dir/ destination_dir/

# Move/rename file
mv oldname.txt newname.txt

# Move file to directory
mv file.txt /path/to/directory/

# Delete file
rm file.txt

# Delete with confirmation
rm -i file.txt

# Windows equivalent: copy, xcopy, move, del
```

**Real Azure example:**

```bash
# Backup nginx config before editing
sudo cp /etc/nginx/nginx.conf /etc/nginx/nginx.conf.backup

# Copy application files to web root
sudo cp -r /home/azureuser/webapp/* /var/www/html/

# Archive old logs
sudo mv /var/log/webapp/app.log /var/log/webapp/app.log.$(date +%Y%m%d)
```

---

## Reading & Searching Files

### Display File Contents (cat/less/head/tail)

```bash
# Display entire file
cat filename.txt

# Display with line numbers
cat -n filename.txt

# Display file one screen at a time (scrollable)
less filename.txt
# Press space to scroll, q to quit

# First 10 lines
head filename.txt

# First 20 lines
head -n 20 filename.txt

# Last 10 lines
tail filename.txt

# Last 50 lines
tail -n 50 filename.txt

# Follow file in real-time (CRITICAL for log monitoring)
tail -f filename.txt

# Follow with line numbers
tail -fn 100 filename.txt

# Windows equivalent: type, Get-Content, more
```

**Real Azure example:**

```bash
# Check nginx error log
sudo tail -n 50 /var/log/nginx/error.log

# Monitor application log in real-time
tail -f /var/log/webapp/app.log

# Watch multiple logs simultaneously
tail -f /var/log/nginx/*.log

# Check system log for Azure-related entries
sudo tail -n 100 /var/log/syslog | grep azure
```

### Search Text (grep)

```bash
# Search for pattern in file
grep "search_term" filename.txt

# Case-insensitive search
grep -i "error" filename.txt

# Show line numbers
grep -n "error" filename.txt

# Show lines before/after match (context)
grep -A 3 "error" filename.txt     # 3 lines after
grep -B 3 "error" filename.txt     # 3 lines before
grep -C 3 "error" filename.txt     # 3 lines before and after

# Search recursively in all files
grep -r "search_term" /path/to/directory/

# Exclude certain files
grep -r "error" /var/log/ --exclude="*.gz"

# Count matches
grep -c "error" filename.txt

# Show only filenames with matches
grep -l "error" /var/log/*.log

# Invert match (show lines that DON'T contain pattern)
grep -v "DEBUG" app.log

# Windows equivalent: Select-String, findstr
```

**Real Azure example:**

```bash
# Find all errors in last 1000 log lines
tail -n 1000 /var/log/syslog | grep -i "error"

# Find failed SSH login attempts
sudo grep "Failed password" /var/log/auth.log

# Find when nginx was last restarted
sudo grep "nginx" /var/log/syslog | grep -i "start\|restart"

# Search all application logs for connection errors
grep -ri "connection refused" /var/log/webapp/

# Find lines with "ERROR" but exclude "DEBUG"
grep "ERROR" app.log | grep -v "DEBUG"
```

### Find Files (find)

```bash
# Find files by name
find /path -name "filename.txt"

# Case-insensitive name search
find /path -iname "*.log"

# Find files modified in last 7 days
find /path -mtime -7

# Find files older than 30 days
find /path -mtime +30

# Find files larger than 100MB
find /path -size +100M

# Find and delete files older than 30 days
find /path -name "*.log" -mtime +30 -delete

# Find files and execute command on each
find /path -name "*.log" -exec grep "error" {} \;

# Windows equivalent: dir /s, Get-ChildItem -Recurse
```

**Real Azure example:**

```bash
# Find large log files eating disk space
sudo find /var/log -type f -size +100M

# Find old logs to clean up
sudo find /var/log -name "*.log" -mtime +30

# Find all nginx config files
sudo find /etc -name "nginx.conf"

# Find files owned by specific user
find /home -user azureuser

# Clean up old application logs
sudo find /var/log/webapp -name "*.log" -mtime +30 -delete
```

---

## File Permissions & Ownership

### Understanding Permissions

```
-rwxr-xr-x  1 azureuser azureuser 2048 Nov  3 10:30 script.sh
 â”‚â”‚â”‚â”‚â”‚â”‚â”‚â”‚â”‚  â”‚ â”‚         â”‚         â”‚    â”‚
 â”‚â”‚â”‚â”‚â”‚â”‚â”‚â”‚â”‚  â”‚ â”‚         â”‚         â”‚    â””â”€ Filename
 â”‚â”‚â”‚â”‚â”‚â”‚â”‚â”‚â”‚  â”‚ â”‚         â”‚         â””â”€â”€â”€â”€â”€â”€ Date
 â”‚â”‚â”‚â”‚â”‚â”‚â”‚â”‚â”‚  â”‚ â”‚         â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ Owner
 â”‚â”‚â”‚â”‚â”‚â”‚â”‚â”‚â”‚  â”‚ â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ Group
 â”‚â”‚â”‚â”‚â”‚â”‚â”‚â”‚â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ Link count
 â”‚â”‚â”‚â”‚â”‚â”‚â”‚â”‚â””â”€ Others: execute
 â”‚â”‚â”‚â”‚â”‚â”‚â”‚â””â”€â”€ Others: write
 â”‚â”‚â”‚â”‚â”‚â”‚â””â”€â”€â”€ Others: read
 â”‚â”‚â”‚â”‚â”‚â””â”€â”€â”€â”€ Group: execute
 â”‚â”‚â”‚â”‚â””â”€â”€â”€â”€â”€ Group: write
 â”‚â”‚â”‚â””â”€â”€â”€â”€â”€â”€ Group: read
 â”‚â”‚â””â”€â”€â”€â”€â”€â”€â”€ Owner: execute
 â”‚â””â”€â”€â”€â”€â”€â”€â”€â”€ Owner: write
 â””â”€â”€â”€â”€â”€â”€â”€â”€â”€ Owner: read
```

### Change Permissions (chmod)

```bash
# Add execute permission to owner
chmod +x script.sh

# Remove write permission from group
chmod g-w file.txt

# Set specific permissions using numbers
chmod 644 file.txt      # rw-r--r-- (owner: rw, group: r, others: r)
chmod 755 script.sh     # rwxr-xr-x (owner: rwx, group: rx, others: rx)
chmod 600 private.key   # rw------- (owner: rw, group: none, others: none)
chmod 777 file.txt      # rwxrwxrwx (full permissions - AVOID THIS!)

# Recursive permission change
chmod -R 755 /var/www/html/

# Windows equivalent: icacls, attrib
```

**Permission number reference:**

```
7 = rwx (read, write, execute)      4 = r-- (read only)
6 = rw- (read, write)                3 = -wx (write, execute)
5 = r-x (read, execute)              2 = -w- (write only)
1 = --x (execute only)               0 = --- (no permissions)
```

**Real Azure example:**

```bash
# Make deployment script executable
chmod +x /home/azureuser/deploy.sh

# Secure SSH private key (Azure requires 600)
chmod 600 ~/.ssh/id_rsa

# Set proper web directory permissions
sudo chmod -R 755 /var/www/html/
sudo chmod 644 /var/www/html/*.html

# Fix permission denied errors
chmod +x /usr/local/bin/myapp
```

### Change Ownership (chown)

```bash
# Change owner
sudo chown newowner file.txt

# Change owner and group
sudo chown newowner:newgroup file.txt

# Change only group
sudo chown :newgroup file.txt

# Recursive ownership change
sudo chown -R azureuser:azureuser /var/www/webapp/

# Windows equivalent: takeown, icacls
```

**Real Azure example:**

```bash
# Fix web application ownership (common fix for permission errors)
sudo chown -R www-data:www-data /var/www/html/

# Change ownership of uploaded files
sudo chown azureuser:azureuser /home/azureuser/uploads/*

# Fix ownership after copying files as root
sudo chown -R azureuser:azureuser /home/azureuser/webapp/
```

---

## Process Management

### List Processes (ps)

```bash
# Show processes for current user
ps

# Show all processes (detailed)
ps aux

# Show processes in tree format
ps auxf

# Show processes for specific user
ps -u azureuser

# Show processes sorted by CPU usage
ps aux --sort=-%cpu | head -10

# Show processes sorted by memory usage
ps aux --sort=-%mem | head -10

# Windows equivalent: Task Manager, Get-Process
```

**Real Azure example:**

```bash
# Find process using most CPU
ps aux --sort=-%cpu | head -10

# Find nginx processes
ps aux | grep nginx

# Check if application is running
ps aux | grep "myapp"
```

### Kill Processes (kill/killall/pkill)

```bash
# Kill process by PID (graceful)
kill 1234

# Force kill process by PID
kill -9 1234

# Kill all processes with name
killall nginx

# Kill processes matching pattern
pkill -f "python.*app.py"

# Send SIGHUP (reload config without restarting)
kill -HUP 1234

# Windows equivalent: Stop-Process, taskkill
```

**Signal reference:**

```
SIGTERM (15) - Default, graceful shutdown
SIGKILL (9)  - Force kill, immediate
SIGHUP (1)   - Reload configuration
SIGINT (2)   - Interrupt (Ctrl+C)
```

**Real Azure example:**

```bash
# Kill hung process
ps aux | grep myapp
# Find PID: 5678
sudo kill 5678

# Force kill if it won't die
sudo kill -9 5678

# Kill all Python processes (BE CAREFUL)
sudo pkill python

# Reload nginx after config change (without restart)
sudo kill -HUP $(cat /var/run/nginx.pid)
```

### Monitor Processes (top/htop)

```bash
# Interactive process viewer
top

# Better interactive viewer (install first: apt install htop)
htop

# Top commands while running:
# P - sort by CPU
# M - sort by memory
# k - kill process
# q - quit

# Windows equivalent: Task Manager, Performance Monitor
```

**Real Azure example:**

```bash
# Monitor resource usage on Azure VM
top

# Find what's eating all CPU/memory
htop
# Press P to sort by CPU, M to sort by memory
```

---

## Service Management

### systemctl (Modern Service Management)

```bash
# Start service
sudo systemctl start nginx

# Stop service
sudo systemctl stop nginx

# Restart service
sudo systemctl restart nginx

# Reload configuration without restarting
sudo systemctl reload nginx

# Check service status
systemctl status nginx

# Enable service to start on boot
sudo systemctl enable nginx

# Disable service from starting on boot
sudo systemctl disable nginx

# Check if service is enabled
systemctl is-enabled nginx

# Check if service is running
systemctl is-active nginx

# List all running services
systemctl list-units --type=service --state=running

# List all failed services
systemctl --failed

# Windows equivalent: services.msc, Get-Service, Start-Service
```

**Real Azure example:**

```bash
# Start web server
sudo systemctl start nginx

# Check status
systemctl status nginx

# Enable to survive VM restarts
sudo systemctl enable nginx

# Restart after config change
sudo systemctl restart nginx

# Check if Docker is running
systemctl is-active docker
```

### View Service Logs (journalctl)

```bash
# View all logs for service
journalctl -u nginx

# Follow logs in real-time
journalctl -u nginx -f

# Last 50 lines
journalctl -u nginx -n 50

# Logs from last boot
journalctl -u nginx -b

# Logs since specific time
journalctl -u nginx --since "2025-11-03 10:00:00"

# Logs from last hour
journalctl -u nginx --since "1 hour ago"

# Windows equivalent: Event Viewer, Get-EventLog
```

**Real Azure example:**

```bash
# Debug why service failed to start
sudo journalctl -u myapp -n 100

# Monitor service logs in real-time
sudo journalctl -u nginx -f

# Check logs from last reboot
sudo journalctl -u myapp -b
```

---

## Disk & Storage

### Check Disk Space (df)

```bash
# Show disk usage (human-readable)
df -h

# Show disk usage for specific filesystem
df -h /dev/sda1

# Show inode usage (file count)
df -i

# Windows equivalent: Get-Volume, wmic
```

**Real Azure example:**

```bash
# Check all disk usage
df -h

# Output:
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1        30G   28G   2G  93% /
/dev/sdb1       100G   45G  55G  45% /mnt/data

# OS disk at 93% - need to free space!
```

### Check Directory Size (du)

```bash
# Size of current directory
du -sh .

# Size of specific directory
du -sh /var/log

# Size of all subdirectories
du -sh *

# Size sorted by largest
du -sh * | sort -hr

# Top 10 largest directories
du -h /var | sort -hr | head -10

# Windows equivalent: dir /s, Get-ChildItem -Recurse
```

**Real Azure example:**

```bash
# Find what's eating disk space
cd /
sudo du -sh * | sort -hr | head -10

# Output:
15G    /var
8G     /usr
3G     /home
2G     /opt

# Drill down into /var
cd /var
sudo du -sh * | sort -hr | head -10

# Output:
12G    /var/log
2G     /var/cache
1G     /var/lib
```

### Clean Up Disk Space

```bash
# Remove old log files
sudo find /var/log -name "*.log" -mtime +30 -delete

# Remove compressed logs
sudo find /var/log -name "*.gz" -mtime +30 -delete

# Clean package cache (Ubuntu/Debian)
sudo apt clean
sudo apt autoclean
sudo apt autoremove

# Clean package cache (CentOS/RHEL)
sudo yum clean all

# Remove old kernels (Ubuntu)
sudo apt autoremove --purge

# Windows equivalent: Disk Cleanup, cleanmgr
```

### Mount Azure Disks

```bash
# List all disks
lsblk

# Create mount point
sudo mkdir /mnt/data

# Mount disk temporarily
sudo mount /dev/sdc1 /mnt/data

# Unmount
sudo umount /mnt/data

# Make mount permanent (edit /etc/fstab)
sudo nano /etc/fstab
# Add line:
# /dev/sdc1  /mnt/data  ext4  defaults  0  2

# Reload fstab
sudo mount -a

# Windows equivalent: Disk Management, mountvol
```

---

## Networking

### Check Network Interfaces (ip)

```bash
# Show all network interfaces
ip addr

# Show specific interface
ip addr show eth0

# Show routing table
ip route

# Windows equivalent: ipconfig, Get-NetIPAddress
```

### Test Connectivity (ping/curl/telnet)

```bash
# Ping host
ping google.com

# Ping with count
ping -c 4 google.com

# Test HTTP endpoint
curl https://example.com

# Test with headers
curl -I https://example.com

# Test specific port
telnet example.com 80

# Better port testing (if telnet not installed)
nc -zv example.com 80

# Windows equivalent: Test-Connection, Test-NetConnection
```

**Real Azure example:**

```bash
# Test connectivity to Azure SQL
nc -zv myserver.database.windows.net 1433

# Test web application
curl -I https://myapp.azurewebsites.net

# Check DNS resolution
nslookup myvm.eastus.cloudapp.azure.com

# Test Azure Storage endpoint
curl -I https://mystorageaccount.blob.core.windows.net
```

### Check Open Ports (netstat/ss)

```bash
# Show all listening ports
sudo netstat -tuln

# Show processes using ports
sudo netstat -tulnp

# Modern replacement for netstat
sudo ss -tuln

# Check specific port
sudo ss -tuln | grep :80

# Windows equivalent: netstat, Get-NetTCPConnection
```

**Real Azure example:**

```bash
# Check if nginx is listening on port 80
sudo netstat -tuln | grep :80

# Find what process is using port 8080
sudo netstat -tulnp | grep :8080

# Check all listening ports on Azure VM
sudo ss -tuln
```

---

## User & Group Management

### User Management

```bash
# Add new user
sudo adduser username

# Delete user
sudo deluser username

# Delete user and home directory
sudo deluser --remove-home username

# Change user password
sudo passwd username

# Switch to another user
su - username

# Run command as another user
sudo -u username command

# Windows equivalent: net user, New-LocalUser
```

### Group Management

```bash
# Add user to group
sudo usermod -aG groupname username

# Create new group
sudo groupadd groupname

# Delete group
sudo groupdel groupname

# List groups for user
groups username

# Windows equivalent: net localgroup, Add-LocalGroupMember
```

**Real Azure example:**

```bash
# Add user to sudo group (give admin rights)
sudo usermod -aG sudo newuser

# Add user to docker group
sudo usermod -aG docker azureuser

# Add user to www-data group (web server)
sudo usermod -aG www-data azureuser
```

---

## Package Management

### Ubuntu/Debian (apt)

```bash
# Update package lists
sudo apt update

# Upgrade all packages
sudo apt upgrade

# Install package
sudo apt install nginx

# Install multiple packages
sudo apt install nginx mysql-server php

# Remove package
sudo apt remove nginx

# Remove package and config files
sudo apt purge nginx

# Clean up unused packages
sudo apt autoremove

# Search for package
apt search nginx

# Show package info
apt show nginx

# Windows equivalent: chocolatey, winget
```

### CentOS/RHEL (yum/dnf)

```bash
# Update package lists
sudo yum update

# Install package
sudo yum install nginx

# Remove package
sudo yum remove nginx

# Search for package
yum search nginx

# Modern replacement: dnf
sudo dnf install nginx

# Windows equivalent: chocolatey, winget
```

**Real Azure example:**

```bash
# Update Ubuntu VM
sudo apt update && sudo apt upgrade -y

# Install web server stack
sudo apt install nginx mysql-server php-fpm -y

# Install Azure CLI on Ubuntu
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Install Docker
sudo apt install docker.io -y
sudo systemctl start docker
sudo systemctl enable docker
```

---

## Text Editing

### nano (Beginner-Friendly)

```bash
# Edit file
nano filename.txt

# Edit file with sudo
sudo nano /etc/nginx/nginx.conf

# Keyboard shortcuts (shown at bottom):
# Ctrl+O - Save file
# Ctrl+X - Exit
# Ctrl+W - Search
# Ctrl+K - Cut line
# Ctrl+U - Paste line
```

### vi/vim (Advanced)

```bash
# Edit file
vi filename.txt

# Basic vi commands:
# Press 'i' - Enter insert mode (now you can type)
# Press Esc - Return to command mode
# :w - Save file
# :q - Quit
# :wq - Save and quit
# :q! - Quit without saving
# /search_term - Search
# :set number - Show line numbers
```

**Real Azure example:**

```bash
# Edit nginx config
sudo nano /etc/nginx/nginx.conf
# Make changes, Ctrl+O to save, Ctrl+X to exit

# Edit hosts file
sudo nano /etc/hosts

# Quick edit of script
nano deploy.sh
```

---

## System Information

### Operating System Info

```bash
# Show OS information
cat /etc/os-release

# Show kernel version
uname -r

# Show all system information
uname -a

# Show hostname
hostname

# Windows equivalent: Get-ComputerInfo, systeminfo
```

### Hardware Info

```bash
# Show CPU information
lscpu

# Show memory usage
free -h

# Show disk information
lsblk

# Show PCI devices
lspci

# Windows equivalent: Get-WmiObject, wmic
```

### Uptime & Load

```bash
# Show uptime and load average
uptime

# Show detailed system stats
vmstat 1 5

# Windows equivalent: Get-Uptime, Performance Monitor
```

**Real Azure example:**

```bash
# Check Azure VM details
cat /etc/os-release
# NAME="Ubuntu"
# VERSION="22.04.3 LTS (Jammy Jellyfish)"

# Check CPU cores
lscpu | grep "^CPU(s)"
# CPU(s): 4

# Check memory
free -h
#               total        used        free      shared  buff/cache   available
# Mem:           15Gi       2.1Gi       11Gi       8.0Mi       2.5Gi       13Gi

# Check uptime
uptime
# 10:30:15 up 45 days,  3:22,  1 user,  load average: 0.23, 0.45, 0.51
```

---

## Azure-Specific Commands

### Azure CLI (az)

```bash
# Login to Azure (opens browser)
az login

# List subscriptions
az account list --output table

# Set subscription
az account set --subscription "My Subscription"

# List VMs
az vm list --output table

# Start VM
az vm start --resource-group rg-prod --name vm-web-01

# Stop VM (deallocate)
az vm deallocate --resource-group rg-prod --name vm-web-01

# Run command on VM
az vm run-command invoke \
  --resource-group rg-prod \
  --name vm-web-01 \
  --command-id RunShellScript \
  --scripts "systemctl status nginx"
```

### Cloud-Init (Azure VM Initialization)

```bash
# Check cloud-init status
cloud-init status

# View cloud-init logs
sudo cat /var/log/cloud-init.log

# Re-run cloud-init
sudo cloud-init clean
sudo cloud-init init
```

### Azure VM Extensions

```bash
# List installed extensions
ls -la /var/lib/waagent/

# Check Azure Agent status
systemctl status walinuxagent

# View extension logs
sudo cat /var/log/azure/*
```

---

## Troubleshooting Patterns

### Pattern 1: Service Won't Start

```bash
# Step 1: Check service status
systemctl status nginx

# Step 2: View recent logs
journalctl -u nginx -n 50

# Step 3: Check for port conflicts
sudo netstat -tuln | grep :80

# Step 4: Check config file syntax
nginx -t

# Step 5: Try starting manually
sudo nginx
```

### Pattern 2: Permission Denied

```bash
# Step 1: Check current permissions
ls -la /path/to/file

# Step 2: Check ownership
ls -l /path/to/file

# Step 3: Fix permissions
chmod +x script.sh

# Step 4: Fix ownership
sudo chown azureuser:azureuser file.txt
```

### Pattern 3: Disk Full

```bash
# Step 1: Check disk usage
df -h

# Step 2: Find large directories
sudo du -sh /* | sort -hr | head -10

# Step 3: Find large files
sudo find / -type f -size +100M

# Step 4: Clean up
sudo find /var/log -name "*.log" -mtime +30 -delete
sudo apt autoremove
```

### Pattern 4: Process Using All CPU

```bash
# Step 1: Find the process
ps aux --sort=-%cpu | head -10

# Step 2: Get more details
top

# Step 3: Check what it's doing
sudo strace -p <PID>

# Step 4: Kill if necessary
sudo kill <PID>
```

### Pattern 5: Can't Connect to Service

```bash
# Step 1: Check if service is running
systemctl status nginx

# Step 2: Check if port is listening
sudo netstat -tuln | grep :80

# Step 3: Test locally
curl http://localhost

# Step 4: Check firewall
sudo iptables -L

# Step 5: Check Azure NSG rules (via portal or CLI)
az network nsg rule list --resource-group rg-prod --nsg-name nsg-vm
```

---

## Windows â†’ Linux Command Translation

| Task | Windows | Linux |
|------|---------|-------|
| List files | `dir` | `ls -la` |
| Change directory | `cd` | `cd` |
| Copy file | `copy` | `cp` |
| Move file | `move` | `mv` |
| Delete file | `del` | `rm` |
| Create directory | `mkdir` | `mkdir` |
| Remove directory | `rmdir /s` | `rm -rf` |
| View text file | `type` | `cat` |
| Find text | `findstr` | `grep` |
| List processes | `tasklist` | `ps aux` |
| Kill process | `taskkill` | `kill` |
| Network config | `ipconfig` | `ip addr` |
| Disk usage | `dir /s` | `du -sh` |
| Free space | N/A | `df -h` |
| Services | `services.msc` | `systemctl` |
| Edit file | `notepad` | `nano` / `vi` |
| Permissions | `icacls` | `chmod` |
| Ownership | `takeown` | `chown` |
| Environment vars | `set` | `env` |
| Path | `echo %PATH%` | `echo $PATH` |

---

## Quick Reference: Most Common Commands

### Daily Use (you'll use these constantly)

```bash
ls -la              # List files
cd /path            # Change directory
pwd                 # Where am I?
cat file.txt        # Read file
tail -f app.log     # Monitor log
grep "error" file   # Search text
sudo command        # Run as admin
systemctl status    # Check service
df -h               # Disk space
ps aux              # List processes
```

### Weekly Use (troubleshooting, maintenance)

```bash
chmod +x script.sh          # Fix permissions
sudo chown user:group file  # Fix ownership
kill -9 PID                 # Kill process
find /path -name "*.log"    # Find files
du -sh *                    # Directory sizes
netstat -tuln               # Open ports
journalctl -u service -n 50 # Service logs
apt update && apt upgrade   # Update system
```

### Monthly Use (system administration)

```bash
sudo adduser username               # Create user
sudo usermod -aG sudo username      # Grant admin
sudo apt autoremove                 # Clean packages
sudo find /var/log -mtime +30 -delete  # Clean logs
lsblk                               # List disks
sudo mount /dev/sdc1 /mnt/data     # Mount disk
free -h                             # Memory usage
uname -a                            # System info
```

---

## Keyboard Shortcuts (Essential)

### Terminal Navigation

```
Ctrl+C          - Cancel current command
Ctrl+D          - Exit terminal
Ctrl+L          - Clear screen
Ctrl+A          - Move to start of line
Ctrl+E          - Move to end of line
Ctrl+U          - Delete from cursor to start
Ctrl+K          - Delete from cursor to end
Ctrl+R          - Search command history
Tab             - Auto-complete
â†‘/â†“             - Previous/next command
```

### Text Editing (nano)

```
Ctrl+O          - Save
Ctrl+X          - Exit
Ctrl+W          - Search
Ctrl+K          - Cut line
Ctrl+U          - Paste
```

---

## Common Mistakes to Avoid

### 1. Running Commands as Root When You Shouldn't

```bash
# âŒ Bad: Creates files owned by root
sudo echo "test" > file.txt

# âœ… Good: Files stay owned by your user
echo "test" > file.txt
```

### 2. Using `rm -rf` Without Double-Checking

```bash
# âŒ VERY BAD: Deletes everything
sudo rm -rf /

# âœ… Good: Always verify path first
ls -la /path/to/delete/
sudo rm -rf /path/to/delete/
```

### 3. Forgetting `-i` with Dangerous Commands

```bash
# âŒ Bad: No confirmation
rm important_file.txt

# âœ… Good: Asks for confirmation
rm -i important_file.txt
```

### 4. Not Using `sudo` When Needed

```bash
# âŒ Bad: Permission denied
systemctl restart nginx

# âœ… Good: Has permissions
sudo systemctl restart nginx
```

### 5. Case Sensitivity

```bash
# Linux is case-sensitive!
cd /Home/azureuser   # âŒ Fails
cd /home/azureuser   # âœ… Works

grep "Error" log.txt  # âŒ Won't find "error"
grep -i "error" log.txt  # âœ… Finds any case
```

---

## Practice Exercises (Use Azure Cloud Shell)

### Exercise 1: Navigation

```bash
pwd
ls -la
cd /usr
ls
cd local
pwd
cd
pwd
```

### Exercise 2: File Operations

```bash
echo "Hello Azure" > test.txt
cat test.txt
cp test.txt test2.txt
mv test2.txt renamed.txt
ls -la
rm renamed.txt
ls -la
```

### Exercise 3: Search and Filter

```bash
cat /etc/os-release
grep "NAME" /etc/os-release
cat /etc/os-release | grep -i "version"
```

### Exercise 4: Process Management

```bash
ps aux | head -10
ps aux | grep bash
top
# Press q to quit
```

### Exercise 5: Permissions

```bash
touch myfile.txt
ls -l myfile.txt
chmod 755 myfile.txt
ls -l myfile.txt
chmod 644 myfile.txt
ls -l myfile.txt
```

---

## Next Steps

**Bookmark this page.** You'll reference it constantly.

**Practice in Azure Cloud Shell** (it's free, no VM needed):
1. Go to [portal.azure.com](https://portal.azure.com)
2. Click Cloud Shell icon
3. Choose Bash
4. Run commands from this guide

**Learn more:**
- [10 Linux Commands That Will Save Your Azure Career](https://azure-noob.com/blog/linux-commands-azure-admin-career/) (shorter, scenario-focused)
- Official Linux documentation: [linux.die.net](https://linux.die.net/)
- Azure Linux VMs: [docs.microsoft.com/azure/virtual-machines/linux](https://docs.microsoft.com/en-us/azure/virtual-machines/linux/)

---

## Final Thought

**You don't need to memorize all this.** Nobody does.

You need to:
1. Understand what's possible
2. Know where to find the answer (this page)
3. Practice the most common commands until they're muscle memory

The Windows admins who thrive in Azure are the ones who embrace Linux as a toolâ€”not a threat.

**Start with the top 10 commands. Everything else will come with practice.**
