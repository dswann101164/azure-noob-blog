# Fix all tags in all posts to use lowercase-hyphenated format
$PostsDir = "C:\Users\dswann\Documents\GitHub\azure-noob-blog\posts"
$ChangedFiles = 0
$TotalFiles = 0

function Slugify-Tag {
    param([string]$Tag)
    return $Tag.ToLower().Replace(' ', '-').Replace(',', '').Trim()
}

Get-ChildItem "$PostsDir\*.md" | ForEach-Object {
    $TotalFiles++
    $FilePath = $_.FullName
    $Lines = Get-Content $FilePath
    
    $InTags = $false
    $NeedsChange = $false
    $NewLines = @()
    
    for ($i = 0; $i -lt $Lines.Count; $i++) {
        $Line = $Lines[$i]
        
        # Check if we're entering the tags section
        if ($Line -match '^tags:\s*$') {
            $InTags = $true
            $NewLines += $Line
            continue
        }
        
        # If we're in tags and hit a non-tag line, we're done with tags
        if ($InTags -and $Line -notmatch '^\s*-\s*') {
            $InTags = $false
        }
        
        # Process tag lines
        if ($InTags -and $Line -match '^\s*-\s*(.+)$') {
            $OriginalTag = $Matches[1].Trim()
            $FixedTag = Slugify-Tag -Tag $OriginalTag
            
            if ($OriginalTag -ne $FixedTag) {
                $NeedsChange = $true
                $NewLines += "- $FixedTag"
                Write-Host "  [$($_.Name)] '$OriginalTag' → '$FixedTag'"
            } else {
                $NewLines += $Line
            }
        } else {
            $NewLines += $Line
        }
    }
    
    if ($NeedsChange) {
        $NewLines | Set-Content -Path $FilePath
        $ChangedFiles++
        Write-Host "✓ $($_.Name)" -ForegroundColor Green
    }
}

Write-Host "`n$('=' * 80)" -ForegroundColor Cyan
Write-Host "SUMMARY" -ForegroundColor Cyan
Write-Host "$('=' * 80)" -ForegroundColor Cyan
Write-Host "Total files: $TotalFiles"
Write-Host "Changed files: $ChangedFiles" -ForegroundColor Green
Write-Host "`n✓ TAG FIX COMPLETE - Ready to freeze" -ForegroundColor Green
