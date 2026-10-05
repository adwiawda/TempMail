# 📧 TempMail Bot

<p align="center">
  <img src="https://img.icons8.com/fluency/192/secured-letter.png" width="150" alt="TempMail Logo">
</p>

<h1 align="center">TempMail Bot</h1>

<p align="center">
  <b>Fast • Simple • Private • Button-Based</b>
</p>

<p align="center">
  A temporary email bot for Telegram powered by the Mail.tm API.
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
* 👤 Separate email session for each user

---

## 🎛️ Simple Interface

```text
╔══════════════════════════════╗
║          📧 TempMail         ║
╠══════════════════════════════╣
║      📧 Create New Email     ║
╠══════════════════════════════╣
║           📬 Inbox           ║
╠══════════════════════════════╣
║  🔄 Refresh    │   🗑 Delete  ║
╠══════════════════════════════╣
║            ℹ️ Help           ║
╚══════════════════════════════╝
```

Everything is controlled through Telegram's inline buttons.

---

## 🚀 Installation

### Clone the repository

```bash
git clone https://github.com/adwiawda/TempMail.git
cd TempMail
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Set your Bot Token

Linux / macOS:

```bash
export BOT_TOKEN="YOUR_TELEGRAM_BOT_TOKEN"
```

Windows PowerShell:

```powershell
$env:BOT_TOKEN="YOUR_TELEGRAM_BOT_TOKEN"
```

### Start the bot

```bash
python bot.py
```

---

## ☁️ Railway Deployment

The project is ready for deployment on Railway.

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

Never publish your Telegram Bot Token in your GitHub repository.

Use environment variables instead:

```text
BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
```

---

## 📬 How It Works

1. Start the Telegram bot.
2. Press **Create New Email**.
3. A temporary email address is generated.
4. Use the address wherever a temporary email is required.
5. Open **Inbox** to view received messages.
6. Press **Refresh** to check for new emails.
7. Press **Delete** when you are finished.

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
