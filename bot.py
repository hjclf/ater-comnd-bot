# bot.py
import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters, ContextTypes

TOKEN = "8726912419:AAGPKnKRpweDu6fwYfXXc7oe5pYKNLZWcqc"
WEBAPP_URL = "https://ater-web-bot.vercel.app"

# ←←← अपना ग्रुप ID यहां डालें (पहले बताए स्टेप से निकालें)
GROUP_ID = -1002581209098   # ←←← जरूर चेंज करें!

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat = update.message.chat
    if chat.type not in ['group', 'supergroup'] or chat.id != GROUP_ID:
        return   # दूसरे ग्रुप/प्राइवेट में कुछ नहीं करेगा

    user = update.effective_user
    first_name = user.first_name or "दोस्त"

    keyboard = [
        [InlineKeyboardButton("🔥 ATER INFO ऐप खोलें 🔥", url=WEBAPP_URL)],
        [InlineKeyboardButton("ℹ️ पूरी जानकारी देखें", url=WEBAPP_URL)]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    text = (
        f"नमस्ते {first_name} जी! 👋\n\n"
        "नंबर, आधार, UPI, व्हीकल, और सारी जानकारी एक जगह! 🚀\n"
        "नीचे बटन दबाकर ऐप खोलो!"
    )

    await update.message.reply_text(
        text,
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )

def main() -> None:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    application = Application.builder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT, handle_message))

    print("Bot started successfully!")
    logger.info("Bot is running...")

    application.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True
    )

if __name__ == "__main__":
    main()
