@echo off
REM Finance Pro 2.0 - Android APK Builder for Windows
REM This script builds the Android APK

echo.
echo ================================
echo Finance Pro 2.0 - APK Builder
echo ================================
echo.

REM Check if buildozer.spec exists
if not exist buildozer.spec (
    echo ERROR: buildozer.spec not found!
    echo Make sure you're in the Finance Pro 2.0 directory.
    pause
    exit /b 1
)

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python 3.8+ first.
    pause
    exit /b 1
)

echo [1/5] Checking buildozer installation...
python -m buildozer --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Buildozer not installed!
    echo Run: pip install buildozer
    pause
    exit /b 1
)

echo [2/5] Checking Android SDK setup...
if not defined ANDROID_SDK_ROOT (
    echo WARNING: ANDROID_SDK_ROOT not set!
    echo You may need to install Android SDK first.
    echo See ANDROID_SETUP.md for instructions.
)

echo [3/5] Cleaning previous builds...
python -m buildozer android clean

echo [4/5] Building Android APK...
echo This may take 5-15 minutes on first build...
python -m buildozer android debug

if errorlevel 1 (
    echo.
    echo ERROR: Build failed!
    echo Check the error messages above.
    pause
    exit /b 1
)

echo [5/5] Build complete!
echo.
echo APK Location: bin\financepro-2.0.0-debug.apk
echo.
echo Installation instructions:
echo 1. Enable Developer Mode on your Android phone
echo 2. Connect phone via USB
echo 3. Run: adb install bin\financepro-2.0.0-debug.apk
echo.
pause
