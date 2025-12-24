@echo off
REM Quick launcher for repository structure export
REM Usage: Just double-click or run: show-repo.bat

echo.
echo ========================================
echo  Azure Noob Blog - Structure Exporter
echo ========================================
echo.

cd /d "%~dp0"

echo Running Export-RepoStructure.ps1...
echo.

powershell -ExecutionPolicy Bypass -File ".\scripts\Export-RepoStructure.ps1"

echo.
echo ========================================
echo  Done! Check repo-structure.txt
echo ========================================
echo.
pause
