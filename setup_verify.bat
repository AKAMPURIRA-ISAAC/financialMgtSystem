@echo off
REM Finance Pro 2.0 - Setup & Verification Script

echo.
echo =====================================================
echo   Finance Pro 2.0 - Setup & Verification
echo =====================================================
echo.

REM Check Python
echo [1/5] Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.8+
    exit /b 1
)

REM Check dependencies
echo.
echo [2/5] Checking dependencies...
pip list | findstr /i "fastapi kivy pandas scikit-learn" >nul
if errorlevel 1 (
    echo.
    echo WARNING: Some dependencies might be missing.
    echo Run: pip install -r requirements.txt
)

REM Check files
echo.
echo [3/5] Checking project files...
set missing=0
for %%f in (main.py api_server.py enhanced_database.py ml_engine.py analytics.py integrations.py config.py requirements.txt) do (
    if not exist %%f (
        echo ERROR: Missing %%f
        set missing=1
    ) else (
        echo OK: %%f
    )
)

if %missing%==1 (
    echo ERROR: Some required files are missing
    exit /b 1
)

REM Test database
echo.
echo [4/5] Testing database connection...
python -c "from enhanced_database import EnhancedDatabase; db = EnhancedDatabase(); print('OK: Database initialized')"
if errorlevel 1 (
    echo ERROR: Database initialization failed
    exit /b 1
)

REM Test ML Engine
echo.
echo [5/5] Testing ML engine...
python -c "from ml_engine import MLEngine; ml = MLEngine(); print('OK: ML Engine loaded')"
if errorlevel 1 (
    echo ERROR: ML Engine failed to load
    exit /b 1
)

echo.
echo =====================================================
echo   ✓ All checks passed!
echo =====================================================
echo.
echo Ready to run:
echo   - Desktop App:  python main.py
echo   - API Server:   python api_server.py
echo.
echo For more info, see README.md or QUICKSTART.md
echo.
