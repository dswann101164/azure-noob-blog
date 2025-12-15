# Create Azure Cost Optimization Facade Hero Image (PNG)
# Generates: azure-cost-optimization-facade.png

Add-Type -AssemblyName System.Drawing

# Image dimensions
$width = 1200
$height = 630

# Create bitmap and graphics object
$bitmap = New-Object System.Drawing.Bitmap($width, $height)
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)
$graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$graphics.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAlias

# Background gradient (dark blue to darker blue)
$gradientBrush = New-Object System.Drawing.Drawing2D.LinearGradientBrush(
    [System.Drawing.Point]::new(0, 0),
    [System.Drawing.Point]::new($width, $height),
    [System.Drawing.Color]::FromArgb(255, 15, 32, 39),
    [System.Drawing.Color]::FromArgb(255, 44, 83, 100)
)
$graphics.FillRectangle($gradientBrush, 0, 0, $width, $height)

# Warning stripe (left side)
$redBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(255, 255, 68, 68))
$graphics.FillRectangle($redBrush, 0, 0, 20, $height)

# Azure blue accent box (top left)
$azureBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(255, 0, 120, 212))
$graphics.FillRectangle($azureBrush, 50, 50, 80, 80)

# Dollar sign in box
$fontLarge = New-Object System.Drawing.Font("Arial", 48, [System.Drawing.FontStyle]::Bold)
$whiteBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::White)
$stringFormat = New-Object System.Drawing.StringFormat
$stringFormat.Alignment = [System.Drawing.StringAlignment]::Center
$stringFormat.LineAlignment = [System.Drawing.StringAlignment]::Center
$graphics.DrawString("$", $fontLarge, $whiteBrush, 90, 90, $stringFormat)

# Crossed out "Advisor" badge (top right)
$advisorBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(100, 0, 120, 212))
$graphics.FillEllipse($advisorBrush, 1040, 40, 120, 120)

$fontMedium = New-Object System.Drawing.Font("Arial", 20, [System.Drawing.FontStyle]::Regular)
$grayBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(150, 255, 255, 255))
$graphics.DrawString("ADVISOR", $fontMedium, $grayBrush, 1100, 100, $stringFormat)

# X mark over advisor
$redPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(255, 255, 68, 68), 8)
$graphics.DrawLine($redPen, 1050, 60, 1150, 140)
$graphics.DrawLine($redPen, 1150, 60, 1050, 140)

# Main title
$fontTitle = New-Object System.Drawing.Font("Arial", 64, [System.Drawing.FontStyle]::Bold)
$graphics.DrawString("Cost Optimization", $fontTitle, $whiteBrush, 100, 280)

$redTextBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(255, 255, 107, 107))
$graphics.DrawString("Is A Façade", $fontTitle, $redTextBrush, 100, 360)

# Subtitle line
$graphics.FillRectangle($redBrush, 100, 400, 800, 4)

# Subtitle text
$fontSubtitle = New-Object System.Drawing.Font("Arial", 32, [System.Drawing.FontStyle]::Regular)
$grayTextBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(255, 170, 170, 170))
$graphics.DrawString("And Microsoft Knows It", $fontSubtitle, $grayTextBrush, 100, 460)

# Bottom metrics
$fontMono = New-Object System.Drawing.Font("Courier New", 20, [System.Drawing.FontStyle]::Regular)
$cyanBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(255, 0, 188, 242))
$graphics.DrawString("Advisor Recommendations: 47", $fontMono, $cyanBrush, 100, 560)
$graphics.DrawString("Actually Useful: 3", $fontMono, $redBrush, 100, 590)

# "Reality Check" badge (bottom right)
$graphics.FillRectangle($redBrush, 950, 500, 200, 60)
$fontBadge = New-Object System.Drawing.Font("Arial", 24, [System.Drawing.FontStyle]::Bold)
$graphics.DrawString("REALITY CHECK", $fontBadge, $whiteBrush, 1050, 530, $stringFormat)

# Save the image
$outputPath = Join-Path $PSScriptRoot "azure-cost-optimization-facade.png"
$bitmap.Save($outputPath, [System.Drawing.Imaging.ImageFormat]::Png)

# Cleanup
$graphics.Dispose()
$bitmap.Dispose()

Write-Host "Hero image created: $outputPath" -ForegroundColor Green
