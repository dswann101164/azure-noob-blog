# Show-RepoStructure.ps1
# Smart directory listing that excludes generated/large folders
# Usage: .\scripts\Show-RepoStructure.ps1

param(
    [string]$Path = ".",
    [int]$MaxDepth = 3,
    [switch]$ShowFiles
)

# Directories to exclude from listing
$ExcludeDirs = @(
    'docs',
    '.venv',
    '__pycache__',
    '.git',
    'node_modules',
    '.pytest_cache',
    '.mypy_cache',
    'dist',
    'build'
)

# Function to display tree structure
function Show-Tree {
    param(
        [string]$Path,
        [int]$CurrentDepth = 0,
        [string]$Prefix = ""
    )
    
    if ($CurrentDepth -gt $MaxDepth) { return }
    
    try {
        $items = Get-ChildItem -Path $Path -Force -ErrorAction Stop | 
                 Where-Object { $_.Name -notin $ExcludeDirs }
        
        $dirs = $items | Where-Object { $_.PSIsContainer } | Sort-Object Name
        $files = $items | Where-Object { -not $_.PSIsContainer } | Sort-Object Name
        
        # Show directories first
        foreach ($dir in $dirs) {
            $isLast = ($dir -eq $dirs[-1]) -and (-not $ShowFiles -or $files.Count -eq 0)
            $branch = if ($isLast) { "└── " } else { "├── " }
            $nextPrefix = if ($isLast) { "    " } else { "│   " }
            
            Write-Host "$Prefix$branch$($dir.Name)/" -ForegroundColor Cyan
            
            if ($CurrentDepth -lt $MaxDepth) {
                Show-Tree -Path $dir.FullName -CurrentDepth ($CurrentDepth + 1) -Prefix "$Prefix$nextPrefix"
            }
        }
        
        # Show files if requested
        if ($ShowFiles) {
            foreach ($file in $files) {
                $isLast = ($file -eq $files[-1])
                $branch = if ($isLast) { "└── " } else { "├── " }
                
                Write-Host "$Prefix$branch$($file.Name)" -ForegroundColor Gray
            }
        }
    }
    catch {
        Write-Warning "Cannot access: $Path"
    }
}

# Main execution
$RepoRoot = Resolve-Path $Path
Write-Host "`n📂 Repository Structure: $RepoRoot" -ForegroundColor Green
Write-Host "   Excluding: $($ExcludeDirs -join ', ')" -ForegroundColor Yellow
Write-Host "   Max Depth: $MaxDepth" -ForegroundColor Yellow
if (-not $ShowFiles) {
    Write-Host "   (Use -ShowFiles to include files)" -ForegroundColor Yellow
}
Write-Host ""

Show-Tree -Path $RepoRoot

Write-Host "`n✅ Done!`n" -ForegroundColor Green
