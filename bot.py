# bot.py
# जरूरी पैकेज इंस्टॉल करने के लिए:
# pip install python-telegram-bot --upgrade

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# ------------------ नया टोकन ------------------
TOKEN = "8737453745:AAGn-q8NkIcPTSqv-U82UNHiXMOzlYj9P0A"

# तुम्हारा वेबसाइट / मिनी ऐप URL
WEBAPP_URL = "https://ater-web-bot.vercel.app"

# लॉगिंग सेटअप
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# हर मैसेज / कमांड पर आने वाला रिस्पॉन्स
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    username = user.username or "User"

    # इनलाइन बटन
    keyboard = [
        [
            InlineKeyboardButton(
                "🔥 ATER INFO ऐप खोलें 🔥",
                web_app={"url": WEBAPP_URL}
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    # आकर्षक मैसेज
    text = (
        f"नमस्ते {user.first_name} जी! 👋\n\n"
        f"सारी जानकारी, नंबर, आधार, UPI, व्हीकल आदि सब कुछ एक जगह!\n"
        "नीचे बटन पर क्लिक करके ऐप खोलें और तुरंत इस्तेमाल शुरू करें 🚀"
    )

    # ग्रुप या प्राइवेट दोनों में काम करेगा
    await update.message.reply_text(
        text,
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )

def main() -> None:
    """बॉट शुरू करने का मुख्य फंक्शन"""
    application = Application.builder().token(TOKEN).build()

    # सभी कमांड्स और सभी टेक्स्ट मैसेज को हैंडल करेगा
    application.add_handler(MessageHandler(filters.TEXT | filters.COMMAND, handle_message))

    print("Bot started successfully! Press Ctrl+C to stop")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
