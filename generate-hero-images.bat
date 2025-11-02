@echo off
echo ====================================
echo Terraform CI/CD Hero Image Generator
echo ====================================
echo.

echo Step 1: Installing Pillow (if needed)...
pip install Pillow --quiet
if %errorlevel% neq 0 (
    echo ERROR: Failed to install Pillow
    echo Please run: pip install Pillow
    pause
    exit /b 1
)
echo ✓ Pillow installed
echo.

echo Step 2: Generating hero images...
python create_hero_images.py
if %errorlevel% neq 0 (
    echo ERROR: Failed to generate images
    echo.
    echo Troubleshooting:
    echo - Make sure Python is installed
    echo - Try running: python --version
    echo - Check create_hero_images.py exists
    pause
    exit /b 1
)
echo.

echo Step 3: Verifying images were created...
if exist "static\images\hero\terraform-devops-series-index.png" (
    echo ✓ Images created successfully!
    echo.
    echo Location: static\images\hero\
    echo.
    dir /B static\images\hero\terraform-devops-*.png
    echo.
    echo ====================================
    echo SUCCESS! All hero images created.
    echo ====================================
    echo.
    echo Next steps:
    echo 1. Review images in static\images\hero\
    echo 2. Run: python freeze.py
    echo 3. Commit: git add static posts docs
    echo 4. Push: git push origin main
) else (
    echo ERROR: Images not found
    echo Check if script ran successfully
)
echo.
pause
