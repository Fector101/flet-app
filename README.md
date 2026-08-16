# Android Notify - Flet Test App

A Flet-based Android app for testing the [android-notify](https://github.com/Fector101/android_notify) library. Send and verify notification styles, channels, callbacks, and permissions on a real device.

## Install

Download the latest APK from the [Releases](../../releases) page and install it on your Android device.

## Contains

| Notification Style | Description |
|---|---|
| Simple | Basic title + message notification |
| Progress | Progress bar with live updates |
| Big Picture | Notification with a large image |
| Big Text | Expanded long-text notification |
| Inbox | Multi-line inbox-style notification |
| Large Icon | Notification with a large icon image |
| Action Buttons | Notification with tap action buttons |
| Custom Icon | Notification with a custom small icon |
| Channels | Create and target specific notification channels |
| Persistent | Notifications that persist until dismissed |
| Update Title/Message | Modify a notification after sending |
| Cancel All | Dismiss all active notifications |


## Permissions

The app requests `POST_NOTIFICATIONS` at runtime on Android 13+. Use the **Ask Permission If Needed** button in the app to trigger the system prompt.

## Build locally

Requires: Python 3.10+, [Flet CLI](https://flet.dev), Flutter SDK, Android SDK.

```bash
# Build APK
flet build apk
# APK output: build/apk/antest_demo.apk
```

## Run tests on device

The app includes an on-device test suite. Tap **Run Tests** in the app to execute the notification test cases and view results in the log viewer.

## Tech Stack

- [Flet](https://flet.dev) - UI framework
- [android-notify](https://github.com/Fector101/android_notify) - Android notification library
- Python 3.14 bundled in release builds
