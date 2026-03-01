# bot.py
# Telegram Mini App वाला बॉट - Render.com पर फ्री deploy के लिए

import logging
import os

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# लॉगिंग सेटअप
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Environment variables से टोकन लो (Render पर Environment Variable में डालना)
TOKEN = os.getenv("BOT_TOKEN")
WEBAPP_URL = os.getenv("WEBAPP_URL", "https://ater-web-bot.vercel.app")  # डिफॉल्ट वैल्यू

if not TOKEN:
    raise ValueError("BOT_TOKEN environment variable नहीं मिला! Render dashboard में Environment → Add Variable करो")

# /start कमांड हैंडलर
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    
    keyboard = [
        [
            InlineKeyboardButton(
                "🔥 ATER INFO ऐप खोलें 🔥",
                web_app={"url": WEBAPP_URL}
            )
        ],
        [
            InlineKeyboardButton(
                "ℹ️ जानकारी के लिए क्लिक करें",
                web_app={"url": WEBAPP_URL}
            )
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = (
        f"नमस्ते {user.first_name}! 👋\n\n"
        "सारी जानकारी और फुल फीचर्स के लिए नीचे बटन दबाओ 👇\n"
        "Mini App में सब कुछ एक क्लिक में!"
    )
    
    await update.message.reply_text(text, reply_markup=reply_markup)


# बाकी टेक्स्ट मैसेज हैंडलर (कमांड छोड़कर)
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # अगर चाहो तो कुछ मैसेज भेजो, वरना चुप रहो (spam avoid करने के लिए)
    # await update.message.reply_text("कृपया /start यूज करो या बटन दबाओ 😊")
    pass  # अभी कुछ नहीं भेज रहा


# एरर हैंडलर (जरूरी Render logs के लिए)
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error("Update caused error:", exc_info=context.error)


def main() -> None:
    application = Application.builder().token(TOKEN).build()

    # हैंडलर्स ऐड करो
    application.add_handler(CommandHandler("start", start))
    
    # टेक्स्ट मैसेज (कमांड छोड़कर)
    application.add_handler(
        MessageHandler(
            filters.TEXT & \~filters.COMMAND,
            handle_text
        )
    )

    # एरर हैंडलिंग
    application.add_error_handler(error_handler)

    print("Bot started... Running in polling mode")
    application.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True  # restart पर पुराने मैसेज ignore
    )


if __name__ == "__main__":
    main()
