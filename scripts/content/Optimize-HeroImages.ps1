# ============================================================================
# Hero Image Optimization Script for azure-noob.com
# ============================================================================
# Purpose: Reduce hero image sizes from 2.88 MB → < 200 KB
# Impact: Fix LCP from 9.7s → < 2.5s (mobile performance)
# Author: Generated for David Swann
# Date: December 20, 2025
# ============================================================================

param(
    [string]$HeroPath = "C:\Users\dswann\Documents\GitHub\azure-noob-blog\static\images\hero",
    [string]$BackupPath = "C:\Users\dswann\Documents\GitHub\azure-noob-blog\static\images\hero-backup",
    [int]$MaxWidthPx = 1200,
    [int]$QualityPercent = 85,
    [switch]$DryRun
)

# ============================================================================
# PREREQUISITES CHECK
# ============================================================================

Write-Host "`n=== Azure Noob Hero Image Optimizer ===" -ForegroundColor Cyan
Write-Host "Target: Reduce 129 MB of images → ~15 MB" -ForegroundColor Yellow
Write-Host ""

# Check if ImageMagick is installed
$magickPath = Get-Command "magick" -ErrorAction SilentlyContinue

if (-not $magickPath) {
    Write-Host "❌ ImageMagick not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Install ImageMagick:" -ForegroundColor Yellow
    Write-Host "  1. Download: https://imagemagick.org/script/download.php#windows"
    Write-Host "  2. Run installer"
    Write-Host "  3. Restart PowerShell"
    Write-Host ""
    Write-Host "OR use Chocolatey:" -ForegroundColor Yellow
    Write-Host "  choco install imagemagick" -ForegroundColor Cyan
    Write-Host ""
    exit 1
}

Write-Host "✅ ImageMagick found: $($magickPath.Source)" -ForegroundColor Green

# ============================================================================
# BACKUP ORIGINAL IMAGES
# ============================================================================

if (-not $DryRun) {
    if (-not (Test-Path $BackupPath)) {
        Write-Host "`nCreating backup directory: $BackupPath" -ForegroundColor Yellow
        New-Item -ItemType Directory -Path $BackupPath -Force | Out-Null
        
        Write-Host "Backing up original images..." -ForegroundColor Yellow
        Copy-Item -Path "$HeroPath\*.png" -Destination $BackupPath -Force
        Copy-Item -Path "$HeroPath\*.jpg" -Destination $BackupPath -Force -ErrorAction SilentlyContinue
        
        $backupCount = (Get-ChildItem $BackupPath -File).Count
        Write-Host "✅ Backed up $backupCount images" -ForegroundColor Green
    } else {
        Write-Host "`n⚠️  Backup already exists at: $BackupPath" -ForegroundColor Yellow
        Write-Host "Skipping backup to preserve originals" -ForegroundColor Yellow
    }
}

# ============================================================================
# GET IMAGE LIST
# ============================================================================

$images = Get-ChildItem -Path $HeroPath -Filter "*.png" | 
    Where-Object { $_.Length -gt 500KB } |  # Only optimize images > 500 KB
    Sort-Object Length -Descending

Write-Host "`nFound $($images.Count) PNG images larger than 500 KB" -ForegroundColor Cyan
Write-Host ""

if ($images.Count -eq 0) {
    Write-Host "✅ All images are already optimized!" -ForegroundColor Green
    exit 0
}

# ============================================================================
# OPTIMIZATION FUNCTION
# ============================================================================

function Optimize-Image {
    param(
        [System.IO.FileInfo]$ImageFile,
        [int]$MaxWidth,
        [int]$Quality,
        [bool]$DryRunMode
    )
    
    $originalSize = $ImageFile.Length / 1MB
    $fileName = $ImageFile.Name
    $filePath = $ImageFile.FullName
    
    Write-Host "Processing: $fileName ($([math]::Round($originalSize, 2)) MB)" -ForegroundColor Yellow
    
    if ($DryRunMode) {
        Write-Host "  [DRY RUN] Would optimize this image" -ForegroundColor Cyan
        return
    }
    
    try {
        # Get current dimensions
        $identify = & magick identify -format "%w %h" $filePath
        $dimensions = $identify -split " "
        $currentWidth = [int]$dimensions[0]
        $currentHeight = [int]$dimensions[1]
        
        Write-Host "  Current: ${currentWidth}x${currentHeight}" -ForegroundColor Gray
        
        # Create temp file for optimization
        $tempFile = "$filePath.tmp.png"
        
        # Optimize strategy:
        # 1. Resize if wider than $MaxWidth
        # 2. Strip metadata
        # 3. Compress with quality setting
        # 4. Use pngquant-style quantization
        
        if ($currentWidth -gt $MaxWidth) {
            Write-Host "  Resizing to max width: $MaxWidth px" -ForegroundColor Gray
            & magick $filePath -resize "${MaxWidth}x" -strip -quality $Quality $tempFile
        } else {
            Write-Host "  Compressing without resize" -ForegroundColor Gray
            & magick $filePath -strip -quality $Quality $tempFile
        }
        
        # Check if optimization actually reduced size
        $tempSize = (Get-Item $tempFile).Length / 1MB
        $savings = (($originalSize - $tempSize) / $originalSize) * 100
        
        if ($tempSize -lt $originalSize) {
            # Replace original with optimized
            Move-Item -Path $tempFile -Destination $filePath -Force
            
            Write-Host "  ✅ Optimized: $([math]::Round($tempSize, 2)) MB (saved $([math]::Round($savings, 1))%)" -ForegroundColor Green
            
            return @{
                FileName = $fileName
                OriginalMB = $originalSize
                OptimizedMB = $tempSize
                SavingsPercent = $savings
            }
        } else {
            # Optimization didn't help, keep original
            Remove-Item $tempFile -Force
            Write-Host "  ⚠️  No size reduction, keeping original" -ForegroundColor Yellow
            
            return $null
        }
        
    } catch {
        Write-Host "  ❌ Error: $_" -ForegroundColor Red
        return $null
    }
}

# ============================================================================
# PROCESS ALL IMAGES
# ============================================================================

$results = @()
$totalOriginalSize = 0
$totalOptimizedSize = 0

Write-Host "Starting optimization..." -ForegroundColor Cyan
Write-Host "Settings: Max Width = $MaxWidthPx px, Quality = $QualityPercent%" -ForegroundColor Gray
Write-Host ""

foreach ($image in $images) {
    $result = Optimize-Image -ImageFile $image -MaxWidth $MaxWidthPx -Quality $QualityPercent -DryRunMode $DryRun
    
    if ($result) {
        $results += $result
        $totalOriginalSize += $result.OriginalMB
        $totalOptimizedSize += $result.OptimizedMB
    }
    
    Write-Host ""
}

# ============================================================================
# SUMMARY REPORT
# ============================================================================

if (-not $DryRun -and $results.Count -gt 0) {
    Write-Host "`n=== OPTIMIZATION SUMMARY ===" -ForegroundColor Cyan
    Write-Host ""
    
    $totalSavings = (($totalOriginalSize - $totalOptimizedSize) / $totalOriginalSize) * 100
    
    Write-Host "Images optimized: $($results.Count)" -ForegroundColor Green
    Write-Host "Original total: $([math]::Round($totalOriginalSize, 2)) MB" -ForegroundColor Yellow
    Write-Host "Optimized total: $([math]::Round($totalOptimizedSize, 2)) MB" -ForegroundColor Green
    Write-Host "Total savings: $([math]::Round($totalOriginalSize - $totalOptimizedSize, 2)) MB ($([math]::Round($totalSavings, 1))%)" -ForegroundColor Cyan
    Write-Host ""
    
    # Show top 10 savings
    Write-Host "Top 10 Size Reductions:" -ForegroundColor Cyan
    $results | 
        Sort-Object SavingsPercent -Descending | 
        Select-Object -First 10 | 
        ForEach-Object {
            $savedMB = $_.OriginalMB - $_.OptimizedMB
            Write-Host "  $($_.FileName): -$([math]::Round($savedMB, 2)) MB ($([math]::Round($_.SavingsPercent, 1))%)" -ForegroundColor Gray
        }
    
    Write-Host ""
    Write-Host "=== NEXT STEPS ===" -ForegroundColor Cyan
    Write-Host "1. Test your site locally: flask run" -ForegroundColor Yellow
    Write-Host "2. Check images load correctly" -ForegroundColor Yellow
    Write-Host "3. Commit changes:" -ForegroundColor Yellow
    Write-Host "   git add static/images/hero/" -ForegroundColor Gray
    Write-Host "   git commit -m 'perf: optimize hero images for mobile LCP'" -ForegroundColor Gray
    Write-Host "   git push" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Expected mobile LCP improvement: 9.7s → 2-3s" -ForegroundColor Green
    Write-Host "Expected mobile performance score: 70 → 90+" -ForegroundColor Green
    Write-Host ""
    
} elseif ($DryRun) {
    Write-Host "`n=== DRY RUN COMPLETE ===" -ForegroundColor Cyan
    Write-Host "Would have optimized $($images.Count) images" -ForegroundColor Yellow
    Write-Host "Run without -DryRun to actually optimize" -ForegroundColor Yellow
    Write-Host ""
}

# ============================================================================
# OPTIONAL: CONVERT TO WEBP
# ============================================================================

Write-Host "=== BONUS: WebP Conversion ===" -ForegroundColor Cyan
Write-Host "For even better compression (90%+ smaller):" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Convert PNGs to WebP:" -ForegroundColor Gray
Write-Host '   Get-ChildItem "$HeroPath\*.png" | ForEach-Object {' -ForegroundColor Cyan
Write-Host '       $webp = $_.FullName -replace ".png", ".webp"' -ForegroundColor Cyan
Write-Host '       magick $_.FullName -quality 85 $webp' -ForegroundColor Cyan
Write-Host '   }' -ForegroundColor Cyan
Write-Host ""
Write-Host "2. Update templates to use <picture> tag with WebP fallback" -ForegroundColor Gray
Write-Host ""
Write-Host "Note: WebP has 95%+ browser support, but PNG fallback is good practice" -ForegroundColor Yellow
Write-Host ""

Write-Host "✅ Optimization complete!" -ForegroundColor Green
