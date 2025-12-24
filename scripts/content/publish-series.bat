@echo off
echo ====================================
echo Publishing Terraform CI/CD Series
echo ====================================
echo.

cd C:\Users\dswann\Documents\GitHub\azure-noob-blog

echo Step 1: Checking git status...
git status
echo.

echo Step 2: Adding all changes...
git add posts docs HERO_IMAGES_INSTRUCTIONS.md create_hero_images.py generate-hero-images.bat SERIES_COMPLETE.md HERO_IMAGES_NEEDED.md
echo ✓ Files staged
echo.

echo Step 3: Committing changes...
git commit -m "Publish Terraform + Azure DevOps CI/CD complete series (7 posts)"
if %errorlevel% neq 0 (
    echo Note: No changes to commit or commit failed
)
echo.

echo Step 4: Pushing to GitHub...
git push origin main
if %errorlevel% neq 0 (
    echo ERROR: Push failed
    echo Check your GitHub credentials and try again
    pause
    exit /b 1
)
echo.

echo ====================================
echo ✓ SUCCESS! Series published!
echo ====================================
echo.
echo Your blog should update in 1-2 minutes at:
echo https://azure-noob.com
echo.
echo Verify deployment:
echo https://azure-noob.com/blog/terraform-azure-devops-cicd-series-index/
echo.
pause
