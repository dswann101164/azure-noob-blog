# AUTOMATED PDF CONVERSION SCRIPT
# Converts all 7 blog posts to professional PDFs using Pandoc

$ErrorActionPreference = "Stop"

# Configuration
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$blogRoot = Split-Path -Parent $scriptDir
$postsDir = Join-Path $blogRoot "posts"
$outputDir = Join-Path $blogRoot "static\downloads"
$templatePath = Join-Path $scriptDir "azure-template.tex"

Write-Host "=== AZURE ADMIN REFERENCE LIBRARY - PDF GENERATOR ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Blog Root: $blogRoot" -ForegroundColor Gray
Write-Host "Posts Dir: $postsDir" -ForegroundColor Gray
Write-Host "Output Dir: $outputDir" -ForegroundColor Gray
Write-Host "Template: $templatePath" -ForegroundColor Gray
Write-Host ""

# Check if Pandoc is installed
if (!(Get-Command pandoc -ErrorAction SilentlyContinue)) {
    Write-Host "ERROR: Pandoc not found!" -ForegroundColor Red
    Write-Host "Please run: .\install-pandoc.ps1 first" -ForegroundColor Yellow
    exit 1
}

# Check if pdflatex is installed
if (!(Get-Command pdflatex -ErrorAction SilentlyContinue)) {
    Write-Host "ERROR: pdflatex (LaTeX) not found!" -ForegroundColor Red
    Write-Host "Please run: .\install-pandoc.ps1 first" -ForegroundColor Yellow
    exit 1
}

Write-Host "✓ Pandoc and LaTeX installed" -ForegroundColor Green
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
        Subtitle = "The $50K Licensing Mistake Every Admin Must Avoid"
    }
)

# Conversion function
function Convert-ToPDF {
    param (
        [string]$SourcePath,
        [string]$OutputPath,
        [string]$Title,
        [string]$Subtitle
    )
    
    Write-Host "Converting: $Title..." -ForegroundColor Yellow
    
    # Pandoc conversion command
    $pandocArgs = @(
        $SourcePath,
        "-o", $OutputPath,
        "--template=$templatePath",
        "--pdf-engine=pdflatex",
        "--toc",
        "--number-sections",
        "-V", "title=$Title",
        "-V", "subtitle=$Subtitle",
        "-V", "author=David Swann",
        "-V", "date=December 2025",
        "-V", "version=1.0",
        "-V", "geometry:margin=1in",
        "-V", "fontsize=11pt",
        "-V", "linkcolor=blue",
        "-V", "urlcolor=blue",
        "-V", "toccolor=blue",
        "--highlight-style=tango",
        "--variable", "colorlinks=true"
    )
    
    try {
        & pandoc $pandocArgs 2>&1 | Out-Null
        
        if (Test-Path $OutputPath) {
            $fileSize = (Get-Item $OutputPath).Length
            $fileSizeMB = [math]::Round($fileSize / 1MB, 2)
            Write-Host "  ✓ Generated: $OutputPath ($fileSizeMB MB)" -ForegroundColor Green
            return $true
        } else {
            Write-Host "  ✗ Failed to generate PDF" -ForegroundColor Red
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
    Write-Host "2. Check file sizes (should be < 5 MB each)" -ForegroundColor White
    Write-Host "3. Test links and formatting" -ForegroundColor White
    Write-Host "4. Add to git: git add static/downloads/*.pdf" -ForegroundColor White
    Write-Host "5. Commit: git commit -m 'Add 7 PDF reference guides'" -ForegroundColor White
}

if ($failCount -gt 0) {
    Write-Host ""
    Write-Host "Some conversions failed. Check the error messages above." -ForegroundColor Red
}

Write-Host ""
Write-Host "=== DONE ===" -ForegroundColor Cyan
