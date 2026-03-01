# bot.py - Render फिक्स्ड वर्जन (no line continuation issues)

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
if not TOKEN:
    raise ValueError("BOT_TOKEN env var नहीं मिला! Render में डालो")

WEBAPP_URL = os.getenv("WEBAPP_URL", "https://ater-web-bot.vercel.app")

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
    pass  # spam avoid, कुछ मत भेजो

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error(msg="Exception:", exc_info=context.error)

def main() -> None:
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    # filters को अलग variable में डालकर issue avoid
    text_no_command = filters.TEXT & (\~filters.COMMAND)

    app.add_handler(
        MessageHandler(
            text_no_command,
            handle_text
        )
    )

    app.add_error_handler(error_handler)

    print("Bot started... Polling mode ON")
    app.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True
    )

if __name__ == "__main__":
    main()
