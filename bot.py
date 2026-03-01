# bot.py - Render Fixed Version
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

# Logging सेटअप
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Environment Variables प्राप्त करना
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("BOT_TOKEN environment variable नहीं मिला! कृपया Render Settings में इसे जोड़ें।")

WEBAPP_URL = os.getenv("WEBAPP_URL", "https://ater-web-bot.vercel.app")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    # बटन सेटअप
    keyboard = [
        [InlineKeyboardButton("🔥 ATER INFO ऐप खोलें 🔥", web_app={"url": WEBAPP_URL})],
        [InlineKeyboardButton("ℹ️ जानकारी के लिए क्लिक करें", web_app={"url": WEBAPP_URL})],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    text = f"नमस्ते {user.first_name}! 👋\n\nसारी जानकारी और फुल फीचर्स के लिए नीचे बटन दबाओ 👇\nMini App में सब कुछ एक क्लिक में!"

    await update.message.reply_text(text, reply_markup=reply_markup)

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # टेक्स्ट मैसेज आने पर कुछ नहीं करना (Spam रोकने के लिए)
    pass

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

def main() -> None:
    # एप्लीकेशन बनाएँ
    app = Application.builder().token(TOKEN).build()

    # कमांड हैंडलर जोड़ें
    app.add_handler(CommandHandler("start", start))

    # फिक्स्ड लाइन: यहाँ से बैकस्लैश (\) हटा दिया गया है
    text_no_command = filters.TEXT & (~filters.COMMAND)

    app.add_handler(
        MessageHandler(
            text_no_command,
            handle_text
        )
    )

    # एरर हैंडलर जोड़ें
    app.add_error_handler(error_handler)

    print("Bot started... Polling mode ON")
    
    # बॉट रन करें
    app.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True
    )

if __name__ == "__main__":
    main()
