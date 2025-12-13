# BATCH 2 APPLY SCRIPT
$hubTemplates = @{
    'finops' = 'This guide is part of our [Azure FinOps hub](/hub/finops/) covering cost management, chargeback models, and financial operations at enterprise scale.'
    'kql' = 'This guide is part of our [KQL Mastery hub](/hub/kql/) covering query patterns, optimization techniques, and real-world Azure Resource Graph examples.'
    'governance' = 'This guide is part of our [Azure Governance hub](/hub/governance/) covering policy enforcement, compliance frameworks, and enterprise controls.'
    'migration' = 'This guide is part of our [Azure Migration hub](/hub/migration/) covering assessment, planning, execution, and post-migration optimization.'
    'monitoring' = 'This guide is part of our [Azure Monitoring hub](/hub/monitoring/) covering workbooks, alerting, and operational visibility.'
    'automation' = 'This guide is part of our [Azure Automation hub](/hub/automation/) covering Infrastructure as Code, CI/CD pipelines, and DevOps practices.'
    'ai' = 'This guide is part of our [AI-Assisted Azure Operations hub](/hub/ai/) exploring how AI tools transform cloud administration and productivity workflows.'
}

$fixContent = Get-Content "C:\Users\dswann\Documents\GitHub\azure-noob-blog\temp-fixes\batch2-fixes.txt" -Raw
$fixLines = $fixContent -split "`n" | Where-Object { $_ -match '\S' -and $_ -notmatch '^#' }
$postsDir = "C:\Users\dswann\Documents\GitHub\azure-noob-blog\posts"

Write-Host "Processing batch 2: $($fixLines.Count) posts..." -ForegroundColor Cyan
$fixed = 0

foreach ($line in $fixLines) {
    $parts = $line -split '\|'
    $filename = $parts[0].Trim()
    $hub = $parts[1].Trim()
    $insertAfter = $parts[2].Trim()
    $relatedPosts = $parts[3].Trim() -split ','
    
    $filepath = Join-Path $postsDir $filename
    
    if (-not (Test-Path $filepath)) {
        Write-Host "  SKIP: $filename" -ForegroundColor Yellow
        continue
    }
    
    try {
        $content = Get-Content $filepath -Raw -Encoding UTF8
        
        if ($content -match '/hub/') {
            Write-Host "  SKIP: $filename (has hub link)" -ForegroundColor Gray
            continue
        }
        
        if ($content -match '(?s)^---\s*\n(.*?)\n---\s*\n(.*)$') {
            $frontmatter = $Matches[1]
            $body = $Matches[2]
            
            if ($frontmatter -notmatch "^hub:", "Multiline") {
                $frontmatter += "`nhub: $hub"
            }
            
            if ($frontmatter -notmatch "related_posts:", "Multiline") {
                $frontmatter += "`nrelated_posts:"
                foreach ($post in $relatedPosts) {
                    $frontmatter += "`n  - $($post.Trim())"
                }
            }
            
            $hubLink = $hubTemplates[$hub]
            $body = $body -replace '(^.+?\n\n)', "`$1`n$hubLink`n`n"
            
            $newContent = "---`n$frontmatter`n---`n$body"
            Set-Content -Path $filepath -Value $newContent -Encoding UTF8 -NoNewline
            
            Write-Host "  FIXED: $filename" -ForegroundColor Green
            $fixed++
        }
    } catch {
        Write-Host "  ERROR: $filename - $_" -ForegroundColor Red
    }
}

Write-Host "`nBatch 2 Summary: Fixed $fixed posts" -ForegroundColor Yellow
