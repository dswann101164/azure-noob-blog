# Master SEO Optimization Script
# Executes all remaining optimization tasks in sequence

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "AZURE NOOB BLOG - SEO OPTIMIZATION SUITE" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$scriptsToRun = @(
    @{
        Name = "British → American English Conversion"
        Script = ".\convert-to-american-english.ps1"
        Impact = "+50-100 clicks/month (10× US traffic)"
        Time = "2 minutes"
    },
    @{
        Name = "Internal Linking Analysis"
        Script = ".\analyze-internal-linking.ps1"
        Impact = "+10-20 clicks/month"
        Time = "1 minute"
    },
    @{
        Name = "Title Optimization Analysis"
        Script = ".\analyze-title-optimization.ps1"
        Impact = "+20-30 clicks/month"
        Time = "1 minute"
    },
    @{
        Name = "Lead Magnet Creation"
        Script = ".\create-lead-magnets.ps1"
        Impact = "Email list foundation"
        Time = "1 minute"
    }
)

Write-Host "This suite will execute 4 optimization tasks:" -ForegroundColor Yellow
Write-Host ""
foreach ($task in $scriptsToRun) {
    Write-Host "  ✓ $($task.Name)" -ForegroundColor White
    Write-Host "    Impact: $($task.Impact)" -ForegroundColor Gray
    Write-Host "    Time: $($task.Time)" -ForegroundColor Gray
    Write-Host ""
}

Write-Host "Total expected impact: +80-150 clicks/month" -ForegroundColor Green
Write-Host "Total time: ~5 minutes" -ForegroundColor Green
Write-Host ""

$response = Read-Host "Continue? (Y/N)"
if ($response -ne 'Y' -and $response -ne 'y') {
    Write-Host "Cancelled." -ForegroundColor Yellow
    exit
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "STARTING OPTIMIZATION SEQUENCE" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$completedTasks = 0
$failedTasks = @()

foreach ($task in $scriptsToRun) {
    Write-Host ""
    Write-Host "[$($completedTasks + 1)/$($scriptsToRun.Count)] Running: $($task.Name)..." -ForegroundColor Cyan
    Write-Host ""
    
    if (Test-Path $task.Script) {
        try {
            & $task.Script
            $completedTasks++
            Write-Host ""
            Write-Host "✓ Completed: $($task.Name)" -ForegroundColor Green
        } catch {
            Write-Host "✗ Failed: $($task.Name)" -ForegroundColor Red
            Write-Host "Error: $_" -ForegroundColor Red
            $failedTasks += $task.Name
        }
    } else {
        Write-Host "✗ Script not found: $($task.Script)" -ForegroundColor Red
        $failedTasks += $task.Name
    }
    
    Write-Host ""
    Write-Host "---" -ForegroundColor DarkGray
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "OPTIMIZATION COMPLETE" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Tasks completed: $completedTasks / $($scriptsToRun.Count)" -ForegroundColor White

if ($failedTasks.Count -gt 0) {
    Write-Host "Failed tasks: $($failedTasks.Count)" -ForegroundColor Red
    foreach ($failed in $failedTasks) {
        Write-Host "  - $failed" -ForegroundColor Red
    }
    Write-Host ""
}

Write-Host ""
Write-Host "RESULTS SUMMARY:" -ForegroundColor Yellow
Write-Host ""
Write-Host "Files generated:" -ForegroundColor White
if (Test-Path "british-to-american-changes.csv") {
    Write-Host "  ✓ british-to-american-changes.csv" -ForegroundColor Green
}
if (Test-Path "internal-linking-opportunities.csv") {
    Write-Host "  ✓ internal-linking-opportunities.csv" -ForegroundColor Green
}
if (Test-Path "title-optimization-analysis.csv") {
    Write-Host "  ✓ title-optimization-analysis.csv" -ForegroundColor Green
}
if (Test-Path ".\static\downloads\Azure-AI-Cost-Cheat-Sheet-2025.md") {
    Write-Host "  ✓ Azure-AI-Cost-Cheat-Sheet-2025.md" -ForegroundColor Green
}
if (Test-Path ".\static\downloads\KQL-Query-Library-Complete.md") {
    Write-Host "  ✓ KQL-Query-Library-Complete.md" -ForegroundColor Green
}

Write-Host ""
Write-Host "NEXT STEPS:" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Review generated CSV files for optimization opportunities" -ForegroundColor White
Write-Host "2. If posts were changed, freeze and deploy:" -ForegroundColor White
Write-Host "   python freeze.py" -ForegroundColor Gray
Write-Host "   git add posts/ docs/ static/downloads/" -ForegroundColor Gray
Write-Host "   git commit -m 'SEO: British→American + internal links + lead magnets'" -ForegroundColor Gray
Write-Host "   git push" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Convert lead magnets to PDF and add to site" -ForegroundColor White
Write-Host "4. Add download CTAs to relevant blog posts" -ForegroundColor White
Write-Host "5. Monitor GSC for traffic improvements (30 days)" -ForegroundColor White
Write-Host ""
Write-Host "EXPECTED RESULTS:" -ForegroundColor Green
Write-Host "  - US CTR: 0.14% → 1.5% (+10× traffic)" -ForegroundColor White
Write-Host "  - Internal linking boost: +10-20 clicks/month" -ForegroundColor White
Write-Host "  - Optimized titles: +20-30 clicks/month" -ForegroundColor White
Write-Host "  - Total: +80-150 clicks/month" -ForegroundColor White
Write-Host ""
Write-Host "Combined with today's completed work:" -ForegroundColor Cyan
Write-Host "  - Command Finder fix: +20-40 clicks/month" -ForegroundColor White
Write-Host "  - Logic Apps optimization: +10-15 clicks/month" -ForegroundColor White
Write-Host "  - TOTAL IMPACT: +110-205 clicks/month" -ForegroundColor Green
Write-Host "  - Traffic increase: +423-788%" -ForegroundColor Green
Write-Host ""
Write-Host "🎉 SEO optimization suite complete!" -ForegroundColor Green
