# Fix the temp-skills submodule issue
cd C:\Users\dswann\Documents\GitHub\azure-noob-blog

# Remove the submodule from git cache if it exists
git rm --cached temp-skills 2>$null

# Remove .gitmodules if it exists
if (Test-Path .gitmodules) {
    Remove-Item .gitmodules -Force
}

# Remove submodule config from .git/config
git config --remove-section submodule.temp-skills 2>$null

# Remove the submodule directory from .git
if (Test-Path .git\modules\temp-skills) {
    Remove-Item -Recurse -Force .git\modules\temp-skills
}

# Stage and commit the fix
git add .gitmodules
git commit -m "Remove broken temp-skills submodule"

# Push to trigger new build
git push

Write-Host "✅ Submodule removed, pushing fix..."
