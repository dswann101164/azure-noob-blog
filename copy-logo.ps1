# Copy logo to digital products directory
Copy-Item -Path "static\images\logo.png" -Destination "digital-products\logo.png" -Force
Write-Host "✓ Logo copied to digital-products/" -ForegroundColor Green

# List files
Get-ChildItem digital-products\ | Format-Table Name, Length, LastWriteTime -AutoSize
