---
title: "Azure Private DNS Resolver Alternative | Fix Private Endpoint DNS in Hybrid Environments"
date: 2025-10-06
summary: "Azure Private DNS Resolver alternative for hybrid environments. Fix private endpoint DNS resolution by duplicating zones in on-prem AD instead of forwarders. Real-world solution managing 1,500+ private endpoints."
tags: ["azure", "private-dns", "dns-resolver", "private-endpoints", "hybrid-cloud", "networking"]
keywords: ["azure private dns resolver", "azure private dns", "hybrid dns azure", "private endpoint dns"]
cover: "static/images/hero/private-endpoint-dns.png"
---

Microsoft's documentation for private endpoint DNS resolution in hybrid environments is comprehensive. It's also complicated.

Conditional forwarders. Azure Private Resolver. DNS forwarding rulesets. Virtual machines running DNS services. Multiple hops between on-prem and Azure.

We don't do any of that.

We duplicate the DNS zones in both places and move on.

## The Problem Microsoft Solves (Correctly)

When you create a private endpoint in Azure, it needs DNS resolution to work:

- **Azure workloads** need to resolve `storage123.privatelink.blob.core.windows.net` → `10.5.2.45`
- **On-prem workloads** need to resolve the same FQDN → same private IP

Microsoft's solution:
1. Azure Private DNS zones linked to VNets (Azure side resolves correctly)
2. On-prem DNS has conditional forwarders pointing to Azure Private Resolver or DNS forwarder VM
3. DNS queries flow: On-prem → Conditional forwarder → Azure DNS forwarder → Azure Private DNS → Response

This works. It's architecturally correct. It's what Microsoft documents.

It's also more complex than necessary if you have existing Active Directory DNS infrastructure.

## Our Pattern: Duplicate the Zones

We create the same `privatelink.*` zones in both Azure Private DNS and on-prem Active Directory DNS.

**Azure side:**
- Private endpoint created
- Azure Private DNS zone: `privatelink.blob.core.windows.net`
- A record added automatically: `storage123.privatelink.blob.core.windows.net` → `10.5.2.45`
- Azure VMs resolve through Azure DNS (168.63.129.16)

**On-prem side:**
- AD DNS zone created: `privatelink.blob.core.windows.net`
- Same A record added manually: `storage123.privatelink.blob.core.windows.net` → `10.5.2.45`
- Domain-joined machines resolve through AD DNS

No forwarders. No cross-environment dependencies. Each side maintains its own zones.

## Why This Works Better for Enterprises

### **1. Clear Team Ownership**

Our environment has separate teams:

**Azure infrastructure team:**
- Builds VMs, joins to domain
- Creates private endpoints
- Documents what was created (FQDN, IP, target resource)
- Hands off to AD team via ticket

**Active Directory team:**
- Manages on-prem DNS infrastructure
- Adds A records to AD DNS based on Azure team documentation
- Maintains DNS records lifecycle

No shared infrastructure to manage. No cross-team coordination on DNS forwarders or Azure Private Resolver deployments.

### **2. Simpler Architecture**

Microsoft's recommended pattern requires:
- Azure Private Resolver (managed service with costs)
- OR DNS forwarder VM in Azure (more infrastructure to manage)
- Conditional forwarders configured on-prem DNS
- DNS forwarding rulesets
- Multiple network hops for resolution

Our pattern requires:
- Azure Private DNS zones (already created with private endpoints)
- Matching zones in on-prem AD DNS
- A records replicated between them

One less layer. One less thing to troubleshoot.

### **3. Works With Existing AD Infrastructure**

Enterprise AD DNS already manages thousands of records. Adding a few more `privatelink.*` zones is not a burden.

Most enterprises already have:
- Mature change control processes for DNS
- Backup and DR for AD DNS
- Monitoring and alerting for DNS services
- Trained staff managing AD infrastructure

Why introduce a new DNS layer (Azure Private Resolver) when existing infrastructure works?

### **4. No Shared Dependencies**

With conditional forwarders, both teams depend on:
- Azure Private Resolver availability
- Network connectivity between on-prem and Azure for DNS queries
- Proper configuration of forwarding rules
- Shared responsibility for troubleshooting

With duplicated zones:
- Azure team owns Azure Private DNS
- AD team owns on-prem AD DNS
- Each works independently
- Failures don't cascade across environments

## The Operational Reality

**How many private endpoints does this pattern scale to?**

We checked using Resource Graph:

```kql
Resources
| where type == "microsoft.network/privateendpoints"
| summarize PrivateEndpointCount = count() by subscriptionId
| order by PrivateEndpointCount desc
```

**Result: Over 1,000 private endpoints across multiple subscriptions**

Breakdown by resource type:
- Storage Accounts (largest portion)
- App Services (second largest)
- Key Vaults
- Data Factory instances
- Plus Synapse, AKS, SQL, Recovery Services Vaults, etc.

**Created over several years.**

Most are created in batches during planned deployments:
- Storage account migrations: dozens of endpoints in one week
- App Service consolidations: 50-100 endpoints in one month
- Not evenly distributed

**Time to maintain AD DNS records:**
- 5 minutes per private endpoint (add A record via change ticket)
- Part of normal deployment process
- Manageable within existing change control workflows

Not overwhelming. Not automated. Just normal enterprise change management.

## When Does This Pattern Break Down?

This pattern works when:
- ✅ You have mature AD DNS infrastructure
- ✅ Private endpoints created through controlled deployments
- ✅ Separate teams with clear handoff processes
- ✅ Change control is acceptable overhead

This pattern struggles when:
- ❌ Private endpoints created constantly by developers (self-service)
- ❌ Need real-time automation (no manual steps)
- ❌ No on-prem AD infrastructure (cloud-native startup)
- ❌ Hundreds of subscriptions with autonomous teams

For cloud-native environments or massive scale, Microsoft's automation-first approach makes more sense.

For enterprises with legacy AD infrastructure and controlled deployments, duplicating zones is simpler.

## The Resource Graph Query

Here's the complete query to inventory all your private endpoints:

```kql
Resources
| where type == "microsoft.network/privateendpoints"
| extend 
    PrivateEndpointName = name,
    ResourceGroup = resourceGroup,
    Location = location,
    SubscriptionName = subscriptionId,
    PrivateIP = properties.customDnsConfigs[0].ipAddresses[0],
    FQDN = properties.customDnsConfigs[0].fqdn,
    TargetResource = properties.privateLinkServiceConnections[0].properties.privateLinkServiceId,
    ConnectionState = properties.privateLinkServiceConnections[0].properties.privateLinkServiceConnectionState.status,
    Subnet = properties.subnet.id
| project 
    PrivateEndpointName,
    SubscriptionName,
    ResourceGroup,
    Location,
    PrivateIP,
    FQDN,
    TargetResource,
    ConnectionState,
    Subnet
| order by PrivateEndpointName asc
```

Run this to see:
- All private endpoints across all subscriptions
- The private IP each one uses
- The FQDN that needs DNS resolution
- What resource it connects to

Export to CSV. Hand to AD team. They have everything needed to add records.

## The Handoff Process

**Azure team creates private endpoint:**

```powershell
# Private endpoint for storage account
$pe = New-AzPrivateEndpoint `
    -Name "pe-storage-prod" `
    -ResourceGroupName "rg-networking" `
    -Location "eastus" `
    -Subnet $subnet `
    -PrivateLinkServiceConnection $connection `
    -PrivateDnsZone $azurePrivateDnsZone

# Document what was created
$documentation = @{
    FQDN = "storage123.privatelink.blob.core.windows.net"
    PrivateIP = $pe.CustomDnsConfigs[0].IpAddresses[0]
    TargetResource = "storage123 (storageAccounts)"
    Zone = "privatelink.blob.core.windows.net"
    CreatedDate = Get-Date
    CreatedBy = $env:USERNAME
}

# Export for AD team
$documentation | Export-Csv -Path "privateendpoint-handoff.csv" -Append
```

**AD team adds record to on-prem DNS:**

```powershell
# Add A record to on-prem AD DNS
Add-DnsServerResourceRecordA `
    -ZoneName "privatelink.blob.core.windows.net" `
    -Name "storage123" `
    -IPv4Address "10.5.2.45" `
    -ComputerName "dc01.contoso.com"
```

Done. Azure resolves through Azure Private DNS. On-prem resolves through AD DNS. No forwarders needed.

## What About DNS Synchronization?

"But what if DNS records get out of sync?"

Valid concern. Here's how we handle it:

**Private endpoint lifecycle is tied to tickets:**
- Private endpoint creation = deployment ticket
- Ticket includes DNS record addition
- Private endpoint deletion = change ticket
- Ticket includes DNS record removal

**If records drift:**
- Resource Graph query shows truth (what exists in Azure)
- Compare against AD DNS records
- Remediate discrepancies during change windows

**Automation option:**
```powershell
# Weekly sync check (read-only)
$azureEndpoints = Get-AzPrivateEndpoint -ResourceGroupName * | 
    Select-Object Name, @{N='FQDN';E={$_.CustomDnsConfigs.Fqdn}}, 
                  @{N='IP';E={$_.CustomDnsConfigs.IpAddresses}}

$adRecords = Get-DnsServerResourceRecord -ZoneName "privatelink.blob.core.windows.net" -ComputerName "dc01"

# Compare and report drift
Compare-Object $azureEndpoints $adRecords -Property FQDN, IP
```

Run weekly. Email discrepancies. Fix during next change window.

Not real-time. Not fully automated. But sufficient for controlled enterprise environments.

## Why Microsoft Doesn't Document This

Microsoft's private endpoint DNS documentation assumes:
- Greenfield deployments (no legacy infrastructure)
- Automation-first mindset (minimal manual processes)
- Single team managing both Azure and networking
- Scale requires real-time synchronization

Enterprise reality:
- Legacy AD infrastructure already in place
- Change control processes are acceptable
- Separate teams with clear boundaries
- Controlled deployments, not constant churn

Microsoft can't document every enterprise pattern. Their docs cover the general case.

This pattern is the enterprise-specific case.

## The Bottom Line

We've managed over 1,000 private endpoints over several years using duplicated DNS zones.

Azure team creates endpoints. AD team maintains on-prem DNS records. No forwarders. No Azure Private Resolver. No shared infrastructure.

Time investment: Manageable within existing change control workflows.

Alternative (Microsoft's way): Deploy Azure Private Resolver, configure conditional forwarders, train both teams on new architecture, troubleshoot DNS forwarding issues, maintain shared infrastructure.

For us, duplicating zones is simpler.

If you have existing AD DNS infrastructure and controlled deployment processes, it might be simpler for you too.

Not what Microsoft documents. But it works.

---

## Resource Graph Queries

**Count private endpoints by subscription:**
```kql
Resources
| where type == "microsoft.network/privateendpoints"
| summarize Count = count() by subscriptionId
| order by Count desc
```

**Find private endpoints by resource type:**
```kql
Resources
| where type == "microsoft.network/privateendpoints"
| extend TargetType = split(properties.privateLinkServiceConnections[0].properties.privateLinkServiceId, '/')[7]
| summarize Count = count() by TargetType
| order by Count desc
```

**List all privatelink DNS zones needed:**
```kql
Resources
| where type == "microsoft.network/privateendpoints"
| extend FQDN = properties.customDnsConfigs[0].fqdn
| extend Zone = substring(FQDN, indexof(FQDN, '.') + 1)
| summarize EndpointCount = count() by Zone
| order by EndpointCount desc
```

Use these to understand what DNS zones you actually need before creating them.

---

*Managing hybrid Azure environments? Check out our [Azure IPAM Tool](/blog/azure-ipam-tool/) for cross-subscription IP visibility, or our [CAF Roles Matrix](/blog/it-roles-responsibilities-matrix/) for practical Azure governance.*
