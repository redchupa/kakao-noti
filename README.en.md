<p align="center">
  <img src="https://raw.githubusercontent.com/redchupa/kakao-noti/main/images/logo.png" alt="Kakao Notify Logo" width="640">
</p>

<p align="center">
  <a href="https://github.com/redchupa/kakao-noti/releases/latest"><img src="https://img.shields.io/github/v/release/redchupa/kakao-noti?include_prereleases&label=release&color=brightgreen" alt="Release"></a>
  <a href="https://github.com/hacs/integration"><img src="https://img.shields.io/badge/HACS-Custom-41BDF5.svg" alt="HACS"></a>
  <img src="https://img.shields.io/badge/Home%20Assistant-2024.4%2B-blue?logo=home-assistant&logoColor=white" alt="HA Version">
  <img src="https://img.shields.io/badge/KakaoTalk-Send_to_myself-FEE500?logo=kakaotalk&logoColor=black" alt="KakaoTalk">
  <a href="LICENSE"><img src="https://img.shields.io/github/license/redchupa/kakao-noti?color=lightgrey" alt="License"></a>
  <img src="https://img.shields.io/badge/lang-English-blue.svg" alt="English">
</p>

<p align="center">
  <a href="https://github.com/redchupa/kakao-noti/stargazers"><img src="https://img.shields.io/github/stars/redchupa/kakao-noti?style=for-the-badge&logo=github&color=yellow" alt="Stars"></a>
  <a href="https://github.com/redchupa/kakao-noti/network/members"><img src="https://img.shields.io/github/forks/redchupa/kakao-noti?style=for-the-badge&logo=github&color=blue" alt="Forks"></a>
  <a href="https://github.com/redchupa/kakao-noti/issues"><img src="https://img.shields.io/github/issues/redchupa/kakao-noti?style=for-the-badge&logo=github&color=orange" alt="Issues"></a>
  <a href="https://github.com/redchupa/kakao-noti/commits/main"><img src="https://img.shields.io/github/last-commit/redchupa/kakao-noti?style=for-the-badge&logo=github&color=brightgreen" alt="Last commit"></a>
</p>

<p align="center">
  <img src="https://img.shields.io/github/repo-size/redchupa/kakao-noti?color=informational&label=repo%20size" alt="Repo size">
  <img src="https://img.shields.io/github/languages/top/redchupa/kakao-noti?color=blueviolet" alt="Top language">
  <img src="https://img.shields.io/maintenance/yes/2026?color=success" alt="Maintained">
  <img src="https://img.shields.io/badge/Made%20with-Python-3776AB?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Made%20for-Home%20Assistant-41BDF5?logo=home-assistant&logoColor=white" alt="Made for HA">
</p>

<p align="center">
  <b>🌐 Language:</b>
  <a href="README.md">🇰🇷 한국어</a> ·
  <b>🇬🇧 English</b>
</p>

# KakaoTalk "Send to Myself" — Home Assistant Notifier

A Home Assistant integration that delivers automation and script messages to your **personal KakaoTalk "Chat with Myself"** room.
Think of it as Telegram bot notifications, but in KakaoTalk instead.

```yaml
# Just add this line to any automation or script — it lands in your KakaoTalk
service: notify.kakao_noti
data:
  message: "Front door was opened"
```

> 💬 This integration only sends messages to **your own KakaoTalk "Chat with Myself"** room.
> It does NOT send messages to friends or family — it's strictly **you → you**.
> ("Chat with Myself" is the chat room with your own profile at the top of your KakaoTalk chat list.)

> 📌 **Note**: KakaoTalk is the dominant messenger in South Korea (95%+ market share). This integration is primarily useful if you already use KakaoTalk daily. Outside Korea, consider Telegram, Pushover, or Discord notifiers instead.

---

## 📑 Table of Contents

- [What you get by following this guide](#-what-you-get-by-following-this-guide)
- [How does it work? (3-min big picture)](#-how-does-it-work-3-min-big-picture)
- [Before you start (please read)](#-before-you-start-please-read)
- [Step 1 · Create an app on Kakao Developers](#step-1--create-an-app-on-kakao-developers)
- [Step 2 · Install the component via HACS](#step-2--install-the-component-via-hacs)
- [Step 3 · Connect KakaoTalk in HA](#step-3--connect-kakaotalk-in-ha)
- [Step 4 · Send your first message](#step-4--send-your-first-message)
- [Real-world automation examples](#real-world-automation-examples)
- [Sending to family members (multi-account)](#sending-to-family-members-multi-account)
- [Tokens refresh automatically](#tokens-refresh-automatically)
- [🔐 Security & Privacy — you can use this with peace of mind](#-security--privacy--you-can-use-this-with-peace-of-mind)
- [Troubleshooting](#troubleshooting)
- [FAQ](#faq)
- [Support](#support)
- [⭐ Please star the repo](#-please-star-the-repo--so-others-can-find-it)
- [License](#license)

---

## 🔍 How does it work? (3-min big picture)

```
[Automation fires in HA]
        ↓
[notify.kakao_noti is called]
        ↓
[HA sends the message via Kakao OAuth token]
        ↓
[Kakao server]
        ↓
[Arrives in your KakaoTalk "Chat with Myself"] ✉️
```

One-time setup:
1. **Create an app on Kakao Developers** (issue REST API key + Client Secret) — ~10 min
2. **Install this integration via HACS** in Home Assistant — ~5 min
3. Authorize Kakao login in HA → token is issued and saved automatically — ~5 min
4. **Send a test message** → confirm it landed in your KakaoTalk

After that: just call `notify.kakao_noti` from any automation. HA handles token refresh in the background.

---

## ✨ What you get by following this guide

- Send a KakaoTalk message with a single `notify.kakao_noti` call from any automation or script
- **Multi-line, emoji, and title support**; auto-truncated past 1850 characters
- **Automatic Kakao token refresh** (HA handles it for you)
- **No extra server or add-on required** — HA talks to Kakao directly
- **Multi-account support** so each family member can receive on their own KakaoTalk

> ⏱️ Plan on **30–40 minutes** end to end. First-time Kakao console users may need a bit longer.

---

## 🧭 Before you start (please read)

| What you need | Description |
|---|---|
| **Home Assistant** | Where this integration runs. If you don't have HA yet → [HA official installation guide](https://www.home-assistant.io/installation/)<br/>**Check version**: HA left sidebar (mobile: top-left ☰) → **Settings** → **About** → **2024.4 or newer required** |
| **HACS** | A community "app store" that makes installing third-party integrations easy. Official install guide: <https://www.hacs.xyz/docs/use/download/download/> |
| **External HTTPS URL** ⚠️ | Required so Kakao can return the login result to your HA. See details below |
| **A KakaoTalk account** | The account that will receive messages. Sign up for Kakao Developers with the same account |

### Why do I need an external HTTPS URL?

When Kakao finishes login and wants to tell HA "login succeeded!", it needs **an HTTPS URL reachable from the public internet to your HA instance**. Without it, this integration cannot work.

#### How to check whether you already have one

1. HA left sidebar → **Settings** → **System** → **Network**
2. Look at the **"Home Assistant URL"** section
3. If the **"Internet (External)"** URL is filled with an `https://...` address and you can open that URL from outside ✅ — proceed
4. If it's empty, only `http://`, or your LAN IP (`192.168.x.x`) ❌ — pick one of the options below

#### Ways to get an external HTTPS URL

| Method | Cost | Difficulty | Recommended for |
|---|---|---|---|
| **Nabu Casa Cloud** | $6.5/month | ⭐ Very easy | First-timers / not comfortable with networking |
| **DuckDNS + Let's Encrypt add-on** | Free | ⭐⭐⭐ Moderate | Some networking experience |
| **Cloudflare Tunnel** | Free | ⭐⭐⭐ Moderate | Have your own domain |

#### Nabu Casa Cloud signup (easiest option)

1. HA left sidebar → **Settings** → **Home Assistant Cloud** (if the menu is missing, go to **Add Integration** and search for "Home Assistant Cloud")
2. Click **"Sign up"** → enter email + password
3. Click the activation link in the confirmation email
4. Return to HA, log in → choose **"Try free for 31 days"** or pay
5. Toggle **"Remote control"** ON → you immediately get an external URL like `https://<random>.ui.nabu.casa`
6. Open that URL in a new tab and confirm your HA loads ✅

Write down your HA external URL. You'll need to enter it once during Step 3-2.

Example: `https://abc12345.ui.nabu.casa` / `https://my-home.duckdns.org`

> ⚠️ **Caution**: If you proceed through Steps 1 and 2 without having an external HTTPS URL, you'll get stuck at the last step of Kakao OAuth. Confirm this first.

---

# Step 1 · Create an app on Kakao Developers

> 💬 First time with Kakao Developers? Just follow along carefully.
> Time: ~10–15 minutes.

## 1-1. Sign up for Kakao Developers

1. Go to **<https://developers.kakao.com>**
2. Click **Login** (top right) → **Log in with Kakao account**
   - Use the same KakaoTalk account you want to receive messages on
3. If this is your first time, accept the terms

## 1-2. Create a new application

1. Click **"My Application"** (top right)
2. Click the **"Add an application"** button
3. Fill in:
   - **App name**: anything (e.g., `HA KakaoTalk Notify`)
   - **Company name**: your name or nickname
   - **Category**: pick anything reasonable (e.g., Lifestyle)
4. **Save**
5. Click the app you just created to enter it

## 1-3. Platform Keys page — four settings in one place

In the left menu click **"App → Platform Keys"**. This opens the **"REST API Key Edit"** page (or click the REST API Key value in the table).

> 📍 Confirm the page title says **"REST API Key Edit"**. If not, click left menu → **App → Platform Keys** again.

> 🎯 **All four of the following are done on this single page:**

### (1) Copy your REST API Key

At the top of the page you'll see the **REST API Key** (32 alphanumeric characters).
👉 Click to copy → save to a notepad 📌 **This is the first value you'll paste into HA later.**

### (2) Register the Kakao Login redirect URI

In the middle of the page, find the **"Kakao Login Redirect URI"** field and enter **exactly** the following:

```
https://my.home-assistant.io/redirect/oauth
```

> 📌 **Do not modify this URL in any way.** A single different character causes the dreaded KOE006 error later.
>
> **What is this?** It's the standard OAuth redirector operated by the Home Assistant Foundation.
> All HA users share this URL. Your own HA address is never exposed to Kakao.

### (3) Generate + activate the Client Secret

Lower on the same page, find the **"Client Secret → Kakao Login"** section.

> ⚠️ Do not touch the **"Business Verification"** section — that's for a different purpose.

1. If the code is empty or shows `-`, click **"Generate code"**
2. Copy the issued 32-character code and **save it to your notepad** 📌 **This is the second value you'll paste into HA later.**
3. **Toggle "Activate" to ON** ⚠️ **Skipping this causes auth failure**

### (4) Click [Save] at the bottom of the page 💾

⚠️ If you leave the page without clicking Save, none of the above applies. **Make sure to click [Save].**

## 1-4. Enable Kakao Login

Left menu → **"Product Settings → Kakao Login"**.

- Make sure the **"Activation"** toggle at the top is **ON**. (If OFF, turn it ON.)

## 1-5. Grant the talk_message (message send) permission

Left menu → **"Product Settings → Kakao Login → Consent Items"**.

Scroll down to the **"Access Permissions"** table and find the **"Send KakaoTalk message (talk_message)"** row.

1. Click **"Settings"** on that row
2. **Consent level** → choose **"Optional consent"**
3. **Consent purpose**: "Send KakaoTalk messages" (or anything sensible)
4. **Save**

> ⚠️ If the talk_message row is **greyed out** and unclickable:
> Go to left menu → **App → Members** and add your KakaoTalk account **as a team member**.
> For self-notifications, that's all you need.

## ✅ Step 1 completion checklist

| Item | OK? |
|---|---|
| REST API Key saved | ⬜ |
| Client Secret code saved | ⬜ |
| Client Secret "Activate" ON | ⬜ |
| Redirect URI registered + page [Save] clicked | ⬜ |
| Kakao Login "Activation" ON | ⬜ |
| talk_message consent item saved as "Optional consent" | ⬜ |

All checked? Proceed to Step 2.

---

# Step 2 · Install the component via HACS

> 💬 HACS is the **"app store"** that lets you install community integrations and cards into Home Assistant.
> Once installed, you can easily add more integrations later.

## 2-1. Do you already have HACS?

If **HACS** appears in your HA left menu → already installed, **skip to 2-2.**

If not → **Official HACS installation guide**: <https://www.hacs.xyz/docs/use/download/download/>
(The procedure differs by HA install type — OS / Container / Core / Supervised. Follow the section that matches yours.
HACS requires a GitHub account during install — free signup: <https://github.com/signup>)

After install, restart HA. **HACS** should appear in the left menu.

## 2-2. Register this integration in HACS

> 💬 HACS has both an **"official catalog"** and supports **"custom repositories"** that anyone can host.
> This integration goes through the latter (custom repository).

1. Click **HACS** in the HA left menu
2. Top right ⋮ (three dots) → **"Custom repositories"**
3. Enter:
   - **Repository URL**: `https://github.com/redchupa/kakao-noti`
   - **Type**: select `Integration`
4. **Add**
5. Close

## 2-3. Download

1. From the HACS main screen, type **"Kakao"** in the search box at the top
2. Click the **"Send to myself on KakaoTalk Notify"** card
3. Click **"Download"** at the bottom right
4. When the version picker appears, leave it on the latest → **"Download"**
5. If you see **"Home Assistant restart required"** → **Settings → System → Restart → "Restart Home Assistant"**
6. Wait for HA to come back (1–5 minutes)

---

# Step 3 · Connect KakaoTalk in HA

## 3-1. Register Application Credentials (one-time)

> 💬 This stores the REST API Key and Client Secret you noted in Step 1 inside HA.

1. Go to **Settings → Devices & Services**
2. Click the **"Application Credentials"** tab at the top
   - Or open the URL directly: `https://<your-ha-address>/config/application_credentials`
3. Click the **"Add credentials"** button at the bottom right
4. Fill in:

   | Field | Value |
   |---|---|
   | Integration | Select **`Send to myself on KakaoTalk Notify`** from the dropdown |
   | Name | Anything (e.g., "My Kakao App") |
   | OAuth Client ID | The **REST API Key** you saved in 1-3 (1) |
   | OAuth Client Secret | The **Client Secret code** you saved in 1-3 (3) |
5. Click **Add** → credentials registered

## 3-2. Add the integration and sign in to Kakao

1. **Settings → Devices & Services → Add Integration** (bottom-right blue button)
2. Search **"Kakao"** → click **"Send to myself on KakaoTalk Notify"**
3. The credentials you just registered are auto-selected → **Next**
4. The browser will **redirect you to the Kakao login page**
5. **Log in with your KakaoTalk account** (or auto-continue if already logged in)
6. Consent screen appears:
   - **Check ✅ "Send KakaoTalk messages"** ⚠️ if you skip this, sending won't work
   - Click **"Agree and continue"**
7. You'll see a one-time screen at this point — a white background titled **"My Home Assistant"** with an input box and Save button:
   - Message: "You are seeing this page because you have been linked to a page in your Home Assistant instance but have not configured My Home Assistant."
   - Enter your **HA external URL** (e.g., `https://abc12345.ui.nabu.casa` or `https://my-home.duckdns.org`)
   - Don't add `/` or `/auth/...` at the end. Just the base URL.
   - Click **Save**
8. You'll be redirected back to your HA → 🎉 **"Success" message + integration registered**

> 💡 **What is this "My Home Assistant" screen?** It's the standard redirector operated by the Home Assistant Foundation — a safe relay that forwards Kakao OAuth results to your HA. You register your HA address once, then the browser remembers it.

---

# Step 4 · Send your first message

Let's send a test message. Go to **Developer Tools → Actions**.

### Method 1 · Legacy service + GUI form (simplest)

1. In the **Action (Service)** dropdown, type **`notify.kakao_noti`** → select it
2. A form appears automatically:
   - **Message**: `My first KakaoTalk message from HA 🎉`
   - **Title** (optional): `Test`
3. Click **"Perform action"** at the bottom right

> 💡 **Only YAML mode shown and no form appears?**: Click **"Go to UI mode"** at the bottom left. Or upgrade to v0.7.0+ if you're on a pre-v0.6.x version (GUI form was added).

### Method 2 · NotifyEntity standard (handy when broadcasting to multiple accounts)

1. In **Action (Service)** type **`notify.send_message`** → select
2. **Target → Entity**: pick `notify.kakao_noti` (you can also select `kakao_noti_2` for multi-account)
3. **Message**: body
4. **Title**: (optional) title
5. **Perform action**

### Method 3 · YAML directly (for automations and scripts)

```yaml
service: notify.kakao_noti
data:
  message: "My first KakaoTalk message from HA 🎉"
  title: "Test"   # optional
```

---

→ Open KakaoTalk and go to **"Chat with Myself"**. If the message arrived, success! 🥳

### Message didn't arrive? Quick checks

| Symptom | Answer |
|---|---|
| **Red error box after clicking "Perform action"** | Empty message body. Fill the **Message** field and retry |
| **"Perform action" succeeds but no message** | You probably didn't check "Send message" on the consent screen during integration setup. Remove the integration and redo [Step 3-2](#3-2-add-the-integration-and-sign-in-to-kakao) — verify the checkbox ✅ |
| **No message after 5–10 seconds** | HA → **Settings → System → Logs**, search for `kakao_noti`, check the error → see the [Troubleshooting](#troubleshooting) section |
| **Other KakaoTalk messages arrive but not this one** | Nothing wrong with the Kakao app itself — token / consent / Kakao console setting is missing somewhere. Redo the Step 1 checklist |

---

## Real-world automation examples

> ⚠️ **Common note**: The examples below are **templates**. Entity IDs like `binary_sensor.front_door`, `sensor.living_room_temperature`, `weather.kma_fold7_weather` **must be replaced with actual entity IDs from your own HA** for them to work.
>
> **How to find your entity IDs**:
> 1. Click **Developer Tools → States**
> 2. In the search box type what you're looking for (e.g., `binary_sensor.`, `sensor.temperature`, `weather.`)
> 3. Copy the entity ID that exists in your environment

### Automation 1 (template): front door open notification

**Settings → Automations & Scenes → Create automation** → "Create new automation" → top right ⋮ → **"Edit in YAML"** and paste:

```yaml
alias: Front door open → KakaoTalk
trigger:
  - platform: state
    entity_id: binary_sensor.front_door   # ← replace with your door sensor
    to: "on"
action:
  - service: notify.kakao_noti
    data:
      message: "Front door opened ({{ now().strftime('%H:%M') }})"
```

### Automation 2 (template): daily 9 AM weather brief

```yaml
alias: Morning briefing KakaoTalk
trigger:
  - platform: time
    at: "09:00:00"
action:
  - service: notify.kakao_noti
    data:
      title: "Morning brief"
      message: |
        🗓 {{ now().strftime('%Y-%m-%d') }}
        🌡 Living room {{ states('sensor.living_room_temperature') }}°C   # ← replace with your sensor
        ☔ Rain chance {{ states('sensor.rain_probability') }}%             # ← replace with your sensor / weather entity
```

### Automation 3: HA start notification (use as-is)

```yaml
alias: HA started KakaoTalk
trigger:
  - platform: homeassistant
    event: start
action:
  - delay: "00:00:30"   # 30s grace period for other integrations to come up
  - service: notify.kakao_noti
    data:
      title: "HA notice"
      message: |
        🏠 Home Assistant started
        ⏰ {{ now().strftime('%Y-%m-%d %H:%M:%S') }}
```

### Automation 4 (template): rain start → notify self + family at the same time

Notifies when the weather entity changes to `rainy` / `pouring` etc. A 6-hour cooldown prevents spam when the rain stops and starts again.

```yaml
alias: Rain started (KakaoTalk)
trigger:
  - platform: state
    entity_id: weather.kma_fold7_weather   # replace with your weather entity
    to:
      - rainy
      - pouring
      - lightning-rainy
      - snowy-rainy
action:
  - service: notify.send_message
    target:
      entity_id:
        - notify.kakao_noti
        - notify.kakao_noti_2
    data:
      title: "Rain started"
      message: |
        ☔ It started raining
        🌡 Temp {{ states('sensor.kma_fold7_temperature') }}°C
        💧 Humidity {{ states('sensor.kma_fold7_humidity') }}%
        🌬 Wind {{ states('sensor.kma_fold7_wind_speed') }} m/s
        ⏰ {{ now().strftime('%H:%M') }}
  - delay: "06:00:00"   # block re-fire for 6 hours
mode: single
```

### Automation 5 (pattern): rich daily briefing — split into 2 messages to bypass the 1850-char cap

Kakao "memo" messages auto-truncate at 1850 characters. For richer content, split into two messages — they arrive as separate KakaoTalk messages.

```yaml
alias: Morning briefing (KakaoTalk)
trigger:
  - platform: time
    at: "09:00:00"
action:
  - service: notify.send_message
    target:
      entity_id: [notify.kakao_noti, notify.kakao_noti_2]
    data:
      title: "Morning briefing (1/2)"
      message: |
        🌤 {{ now().strftime('%m/%d') }}
        📍 {{ states('sensor.kma_fold7_location') }}

        Now: {{ states('sensor.kma_fold7_condition') }}
        Temp: {{ states('sensor.kma_fold7_temperature') }}°C
        … (today + air quality, etc. ~1700 chars)
  - delay: "00:00:01"
  - service: notify.send_message
    target:
      entity_id: [notify.kakao_noti, notify.kakao_noti_2]
    data:
      title: "Morning briefing (2/2)"
      message: |
        ▶ Tomorrow · sun · moon · milky way
        … (tomorrow forecast + sunrise/sunset + moon phase + milky way ~700 chars)
mode: single
```

---

## Sending to family members (multi-account)

> 💬 Want Dad and Mom to each get their own KakaoTalk notifications? — Each person adds their own Kakao account.

You'll **add family members as team members on your own Kakao app** (you keep using the same Application Credentials — no need to create new ones).

| Item | Description |
|---|---|
| Kakao app | Same app you created |
| What family must do | Sign up for Kakao Developers (one-time) + accept the invite |
| Extra HA work | Use an Incognito/InPrivate browser to add the second integration with the family Kakao login |

### ⚠️ Key — **Incognito/InPrivate browser is required**

If you add a second integration in a browser that's already auto-logged into your own Kakao account, it ends up registering you again and throws **"Kakao notify is already registered"**. To log in as a family member, you **must open a new Incognito/InPrivate window**.

| Browser | Incognito shortcut |
|---|---|
| Chrome / Edge | **Ctrl + Shift + N** |
| Firefox | **Ctrl + Shift + P** |
| Safari (Mac) | **Cmd + Shift + N** |

---

### 1. Add a family member in the Kakao console

1. Kakao Developers → **Your app → left menu "App → Members"**
2. Click **"Add member"**
3. Fill in:
   - **Kakao account (email)**: the email your family used to sign up for KakaoTalk (e.g., `family@kakao.com`, `name@daum.net`, `name@gmail.com`)
   - **Role**: **Viewer** ← the lowest role is enough (see the note below)
4. **Save**

> ⚠️ **If a family member signed up for KakaoTalk with a phone number only and no email registered**:
> They need to register an email first: KakaoTalk app → **More → Settings → Personal/Security → Kakao Account**. Or add an email at <https://accounts.kakao.com>.

> 💡 **Why is Viewer enough?**
> Per Kakao policy, dev-stage apps (not converted to a business app) can send talk_message to **all app members** regardless of role (Owner / Editor / Message Editor / Viewer). Viewer = read-only, so family members can't change your app settings — it's the safest.

### 2. Family member accepts the invite

Steps the family member must do themselves:

1. They receive a **Kakao Developers invite notification** on their KakaoTalk (or skip to step 4 if it doesn't arrive)
2. Tap the notification → moves to the Developers site
3. **Log in with their own Kakao account**
4. If no notification arrived → they open **<https://developers.kakao.com>** directly → top-right login → **My Application** → click the invited app
5. First time? Accept the Developers terms of service
6. Invite is accepted or auto-activated — your app's **App → Members** page shows them as **"Active"** ✅

> 💡 **Don't know the family member's email?**: Have them check it in their KakaoTalk app → **More → Settings → Personal/Security → Kakao Account**.

> ⚠️ **The family member must agree to sign up for Kakao Developers** for this approach to work. Signup is free with almost no info required, so it's a low burden.

### 3. Add a second integration in HA (Incognito required)

1. Open a new **Incognito window** (shortcut above)
2. In the Incognito window, open `https://<your-HA-external-url>` → log in to HA
3. **Settings → Devices & Services → Add Integration**
4. Search for **"KakaoTalk"** or **"Send to myself"** → click the card
5. Application Credentials are auto-selected → **Next**
6. **Log in with the family member's Kakao account on the Kakao login page** ← most important
   - Or use the **QR code** on the right of the Kakao login page — have the family scan it with their KakaoTalk app (More → QR code scan) for an easier flow
7. On the consent screen, check ✅ **"Send KakaoTalk messages"** → **"Agree and continue"**
8. If the **"My Home Assistant"** screen reappears, enter your HA external URL → Save (Incognito doesn't remember)
9. Return to HA → 🎉 the second integration is registered as **`notify.kakao_noti_2`**

> 💡 When you close the Incognito window, the family Kakao login disappears from that browser — but the token is already safely stored in HA, so it's fine.

---

### Using the registered second service

- First integration → `notify.kakao_noti`
- Second → `notify.kakao_noti_2`
- Third → `notify.kakao_noti_3` … numbered automatically

> 💡 **If you try to register the same Kakao account twice**, it's rejected automatically (`Kakao notify is already registered`) — a built-in safeguard.

### Broadcasting to two people from one automation

Cleanest (NotifyEntity standard):
```yaml
action:
  - service: notify.send_message
    target:
      entity_id:
        - notify.kakao_noti      # you
        - notify.kakao_noti_2    # family
    data:
      title: "Notice"
      message: "..."
```

Or call the legacy service twice:
```yaml
action:
  - service: notify.kakao_noti
    data:
      message: "..."
  - service: notify.kakao_noti_2
    data:
      message: "..."
```

---

## Tokens refresh automatically

- The Kakao login token is **refreshed every 6 hours** automatically (HA handles it)
- The refresh token is valid for **2 months** — if you send at least one message within that window, it gets auto-extended
- **Only if you send nothing for 2 months** does re-login become necessary — see "Re-authenticate" below

### Re-authenticate (when the token has expired)

1. **Settings → Devices & Services** → on the Kakao Notify integration card, click ⋮ → **Delete**
2. Redo from **Step 3-2 (Add integration)** → Kakao login + consent

> 💡 The Application Credentials still live — no need to register them again. If you do want to recreate them, delete them in **Settings → Devices & Services → "Application Credentials"** tab and re-add.

### Fully remove the integration

Remove `notify.kakao_noti` calls from your automations/scripts first, then:

1. **Settings → Devices & Services → Kakao Notify** → ⋮ → **Delete**
2. (Optional) Also delete the entry in **Application Credentials**
3. (Optional) HACS → Integrations → "Send to myself on KakaoTalk Notify" → ⋮ → **Remove** (also removes the code)
4. Restart HA

---

## 🔐 Security & Privacy — you can use this with peace of mind

> 💡 In one sentence: **This integration only "sends" messages to your own KakaoTalk. It cannot read your chats, fetch your friends list, or see conversations with other people.**

### ✅ What this integration can do (one thing)

- Send a message to **your own KakaoTalk "Chat with Myself"** (Kakao official API `talk/memo/default/send`)

### 🚫 What this integration **cannot** do

- ❌ Read your other KakaoTalk conversations (friend/group chats)
- ❌ Look up your friends list or contacts
- ❌ Send messages to other people (only to **yourself**)
- ❌ Change your KakaoTalk profile, picture, or status message
- ❌ Any Kakao Pay, transfer, or financial functions
- ❌ Access other Kakao services like Mail, Calendar, Gift, etc.

→ On the Kakao OAuth consent screen, **only the "Send KakaoTalk message (talk_message)" permission** is requested. The code does not even ask for anything else.

### 🔑 Where is your credential info stored?

| Info | Storage location | Exposed externally? |
|---|---|---|
| Kakao REST API Key, Client Secret | **Your HA's encrypted storage** (`.storage/application_credentials`) | ❌ stays inside your HA |
| Kakao access_token, refresh_token | **Your HA's encrypted storage** (`.storage/core.config_entries`) | ❌ stays inside your HA |
| Message body | Sent to Kakao only at the moment of dispatch — not stored in HA | (Kakao server retains it in your chat history) |

→ **Nothing about you is hardcoded in this component or its GitHub repo.** Source is on [GitHub](https://github.com/redchupa/kakao-noti) — verify directly (open-source, MIT license).

### 🌐 Communication path

```
HA (your home) ──HTTPS──> kapi.kakao.com (Kakao official) ──> your KakaoTalk
```

- All traffic is **HTTPS encrypted**
- **No middleman server / cloud / bridge** — HA talks to the Kakao official API directly
- The developer (me) cannot see your messages. They only flow between your HA and Kakao's servers.

### 🛑 You're always in control

| Goal | How |
|---|---|
| Pause sending temporarily | Disable the call in your automations/scripts |
| Revoke the token | Delete the integration (Settings → Devices & Services → Kakao Notify → ⋮ → Delete) |
| Decommission the Kakao app | Delete the app in Kakao Developers — all tokens become instantly invalid |
| Revoke consent | Kakao Account ([accounts.kakao.com](https://accounts.kakao.com)) → Connected Services → unlink your app |

### 🔍 What exactly does the "talk_message consent" allow?

The **"Send KakaoTalk message"** option you check on the Kakao consent screen means:

- ✅ This app can send KakaoTalk messages **only to you**
- ❌ It does **NOT** mean reading your KakaoTalk conversation history
- ❌ It does **NOT** mean sending messages to your friends

Per Kakao's official policy, **dev-stage apps (not converted to business)** can only send messages to **the app's own members**. In other words, Kakao blocks at the source any attempt to spam other people through this integration.

### 📜 Code verification

100% open source. If you suspect anything, audit it yourself:

- `custom_components/kakao_noti/api.py` — Kakao API call logic (only invokes the send API)
- `custom_components/kakao_noti/const.py` — the three Kakao endpoint URLs used (authorize · token · memo send)
- `custom_components/kakao_noti/notify.py` — message dispatch function

→ <https://github.com/redchupa/kakao-noti/tree/main/custom_components/kakao_noti>

---

## Troubleshooting

### During integration setup

| Message on screen | Cause | Fix |
|---|---|---|
| **"Application Credentials required"** | Skipped Step 3-1 | Redo Step 3-1 |
| Kakao screen shows **"KOE006 App admin setting error"** | Redirect URI mismatch | Verify the URI in 1-3 (2) exactly matches `https://my.home-assistant.io/redirect/oauth` AND that you clicked [Save] at the bottom |
| **"KOE003"** | Wrong REST API Key | Verify the Client ID pasted in 3-1 (typo / different app) |
| **"KOE101 no app permission"** | Kakao Login activation OFF | Confirm Step 1-4 |
| Consent screen has no **"Send message"** item | talk_message not set or greyed out | Check Step 1-5. If grey, add yourself as a team member |
| **"Unauthorized"** etc. | Client Secret mismatch | Verify 1-3 (3) Activate is ON + the code was copied exactly |
| **"Kakao notify is already registered"** | Same Kakao account being registered twice | For multi-account, you **must** log in as the family account in an Incognito/InPrivate window. See [the multi-account section](#sending-to-family-members-multi-account) |
| talk_message row is **greyed out** in consent | Family not registered as app member | Step 1 Kakao console → **App → Members** → add family Kakao email (Viewer role is fine) → family signs up for Developers + accepts the invite |
| HACS search for **"Send to myself..."** card shows nothing | Cache delay right after custom repository add | Refresh HACS (F5) or wait 30s–1 min. Still missing → verify the repo URL (`https://github.com/redchupa/kakao-noti`) |
| Application Credentials' **"Integration"** dropdown is empty | Forgot to restart HA after HACS download | **Settings → System → Restart** once more |
| Kakao console menus look different from this guide | Kakao revises its UI from time to time | If a menu name is slightly different but the meaning matches, click that one. Can't find it → open a GitHub Issue with a screenshot |

### On the My Home Assistant page

| Symptom | Fix |
|---|---|
| **"Enter Home Assistant URL"** screen appears | Enter your HA external URL (e.g., `https://abc.ui.nabu.casa`). Don't add `/` at the end |
| Pressed Save but got **"Connection failed"** | Confirm the URL is really reachable from outside. On a different network (4G/LTE), can you open HA via that URL? |

### During use

| Symptom | Fix |
|---|---|
| Integration added OK but no message arrives | "Send message" wasn't checked during Kakao consent. Delete the integration and redo Step 3-2 |
| Worked fine, then suddenly fails (401-ish) | 2 months idle → token expired. Delete the integration and redo Step 3-2 |
| Long message is truncated | Working as intended — past 1850 chars it auto-truncates and appends `\n… (truncated)` |

### Verbose logs

Add to `configuration.yaml` and restart HA:

```yaml
logger:
  default: warning
  logs:
    custom_components.kakao_noti: debug
```

Then **Settings → System → Logs**, search `kakao_noti`.

---

## FAQ

**Q. Can I send to a friend's or family member's KakaoTalk?**
A. This integration only supports **"send to myself"** (KakaoTalk "Chat with Myself" only). To send to friends, you'd need a separate paid service like Kakao Business Channel + AlimTalk. To notify family members individually, **each person registers their own account separately** (see [Multi-account](#sending-to-family-members-multi-account)).

**Q. Is the HA external URL truly mandatory?**
A. Yes — Kakao needs to return the login result to HA, which requires **an external HTTPS URL**. Pick one of Nabu Casa Cloud (paid, easiest), DuckDNS + Let's Encrypt (free), or Cloudflare Tunnel (free).

**Q. How many KakaoTalk messages can I send per day?**
A. Kakao's "send to me" allows **100–500 messages per user per day** depending on app tier. Plenty for typical automations.

**Q. Can I control HA by replying to the KakaoTalk message?**
A. This integration is **send-only**. For two-way control, a Telegram bot is the better choice.

**Q. Can I receive these messages on iPhone?**
A. Yes — wherever the KakaoTalk app is installed (Android / iOS / PC). HA sends the message to Kakao's server, which pushes it to all your devices.

**Q. Can I install without HACS?**
A. Yes (manual copy). Copy the entire `custom_components/kakao_noti/` folder from this repo into your HA's `config/custom_components/` and restart HA. But with HACS, updates are automatic — recommended.

**Q. How do I get updates?**
A. HACS → Integrations → "Send to myself on KakaoTalk Notify" card shows an **update available** badge when a new version exists. Click → download latest → restart HA. Your existing integration entry, automations, and tokens are preserved.

---

## Support

If you found this integration useful, a coffee donation is appreciated! 🙏

<table>
  <tr>
    <td align="center">
      <b>Toss (Korea)</b><br>
      <img src="https://raw.githubusercontent.com/redchupa/kakao-noti/main/images/toss-donation.png" width="200">
    </td>
    <td align="center">
      <b>PayPal</b><br>
      <img src="https://raw.githubusercontent.com/redchupa/kakao-noti/main/images/paypal-donation.png" width="200">
    </td>
  </tr>
</table>

---

## Help / Contact

- **Issues / bug reports**: <https://github.com/redchupa/kakao-noti/issues>
- **Discussion / questions**: <https://github.com/redchupa/kakao-noti/discussions>

---

## ⭐ Please star the repo — so others can find it

If this integration works for you, please **star** the GitHub repository.
More stars push it higher in GitHub search and the HACS catalog, helping **others discover this integration** more easily. It's a small action that helps the next person in Korea (or beyond) who needs KakaoTalk notifications find it faster.

### How to star

1. Go to <https://github.com/redchupa/kakao-noti> (same URL you registered in HACS)
2. **Sign in to GitHub** (free signup if needed: <https://github.com/signup> — if you use HACS, you already have one)
3. Click the **☆ Star** button at the **top right** → it turns into **★ Starred**
4. The star count increments ✨ — the next user will find this integration faster

---

## License

MIT License — [LICENSE](LICENSE)

---

**Found a bug or have an improvement idea? Let me know via GitHub Issues!**
