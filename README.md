# 📧 TempMail Bot

<p align="center">
  <img src="https://img.icons8.com/fluency/192/secured-letter.png" width="140" alt="TempMail Logo">
</p>

<p align="center">
  <b>ربات ایمیل موقت سریع و ساده با Mail.tm</b>
</p>

<p align="center">
  <a href="https://t.me/meov2ray">📢 Telegram</a> •
  <a href="https://youtube.com/@meov2ray">▶️ YouTube</a> •
  <a href="https://t.me/arshannaebi">💬 Support</a>
</p>

---

# 🇮🇷 راهنمای فارسی

## 📖 درباره پروژه

**TempMail Bot** یک ربات تلگرامی برای ساخت ایمیل موقت است که از API سرویس **Mail.tm** استفاده می‌کند.

با این ربات می‌توانید بدون ساخت حساب دائمی، یک آدرس ایمیل موقت ایجاد کنید و پیام‌های دریافتی آن را داخل تلگرام مشاهده کنید.

## ✨ امکانات

* 📧 ساخت ایمیل موقت
* 📬 مشاهده صندوق ورودی
* 🔄 بروزرسانی صندوق ورودی
* 🗑 حذف ایمیل فعلی
* ℹ️ راهنمای داخلی ربات
* ⚡ استفاده از API سرویس Mail.tm
* 🤖 دارای دکمه‌های Inline
* ☁️ مناسب برای Deploy روی Railway
* 🔐 استفاده از Environment Variable برای Bot Token

## 🎛 منوی ربات

| دکمه               | عملکرد                   |
| ------------------ | ------------------------ |
| 📧 ساخت ایمیل جدید | ساخت یک ایمیل موقت جدید  |
| 📬 صندوق ورودی     | مشاهده ایمیل‌های دریافتی |
| 🔄 بروزرسانی       | بررسی دوباره صندوق ورودی |
| 🗑 حذف             | حذف ایمیل فعلی از ربات   |
| ℹ️ راهنما          | نمایش راهنمای استفاده    |

## 🚀 نصب و اجرا

### 1. دریافت پروژه

```bash
git clone https://github.com/adwiawda/TempMail.git
cd TempMail
```

### 2. نصب وابستگی‌ها

```bash
pip install -r requirements.txt
```

### 3. تنظیم Bot Token

متغیر محیطی زیر را تنظیم کنید:

```text
BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
```

**نکته:** توکن واقعی ربات را داخل `bot.py` یا GitHub قرار ندهید.

### 4. اجرای ربات

```bash
python bot.py
```

---

# ☁️ Deploy روی Railway

این پروژه برای اجرای Worker روی Railway آماده شده است.

ساختار اصلی پروژه باید به شکل زیر باشد:

```text
TempMail/
├── bot.py
├── requirements.txt
├── Procfile
└── README.md
```

### requirements.txt

```text
python-telegram-bot==22.5
aiohttp==3.12.15
```

### Procfile

```text
worker: python bot.py
```

### متغیر محیطی Railway

در Railway یک Variable با نام زیر ایجاد کنید:

```text
BOT_TOKEN
```

و مقدار آن را برابر توکن ربات تلگرام خود قرار دهید.

سپس پروژه را Deploy کنید.

---

## ⚠️ نکات مهم

* فایل باید دقیقاً `requirements.txt` نام داشته باشد.
* فایل نباید `Requirements (1).txt` یا `requirements.txt.txt` باشد.
* فایل `Procfile` نیز باید دقیقاً همین نام را داشته باشد.
* `BOT_TOKEN` را در GitHub Commit نکنید.
* در صورت لو رفتن توکن، آن را از طریق BotFather تغییر دهید.

---

## 🛠 تکنولوژی‌ها

* Python
* python-telegram-bot
* aiohttp
* Mail.tm API
* Railway
* Telegram Bot API

---

# 🇬🇧 English Guide

## 📖 About

**TempMail Bot** is a simple Telegram temporary email bot powered by the **Mail.tm API**.

It allows users to create temporary email addresses and check received messages directly from Telegram.

## ✨ Features

* 📧 Create temporary email addresses
* 📬 Check inbox
* 🔄 Refresh inbox
* 🗑 Delete current email
* ℹ️ Built-in help
* ⚡ Mail.tm API integration
* 🤖 Inline Telegram buttons
* ☁️ Railway deployment support
* 🔐 Secure environment variable configuration

## 🎛 Bot Menu

| Button              | Function                      |
| ------------------- | ----------------------------- |
| 📧 Create New Email | Creates a new temporary email |
| 📬 Inbox            | Shows received messages       |
| 🔄 Refresh          | Refreshes the inbox           |
| 🗑 Delete           | Removes the current email     |
| ℹ️ Help             | Shows the bot guide           |

## 🚀 Local Installation

### 1. Clone the repository

```bash
git clone https://github.com/adwiawda/TempMail.git
cd TempMail
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set your Bot Token

Create an environment variable:

```text
BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
```

Never put your real bot token directly inside the source code.

### 4. Run the bot

```bash
python bot.py
```

---

# ☁️ Railway Deployment

The project is designed to run as a Railway Worker.

Required project structure:

```text
TempMail/
├── bot.py
├── requirements.txt
├── Procfile
└── README.md
```

### requirements.txt

```text
python-telegram-bot==22.5
aiohttp==3.12.15
```

### Procfile

```text
worker: python bot.py
```

### Railway Environment Variable

Add the following variable in Railway:

```text
BOT_TOKEN
```

Set its value to your Telegram bot token.

Then deploy the project.

---

## ⚠️ Important

Make sure the dependency file is named exactly:

```text
requirements.txt
```

Not:

```text
Requirements (1).txt
requirements.txt.txt
```

The process file must also be named exactly:

```text
Procfile
```

Do not commit your real Telegram bot token to GitHub.

---

## 🛠 Built With

* Python
* python-telegram-bot
* aiohttp
* Mail.tm API
* Railway
* Telegram Bot API

---

## 🔗 Community & Support

📢 **Telegram:**
https://t.me/meov2ray

▶️ **YouTube:**
https://youtube.com/@meov2ray

💬 **Support:**
https://t.me/arshannaebi

---

## 📄 License

This project is provided for educational and personal use.

---

<p align="center">
  Made with ❤️ for Telegram
</p>
