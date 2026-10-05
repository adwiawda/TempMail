import os
import re
import html
import imaplib
import email
import logging
from email.header import decode_header

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CopyTextButton,
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# =========================
# SETTINGS
# =========================

BOT_TOKEN = os.getenv("BOT_TOKEN")
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")

IMAP_SERVER = "imap.gmail.com"

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is missing")

if not EMAIL_ADDRESS:
    raise RuntimeError("EMAIL_ADDRESS is missing")

if not EMAIL_APP_PASSWORD:
    raise RuntimeError("EMAIL_APP_PASSWORD is missing")


logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


# =========================
# TELEGRAM MENU
# =========================

def main_keyboard():
    return InlineKeyboardMarkup([
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
            )
        ],
        [
            InlineKeyboardButton(
                "ℹ️ راهنما",
                callback_data="help"
            )
        ]
    ])


# =========================
# GMAIL
# =========================

def decode_text(value):
    if not value:
        return ""

    parts = decode_header(value)
    result = ""

    for part, encoding in parts:
        if isinstance(part, bytes):
            try:
                result += part.decode(
                    encoding or "utf-8",
                    errors="ignore"
                )
            except Exception:
                result += part.decode(
                    "utf-8",
                    errors="ignore"
                )
        else:
            result += part

    return result


def get_body(msg):
    text = ""

    if msg.is_multipart():

        for part in msg.walk():

            content_type = part.get_content_type()
            disposition = str(
                part.get("Content-Disposition", "")
            )

            if "attachment" in disposition:
                continue

            if content_type == "text/plain":

                try:
                    payload = part.get_payload(
                        decode=True
                    )

                    if payload:
                        text += payload.decode(
                            part.get_content_charset()
                            or "utf-8",
                            errors="ignore"
                        )
                except Exception:
                    pass

    else:

        try:
            payload = msg.get_payload(
                decode=True
            )

            if payload:
                text = payload.decode(
                    msg.get_content_charset()
                    or "utf-8",
                    errors="ignore"
                )

        except Exception:
            pass

    if not text:

        html_parts = []

        if msg.is_multipart():

            for part in msg.walk():

                if part.get_content_type() == "text/html":

                    try:
                        payload = part.get_payload(
                            decode=True
                        )

                        if payload:
                            html_parts.append(
                                payload.decode(
                                    part.get_content_charset()
                                    or "utf-8",
                                    errors="ignore"
                                )
                            )
                    except Exception:
                        pass

        else:

            if msg.get_content_type() == "text/html":

                try:
                    payload = msg.get_payload(
                        decode=True
                    )

                    if payload:
                        html_parts.append(
                            payload.decode(
                                msg.get_content_charset()
                                or "utf-8",
                                errors="ignore"
                            )
                        )
                except Exception:
                    pass

        if html_parts:

            text = "\n".join(html_parts)

            text = re.sub(
                r"<[^>]+>",
                " ",
                text
            )

            text = html.unescape(text)

    return text.strip()


def extract_code(text):
    if not text:
        return None

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    patterns = [
        r"github.{0,100}?(\d{6})",
        r"verification code.{0,60}?(\d{4,8})",
        r"verify.{0,60}?(\d{4,8})",
        r"confirmation code.{0,60}?(\d{4,8})",
        r"security code.{0,60}?(\d{4,8})",
        r"one[- ]time password.{0,60}?(\d{4,8})",
        r"otp.{0,30}?(\d{4,8})",
        r"کد.{0,40}?(\d{4,8})",
        r"\b(\d{6})\b",
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            return match.group(1)

    return None


def read_gmail():

    mail = None

    try:

        mail = imaplib.IMAP4_SSL(
            IMAP_SERVER,
            993
        )

        mail.login(
            EMAIL_ADDRESS,
            EMAIL_APP_PASSWORD
        )

        mail.select("INBOX")

        status, data = mail.search(
            None,
            "ALL"
        )

        if status != "OK":
            return []

        message_ids = data[0].split()

        # newest first
        message_ids = message_ids[-10:]
        message_ids.reverse()

        messages = []

        for message_id in message_ids:

            status, msg_data = mail.fetch(
                message_id,
                "(RFC822)"
            )

            if status != "OK":
                continue

            raw_email = None

            for item in msg_data:

                if isinstance(item, tuple):

                    raw_email = item[1]
                    break

            if not raw_email:
                continue

            msg = email.message_from_bytes(
                raw_email
            )

            subject = decode_text(
                msg.get("Subject", "")
            )

            sender = decode_text(
                msg.get("From", "")
            )

            body = get_body(msg)

            code = extract_code(
                subject + " " + body
            )

            messages.append({
                "subject": subject,
                "sender": sender,
                "body": body,
                "code": code,
            })

        mail.close()
        mail.logout()

        return messages

    except Exception as e:

        logger.exception(
            "Gmail error: %s",
            e
        )

        if mail:

            try:
                mail.logout()
            except Exception:
                pass

        return None


# =========================
# START
# =========================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    text = (
        "📧 <b>TempMail Bot</b>\n\n"
        "ربات آماده است.\n\n"
        "ایمیل‌های دریافتی Gmail را "
        "بررسی می‌کنم و در صورت وجود "
        "کد تأیید، آن را پیدا می‌کنم.\n\n"
        "👇"
    )

    await update.message.reply_text(
        text,
        parse_mode="HTML",
        reply_markup=main_keyboard()
    )


# =========================
# INBOX
# =========================

async def show_inbox(query):

    await query.edit_message_text(
        "⏳ <b>در حال بررسی Gmail...</b>",
        parse_mode="HTML"
    )

    messages = read_gmail()

    if messages is None:

        await query.edit_message_text(
            "❌ <b>اتصال به Gmail ناموفق بود.</b>\n\n"
            "Variables و App Password را بررسی کن.",
            parse_mode="HTML",
            reply_markup=main_keyboard()
        )

        return

    if not messages:

        await query.edit_message_text(
            "📭 <b>صندوق ورودی خالی است.</b>\n\n"
            "ایمیل جدیدی دریافت نشده.",
            parse_mode="HTML",
            reply_markup=main_keyboard()
        )

        return

    parts = [
        "📬 <b>صندوق ورودی</b>",
        ""
    ]

    keyboard = []

    for index, message in enumerate(messages[:5]):

        subject = message["subject"] or "بدون موضوع"
        sender = message["sender"] or "نامشخص"
        body = message["body"]
        code = message["code"]

        parts.append(
            "━━━━━━━━━━━━━━━━"
        )

        parts.append(
            f"✉️ <b>{html.escape(subject)}</b>"
        )

        parts.append(
            f"👤 <code>{html.escape(sender)}</code>"
        )

        if code:

            parts.append("")

            parts.append(
                f"🔐 <b>کد:</b> "
                f"<code>{html.escape(code)}</code>"
            )

            keyboard.append([
                InlineKeyboardButton(
                    f"📋 کپی {code}",
                    copy_text=CopyTextButton(
                        text=code
                    )
                )
            ])

        if body:

            clean_body = body[:800]

            parts.append("")

            parts.append(
                "📝 <b>متن:</b>"
            )

            parts.append(
                html.escape(clean_body)
            )

    keyboard.extend([
        [
            InlineKeyboardButton(
                "🔄 بروزرسانی",
                callback_data="refresh"
            )
        ],
        [
            InlineKeyboardButton(
                "ℹ️ راهنما",
                callback_data="help"
            )
        ]
    ])

    text = "\n".join(parts)

    if len(text) > 3900:
        text = text[:3900] + "\n..."

    await query.edit_message_text(
        text,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(
            keyboard
        )
    )


# =========================
# HELP
# =========================

async def show_help(query):

    text = (
        "ℹ️ <b>راهنما</b>\n\n"
        "📬 صندوق ورودی\n"
        "ایمیل‌های Gmail را بررسی می‌کند.\n\n"
        "🔐 کد تأیید\n"
        "ربات کدهای عددی موجود در "
        "ایمیل را تشخیص می‌دهد.\n\n"
        "📋 کپی\n"
        "با زدن دکمه کپی، کد را "
        "مستقیماً کپی می‌کنید."
    )

    await query.edit_message_text(
        text,
        parse_mode="HTML",
        reply_markup=main_keyboard()
    )


# =========================
# BUTTONS
# =========================

async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    if query.data in ("inbox", "refresh"):
        await show_inbox(query)

    elif query.data == "help":
        await show_help(query)


# =========================
# MAIN
# =========================

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
        "Bot started successfully"
    )

    application.run_polling(
        drop_pending_updates=True
    )


if __name__ == "__main__":
    main()
