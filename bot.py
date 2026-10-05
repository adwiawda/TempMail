import os
import asyncio
import logging
import aiohttp

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable is missing")

API_URL = "https://api.mail.tm"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# اطلاعات ایمیل موقت هر کاربر
users = {}


async def api_request(method, url, **kwargs):
    async with aiohttp.ClientSession() as session:
        async with session.request(method, url, **kwargs) as response:
            try:
                data = await response.json()
            except Exception:
                data = {}

            return response.status, data


async def get_domain():
    status, data = await api_request(
        "GET",
        f"{API_URL}/domains?page=1"
    )

    if status != 200:
        return None

    members = data.get("hydra:member", [])

    if not members:
        return None

    return members[0]["domain"]


async def create_temp_mail():
    domain = await get_domain()

    if not domain:
        return None

    username = f"user{os.urandom(5).hex()}"
    email = f"{username}@{domain}"
    password = os.urandom(12).hex()

    status, data = await api_request(
        "POST",
        f"{API_URL}/accounts",
        json={
            "address": email,
            "password": password
        }
    )

    if status not in (200, 201):
        return None

    status, token_data = await api_request(
        "POST",
        f"{API_URL}/token",
        json={
            "address": email,
            "password": password
        }
    )

    if status != 200:
        return None

    token = token_data.get("token")

    if not token:
        return None

    return {
        "email": email,
        "password": password,
        "token": token
    }


async def get_messages(token):
    status, data = await api_request(
        "GET",
        f"{API_URL}/messages",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    if status != 200:
        return []

    return data.get("hydra:member", [])


def main_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "📧 ساخت ایمیل جدید",
                callback_data="create"
            )
        ],
        [
            InlineKeyboardButton(
                "📬 صندوق ورودی",
                callback_data="inbox"
            )
        ],
        [
            InlineKeyboardButton(
                "🔄 بروزرسانی",
                callback_data="refresh"
            ),
            InlineKeyboardButton(
                "🗑 حذف",
                callback_data="delete"
            )
        ],
        [
            InlineKeyboardButton(
                "ℹ️ راهنما",
                callback_data="help"
            )
        ]
    ])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "📧 *Temp Mail Bot*\n\n"
        "به ربات ایمیل موقت خوش آمدید.\n\n"
        "از دکمه‌های زیر استفاده کنید:"
    )

    await update.message.reply_text(
        text,
        parse_mode="Markdown",
        reply_markup=main_keyboard()
    )


async def create_email(query):
    user_id = query.from_user.id

    await query.edit_message_text(
        "⏳ در حال ساخت ایمیل موقت..."
    )

    account = await create_temp_mail()

    if not account:
        await query.edit_message_text(
            "❌ ساخت ایمیل ناموفق بود.\n\n"
            "لطفاً چند لحظه بعد دوباره تلاش کنید.",
            reply_markup=main_keyboard()
        )
        return

    users[user_id] = account

    text = (
        "✅ *ایمیل موقت ساخته شد!*\n\n"
        f"📧 ایمیل:\n`{account['email']}`\n\n"
        "برای دریافت ایمیل‌های جدید، روی «صندوق ورودی» بزنید."
    )

    await query.edit_message_text(
        text,
        parse_mode="Markdown",
        reply_markup=main_keyboard()
    )


async def show_inbox(query):
    user_id = query.from_user.id

    account = users.get(user_id)

    if not account:
        await query.edit_message_text(
            "❌ هنوز ایمیل موقتی نساختید.",
            reply_markup=main_keyboard()
        )
        return

    messages = await get_messages(account["token"])

    if not messages:
        text = (
            "📬 *صندوق ورودی*\n\n"
            f"📧 `{account['email']}`\n\n"
            "📭 هنوز ایمیلی دریافت نشده است."
        )
    else:
        lines = [
            "📬 *صندوق ورودی*",
            "",
            f"📧 `{account['email']}`",
            ""
        ]

        for message in messages[:10]:
            sender = message.get("from", {})
            sender_address = sender.get("address", "نامشخص")
            subject = message.get("subject", "بدون موضوع")

            lines.append(
                f"✉️ *{subject}*\n"
                f"👤 {sender_address}"
            )

        text = "\n\n".join(lines)

    await query.edit_message_text(
        text,
        parse_mode="Markdown",
        reply_markup=main_keyboard()
    )


async def delete_email(query):
    user_id = query.from_user.id

    if user_id in users:
        del users[user_id]

        text = (
            "🗑 *ایمیل حذف شد.*\n\n"
            "می‌توانید یک ایمیل موقت جدید بسازید."
        )
    else:
        text = "ℹ️ ایمیلی برای حذف وجود ندارد."

    await query.edit_message_text(
        text,
        parse_mode="Markdown",
        reply_markup=main_keyboard()
    )


async def show_help(query):
    text = (
        "ℹ️ *راهنمای ربات*\n\n"
        "📧 ساخت ایمیل جدید\n"
        "یک آدرس ایمیل موقت ایجاد می‌کند.\n\n"
        "📬 صندوق ورودی\n"
        "ایمیل‌های دریافت‌شده را نمایش می‌دهد.\n\n"
        "🔄 بروزرسانی\n"
        "صندوق ورودی را دوباره بررسی می‌کند.\n\n"
        "🗑 حذف\n"
        "ایمیل فعلی را از ربات حذف می‌کند."
    )

    await query.edit_message_text(
        text,
        parse_mode="Markdown",
        reply_markup=main_keyboard()
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    await query.answer()

    if query.data == "create":
        await create_email(query)

    elif query.data == "inbox":
        await show_inbox(query)

    elif query.data == "refresh":
        await show_inbox(query)

    elif query.data == "delete":
        await delete_email(query)

    elif query.data == "help":
        await show_help(query)


def main():
    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .build()
    )

    application.add_handler(
        CommandHandler("start", start)
    )

    application.add_handler(
        CallbackQueryHandler(button_handler)
    )

    print("Bot started...")

    application.run_polling(
        drop_pending_updates=True
    )


if __name__ == "__main__":
    main()
