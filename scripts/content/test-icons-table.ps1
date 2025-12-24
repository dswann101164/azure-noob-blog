# Test and Publish Azure Icons Reference
# Quick helper script for validating the icons table

Write-Host "`n🎨 Azure Icons Reference - Test & Publish Helper`n" -ForegroundColor Cyan

# Check if files exist
$htmlFile = ".\static\azure-icons-table.html"
$excelFile = ".\static\files\Azure-Icons-Reference.xlsx"
$blogPost = ".\posts\2025-10-29-azure-icons-reference.md"

Write-Host "Checking files..." -ForegroundColor Yellow

if (Test-Path $htmlFile) {
    $htmlSize = (Get-Item $htmlFile).Length / 1KB
    Write-Host "✅ HTML Table: $([math]::Round($htmlSize, 2)) KB" -ForegroundColor Green
} else {
    Write-Host "❌ HTML Table missing!" -ForegroundColor Red
}

if (Test-Path $excelFile) {
    $excelSize = (Get-Item $excelFile).Length / 1KB
    Write-Host "✅ Excel File: $([math]::Round($excelSize, 2)) KB" -ForegroundColor Green
} else {
    Write-Host "❌ Excel File missing!" -ForegroundColor Red
}

if (Test-Path $blogPost) {
    Write-Host "✅ Blog Post exists" -ForegroundColor Green
} else {
    Write-Host "❌ Blog Post missing!" -ForegroundColor Red
}

Write-Host "`n📝 What would you like to do?`n" -ForegroundColor Cyan
Write-Host "1. Test locally (start Flask server)"
Write-Host "2. Open HTML table in browser"
Write-Host "3. Open Excel file"
Write-Host "4. Freeze site for publishing"
Write-Host "5. Full publish (freeze + git commit + push)"
Write-Host "6. Exit`n"

$choice = Read-Host "Enter choice (1-6)"

switch ($choice) {
    "1" {
        Write-Host "`n🚀 Starting Flask server...`n" -ForegroundColor Green
        Write-Host "Visit these URLs to test:" -ForegroundColor Yellow
        Write-Host "  • HTML Table: http://127.0.0.1:5000/static/azure-icons-table.html"
        Write-Host "  • Blog Post:  http://127.0.0.1:5000/blog/azure-icons-reference"
        Write-Host "`nPress Ctrl+C to stop the server`n"
        flask run
    }
    "2" {
        Write-Host "`n🌐 Opening HTML table in browser..." -ForegroundColor Green
        Start-Process $htmlFile
    }
    "3" {
        Write-Host "`n📊 Opening Excel file..." -ForegroundColor Green
        Start-Process $excelFile
    }
    "4" {
        Write-Host "`n❄️  Freezing site..." -ForegroundColor Green
        python freeze.py
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Site frozen successfully!" -ForegroundColor Green
            Write-Host "`nNext steps:" -ForegroundColor Yellow
            Write-Host "  git add static docs"
            Write-Host "  git commit -m 'Add Azure Icons Reference table'"
            Write-Host "  git push"
        } else {
            Write-Host "❌ Freeze failed!" -ForegroundColor Red
        }
    }
    "5" {
        Write-Host "`n🚀 Full publish sequence...`n" -ForegroundColor Green
        
        # Freeze
        Write-Host "1/3 Freezing site..." -ForegroundColor Yellow
        python freeze.py
        if ($LASTEXITCODE -ne 0) {
            Write-Host "❌ Freeze failed! Aborting." -ForegroundColor Red
            exit
        }
        
        # Git add
        Write-Host "2/3 Adding files to git..." -ForegroundColor Yellow
        git add static/azure-icons-table.html
        git add static/files/Azure-Icons-Reference.xlsx
        git add docs/
        
        # Git commit
        Write-Host "3/3 Committing..." -ForegroundColor Yellow
        git commit -m "Add Azure Icons Reference interactive table and Excel download"
        
        if ($LASTEXITCODE -eq 0) {
            $push = Read-Host "`nCommitted! Push to GitHub? (y/n)"
            if ($push -eq "y") {
                git push
                Write-Host "`n✅ Published successfully!" -ForegroundColor Green
                Write-Host "`nLive URLs:" -ForegroundColor Cyan
                Write-Host "  • https://azure-noob.com/static/azure-icons-table.html"
                Write-Host "  • https://azure-noob.com/static/files/Azure-Icons-Reference.xlsx"
                Write-Host "  • https://azure-noob.com/blog/azure-icons-reference"
            } else {
                Write-Host "`nCommitted locally. Push when ready with: git push" -ForegroundColor Yellow
            }
        } else {
            Write-Host "❌ Commit failed!" -ForegroundColor Red
        }
    }
    "6" {
        Write-Host "`nGoodbye! 👋`n" -ForegroundColor Cyan
        exit
    }
    default {
        Write-Host "`n❌ Invalid choice!" -ForegroundColor Red
    }
}

Write-Host ""
