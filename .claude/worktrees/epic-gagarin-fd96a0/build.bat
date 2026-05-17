@echo off
echo ========================================
echo  Sandy Roofing Pros - Build Script
echo ========================================
echo.

cd /d "%~dp0"

echo [1/2] Running npm install...
call npm install
if %errorlevel% neq 0 (
    echo ERROR: npm install failed.
    pause
    exit /b 1
)

echo.
echo [2/2] Running npm run build...
call npm run build
if %errorlevel% neq 0 (
    echo ERROR: npm run build failed.
    pause
    exit /b 1
)

echo.
echo ========================================
echo  BUILD COMPLETE - dist/ folder is ready
echo ========================================
echo.
pause
