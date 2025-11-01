# Export-RepoStructure.ps1
# Exports clean repository structure to a text file for sharing
# Usage: .\scripts\Export-RepoStructure.ps1

param(
    [string]$OutputFile = "repo-structure.txt",
    [int]$MaxDepth = 3
)

# Directories to exclude
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

# Function to build tree structure
function Get-TreeStructure {
    param(
        [string]$Path,
        [int]$CurrentDepth = 0,
        [string]$Prefix = ""
    )
    
    if ($CurrentDepth -gt $MaxDepth) { return }
    
    $output = @()
    
    try {
        $items = Get-ChildItem -Path $Path -Force -ErrorAction Stop | 
                 Where-Object { $_.Name -notin $ExcludeDirs }
        
        $dirs = $items | Where-Object { $_.PSIsContainer } | Sort-Object Name
        $files = $items | Where-Object { -not $_.PSIsContainer } | Sort-Object Name
        
        # Process directories
        foreach ($dir in $dirs) {
            $isLast = ($dir -eq $dirs[-1]) -and ($files.Count -eq 0)
            $branch = if ($isLast) { "└── " } else { "├── " }
            $nextPrefix = if ($isLast) { "    " } else { "│   " }
            
            $output += "$Prefix$branch$($dir.Name)/"
            
            if ($CurrentDepth -lt $MaxDepth) {
                $output += Get-TreeStructure -Path $dir.FullName -CurrentDepth ($CurrentDepth + 1) -Prefix "$Prefix$nextPrefix"
            }
        }
        
        # Process files
        foreach ($file in $files) {
            $isLast = ($file -eq $files[-1])
            $branch = if ($isLast) { "└── " } else { "├── " }
            $output += "$Prefix$branch$($file.Name)"
        }
    }
    catch {
        $output += "$Prefix[Error accessing directory]"
    }
    
    return $output
}

# Main execution
$RepoRoot = Get-Location
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

$header = @"
================================================================================
Azure Noob Blog - Repository Structure
Generated: $timestamp
Excluded: $($ExcludeDirs -join ', ')
Max Depth: $MaxDepth
================================================================================

"@

Write-Host "📂 Generating repository structure..." -ForegroundColor Cyan

$structure = Get-TreeStructure -Path $RepoRoot
$content = $header + ($structure -join "`n")

# Write to file
$content | Out-File -FilePath $OutputFile -Encoding UTF8

Write-Host "✅ Structure exported to: $OutputFile" -ForegroundColor Green
Write-Host "   File size: $((Get-Item $OutputFile).Length) bytes" -ForegroundColor Gray

# Show preview
Write-Host "`n📄 Preview (first 20 lines):" -ForegroundColor Yellow
Get-Content $OutputFile | Select-Object -First 20
