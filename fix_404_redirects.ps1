# Generate HTML redirect pages for 404 tag URLs
# This creates meta-refresh redirect pages for tag URLs with spaces/capitals
# that Google has cached, redirecting them to the correct slugified versions.

# Map of bad tag names (from 404 report) to correct slugified versions
$tagRedirects = @{
    # Spaces
    "Management Groups" = "management-groups"
    "azure governance" = "azure-governance"
    "Cloud Adoption Framework" = "cloud-adoption-framework"
    "Private DNS" = "private-dns"
    "Resource Tags" = "azure-tags"
    "Hybrid Cloud" = "hybrid-cloud"
    "application discovery" = "application-mapping"
    "update manager" = "azure-update-manager"
    "technical debt" = "technical-debt"
    "update management" = "update-management"
    "resource graph" = "resource-graph"
    "vm inventory" = "vm-inventory"
    "DNS Resolver" = "dns-resolver"
    "Cloud Strategy" = "cloud-strategy"
    
    # Capitals
    "GPT-4" = "gpt-4"
    "WSUS" = "wsus"
    "DNS" = "private-dns"
}

# HTML template for redirect pages
$redirectTemplate = @'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="0; url=/tags/{0}/">
    <link rel="canonical" href="https://azure-noob.com/tags/{0}/">
    <title>Redirecting...</title>
    <script>
        window.location.href = "/tags/{0}/";
    </script>
</head>
<body>
    <p>Redirecting to <a href="/tags/{0}/">/tags/{0}/</a>...</p>
</body>
</html>
'@

# Main script
$docsTagsDir = "docs\tags"

if (-not (Test-Path $docsTagsDir)) {
    Write-Host "❌ Error: Directory '$docsTagsDir' does not exist" -ForegroundColor Red
    Write-Host "   Current directory: $(Get-Location)" -ForegroundColor Yellow
    exit 1
}

Write-Host "`n🔧 Creating $($tagRedirects.Count) redirect pages...`n" -ForegroundColor Cyan

foreach ($badTag in $tagRedirects.Keys) {
    $correctSlug = $tagRedirects[$badTag]
    
    # Create directory for bad tag (with spaces/capitals as-is)
    $tagDir = Join-Path $docsTagsDir $badTag
    New-Item -ItemType Directory -Path $tagDir -Force | Out-Null
    
    # Create index.html with redirect
    $indexFile = Join-Path $tagDir "index.html"
    $htmlContent = $redirectTemplate -f $correctSlug
    
    Set-Content -Path $indexFile -Value $htmlContent -Encoding UTF8
    Write-Host "✅ Created redirect: /tags/$badTag/ → /tags/$correctSlug/" -ForegroundColor Green
}

Write-Host "`n✅ Done! Created $($tagRedirects.Count) redirect pages" -ForegroundColor Green
Write-Host "`n📝 Next steps:" -ForegroundColor Yellow
Write-Host "   1. Review the created directories in docs/tags/" -ForegroundColor White
Write-Host "   2. Commit and push to GitHub" -ForegroundColor White
Write-Host "   3. Wait for Google to recrawl (or submit via Search Console)" -ForegroundColor White
Write-Host "`n   git add docs/tags" -ForegroundColor Cyan
Write-Host "   git commit -m `"Add redirect pages for 404 tag URLs`"" -ForegroundColor Cyan
Write-Host "   git push" -ForegroundColor Cyan
