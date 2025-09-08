# init_push.ps1
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

Write-Host "=== Azure Noob Blog: Initial Git push script ===`n"

# 1. Create .gitignore if missing
$gitignorePath = ".gitignore"
if (-Not (Test-Path $gitignorePath)) {
@"
# Python
__pycache__/
*.pyc
*.pyo
*.pyd
*.db

# Virtual env
.venv/
env/
venv/

# Build artifacts
build/
dist/
*.egg-info/

# IDE/editor junk
.vscode/
.idea/
*.swp
.DS_Store
Thumbs.db

# Logs
*.log

# OS
desktop.ini
"@ | Out-File -Encoding UTF8 $gitignorePath
    Write-Host "✅ Created .gitignore"
} else {
    Write-Host "ℹ️ .gitignore already exists, skipping..."
}

# 2. Untrack .venv if it was staged
git rm -r --cached .venv 2>$null | Out-Null

# 3. Stage and commit everything
git add .
try {
    git commit -m "Initial commit with Flask blog and deploy workflow"
} catch {
    Write-Host "ℹ️ Nothing to commit (maybe already committed)"
}

# 4. Make sure branch is main
git branch -M main

# 5. Add remote (ignore if already exists)
try {
    git remote add origin https://github.com/dswann101164/azure-noob-blog.git
    Write-Host "✅ Remote added"
} catch {
    Write-Host "ℹ️ Remote already set, skipping..."
}

# 6. Push to GitHub
git push -u origin main

Write-Host "`n🎉 Done! Check GitHub → Actions tab for your deploy workflow."
