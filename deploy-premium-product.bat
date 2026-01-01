@echo off
echo ========================================
echo DEPLOYING PREMIUM PRODUCT TO PRODUCTS PAGE
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
git commit -m "feat: add $497 ROI Toolkit to products page as premium product"
git push

echo.
echo ========================================
echo DEPLOYMENT COMPLETE
echo ========================================
echo.
echo Added to products page:
echo   - Azure OpenAI ROI Toolkit ($497) at TOP
echo   - Purple gradient "PREMIUM" badge
echo   - Links to: davidnoob.gumroad.com/l/azure-openai-roi-toolkit
echo.
echo NOTE: You need to create product image:
echo   /static/images/products/openai-roi-toolkit.png
echo.
echo GitHub Pages will rebuild in 2-5 minutes.
echo.
pause
