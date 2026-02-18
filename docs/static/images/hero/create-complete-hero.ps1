# Create Azure Cost Optimization Complete Guide Hero Image (PNG)
# Generates: azure-cost-optimization-complete.png

Add-Type -AssemblyName System.Drawing

# Image dimensions
$width = 1200
$height = 630

# Create bitmap and graphics object
$bitmap = New-Object System.Drawing.Bitmap($width, $height)
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)
$graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$graphics.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAlias

# Background gradient (professional blue)
$gradientBrush = New-Object System.Drawing.Drawing2D.LinearGradientBrush(
    [System.Drawing.Point]::new(0, 0),
    [System.Drawing.Point]::new($width, $height),
    [System.Drawing.Color]::FromArgb(255, 0, 21, 41),
    [System.Drawing.Color]::FromArgb(255, 0, 120, 212)
)
$graphics.FillRectangle($gradientBrush, 0, 0, $width, $height)

# Grid pattern overlay
$gridPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(80, 0, 120, 212), 1)
for ($x = 0; $x -lt $width; $x += 40) {
    $graphics.DrawLine($gridPen, $x, 0, $x, $height)
}
for ($y = 0; $y -lt $height; $y += 40) {
    $graphics.DrawLine($gridPen, 0, $y, $width, $y)
}

# Left accent bar
$accentBrush = New-Object System.Drawing.Drawing2D.LinearGradientBrush(
    [System.Drawing.Point]::new(0, 0),
    [System.Drawing.Point]::new(10, 630),
    [System.Drawing.Color]::FromArgb(255, 0, 188, 242),
    [System.Drawing.Color]::FromArgb(255, 0, 212, 170)
)
$graphics.FillRectangle($accentBrush, 0, 0, 10, $height)

# Framework boxes (5 phases)
$azureBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(230, 0, 120, 212))
$greenBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(230, 0, 212, 170))
$whiteBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::White)
$fontBox = New-Object System.Drawing.Font("Arial", 16, [System.Drawing.FontStyle]::Bold)
$stringFormat = New-Object System.Drawing.StringFormat
$stringFormat.Alignment = [System.Drawing.StringAlignment]::Center
$stringFormat.LineAlignment = [System.Drawing.StringAlignment]::Center

# Phase boxes
$boxY = 180
$graphics.FillRectangle($azureBrush, 100, $boxY, 140, 60)
$graphics.DrawString("1. BASELINE", $fontBox, $whiteBrush, 170, $boxY + 30, $stringFormat)

$graphics.FillRectangle($azureBrush, 310, $boxY, 140, 60)
$graphics.DrawString("2. TAGGING", $fontBox, $whiteBrush, 380, $boxY + 30, $stringFormat)

$graphics.FillRectangle($azureBrush, 520, $boxY, 140, 60)
$graphics.DrawString("3. ANALYSIS", $fontBox, $whiteBrush, 590, $boxY + 30, $stringFormat)

$graphics.FillRectangle($azureBrush, 730, $boxY, 140, 60)
$graphics.DrawString("4. EXECUTE", $fontBox, $whiteBrush, 800, $boxY + 30, $stringFormat)

$graphics.FillRectangle($greenBrush, 940, $boxY, 160, 60)
$graphics.DrawString("5. GOVERN", $fontBox, $whiteBrush, 1020, $boxY + 30, $stringFormat)

# Connection lines between boxes
$cyanPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(255, 0, 188, 242), 3)
$graphics.DrawLine($cyanPen, 250, $boxY + 30, 300, $boxY + 30)
$graphics.DrawLine($cyanPen, 460, $boxY + 30, 510, $boxY + 30)
$graphics.DrawLine($cyanPen, 670, $boxY + 30, 720, $boxY + 30)
$graphics.DrawLine($cyanPen, 880, $boxY + 30, 930, $boxY + 30)

# Main title
$fontTitle1 = New-Object System.Drawing.Font("Arial", 48, [System.Drawing.FontStyle]::Bold)
$graphics.DrawString("The Complete Guide to", $fontTitle1, $whiteBrush, 100, 320)

$fontTitle2 = New-Object System.Drawing.Font("Arial", 60, [System.Drawing.FontStyle]::Bold)
$cyanTextBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(255, 0, 212, 170))
$graphics.DrawString("Azure Cost Optimization", $fontTitle2, $cyanTextBrush, 100, 380)

# Subtitle
$fontSubtitle = New-Object System.Drawing.Font("Arial", 28, [System.Drawing.FontStyle]::Regular)
$grayBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(255, 204, 204, 204))
$graphics.DrawString("That Actually Works", $fontSubtitle, $grayBrush, 100, 440)

# Bottom feature badges
$badgeBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(200, 0, 120, 212))
$fontBadge = New-Object System.Drawing.Font("Arial", 18, [System.Drawing.FontStyle]::Regular)
$checkmark = [char]0x2713

$graphics.FillRectangle($badgeBrush, 100, 490, 200, 50)
$graphics.DrawString("$checkmark KQL Queries", $fontBadge, $whiteBrush, 200, 515, $stringFormat)

$graphics.FillRectangle($badgeBrush, 320, 490, 220, 50)
$graphics.DrawString("$checkmark Tagging Strategy", $fontBadge, $whiteBrush, 430, 515, $stringFormat)

$graphics.FillRectangle($badgeBrush, 560, 490, 200, 50)
$graphics.DrawString("$checkmark Governance", $fontBadge, $whiteBrush, 660, 515, $stringFormat)

$graphics.FillRectangle($badgeBrush, 780, 490, 220, 50)
$graphics.DrawString("$checkmark Battle-Tested", $fontBadge, $whiteBrush, 890, 515, $stringFormat)

# Success metric callout (top right)
$graphics.FillRectangle($greenBrush, 950, 80, 180, 100)
$fontMetric = New-Object System.Drawing.Font("Arial", 48, [System.Drawing.FontStyle]::Bold)
$graphics.DrawString("30-40%", $fontMetric, $whiteBrush, 1040, 115, $stringFormat)
$fontMetricLabel = New-Object System.Drawing.Font("Arial", 18, [System.Drawing.FontStyle]::Regular)
$graphics.DrawString("Savings", $fontMetricLabel, $whiteBrush, 1040, 155, $stringFormat)

# "Comprehensive" badge (bottom right)
$graphics.FillRectangle($greenBrush, 950, 500, 180, 60)
$fontComprehensive = New-Object System.Drawing.Font("Arial", 20, [System.Drawing.FontStyle]::Bold)
$graphics.DrawString("COMPREHENSIVE", $fontComprehensive, $whiteBrush, 1040, 530, $stringFormat)

# Save the image
$outputPath = Join-Path $PSScriptRoot "azure-cost-optimization-complete.png"
$bitmap.Save($outputPath, [System.Drawing.Imaging.ImageFormat]::Png)

# Cleanup
$graphics.Dispose()
$bitmap.Dispose()

Write-Host "Hero image created: $outputPath" -ForegroundColor Green
