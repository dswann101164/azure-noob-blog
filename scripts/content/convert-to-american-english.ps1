# Convert British English to American English in blog posts
# This script will fix spellings to improve US CTR (currently 0.14% vs UK 3.79%)

$postsDir = ".\posts"
$changesLog = @()

# Define British → American replacements
$replacements = @{
    # Common British spellings
    'optimise' = 'optimize'
    'optimised' = 'optimized'
    'optimising' = 'optimizing'
    'optimisation' = 'optimization'
    'realise' = 'realize'
    'realised' = 'realized'
    'realising' = 'realizing'
    'realisation' = 'realization'
    'organisation' = 'organization'
    'organisations' = 'organizations'
    'organisational' = 'organizational'
    'colour' = 'color'
    'colours' = 'colors'
    'behaviour' = 'behavior'
    'behaviours' = 'behaviors'
    'behavioural' = 'behavioral'
    'analyse' = 'analyze'
    'analysed' = 'analyzed'
    'analysing' = 'analyzing'
    'analysis' = 'analysis'  # Same in both
    'favourite' = 'favorite'
    'favourites' = 'favorites'
    'honour' = 'honor'
    'honours' = 'honors'
    'labour' = 'labor'
    'neighbour' = 'neighbor'
    'centre' = 'center'
    'centres' = 'centers'
    'litre' = 'liter'
    'metre' = 'meter'
    'fibre' = 'fiber'
    'theatre' = 'theater'
}

# Currency and region replacements
$contextReplacements = @{
    '£' = '$'
    'UK South' = 'East US'
    'UK West' = 'West US'
    'UK regions' = 'US regions'
}

Write-Host "Starting British → American English conversion..." -ForegroundColor Cyan
Write-Host "Target directory: $postsDir" -ForegroundColor Cyan
Write-Host ""

$totalFiles = 0
$totalChanges = 0
$filesChanged = 0

Get-ChildItem -Path $postsDir -Filter "*.md" | ForEach-Object {
    $file = $_
    $totalFiles++
    $content = Get-Content $file.FullName -Raw
    $originalContent = $content
    $fileChanges = 0
    $changeDetails = @()
    
    # Apply word replacements
    foreach ($british in $replacements.Keys) {
        $american = $replacements[$british]
        
        # Case-sensitive replacement
        if ($content -match $british) {
            $count = ([regex]::Matches($content, [regex]::Escape($british))).Count
            if ($count -gt 0) {
                $content = $content -replace [regex]::Escape($british), $american
                $fileChanges += $count
                $changeDetails += "  - '$british' → '$american' ($count occurrences)"
            }
        }
        
        # Capitalized version
        $britishCap = $british.Substring(0,1).ToUpper() + $british.Substring(1)
        $americanCap = $american.Substring(0,1).ToUpper() + $american.Substring(1)
        if ($content -match $britishCap) {
            $count = ([regex]::Matches($content, [regex]::Escape($britishCap))).Count
            if ($count -gt 0) {
                $content = $content -replace [regex]::Escape($britishCap), $americanCap
                $fileChanges += $count
                $changeDetails += "  - '$britishCap' → '$americanCap' ($count occurrences)"
            }
        }
    }
    
    # Apply context replacements
    foreach ($old in $contextReplacements.Keys) {
        $new = $contextReplacements[$old]
        if ($content -match [regex]::Escape($old)) {
            $count = ([regex]::Matches($content, [regex]::Escape($old))).Count
            if ($count -gt 0) {
                $content = $content -replace [regex]::Escape($old), $new
                $fileChanges += $count
                $changeDetails += "  - '$old' → '$new' ($count occurrences)"
            }
        }
    }
    
    # Save if changes were made
    if ($content -ne $originalContent) {
        Set-Content -Path $file.FullName -Value $content -NoNewline
        $filesChanged++
        $totalChanges += $fileChanges
        
        Write-Host "✓ $($file.Name)" -ForegroundColor Green
        $changeDetails | ForEach-Object { Write-Host $_ -ForegroundColor Gray }
        Write-Host ""
        
        $changesLog += [PSCustomObject]@{
            File = $file.Name
            Changes = $fileChanges
            Details = ($changeDetails -join "`n")
        }
    }
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "CONVERSION COMPLETE" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Total files scanned: $totalFiles" -ForegroundColor White
Write-Host "Files changed: $filesChanged" -ForegroundColor Green
Write-Host "Total replacements: $totalChanges" -ForegroundColor Green
Write-Host ""

if ($filesChanged -gt 0) {
    Write-Host "Changed files:" -ForegroundColor Yellow
    $changesLog | ForEach-Object {
        Write-Host "  - $($_.File): $($_.Changes) changes" -ForegroundColor White
    }
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "1. Review changes: git diff" -ForegroundColor White
    Write-Host "2. Freeze site: python freeze.py" -ForegroundColor White
    Write-Host "3. Commit: git add posts/ && git commit -m 'Fix: Convert British to American English (improves US CTR)'" -ForegroundColor White
    Write-Host "4. Deploy: git push" -ForegroundColor White
    Write-Host ""
    Write-Host "Expected impact: US CTR 0.14% → 1.5% = +50-100 clicks/month" -ForegroundColor Green
}

# Export detailed log
$changesLog | Export-Csv "british-to-american-changes.csv" -NoTypeInformation
Write-Host "Detailed log saved to: british-to-american-changes.csv" -ForegroundColor Cyan
