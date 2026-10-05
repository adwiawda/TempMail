import requests
import telebot
import time

import os
TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)
API = "https://api.mail.tm"

users = {}

def get_domain():
    r = requests.get(f"{API}/domains").json()
    return r["hydra:member"][0]["domain"]

def create_account():
    domain = get_domain()
    name = f"user{int(time.time())}"
    address = f"{name}@{domain}"
    password = "Temp123456!"
    r = requests.post(f"{API}/accounts", json={"address": address, "password": password})
    if r.status_code not in [200, 201]:
        return None, None
    r2 = requests.post(f"{API}/token", json={"address": address, "password": password}).json()
    token = r2["token"]
    return address, token

@bot.message_handler(commands=['start', 'new'])
def start(m):
    address, token = create_account()
    if not address:
        bot.send_message(m.chat.id, "خطا در ساخت ایمیل، دوباره تلاش کن.")
        return
    users[m.chat.id] = {"address": address, "token": token}
    bot.send_message(m.chat.id, f"ایمیل موقتت ساخته شد:\n`{address}`\n\nبرای دیدن پیام‌ها بفرست:\n/inbox", parse_mode="Markdown")

@bot.message_handler(commands=['inbox'])
def inbox(m):
    if m.chat.id not in users:
        bot.send_message(m.chat.id, "اول /start رو بزن.")
        return
    token = users[m.chat.id]["token"]
    h = {"Authorization": f"Bearer {token}"}
    r = requests.get(f"{API}/messages", headers=h).json()
    msgs = r.get("hydra:member", [])
    if not msgs:
        bot.send_message(m.chat.id, "هنوز ایمیلی نیومده.")
        return
    for msg in msgs[:5]:
        mid = msg["id"]
        d = requests.get(f"{API}/messages/{mid}", headers=h).json()
        text = f"از: {d.get('from', {}).get('address')}\nموضوع: {d.get('subject')}\n\n{d.get('text', '')[:2000]}"
        bot.send_message(m.chat.id, text)

print("ربات روشن شد...")
bot.infinity_polling()
