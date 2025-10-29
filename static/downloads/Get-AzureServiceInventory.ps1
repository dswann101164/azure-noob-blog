<#
.SYNOPSIS
    Azure Service Inventory Tool
.DESCRIPTION
    Queries all subscriptions to determine which Azure services are actually in use.
    Creates an Excel-compatible CSV with service counts, categories, and metadata.
.PARAMETER SubscriptionId
    Optional. Specific subscription ID to scan. If not provided, scans all enabled subscriptions.
.PARAMETER OutputPath
    Optional. Path for the output CSV file. Default: .\AzureServiceInventory.csv
.EXAMPLE
    .\Get-AzureServiceInventory.ps1
.EXAMPLE
    .\Get-AzureServiceInventory.ps1 -SubscriptionId "12345678-1234-1234-1234-123456789012"
.EXAMPLE
    .\Get-AzureServiceInventory.ps1 -OutputPath "C:\Reports\Inventory.csv"
.NOTES
    Author: Azure Noob Blog (azure-noob.com)
    Requires: Az.ResourceGraph module
    Version: 1.0
#>

param(
    [Parameter(Mandatory=$false)]
    [string]$SubscriptionId,
    
    [Parameter(Mandatory=$false)]
    [string]$OutputPath = ".\AzureServiceInventory.csv"
)

# Ensure Az.ResourceGraph module
if (-not (Get-Module -ListAvailable Az.ResourceGraph)) {
    Write-Host "Installing Az.ResourceGraph module..." -ForegroundColor Yellow
    Install-Module Az.ResourceGraph -Force -AllowClobber
}

Import-Module Az.ResourceGraph

# Check if logged in
$context = Get-AzContext
if (-not $context) {
    Write-Host "Not logged in to Azure. Running Connect-AzAccount..." -ForegroundColor Yellow
    Connect-AzAccount
}

Write-Host "`n🔍 Querying Azure Resource Graph for service inventory..." -ForegroundColor Cyan

# Build subscription scope
$subscriptionScope = if ($SubscriptionId) {
    @($SubscriptionId)
} else {
    (Get-AzSubscription | Where-Object {$_.State -eq 'Enabled'}).Id
}

Write-Host "📊 Scanning $($subscriptionScope.Count) subscription(s)..." -ForegroundColor Cyan

# Query all resource types
$query = @"
Resources
| summarize 
    Count = count(),
    SubscriptionCount = dcount(subscriptionId),
    Locations = make_set(location)
  by type
| extend 
    Provider = split(type, '/')[0],
    ServiceType = split(type, '/')[1]
| project Provider, ServiceType, Count, SubscriptionCount, Locations
| order by Count desc
"@

$results = Search-AzGraph -Query $query -Subscription $subscriptionScope -First 1000

Write-Host "✅ Found $($results.Count) distinct Azure service types in use`n" -ForegroundColor Green

# Service category mapping
$categoryMap = @{
    'Microsoft.Compute' = 'Compute'
    'Microsoft.Network' = 'Networking'
    'Microsoft.Storage' = 'Storage'
    'Microsoft.Web' = 'Web + Mobile'
    'Microsoft.Sql' = 'Databases'
    'Microsoft.DBforPostgreSQL' = 'Databases'
    'Microsoft.DBforMySQL' = 'Databases'
    'Microsoft.DocumentDB' = 'Databases'
    'Microsoft.KeyVault' = 'Security'
    'Microsoft.ManagedIdentity' = 'Security'
    'Microsoft.Security' = 'Security'
    'Microsoft.OperationalInsights' = 'Monitoring'
    'Microsoft.Insights' = 'Monitoring'
    'Microsoft.Monitor' = 'Monitoring'
    'Microsoft.RecoveryServices' = 'Backup + DR'
    'Microsoft.Backup' = 'Backup + DR'
    'Microsoft.ContainerService' = 'Containers'
    'Microsoft.ContainerRegistry' = 'Containers'
    'Microsoft.Logic' = 'Integration'
    'Microsoft.ServiceBus' = 'Integration'
    'Microsoft.EventHub' = 'Integration'
    'Microsoft.Automation' = 'Management'
    'Microsoft.Resources' = 'Management'
    'Microsoft.Authorization' = 'Management'
    'Microsoft.PolicyInsights' = 'Management'
}

# Cost tier estimation (rough guidelines)
$costTierMap = @{
    'virtualmachines' = 'High'
    'disks' = 'Medium'
    'snapshots' = 'Low'
    'storageaccounts' = 'Medium'
    'virtualnetworks' = 'Low'
    'networkinterfaces' = 'Free'
    'publicipaddresses' = 'Low'
    'loadbalancers' = 'Low'
    'applicationgateways' = 'High'
    'vaults' = 'Medium'
    'servers' = 'High'
    'workspaces' = 'Medium'
    'sites' = 'Medium'
    'serverfarms' = 'Medium'
    'databases' = 'High'
}

# Deprecated/Classic services
$deprecatedServices = @{
    'Microsoft.ClassicCompute/virtualMachines' = 'Migrate to Azure Resource Manager VMs'
    'Microsoft.ClassicStorage/storageAccounts' = 'Migrate to v2 Storage Accounts'
    'Microsoft.ClassicNetwork/virtualNetworks' = 'Migrate to ARM Virtual Networks'
    'Microsoft.ClassicNetwork/reservedIps' = 'Migrate to ARM Public IPs'
}

# Build enriched inventory
$inventory = $results | ForEach-Object {
    $provider = $_.Provider
    $serviceType = $_.ServiceType
    $fullType = "$provider/$serviceType"
    
    $category = if ($categoryMap.ContainsKey($provider)) {
        $categoryMap[$provider]
    } else {
        'Other'
    }
    
    $costTier = if ($costTierMap.ContainsKey($serviceType.ToLower())) {
        $costTierMap[$serviceType.ToLower()]
    } else {
        'Unknown'
    }
    
    $deprecated = if ($deprecatedServices.ContainsKey($fullType)) {
        "YES - $($deprecatedServices[$fullType])"
    } else {
        'No'
    }
    
    $docsLink = "https://learn.microsoft.com/azure/?product=$($serviceType.ToLower())"
    
    [PSCustomObject]@{
        Provider = $provider
        ServiceType = $serviceType
        Category = $category
        Count = $_.Count
        SubscriptionCount = $_.SubscriptionCount
        Locations = ($_.Locations -join ', ')
        CostTier = $costTier
        Deprecated = $deprecated
        DocsLink = $docsLink
        Notes = ''
        Owner = ''
    }
}

# Export to CSV
$inventory | Export-Csv -Path $OutputPath -NoTypeInformation -Encoding UTF8

Write-Host "✅ Service inventory exported to: $OutputPath" -ForegroundColor Green
Write-Host "`n📊 Summary:" -ForegroundColor Cyan
Write-Host "   Total Services in Use: $($inventory.Count)" -ForegroundColor White
Write-Host "   Total Resources: $(($inventory | Measure-Object -Property Count -Sum).Sum)" -ForegroundColor White

# Category breakdown
$categoryBreakdown = $inventory | Group-Object Category | Sort-Object Count -Descending
Write-Host "`n📁 By Category:" -ForegroundColor Cyan
foreach ($cat in $categoryBreakdown) {
    Write-Host "   $($cat.Name): $($cat.Count) service types" -ForegroundColor White
}

# Top 10 services
$top10 = $inventory | Sort-Object Count -Descending | Select-Object -First 10
Write-Host "`n🔝 Top 10 Services (by count):" -ForegroundColor Cyan
foreach ($service in $top10) {
    Write-Host "   $($service.ServiceType): $($service.Count)" -ForegroundColor White
}

# Check for deprecated services
$deprecatedCount = ($inventory | Where-Object {$_.Deprecated -ne 'No'}).Count
if ($deprecatedCount -gt 0) {
    Write-Host "`n⚠️  Warning: $deprecatedCount deprecated service(s) found!" -ForegroundColor Yellow
    $inventory | Where-Object {$_.Deprecated -ne 'No'} | ForEach-Object {
        Write-Host "   - $($_.ServiceType): $($_.Deprecated)" -ForegroundColor Yellow
    }
}

Write-Host "`n💡 Next Steps:" -ForegroundColor Cyan
Write-Host "   1. Open $OutputPath in Excel" -ForegroundColor White
Write-Host "   2. Add Owner and Notes columns for your team" -ForegroundColor White
Write-Host "   3. Filter by Category or CostTier" -ForegroundColor White
Write-Host "   4. Share with your team for service ownership mapping" -ForegroundColor White
Write-Host ""
