@echo off
echo ========================================
echo REMOVING BUNDLE PROMOTION TEMPORARILY
echo ========================================
echo.

cd /d C:\Users\dswann\Documents\GitHub\azure-noob-blog

echo [1/3] Freezing site...
.\.venv\Scripts\python.exe freeze.py

echo.
echo [2/3] Adding changes to git...
git add templates docs

echo.
echo [3/3] Committing and pushing...
git commit -m "fix: temporarily hide bundle promotion until Gumroad product created"
git push

echo.
echo ========================================
echo DEPLOYMENT COMPLETE
echo ========================================
echo.
echo Changes:
echo   - Bundle section commented out in base.html footer
echo   - Will be hidden on all pages site-wide
echo   - Can re-enable later when Gumroad product is ready
echo.
echo GitHub Pages will rebuild in 2-5 minutes.
echo.
pause
