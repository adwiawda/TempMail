import os
import re
import html
import asyncio
import logging
import aiohttp

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CopyTextButton,
    Update,
)
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

# =========================================================
# CONFIG
# =========================================================

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError(
        "BOT_TOKEN environment variable is missing."
    )

API_URL = "https://api.mail.tm"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)

# User temporary accounts
users = {}

# =========================================================
# API
# =========================================================


async def api_request(method, url, **kwargs):
    try:
        timeout = aiohttp.ClientTimeout(total=30)

        async with aiohttp.ClientSession(
            timeout=timeout
        ) as session:

            async with session.request(
                method,
                url,
                **kwargs
            ) as response:

                try:
                    data = await response.json(
                        content_type=None
                    )
                except Exception:
                    data = {}

                return response.status, data

    except Exception as e:
        logger.error("API request error: %s", e)
        return 0, {}


# =========================================================
# MAIL.TM
# =========================================================


async def get_domain():
    status, data = await api_request(
        "GET",
        f"{API_URL}/domains?page=1"
    )

    if status != 200:
        logger.error(
            "Failed to get domains. Status: %s",
            status
        )
        return None

    domains = data.get("hydra:member", [])

    if not domains:
        return None

    return domains[0].get("domain")


async def create_temp_mail():

    domain = await get_domain()

    if not domain:
        return None

    username = (
        "user"
        + os.urandom(8).hex()
    )

    email = f"{username}@{domain}"

    password = os.urandom(16).hex()

    # Create account
    status, data = await api_request(
        "POST",
        f"{API_URL}/accounts",
        json={
            "address": email,
            "password": password
        }
    )

    if status not in (200, 201):
        logger.error(
            "Account creation failed: %s",
            data
        )
        return None

    # Get authentication token
    status, token_data = await api_request(
        "POST",
        f"{API_URL}/token",
        json={
            "address": email,
            "password": password
        }
    )

    if status != 200:
        logger.error(
            "Token creation failed: %s",
            token_data
        )
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

    return data.get(
        "hydra:member",
        []
    )


async def get_message(token, message_id):

    status, data = await api_request(
        "GET",
        f"{API_URL}/messages/{message_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    if status != 200:
        return None

    return data


# =========================================================
# CODE EXTRACTION
# =========================================================


def extract_code(text):
    """
    Try to find verification codes.

    Examples:
    123456
    482913
    Your code is 123456
    GitHub code: 123456
    """

    if not text:
        return None

    # Normalize whitespace
    clean = re.sub(
        r"\s+",
        " ",
        text
    )

    # Common phrases first
    patterns = [

        # GitHub
        r"github.{0,80}?(\d{6})",

        # verification code
        r"verification code.{0,40}?(\d{4,8})",

        r"verify.{0,40}?(\d{4,8})",

        r"confirmation code.{0,40}?(\d{4,8})",

        r"security code.{0,40}?(\d{4,8})",

        r"one[- ]time password.{0,40}?(\d{4,8})",

        r"otp.{0,20}?(\d{4,8})",

        # Persian
        r"کد.{0,30}?(\d{4,8})",

        # Generic 6 digit code
        r"\b(\d{6})\b",

        # Generic 5 digit
        r"\b(\d{5})\b",

        # Generic 4 digit
        r"\b(\d{4})\b",

        # Generic 7/8 digit
        r"\b(\d{7,8})\b",
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            clean,
            re.IGNORECASE
        )

        if match:
            return match.group(1)

    return None


# =========================================================
# KEYBOARDS
# =========================================================


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


# =========================================================
# START
# =========================================================


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    text = (
        "📧 <b>Temp Mail Bot</b>\n\n"
        "به ربات ایمیل موقت خوش آمدید.\n\n"
        "با استفاده از این ربات می‌توانید "
        "یک ایمیل موقت بسازید و کدهای تأیید "
        "را دریافت کنید.\n\n"
        "👇 یکی از گزینه‌ها را انتخاب کنید:"
    )

    await update.message.reply_text(
        text,
        parse_mode="HTML",
        reply_markup=main_keyboard()
    )


# =========================================================
# CREATE EMAIL
# =========================================================


async def create_email(query):

    user_id = query.from_user.id

    await query.edit_message_text(
        "⏳ <b>در حال ساخت ایمیل موقت...</b>",
        parse_mode="HTML"
    )

    account = await create_temp_mail()

    if not account:

        await query.edit_message_text(
            "❌ <b>ساخت ایمیل ناموفق بود.</b>\n\n"
            "لطفاً چند ثانیه بعد دوباره تلاش کنید.",
            parse_mode="HTML",
            reply_markup=main_keyboard()
        )

        return

    users[user_id] = account

    text = (
        "✅ <b>ایمیل موقت ساخته شد!</b>\n\n"
        "📧 آدرس ایمیل:\n"
        f"<code>{html.escape(account['email'])}</code>\n\n"
        "📬 برای دریافت کد یا پیام، "
        "روی «صندوق ورودی» بزنید."
    )

    await query.edit_message_text(
        text,
        parse_mode="HTML",
        reply_markup=main_keyboard()
    )


# =========================================================
# INBOX
# =========================================================


async def show_inbox(query):

    user_id = query.from_user.id

    account = users.get(user_id)

    if not account:

        await query.edit_message_text(
            "❌ <b>هنوز ایمیلی نساختید.</b>\n\n"
            "ابتدا روی «ساخت ایمیل جدید» بزنید.",
            parse_mode="HTML",
            reply_markup=main_keyboard()
        )

        return

    await query.edit_message_text(
        "⏳ <b>در حال بررسی صندوق ورودی...</b>",
        parse_mode="HTML"
    )

    messages = await get_messages(
        account["token"]
    )

    if not messages:

        text = (
            "📬 <b>صندوق ورودی</b>\n\n"
            f"📧 <code>{html.escape(account['email'])}</code>\n\n"
            "📭 هنوز ایمیلی دریافت نشده است.\n\n"
            "اگر منتظر کد هستید، چند ثانیه صبر کنید "
            "و دوباره «بروزرسانی» را بزنید."
        )

        await query.edit_message_text(
            text,
            parse_mode="HTML",
            reply_markup=main_keyboard()
        )

        return

    # Show newest messages first
    messages = messages[:5]

    text_parts = [
        "📬 <b>صندوق ورودی</b>",
        "",
        f"📧 <code>{html.escape(account['email'])}</code>",
        ""
    ]

    copy_buttons = []

    for message in messages:

        message_id = message.get("id")

        full_message = await get_message(
            account["token"],
            message_id
        )

        if not full_message:
            full_message = message

        sender = full_message.get(
            "from",
            {}
        )

        sender_address = sender.get(
            "address",
            "نامشخص"
        )

        subject = full_message.get(
            "subject",
            "بدون موضوع"
        )

        intro = full_message.get(
            "intro",
            ""
        )

        text_body = full_message.get(
            "text",
            ""
        )

        # Mail.tm can sometimes provide HTML only
        html_body = full_message.get(
            "html",
            ""
        )

        if isinstance(html_body, list):
            html_body = "\n".join(
                str(x)
                for x in html_body
            )

        body = (
            text_body
            or intro
            or ""
        )

        # If no text body exists, strip basic HTML
        if not body and html_body:

            body = re.sub(
                r"<[^>]+>",
                " ",
                str(html_body)
            )

            body = html.unescape(body)

        body = body.strip()

        # Limit very long emails
        if len(body) > 1500:
            body = body[:1500] + "..."

        # Find verification code
        code = extract_code(
            f"{subject} {body}"
        )

        text_parts.append(
            "━━━━━━━━━━━━━━━━━━"
        )

        text_parts.append(
            f"✉️ <b>{html.escape(subject)}</b>"
        )

        text_parts.append(
            f"👤 <code>{html.escape(sender_address)}</code>"
        )

        if code:

            text_parts.append("")

            text_parts.append(
                f"🔐 <b>کد تأیید:</b> "
                f"<code>{html.escape(code)}</code>"
            )

            # Copy button
            copy_buttons.append(
                InlineKeyboardButton(
                    f"📋 کپی کد {code}",
                    copy_text=CopyTextButton(
                        text=code
                    )
                )
            )

        if body:

            # Clean excessive whitespace
            display_body = re.sub(
                r"\n{3,}",
                "\n\n",
                body
            )

            text_parts.append("")

            text_parts.append(
                "📝 <b>متن پیام:</b>"
            )

            text_parts.append(
                html.escape(display_body)
            )

    text = "\n".join(text_parts)

    # Telegram message limit protection
    if len(text) > 3900:

        text = text[:3900] + "\n\n..."

    keyboard = []

    # Add copy buttons
    for button in copy_buttons[:5]:

        keyboard.append(
            [button]
        )

    # Main buttons
    keyboard.extend([
        [
            InlineKeyboardButton(
                "🔄 بروزرسانی",
                callback_data="refresh"
            )
        ],
        [
            InlineKeyboardButton(
                "🗑 حذف ایمیل",
                callback_data="delete"
            ),
            InlineKeyboardButton(
                "🏠 منوی اصلی",
                callback_data="home"
            )
        ]
    ])

    await query.edit_message_text(
        text,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(
            keyboard
        )
    )


# =========================================================
# DELETE
# =========================================================


async def delete_email(query):

    user_id = query.from_user.id

    if user_id in users:

        del users[user_id]

        text = (
            "🗑 <b>ایمیل حذف شد.</b>\n\n"
            "می‌توانید یک ایمیل موقت جدید بسازید."
        )

    else:

        text = (
            "ℹ️ <b>ایمیلی برای حذف وجود ندارد.</b>"
        )

    await query.edit_message_text(
        text,
        parse_mode="HTML",
        reply_markup=main_keyboard()
    )


# =========================================================
# HELP
# =========================================================


async def show_help(query):

    text = (
        "ℹ️ <b>راهنمای ربات</b>\n\n"

        "📧 <b>ساخت ایمیل جدید</b>\n"
        "یک آدرس ایمیل موقت می‌سازد.\n\n"

        "📬 <b>صندوق ورودی</b>\n"
        "پیام‌های دریافت‌شده را نمایش می‌دهد.\n\n"

        "🔐 <b>کد تأیید</b>\n"
        "ربات تلاش می‌کند کدهای تأیید "
        "را به صورت خودکار پیدا کند.\n\n"

        "📋 <b>کپی کد</b>\n"
        "با زدن دکمه کپی، کد مستقیماً "
        "در کلیپ‌بورد شما قرار می‌گیرد.\n\n"

        "🔄 <b>بروزرسانی</b>\n"
        "صندوق ورودی را دوباره بررسی می‌کند.\n\n"

        "🗑 <b>حذف</b>\n"
        "ایمیل فعلی را از ربات حذف می‌کند."
    )

    await query.edit_message_text(
        text,
        parse_mode="HTML",
        reply_markup=main_keyboard()
    )


# =========================================================
# BUTTON HANDLER
# =========================================================


async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    try:

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

        elif query.data == "home":

            text = (
                "📧 <b>Temp Mail Bot</b>\n\n"
                "👇 یکی از گزینه‌ها را انتخاب کنید:"
            )

            await query.edit_message_text(
                text,
                parse_mode="HTML",
                reply_markup=main_keyboard()
            )

    except Exception as e:

        logger.exception(
            "Button handler error: %s",
            e
        )

        try:

            await query.edit_message_text(
                "❌ یک خطای موقت رخ داد.\n\n"
                "لطفاً دوباره تلاش کنید.",
                reply_markup=main_keyboard()
            )

        except Exception:
            pass


# =========================================================
# MAIN
# =========================================================


def main():

    application = (
        Application
        .builder()
        .token(BOT_TOKEN)
        .build()
    )

    application.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            button_handler
        )
    )

    logger.info(
        "TempMail Bot started..."
    )

    application.run_polling(
        drop_pending_updates=True
    )


if __name__ == "__main__":
    main()
