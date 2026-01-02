@echo off
echo ========================================
echo DEPLOYING FUNNEL OPTIMIZATION CHANGES
echo ========================================
echo.

cd /d C:\Users\dswann\Documents\GitHub\azure-noob-blog

echo [1/4] Freezing site...
.\.venv\Scripts\python.exe freeze.py

echo.
echo [2/4] Adding changes to git...
git add posts templates docs

echo.
echo [3/4] Committing changes...
git commit -m "feat: funnel optimization - new meta, lead magnets, $497 risk-focused copy"

echo.
echo [4/4] Pushing to GitHub...
git push

echo.
echo ========================================
echo DEPLOYMENT COMPLETE
echo ========================================
echo.
echo CHANGES DEPLOYED:
echo.
echo 1. OpenAI Pricing Page:
echo    - New meta title: "Azure OpenAI Real Costs 2026: PTU vs Pay-As-You-Go Calculator"
echo    - New meta description (Microsoft $150 vs $1,906 hook)
echo    - FREE lead magnet CTA added (email capture for lite calculator)
echo.
echo 2. Products Page:
echo    - New headline: "Decision Insurance: The $497 That Prevents $100K+ Mistakes"
echo    - Risk-focused features (not feature list)
echo    - 3 trust signals added:
echo      * Customer result: $7,344/month savings
echo      * Stronger guarantee: "Never had a refund. Ever."
echo      * Authority: $2.4M spend, Fortune 500 merger
echo.
echo 3. Expected Impact:
echo    - OpenAI page: Position 12 -^> 8-10 within 14 days
echo    - CTR: 0%% -^> 2-3%% = 135-202 clicks/month
echo    - Email captures: 15%% = 20-30/month
echo    - Revenue Month 1: $687-782
echo.
echo NEXT STEPS:
echo    1. Request re-indexing in Google Search Console
echo    2. Create lite Excel calculator lead magnet
echo    3. Monitor ConvertKit form submissions
echo    4. Watch for first $497 sale (Week 3-4)
echo.
echo GitHub Pages will rebuild in 2-5 minutes.
echo.
pause
