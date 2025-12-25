# FIXED PDF CONVERSION SCRIPT v2 - Preserves YAML Frontmatter
# Converts all 7 blog posts to professional PDFs using Pandoc

$ErrorActionPreference = "Continue"

# Configuration
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$blogRoot = Split-Path -Parent $scriptDir
$postsDir = Join-Path $blogRoot "posts"
$outputDir = Join-Path $blogRoot "static\downloads"
$tempDir = Join-Path $blogRoot "temp-pdf-conversion"

Write-Host "=== AZURE ADMIN REFERENCE LIBRARY - PDF GENERATOR ===" -ForegroundColor Cyan
Write-Host ""

# Create temp directory
if (!(Test-Path $tempDir)) {
    New-Item -ItemType Directory -Path $tempDir | Out-Null
}

# Check dependencies
if (!(Get-Command pandoc -ErrorAction SilentlyContinue)) {
    Write-Host "ERROR: Pandoc not found!" -ForegroundColor Red
    exit 1
}

if (!(Get-Command pdflatex -ErrorAction SilentlyContinue)) {
    Write-Host "ERROR: pdflatex not found!" -ForegroundColor Red
    exit 1
}

Write-Host "✓ Pandoc and LaTeX installed" -ForegroundColor Green
Write-Host ""

# Configure MiKTeX
Write-Host "Configuring MiKTeX..." -ForegroundColor Yellow
try {
    initexmf --set-config-value [MPM]AutoInstall=1 2>&1 | Out-Null
    Write-Host "✓ MiKTeX configured" -ForegroundColor Green
} catch {
    Write-Host "⚠ MiKTeX configuration skipped" -ForegroundColor Yellow
}
Write-Host ""

# Define guides
$guides = @(
    @{
        Name = "Linux Commands for Azure Admins"
        SourceFile = "2025-12-08-50-linux-commands-azure.md"
        OutputFile = "Linux-Commands-Azure-Admins-2025.pdf"
        Title = "50 Essential Linux Commands for Azure Admins"
    },
    @{
        Name = "Windows Commands for Azure Admins"
        SourceFile = "2025-12-08-50-windows-commands-azure.md"
        OutputFile = "Windows-Commands-Azure-Admins-2025.pdf"
        Title = "50 Essential Windows Commands for Azure Admins"
    },
    @{
        Name = "PowerShell 7 Migration"
        SourceFile = "2025-11-03-powershell-7-enterprise-migration.md"
        OutputFile = "PowerShell-7-Migration-Checklist-2025.pdf"
        Title = "PowerShell 7 Enterprise Migration"
    },
    @{
        Name = "Terraform Troubleshooting"
        SourceFile = "2025-11-08-terraform-azure-devops-cicd-part6-troubleshooting.md"
        OutputFile = "Terraform-Troubleshooting-Guide-2025.pdf"
        Title = "Terraform CI/CD Troubleshooting"
    },
    @{
        Name = "Private Endpoint DNS"
        SourceFile = "2025-10-06-private-endpoint-dns-hybrid-ad.md"
        OutputFile = "Private-Endpoint-DNS-Guide-2025.pdf"
        Title = "Azure Private Endpoint DNS Configuration"
    },
    @{
        Name = "Azure Update Manager"
        SourceFile = "2025-09-24-azure-update-manager-reality-check.md"
        OutputFile = "Azure-Update-Manager-Reference-2025.pdf"
        Title = "Azure Update Manager Reality Check"
    },
    @{
        Name = "Azure Hybrid Benefit"
        SourceFile = "2025-12-11-azure-hybrid-benefit-complete.md"
        OutputFile = "Azure-Hybrid-Benefit-Compliance-Guide-2025.pdf"
        Title = "Azure Hybrid Benefit Compliance Guide"
    }
)

# Function to clean markdown
function Clean-Markdown {
    param (
        [string]$SourcePath,
        [string]$TempPath
    )
    
    # Read file as bytes to avoid encoding issues
    $bytes = [System.IO.File]::ReadAllBytes($SourcePath)
    $content = [System.Text.Encoding]::UTF8.GetString($bytes)
    
    # Replace emojis with text equivalents
    $content = $content -replace '💼', '[Enterprise]'
    $content = $content -replace '⚡', ''
    $content = $content -replace '✅', '[checkmark]'
    $content = $content -replace '❌', '[x]'
    $content = $content -replace '⚠️', '[Warning]'
    $content = $content -replace '⚠', '[Warning]'
    $content = $content -replace '🎯', ''
    $content = $content -replace '🚀', ''
    $content = $content -replace '📊', ''
    $content = $content -replace '📈', ''
    $content = $content -replace '💰', ''
    $content = $content -replace '🔧', ''
    $content = $content -replace '🔍', ''
    $content = $content -replace '✓', '[check]'
    $content = $content -replace '✗', '[x]'
    $content = $content -replace '→', '->'
    $content = $content -replace '←', '<-'
    
    # Remove remaining emoji ranges
    $content = $content -replace '[\u2600-\u26FF]', ''
    $content = $content -replace '[\u2700-\u27BF]', ''
    $content = $content -replace '[\u1F300-\u1F9FF]', ''
    
    # Write as UTF-8 without BOM
    $utf8NoBom = New-Object System.Text.UTF8Encoding $false
    [System.IO.File]::WriteAllText($TempPath, $content, $utf8NoBom)
}

# Conversion function
function Convert-ToPDF {
    param (
        [string]$SourcePath,
        [string]$OutputPath,
        [string]$Title
    )
    
    Write-Host "Converting: $Title..." -ForegroundColor Yellow
    
    # Create cleaned temp file
    $tempFile = Join-Path $tempDir "temp-$(Split-Path $SourcePath -Leaf)"
    
    try {
        Clean-Markdown -SourcePath $SourcePath -TempPath $tempFile
    } catch {
        Write-Host "  ✗ Failed to clean markdown: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
    
    # Simple Pandoc conversion
    $pandocArgs = @(
        $tempFile,
        "-o", $OutputPath,
        "--pdf-engine=pdflatex",
        "--toc",
        "-V", "geometry:margin=1in",
        "-V", "fontsize=11pt",
        "-V", "documentclass=article",
        "-V", "colorlinks=true"
    )
    
    try {
        $null = & pandoc $pandocArgs 2>&1
        
        if (Test-Path $OutputPath) {
            $fileSize = (Get-Item $OutputPath).Length
            $fileSizeMB = [math]::Round($fileSize / 1MB, 2)
            Write-Host "  ✓ Success: $fileSizeMB MB" -ForegroundColor Green
            Remove-Item $tempFile -ErrorAction SilentlyContinue
            return $true
        } else {
            Write-Host "  ✗ PDF not created" -ForegroundColor Red
            return $false
        }
    }
    catch {
        Write-Host "  ✗ Conversion failed: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Convert all guides
$successCount = 0
$failCount = 0

Write-Host "=== STARTING PDF CONVERSION ===" -ForegroundColor Cyan
Write-Host ""

foreach ($guide in $guides) {
    $sourcePath = Join-Path $postsDir $guide.SourceFile
    $outputPath = Join-Path $outputDir $guide.OutputFile
    
    if (!(Test-Path $sourcePath)) {
        Write-Host "⚠ Skipping: $($guide.Name) - Not found" -ForegroundColor Yellow
        $failCount++
        continue
    }
    
    $success = Convert-ToPDF -SourcePath $sourcePath `
                             -OutputPath $outputPath `
                             -Title $guide.Title
    
    if ($success) {
        $successCount++
    } else {
        $failCount++
    }
    
    Write-Host ""
}

# Cleanup
Remove-Item $tempDir -Recurse -Force -ErrorAction SilentlyContinue

# Summary
Write-Host "=== SUMMARY ===" -ForegroundColor Cyan
Write-Host "Successful: $successCount" -ForegroundColor Green
Write-Host "Failed: $failCount" -ForegroundColor $(if ($failCount -gt 0) { "Red" } else { "Green" })

if ($successCount -gt 0) {
    Write-Host ""
    Write-Host "PDFs saved to: $outputDir" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next: git add static/downloads/*.pdf" -ForegroundColor Yellow
}

Write-Host ""
