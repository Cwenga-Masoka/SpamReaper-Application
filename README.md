# SpamReaper

A personal Android app that scans your Gmail inbox for spam, tracks flagged
messages over a configurable review window, sends push notifications before
anything gets deleted, and lets you review and keep or delete individual
emails — all from a clean, custom-built mobile UI.

This is a personal project, built to solve a personal spam problem, not a
published or commercially distributed app.

---

## What it does

- **Scans your Gmail inbox** for spam using a two-pass keyword + sender
  heuristic — checking sender format and subject first (fast), then falling
  back to a full body check only when needed.
- **Tracks flagged emails locally** in a SQLite database, with a
  configurable "review window" (default: 5 days) before anything is
  actually deleted.
- **Sends a push notification** the day before a flagged email is
  permanently removed, so nothing disappears without warning.
- **Lets you review, keep, or delete** flagged emails individually from
  the app, with a full history screen showing everything that's been
  actioned — including a restore option for anything still sitting in
  Gmail's Trash.
- **Fully configurable** — review window length, spam keyword list, and
  scan interval are all editable from the Settings screen, no rebuild
  required.

---

## Tech stack

| Layer | Tech |
|---|---|
| UI framework | [Kivy](https://kivy.org/) 2.2.1 + [KivyMD](https://kivymd.readthedocs.io/) 1.2.0 |
| Language | Python 3.11 |
| Android packaging | [Buildozer](https://buildozer.readthedocs.io/) + python-for-android (`v2024.01.21`) |
| Backend / Gmail access | Gmail API via raw `requests` calls (OAuth2, no Google client library) |
| Local storage | SQLite |
| Notifications | [Plyer](https://plyer.readthedocs.io/) |
| Design system | Custom "Surgical Minimalism" theme (`theme.py`) — Hanken Grotesk + JetBrains Mono |

**Why raw `requests` instead of Google's official Python client?** Google's
`google-api-python-client` pulls in `cryptography`, which fails to
cross-compile for Android under python-for-android. Talking to the Gmail
REST API directly with `requests` sidesteps that entirely.

**Target platform:** Android API 26–35, built for `arm64-v8a` and
`armeabi-v7a`.

---

## Project structure

```
SpamReaper/
├── main.py                # App entry point, screen navigation, login orchestration
├── gmail_auth.py           # OAuth2 flow, token storage/refresh
├── email_reader.py         # Gmail inbox scanning (metadata + body fetch)
├── email_deleter.py        # Trash / untrash via Gmail API
├── spam_detector.py        # Keyword + sender-pattern spam heuristics
├── scheduler.py             # Background scan loop + deletion reminders
├── tracker_db.py            # SQLite layer — flagged messages + action history
├── notifier.py               # Push notifications (Plyer)
├── config_manager.py        # Reads/writes config.json, in-memory cache
├── config.json               # User-editable settings (review window, keywords, etc.)
├── theme.py                    # Design tokens — colors, fonts, urgency states
├── review_screen.py           # Main inbox review UI
├── settings_screen.py         # Settings UI (review window, keywords, account, notifications)
├── history_screen.py           # Action history UI (deleted / kept emails)
├── spamreaper.kv                # Kivy layout definitions
├── intent_filters.xml            # Android manifest intent filters (OAuth redirect)
└── buildozer.spec                 # Android build configuration
```

---

## Setup

### Prerequisites

- Python 3.11+ (Windows or Linux)
- For Android builds: WSL/Ubuntu with Buildozer, python-for-android, and
  the Android SDK/NDK toolchain
- A Google Cloud project with the **Gmail API** enabled
- An OAuth 2.0 client (see [Google Cloud setup](#google-cloud-setup) below)

### Desktop (fastest way to test app logic)

Desktop runs the exact same Python code as Android for anything that isn't
Android-specific (UI layout, OAuth logic, spam detection, database, etc.),
so it's the quickest way to iterate without a full Buildozer rebuild.

```bash
python -m venv venv
venv\Scripts\activate          # Windows
pip install kivy==2.2.1 kivymd==1.2.0 requests plyer
python main.py
```

### Android build

```bash
# Inside WSL/Ubuntu
source ~/SpamReaper/env/bin/activate
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64

buildozer android debug deploy run
```

> **Note:** Omit `buildozer android clean` unless you've changed native
> dependencies in `buildozer.spec`'s `requirements` — running a full clean
> before every build forces a complete native recompile and can turn a
> few-minute build into an hour-long one.

### Google Cloud setup

1. Create a project in [Google Cloud Console](https://console.cloud.google.com)
   and enable the **Gmail API**.
2. Create an OAuth 2.0 client and configure the consent screen with the
   `gmail.modify` scope.
3. If the app is in "Testing" publishing status (typical for a personal
   project), add your own Google account under **Test users** — otherwise
   login will fail regardless of client configuration.
4. Download the client credentials JSON and place it in the project root
   (see `gmail_auth.py` for the expected filename).

---

## Current status

The backend (Gmail scanning, spam detection, tracking database, deletion,
and notifications) is fully functional and confirmed working on-device.

**Known issue — Gmail OAuth login on Android:** Google's OAuth flow
requires a redirect back into the app after the user logs in via browser,
and Android's app lifecycle makes this reliably harder than on desktop.
A few approaches have been tried:

- ❌ **Loopback HTTP server** (`127.0.0.1`) — works well on desktop, but
  Android backgrounds the app and blocks the local socket the moment the
  browser opens, even with a wake lock held.
- ❌ **OAuth Device Authorization flow** — sidesteps the redirect problem
  entirely, but Google blocks restricted scopes like `gmail.modify` from
  this flow specifically.
- 🔄 **Custom URI scheme + Android intent** (current approach) — Google
  redirects to a custom `app://` scheme, which Android hands back to the
  app via an intent. Currently being debugged with `adb logcat`
  instrumentation at each handoff point to pin down exactly where
  delivery breaks.

Once login is stable, remaining polish items include improved onboarding
around the Android notification permission flow and general performance
tuning of the inbox scan.

---

## License

Personal project — not currently licensed for redistribution.
