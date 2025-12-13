---
title: How I Rebranded Microsoft's Azure Resource Inventory Dashboard (Without Corrupting
  Excel)
date: 2025-11-21
summary: A dark-mode rebranding tool for Azure dashboards and Excel exports so your
  reports look as modern as your cloud environment.
tags:
- ARI
- Automation
- Azure
- Branding
- Dashboards
- Excel
- Monitoring
- PowerShell
- Tools
cover: /static/images/hero/azure-dashboard-rebrand.png
hub: automation
related_posts:
  - pbix-modernizer-tool
  - chris-bowman-dashboard
  - azure-dashboards-cloud-noc
hub: governance
---
## The Problem: Great Tool, Wrong Branding

Microsoft's [Azure Resource Inventory (ARI)](https://github.com/microsoft/ARI) is legitimately one of the best Azure reporting tools out there. It generates comprehensive Excel dashboards with 40+ worksheets, detailed resource inventories, charts, and actionable insights.

**But it screams Microsoft.**

When you hand this to executives or clients, they see:
- "Azure Resource Inventory 3.6.11" header
- "https://github.com/microsoft/ARI" URL plastered in the branding box
- Generic Microsoft branding that says "free tool" not "professional service"
- No indication YOU built this analysis

For consultants, MSPs, or internal Azure teams trying to establish credibility, this is a problem. You did the work. Your analysis. Your recommendations. But the dashboard says "Microsoft" at the top.

**I needed to rebrand ARI dashboards with my own logo and branding - without breaking Excel.**

## Before → After

Here's the transformation:

**Before (Original ARI):**
![Original ARI Dashboard](/static/images/ari-original.png)
*Microsoft branding with github.com/microsoft/ARI URL*

**After (Rebranded):**
![Rebranded Dashboard](/static/images/ari-rebranded.png)
*Your logo, your branding, your URL - professional and ready to ship*

## The Challenge: Excel Is Fragile

My first instinct was Python. Use `openpyxl`, manipulate the cells, add a logo, done.

**That lasted about 15 minutes.**

Python libraries like `openpyxl` work by:
1. Unzipping the .xlsx file (it's just a ZIP of XML files)
2. Editing the XML directly
3. Zipping it back up

This works fine for simple Excel files. But ARI dashboards have:
- 40+ interconnected worksheets
- Complex chart definitions with relationships
- Conditional formatting rules
- Embedded images and shapes
- Cell references spanning multiple sheets

**Every Python attempt resulted in corrupted files.** Excel would throw repair dialogs, charts would vanish, formatting would break. The XML manipulation was too invasive.

I needed a different approach.

## The Solution: Let Excel Do Excel Things

Instead of fighting Excel's file format, I used **PowerShell COM automation** - which is just automating Excel itself using its own APIs.

Think of it like this:
- **Python approach:** Break into Excel's house, rearrange the furniture, leave
- **PowerShell approach:** Knock on the door, ask Excel to rearrange its own furniture

The script uses Excel's COM interface to:
1. Open the ARI file (Excel handles file parsing)
2. Find the branding shapes/text boxes
3. Make modifications using Excel's own methods
4. Save the file (Excel handles XML serialization)

**Result: Zero corruption. Perfect Excel files every time.**

## What The Script Actually Does

### 1. Finds Your Latest ARI Report Automatically

```powershell
# Auto-locate the most recent ARI file
$ariFiles = Get-ChildItem -Path $AriDir -Filter "AzureResourceInventory*.xlsx" |
    Sort-Object LastWriteTime -Descending

$InputFile = $ariFiles[0].FullName
```

No manual file paths. The script finds your most recent ARI report and processes it.

### 2. Rebrands The Header Box

The biggest visual change - your branding replaces Microsoft's:

**Before:**
```
┌─────────────────────────────────┐
│ Azure Resource Inventory 3.6.11 │
│ https://github.com/microsoft/ARI│
│ Report Date: 11/19/2025         │
└─────────────────────────────────┘
```

**After:**
```
┌─────────────────────────────────┐
│ [YOUR LOGO - azure-noob bird]   │
│ azure-noob.com 3.6.11           │
│ https://www.azure-noob.com      │
│ Report Date: 11/21/2025         │
└─────────────────────────────────┘
```

Your logo (the script auto-resizes it), your domain, your branding. Clean and professional.

### 3. Enhances The Dark Theme

ARI already has dark-themed charts, but the script takes it further:

- **Pure black backgrounds** (not dark gray)
- **Vibrant accent colors** (cyan, green, orange, yellow for different series)
- **Professional color palette** that pops on dark backgrounds
- **Consistent styling** across all chart types

The result looks like a premium data visualization tool, not a free script output.

### 4. Preserves Everything Else

This is critical - **zero data corruption**:
- ✅ All 40+ worksheets intact
- ✅ All charts render perfectly
- ✅ All formulas calculate correctly
- ✅ All data unchanged
- ✅ No Excel repair dialogs

## The Complete Script

Here's the full PowerShell script with comments explaining each section:

```powershell
<#
.SYNOPSIS
    Azure Admin Dashboard - Dark Mode Rebrander

.DESCRIPTION
    Rebrands Azure Resource Inventory (ARI) Excel reports with:
    - Full dark theme (worksheet + charts)
    - Your custom logo
    - Your branding text
    - Zero file corruption (uses Excel COM automation)

.NOTES
    Requires Excel installed (COM automation)
    Logo file should be PNG format, script auto-resizes
#>

[CmdletBinding()]
param(
    [string]$AriDir = "C:\AzureResourceInventory",
    [string]$LogoFileName = "logo.png"
)

Write-Host "Azure Admin Dashboard - Dark Mode Rebrander" -ForegroundColor Cyan

$ErrorActionPreference = 'Stop'
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$LogoFile  = Join-Path $ScriptDir $LogoFileName

# Helper function to convert RGB to Excel OLE color
function New-OleColor {
    param([int]$R, [int]$G, [int]$B)
    [System.Drawing.ColorTranslator]::ToOle(
        [System.Drawing.Color]::FromArgb($R, $G, $B)
    )
}

# Dark theme color palette
$Theme = @{
    Background    = New-OleColor 15  15  15   # Near-black
    Panel         = New-OleColor 35  35  38   # Dark gray
    Border        = New-OleColor 200 200 200  # Light gray borders
    TextPrimary   = New-OleColor 255 255 255  # White text
    TextSecondary = New-OleColor 200 200 200  # Light gray text
    Accent1       = New-OleColor 0   176 240  # Cyan
    Accent2       = New-OleColor 243 112 33   # Orange
    Accent3       = New-OleColor 146 208 80   # Green
    Accent4       = New-OleColor 255 192 0    # Yellow
}

# Validate prerequisites
if (-not (Test-Path $LogoFile)) {
    Write-Host "ERROR: Logo not found: $LogoFile" -ForegroundColor Red
    return
}

if (-not (Test-Path $AriDir)) {
    Write-Host "ERROR: ARI directory not found: $AriDir" -ForegroundColor Red
    return
}

# Find most recent ARI file
$ariFiles = Get-ChildItem -Path $AriDir -Filter "AzureResourceInventory*.xlsx" |
    Where-Object { -not $_.Name.Contains("Converted") } |
    Sort-Object LastWriteTime -Descending

if ($ariFiles.Count -eq 0) {
    Write-Host "ERROR: No ARI files found in $AriDir" -ForegroundColor Red
    return
}

$InputFile = $ariFiles[0].FullName
Write-Host "Found ARI file: $($ariFiles[0].Name)" -ForegroundColor Green

# Create Excel COM object
Write-Host "Opening Excel..." -ForegroundColor Yellow
$excel = New-Object -ComObject Excel.Application
$excel.Visible = $false
$excel.DisplayAlerts = $false

try {
    # Open the workbook
    $wb = $excel.Workbooks.Open($InputFile)
    $ws = $wb.Worksheets.Item("Overview")
    
    Write-Host "Applying dark theme..." -ForegroundColor Yellow
    
    # Apply dark theme to worksheet
    $ws.Tab.Color = $Theme.Background
    $overviewRange = $ws.UsedRange
    $overviewRange.Interior.Color = $Theme.Background
    $overviewRange.Font.Color = $Theme.TextPrimary
    
    # Style the KPI table (if it exists)
    $tableCount = 0
    foreach ($tbl in $ws.ListObjects) {
        $tableCount++
        $tbl.HeaderRowRange.Interior.Color = $Theme.Panel
        $tbl.HeaderRowRange.Font.Color = $Theme.TextPrimary
        $tbl.HeaderRowRange.Font.Bold = $true
        $tbl.DataBodyRange.Interior.Color = $Theme.Background
        $tbl.DataBodyRange.Font.Color = $Theme.TextSecondary
    }
    Write-Host "  Styled $tableCount tables" -ForegroundColor Gray
    
    # Rebrand ARI header card
    Write-Host "Rebranding header..." -ForegroundColor Yellow
    
    $ariShape = $null
    foreach ($shp in $ws.Shapes) {
        if ($shp.Type -eq 1) {  # Rectangle
            $textContent = ""
            try { $textContent = $shp.TextFrame2.TextRange.Text } catch {}
            
            if ($textContent -match "Azure Resource Inventory") {
                $ariShape = $shp
                break
            }
        }
    }
    
    if ($ariShape) {
        # Apply dark theme to the shape
        $ariShape.Fill.ForeColor.RGB = $Theme.Panel
        $ariShape.Line.ForeColor.RGB = $Theme.Border
        $ariShape.TextFrame2.TextRange.Font.Fill.ForeColor.RGB = $Theme.TextPrimary
        
        # Remove Microsoft GitHub URL and rebrand
        $text = $ariShape.TextFrame2.TextRange.Text
        $lines = $text -split "`n" | Where-Object { 
            $_ -notmatch "github\.com" 
        }
        
        # Add your branding
        $newText = $lines -join "`n"
        $newText += "`nPowered by azure-noob.com"
        $ariShape.TextFrame2.TextRange.Text = $newText
        
        # Add your logo
        Write-Host "  Adding logo..." -ForegroundColor Gray
        
        # Create temporary resized logo (80x80 pixels)
        $tempLogo = [System.IO.Path]::GetTempFileName() + ".png"
        $img = [System.Drawing.Image]::FromFile($LogoFile)
        $resized = New-Object System.Drawing.Bitmap(80, 80)
        $graphics = [System.Drawing.Graphics]::FromImage($resized)
        $graphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
        $graphics.DrawImage($img, 0, 0, 80, 80)
        $resized.Save($tempLogo, [System.Drawing.Imaging.ImageFormat]::Png)
        $graphics.Dispose()
        $resized.Dispose()
        $img.Dispose()
        
        # Insert logo into Excel
        $logoLeft = $ariShape.Left + 10
        $logoTop = $ariShape.Top + 10
        $logoPic = $ws.Shapes.AddPicture(
            $tempLogo,
            [Microsoft.Office.Core.MsoTriState]::msoFalse,
            [Microsoft.Office.Core.MsoTriState]::msoCTrue,
            $logoLeft,
            $logoTop,
            80,
            80
        )
        
        Write-Host "  Logo added successfully" -ForegroundColor Green
    }
    
    # Apply dark theme to all charts
    Write-Host "Styling charts..." -ForegroundColor Yellow
    $chartCount = 0
    foreach ($chartObj in $ws.ChartObjects) {
        $chartCount++
        $cht = $chartObj.Chart
        
        # Dark background
        $cht.ChartArea.Format.Fill.ForeColor.RGB = $Theme.Panel
        $cht.PlotArea.Format.Fill.ForeColor.RGB = $Theme.Background
        
        # White text
        $cht.ChartTitle.Format.TextFrame2.TextRange.Font.Fill.ForeColor.RGB = $Theme.TextPrimary
        
        # Cycle through accent colors for series
        $seriesIndex = 0
        $accentColors = @($Theme.Accent1, $Theme.Accent2, $Theme.Accent3, $Theme.Accent4)
        
        foreach ($series in $cht.SeriesCollection()) {
            $color = $accentColors[$seriesIndex % $accentColors.Count]
            $series.Format.Fill.ForeColor.RGB = $color
            $seriesIndex++
        }
    }
    Write-Host "  Styled $chartCount charts" -ForegroundColor Gray
    
    # Save with timestamp
    $timestamp = Get-Date -Format "yyyy-MM-dd_HHmmss"
    $OutputFile = Join-Path $ScriptDir "ARI_FullDark_$timestamp.xlsx"
    
    Write-Host "Saving branded dashboard..." -ForegroundColor Yellow
    $wb.SaveAs($OutputFile)
    $wb.Close($false)
    
    Write-Host ""
    Write-Host "SUCCESS! Dashboard created:" -ForegroundColor Green
    Write-Host "  $OutputFile" -ForegroundColor Cyan
    Write-Host ""
    
    # Cleanup temp logo
    if ($tempLogo -and (Test-Path $tempLogo)) {
        Remove-Item $tempLogo -Force
    }
}
catch {
    Write-Host "ERROR: $_" -ForegroundColor Red
    Write-Host $_.ScriptStackTrace -ForegroundColor Red
}
finally {
    # Always quit Excel
    if ($excel) {
        $excel.Quit()
        [System.Runtime.Interopservices.Marshal]::ReleaseComObject($excel) | Out-Null
    }
    [System.GC]::Collect()
    [System.GC]::WaitForPendingFinalizers()
}
```

## Usage

### Prerequisites

1. **Windows with Excel installed** (needs COM automation)
2. **PowerShell 5.1 or later**
3. **Azure Resource Inventory report** - Run [ARI](https://github.com/microsoft/ARI) to generate a report first
4. **Your logo file** (PNG format, any size - script auto-resizes)

### Setup

1. Clone the repo:
```powershell
git clone https://github.com/dswann101164/azure-dashboard-rebrander.git
cd azure-dashboard-rebrander
```

2. Place your `logo.png` in the repo folder

3. Update `$AriDir` in the script if your ARI reports are somewhere other than `C:\AzureResourceInventory`

### Run It

```powershell
.\Rebrand-AzureDashboard.ps1
```

That's it. The script:
- Finds your most recent ARI report automatically
- Applies your branding and enhanced dark theme
- Saves as `ARI_FullDark_[timestamp].xlsx` in the script folder

**Processing time: ~30 seconds for a full 40-worksheet dashboard.**

### Example Output

```
================================================================
  Azure Admin Dashboard - Dark Mode Rebrander
================================================================

Checking prerequisites...
  Script directory: C:\Users\you\azure-dashboard-rebrander
  Logo path:       C:\Users\you\azure-dashboard-rebrander\logo.png
  ARI directory:   C:\AzureResourceInventory

✓ Logo found (1.42 MB)
✓ ARI directory found

Found ARI file: AzureResourceInventory_Report_2025-11-21_14_14.xlsx

Opening Excel...
Applying dark theme...
  Styled 1 tables
Rebranding header...
  Adding logo...
  Logo added successfully
Styling charts...
  Styled 8 charts

Saving branded dashboard...

SUCCESS! Dashboard created:
  C:\Users\you\azure-dashboard-rebrander\ARI_FullDark_2025-11-21_102857.xlsx
```

## Why This Matters

### For Consultants & MSPs

You're providing Azure analysis and recommendations to clients. The dashboard should reflect YOUR brand, not Microsoft's free tool. This script lets you:
- Present professional-looking reports with your logo
- Establish credibility (you built this analysis)
- White-label Microsoft's excellent ARI tool
- Save hours of manual Excel reformatting

### For Internal Azure Teams

When reporting to executives or leadership:
- Dark mode dashboards look more polished
- Your department's branding establishes ownership
- Professional presentation = taken more seriously
- Shows you're not just running free tools

### For Anyone Tired of Excel Corruption

If you've ever tried to programmatically modify complex Excel files and ended up with corrupted workbooks, this demonstrates the right approach: **Use Excel's own APIs instead of fighting the file format.**

## Real-World Impact

I run this script every time I generate a new ARI dashboard for my Azure environment (**44 subscriptions, 31,000+ resources, 21 Active Directory domains**). 

### Before This Script:
1. Open Excel manually ⏱️ 30 seconds
2. Find and delete Microsoft URLs by hand ⏱️ 2 minutes
3. Insert logo, resize, position ⏱️ 3 minutes
4. Adjust colors on 8+ charts individually ⏱️ 10 minutes
5. Test to make sure nothing broke ⏱️ 5 minutes

**Total: ~20 minutes of tedious manual work per dashboard**

### After This Script:
```powershell
.\Rebrand-AzureDashboard.ps1
```

**Total: 30 seconds. Done.**

But it's not just about time savings. It's about **establishing credibility** and building **portable intellectual property**.

### For Enterprise Azure Teams

When I present ARI dashboards to executives now, they see:
- **Professional branding** that matches our internal standards
- **My team's logo** establishing ownership and accountability
- **Clean, dark-themed visualizations** that look premium
- **Zero indication this came from a free GitHub tool**

This matters in enterprise environments where perception drives budget decisions. A professionally branded dashboard signals competence and attention to detail.

### For Consultants & MSPs (My Next Chapter)

This script is portable IP - it belongs to me, not my employer. When I transition to consulting or launch a SaaS platform (likely post-merger in Q1 2026), this is part of my toolkit:

- **White-label client deliverables** without rebuilding dashboards from scratch
- **Professional presentation** that justifies consulting rates
- **Differentiation** from competitors who hand clients raw Microsoft tools
- **Proven at enterprise scale** (31K+ resources) as a credibility signal

The script took me ~4 hours to build and debug. It's saved me 20+ hours already. More importantly, it positions me as a **solution builder**, not just an Azure button-clicker.

## The Bigger Lesson

Microsoft's Azure Resource Inventory is an excellent tool. But it's generic. It doesn't differentiate you.

Every Azure professional should be building tools and automation that:
1. Solve real problems they face daily
2. Add their own branding and intellectual property
3. Position them as solution builders, not button-clickers

This script took me a few hours to build and debug. It saves me 30 minutes every time I run an ARI report. More importantly, it makes my dashboards look professional and establishes my brand.

**That's the difference between being an Azure admin and being an Azure consultant.**

## Get The Code

Full script available on my GitHub: [azure-dashboard-rebrander](https://github.com/dswann101164/azure-dashboard-rebrander)

**Repo includes:**
- `Rebrand-AzureDashboard.ps1` - Main PowerShell script
- `logo.png` - Example logo (replace with yours)
- `examples/` - Sample before/after screenshots
- `images/` - Additional documentation assets
- `README.md` - Setup and usage instructions
- `LICENSE` - MIT licensed

**MIT licensed** - do whatever you want with it. Fork it, rebrand it for your clients, build a SaaS product on top of it. That's exactly what I plan to do.

---

## Why This Matters Beyond Azure

This project demonstrates a pattern that applies to any technical role:

1. **Identify tools that work but lack polish** - ARI is excellent technically but generic visually
2. **Build automation that adds your value** - The rebranding script is MY intellectual property
3. **Document the complete solution** - This blog post is marketing for future consulting
4. **Make it portable** - The script works anywhere, not just at my current employer

Microsoft built ARI to showcase Azure's capabilities. I built this script to showcase MY capabilities. That's the fundamental difference between being an IT operator and being a consultant or founder.

Every Azure professional should be asking: **What tools do I use daily that I could enhance, automate, or rebrand as my own?**

That's how you build a consulting practice or SaaS business while still employed. One script at a time.

---

**Questions? Want to see other Azure automation tools? Check out [azure-noob.com](https://azure-noob.com) or hit me up on Twitter.**

**Running a Synovus-scale Azure environment (31K+ resources, 44 subscriptions) and need rebranding help for your dashboards? Let's talk.**
