# Finance Pro 2.0 - Android Build Setup Guide

## 📱 Build Android APK on Windows

This guide walks through building a fully functional Finance Pro 2.0 Android app.

---

## ✅ Prerequisites

You need these installed on your Windows PC:

1. **Python 3.8+** (already have it ✓)
2. **Java Development Kit (JDK) 11+** 
3. **Android SDK**
4. **Buildozer** (already installed ✓)

---

## 🔧 Step 1: Install Java Development Kit (JDK)

### Option A: Using Java 11 (Recommended)

1. Download **OpenJDK 11** from:
   - https://jdk.java.net/archive/ (Look for Java 11)
   - Or: https://www.microsoft.com/openjdk

2. Install it (e.g., to `C:\Java\jdk-11`)

3. Set environment variable:
   ```powershell
   # In PowerShell (Run as Administrator):
   [Environment]::SetEnvironmentVariable("JAVA_HOME", "C:\Java\jdk-11", "Machine")
   ```

4. Verify installation:
   ```powershell
   java -version
   javac -version
   ```

---

## 🔧 Step 2: Install Android SDK

### Option A: Using Android Studio (Easiest)

1. Download **Android Studio** from:
   - https://developer.android.com/studio

2. Install Android Studio

3. During installation, select:
   - ✓ Android SDK
   - ✓ Android SDK Platform-Tools
   - ✓ Android Emulator

4. After installation, open Android Studio → Settings → Android SDK
   - Install **SDK Platform 30+** (API Level 30+)
   - Install **Build Tools 34+**

5. Find your SDK location (usually `C:\Users\YourName\AppData\Local\Android\Sdk`)

### Option B: Command Line (Advanced)

1. Create folder: `C:\Android\Sdk`

2. Download Command Line Tools from:
   - https://developer.android.com/studio/command-line

3. Extract to `C:\Android\Sdk\cmdline-tools`

4. Install SDKs:
   ```powershell
   cd C:\Android\Sdk\cmdline-tools\bin
   .\sdkmanager --sdk_root=.. "platforms;android-31" "build-tools;34.0.0"
   ```

---

## 🔧 Step 3: Set Environment Variables

Add these to your Windows environment (Run as Administrator):

```powershell
# Set JAVA_HOME
[Environment]::SetEnvironmentVariable("JAVA_HOME", "C:\Java\jdk-11", "Machine")

# Set ANDROID_SDK_ROOT (adjust path if different)
[Environment]::SetEnvironmentVariable("ANDROID_SDK_ROOT", "C:\Users\YourName\AppData\Local\Android\Sdk", "Machine")

# Set ANDROID_HOME (same as ANDROID_SDK_ROOT)
[Environment]::SetEnvironmentVariable("ANDROID_HOME", "C:\Users\YourName\AppData\Local\Android\Sdk", "Machine")
```

**Verify:**
```powershell
echo $env:JAVA_HOME
echo $env:ANDROID_SDK_ROOT
```

---

## 🔧 Step 4: Install Build Tools

Open PowerShell and run:

```powershell
# Install additional dependencies
pip install --upgrade pip
pip install cython
pip install buildozer
```

---

## 🚀 Step 5: Build Android APK

### Method 1: Use Build Script (Recommended for Windows)

```powershell
cd C:\Users\akamp\Desktop\selfPython\my_financial_mgt
.\build_android.bat
```

### Method 2: Manual Build

```powershell
cd C:\Users\akamp\Desktop\selfPython\my_financial_mgt
python -m buildozer android debug
```

### Build Process
- **First time:** 10-20 minutes (downloads NDK, builds)
- **Subsequent builds:** 2-5 minutes

---

## ✅ Verify Build Success

After successful build, you'll see:

```
APK Location: bin\financepro-2.0.0-debug.apk
```

---

## 📱 Step 6: Install on Android Phone

### Prerequisites:
- Android phone with USB debugging enabled
- USB cable
- ADB (Android Debug Bridge)

### Enable Developer Mode on Android:
1. Settings → About Phone
2. Tap Build Number 7 times
3. Settings → Developer Options → USB Debugging ON

### Install APK:

```powershell
# Connect phone via USB
# Verify connection:
adb devices

# Install app:
adb install bin\financepro-2.0.0-debug.apk

# Monitor installation:
adb logcat | findstr "financepro"
```

---

## 🎉 Running the App

1. Look for "Finance Pro 2.0" on your Android phone
2. Tap to launch
3. Enjoy full financial management on mobile!

---

## 🐛 Troubleshooting

### Build Error: "java command not found"
```
Solution: Set JAVA_HOME environment variable (see Step 3)
```

### Build Error: "Android SDK not found"
```
Solution: Set ANDROID_SDK_ROOT environment variable (see Step 3)
```

### Build Error: "NDK installation failed"
```
Solution: Let it download (~1GB), this is normal on first build
Alternatively: Manually download NDK r25 from developer.android.com
```

### APK won't install
```bash
# Check phone compatibility
adb devices

# Clear app data
adb shell pm uninstall org.financepro

# Try install again
adb install -r bin\financepro-2.0.0-debug.apk
```

### App crashes on Android
```bash
# View error logs:
adb logcat | findstr "financepro"

# Or use logcat viewer in Android Studio
```

---

## 📋 Quick Reference

| Command | Purpose |
|---------|---------|
| `python -m buildozer android debug` | Build debug APK |
| `python -m buildozer android release` | Build signed release APK |
| `python -m buildozer android clean` | Clean build files |
| `adb devices` | List connected phones |
| `adb install bin/financepro-2.0.0-debug.apk` | Install app |
| `adb uninstall org.financepro` | Uninstall app |
| `adb logcat` | View app logs |

---

## 🎯 What's Included in Android APK

✅ All features from desktop app:
- Dashboard with health score
- Add expenses/income
- ML predictions & anomaly detection
- Auto-categorization
- Analytics & reports
- Multi-currency support
- SQLite database (stores on phone)
- 2,500+ lines of code
- All AI/ML models

---

## ✨ Next Steps

After successfully building:

1. **Test on Phone:**
   - Add some transactions
   - Check dashboard
   - Explore analytics

2. **Share App:**
   - APK location: `bin/financepro-2.0.0-debug.apk`
   - Can install on multiple phones via ADB
   - Or build release APK for Google Play

3. **Customize:**
   - Edit buildozer.spec for app icon/name
   - Modify colors in main.py
   - Add your branding

---

## 📞 Need Help?

Common issues and solutions in `buildozer.spec` comments.

For more info:
- Buildozer docs: https://buildozer.readthedocs.io/
- Kivy Android: https://kivy.org/doc/stable/guide/android.html
- Android Debug Bridge: https://developer.android.com/tools/adb

---

**Status:** Ready to build your Android app! 📱💰
