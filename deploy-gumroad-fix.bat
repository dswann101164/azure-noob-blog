@echo off
echo ========================================
echo DEPLOYING GUMROAD URL FIX
echo ========================================
echo.

cd /d C:\Users\dswann\Documents\GitHub\azure-noob-blog

echo [1/3] Freezing site...
.\.venv\Scripts\python.exe freeze.py

echo.
echo [2/3] Adding changes to git...
git add posts templates docs

echo.
echo [3/3] Committing and pushing...
git commit -m "fix: update Gumroad URLs from azurenoob to davidnoob"
git push

echo.
echo ========================================
echo DEPLOYMENT COMPLETE
echo ========================================
echo.
echo Updated URLs:
echo   - Azure OpenAI ROI Toolkit: davidnoob.gumroad.com/l/azure-openai-roi-toolkit
echo   - Bundle (footer): davidnoob.gumroad.com/l/azure-ops-bundle
echo.
echo GitHub Pages will rebuild in 2-5 minutes.
echo.
pause
