# Fix YAML parsing errors caused by multiline summaries

$files = @(
    "posts\2025-10-16-azure-chargeback-tags-model.md",
    "posts\2025-10-31-azure-tag-governance-policy.md",
    "posts\2025-11-03-azure-cost-optimization-facade.md",
    "posts\azure-cost-management-is-confusing-but-you-can-tame-it.md"
)

foreach ($file in $files) {
    Write-Host "🔧 Fixing: $file"
    
    $content = Get-Content $file -Raw
    
    # Replace multiline summaries with single-line versions
    $content = $content -replace 'summary: A chargeback/showback model built on tags that finance, app owners, and cloud\s+teams can all live with—without 47 competing cost spreadsheets\.', 'summary: "A chargeback/showback model built on tags that finance, app owners, and cloud teams can all live with—without 47 competing cost spreadsheets."'
    
    $content = $content -replace 'summary: How to turn Azure tags from ''nice to have'' into enforceable governance using\s+Azure Policy, deny/modify effects, and remediation so teams can''t slip around your\s+standards\.', 'summary: "How to turn Azure tags from ''nice to have'' into enforceable governance using Azure Policy, deny/modify effects, and remediation so teams can''t slip around your standards."'
    
    $content = $content -replace 'summary: Most Azure optimization advice is surface-level\. Reserved instances aren''t\s+FinOps\. Here''s what meaningful cost reduction really takes\.', 'summary: "Most Azure optimization advice is surface-level. Reserved instances aren''t FinOps. Here''s what meaningful cost reduction really takes."'
    
    $content = $content -replace 'summary: Azure Cost Management has too many blades, scopes, and exports\. Learn the\s+core workflows you actually need to make FinOps sustainable\.', 'summary: "Azure Cost Management has too many blades, scopes, and exports. Learn the core workflows you actually need to make FinOps sustainable."'
    
    # Write back
    $content | Out-File -FilePath $file -Encoding UTF8 -NoNewline
    
    Write-Host "✅ Fixed: $file"
}

Write-Host "`n✅ All 4 files fixed. Run 'python freeze.py' to test."
