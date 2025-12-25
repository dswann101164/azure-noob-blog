# FIXED PDF CONVERSION SCRIPT - Handles Unicode/Emojis
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

# Configure MiKTeX to auto-install packages
Write-Host "Configuring MiKTeX..." -ForegroundColor Yellow
try {
    initexmf --set-config-value [MPM]AutoInstall=1 2>&1 | Out-Null
    Write-Host "✓ MiKTeX configured for auto-install" -ForegroundColor Green
} catch {
    Write-Host "⚠ Could not configure MiKTeX auto-install (may need manual package installation)" -ForegroundColor Yellow
}
Write-Host ""

# Define guides to convert
$guides = @(
    @{
        Name = "Linux Commands for Azure Admins"
        SourceFile = "2025-12-08-50-linux-commands-azure.md"
        OutputFile = "Linux-Commands-Azure-Admins-2025.pdf"
        Title = "50 Essential Linux Commands for Azure Admins"
        Subtitle = "Complete 2025 Guide"
    },
    @{
        Name = "Windows Commands for Azure Admins"
        SourceFile = "2025-12-08-50-windows-commands-azure.md"
        OutputFile = "Windows-Commands-Azure-Admins-2025.pdf"
        Title = "50 Essential Windows Commands for Azure Admins"
        Subtitle = "Complete 2025 Guide"
    },
    @{
        Name = "PowerShell 7 Migration"
        SourceFile = "2025-11-03-powershell-7-enterprise-migration.md"
        OutputFile = "PowerShell-7-Migration-Checklist-2025.pdf"
        Title = "PowerShell 7 Enterprise Migration"
        Subtitle = "Complete Migration Checklist"
    },
    @{
        Name = "Terraform Troubleshooting"
        SourceFile = "2025-11-08-terraform-azure-devops-cicd-part6-troubleshooting.md"
        OutputFile = "Terraform-Troubleshooting-Guide-2025.pdf"
        Title = "Terraform Azure DevOps CI/CD Troubleshooting"
        Subtitle = "Complete Reference Guide"
    },
    @{
        Name = "Private Endpoint DNS"
        SourceFile = "2025-10-06-private-endpoint-dns-hybrid-ad.md"
        OutputFile = "Private-Endpoint-DNS-Guide-2025.pdf"
        Title = "Azure Private Endpoint DNS Configuration"
        Subtitle = "Hybrid Active Directory Integration Guide"
    },
    @{
        Name = "Azure Update Manager"
        SourceFile = "2025-09-24-azure-update-manager-reality-check.md"
        OutputFile = "Azure-Update-Manager-Reference-2025.pdf"
        Title = "Azure Update Manager Reality Check"
        Subtitle = "Complete Operational Reference"
    },
    @{
        Name = "Azure Hybrid Benefit"
        SourceFile = "2025-12-11-azure-hybrid-benefit-complete.md"
        OutputFile = "Azure-Hybrid-Benefit-Compliance-Guide-2025.pdf"
        Title = "Azure Hybrid Benefit Compliance Guide"
        Subtitle = "The `$50K Licensing Mistake Every Admin Must Avoid"
    }
)

# Function to clean markdown (remove emojis and problematic Unicode)
function Clean-Markdown {
    param (
        [string]$SourcePath,
        [string]$TempPath
    )
    
    $content = Get-Content -Path $SourcePath -Raw -Encoding UTF8
    
    # Remove common emojis (replace with text equivalents)
    $content = $content -replace '💼', '[Enterprise]'
    $content = $content -replace '⚡', '[Fast]'
    $content = $content -replace '✅', '[checkmark]'
    $content = $content -replace '❌', '[x]'
    $content = $content -replace '⚠️', '[Warning]'
    $content = $content -replace '⚠', '[Warning]'
    $content = $content -replace '🎯', '[Target]'
    $content = $content -replace '🚀', '[Rocket]'
    $content = $content -replace '📊', '[Chart]'
    $content = $content -replace '📈', '[Graph]'
    $content = $content -replace '💰', '[Money]'
    $content = $content -replace '🔧', '[Tool]'
    $content = $content -replace '🔍', '[Search]'
    $content = $content -replace '✓', '[check]'
    $content = $content -replace '✗', '[x]'
    
    # Remove any remaining emoji-like characters (Unicode ranges)
    # This is a broad stroke - removes most emoji ranges
    $content = $content -replace '[\u2600-\u26FF]', ''  # Miscellaneous Symbols
    $content = $content -replace '[\u2700-\u27BF]', ''  # Dingbats
    $content = $content -replace '[\u1F300-\u1F9FF]', '' # Emoticons and misc symbols
    
    # Write cleaned content
    Set-Content -Path $TempPath -Value $content -Encoding UTF8
}

# Conversion function
function Convert-ToPDF {
    param (
        [string]$SourcePath,
        [string]$OutputPath,
        [string]$Title,
        [string]$Subtitle
    )
    
    Write-Host "Converting: $Title..." -ForegroundColor Yellow
    
    # Create cleaned temp file
    $tempFile = Join-Path $tempDir "temp-$(Split-Path $SourcePath -Leaf)"
    Clean-Markdown -SourcePath $SourcePath -TempPath $tempFile
    
    # Pandoc conversion command (simplified - no custom template for now)
    $pandocArgs = @(
        $tempFile,
        "-o", $OutputPath,
        "--pdf-engine=pdflatex",
        "--toc",
        "--number-sections",
        "-V", "geometry:margin=1in",
        "-V", "fontsize=11pt",
        "-V", "colorlinks=true",
        "-V", "linkcolor=blue",
        "-V", "urlcolor=blue",
        "-V", "title=$Title",
        "-V", "author=David Swann - Azure-Noob.com",
        "-V", "date=December 2025"
    )
    
    try {
        $output = & pandoc $pandocArgs 2>&1
        
        if (Test-Path $OutputPath) {
            $fileSize = (Get-Item $OutputPath).Length
            $fileSizeMB = [math]::Round($fileSize / 1MB, 2)
            Write-Host "  ✓ Generated: $OutputPath ($fileSizeMB MB)" -ForegroundColor Green
            
            # Clean up temp file
            Remove-Item $tempFile -ErrorAction SilentlyContinue
            return $true
        } else {
            Write-Host "  ✗ Failed to generate PDF" -ForegroundColor Red
            Write-Host "  Error: $output" -ForegroundColor Red
            return $false
        }
    }
    catch {
        Write-Host "  ✗ Error: $($_.Exception.Message)" -ForegroundColor Red
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
    
    # Check if source file exists
    if (!(Test-Path $sourcePath)) {
        Write-Host "⚠ Skipping: $($guide.Name) - Source file not found" -ForegroundColor Yellow
        Write-Host "  Expected: $sourcePath" -ForegroundColor Gray
        $failCount++
        continue
    }
    
    # Convert
    $success = Convert-ToPDF -SourcePath $sourcePath `
                             -OutputPath $outputPath `
                             -Title $guide.Title `
                             -Subtitle $guide.Subtitle
    
    if ($success) {
        $successCount++
    } else {
        $failCount++
    }
    
    Write-Host ""
}

# Cleanup temp directory
Write-Host "Cleaning up temporary files..." -ForegroundColor Gray
Remove-Item $tempDir -Recurse -Force -ErrorAction SilentlyContinue

# Summary
Write-Host "=== CONVERSION SUMMARY ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Successful: $successCount" -ForegroundColor Green
Write-Host "Failed: $failCount" -ForegroundColor $(if ($failCount -gt 0) { "Red" } else { "Green" })
Write-Host ""

if ($successCount -gt 0) {
    Write-Host "PDFs saved to: $outputDir" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "1. Review PDFs for quality" -ForegroundColor White
    Write-Host "2. Check file sizes" -ForegroundColor White
    Write-Host "3. Add to git: git add static/downloads/*.pdf" -ForegroundColor White
    Write-Host "4. Commit: git commit -m 'Add 7 PDF reference guides'" -ForegroundColor White
}

if ($failCount -gt 0) {
    Write-Host ""
    Write-Host "Some conversions failed. Check the error messages above." -ForegroundColor Red
}

Write-Host ""
Write-Host "=== DONE ===" -ForegroundColor Cyan
