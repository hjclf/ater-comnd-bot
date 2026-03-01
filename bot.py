import logging
import os
import http.server
import socketserver
import threading
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# 1. Logging सेटअप
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# 2. टोकन और URL (सीधे कोड में या Environment Variables से)
TOKEN = "8737453745:AAFmPHK4ewfcFNuXg_8DfnaIHx7-n9a7sTg"
WEBAPP_URL = os.getenv("WEBAPP_URL", "https://ater-web-bot.vercel.app")

# 3. Render 'Port' एरर फिक्स करने के लिए छोटा सर्वर
def run_health_check_server():
    port = int(os.environ.get("PORT", 8080))
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Health check server running on port {port}")
        httpd.serve_forever()

# 4. बोट कमांड्स
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    keyboard = [
        [InlineKeyboardButton("🔥 ATER INFO ऐप खोलें 🔥", web_app={"url": WEBAPP_URL})],
        [InlineKeyboardButton("ℹ️ जानकारी के लिए क्लिक करें", web_app={"url": WEBAPP_URL})],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = f"नमस्ते {user.first_name}! 👋\n\nसारी जानकारी के लिए नीचे बटन दबाओ 👇"
    await update.message.reply_text(text, reply_markup=reply_markup)

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    pass

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error(msg="Exception:", exc_info=context.error)

# 5. मुख्य फंक्शन
def main() -> None:
    # पोर्ट सर्वर को अलग थ्रेड में चलाएं ताकि बोट न रुके
    threading.Thread(target=run_health_check_server, daemon=True).start()

    # बोट शुरू करें
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    
    # फिल्टर फिक्स (बिना बैकस्लैश के)
    text_no_command = filters.TEXT & (~filters.COMMAND)
    app.add_handler(MessageHandler(text_no_command, handle_text))
    
    app.add_error_handler(error_handler)

    print("Bot is starting...")
    app.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)

if __name__ == "__main__":
    main()
