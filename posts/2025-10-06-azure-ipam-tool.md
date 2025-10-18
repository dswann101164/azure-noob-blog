---
title: "Azure IPAM Tool for Multi-Subscription Environments | Free Open Source IP Tracking"
date: 2025-10-06
summary: "Track IPs across Azure subscriptions with this free IPAM tool. Search IPs, detect conflicts, reserve ranges, visualize network topology. Built for enterprise consolidation managing 44+ subscriptions. Full source code on GitHub."
tags: ["Azure", "FinOps", "Governance", "Migration", "Networking", "Open Source"]
cover: "static/images/hero/azure-ipam.png"
---

## The Problem Leadership Doesn't Understand

Enterprise mergers consolidate multiple Azure subscriptions, AD domains, and hundreds of applications into one environment. Leadership wants a migration plan. Questions that need answers:

- Which subnet contains 10.5.2.45?
- Do we have IP conflicts between the two merged environments?
- Where can I allocate 10.8.0.0/24 for the new firewall rules?
- Which subnets are approaching capacity?

**Azure's answer:** Click through 44 subscriptions one at a time in the portal.

That's not a plan. That's career suicide.

## What Azure Gives You (And Why It's Not Enough)

Azure has IP management. Sort of.

**Azure Portal:**
- Shows one subscription at a time
- No cross-subscription search
- Can't answer "find me available /24 blocks across all subscriptions"
- No way to reserve IPs for future use

**Azure Resource Graph:**
- Can query across subscriptions
- Returns resource data, not IP allocation details
- Requires manual KQL queries for every lookup
- No visualization of network topology

**Third-party IPAM tools:**
- Enterprise pricing (InfoBlox starts at $10k+/year)
- Designed for on-premises networks, not cloud-native architectures
- Overkill for Azure-only environments
- Require ongoing license negotiations with procurement

**What I needed:**
- Real-time IP utilization across all subscriptions
- IP address search (which subnet contains X?)
- Reservation system for migration planning
- Capacity alerts before subnets fill up
- Free (no budget approvals during a merger)

If you can't build it, you can't manage it. So I built it.

## The Solution: Azure IPAM Tool

Flask-based IPAM tool that scans all Azure subscriptions you have access to and gives you real-time IP visibility.

**Core capabilities:**
- Multi-subscription IP tracking
- IP address search across all VNets
- Reservation system for planning migrations
- Capacity alerts (>75%, >90% utilization)
- Network topology visualization
- Export reports for leadership

**Tech stack:**
- Python + Flask (lightweight, no framework bloat)
- Azure SDK for Python (resource scanning)
- D3.js (network topology visualization)
- Browser localStorage (reservation tracking)

**GitHub repo:** [https://github.com/dswann101164/azure-ipam](https://github.com/dswann101164/azure-ipam)

## How It Works

### 1. Multi-Subscription Discovery

Azure SDK automatically finds all subscriptions your app registration has access to:

```python
from azure.identity import DefaultAzureCredential
from azure.mgmt.subscription import SubscriptionClient

credential = DefaultAzureCredential()
subscription_client = SubscriptionClient(credential)

subscriptions = []
for sub in subscription_client.subscriptions.list():
    subscriptions.append({
        'id': sub.subscription_id,
        'name': sub.display_name
    })
```

### 2. VNet and Subnet Enumeration

For each subscription, scan all VNets and subnets:

```python
from azure.mgmt.network import NetworkManagementClient

def scan_subscription(subscription_id):
    network_client = NetworkManagementClient(credential, subscription_id)
    
    vnets = []
    for vnet in network_client.virtual_networks.list_all():
        subnets = []
        for subnet in vnet.subnets:
            # Calculate actual available IPs (Azure reserves 5 per subnet)
            total_ips = 2 ** (32 - int(subnet.address_prefix.split('/')[1]))
            reserved_ips = 5  # Azure reserves first 3 + last 2
            available_ips = total_ips - reserved_ips
            
            # Count IPs in use
            used_ips = len(subnet.ip_configurations) if subnet.ip_configurations else 0
            
            subnets.append({
                'name': subnet.name,
                'address_prefix': subnet.address_prefix,
                'total_ips': total_ips,
                'used_ips': used_ips,
                'available_ips': available_ips - used_ips,
                'utilization': (used_ips / available_ips) * 100
            })
        
        vnets.append({
            'name': vnet.name,
            'address_space': vnet.address_space.address_prefixes,
            'subnets': subnets
        })
    
    return vnets
```

### 3. IP Address Search

Search across all subscriptions to find which subnet contains a specific IP:

```python
import ipaddress

def find_ip(ip_address, all_vnets):
    ip = ipaddress.ip_address(ip_address)
    results = []
    
    for subscription in all_vnets:
        for vnet in subscription['vnets']:
            for subnet in vnet['subnets']:
                network = ipaddress.ip_network(subnet['address_prefix'])
                if ip in network:
                    results.append({
                        'subscription': subscription['name'],
                        'vnet': vnet['name'],
                        'subnet': subnet['name'],
                        'cidr': subnet['address_prefix'],
                        'utilization': subnet['utilization']
                    })
    
    return results
```

### 4. Capacity Alerts

Automatically flag subnets approaching capacity:

```python
def get_capacity_alerts(all_vnets):
    critical = []  # >90% utilization
    warning = []   # 75-90% utilization
    
    for subscription in all_vnets:
        for vnet in subscription['vnets']:
            for subnet in vnet['subnets']:
                utilization = subnet['utilization']
                
                if utilization > 90:
                    critical.append(subnet)
                elif utilization > 75:
                    warning.append(subnet)
    
    return {'critical': critical, 'warning': warning}
```

### 5. Reservation System

Track IP ranges reserved for future use (stored in browser localStorage for simplicity):

```javascript
// Reserve an IP range
function reserveIP(cidr, purpose, owner, expiration) {
    const reservations = JSON.parse(localStorage.getItem('ipReservations') || '[]');
    
    reservations.push({
        id: Date.now(),
        cidr: cidr,
        purpose: purpose,
        owner: owner,
        expiration: expiration,
        created: new Date().toISOString()
    });
    
    localStorage.setItem('ipReservations', JSON.stringify(reservations));
}

// Check if IP overlaps with existing reservations
function checkReservation(cidr) {
    const reservations = JSON.parse(localStorage.getItem('ipReservations') || '[]');
    
    for (let reservation of reservations) {
        if (cidrsOverlap(cidr, reservation.cidr)) {
            return reservation;
        }
    }
    
    return null;
}
```

## Real-World Usage: Bank Merger Scenario

### Before: The IP Conflict Discovery Problem

**Scenario:** Need to migrate acquired company's finance application to primary Azure environment.

**Questions that couldn't be answered:**
- Does the acquired company's 10.50.0.0/16 network overlap with existing infrastructure?
- Where can I allocate a new /24 for the migration subnet?
- Which existing subnets have capacity for 50 new VMs?

**Old process:**
1. Open Azure Portal
2. Click through every subscription manually
3. Screenshot each VNet's address space
4. Build Excel spreadsheet to track IPs
5. Pray the spreadsheet is accurate when firewall team asks questions

**Time required:** 6-8 hours  
**Accuracy:** Maybe 80% (always missed something)  
**Confidence level:** Low

### After: The IPAM Tool in Action

**Same scenario with IPAM tool:**

1. **Dashboard shows immediate conflicts:**
   - Acquired company's 10.50.0.0/16 overlaps with production DMZ
   - 3 subnets >90% capacity flagged for expansion
   - Total available IP capacity across all subscriptions visible at a glance

2. **IP search finds available space:**
   - Search for "10.60.0.0/24"
   - Tool confirms no conflicts
   - Shows 3 VNets with capacity for this range

3. **Reserve IPs for migration:**
   - Reserve 10.60.0.0/24 for "Finance Migration - Ticket SRV-4521"
   - Set expiration for Q2 2026 (post-migration)
   - Firewall team can see reservation and plan rules

**Time required:** 15 minutes  
**Accuracy:** 100% (real-time Azure data)  
**Confidence level:** High

### Capacity Planning for Leadership

**Monthly review meeting:**
- Export subnet utilization report
- Show topology visualization of network hierarchy
- Identify 5 subnets needing expansion in next quarter
- Present data-driven capacity plan

**Before:** "We'll probably need more IPs soon."  
**After:** "These 5 specific subnets will hit 90% capacity by March based on current growth."

Leadership loves data. IPAM tool gives you data.

## Screenshots

### Authentication
![Azure AD Login](https://raw.githubusercontent.com/dswann101164/azure-ipam/main/screenshots/01-login.png)
*Enterprise SSO with Azure AD - request required permissions on first login*

### Dashboard Overview
![IP Address Dashboard](https://raw.githubusercontent.com/dswann101164/azure-ipam/main/screenshots/02-dashboard.png)
*Real-time IP scope utilization across all subscriptions*

### IP Address Search
![IP Search](https://raw.githubusercontent.com/dswann101164/azure-ipam/main/screenshots/03-ip-search.png)
*Find available IPs across VNets with subnet filtering*

### Network Browser
![Network Browser](https://raw.githubusercontent.com/dswann101164/azure-ipam/main/screenshots/04-network-browser.png)
*Navigate subscription hierarchy to find specific VNets and subnets*

### IP Reservations
![Reservation Management](https://raw.githubusercontent.com/dswann101164/azure-ipam/main/screenshots/05-reservations.png)
*Reserve IPs for future use with three reservation types: NIC, Private Endpoint, or General*

### Topology View
![Multi-Subscription Topology](https://raw.githubusercontent.com/dswann101164/azure-ipam/main/screenshots/06-topology.png)
*Visual network topology showing relationships across subscriptions*

## Installation and Setup

**Prerequisites:**
- Python 3.8+
- Azure AD App Registration with:
  - Microsoft Graph: `User.Read`
  - Azure Service Management: `user_impersonation`
  - Reader role on target subscriptions

**Quick start:**

```bash
# Clone repo
git clone https://github.com/dswann101164/azure-ipam.git
cd azure-ipam

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Configure .env file
cp .env.example .env
# Add your CLIENT_ID, CLIENT_SECRET, TENANT_ID

# Run
python app.py
# Visit http://localhost:5000
```

Full installation guide with Azure AD setup: [GitHub README](https://github.com/dswann101164/azure-ipam)

## Known Limitations (And Why They Don't Matter Yet)

**Reservation storage uses browser localStorage:**
- Per-browser, not shared across team
- For production with multiple users, implement database storage
- **Why it's fine for now:** Solo architect doing migration planning

**Private endpoint IP consumption is unpredictable:**
- Azure private endpoints consume IPs from subnet address space
- Can't predict exactly which IPs they'll take
- Tool tracks them after creation, but can't reserve specific IPs ahead of time
- **Why it matters:** Plan extra capacity in subnets with private endpoints

**Scanning many subscriptions takes time:**
- Initial page load can be slow with large environments
- **Future improvement:** Background job queue for enterprises with dozens of subscriptions
- **Why it's acceptable:** Even 60 seconds beats 6 hours of manual work

**No automatic refresh:**
- Data is fetched on page load
- For rapidly changing environments, implement auto-refresh
- **Why it's fine:** IP changes aren't that frequent in production

## Technical Lessons Learned

### Lesson 1: Azure Reserves 5 IPs Per Subnet

Every Azure subnet reserves:
- First 3 IPs (network, gateway, Azure DNS)
- Last 2 IPs (broadcast, future use)

**Impact on calculations:**
- /24 subnet = 256 total IPs
- Azure reserves 5
- Actual usable IPs = 251

Always subtract reserved IPs in your utilization math. Don't trust raw IP counts.

### Lesson 2: Private Endpoints Break Traditional IPAM

Private endpoints consume IPs from your subnet, but:
- You don't specify which IP they use
- Azure picks an available IP automatically
- Can't reserve IPs for future private endpoints

**Workaround:** Allocate entire subnets for private endpoints, track at subnet level.

### Lesson 3: Concurrent API Calls Speed Everything Up

Scanning many subscriptions serially can take minutes.  
Scanning with Python's `concurrent.futures` brings it down significantly.

```python
from concurrent.futures import ThreadPoolExecutor

def scan_all_subscriptions(subscriptions):
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(scan_subscription, subscriptions))
    return results
```

Use threading for I/O-bound operations like API calls.

### Lesson 4: Browser LocalStorage is Good Enough (For Now)

Don't over-engineer early. LocalStorage works for:
- Single-user scenarios
- Rapid prototyping
- Proof of concept

Upgrade to database when:
- Multiple team members need shared reservations
- Audit trail required
- Compliance needs persist data server-side

Start simple. Add complexity only when proven necessary.

## What's Next

**Immediate improvements:**
- Export to CSV for capacity planning spreadsheets
- Email alerts when subnets hit 90% capacity
- CIDR calculator for subnet planning

**Production deployment:**
- Deploy to Azure App Service with managed identity
- Replace localStorage with Azure SQL Database
- Add RBAC for multi-user access
- Implement auto-refresh for real-time monitoring

**Future features:**
- Integration with Azure Firewall rules validation
- NSG rule overlap detection
- Route table conflict identification
- Cost analysis per subnet (FinOps integration)

## Bottom Line

Azure subscription consolidations expose a hard truth: **native tools assume you're managing one subscription at a time.**

When you're consolidating multiple subscriptions during an enterprise merger, you need:
- Cross-subscription visibility
- IP conflict detection
- Capacity planning
- Migration reservation system

This tool solved that problem in 2 weeks of development. Now it saves 6+ hours every time leadership asks about network capacity.

**If you're managing multi-subscription environments, you need IPAM visibility.** Build your own or buy expensive enterprise tools. Either way, you can't consolidate subscriptions without it.

GitHub repo with full source code: [https://github.com/dswann101164/azure-ipam](https://github.com/dswann101164/azure-ipam)

Questions? Hit me up on GitHub issues or via the contact form. I'm documenting everything I learn during this merger at [azure-noob.com](https://azure-noob.com).
