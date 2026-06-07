[app]
title = Finance Pro 2.0
package.name = financepro
package.domain = org.financepro
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf
version = 2.0.0
requirements = python3,kivy,pandas,numpy,scikit-learn,requests,python-dateutil,pytz
permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
fullscreen = 0
orientation = portrait

[buildozer]
log_level = 2
warn_on_root = 1
build_dir = .buildozer
bin_dir = ./bin

[app:android]
permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
features = android.hardware.touchscreen
api = 31
minapi = 21
ndk = 25b
arch = armeabi-v7a

[buildozer:android]
accept_sdk_license = True
android_api = 31
android_minapi = 21
android_ndk = 25b
android_accept_sdk_license = True
