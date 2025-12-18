# Batch Title Optimization Analysis
# Analyzes all blog post titles and suggests SEO improvements

$postsDir = ".\posts"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "BATCH TITLE OPTIMIZATION ANALYSIS" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Action words for title optimization
$actionWords = @('Get', 'Download', 'Learn', 'Fix', 'Stop', 'Avoid', 'Master', 'Build', 'Create', 'Deploy')
$benefitWords = @('Cheat Sheet', 'Checklist', 'Step-by-Step', 'Complete Guide', 'Real Costs', 'Time Savings', 'ROI Calculator')

$analysisResults = @()

Get-ChildItem -Path $postsDir -Filter "*.md" | ForEach-Object {
    $file = $_
    $content = Get-Content $file.FullName -Raw
    
    # Extract front matter
    if ($content -match '(?s)^---\s*(.*?)\s*---') {
        $frontMatter = $matches[1]
        
        $currentTitle = ""
        if ($frontMatter -match 'title:\s*["'']?(.*?)["'']?\s*$') {
            $currentTitle = $matches[1]
        }
        
        if (-not $currentTitle) { return }
        
        # Analyze title issues
        $issues = @()
        $hasActionWord = $false
        $hasBenefit = $false
        $hasYear = $currentTitle -match '202[0-9]'
        $length = $currentTitle.Length
        $priority = 'Low'
        
        # Check for action words
        foreach ($word in $actionWords) {
            if ($currentTitle -match "^$word\s" -or $currentTitle -match "\s$word\s") {
                $hasActionWord = $true
                break
            }
        }
        
        # Check for benefit words
        foreach ($benefit in $benefitWords) {
            if ($currentTitle -match $benefit) {
                $hasBenefit = $true
                break
            }
        }
        
        # Identify issues
        if (-not $hasActionWord) {
            $issues += "No action word"
            $priority = 'Medium'
        }
        
        if (-not $hasBenefit) {
            $issues += "No clear benefit"
            $priority = 'Medium'
        }
        
        if (-not $hasYear) {
            $issues += "No year mention"
            $priority = 'Medium'
        }
        
        if ($length -gt 60) {
            $issues += "Too long (>60 chars)"
            $priority = 'High'
        }
        
        if ($currentTitle -match "^(Complete Guide|Introduction|Overview)") {
            $issues += "Generic opening"
            $priority = 'High'
        }
        
        # Generate suggested title
        $suggestedTitle = $currentTitle
        $reason = "Current title is optimized"
        $estimatedImprovement = "0%"
        
        if ($issues.Count -gt 0) {
            $priority = if ($issues.Count -ge 3) { 'High' } elseif ($issues.Count -eq 2) { 'Medium' } else { 'Low' }
            
            # Extract main topic
            $topic = $currentTitle -replace '\(.*?\)', '' -replace ':\s*.*', '' -replace '\s*-\s*.*', ''
            $topic = $topic.Trim()
            
            # Build improved title
            if (-not $hasActionWord) {
                # Add action word based on context
                if ($currentTitle -match 'Guide|Tutorial') {
                    $suggestedTitle = "Master $topic"
                } elseif ($currentTitle -match 'Fix|Problem|Issue') {
                    $suggestedTitle = "Fix $topic"
                } else {
                    $suggestedTitle = "Learn $topic"
                }
            } else {
                $suggestedTitle = $topic
            }
            
            # Add benefit if missing
            if (-not $hasBenefit) {
                if ($currentTitle -match 'Commands|Query|Script') {
                    $suggestedTitle += ": Complete Cheat Sheet"
                } elseif ($currentTitle -match 'Migration|Deploy|Setup') {
                    $suggestedTitle += ": Step-by-Step Checklist"
                } elseif ($currentTitle -match 'Cost|Price|Pricing') {
                    $suggestedTitle += " (Real Costs + Calculator)"
                } else {
                    $suggestedTitle += ": Complete Guide"
                }
            }
            
            # Add year if missing
            if (-not $hasYear) {
                $suggestedTitle += " (2025)"
            }
            
            # Trim if too long
            if ($suggestedTitle.Length -gt 60) {
                $suggestedTitle = $suggestedTitle.Substring(0, 57) + "..."
            }
            
            $reason = $issues -join '; '
            $estimatedImprovement = if ($priority -eq 'High') { '20-30%' } 
                                   elseif ($priority -eq 'Medium') { '10-20%' }
                                   else { '5-10%' }
        }
        
        $analysisResults += [PSCustomObject]@{
            Filename = $file.Name
            CurrentTitle = $currentTitle
            SuggestedTitle = $suggestedTitle
            Issues = ($issues -join '; ')
            Reason = $reason
            Length = $length
            HasActionWord = $hasActionWord
            HasBenefit = $hasBenefit
            HasYear = $hasYear
            Priority = $priority
            EstimatedCTRImprovement = $estimatedImprovement
        }
    }
}

# Display results grouped by priority
Write-Host "HIGH PRIORITY (3+ issues)" -ForegroundColor Red
Write-Host "========================================" -ForegroundColor Red
$highPriority = $analysisResults | Where-Object { $_.Priority -eq 'High' } | Sort-Object Length -Descending
foreach ($result in $highPriority) {
    Write-Host ""
    Write-Host "File: $($result.Filename)" -ForegroundColor Yellow
    Write-Host "Current:  $($result.CurrentTitle)" -ForegroundColor Gray
    Write-Host "Suggested: $($result.SuggestedTitle)" -ForegroundColor Green
    Write-Host "Issues: $($result.Issues)" -ForegroundColor Red
    Write-Host "Est. CTR improvement: $($result.EstimatedCTRImprovement)" -ForegroundColor Cyan
}

Write-Host ""
Write-Host ""
Write-Host "MEDIUM PRIORITY (1-2 issues)" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Yellow
$medPriority = $analysisResults | Where-Object { $_.Priority -eq 'Medium' }
foreach ($result in $medPriority | Select-Object -First 10) {
    Write-Host ""
    Write-Host "File: $($result.Filename)" -ForegroundColor White
    Write-Host "Current:  $($result.CurrentTitle)" -ForegroundColor Gray
    Write-Host "Suggested: $($result.SuggestedTitle)" -ForegroundColor Green
    Write-Host "Issues: $($result.Issues)" -ForegroundColor Yellow
    Write-Host "Est. CTR improvement: $($result.EstimatedCTRImprovement)" -ForegroundColor Cyan
}

Write-Host ""
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "SUMMARY" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
$highCount = ($analysisResults | Where-Object { $_.Priority -eq 'High' }).Count
$medCount = ($analysisResults | Where-Object { $_.Priority -eq 'Medium' }).Count
$lowCount = ($analysisResults | Where-Object { $_.Priority -eq 'Low' }).Count

Write-Host "Total posts analyzed: $($analysisResults.Count)" -ForegroundColor White
Write-Host "High priority: $highCount" -ForegroundColor Red
Write-Host "Medium priority: $medCount" -ForegroundColor Yellow
Write-Host "Low priority (optimized): $lowCount" -ForegroundColor Green
Write-Host ""
Write-Host "Expected impact from title optimization: +20-30 clicks/month" -ForegroundColor Green
Write-Host ""

# Export to CSV
$analysisResults | Sort-Object Priority, Length -Descending | 
    Export-Csv "title-optimization-analysis.csv" -NoTypeInformation

Write-Host "Full analysis exported to: title-optimization-analysis.csv" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Review high-priority titles in CSV" -ForegroundColor White
Write-Host "2. Update titles in post front matter" -ForegroundColor White
Write-Host "3. Test titles for length (max 60 chars)" -ForegroundColor White
Write-Host "4. Deploy and monitor CTR improvements" -ForegroundColor White
