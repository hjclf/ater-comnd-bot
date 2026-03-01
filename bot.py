import logging
import os
from dotenv import load_dotenv

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# ------------------ लोडिंग ------------------
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
WEBAPP_URL = "https://ater-web-bot.vercel.app"

if not TOKEN:
    raise ValueError("BOT_TOKEN .env में नहीं मिला!")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ------------------ हैंडलर ------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    keyboard = [
        [InlineKeyboardButton("🔥 ATER INFO ऐप खोलें 🔥", web_app={"url": WEBAPP_URL})],
        [InlineKeyboardButton("ℹ️ जानकारी के लिए क्लिक करें", web_app={"url": WEBAPP_URL})],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    text = (
        f"नमस्ते {user.first_name}! 👋\n\n"
        "सारी जानकारी और फुल फीचर्स के लिए नीचे बटन दबाओ 👇\n"
        "Mini App में सब कुछ एक क्लिक में!"
    )

    await update.message.reply_text(text, reply_markup=reply_markup)


async def handle_random_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # अगर चाहो तो कुछ मैसेज भेज सकते हो, या बिल्कुल चुप रह सकते हो
    # await update.message.reply_text("कृपया /start कमांड यूज करें 😊")
    pass  # या हल्का सा मैसेज


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error("Exception while handling an update:", exc_info=context.error)


def main() -> None:
    application = Application.builder().token(TOKEN).build()

    # कमांड
    application.add_handler(CommandHandler("start", start))

    # बाकी सारे टेक्स्ट मैसेज (कमांड छोड़कर)
    application.add_handler(MessageHandler(filters.TEXT & \~filters.COMMAND, handle_random_text))

    # एरर हैंडलिंग
    application.add_error_handler(error_handler)

    print("Bot started... Press Ctrl+C to stop")
    application.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True   # बहुत जरूरी
    )


if __name__ == "__main__":
    main()
