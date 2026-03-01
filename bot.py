# bot.py - Render पर काम करने वाला क्लीन वर्जन

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

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("BOT_TOKEN")
WEBAPP_URL = os.getenv("WEBAPP_URL", "https://ater-web-bot.vercel.app")

if not TOKEN:
    raise ValueError("BOT_TOKEN environment variable नहीं मिला!")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    keyboard = [
        [InlineKeyboardButton("🔥 ATER INFO ऐप खोलें 🔥", web_app={"url": WEBAPP_URL})],
        [InlineKeyboardButton("ℹ️ जानकारी के लिए क्लिक करें", web_app={"url": WEBAPP_URL})],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    text = f"नमस्ते {user.first_name}! 👋\n\nसारी जानकारी और फुल फीचर्स के लिए नीचे बटन दबाओ 👇\nMini App में सब कुछ एक क्लिक में!"

    await update.message.reply_text(text, reply_markup=reply_markup)

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # अभी कुछ नहीं, spam avoid के लिए
    pass

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error("Error occurred:", exc_info=context.error)

def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))

    # ये लाइन पहले क्रैश कर रही थी - अब parentheses में सेफ
    application.add_handler(
        MessageHandler(
            filters.TEXT & \~filters.COMMAND,
            handle_text
        )
    )

    application.add_error_handler(error_handler)

    print("Bot started... Running in polling mode")
    application.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True
    )

if __name__ == "__main__":
    main()
