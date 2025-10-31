# PowerShell Script to Add Visual Icons to Azure Icons Reference Excel
# Run this on your local Windows machine with: .\Add-Icons-To-Excel.ps1

Write-Host "🎨 Azure Icons Excel Image Embedder" -ForegroundColor Cyan
Write-Host "====================================`n" -ForegroundColor Cyan

# File paths
$inputFile = "C:\Users\dswann\Documents\GitHub\azure-noob-blog\static\Azure-Icons-Reference.xlsx"
$tempFolder = "$env:TEMP\azure-icons"
$outputFile = "C:\Users\dswann\Documents\GitHub\azure-noob-blog\static\Azure-Icons-Reference-with-Images.xlsx"

# Create temp folder for downloaded icons
if (-not (Test-Path $tempFolder)) {
    New-Item -Path $tempFolder -ItemType Directory | Out-Null
}

Write-Host "📂 Input file: $inputFile"
Write-Host "📁 Temp folder: $tempFolder"
Write-Host "💾 Output file: $outputFile`n"

# Load Excel COM object
Write-Host "📊 Loading Excel..." -ForegroundColor Yellow
$excel = New-Object -ComObject Excel.Application
$excel.Visible = $false
$excel.DisplayAlerts = $false

try {
    # Open the workbook
    $workbook = $excel.Workbooks.Open($inputFile)
    $worksheet = $workbook.Worksheets.Item(1)
    
    # Insert new column A for icons
    Write-Host "➕ Inserting Icon column..." -ForegroundColor Yellow
    $worksheet.Columns.Item(1).Insert() | Out-Null
    
    # Set header for icon column
    $worksheet.Cells.Item(1, 1).Value2 = "Icon"
    $worksheet.Cells.Item(1, 1).Font.Bold = $true
    $worksheet.Cells.Item(1, 1).Interior.Color = 0xD47800  # Azure blue
    $worksheet.Cells.Item(1, 1).Font.Color = 0xFFFFFF  # White text
    
    # Set column width for icons
    $worksheet.Columns.Item(1).ColumnWidth = 10
    
    # Get total rows
    $lastRow = $worksheet.UsedRange.Rows.Count
    Write-Host "📋 Found $($lastRow - 1) icons to process`n" -ForegroundColor Yellow
    
    # Process each row (starting from row 2, after header)
    $successCount = 0
    $failCount = 0
    
    for ($row = 2; $row -le $lastRow; $row++) {
        # Icon URL is now in column E (was D, but we inserted a column)
        $iconUrl = $worksheet.Cells.Item($row, 5).Value2
        $iconName = $worksheet.Cells.Item($row, 2).Value2
        
        if ($iconUrl) {
            try {
                # Download icon
                $iconFileName = Split-Path $iconUrl -Leaf
                $localIconPath = Join-Path $tempFolder $iconFileName
                
                # Download if not already cached
                if (-not (Test-Path $localIconPath)) {
                    Invoke-WebRequest -Uri $iconUrl -OutFile $localIconPath -TimeoutSec 5 -ErrorAction Stop
                }
                
                # Insert image into Excel
                $range = $worksheet.Cells.Item($row, 1)
                $shape = $worksheet.Shapes.AddPicture(
                    $localIconPath,
                    $false,  # LinkToFile
                    $true,   # SaveWithDocument
                    $range.Left + 5,
                    $range.Top + 5,
                    40,      # Width
                    40       # Height
                )
                
                # Set row height
                $worksheet.Rows.Item($row).RowHeight = 50
                
                $successCount++
                
                if ($successCount % 10 -eq 0) {
                    Write-Host "   ✓ Processed $successCount icons..." -ForegroundColor Green
                }
                
            } catch {
                Write-Host "   ⚠️  Failed: $iconName - $($_.Exception.Message)" -ForegroundColor Red
                $failCount++
            }
        }
    }
    
    Write-Host "`n✅ Complete!" -ForegroundColor Green
    Write-Host "   Successfully embedded: $successCount icons" -ForegroundColor Green
    Write-Host "   Failed: $failCount icons" -ForegroundColor Yellow
    
    # Save the new workbook
    Write-Host "`n💾 Saving workbook..." -ForegroundColor Yellow
    $workbook.SaveAs($outputFile)
    $workbook.Close($false)
    
    Write-Host "✅ Done! New file created:" -ForegroundColor Green
    Write-Host "   $outputFile" -ForegroundColor Cyan
    
} catch {
    Write-Host "`n❌ Error: $($_.Exception.Message)" -ForegroundColor Red
} finally {
    $excel.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($excel) | Out-Null
    
    # Cleanup temp folder
    Write-Host "`n🧹 Cleaning up temp files..." -ForegroundColor Yellow
    Remove-Item $tempFolder -Recurse -Force -ErrorAction SilentlyContinue
}

Write-Host "`n✨ All done! Open the new file to see the icons." -ForegroundColor Cyan
