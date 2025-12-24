# Fix image paths in all markdown posts
# Remove leading slash from cover paths

$postsDir = "C:\Users\dswann\Documents\GitHub\azure-noob-blog\posts"
$files = Get-ChildItem -Path $postsDir -Filter "*.md"

foreach ($file in $files) {
    $content = Get-Content $file.FullName -Raw
    
    # Replace /static/ with static/ in cover field
    $newContent = $content -replace 'cover: "/static/', 'cover: "static/'
    
    # Only write if something changed
    if ($content -ne $newContent) {
        Set-Content -Path $file.FullName -Value $newContent -NoNewline
        Write-Host "Fixed: $($file.Name)"
    }
}

Write-Host "`nDone! All image paths fixed."
