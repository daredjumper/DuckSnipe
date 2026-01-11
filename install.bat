@echo off
setlocal enabledelayedexpansion

echo ========================================
echo    DuckSnipe v1.0.9 - Auto Installer
echo ========================================
echo.

:: Check if Python is installed
echo [1/5] Checking for Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH!
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

:: Display Python version
for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo [OK] Found !PYTHON_VERSION!
echo.

:: Check if venv already exists
if exist "venv\" (
    echo [WARNING] Virtual environment already exists.
    set /p RECREATE="Do you want to recreate it? (y/n): "
    if /i "!RECREATE!"=="y" (
        echo [2/5] Removing old virtual environment...
        rmdir /s /q venv
        echo [OK] Old environment removed.
        echo.
    ) else (
        echo [SKIP] Using existing virtual environment.
        echo.
        goto :activate_venv
    )
)

:: Create virtual environment
echo [2/5] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo [ERROR] Failed to create virtual environment!
    echo Try running: python -m pip install --upgrade pip
    pause
    exit /b 1
)
echo [OK] Virtual environment created successfully.
echo.

:activate_venv
:: Activate virtual environment
echo [3/5] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment!
    pause
    exit /b 1
)
echo [OK] Virtual environment activated.
echo.

:: Upgrade pip
echo [4/5] Upgrading pip to latest version...
python -m pip install --upgrade pip --quiet
if errorlevel 1 (
    echo [WARNING] Failed to upgrade pip, continuing anyway...
) else (
    echo [OK] Pip upgraded successfully.
)
echo.

:: Install dependencies
echo [5/5] Installing required dependencies...
echo.

:: Install aiohttp
echo Installing: aiohttp (async HTTP client)
python -m pip install aiohttp --quiet
if errorlevel 1 (
    echo [ERROR] Failed to install aiohttp!
    pause
    exit /b 1
)
echo [OK] aiohttp installed.

:: Install colorama
echo Installing: colorama (colored terminal output)
python -m pip install colorama --quiet
if errorlevel 1 (
    echo [ERROR] Failed to install colorama!
    pause
    exit /b 1
)
echo [OK] colorama installed.

echo.
echo ========================================
echo    Installation Complete!
echo ========================================
echo.
echo Virtual environment created: venv\
echo.
echo Dependencies installed:
echo   - aiohttp  (async HTTP requests)
echo   - colorama (colored terminal output)
echo.
echo To run DuckSnipe:
echo   1. Run: start.bat
echo   OR
echo   2. Manually activate venv: venv\Scripts\activate.bat
echo   3. Then run: python ducksnipe.py
echo.
echo ========================================
pause