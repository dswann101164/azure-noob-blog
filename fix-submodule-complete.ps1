# Complete submodule removal fix
cd C:\Users\dswann\Documents\GitHub\azure-noob-blog

Write-Host "Removing temp-skills submodule completely..." -ForegroundColor Yellow

# Step 1: Remove from index
git rm --cached temp-skills -f 2>$null

# Step 2: Remove from .gitmodules
if (Test-Path .gitmodules) {
    Remove-Item .gitmodules -Force
}

# Step 3: Remove from .git/config
git config --remove-section submodule.temp-skills 2>$null

# Step 4: Remove from .git/modules
if (Test-Path .git\modules\temp-skills) {
    Remove-Item -Recurse -Force .git\modules\temp-skills
}

# Step 5: Remove the directory itself if it exists
if (Test-Path temp-skills) {
    Remove-Item -Recurse -Force temp-skills
}

# Step 6: Stage all changes
git add -A

# Step 7: Commit
git commit -m "Complete removal of temp-skills submodule" --allow-empty

# Step 8: Push
git push origin main

Write-Host "✅ Done! Check GitHub Actions in 30 seconds..." -ForegroundColor Green
