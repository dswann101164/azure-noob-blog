# normalize-post-tags.ps1
# Normalizes all tags in blog posts to lowercase-hyphenated format
# This eliminates duplicate tag pages and fixes 404 errors

$postsDir = "C:\Users\dswann\Documents\GitHub\azure-noob-blog\posts"

function Slugify-Tag {
    param([string]$tag)
    return $tag.ToLower().Replace(' ', '-').Replace(',', '').Trim()
}

function Normalize-PostTags {
    param([string]$filePath)
    
    try {
        $content = Get-Content -Path $filePath -Raw -Encoding UTF8
        
        # Check if file has frontmatter
        if (-not $content.StartsWith('---')) {
            return @{Changed=$false; Message="No frontmatter"}
        }
        
        # Split frontmatter and body
        $parts = $content -split '---', 3
        if ($parts.Length -lt 3) {
            return @{Changed=$false; Message="Invalid frontmatter"}
        }
        
        $frontmatter = $parts[1]
        $body = $parts[2]
        
        # Find tags line
        if ($frontmatter -notmatch '(?ms)^tags:\s*\[(.*?)\]') {
            if ($frontmatter -notmatch '(?ms)^tags:\s*$') {
                return @{Changed=$false; Message="No tags"}
            }
        }
        
        # Parse tags (handle both list and array formats)
        $tagPattern = 'tags:\s*\[(.*?)\]'
        $listPattern = 'tags:\s*\n((?:^[-\s]+.+\n)+)'
        
        $originalTags = @()
        $tagsMatch = $null
        
        if ($frontmatter -match $tagPattern) {
            $tagsMatch = $matches[1]
            $originalTags = $tagsMatch -split ',' | ForEach-Object { 
                $_.Trim().Trim('"').Trim("'") 
            } | Where-Object { $_ -ne '' }
        }
        elseif ($frontmatter -match $listPattern) {
            $tagsMatch = $matches[1]
            $originalTags = $tagsMatch -split '\n' | ForEach-Object { 
                ($_ -replace '^[-\s]+', '').Trim() 
            } | Where-Object { $_ -ne '' }
        }
        
        if ($originalTags.Count -eq 0) {
            return @{Changed=$false; Message="No tags found"}
        }
        
        # Normalize tags
        $normalizedTags = $originalTags | ForEach-Object { Slugify-Tag $_ }
        
        # Check if changes needed
        $needsUpdate = $false
        for ($i = 0; $i -lt $originalTags.Count; $i++) {
            if ($originalTags[$i] -ne $normalizedTags[$i]) {
                $needsUpdate = $true
                break
            }
        }
        
        if (-not $needsUpdate) {
            return @{Changed=$false; Message="Already normalized"}
        }
        
        # Build new tags line
        $newTagsLine = "tags: [" + ($normalizedTags | ForEach-Object { "`"$_`"" }) -join ", " + "]"
        
        # Replace tags in frontmatter
        if ($frontmatter -match $tagPattern) {
            $newfrontmatter = $frontmatter -replace $tagPattern, $newTagsLine
        }
        else {
            $newfrontmatter = $frontmatter -replace $listPattern, "$newTagsLine`n"
        }
        
        # Rebuild file
        $newContent = "---`n$newfrontmatter---$body"
        
        # Write back
        Set-Content -Path $filePath -Value $newContent -Encoding UTF8 -NoNewline
        
        return @{
            Changed=$true
            Message="Updated: $(($originalTags -join ', ')) → $(($normalizedTags -join ', '))"
            OriginalTags=$originalTags
            NormalizedTags=$normalizedTags
        }
    }
    catch {
        return @{Changed=$false; Message="Error: $_"}
    }
}

# Main execution
Write-Host "=" * 80
Write-Host "NORMALIZING TAGS IN ALL POSTS"
Write-Host "=" * 80
Write-Host ""

$mdFiles = Get-ChildItem -Path $postsDir -Filter "*.md" | Sort-Object Name

$updated = 0
$skipped = 0
$errors = 0

foreach ($file in $mdFiles) {
    $result = Normalize-PostTags -filePath $file.FullName
    
    if ($result.Changed) {
        Write-Host "✓ $($file.Name)" -ForegroundColor Green
        Write-Host "  $($result.Message)" -ForegroundColor Gray
        $updated++
    }
    else {
        if ($result.Message.StartsWith("Error")) {
            Write-Host "✗ $($file.Name): $($result.Message)" -ForegroundColor Red
            $errors++
        }
        else {
            $skipped++
        }
    }
}

Write-Host ""
Write-Host "=" * 80
Write-Host "RESULTS: $updated updated, $skipped already normalized, $errors errors" -ForegroundColor Cyan
Write-Host "=" * 80
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Review the changes: git diff posts/" -ForegroundColor Gray
Write-Host "2. Run freeze.py to regenerate the site" -ForegroundColor Gray
Write-Host "3. Commit and push: git add posts docs && git commit -m 'fix: normalize all tags' && git push" -ForegroundColor Gray
