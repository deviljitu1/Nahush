# LinkedIn AI Post Generator - PowerShell Startup Script

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   LinkedIn AI Post Generator" -ForegroundColor Cyan
Write-Host "   Web Server Startup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.7 or higher" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if requirements are installed
Write-Host "Checking dependencies..." -ForegroundColor Yellow
try {
    pip show requests | Out-Null
    Write-Host "✅ Dependencies are installed" -ForegroundColor Green
} catch {
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ ERROR: Failed to install dependencies" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   API Key Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if API key is already set
if ($env:OPEN_ROUTER) {
    Write-Host "✅ OpenRouter API key is already set" -ForegroundColor Green
    Write-Host "Current key: $($env:OPEN_ROUTER.Substring(0, [Math]::Min(10, $env:OPEN_ROUTER.Length)))..." -ForegroundColor Gray
} else {
    Write-Host "⚠️  OpenRouter API key not found" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Please enter your OpenRouter API key:" -ForegroundColor White
    Write-Host "(Get it from: https://openrouter.ai)" -ForegroundColor Gray
    Write-Host ""
    
    $apiKey = Read-Host "Enter your API key"
    
    if ($apiKey.Length -eq 0) {
        Write-Host "❌ ERROR: No API key provided" -ForegroundColor Red
        Write-Host "Please get your API key from https://openrouter.ai" -ForegroundColor Yellow
        Read-Host "Press Enter to exit"
        exit 1
    }
    
    # Set environment variable
    $env:OPEN_ROUTER = $apiKey
    Write-Host "✅ API key set successfully" -ForegroundColor Green
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Starting Server" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "🚀 Starting LinkedIn AI Post Generator Server..." -ForegroundColor Green
Write-Host "📁 Server will run on: http://localhost:8000" -ForegroundColor White
Write-Host "🌐 Open your browser and go to: http://localhost:8000" -ForegroundColor White
Write-Host "⏹️  Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Start the server
try {
    python server.py
} catch {
    Write-Host "❌ ERROR: Failed to start server" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
}

Read-Host "Press Enter to exit" 