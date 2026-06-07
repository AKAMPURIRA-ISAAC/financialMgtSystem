# Finance Pro 2.0 - Android APK Builder (PowerShell)
# Usage: powershell -ExecutionPolicy Bypass -File build_android.ps1

Write-Host "================================" -ForegroundColor Cyan
Write-Host "Finance Pro 2.0 - APK Builder" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
Write-Host "[1/4] Checking Python..." -ForegroundColor Yellow
python --version
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Python not found!" -ForegroundColor Red
    exit 1
}

# Check buildozer
Write-Host "[2/4] Checking buildozer..." -ForegroundColor Yellow
python -m buildozer --version
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Buildozer not installed!" -ForegroundColor Red
    Write-Host "Run: pip install buildozer" -ForegroundColor Yellow
    exit 1
}

# Check environment variables
Write-Host "[3/4] Checking Android environment..." -ForegroundColor Yellow
if ($env:JAVA_HOME) {
    Write-Host "  ✓ JAVA_HOME: $env:JAVA_HOME" -ForegroundColor Green
} else {
    Write-Host "  ✗ JAVA_HOME not set (see ANDROID_SETUP.md)" -ForegroundColor Red
}

if ($env:ANDROID_SDK_ROOT) {
    Write-Host "  ✓ ANDROID_SDK_ROOT: $env:ANDROID_SDK_ROOT" -ForegroundColor Green
} else {
    Write-Host "  ✗ ANDROID_SDK_ROOT not set (see ANDROID_SETUP.md)" -ForegroundColor Yellow
}

# Build
Write-Host "[4/4] Building Android APK..." -ForegroundColor Yellow
Write-Host "This may take 5-15 minutes on first build..." -ForegroundColor Gray
Write-Host ""

python -m buildozer android debug

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✓ Build successful!" -ForegroundColor Green
    Write-Host ""
    Write-Host "APK Location: bin\financepro-2.0.0-debug.apk" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "  1. Enable USB Debugging on your Android phone" -ForegroundColor Gray
    Write-Host "  2. Connect phone via USB" -ForegroundColor Gray
    Write-Host "  3. Run: adb install bin\financepro-2.0.0-debug.apk" -ForegroundColor Gray
} else {
    Write-Host ""
    Write-Host "✗ Build failed!" -ForegroundColor Red
    Write-Host "Check the error messages above and see ANDROID_SETUP.md" -ForegroundColor Yellow
}
