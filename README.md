# TempMail Bot

<p align="center">
  <img src="https://img.icons8.com/fluency/192/secured-letter.png" width="150" alt="TempMail Logo">
</p>

<h1 align="center">TempMail Bot</h1>

<p align="center">
  <b>سریع • ساده • کاربردی • دکمه‌ای</b>
</p>

<p align="center">
  ربات ایمیل موقت تلگرام با رابط کاربری کاملاً دکمه‌ای
</p>

<p align="center">
  <a href="https://t.me/meov2ray">
    <img src="https://img.shields.io/badge/Telegram-Channel-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram">
  </a>
  <a href="https://youtube.com/@meov2ray">
    <img src="https://img.shields.io/badge/YouTube-Channel-FF0000?style=for-the-badge&logo=youtube&logoColor=white" alt="YouTube">
  </a>
  <a href="https://t.me/arshannaebi">
    <img src="https://img.shields.io/badge/Support-Contact-00BFA5?style=for-the-badge&logo=telegram&logoColor=white" alt="Support">
  </a>
</p>

---

# 🇮🇷 راهنمای فارسی

## ✨ امکانات

* 📧 ساخت ایمیل موقت
* 📬 دریافت ایمیل‌های ورودی
* 🔄 بروزرسانی صندوق ورودی
* 🗑️ حذف ایمیل موقت
* 🔘 رابط کاربری کاملاً دکمه‌ای
* 🤖 استفاده از Inline Keyboard تلگرام
* ⚡ سریع و سبک
* ☁️ آماده برای Railway
* 📡 اتصال به Mail.tm API
* 👤 نشست جداگانه برای هر کاربر

---

## 🎛️ منوی ربات

```text
╔══════════════════════════════╗
║          📧 TempMail         ║
╠══════════════════════════════╣
║      📧 ساخت ایمیل جدید      ║
╠══════════════════════════════╣
║        📬 صندوق ورودی        ║
╠══════════════════════════════╣
║  🔄 بروزرسانی   │  🗑️ حذف    ║
╠══════════════════════════════╣
║           ℹ️ راهنما           ║
╚══════════════════════════════╝
```

تمام امکانات ربات از طریق دکمه‌های تلگرام قابل استفاده هستند و نیازی به تایپ دستورات پیچیده نیست.

---

## 📧 ساخت ایمیل موقت

برای ساخت یک ایمیل موقت، روی دکمه:

**📧 ساخت ایمیل جدید**

بزنید.

ربات به‌صورت خودکار یک آدرس ایمیل موقت ایجاد می‌کند.

---

## 📬 صندوق ورودی

بعد از ساخت ایمیل، با انتخاب:

**📬 صندوق ورودی**

می‌توانید ایمیل‌های دریافت‌شده را مشاهده کنید.

---

## 🔄 بروزرسانی

اگر منتظر دریافت ایمیل هستید، روی:

**🔄 بروزرسانی**

بزنید تا صندوق ورودی دوباره بررسی شود.

---

## 🗑️ حذف ایمیل

برای حذف ایمیل فعلی، روی:

**🗑️ حذف**

بزنید.

---

## ℹ️ راهنما

با انتخاب:

**ℹ️ راهنما**

می‌توانید توضیحات مربوط به امکانات ربات را مشاهده کنید.

---

## ⚠️ نکات مهم

ایمیل‌های موقت برای استفاده‌های کوتاه‌مدت ساخته شده‌اند.

برای موارد حساس مانند:

* 🏦 حساب‌های بانکی
* 💳 اطلاعات مالی
* 🔐 بازیابی حساب‌های مهم
* 📄 اطلاعات محرمانه
* 👤 حساب‌های شخصی مهم

از ایمیل موقت استفاده نکنید.

ممکن است ایمیل‌ها یا حساب‌های موقت توسط سرویس ارائه‌دهنده منقضی یا حذف شوند.

---

## 🚀 نصب

ابتدا Repository را دریافت کنید:

```bash
git clone https://github.com/adwiawda/TempMail.git
cd TempMail
```

سپس وابستگی‌ها را نصب کنید:

```bash
pip install -r requirements.txt
```

توکن ربات تلگرام را به‌عنوان Environment Variable قرار دهید:

```text
BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
```

و ربات را اجرا کنید:

```bash
python bot.py
```

---

## ☁️ نصب روی Railway

این پروژه برای Railway آماده شده است.

در قسمت **Variables** مقدار زیر را اضافه کنید:

```text
BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
```

دستور اجرا:

```bash
python bot.py
```

یا از `Procfile` استفاده کنید:

```text
worker: python bot.py
```

---

## 📁 ساختار پروژه

```text
TempMail/
│
├── bot.py
├── requirements.txt
├── Procfile
└── README.md
```

نیازی به فایل جداگانه برای لوگو نیست.

---

# 🇬🇧 English Guide

## ✨ Features

* 📧 Create temporary email addresses
* 📬 Receive incoming emails
* 🔄 Refresh inbox
* 🗑️ Delete temporary email
* 🔘 Fully button-based interface
* 🤖 Telegram Inline Keyboard
* ⚡ Fast and lightweight
* ☁️ Railway ready
* 📡 Mail.tm API integration
* 👤 Separate session for each user

---

## 🎛️ Bot Interface

```text
╔══════════════════════════════╗
║          📧 TempMail         ║
╠══════════════════════════════╣
║      📧 Create New Email     ║
╠══════════════════════════════╣
║           📬 Inbox           ║
╠══════════════════════════════╣
║  🔄 Refresh    │   🗑️ Delete  ║
╠══════════════════════════════╣
║            ℹ️ Help           ║
╚══════════════════════════════╝
```

Everything can be controlled using Telegram inline buttons.

---

## 📧 Create Temporary Email

Press:

**📧 Create New Email**

The bot will automatically generate a temporary email address.

---

## 📬 Inbox

Press:

**📬 Inbox**

to view received messages.

---

## 🔄 Refresh

If you are waiting for a new message, press:

**🔄 Refresh**

to check the inbox again.

---

## 🗑️ Delete Email

Press:

**🗑️ Delete**

to remove the current temporary email from the bot session.

---

## 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/adwiawda/TempMail.git
cd TempMail
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Set your Telegram Bot Token:

```text
BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
```

Run the bot:

```bash
python bot.py
```

---

## ☁️ Railway Deployment

The project is ready for Railway.

Add the following environment variable:

```text
BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
```

Start command:

```bash
python bot.py
```

Or use the included `Procfile`:

```text
worker: python bot.py
```

---

## 📁 Project Structure

```text
TempMail/
│
├── bot.py
├── requirements.txt
├── Procfile
└── README.md
```

No additional logo file is required.

---

## 🔐 Security

Never publish your Telegram Bot Token on GitHub.

Always use environment variables:

```text
BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
```

---

## 🛠️ Built With

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram">
  <img src="https://img.shields.io/badge/Mail.tm-API-6C63FF?style=for-the-badge" alt="Mail.tm">
  <img src="https://img.shields.io/badge/Railway-000000?style=for-the-badge&logo=railway&logoColor=white" alt="Railway">
</p>

---

## 📺 Community & Support

<p align="center">

<a href="https://t.me/meov2ray">
  <img src="https://img.shields.io/badge/Join%20Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram">
</a>

<a href="https://youtube.com/@meov2ray">
  <img src="https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white" alt="YouTube">
</a>

<a href="https://t.me/arshannaebi">
  <img src="https://img.shields.io/badge/Contact%20Support-00BFA5?style=for-the-badge&logo=telegram&logoColor=white" alt="Support">
</a>

</p>

---

## ⭐ Support

If you find this project useful, consider giving it a ⭐ on GitHub.

Your support helps with future updates and improvements.

---

## 📄 License

This project is provided for educational and development purposes.

Please use temporary email services responsibly and follow the terms of the services and APIs you use.

---

<p align="center">
  Made with ❤️ for Telegram
</p>

<p align="center">
  <b>TempMail Bot</b>
</p>
