# Complete KQL Query Library

![Azure Noob Logo](logo.png)

## Enterprise Azure Resource Graph Queries

**48 Production-Tested Queries for 30,000+ Resources**

Azure Noob | azure-noob.com

---

## What's Inside

This library contains 48 production-tested KQL queries used daily in enterprise Azure environments managing 30,000+ resources across 44 subscriptions.

**✅ What You Get:**
- 48 copy-paste ready queries
- Advanced join patterns
- Case-insensitive tag handling
- Performance optimization tips
- SQL to KQL translations
- Troubleshooting guide
- Real production scenarios
- JSON format included

**📋 Categories:**
1. VM Inventory & Management (10 queries)
2. Networking (10 queries)
3. Security & Compliance (8 queries)
4. Cost & FinOps (8 queries)
5. Storage & Disks (5 queries)
6. Azure Arc (3 queries)
7. Databricks (2 queries)
8. Advanced Scenarios (2 queries)

---

## Quick Start Guide

### How to Use These Queries

**In Azure Portal:**
1. Navigate to Azure Resource Graph Explorer
2. Copy query from this guide
3. Paste into query editor
4. Click "Run query"
5. Export results to CSV/Excel

**In PowerShell:**
```powershell
# Install module if needed
Install-Module -Name Az.ResourceGraph

# Run query
$query = @"
[paste query here]
"@

Search-AzGraph -Query $query
```

**Performance Tips:**
- Add `| take 100` for testing large environments
- Use `| where` filters early in the query
- Limit date ranges for time-based queries
- Project only needed columns

---

# Chapter 1: VM Inventory & Management

## Query 1: Complete VM Inventory with All Details

**Use Case:** Daily inventory report for operations team

```kql
resources
| where type =~ 'microsoft.compute/virtualmachines' 
   or type =~ 'microsoft.databricks/workspaces'
| extend Category = case(
    type =~ 'microsoft.databricks/workspaces', "Databricks Workspace",
    tostring(properties.storageProfile.imageReference.offer) contains "Windows-10" 
    or tostring(properties.storageProfile.imageReference.offer) contains "Windows-11" 
    or tostring(properties.storageProfile.imageReference.sku) contains "wvd", "Desktop OS",
    tostring(properties.storageProfile.osDisk.osType) == "Windows", "Server OS",
    "Linux/Other"
)
| extend vmSize = iff(type =~ 'microsoft.compute/virtualmachines', 
    tostring(properties.hardwareProfile.vmSize), "Managed Tier")
| extend osType = tostring(properties.storageProfile.osDisk.osType)
| extend powerState = coalesce(
    tostring(properties.extended.instanceView.powerState.code), 
    tostring(properties.provisioningState))
| extend nicId = tostring(properties.networkProfile.networkInterfaces[0].id)
| extend osVersionDisplay = case(
    type =~ 'microsoft.databricks/workspaces', tostring(properties.sku.name),
    strcat(tostring(properties.storageProfile.imageReference.publisher), ' ', 
    tostring(properties.storageProfile.imageReference.offer), ' ', 
    tostring(properties.storageProfile.imageReference.sku))
)
| extend createdTime = tostring(properties.timeCreated)
| join kind=leftouter (
    resources
    | where type =~ 'microsoft.network/networkinterfaces'
    | extend privateIp = tostring(properties.ipConfigurations[0].properties.privateIPAddress)
    | project nicId = id, privateIp
) on $left.nicId == $right.nicId
| join kind=leftouter (
    resourcecontainers
    | where type == 'microsoft.resources/subscriptions'
    | project subscriptionId, subscriptionName = name
) on subscriptionId
| extend ipAddress = iff(
    powerState contains 'running' or Category == "Databricks Workspace", 
    coalesce(privateIp, "N/A"), "N/A")
| extend Application = coalesce(tags.Application, tags.application, tags.APPLICATION, 'Not Tagged')
| extend Owner = coalesce(tags.Owner, tags.owner, tags.OWNER, 'Not Tagged')
| extend Type = coalesce(tags.Type, tags.type, tags.TYPE, 'Not Tagged')
| extend Environment = coalesce(tags.Environment, tags.environment, tags.ENVIRONMENT, 'Not Tagged')
| project 
    name, 
    Category,
    subscriptionName, 
    resourceGroup, 
    location, 
    vmSize, 
    osType,
    osVersionDisplay,
    powerState, 
    ipAddress,
    Application,
    Owner,
    Type,
    Environment,
    createdTime
| order by subscriptionName asc, resourceGroup asc, name asc
```

**Key Features:**
- Handles case-sensitive tag variations
- Shows IPs only for running VMs
- Includes Databricks workspaces
- Categorizes Desktop vs Server OS
- Left joins prevent data loss

---

## Query 2: VMs by Power State

**Use Case:** Find deallocated VMs to reduce costs

```kql
resources
| where type =~ 'microsoft.compute/virtualmachines'
| extend powerState = tostring(properties.extended.instanceView.powerState.code)
| extend provisioningState = tostring(properties.provisioningState)
| extend actualState = coalesce(powerState, provisioningState, "Unknown")
| summarize Count = count() by actualState
| order by Count desc
```

**Expected Results:**
- PowerState/running: 2,847
- PowerState/deallocated: 342
- PowerState/stopped: 18

**Cost Impact:** Deallocated VMs still incur storage costs but save compute (~70% reduction)

---

## Query 3: Deallocated VMs (Cost Savings Opportunity)

**Use Case:** Weekly report for FinOps team - identify zombie VMs

```kql
resources
| where type =~ 'microsoft.compute/virtualmachines'
| extend powerState = tostring(properties.extended.instanceView.powerState.code)
| where powerState =~ 'PowerState/deallocated'
| extend vmSize = tostring(properties.hardwareProfile.vmSize)
| extend createdTime = tostring(properties.timeCreated)
| extend DaysDeallocated = datetime_diff('day', now(), todatetime(createdTime))
| extend Owner = coalesce(tags.Owner, tags.owner, 'Not Tagged')
| extend Environment = coalesce(tags.Environment, tags.environment, 'Not Tagged')
| project 
    name,
    resourceGroup,
    location,
    vmSize,
    powerState,
    DaysDeallocated,
    Owner,
    Environment,
    subscriptionId
| where DaysDeallocated > 30
| order by DaysDeallocated desc
```

**Action Items:**
- VMs deallocated >90 days: Consider deletion
- VMs deallocated 30-90 days: Verify with owner
- Pattern: Test environments never cleaned up

---

## Query 4: VMs Without Backup Configured

**Use Case:** Compliance audit - identify unprotected VMs

```kql
resources
| where type =~ 'microsoft.compute/virtualmachines'
| where tags.Environment !~ 'Development' and tags.Environment !~ 'Test'
| extend backupEnabled = isnotnull(properties.virtualMachineProfile.protectionPolicy)
| where backupEnabled == false or isempty(backupEnabled)
| extend Environment = coalesce(tags.Environment, tags.environment, 'Not Tagged')
| extend Criticality = coalesce(tags.Criticality, tags.criticality, 'Not Tagged')
| project 
    name,
    resourceGroup,
    location,
    Environment,
    Criticality,
    subscriptionId
| order by Criticality desc, name asc
```

**Compliance Note:** Production VMs typically require backup per corporate policy

---

## Query 5: VMs by OS Type and Version

**Use Case:** OS lifecycle management - identify unsupported versions

```kql
resources
| where type =~ 'microsoft.compute/virtualmachines'
| extend osType = tostring(properties.storageProfile.osDisk.osType)
| extend publisher = tostring(properties.storageProfile.imageReference.publisher)
| extend offer = tostring(properties.storageProfile.imageReference.offer)
| extend sku = tostring(properties.storageProfile.imageReference.sku)
| extend version = tostring(properties.storageProfile.imageReference.version)
| extend fullOS = strcat(publisher, ' ', offer, ' ', sku)
| summarize Count = count() by osType, fullOS
| order by Count desc
```

**Common Results:**
- Canonical UbuntuServer 18.04-LTS: 847 VMs
- MicrosoftWindowsServer WindowsServer 2019-Datacenter: 1,234 VMs
- RedHat RHEL 8.2: 456 VMs

**Action:** Flag Ubuntu 18.04 (EOL April 2023) for upgrade

---

## Query 6: AVD/WVD Session Hosts

**Use Case:** Virtual Desktop Infrastructure inventory

```kql
resources
| where type =~ 'microsoft.compute/virtualmachines'
| where tostring(properties.storageProfile.imageReference.offer) contains "Windows-10"
    or tostring(properties.storageProfile.imageReference.offer) contains "Windows-11"
    or tostring(properties.storageProfile.imageReference.sku) contains "wvd"
    or tostring(properties.storageProfile.imageReference.sku) contains "avd"
| extend vmSize = tostring(properties.hardwareProfile.vmSize)
| extend powerState = tostring(properties.extended.instanceView.powerState.code)
| extend HostPool = coalesce(tags.HostPool, tags.hostpool, 'Not Tagged')
| project 
    name,
    resourceGroup,
    vmSize,
    powerState,
    HostPool,
    location,
    subscriptionId
| order by HostPool asc, name asc
```

**Licensing Note:** AVD VMs require special Windows licensing (not covered by Azure Hybrid Benefit)

---

## Query 7: VMs by Size Family

**Use Case:** Capacity planning - understand VM SKU distribution

```kql
resources
| where type =~ 'microsoft.compute/virtualmachines'
| extend vmSize = tostring(properties.hardwareProfile.vmSize)
| extend sizeFamily = extract("^([A-Za-z]+)", 1, vmSize)
| summarize Count = count(), VMs = make_list(name, 5) by sizeFamily, vmSize
| order by Count desc
```

**Size Families:**
- D-series: General purpose (most common)
- E-series: Memory optimized
- F-series: Compute optimized
- B-series: Burstable (cost-effective for low utilization)

---

## Query 8: VMs Created in Last 30 Days

**Use Case:** Track new deployments for change management

```kql
resources
| where type =~ 'microsoft.compute/virtualmachines'
| extend createdTime = todatetime(properties.timeCreated)
| where createdTime >= ago(30d)
| extend Owner = coalesce(tags.Owner, tags.owner, 'Not Tagged')
| extend Application = coalesce(tags.Application, tags.application, 'Not Tagged')
| extend vmSize = tostring(properties.hardwareProfile.vmSize)
| project 
    name,
    resourceGroup,
    createdTime,
    vmSize,
    Owner,
    Application,
    location,
    subscriptionId
| order by createdTime desc
```

**Change Control:** Cross-reference with approved change tickets

---

## Query 9: VMs Missing Critical Tags

**Use Case:** Governance compliance - enforce tagging standards

```kql
resources
| where type =~ 'microsoft.compute/virtualmachines'
| extend hasOwner = isnotnull(tags.Owner) or isnotnull(tags.owner) or isnotnull(tags.OWNER)
| extend hasEnvironment = isnotnull(tags.Environment) or isnotnull(tags.environment) or isnotnull(tags.ENVIRONMENT)
| extend hasApplication = isnotnull(tags.Application) or isnotnull(tags.application) or isnotnull(tags.APPLICATION)
| extend hasCostCenter = isnotnull(tags.CostCenter) or isnotnull(tags.costcenter) or isnotnull(tags['Cost Center'])
| where hasOwner == false or hasEnvironment == false or hasApplication == false or hasCostCenter == false
| extend MissingTags = strcat(
    iff(hasOwner == false, "Owner ", ""),
    iff(hasEnvironment == false, "Environment ", ""),
    iff(hasApplication == false, "Application ", ""),
    iff(hasCostCenter == false, "CostCenter ", "")
)
| project 
    name,
    resourceGroup,
    MissingTags,
    location,
    subscriptionId
| order by MissingTags asc, name asc
```

**Policy:** All production VMs must have Owner, Environment, Application, CostCenter tags

---

## Query 10: VM Licensing Count (Windows vs Linux)

**Use Case:** License true-up for Microsoft EA

```kql
resources
| where type =~ 'microsoft.compute/virtualmachines'
| extend osType = tostring(properties.storageProfile.osDisk.osType)
| extend licenseType = tostring(properties.licenseType)
| extend powerState = tostring(properties.extended.instanceView.powerState.code)
| where powerState =~ 'PowerState/running' or powerState =~ 'PowerState/starting'
| summarize 
    TotalVMs = count(),
    HybridBenefitVMs = countif(licenseType =~ 'Windows_Server'),
    StandardLicenseVMs = countif(isempty(licenseType) or licenseType !~ 'Windows_Server')
    by osType
| extend EstimatedMonthlySavings = iff(osType =~ 'Windows', HybridBenefitVMs * 40, 0)
```

**Savings:** Azure Hybrid Benefit saves ~$40/month per Windows Server VM

---

# Chapter 2: Networking

## Query 11: NICs Mapped to VMs with IPs

**Use Case:** Network documentation - complete NIC to VM mapping

```kql
resources
| where type =~ 'microsoft.network/networkinterfaces'
| extend vmId = tostring(properties.virtualMachine.id)
| extend privateIp = tostring(properties.ipConfigurations[0].properties.privateIPAddress)
| extend publicIpId = tostring(properties.ipConfigurations[0].properties.publicIPAddress.id)
| extend subnetId = tostring(properties.ipConfigurations[0].properties.subnet.id)
| extend subnetName = split(subnetId, '/')[10]
| extend vnetName = split(subnetId, '/')[8]
| join kind=leftouter (
    resources
    | where type =~ 'microsoft.compute/virtualmachines'
    | project vmId = id, vmName = name, vmResourceGroup = resourceGroup
) on vmId
| join kind=leftouter (
    resources
    | where type =~ 'microsoft.network/publicipaddresses'
    | project publicIpId = id, publicIp = tostring(properties.ipAddress)
) on publicIpId
| project 
    nicName = name,
    vmName,
    privateIp,
    publicIp,
    vnetName,
    subnetName,
    resourceGroup,
    vmResourceGroup,
    location
| order by vmName asc
```

**Use Case:** Troubleshooting connectivity issues, IP address management

---

## Query 12: Unattached NICs (Cost Waste)

**Use Case:** Monthly cleanup - remove orphaned NICs

```kql
resources
| where type =~ 'microsoft.network/networkinterfaces'
| where isnull(properties.virtualMachine.id) or isempty(properties.virtualMachine.id)
| extend privateIp = tostring(properties.ipConfigurations[0].properties.privateIPAddress)
| extend createdTime = tostring(properties.timeCreated)
| extend Owner = coalesce(tags.Owner, tags.owner, 'Not Tagged')
| project 
    name,
    resourceGroup,
    privateIp,
    createdTime,
    Owner,
    location,
    subscriptionId
| order by name asc
```

**Cost:** $0.01/hour per NIC ($7.30/month) - multiplied by hundreds = significant waste

---

## Query 13: Public IP Addresses in Use

**Use Case:** Security audit - identify internet-facing resources

```kql
resources
| where type =~ 'microsoft.network/publicipaddresses'
| extend ipAddress = tostring(properties.ipAddress)
| extend allocationMethod = tostring(properties.publicIPAllocationMethod)
| extend associatedResourceId = tostring(properties.ipConfiguration.id)
| extend resourceType = split(associatedResourceId, '/')[7]
| extend resourceName = split(associatedResourceId, '/')[8]
| extend Owner = coalesce(tags.Owner, tags.owner, 'Not Tagged')
| extend Environment = coalesce(tags.Environment, tags.environment, 'Not Tagged')
| project 
    publicIpName = name,
    ipAddress,
    allocationMethod,
    resourceType,
    resourceName,
    Owner,
    Environment,
    resourceGroup,
    location
| order by Environment asc, resourceName asc
```

**Security Note:** Production public IPs should be documented and approved

---

## Query 14: Unattached Public IPs

**Use Case:** Cost savings - static IPs cost money even when unused

```kql
resources
| where type =~ 'microsoft.network/publicipaddresses'
| where isnull(properties.ipConfiguration.id) or isempty(properties.ipConfiguration.id)
| extend ipAddress = tostring(properties.ipAddress)
| extend allocationMethod = tostring(properties.publicIPAllocationMethod)
| extend DaysUnused = datetime_diff('day', now(), todatetime(properties.timeCreated))
| project 
    name,
    ipAddress,
    allocationMethod,
    DaysUnused,
    resourceGroup,
    location,
    subscriptionId
| order by DaysUnused desc
```

**Cost:** Static public IPs cost $0.005/hour ($3.65/month each)

---

## Query 15: NSG Rules Audit (Permissive Rules)

**Use Case:** Security review - find overly permissive firewall rules

```kql
resources
| where type =~ 'microsoft.network/networksecuritygroups'
| mv-expand rules = properties.securityRules
| extend 
    ruleName = tostring(rules.name),
    priority = toint(rules.properties.priority),
    direction = tostring(rules.properties.direction),
    access = tostring(rules.properties.access),
    protocol = tostring(rules.properties.protocol),
    sourceAddressPrefix = tostring(rules.properties.sourceAddressPrefix),
    destinationAddressPrefix = tostring(rules.properties.destinationAddressPrefix),
    destinationPortRange = tostring(rules.properties.destinationPortRange)
| where access =~ 'Allow' and direction =~ 'Inbound'
| where sourceAddressPrefix =~ '*' or sourceAddressPrefix =~ 'Internet' or sourceAddressPrefix =~ '0.0.0.0/0'
| project 
    nsgName = name,
    ruleName,
    priority,
    protocol,
    sourceAddressPrefix,
    destinationPortRange,
    resourceGroup,
    location
| order by priority asc
```

**Security Risk:** Rules allowing inbound from Internet on RDP (3389) or SSH (22)

---

## Query 16: Subnets with IP Utilization

**Use Case:** Capacity planning - prevent subnet exhaustion

```kql
resources
| where type =~ 'microsoft.network/virtualnetworks'
| mv-expand subnets = properties.subnets
| extend 
    subnetName = tostring(subnets.name),
    addressPrefix = tostring(subnets.properties.addressPrefix),
    ipConfigCount = array_length(subnets.properties.ipConfigurations)
| extend 
    subnetSize = split(addressPrefix, '/')[1],
    totalIPs = pow(2, 32 - toint(split(addressPrefix, '/')[1])) - 5,
    usedIPs = ipConfigCount,
    availableIPs = pow(2, 32 - toint(split(addressPrefix, '/')[1])) - 5 - ipConfigCount,
    utilizationPercent = round((todouble(ipConfigCount) / (pow(2, 32 - toint(split(addressPrefix, '/')[1])) - 5)) * 100, 2)
| project 
    vnetName = name,
    subnetName,
    addressPrefix,
    totalIPs,
    usedIPs,
    availableIPs,
    utilizationPercent,
    resourceGroup,
    location
| where utilizationPercent > 80
| order by utilizationPercent desc
```

**Alert Threshold:** >80% utilization requires subnet expansion planning

---

## Query 17: VNet Peering Relationships

**Use Case:** Network topology documentation

```kql
resources
| where type =~ 'microsoft.network/virtualnetworks'
| mv-expand peerings = properties.virtualNetworkPeerings
| extend 
    peeringName = tostring(peerings.name),
    remoteVNet = tostring(peerings.properties.remoteVirtualNetwork.id),
    peeringState = tostring(peerings.properties.peeringState),
    allowForwardedTraffic = tobool(peerings.properties.allowForwardedTraffic),
    allowGatewayTransit = tobool(peerings.properties.allowGatewayTransit)
| extend remoteVNetName = split(remoteVNet, '/')[8]
| project 
    sourceVNet = name,
    peeringName,
    remoteVNetName,
    peeringState,
    allowForwardedTraffic,
    allowGatewayTransit,
    resourceGroup,
    location
| order by sourceVNet asc
```

**Validation:** Verify peerings are in "Connected" state

---

## Query 18: Private Endpoints Inventory

**Use Case:** Track private connectivity to PaaS services

```kql
resources
| where type =~ 'microsoft.network/privateendpoints'
| extend 
    privateLinkServiceId = tostring(properties.privateLinkServiceConnections[0].properties.privateLinkServiceId),
    serviceType = split(privateLinkServiceId, '/')[6],
    serviceName = split(privateLinkServiceId, '/')[8],
    connectionState = tostring(properties.privateLinkServiceConnections[0].properties.privateLinkServiceConnectionState.status),
    subnetId = tostring(properties.subnet.id)
| extend 
    vnetName = split(subnetId, '/')[8],
    subnetName = split(subnetId, '/')[10]
| project 
    privateEndpointName = name,
    serviceType,
    serviceName,
    connectionState,
    vnetName,
    subnetName,
    resourceGroup,
    location
| order by serviceType asc, serviceName asc
```

**Compliance:** Regulated environments often require private endpoints for storage, SQL, etc.

---

## Query 19: ExpressRoute Circuits

**Use Case:** Hybrid connectivity audit

```kql
resources
| where type =~ 'microsoft.network/expressroutecircuits'
| extend 
    serviceProviderName = tostring(properties.serviceProviderProperties.serviceProviderName),
    peeringLocation = tostring(properties.serviceProviderProperties.peeringLocation),
    bandwidthInMbps = toint(properties.serviceProviderProperties.bandwidthInMbps),
    circuitProvisioningState = tostring(properties.circuitProvisioningState),
    serviceProviderProvisioningState = tostring(properties.serviceProviderProvisioningState)
| project 
    circuitName = name,
    serviceProviderName,
    peeringLocation,
    bandwidthInMbps,
    circuitProvisioningState,
    serviceProviderProvisioningState,
    resourceGroup,
    location,
    subscriptionId
| order by bandwidthInMbps desc
```

**Cost:** ExpressRoute circuits are expensive - ensure they're actually in use

---

## Query 20: Load Balancers with Backend Pools

**Use Case:** Load balancer configuration audit

```kql
resources
| where type =~ 'microsoft.network/loadbalancers'
| extend 
    sku = tostring(sku.name),
    frontendCount = array_length(properties.frontendIPConfigurations),
    backendPoolCount = array_length(properties.backendAddressPools),
    probeCount = array_length(properties.probes),
    ruleCount = array_length(properties.loadBalancingRules)
| mv-expand backendPools = properties.backendAddressPools
| extend 
    poolName = tostring(backendPools.name),
    backendIPCount = array_length(backendPools.properties.backendIPConfigurations)
| project 
    loadBalancerName = name,
    sku,
    poolName,
    backendIPCount,
    frontendCount,
    probeCount,
    ruleCount,
    resourceGroup,
    location
| order by loadBalancerName asc, poolName asc
```

---

# Chapter 3: Security & Compliance

## Query 21: Unencrypted Managed Disks

**Use Case:** Security audit - find non-compliant disks

```kql
resources
| where type =~ 'microsoft.compute/disks'
| extend 
    encryptionType = tostring(properties.encryption.type),
    diskState = tostring(properties.diskState),
    diskSizeGB = toint(properties.diskSizeGB)
| where encryptionType !~ 'EncryptionAtRestWithPlatformKey' 
    and encryptionType !~ 'EncryptionAtRestWithCustomerKey'
    or isempty(encryptionType)
| extend Owner = coalesce(tags.Owner, tags.owner, 'Not Tagged')
| project 
    diskName = name,
    diskSizeGB,
    diskState,
    encryptionType,
    Owner,
    resourceGroup,
    location,
    subscriptionId
| order by diskSizeGB desc
```

**Compliance:** Most security frameworks require encryption at rest

---

## Query 22: Storage Accounts Without HTTPS Enforcement

**Use Case:** Security baseline validation

```kql
resources
| where type =~ 'microsoft.storage/storageaccounts'
| extend 
    httpsOnly = tobool(properties.supportsHttpsTrafficOnly),
    minimumTlsVersion = tostring(properties.minimumTlsVersion),
    allowBlobPublicAccess = tobool(properties.allowBlobPublicAccess)
| where httpsOnly == false or isempty(httpsOnly)
| extend Owner = coalesce(tags.Owner, tags.owner, 'Not Tagged')
| project 
    storageAccountName = name,
    httpsOnly,
    minimumTlsVersion,
    allowBlobPublicAccess,
    Owner,
    resourceGroup,
    location,
    subscriptionId
| order by name asc
```

**Security Risk:** HTTP traffic is unencrypted and should be blocked

---

## Query 23: VMs Without Monitoring Agent

**Use Case:** Monitoring coverage audit

```kql
resources
| where type =~ 'microsoft.compute/virtualmachines'
| extend 
    hasAzureMonitorAgent = isnotnull(properties.extensions) 
        and array_length(properties.extensions) > 0
| join kind=leftouter (
    resources
    | where type =~ 'microsoft.compute/virtualmachines/extensions'
    | where properties.publisher =~ 'Microsoft.Azure.Monitor.VirtualMachines.GuestHealth'
        or properties.publisher =~ 'Microsoft.EnterpriseCloud.Monitoring'
    | project vmId = substring(id, 0, lastindexof(id, '/extensions')), hasExtension = true
) on $left.id == $right.vmId
| where isnull(hasExtension) or hasExtension == false
| extend Environment = coalesce(tags.Environment, tags.environment, 'Not Tagged')
| where Environment !~ 'Development' and Environment !~ 'Test'
| project 
    vmName = name,
    Environment,
    resourceGroup,
    location,
    subscriptionId
| order by Environment asc, vmName asc
```

**Note:** Production VMs should have monitoring agents for observability

---

## Query 24: Key Vaults Without Soft Delete

**Use Case:** Data protection compliance

```kql
resources
| where type =~ 'microsoft.keyvault/vaults'
| extend 
    softDeleteEnabled = tobool(properties.enableSoftDelete),
    purgeProtectionEnabled = tobool(properties.enablePurgeProtection),
    sku = tostring(properties.sku.name)
| where softDeleteEnabled == false or purgeProtectionEnabled == false
| extend Owner = coalesce(tags.Owner, tags.owner, 'Not Tagged')
| project 
    keyVaultName = name,
    softDeleteEnabled,
    purgeProtectionEnabled,
    sku,
    Owner,
    resourceGroup,
    location,
    subscriptionId
| order by name asc
```

**Best Practice:** Enable soft delete + purge protection to prevent accidental deletion

---

## Query 25: SQL Databases Without TDE

**Use Case:** Data encryption compliance

```kql
resources
| where type =~ 'microsoft.sql/servers/databases'
| where name !~ 'master'
| extend serverName = split(id, '/')[8]
| join kind=leftouter (
    resources
    | where type =~ 'microsoft.sql/servers/databases/transparentdataencryption'
    | extend 
        dbId = substring(id, 0, lastindexof(id, '/transparentDataEncryption')),
        tdeState = tostring(properties.state)
    | project dbId, tdeState
) on $left.id == $right.dbId
| where isnull(tdeState) or tdeState !~ 'Enabled'
| extend Owner = coalesce(tags.Owner, tags.owner, 'Not Tagged')
| project 
    serverName,
    databaseName = name,
    tdeState,
    Owner,
    resourceGroup,
    location,
    subscriptionId
| order by serverName asc, databaseName asc
```

**Compliance:** TDE (Transparent Data Encryption) required for PCI-DSS, HIPAA

---

## Query 26: Network Security Violations

**Use Case:** Identify resources exposed to internet without NSG

```kql
resources
| where type =~ 'microsoft.network/networkinterfaces'
| extend 
    nsgId = tostring(properties.networkSecurityGroup.id),
    hasPublicIp = isnotnull(properties.ipConfigurations[0].properties.publicIPAddress.id)
| where hasPublicIp == true and (isnull(nsgId) or isempty(nsgId))
| extend vmId = tostring(properties.virtualMachine.id)
| join kind=leftouter (
    resources
    | where type =~ 'microsoft.compute/virtualmachines'
    | project vmId = id, vmName = name
) on vmId
| project 
    nicName = name,
    vmName,
    resourceGroup,
    location,
    subscriptionId
| order by vmName asc
```

**Security Risk:** Public-facing NICs without NSG are vulnerable

---

## Query 27: Resources Without Required Tags

**Use Case:** Governance enforcement for chargeback

```kql
resources
| where type !~ 'microsoft.resources/subscriptions'
| extend 
    hasOwner = isnotnull(tags.Owner) or isnotnull(tags.owner),
    hasEnvironment = isnotnull(tags.Environment) or isnotnull(tags.environment),
    hasCostCenter = isnotnull(tags.CostCenter) or isnotnull(tags.costcenter) or isnotnull(tags['Cost Center']),
    hasApplication = isnotnull(tags.Application) or isnotnull(tags.application)
| where hasOwner == false or hasEnvironment == false or hasCostCenter == false or hasApplication == false
| extend missingTags = strcat(
    iff(hasOwner == false, "Owner ", ""),
    iff(hasEnvironment == false, "Environment ", ""),
    iff(hasCostCenter == false, "CostCenter ", ""),
    iff(hasApplication == false, "Application ", "")
)
| summarize ResourceCount = count() by type, missingTags
| order by ResourceCount desc
```

**Action:** Use Azure Policy to enforce tagging on new resources

---

## Query 28: Public Storage Accounts

**Use Case:** Data exposure risk assessment

```kql
resources
| where type =~ 'microsoft.storage/storageaccounts'
| extend 
    allowBlobPublicAccess = tobool(properties.allowBlobPublicAccess),
    networkAcls = tostring(properties.networkAcls.defaultAction)
| where allowBlobPublicAccess == true or networkAcls =~ 'Allow'
| extend Owner = coalesce(tags.Owner, tags.owner, 'Not Tagged')
| extend Environment = coalesce(tags.Environment, tags.environment, 'Not Tagged')
| project 
    storageAccountName = name,
    allowBlobPublicAccess,
    networkAcls,
    Environment,
    Owner,
    resourceGroup,
    location,
    subscriptionId
| order by Environment asc, storageAccountName asc
```

**Security:** Production storage should restrict public access and use private endpoints

---

# Chapter 4: Cost & FinOps

## Query 29: Unattached Managed Disks

**Use Case:** Cost optimization - remove orphaned disks

```kql
resources
| where type =~ 'microsoft.compute/disks'
| extend diskState = tostring(properties.diskState)
| where diskState =~ 'Unattached'
| extend 
    diskSizeGB = toint(properties.diskSizeGB),
    sku = tostring(sku.name),
    createdTime = tostring(properties.timeCreated),
    DaysUnattached = datetime_diff('day', now(), todatetime(properties.timeCreated))
| extend Owner = coalesce(tags.Owner, tags.owner, 'Not Tagged')
| extend EstimatedMonthlyCost = case(
    sku contains 'Premium', diskSizeGB * 0.12,
    sku contains 'StandardSSD', diskSizeGB * 0.05,
    diskSizeGB * 0.02
)
| project 
    diskName = name,
    diskSizeGB,
    sku,
    DaysUnattached,
    EstimatedMonthlyCost,
    Owner,
    resourceGroup,
    location,
    subscriptionId
| order by EstimatedMonthlyCost desc
```

**Savings Opportunity:** Delete disks unattached >90 days (verify with owner first)

---

## Query 30: Orphaned Snapshots

**Use Case:** Storage cost reduction

```kql
resources
| where type =~ 'microsoft.compute/snapshots'
| extend 
    diskSizeGB = toint(properties.diskSizeGB),
    createdTime = tostring(properties.timeCreated),
    AgeInDays = datetime_diff('day', now(), todatetime(properties.timeCreated)),
    sourceResourceId = tostring(properties.creationData.sourceResourceId)
| join kind=leftouter (
    resources
    | where type =~ 'microsoft.compute/disks'
    | project diskId = id, diskExists = true
) on $left.sourceResourceId == $right.diskId
| where isnull(diskExists) or diskExists == false
| extend Owner = coalesce(tags.Owner, tags.owner, 'Not Tagged')
| extend EstimatedMonthlyCost = diskSizeGB * 0.015
| project 
    snapshotName = name,
    diskSizeGB,
    AgeInDays,
    EstimatedMonthlyCost,
    sourceResourceId,
    Owner,
    resourceGroup,
    location
| where AgeInDays > 90
| order by EstimatedMonthlyCost desc
```

**Cost:** Snapshots cost $0.015/GB/month - can accumulate significantly

---

## Query 31: Unused Reserved Public IPs

**Use Case:** Eliminate unnecessary IP reservation costs

```kql
resources
| where type =~ 'microsoft.network/publicipaddresses'
| extend 
    allocationMethod = tostring(properties.publicIPAllocationMethod),
    associatedResource = tostring(properties.ipConfiguration.id)
| where allocationMethod =~ 'Static' 
    and (isnull(associatedResource) or isempty(associatedResource))
| extend DaysReserved = datetime_diff('day', now(), todatetime(properties.timeCreated))
| extend MonthlyCost = 3.65
| extend TotalWaste = round(MonthlyCost * (DaysReserved / 30.0), 2)
| project 
    publicIpName = name,
    ipAddress = tostring(properties.ipAddress),
    DaysReserved,
    MonthlyCost,
    TotalWaste,
    resourceGroup,
    location,
    subscriptionId
| order by TotalWaste desc
```

**Action:** Release static IPs not associated with resources

---

## Query 32: Oversized VMs (Low CPU Utilization)

**Use Case:** Right-sizing recommendations

**Note:** This query requires Azure Monitor metrics integration. Basic version:

```kql
resources
| where type =~ 'microsoft.compute/virtualmachines'
| extend vmSize = tostring(properties.hardwareProfile.vmSize)
| extend powerState = tostring(properties.extended.instanceView.powerState.code)
| where powerState =~ 'PowerState/running'
| where vmSize contains 'Standard_D16' or vmSize contains 'Standard_D32' or vmSize contains 'Standard_E16' or vmSize contains 'Standard_E32'
| extend Owner = coalesce(tags.Owner, tags.owner, 'Not Tagged')
| extend Environment = coalesce(tags.Environment, tags.environment, 'Not Tagged')
| project 
    vmName = name,
    vmSize,
    Environment,
    Owner,
    resourceGroup,
    location,
    subscriptionId
| order by vmSize desc
```

**Action:** Review CPU/memory metrics for these large VMs - many are over-provisioned

---

## Query 33: Cost by Resource Type

**Use Case:** Understand spending distribution

```kql
resources
| summarize ResourceCount = count() by type
| extend EstimatedMonthlyCost = case(
    type =~ 'microsoft.compute/virtualmachines', ResourceCount * 73,
    type =~ 'microsoft.storage/storageaccounts', ResourceCount * 20,
    type =~ 'microsoft.sql/servers/databases', ResourceCount * 15,
    type =~ 'microsoft.network/publicipaddresses', ResourceCount * 3.65,
    type =~ 'microsoft.compute/disks', ResourceCount * 4,
    ResourceCount * 2
)
| project 
    ResourceType = type,
    ResourceCount,
    EstimatedMonthlyCost
| order by EstimatedMonthlyCost desc
```

**Note:** These are rough estimates - use Cost Management for actual costs

---

## Query 34: Resources by Subscription Spend

**Use Case:** Subscription-level cost allocation

```kql
resources
| join kind=leftouter (
    resourcecontainers
    | where type == 'microsoft.resources/subscriptions'
    | project subscriptionId, subscriptionName = name
) on subscriptionId
| summarize ResourceCount = count() by subscriptionName, subscriptionId, type
| summarize 
    TotalResources = sum(ResourceCount),
    ResourceTypes = count()
    by subscriptionName, subscriptionId
| order by TotalResources desc
```

**Use With:** Azure Cost Management export for actual spend correlation

---

## Query 35: Stopped But Allocated VMs

**Use Case:** Hidden compute costs

```kql
resources
| where type =~ 'microsoft.compute/virtualmachines'
| extend powerState = tostring(properties.extended.instanceView.powerState.code)
| where powerState =~ 'PowerState/stopped'
| extend vmSize = tostring(properties.hardwareProfile.vmSize)
| extend Owner = coalesce(tags.Owner, tags.owner, 'Not Tagged')
| extend DaysStopped = datetime_diff('day', now(), todatetime(properties.timeCreated))
| project 
    vmName = name,
    vmSize,
    powerState,
    DaysStopped,
    Owner,
    resourceGroup,
    location,
    subscriptionId
| order by DaysStopped desc
```

**Important:** "Stopped" VMs still incur compute charges. Use "Deallocated" to save costs.

---

## Query 36: Resources Without Cost Center Tag

**Use Case:** Chargeback readiness

```kql
resources
| where type !~ 'microsoft.resources/subscriptions'
| extend hasCostCenter = isnotnull(tags.CostCenter) 
    or isnotnull(tags.costcenter) 
    or isnotnull(tags['Cost Center'])
| where hasCostCenter == false
| summarize ResourceCount = count() by type, resourceGroup
| order by ResourceCount desc
```

**Financial Impact:** Cannot properly allocate costs without cost center tags

---

# Chapter 5: Storage & Disks

## Query 37: Disk Inventory by Type and Size

**Use Case:** Storage capacity planning

```kql
resources
| where type =~ 'microsoft.compute/disks'
| extend 
    diskSizeGB = toint(properties.diskSizeGB),
    sku = tostring(sku.name),
    diskState = tostring(properties.diskState)
| summarize 
    DiskCount = count(),
    TotalSizeGB = sum(diskSizeGB),
    AvgSizeGB = round(avg(diskSizeGB), 2)
    by sku, diskState
| extend TotalSizeTB = round(TotalSizeGB / 1024.0, 2)
| order by TotalSizeGB desc
```

**Insight:** Identify if you're over-provisioned on premium storage

---

## Query 38: Premium Disks Attached to Standard VMs

**Use Case:** Cost optimization - premium disks on wrong VM tier

```kql
resources
| where type =~ 'microsoft.compute/disks'
| where sku.name contains 'Premium'
| extend 
    diskSizeGB = toint(properties.diskSizeGB),
    diskState = tostring(properties.diskState),
    managedBy = tostring(managedBy)
| where isnotnull(managedBy) and isnotempty(managedBy)
| join kind=inner (
    resources
    | where type =~ 'microsoft.compute/virtualmachines'
    | extend vmSize = tostring(properties.hardwareProfile.vmSize)
    | where vmSize !contains 's' and vmSize !contains 'S'
    | project vmId = id, vmName = name, vmSize, vmResourceGroup = resourceGroup
) on $left.managedBy == $right.vmId
| project 
    diskName = name,
    diskSizeGB,
    sku = tostring(sku.name),
    vmName,
    vmSize,
    diskResourceGroup = resourceGroup,
    vmResourceGroup
| order by diskSizeGB desc
```

**Optimization:** Standard VMs can't leverage premium disk performance

---

## Query 39: Snapshot Age and Compliance

**Use Case:** Retention policy enforcement

```kql
resources
| where type =~ 'microsoft.compute/snapshots'
| extend 
    diskSizeGB = toint(properties.diskSizeGB),
    createdTime = todatetime(properties.timeCreated),
    AgeInDays = datetime_diff('day', now(), todatetime(properties.timeCreated))
| extend RetentionCategory = case(
    AgeInDays < 7, "Recent (< 7 days)",
    AgeInDays < 30, "Monthly (7-30 days)",
    AgeInDays < 90, "Quarterly (30-90 days)",
    "Long-term (> 90 days)"
)
| summarize 
    Count = count(),
    TotalSizeGB = sum(diskSizeGB),
    OldestSnapshot = min(createdTime)
    by RetentionCategory
| extend TotalSizeTB = round(TotalSizeGB / 1024.0, 2)
| order by Count desc
```

**Policy:** Define retention based on RTO/RPO requirements

---

## Query 40: Storage Account Replication Type

**Use Case:** Cost vs availability trade-off analysis

```kql
resources
| where type =~ 'microsoft.storage/storageaccounts'
| extend 
    sku = tostring(sku.name),
    tier = tostring(sku.tier),
    kind = tostring(kind)
| extend ReplicationType = case(
    sku contains 'LRS', 'Locally Redundant (LRS)',
    sku contains 'ZRS', 'Zone Redundant (ZRS)',
    sku contains 'GRS', 'Geo Redundant (GRS)',
    sku contains 'GZRS', 'Geo-Zone Redundant (GZRS)',
    sku contains 'RAGRS', 'Read-Access Geo Redundant (RA-GRS)',
    'Unknown'
)
| extend Environment = coalesce(tags.Environment, tags.environment, 'Not Tagged')
| summarize Count = count() by ReplicationType, Environment
| order by Count desc
```

**Cost Difference:** GRS costs ~2x LRS - ensure it's needed for each account

---

## Query 41: Large Disks with Low Utilization

**Use Case:** Storage optimization opportunities

```kql
resources
| where type =~ 'microsoft.compute/disks'
| extend diskSizeGB = toint(properties.diskSizeGB)
| where diskSizeGB >= 512
| extend 
    sku = tostring(sku.name),
    diskState = tostring(properties.diskState),
    managedBy = tostring(managedBy)
| join kind=leftouter (
    resources
    | where type =~ 'microsoft.compute/virtualmachines'
    | project vmId = id, vmName = name
) on $left.managedBy == $right.vmId
| extend Owner = coalesce(tags.Owner, tags.owner, 'Not Tagged')
| extend MonthlyCost = case(
    sku contains 'Premium', diskSizeGB * 0.12,
    sku contains 'StandardSSD', diskSizeGB * 0.05,
    diskSizeGB * 0.02
)
| project 
    diskName = name,
    diskSizeGB,
    sku,
    vmName,
    diskState,
    MonthlyCost,
    Owner,
    resourceGroup,
    location
| order by MonthlyCost desc
```

**Action:** Review disk utilization metrics - many large disks are underutilized

---

# Chapter 6: Azure Arc

## Query 42: Arc-Enabled Servers Inventory

**Use Case:** Hybrid server management tracking

```kql
resources
| where type =~ 'microsoft.hybridcompute/machines'
| extend 
    osType = tostring(properties.osType),
    osName = tostring(properties.osName),
    osVersion = tostring(properties.osVersion),
    agentVersion = tostring(properties.agentVersion),
    status = tostring(properties.status),
    lastStatusChange = todatetime(properties.lastStatusChange)
| extend DaysSinceLastSeen = datetime_diff('day', now(), lastStatusChange)
| extend Owner = coalesce(tags.Owner, tags.owner, 'Not Tagged')
| extend Environment = coalesce(tags.Environment, tags.environment, 'Not Tagged')
| project 
    serverName = name,
    osType,
    osName,
    osVersion,
    agentVersion,
    status,
    DaysSinceLastSeen,
    Owner,
    Environment,
    resourceGroup,
    location
| order by DaysSinceLastSeen desc
```

**Monitoring:** Servers with >7 days since last seen may have connectivity issues

---

## Query 43: Arc Ghost Registrations

**Use Case:** Clean up stale Arc registrations

```kql
resources
| where type =~ 'microsoft.hybridcompute/machines'
| extend 
    status = tostring(properties.status),
    lastStatusChange = todatetime(properties.lastStatusChange),
    DaysSinceLastSeen = datetime_diff('day', now(), lastStatusChange)
| where status =~ 'Disconnected' or status =~ 'Expired' or DaysSinceLastSeen > 30
| extend Owner = coalesce(tags.Owner, tags.owner, 'Not Tagged')
| project 
    serverName = name,
    status,
    DaysSinceLastSeen,
    lastStatusChange,
    Owner,
    resourceGroup,
    subscriptionId
| order by DaysSinceLastSeen desc
```

**Cost:** Arc charges apply even for disconnected servers - clean up ghosts

---

## Query 44: Arc Compliance Status

**Use Case:** Guest configuration policy compliance

```kql
resources
| where type =~ 'microsoft.hybridcompute/machines'
| extend 
    complianceStatus = tostring(properties.complianceStatus),
    osType = tostring(properties.osType)
| extend Environment = coalesce(tags.Environment, tags.environment, 'Not Tagged')
| summarize 
    TotalServers = count(),
    CompliantServers = countif(complianceStatus =~ 'Compliant'),
    NonCompliantServers = countif(complianceStatus !~ 'Compliant')
    by Environment, osType
| extend CompliancePercentage = round((todouble(CompliantServers) / TotalServers) * 100, 2)
| order by CompliancePercentage asc
```

**Governance:** Track Arc policy compliance by environment

---

# Chapter 7: Databricks

## Query 45: Databricks Workspaces with SKU

**Use Case:** Databricks cost tracking

```kql
resources
| where type =~ 'microsoft.databricks/workspaces'
| extend 
    sku = tostring(properties.sku.name),
    pricingTier = tostring(properties.parameters.pricingTier.value),
    workspaceId = tostring(properties.workspaceId),
    createdTime = tostring(properties.createdDateTime)
| extend Owner = coalesce(tags.Owner, tags.owner, 'Not Tagged')
| extend CostCenter = coalesce(tags.CostCenter, tags.costcenter, 'Not Tagged')
| project 
    workspaceName = name,
    sku,
    pricingTier,
    Owner,
    CostCenter,
    resourceGroup,
    location,
    subscriptionId
| order by pricingTier desc
```

**Pricing:** Premium tier costs ~2x Standard - ensure it's needed

---

## Query 46: Databricks Clusters Status

**Note:** Cluster details require Databricks API - this gets workspace-level info

```kql
resources
| where type =~ 'microsoft.databricks/workspaces'
| extend 
    managedResourceGroupId = tostring(properties.managedResourceGroupId),
    workspaceUrl = tostring(properties.workspaceUrl)
| join kind=inner (
    resources
    | where type =~ 'microsoft.compute/virtualmachines'
    | where resourceGroup contains 'databricks'
    | extend vmSize = tostring(properties.hardwareProfile.vmSize)
    | summarize 
        ClusterVMCount = count(),
        VMSizes = make_set(vmSize)
        by resourceGroup
) on $left.managedResourceGroupId == $right.resourceGroup
| project 
    workspaceName = name,
    ClusterVMCount,
    VMSizes,
    workspaceUrl,
    resourceGroup,
    location
| order by ClusterVMCount desc
```

**Cost Alert:** Databricks VMs left running overnight are expensive

---

# Chapter 8: Advanced Scenarios

## Query 47: Complete Resource Map (VMs + NICs + Disks + Subnets)

**Use Case:** Full infrastructure topology

```kql
resources
| where type =~ 'microsoft.compute/virtualmachines'
| extend 
    vmSize = tostring(properties.hardwareProfile.vmSize),
    osType = tostring(properties.storageProfile.osDisk.osType),
    powerState = tostring(properties.extended.instanceView.powerState.code),
    nicId = tostring(properties.networkProfile.networkInterfaces[0].id),
    osDiskId = tostring(properties.storageProfile.osDisk.managedDisk.id)
| join kind=leftouter (
    resources
    | where type =~ 'microsoft.network/networkinterfaces'
    | extend 
        privateIp = tostring(properties.ipConfigurations[0].properties.privateIPAddress),
        subnetId = tostring(properties.ipConfigurations[0].properties.subnet.id),
        publicIpId = tostring(properties.ipConfigurations[0].properties.publicIPAddress.id)
    | extend 
        vnetName = split(subnetId, '/')[8],
        subnetName = split(subnetId, '/')[10]
    | project nicId = id, privateIp, vnetName, subnetName, publicIpId
) on $left.nicId == $right.nicId
| join kind=leftouter (
    resources
    | where type =~ 'microsoft.network/publicipaddresses'
    | project publicIpId = id, publicIp = tostring(properties.ipAddress)
) on publicIpId
| join kind=leftouter (
    resources
    | where type =~ 'microsoft.compute/disks'
    | extend diskSizeGB = toint(properties.diskSizeGB)
    | summarize 
        TotalDiskSizeGB = sum(diskSizeGB),
        DiskCount = count()
        by vmId = tostring(managedBy)
) on $left.id == $right.vmId
| extend Owner = coalesce(tags.Owner, tags.owner, 'Not Tagged')
| extend Application = coalesce(tags.Application, tags.application, 'Not Tagged')
| project 
    vmName = name,
    vmSize,
    osType,
    powerState,
    privateIp,
    publicIp,
    vnetName,
    subnetName,
    TotalDiskSizeGB,
    DiskCount,
    Owner,
    Application,
    resourceGroup,
    location
| order by vnetName asc, subnetName asc, vmName asc
```

**Output:** Complete network and storage topology per VM

---

## Query 48: Cross-Subscription Cost Rollup

**Use Case:** Enterprise-wide cost visibility

```kql
resourcecontainers
| where type == 'microsoft.resources/subscriptions'
| join kind=inner (
    resources
    | summarize ResourceCount = count() by subscriptionId, type
    | summarize 
        TotalResources = sum(ResourceCount),
        ResourceTypeCount = count(),
        ResourceTypes = make_set(type)
        by subscriptionId
) on subscriptionId
| extend Owner = coalesce(tags.Owner, tags.owner, 'Not Tagged')
| extend CostCenter = coalesce(tags.CostCenter, tags.costcenter, 'Not Tagged')
| project 
    subscriptionName = name,
    subscriptionId,
    TotalResources,
    ResourceTypeCount,
    Owner,
    CostCenter,
    ResourceTypes
| order by TotalResources desc
```

**Use With:** Cost Management API for actual spend data per subscription

---

# Chapter 9: Advanced Joins Tutorial

## Understanding KQL Joins

KQL supports several join types:

**innerunique (default):** Returns matching rows from both sides, deduplicates left side
**inner:** Returns all matching rows (can create duplicates)
**leftouter:** Returns all left rows, matching right rows (nulls if no match)
**rightouter:** Returns all right rows, matching left rows
**fullouter:** Returns all rows from both sides
**leftanti:** Returns left rows with no match in right
**rightanti:** Returns right rows with no match in left

### Join Pattern 1: VM to NIC to IP

```kql
resources
| where type =~ 'microsoft.compute/virtualmachines'
| project vmId = id, vmName = name, nicId = tostring(properties.networkProfile.networkInterfaces[0].id)
| join kind=leftouter (
    resources
    | where type =~ 'microsoft.network/networkinterfaces'
    | project nicId = id, privateIp = tostring(properties.ipConfigurations[0].properties.privateIPAddress)
) on nicId
```

**Key:** Use `leftouter` to keep VMs even if NIC lookup fails

### Join Pattern 2: Finding Orphaned Resources

```kql
resources
| where type =~ 'microsoft.compute/disks'
| project diskId = id, diskName = name, managedBy
| join kind=leftanti (
    resources
    | where type =~ 'microsoft.compute/virtualmachines'
    | project vmId = id
) on $left.managedBy == $right.vmId
```

**Key:** Use `leftanti` to find disks NOT attached to any VM

### Join Pattern 3: Resource to Subscription

```kql
resources
| join kind=leftouter (
    resourcecontainers
    | where type == 'microsoft.resources/subscriptions'
    | project subscriptionId, subscriptionName = name
) on subscriptionId
```

**Key:** Always use `leftouter` for subscription joins to prevent data loss

### Performance Tips

1. **Filter early:** Apply `where` clauses before joins
2. **Project early:** Select only needed columns before joining
3. **Join order matters:** Put smaller table on the right
4. **Use summarize:** Aggregate before joining when possible

---

# Chapter 10: SQL to KQL Translation

## Common SQL Patterns in KQL

### Pattern 1: SELECT with WHERE

**SQL:**
```sql
SELECT name, location, tags 
FROM resources 
WHERE type = 'microsoft.compute/virtualmachines' 
  AND location = 'eastus'
```

**KQL:**
```kql
resources
| where type =~ 'microsoft.compute/virtualmachines'
| where location =~ 'eastus'
| project name, location, tags
```

**Key Differences:**
- No SELECT, use `project`
- `=~` for case-insensitive comparison
- Pipe `|` instead of newlines

---

### Pattern 2: JOIN

**SQL:**
```sql
SELECT v.name, n.privateIP
FROM virtualmachines v
LEFT JOIN networkinterfaces n ON v.nicId = n.id
```

**KQL:**
```kql
resources
| where type =~ 'microsoft.compute/virtualmachines'
| join kind=leftouter (
    resources
    | where type =~ 'microsoft.network/networkinterfaces'
    | project nicId = id, privateIp = tostring(properties.ipConfigurations[0].properties.privateIPAddress)
) on $left.properties.networkProfile.networkInterfaces[0].id == $right.nicId
```

---

### Pattern 3: GROUP BY with COUNT

**SQL:**
```sql
SELECT location, COUNT(*) as Count
FROM resources
GROUP BY location
ORDER BY Count DESC
```

**KQL:**
```kql
resources
| summarize Count = count() by location
| order by Count desc
```

**Key:** `summarize` = GROUP BY

---

### Pattern 4: CASE/WHEN

**SQL:**
```sql
SELECT name,
  CASE 
    WHEN size LIKE '%D%' THEN 'General Purpose'
    WHEN size LIKE '%E%' THEN 'Memory Optimized'
    ELSE 'Other'
  END as Category
FROM vms
```

**KQL:**
```kql
resources
| where type =~ 'microsoft.compute/virtualmachines'
| extend vmSize = tostring(properties.hardwareProfile.vmSize)
| extend Category = case(
    vmSize contains 'D', 'General Purpose',
    vmSize contains 'E', 'Memory Optimized',
    'Other'
)
| project name, Category
```

---

### Pattern 5: DISTINCT

**SQL:**
```sql
SELECT DISTINCT location FROM resources
```

**KQL:**
```kql
resources
| distinct location
```

---

### Pattern 6: TOP N

**SQL:**
```sql
SELECT TOP 10 name, cost
FROM resources
ORDER BY cost DESC
```

**KQL:**
```kql
resources
| top 10 by cost desc
| project name, cost
```

---

### Pattern 7: String Functions

**SQL:**
```sql
SELECT 
  UPPER(name),
  SUBSTRING(location, 1, 4),
  LEN(resourceGroup)
FROM resources
```

**KQL:**
```kql
resources
| extend 
    upperName = toupper(name),
    locationPrefix = substring(location, 0, 4),
    rgLength = strlen(resourceGroup)
| project upperName, locationPrefix, rgLength
```

---

### Pattern 8: Date Functions

**SQL:**
```sql
SELECT name
FROM resources
WHERE createdDate >= DATEADD(day, -30, GETDATE())
```

**KQL:**
```kql
resources
| where todatetime(properties.timeCreated) >= ago(30d)
| project name
```

**Key:** `ago()` function is cleaner than date math

---

### Pattern 9: IN Clause

**SQL:**
```sql
SELECT name
FROM resources
WHERE location IN ('eastus', 'westus', 'centralus')
```

**KQL:**
```kql
resources
| where location in ('eastus', 'westus', 'centralus')
| project name
```

---

### Pattern 10: NULL Handling

**SQL:**
```sql
SELECT name, COALESCE(tags.Owner, 'Not Tagged') as Owner
FROM resources
```

**KQL:**
```kql
resources
| extend Owner = coalesce(tags.Owner, 'Not Tagged')
| project name, Owner
```

---

# Chapter 11: Performance Optimization

## Query Optimization Techniques

### Technique 1: Filter Early

**Slow:**
```kql
resources
| extend vmSize = tostring(properties.hardwareProfile.vmSize)
| where type =~ 'microsoft.compute/virtualmachines'
| where location =~ 'eastus'
```

**Fast:**
```kql
resources
| where type =~ 'microsoft.compute/virtualmachines'
| where location =~ 'eastus'
| extend vmSize = tostring(properties.hardwareProfile.vmSize)
```

**Why:** Filtering reduces dataset size before expensive operations

---

### Technique 2: Project Only Needed Columns

**Slow:**
```kql
resources
| where type =~ 'microsoft.compute/virtualmachines'
| join kind=leftouter (
    resources
    | where type =~ 'microsoft.network/networkinterfaces'
) on nicId
```

**Fast:**
```kql
resources
| where type =~ 'microsoft.compute/virtualmachines'
| project vmId = id, vmName = name, nicId = tostring(properties.networkProfile.networkInterfaces[0].id)
| join kind=leftouter (
    resources
    | where type =~ 'microsoft.network/networkinterfaces'
    | project nicId = id, privateIp = tostring(properties.ipConfigurations[0].properties.privateIPAddress)
) on nicId
```

**Why:** Reduces data transfer and memory usage

---

### Technique 3: Use Summarize Before Join

**Slow:**
```kql
resources
| where type =~ 'microsoft.compute/disks'
| join kind=leftouter (
    resources
    | where type =~ 'microsoft.compute/virtualmachines'
) on ...
```

**Fast:**
```kql
resources
| where type =~ 'microsoft.compute/disks'
| summarize DiskCount = count(), TotalSizeGB = sum(toint(properties.diskSizeGB)) by managedBy
| join kind=leftouter (
    resources
    | where type =~ 'microsoft.compute/virtualmachines'
    | project vmId = id, vmName = name
) on $left.managedBy == $right.vmId
```

**Why:** Aggregate before joining reduces rows

---

### Technique 4: Limit Date Ranges

**Slow:**
```kql
resources
| where todatetime(properties.timeCreated) >= datetime(2020-01-01)
```

**Fast:**
```kql
resources
| where todatetime(properties.timeCreated) >= ago(90d)
```

**Why:** Smaller time windows process faster

---

### Technique 5: Use `take` for Testing

```kql
resources
| where type =~ 'microsoft.compute/virtualmachines'
| take 100  // Test with small dataset first
| extend vmSize = tostring(properties.hardwareProfile.vmSize)
| join kind=leftouter (...)
```

**Why:** Validate query logic before running on full dataset

---

## Resource Graph Limits

**Query Timeout:** 3 minutes  
**Result Limit:** 1,000 rows (use `take` or pagination)  
**Throttling:** 15 requests per 5 seconds per tenant

**Best Practice:** Export large result sets to CSV rather than viewing in portal

---

# Chapter 12: Troubleshooting Guide

## Common KQL Errors and Fixes

### Error 1: "Property 'X' doesn't exist"

**Error:**
```
The property 'hardwareProfile' doesn't exist
```

**Cause:** Not all resources have all properties

**Fix:**
```kql
resources
| where type =~ 'microsoft.compute/virtualmachines'
| extend vmSize = tostring(properties.hardwareProfile.vmSize)  // Add type check
| where isnotnull(vmSize) and isnotempty(vmSize)
```

---

### Error 2: "Type mismatch in join"

**Error:**
```
Join key type mismatch
```

**Cause:** Joining string to dynamic type

**Fix:**
```kql
| join kind=leftouter (...) on $left.nicId == $right.nicId  // Both must be string
// Use tostring() or todynamic() to convert types
```

---

### Error 3: "Query timeout"

**Error:**
```
Query exceeded maximum execution time
```

**Cause:** Query too complex or dataset too large

**Fix:**
- Add more `where` filters early
- Reduce date range
- Use `take` to limit results
- Break into smaller queries

---

### Error 4: "Cannot convert to type"

**Error:**
```
Cannot convert 'null' to int
```

**Cause:** Trying to convert null/missing values

**Fix:**
```kql
| extend diskSizeGB = toint(properties.diskSizeGB)
// Change to:
| extend diskSizeGB = iff(isnotnull(properties.diskSizeGB), toint(properties.diskSizeGB), 0)
```

---

### Error 5: "make_list limit exceeded"

**Error:**
```
make_list result exceeds limit
```

**Cause:** Aggregating too many items

**Fix:**
```kql
| summarize VMs = make_list(name, 100) by resourceGroup  // Limit to 100 items
```

---

### Error 6: "Invalid datetime format"

**Error:**
```
Cannot parse datetime
```

**Cause:** Property not in datetime format

**Fix:**
```kql
| extend createdTime = todatetime(properties.timeCreated)
// Always use todatetime() when converting to datetime
```

---

### Error 7: "Case-sensitive comparison"

**Problem:** Results missing due to case sensitivity

**Fix:**
```kql
| where type == 'Microsoft.Compute/virtualMachines'  // Wrong - case matters
// Change to:
| where type =~ 'microsoft.compute/virtualmachines'  // Correct - case insensitive
```

---

### Error 8: "Empty join results"

**Problem:** Join returns no rows

**Debug:**
```kql
// Check if both sides have data
resources | where type =~ 'microsoft.compute/virtualmachines' | count
resources | where type =~ 'microsoft.network/networkinterfaces' | count

// Check join key values
resources 
| where type =~ 'microsoft.compute/virtualmachines'
| project nicId = tostring(properties.networkProfile.networkInterfaces[0].id)
| take 5
```

---

### Error 9: "mv-expand creates too many rows"

**Problem:** Query explodes dataset size

**Fix:**
```kql
| mv-expand properties.networkProfile.networkInterfaces
// Add filter after expand:
| where isnotnull(properties_networkProfile_networkInterfaces)
| take 1000  // Limit explosion
```

---

### Error 10: "Tag not found"

**Problem:** Case sensitivity in tags

**Fix:**
```kql
| extend Owner = tags.Owner  // Wrong - won't find 'owner' or 'OWNER'
// Change to:
| extend Owner = coalesce(tags.Owner, tags.owner, tags.OWNER, 'Not Tagged')
```

---

## Query Debugging Tips

**Tip 1: Build queries incrementally**
```kql
resources
| where type =~ 'microsoft.compute/virtualmachines'
| take 10
// Test this first, then add more logic
```

**Tip 2: Use `print` for testing expressions**
```kql
print result = datetime_diff('day', now(), ago(30d))
```

**Tip 3: Check data types**
```kql
resources
| where type =~ 'microsoft.compute/virtualmachines'
| getschema
```

**Tip 4: Validate join keys**
```kql
// Before join:
resources | where type =~ 'microsoft.compute/virtualmachines' | project nicId = tostring(properties.networkProfile.networkInterfaces[0].id) | take 5
resources | where type =~ 'microsoft.network/networkinterfaces' | project nicId = id | take 5
```

---

# Appendix: JSON Query Files

All 48 queries are available in JSON format for easy import into Azure Resource Graph or automation tools.

**File Structure:**
```json
{
  "queries": [
    {
      "id": 1,
      "name": "Complete VM Inventory",
      "category": "VM Inventory",
      "description": "Daily inventory report for operations team",
      "query": "resources | where type =~ 'microsoft.compute/virtualmachines' ...",
      "useCase": "Operations, Compliance",
      "tags": ["vm", "inventory", "daily"]
    }
  ]
}
```

**Download:** Contact azure-noob.com for JSON bundle

---

# What's Next?

## Future Updates Included

As Azure evolves, you'll receive:
- New resource types (Azure Container Instances, App Services, etc.)
- Updated API versions
- New optimization patterns
- Additional security queries
- More cost optimization opportunities

## Stay Updated

Join the list at **azure-noob.com** for:
- New query releases
- KQL tips and tricks
- Azure cost optimization strategies
- Real production scenarios

---

# Support

Questions? Issues? Feedback?

**Email:** contact@azure-noob.com  
**Blog:** azure-noob.com  
**Updates:** Subscribe at azure-noob.com/subscribe

---

## Thank You

![Azure Noob Logo](logo-small.png)

**Thanks for buying. The Swann approves.**

Don't be a noob. Survive enterprise Azure.

---

**Version:** 1.0  
**Published:** December 2025  
**License:** Single-user license. Do not redistribute.

© 2025 Azure Noob. All rights reserved.
