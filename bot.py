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

# 1. Logging सेटअप (एरर देखने के लिए)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# 2. टोकन और URL सेटअप
# नोट: सुरक्षा के लिए Render के Environment Variables में BOT_TOKEN डालना बेहतर है
TOKEN = "8737453745:AAFmPHK4ewfcFNuXg_8DfnaIHx7-n9a7sTg"
WEBAPP_URL = os.getenv("WEBAPP_URL", "https://ater-web-bot.vercel.app")

# 3. Render 'No open ports' एरर फिक्स करने के लिए छोटा सर्वर
def run_health_check_server():
    try:
        port = int(os.environ.get("PORT", 8080))
        handler = http.server.SimpleHTTPRequestHandler
        with socketserver.TCPServer(("", port), handler) as httpd:
            print(f"Health check server running on port {port}")
            httpd.serve_forever()
    except Exception as e:
        print(f"Server Error: {e}")

# 4. बोट कमांड्स
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
    # टेक्स्ट मैसेज आने पर रिस्पॉन्स (वैकल्पिक)
    pass

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

# 5. मुख्य फंक्शन (Main Function)
def main() -> None:
    # पोर्ट सर्वर को अलग थ्रेड में चलाएं ताकि Render सर्विस को 'Live' माने
    threading.Thread(target=run_health_check_server, daemon=True).start()

    # एप्लीकेशन बनाएँ
    app = Application.builder().token(TOKEN).build()

    # कमांड हैंडलर जोड़ें
    app.add_handler(CommandHandler("start", start))

    # फ़िल्टर फिक्स: यहाँ से बैकस्लैश (\) हटा दिया गया है
    text_no_command = filters.TEXT & (~filters.COMMAND)
    app.add_handler(MessageHandler(text_no_command, handle_text))

    # एरर हैंडलर जोड़ें
    app.add_error_handler(error_handler)

    print("Bot is starting... polling updates...")
    
    # बॉट रन करें (पुराने पेंडिंग मैसेज हटाकर)
    app.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True
    )

if __name__ == "__main__":
    main()
