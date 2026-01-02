@echo off
echo ========================================
echo COPYING LITE CALCULATOR TO DOWNLOADS
echo ========================================
echo.

echo The lite calculator was created at:
echo   /tmp/Azure_OpenAI_Calculator_Lite.xlsx (in WSL/Linux)
echo.
echo You need to manually copy it to:
echo   C:\Users\dswann\Documents\GitHub\azure-noob-blog\static\downloads\
echo.
echo OPTION 1: Copy from WSL to Windows
echo   Run in PowerShell:
echo   wsl cp /tmp/Azure_OpenAI_Calculator_Lite.xlsx /mnt/c/Users/dswann/Documents/GitHub/azure-noob-blog/static/downloads/
echo.
echo OPTION 2: Use the file I can access
echo   The file already exists in /tmp/
echo   Open WSL and run:
echo   cp /tmp/Azure_OpenAI_Calculator_Lite.xlsx ~/azure-noob-blog/static/downloads/
echo.
echo OPTION 3: Download from this chat (if available)
echo   I'll create a new version you can download directly
echo.
pause
