# validate-redirects.ps1
# Tests that redirects are working after deployment

$baseUrl = "https://azure-noob.com"
$testUrls = @(
    # Tag redirects
    @{Old="/tags/Azure Arc/"; Expected="/tags/azure-arc/"; Description="Space in tag"},
    @{Old="/tags/DNS Resolver/"; Expected="/tags/dns-resolver/"; Description="Space in tag"},
    @{Old="/tags/Azure/"; Expected="/tags/azure/"; Description="Case mismatch"},
    @{Old="/tags/KQL/"; Expected="/tags/kql/"; Description="Case mismatch"},
    @{Old="/tags/Management Groups/"; Expected="/tags/management-groups/"; Description="Space in tag"},
    
    # Old test posts
    @{Old="/blog/hello-world/"; Expected="/start-here/"; Description="Deleted test post"},
    @{Old="/blog/my-second-post/"; Expected="/blog/"; Description="Deleted test post"},
    
    # Date-prefixed posts
    @{Old="/blog/2025-01-15-kql-cheat-sheet-complete/"; Expected="/blog/kql-cheat-sheet-complete/"; Description="Date prefix"},
    @{Old="/blog/2025-09-24-why-most-azure-migrations-fail/"; Expected="/blog/why-most-azure-migrations-fail/"; Description="Date prefix"}
)

Write-Host "=" * 80
Write-Host "VALIDATING REDIRECTS" -ForegroundColor Cyan
Write-Host "=" * 80
Write-Host ""

$passed = 0
$failed = 0

foreach ($test in $testUrls) {
    $url = $baseUrl + $test.Old
    
    try {
        # Follow redirects and get final URL
        $response = Invoke-WebRequest -Uri $url -MaximumRedirection 5 -UseBasicParsing
        $finalUrl = $response.BaseResponse.ResponseUri.AbsoluteUri
        
        # Check if we ended up at the expected URL
        $expectedUrl = $baseUrl + $test.Expected
        
        if ($finalUrl -eq $expectedUrl) {
            Write-Host "✓ PASS: $($test.Description)" -ForegroundColor Green
            Write-Host "  $($test.Old) → $($test.Expected)" -ForegroundColor Gray
            $passed++
        }
        else {
            Write-Host "✗ FAIL: $($test.Description)" -ForegroundColor Red
            Write-Host "  Expected: $expectedUrl" -ForegroundColor Gray
            Write-Host "  Got:      $finalUrl" -ForegroundColor Gray
            $failed++
        }
    }
    catch {
        Write-Host "✗ ERROR: $($test.Description)" -ForegroundColor Red
        Write-Host "  $($_.Exception.Message)" -ForegroundColor Gray
        $failed++
    }
    
    Start-Sleep -Milliseconds 500  # Be nice to the server
}

Write-Host ""
Write-Host "=" * 80
if ($failed -eq 0) {
    Write-Host "✓ ALL TESTS PASSED ($passed/$($testUrls.Count))" -ForegroundColor Green
}
else {
    Write-Host "⚠ $failed TESTS FAILED ($passed passed, $failed failed)" -ForegroundColor Yellow
}
Write-Host "=" * 80
Write-Host ""

if ($failed -gt 0) {
    Write-Host "Note: If tests fail, wait 2-3 minutes for GitHub Pages to deploy, then re-run." -ForegroundColor Yellow
}
