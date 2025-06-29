@echo off
echo ========================================
echo    LinkedIn AI Post Generator
echo    Web Server Startup
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
pip show requests >nul 2>&1
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
echo ========================================
echo    API Key Setup
echo ========================================
echo.

REM Check if API key is already set
if defined OPEN_ROUTER (
    echo ✅ OpenRouter API key is already set
    echo Current key: %OPEN_ROUTER:~0,10%...
) else (
    echo ⚠️  OpenRouter API key not found
    echo.
    echo Please enter your OpenRouter API key:
    echo (Get it from: https://openrouter.ai)
    echo.
    set /p api_key="Enter your API key: "
    
    if "%api_key%"=="" (
        echo ERROR: No API key provided
        echo Please get your API key from https://openrouter.ai
        pause
        exit /b 1
    )
    
    REM Set the environment variable
    set OPEN_ROUTER=%api_key%
    echo ✅ API key set successfully
)

echo.
echo ========================================
echo    Starting Server
echo ========================================
echo.
echo 🚀 Starting LinkedIn AI Post Generator Server...
echo 📁 Server will run on: http://localhost:8000
echo 🌐 Open your browser and go to: http://localhost:8000
echo ⏹️  Press Ctrl+C to stop the server
echo.

REM Start the server
python server.py

pause 