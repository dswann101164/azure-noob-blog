@echo off
cd C:\Users\dswann\Documents\GitHub\azure-noob-blog

echo Adding docs...
git add docs/

echo Committing...
git commit -m "Update frozen site with Terraform CI/CD series"

echo Pushing to GitHub...
git push origin main

echo.
echo Done! Wait 1-2 minutes, then check:
echo https://azure-noob.com/blog/terraform-azure-devops-cicd-series-index/
echo.
pause
