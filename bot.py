import html
import os
import time

import requests
import telebot

TOKEN = os.getenv("TOKEN")
API = "https://api.mail.tm"

if not TOKEN:
    raise RuntimeError("TOKEN environment variable is not set")

bot = telebot.TeleBot(TOKEN)
users = {}


def api_request(method, url, **kwargs):
    kwargs.setdefault("timeout", 20)
    response = requests.request(method, url, **kwargs)
    response.raise_for_status()
    return response


def get_domain():
    data = api_request("GET", f"{API}/domains").json()
    domains = data.get("hydra:member", [])

    if not domains:
        raise RuntimeError("No mail.tm domains available")

    return domains[0]["domain"]


def create_account():
    domain = get_domain()

    # زمان میلی‌ثانیه‌ای برای جلوگیری از تکراری شدن آدرس
    name = f"user{int(time.time() * 1000)}"
    address = f"{name}@{domain}"

    password = f"Temp{int(time.time() * 1000)}Mail!"

    response = requests.post(
        f"{API}/accounts",
        json={
            "address": address,
            "password": password,
        },
        timeout=20,
    )

    if response.status_code not in (200, 201):
        return None, None

    token_response = requests.post(
        f"{API}/token",
        json={
            "address": address,
            "password": password,
        },
        timeout=20,
    )

    token_response.raise_for_status()

    token = token_response.json().get("token")

    if not token:
        return None, None

    return address, token


@bot.message_handler(commands=["start", "new"])
def start(message):
    try:
        address, token = create_account()
    except (requests.RequestException, ValueError, KeyError, RuntimeError):
        address, token = None, None

    if not address or not token:
        bot.send_message(
            message.chat.id,
            "خطا در ساخت ایمیل. چند لحظه بعد دوباره تلاش کن."
        )
        return

    users[message.chat.id] = {
        "address": address,
        "token": token,
    }

    bot.send_message(
        message.chat.id,
        f"ایمیل موقتت ساخته شد:\n"
        f"<code>{html.escape(address)}</code>\n\n"
        f"برای دیدن پیام‌ها بفرست:\n/inbox",
        parse_mode="HTML",
    )


@bot.message_handler(commands=["inbox"])
def inbox(message):
    user = users.get(message.chat.id)

    if not user:
        bot.send_message(
            message.chat.id,
            "اول /start رو بزن."
        )
        return

    headers = {
        "Authorization": f"Bearer {user['token']}"
    }

    try:
        response = api_request(
            "GET",
            f"{API}/messages",
            headers=headers,
        )

        messages = response.json().get(
            "hydra:member",
            []
        )

    except (requests.RequestException, ValueError):
        bot.send_message(
            message.chat.id,
            "خطا در دریافت ایمیل‌ها. دوباره تلاش کن."
        )
        return

    if not messages:
        bot.send_message(
            message.chat.id,
            "هنوز ایمیلی نیومده."
        )
        return

    for msg in messages[:5]:
        message_id = msg.get("id")

        if not message_id:
            continue

        try:
            detail = api_request(
                "GET",
                f"{API}/messages/{message_id}",
                headers=headers,
            ).json()

        except (requests.RequestException, ValueError):
            continue

        sender = detail.get(
            "from", {}
        ).get(
            "address",
            "نامشخص"
        )

        subject = detail.get(
            "subject",
            "بدون موضوع"
        )

        body = (
            detail.get("text")
            or detail.get("html")
            or ""
        )

        body = str(body)[:2000]

        text = (
            f"<b>از:</b> {html.escape(str(sender))}\n"
            f"<b>موضوع:</b> {html.escape(str(subject))}\n\n"
            f"{html.escape(body)}"
        )

        bot.send_message(
            message.chat.id,
            text,
            parse_mode="HTML",
        )


if __name__ == "__main__":
    print("ربات روشن شد...", flush=True)

    bot.infinity_polling(
        skip_pending=True,
        timeout=30,
        long_polling_timeout=30,
    )
