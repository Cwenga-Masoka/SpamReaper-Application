[app]

# This is the name of the app that will appear on the android homescreen
title = SpamReaper

# This must be unique on the playstore if the app is ever uploaded
# It follows the format: com.yourname.appname
package.name = spamreaper
package.domain = com.cwengamasoka

# Specify the folder where main.py lives - a single dot means ths current file
source.dir = .

# The entry point of your app - the file Kivy runs first 
source.include_exts = py,png,jpg,kv,atlas,json,ttf

# The current version of the app
version = 1.0

# Every libraryy the app will need is listed below
# Buildozer will download and compile all these for android
requirements = python3,
               kivy==2.2.1,
               kivymd==1.2.0,
               plyer,
               sqlite3,
               android,
               requests,
               pyjnius

# Permissions your app needs on android device
# READ_SMS - allows the app to read messages from the inbox
# WRITE_SMS - alls the app to delete messages
# RECEIVE_BOTT_COMPLETED - allows schduler to restart aftre phone reboot 
# VIBRATE - allows notifications to vibrate the phone

android.permissions = INTERNET,
                      ACCESS_NETWORK_STATE,
                      RECEIVE_BOOT_COMPLETED,
                      VIBRATE,
                      POST_NOTIFICATION

# This tells Android this app is built for modern Android versions
android.targetapi = 35

# The minimum Android version your app supports
# API 21 = Android 5.0 (Lollipop) — covers most devices in use today
android.minapi = 26

# The Android API version to build against
# Always use a recent one for best compatibility
android.api = 35

# The Android NDK version Buildozer should use
# NDK is needed to compile Python and libraries for Android's CPU
android.ndk = 25b

# The architecture(s) to build for
# arm64-v8a covers all modern Android phones
# armeabi-v7a covers older 32-bit phones
android.archs = arm64-v8a, armeabi-v7a

# Allows the app to write to external storage if needed
android.allow_backup = True

# forces Buildozer to use the latest python-for-android
p4a.branch = v2024.01.21

# The orientation your app supports
# 'portrait' means the app stays upright and doesn't rotate
orientation = portrait

# Whether the app runs in fullscreen mode
# 0 means the status bar at the top remains visible
fullscreen = 0

# Path to your app icon — create a 512x512 PNG image called icon.png
# and place it in your project folder
icon.filename = %(source.dir)s/icon.png

# Path to a presplash screen image shown while the app loads
# presplash.filename = %(source.dir)s/presplash.png

[buildozer]

# The level of detail in Buildozer's output logs
# 2 is verbose — good for debugging build errors
# Set to 1 for cleaner output once everything is working
log_level = 2

# Warns you if you run Buildozer as the root user (generally not recommended)
warn_on_root = 1
