---
title: "10 Linux Commands That Will Save Your Azure Career"
date: 2025-11-03
summary: "You've been avoiding Linux. But Azure Cloud Shell runs Linux. Your VMs run Linux. AKS runs Linux. Here are the 10 commands you actually need to know—and why Windows admins who ignore this are limiting their careers."
tags: ["Azure", "Linux", "Cloud Shell", "AKS", "Career"]
cover: "/static/images/hero/linux-commands-azure-career.svg"
---

You're a Windows admin. You know PowerShell, Active Directory, Group Policy. You've built a career on Microsoft technologies.

Then Azure came along and changed the rules.

**The uncomfortable truth:** Modern Azure administration increasingly requires Linux knowledge. Not because Microsoft wants to punish you, but because:

- Azure Cloud Shell runs **Linux** (not Windows)
- 60%+ of Azure VMs run **Linux** (not Windows Server)
- Azure Kubernetes Service runs **Linux** containers
- Azure DevOps agents default to **Ubuntu** (not Windows)
- Azure Container Instances run **Linux** containers

**You can't avoid it anymore.**

The good news? You don't need to become a Linux expert. You need to know **10 commands** that cover 90% of what Azure admins actually do.

Here they are.

---

## The Reality Check

**Scenario 1:** You SSH into an Azure Ubuntu VM because a critical app is down. You stare at the terminal. What now?

**Scenario 2:** You're troubleshooting an AKS pod failure. kubectl logs shows a file permission error. How do you check permissions on a Linux container?

**Scenario 3:** Cloud Shell is your only access to Azure because the portal is slow. You need to edit a bash script. What editor do you use?

**If you don't know the answers, you're limiting your Azure career.**

---

## Command 1: `ls -la` (What's Actually Here?)

**What it does:** Lists files and directories with full details (permissions, ownership, hidden files)

**Why it matters:** The first thing you do when SSH'ing into any Linux VM is figure out what's there.

**Windows equivalent:** `dir /a` (but less useful)

**Real Azure scenario:**

```bash
# You SSH into an Azure Ubuntu VM
ssh azureuser@20.12.34.56

# First command - see everything
ls -la

# Output shows:
drwxr-xr-x  5 azureuser azureuser 4096 Nov  3 10:30 .
drwxr-xr-x 12 root      root      4096 Oct 15 08:22 ..
-rw-------  1 azureuser azureuser 1234 Nov  3 09:15 .bash_history
-rw-r--r--  1 azureuser azureuser  220 Oct 15 08:22 .bash_logout
drwx------  2 azureuser azureuser 4096 Nov  2 14:30 .ssh
-rwxr-xr-x  1 azureuser azureuser 2048 Nov  3 10:30 deploy.sh
```

**What this tells you:**
- `drwx` = directory
- `-rwx` = file (executable)
- `azureuser` = owner
- `.ssh` = hidden directory (starts with .)
- `deploy.sh` = has execute permissions

**Common mistake:** Running just `ls` and wondering why you don't see hidden files like `.ssh` or `.bashrc`

---

## Command 2: `cd` and `pwd` (Where Am I?)

**What it does:** 
- `cd` = change directory
- `pwd` = print working directory (shows current location)

**Why it matters:** Linux file paths are different from Windows. You need to know where you are.

**Windows equivalent:** `cd` (same command, different paths)

**Real Azure scenario:**

```bash
# You're lost in the filesystem
pwd
# Output: /home/azureuser

# Navigate to app directory
cd /var/www/webapp

# Verify location
pwd
# Output: /var/www/webapp

# Go up one level
cd ..

# Go back to home directory (two ways)
cd ~
cd /home/azureuser
```

**Azure-specific paths you'll use:**
- `/home/azureuser` - Your user home
- `/var/log` - System and app logs
- `/etc` - Configuration files
- `/var/www` - Web app files (if running nginx/apache)
- `/mnt` - Mounted Azure disks

**Common mistake:** Using backslashes `\` instead of forward slashes `/` (Windows habit)

---

## Command 3: `cat` and `tail -f` (Read Files Fast)

**What it does:**
- `cat` = dump entire file to screen
- `tail -f` = show last 10 lines and follow in real-time

**Why it matters:** You need to read logs, config files, and scripts constantly.

**Windows equivalent:** 
- `type` (cat)
- `Get-Content -Tail 10 -Wait` (tail -f)

**Real Azure scenario:**

```bash
# Quick look at a config file
cat /etc/nginx/nginx.conf

# Check the last 50 lines of system log
tail -n 50 /var/log/syslog

# Monitor application log in real-time (CRITICAL for troubleshooting)
tail -f /var/log/webapp/app.log

# Watch multiple logs at once
tail -f /var/log/webapp/*.log
```

**Why `tail -f` is essential:** When debugging a failing app on Azure VM, you run `tail -f` on the app log, then trigger the failure. You see errors in real-time instead of guessing.

**Common mistake:** Using `cat` on massive log files (crashes your terminal). Use `tail` or `less` instead.

---

## Command 4: `grep` (Find Anything Fast)

**What it does:** Searches for text patterns in files or output

**Why it matters:** Finding specific errors in 50,000-line log files

**Windows equivalent:** `Select-String` (PowerShell) or `findstr` (cmd)

**Real Azure scenario:**

```bash
# Find all "ERROR" lines in log
grep "ERROR" /var/log/webapp/app.log

# Case-insensitive search
grep -i "error" /var/log/webapp/app.log

# Show 3 lines before and after match (context)
grep -C 3 "Connection refused" /var/log/syslog

# Search all logs in directory
grep -r "OutOfMemory" /var/log/

# Pipe output from other commands
tail -n 1000 /var/log/syslog | grep "azure"
```

**The Azure admin power move:**

```bash
# Find all failed authentication attempts in the last 1000 log lines
tail -n 1000 /var/log/auth.log | grep "Failed password"

# Find when a specific service last restarted
grep "nginx" /var/log/syslog | grep "start"
```

**Common mistake:** Forgetting `-i` for case-insensitive search (Linux is case-sensitive by default)

---

## Command 5: `chmod` (Fix Permissions)

**What it does:** Changes file/directory permissions (read, write, execute)

**Why it matters:** "Permission denied" errors are the #1 Linux gotcha for Windows admins

**Windows equivalent:** Right-click → Properties → Security (but completely different model)

**Real Azure scenario:**

```bash
# Your deployment script won't run
./deploy.sh
# Error: Permission denied

# Check current permissions
ls -l deploy.sh
# Output: -rw-r--r-- (no execute permission)

# Add execute permission
chmod +x deploy.sh

# Now it runs
./deploy.sh
# Success!

# Common permission fixes:
chmod 644 config.json    # rw-r--r-- (readable by all, writable by owner)
chmod 755 script.sh      # rwxr-xr-x (executable by all, writable by owner)
chmod 600 private.key    # rw------- (only owner can read/write)
```

**The permission numbers:**
- `7` = rwx (read, write, execute)
- `6` = rw- (read, write)
- `5` = r-x (read, execute)
- `4` = r-- (read only)

**First digit** = owner, **second** = group, **third** = everyone

**Common mistake:** Setting `chmod 777` (full permissions for everyone) - major security risk. Use `755` for scripts, `644` for files.

---

## Command 6: `sudo` (I Need Admin Rights)

**What it does:** Runs commands as administrator (root user)

**Why it matters:** Most system operations require elevated permissions

**Windows equivalent:** "Run as Administrator"

**Real Azure scenario:**

```bash
# Try to restart nginx without sudo
systemctl restart nginx
# Error: Permission denied

# Run with sudo
sudo systemctl restart nginx
# Success!

# Install package
sudo apt update
sudo apt install nginx -y

# Edit system config file
sudo nano /etc/nginx/nginx.conf

# Become root user (use sparingly)
sudo -i
```

**Azure VM default:** The `azureuser` account you create has sudo access (it's in the `sudo` group)

**Common mistake:** Running `sudo` on commands that don't need it (creates files owned by root that you can't edit later)

---

## Command 7: `systemctl` (Manage Services)

**What it does:** Start, stop, restart, and check status of Linux services

**Why it matters:** Apps run as services. You need to control them.

**Windows equivalent:** `services.msc` or `Get-Service` / `Restart-Service`

**Real Azure scenario:**

```bash
# Check if nginx is running
systemctl status nginx

# Start nginx
sudo systemctl start nginx

# Restart after config change
sudo systemctl restart nginx

# Enable service to start on boot (important!)
sudo systemctl enable nginx

# Stop service
sudo systemctl stop nginx

# Check all failed services
systemctl --failed
```

**The Azure troubleshooting pattern:**

```bash
# App not responding?
# Step 1: Check service status
systemctl status myapp

# Step 2: Check logs
journalctl -u myapp -n 50

# Step 3: Restart if needed
sudo systemctl restart myapp

# Step 4: Verify it restarted
systemctl status myapp
```

**Common mistake:** Forgetting to `enable` a service after installation - it won't survive VM reboots

---

## Command 8: `ps aux` and `kill` (Process Management)

**What it does:**
- `ps aux` = list all running processes
- `kill` = stop a process

**Why it matters:** Runaway processes eating CPU, memory leaks, hung applications

**Windows equivalent:** Task Manager or `Get-Process` / `Stop-Process`

**Real Azure scenario:**

```bash
# What's eating all my CPU?
ps aux | grep -v "0.0" | sort -k3 -rn | head -10

# Find process by name
ps aux | grep nginx

# Output shows:
# USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
# www-data  1234  5.0  2.1 123456 87654 ?       S    10:30   0:05 nginx

# Kill process by PID
sudo kill 1234

# Force kill if it won't die
sudo kill -9 1234

# Kill all processes matching name
sudo pkill nginx
```

**The Azure admin emergency pattern:**

```bash
# Out of memory! Find the culprit
ps aux --sort=-%mem | head -10

# Kill the memory hog
sudo kill -9 <PID>
```

**Common mistake:** Using `kill -9` first (force kill) - try regular `kill` first, it's cleaner

---

## Command 9: `df -h` and `du -sh` (Disk Space)

**What it does:**
- `df -h` = disk free space (entire system)
- `du -sh` = disk usage (specific directories)

**Why it matters:** "No space left on device" errors kill apps

**Windows equivalent:** `Get-Volume` or right-click drive → Properties

**Real Azure scenario:**

```bash
# Check disk space on all mounted drives
df -h

# Output:
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1        30G   28G   2G  93% /
/dev/sdb1       100G   45G  55G  45% /mnt/data

# PROBLEM: Root partition at 93%!

# Find what's eating space
cd /
sudo du -sh * | sort -hr | head -10

# Output:
15G    /var
8G     /usr
3G     /home
2G     /opt

# Drill down
cd /var
sudo du -sh * | sort -hr | head -10

# Output:
12G    /var/log
2G     /var/cache
1G     /var/lib

# Found it! Logs are massive
# Clean up old logs
sudo find /var/log -name "*.log" -mtime +30 -delete
```

**Common mistake:** Not monitoring disk space until it's too late (VMs grind to a halt at 100%)

---

## Command 10: `nano` or `vi` (Edit Files Without Leaving Terminal)

**What it does:** Text editors that work in SSH sessions (no GUI needed)

**Why it matters:** You need to edit config files, scripts, and cron jobs on remote VMs

**Windows equivalent:** Notepad (but you can't SSH to Notepad)

**Real Azure scenario:**

```bash
# Edit a config file with nano (easier for beginners)
nano /etc/nginx/nginx.conf

# Edit with vi (more powerful, steeper learning curve)
vi /etc/nginx/nginx.conf

# If file needs sudo:
sudo nano /etc/nginx/nginx.conf
```

**Nano basics (what you need to know):**
- `Ctrl+O` = save file
- `Ctrl+X` = exit
- `Ctrl+W` = search
- That's it. Really.

**Vi basics (survival mode):**
- Press `i` = insert mode (now you can type)
- Press `Esc` = back to command mode
- Type `:wq` = write and quit
- Type `:q!` = quit without saving

**The Azure reality:** Use `nano` unless you're already a vi expert. Life's too short.

**Common mistake:** Opening a file in `vi`, not knowing how to exit, and force-closing your SSH session

---

## Bonus: The One Command That Saves Everything

```bash
history
```

**What it does:** Shows your command history (last 500-1000 commands)

**Why it matters:** You ran a working command 2 hours ago. What was it?

```bash
# Show history
history

# Search history
history | grep "nginx"

# Re-run command #342 from history
!342

# Re-run last command
!!

# Re-run last command with sudo
sudo !!
```

**Pro tip:** Add to `.bashrc` to make history unlimited:

```bash
echo 'HISTSIZE=10000' >> ~/.bashrc
echo 'HISTFILESIZE=10000' >> ~/.bashrc
```

---

## The Azure Admin's Linux Survival Kit

These 10 commands handle:
- ✅ Navigating filesystems (`ls`, `cd`, `pwd`)
- ✅ Reading files and logs (`cat`, `tail`, `grep`)
- ✅ Fixing permissions (`chmod`, `sudo`)
- ✅ Managing services (`systemctl`)
- ✅ Troubleshooting processes (`ps`, `kill`)
- ✅ Monitoring disk space (`df`, `du`)
- ✅ Editing configs (`nano`, `vi`)

**That's 90% of what you'll do on Azure Linux VMs.**

---

## Real-World Azure Scenarios (Putting It Together)

### Scenario 1: Web App Down on Azure Ubuntu VM

```bash
# SSH in
ssh azureuser@myvm.eastus.cloudapp.azure.com

# Check if nginx is running
systemctl status nginx
# Not running!

# Check logs for errors
tail -n 50 /var/log/nginx/error.log | grep -i "error"
# Found: "Permission denied on /var/www/html"

# Check permissions
ls -la /var/www/html
# Wrong owner!

# Fix ownership
sudo chown -R www-data:www-data /var/www/html

# Start nginx
sudo systemctl start nginx

# Verify
systemctl status nginx
# Running!
```

### Scenario 2: AKS Node Running Out of Disk Space

```bash
# Connect to AKS node (using kubectl debug or SSH)
kubectl debug node/aks-nodepool-12345 -it --image=ubuntu

# Check disk usage
df -h
# /var at 95%!

# Find the culprit
cd /var
sudo du -sh * | sort -hr | head -5
# /var/log/containers is 30GB!

# Clean up old container logs
sudo find /var/log/containers -name "*.log" -mtime +7 -delete

# Verify space freed
df -h
# /var now at 65% - problem solved
```

### Scenario 3: Cloud Shell Script Debugging

```bash
# Your bash script fails in Cloud Shell
./deploy-resources.sh
# Error: Permission denied

# Fix permissions
chmod +x deploy-resources.sh

# Run again
./deploy-resources.sh
# Error: "az command not found" inside script

# Check if Azure CLI is available
which az
# /usr/bin/az - it's there

# Edit script to debug
nano deploy-resources.sh

# Add at top:
#!/bin/bash
set -e  # Exit on error
set -x  # Print each command

# Save and run
./deploy-resources.sh
# Now you see exactly where it fails
```

---

## What You Don't Need to Learn (Yet)

Windows admins panic about Linux. You don't need to know:
- ❌ Advanced shell scripting (PowerShell skills transfer)
- ❌ Linux networking deep dives (Azure handles this)
- ❌ Kernel configuration (Azure VMs are pre-configured)
- ❌ Package compilation (use apt/yum packages)

**Focus on the 10 commands above.** Everything else is Google-able when you need it.

---

## The Career Reality

**Azure jobs increasingly require Linux knowledge:**
- "Azure Administrator" job posts mention Linux: 65%
- "DevOps Engineer" roles assume Linux: 90%+
- Kubernetes expertise = Linux expertise
- Salary premium for Azure admins with Linux skills: ~15%

**You don't need to abandon Windows.** You need to be **bilingual** (Windows + Linux).

---

## Practice Right Now (Azure Cloud Shell)

You don't need to spin up a VM. Azure Cloud Shell runs Linux **right now**.

**Try this:**

1. Go to [portal.azure.com](https://portal.azure.com)
2. Click the Cloud Shell icon (top-right)
3. Choose Bash (not PowerShell)
4. Run all 10 commands from this post

**5-minute practice session:**

```bash
# Command 1-2: Navigate
pwd
ls -la
cd /usr
pwd

# Command 3: Read files
cat /etc/os-release

# Command 4: Search
grep "Azure" /etc/os-release

# Command 5: Check permissions (can't change in Cloud Shell, read-only filesystem)
ls -la ~

# Command 6: Sudo (not needed in Cloud Shell)

# Command 7: Services (limited in Cloud Shell)

# Command 8: Processes
ps aux | head -10

# Command 9: Disk space
df -h

# Command 10: Edit file
cd ~
echo "Hello Azure" > test.txt
nano test.txt
cat test.txt
```

**Result:** You just ran Linux commands in production Azure environment. No VM needed.

---

## Next Steps

**Want the deep dive?** I wrote a comprehensive Linux cheat sheet specifically for Azure admins:
→ [The Complete Linux Cheat Sheet for Azure Admins](https://azure-noob.com/blog/linux-cheat-sheet-azure-admins/)

It includes:
- Every command with Azure-specific examples
- Windows → Linux command translations
- Troubleshooting patterns for common Azure scenarios
- Copy/paste ready scripts
- File system layout for Azure VMs

**Or just bookmark this post.** These 10 commands will handle 90% of your Linux needs on Azure.

---

## Final Thought

You're not betraying Windows by learning Linux. You're **future-proofing your Azure career**.

The admins who refuse to learn Linux basics are the same ones who refused to learn PowerShell in 2010. Where are they now?

Don't be that person.

**10 commands. 30 minutes of practice. Career saved.**

Go open Cloud Shell and try them right now. Your future self will thank you.
