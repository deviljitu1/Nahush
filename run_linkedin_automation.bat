@echo off
echo ========================================
echo    LinkedIn Automation Tool
echo    with AI Content Generation
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7 or higher
    pause
    exit /b 1
)

REM Check if requirements are installed
echo Checking dependencies...
pip show linkedin-api >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

echo.
echo Choose an option:
echo 1. Run GUI Interface (Recommended)
echo 2. Run Command Line Interface
echo 3. Test AI Content Generation
echo 4. Run AI Examples
echo 5. Exit
echo.
set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" (
    echo Starting GUI Interface...
    python linkedin_gui.py
) else if "%choice%"=="2" (
    echo Starting Command Line Interface...
    python linkedin_automation.py
) else if "%choice%"=="3" (
    echo Testing AI Content Generation...
    python ai_content_generator.py
) else if "%choice%"=="4" (
    echo Running AI Examples...
    python ai_example_usage.py
) else if "%choice%"=="5" (
    echo Goodbye!
    exit /b 0
) else (
    echo Invalid choice. Please run the script again.
)

pause 