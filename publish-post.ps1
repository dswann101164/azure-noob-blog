# Publish new blog post - PowerShell 7 Chocolatey fix

Write-Host "`n=== Publishing New Blog Post ===" -ForegroundColor Cyan

# Step 1: Unstage everything first (clean slate)
Write-Host "`n[1/5] Unstaging all files..." -ForegroundColor Yellow
git reset

# Step 2: Stage only the new post and hero image
Write-Host "`n[2/5] Staging new post + hero image..." -ForegroundColor Yellow
git add posts/2026-01-22-azure-marketplace-vms-broken-winget-chocolatey-fix.md
git add static/images/hero/azure-marketplace-vms-broken-winget-chocolatey-fix.png

# Show what's staged
Write-Host "`n[3/5] Files staged:" -ForegroundColor Green
git status --short

# Step 3: Freeze the site
Write-Host "`n[4/5] Freezing site (generating /docs)..." -ForegroundColor Yellow
python freeze.py

# Step 4: Stage the generated docs
Write-Host "`n[5/5] Staging generated docs..." -ForegroundColor Yellow
git add docs

# Show final status
Write-Host "`nFinal staged files:" -ForegroundColor Green
git status --short

# Commit
Write-Host "`n=== Ready to Commit ===" -ForegroundColor Cyan
$commitMessage = @"
feat(blog): add PowerShell 7 bootstrap problem on Azure VMs - Chocolatey fix

- New post: Azure Marketplace VMs ship with broken winget
- Can't install PowerShell 7 on fresh VMs (dependency loop)
- Solution: Use Chocolatey automation script
- Includes GitHub repo link to azure-admin-workstation-setup
- Hero image showing problem → solution workflow
"@

git commit -m $commitMessage

# Push
Write-Host "`n=== Pushing to GitHub ===" -ForegroundColor Cyan
git push

Write-Host "`n✅ Post published!`n" -ForegroundColor Green
Write-Host "Next: Paste ChatGPT hero prompt to generate distribution content" -ForegroundColor Gray
