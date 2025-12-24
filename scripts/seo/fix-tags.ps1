$files = Get-ChildItem posts\*.md

foreach ($file in $files) {
    $content = Get-Content $file.FullName -Raw
    
    # Fix common capital letter tags
    $content = $content -replace '"Azure"', '"azure"'
    $content = $content -replace '"Migration"', '"migration"'
    $content = $content -replace '"Cloud Strategy"', '"cloud-strategy"'
    $content = $content -replace '"Enterprise"', '"enterprise"'
    $content = $content -replace '"Mistakes"', '"mistakes"'
    $content = $content -replace '"PowerShell"', '"powershell"'
    $content = $content -replace '"Automation"', '"automation"'
    $content = $content -replace '"DevOps"', '"devops"'
    $content = $content -replace '"Troubleshooting"', '"troubleshooting"'
    $content = $content -replace '"Windows Server"', '"windows-server"'
    $content = $content -replace '"Operations"', '"operations"'
    $content = $content -replace '"Documentation"', '"documentation"'
    $content = $content -replace '"Productivity"', '"productivity"'
    $content = $content -replace '"Private DNS"', '"private-dns"'
    $content = $content -replace '"DNS Resolver"', '"dns-resolver"'
    $content = $content -replace '"Private Endpoints"', '"private-endpoints"'
    $content = $content -replace '"Hybrid Cloud"', '"hybrid-cloud"'
    $content = $content -replace '"Networking"', '"networking"'
    $content = $content -replace '"CAF"', '"caf"'
    $content = $content -replace '"Cloud Adoption Framework"', '"cloud-adoption-framework"'
    $content = $content -replace '"Governance"', '"governance"'
    $content = $content -replace '"Azure Policy"', '"azure-policy"'
    $content = $content -replace '"Management Groups"', '"management-groups"'
    $content = $content -replace '"VMware"', '"vmware"'
    $content = $content -replace '"Serial Console"', '"serial-console"'
    $content = $content -replace '"SCCM"', '"sccm"'
    $content = $content -replace '"WSUS"', '"wsus"'
    $content = $content -replace '"Intune"', '"intune"'
    $content = $content -replace '"Azure Update Manager"', '"azure-update-manager"'
    $content = $content -replace '"Patch Management"', '"patch-management"'
    $content = $content -replace '"CMDB"', '"cmdb"'
    $content = $content -replace '"Resource Graph"', '"resource-graph"'
    $content = $content -replace '"KQL"', '"kql"'
    $content = $content -replace '"Inventory"', '"inventory"'
    $content = $content -replace '"Power BI"', '"power-bi"'
    $content = $content -replace '"Python"', '"python"'
    $content = $content -replace '"Tools"', '"tools"'
    $content = $content -replace '"CCO Dashboard"', '"cco-dashboard"'
    
    # Save the file
    Set-Content -Path $file.FullName -Value $content -NoNewline
    Write-Host "✅ Fixed: $($file.Name)"
}

Write-Host "`n✅ All tags standardized to lowercase with hyphens!"
