# Android Notify - Flet Test App

A Flet-based Android app for testing the [android-notify](https://github.com/Fector101/android_notify) library. Send and verify notification styles, channels, callbacks, and permissions on a real device.

## Install

Download the latest APK from the [Releases](../../releases) page and install it on your Android device.

## App Sections

### Home
- Permission status indicator
- Send a basic notification
- Request notification permission
- Cancel all active notifications

### Styles
Test every notification style the library supports:

| Style | What it does |
|---|---|
| Simple | Basic title + message |
| Progress | Live progress bar with updates |
| Big Text | Expandable long text block |
| Big Picture | Large image preview |
| Large Icon | Right-side icon image |
| Inbox | Multi-line list style |
| Buttons | Action buttons below content |
| Persistent | Survives clear-all |
| Update Title/Msg | Modify title and message after sending |
<!-- | Custom Colors | Colored title and body text | -->

### Channels
- Create and send notifications on custom channels
- Check if a channel exists
- List all active channels

### Tests
- Run the full on-device unittest suite
- View test output in a scrollable log viewer

## Permissions

The app requests `POST_NOTIFICATIONS` at runtime on Android 13+. The Home tab shows permission status with a green/red indicator.

## Build locally

Requires: Python 3.10+, [Flet CLI](https://flet.dev), Flutter SDK, Android SDK.

```bash
# Build APK
flet build apk
# APK output: build/apk/antest_demo.apk
```

## Tech Stack

- [Flet](https://flet.dev) - UI framework (NavigationBar, Cards, Snackbar)
- [android-notify](https://github.com/Fector101/android_notify) - Android notification library
- Python 3.14 bundled in release builds
