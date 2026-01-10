@echo off


:: Check if venv exists
if not exist "venv\" (
    echo [ERROR] Virtual environment not found!
    echo Please run install.bat first to set up the environment.
    echo.
    pause
    exit /b 1
)

:: Check if Python script exists
if not exist "ducksnipe.py" (
    echo [ERROR] ducksnipe.py not found!
    echo Make sure the Python script is in the same folder as this batch file.
    echo.
    pause
    exit /b 1
)

:: Activate venv and run program
call venv\Scripts\activate.bat
python ducksnipe.py

:: Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo [ERROR] Program exited with an error.
    pause
)