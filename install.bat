@echo off
setlocal enabledelayedexpansion
echo ========================================
echo    DuckSnipe v1.0.9 - Auto Installer
echo ========================================
echo.

:: Check if Python is installed
echo [1/7] Checking for Python installation...
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
        echo [2/7] Removing old virtual environment...
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
echo [2/7] Creating virtual environment...
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
echo [3/7] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment!
    pause
    exit /b 1
)
echo [OK] Virtual environment activated.
echo.

:: Upgrade pip
echo [4/7] Upgrading pip to latest version...
python -m pip install --upgrade pip --quiet
if errorlevel 1 (
    echo [WARNING] Failed to upgrade pip, continuing anyway...
) else (
    echo [OK] Pip upgraded successfully.
)
echo.

:: Install dependencies
echo [5/7] Installing required dependencies...
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

:: Install Flask for web UI
echo Installing: Flask (web interface framework)
python -m pip install Flask --quiet
if errorlevel 1 (
    echo [ERROR] Failed to install Flask!
    pause
    exit /b 1
)
echo [OK] Flask installed.

echo.

:: Create templates directory
echo [6/7] Setting up web interface...
if not exist "templates\" (
    echo Creating templates directory...
    mkdir templates
    echo [OK] Templates directory created.
) else (
    echo [OK] Templates directory already exists.
)

:: Check if index.html exists
if not exist "templates\index.html" (
    echo [WARNING] templates\index.html not found!
    echo Please make sure to copy index.html to the templates folder.
    echo Web interface will not work without this file.
) else (
    echo [OK] Web interface template found.
)
echo.

:: Verify all files
echo [7/7] Verifying installation...
echo.

set MISSING_FILES=0

if not exist "ducksnipe.py" (
    echo [MISSING] ducksnipe.py
    set MISSING_FILES=1
)

if not exist "config.py" (
    echo [MISSING] config.py
    set MISSING_FILES=1
)

if not exist "api.py" (
    echo [MISSING] api.py
    set MISSING_FILES=1
)

if not exist "commands.py" (
    echo [MISSING] commands.py
    set MISSING_FILES=1
)

if not exist "utils.py" (
    echo [MISSING] utils.py
    set MISSING_FILES=1
)

if not exist "web_server.py" (
    echo [MISSING] web_server.py (Web UI will not work)
    set MISSING_FILES=1
)

if not exist "templates\index.html" (
    echo [MISSING] templates\index.html (Web UI will not work)
    set MISSING_FILES=1
)

if !MISSING_FILES!==1 (
    echo.
    echo [WARNING] Some files are missing! Please check above.
    echo DuckSnipe may not work correctly.
    echo.
) else (
    echo [OK] All core files present.
    echo.
)

echo ========================================
echo    Installation Complete!
echo ========================================
echo.
echo Virtual environment: venv\
echo.
echo Dependencies installed:
echo   - aiohttp  (async HTTP requests)
echo   - colorama (colored terminal output)
echo   - Flask    (web interface)
echo.
echo Available modes:
echo   1. CLI Mode  : Run start.bat or python ducksnipe.py
echo   2. Web UI    : Type 'web' in CLI to start web interface
echo                  Then open: http://localhost:8080
echo.
echo Quick Start:
echo   Run: start.bat
echo.
echo Manual activation:
echo   venv\Scripts\activate.bat
echo   python ducksnipe.py
echo.
echo ========================================

pause
