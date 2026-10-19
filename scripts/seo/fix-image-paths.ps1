# Fix image paths in all markdown posts
# Remove leading slash from cover paths

$postsDir = ".\posts"
$files = Get-ChildItem -Path $postsDir -Filter "*.md"

# Posts are UTF-8 without BOM; plain Get-Content/Set-Content in PS 5.1 use ANSI.
$utf8NoBom = New-Object System.Text.UTF8Encoding $false

foreach ($file in $files) {
    $content = [System.IO.File]::ReadAllText($file.FullName, $utf8NoBom)
    
    # Replace /static/ with static/ in cover field
    $newContent = $content -replace 'cover: "/static/', 'cover: "static/'
    
    # Only write if something changed
    if ($content -cne $newContent) {
        [System.IO.File]::WriteAllText($file.FullName, $newContent, $utf8NoBom)
        Write-Host "Fixed: $($file.Name)"
    }
}

Write-Host "`nDone! All image paths fixed."
