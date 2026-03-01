# bot.py
# Render पर होस्ट करने के लिए जरूरी पैकेज: python-telegram-bot==20.7
# GitHub में requirements.txt में लिखना: python-telegram-bot==20.7

import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# ------------------ नया टोकन ------------------
TOKEN = "8726912419:AAGPKnKRpweDu6fwYfXXc7oe5pYKNLZWcqc"

# तुम्हारा वेबसाइट URL (Mini App)
WEBAPP_URL = "https://ater-web-bot.vercel.app"

# स्पेसिफिक ग्रुप का Chat ID (यहां अपना ID डालें, जैसे -1001234567890)
GROUP_ID = -1002581209098  # <--- यहां चेंज करें! पहले बताए स्टेप से ID निकालें

# लॉगिंग सेटअप (Render logs में दिखेगा)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# हर मैसेज / कमांड पर रिस्पॉन्स (सिर्फ स्पेसिफिक ग्रुप में)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat = update.message.chat
    # चेक: सिर्फ ग्रुप/सुपरग्रुप में, और स्पेसिफिक ID मैच करे
    if chat.type not in ['group', 'supergroup'] or chat.id != GROUP_ID:
        return  # अगर नहीं मैच, तो इग्नोर करो (ना रिस्पॉन्स)

    user = update.effective_user
    first_name = user.first_name or "दोस्त"

    # इनलाइन बटन (web_app टाइप — क्लिक पर Mini App खुलेगा)
    keyboard = [
        [
            InlineKeyboardButton(
                "🔥 ATER INFO ऐप खोलें 🔥",
                web_app={"url": WEBAPP_URL}
            )
        ],
        [
            InlineKeyboardButton(
                "ℹ️ पूरी जानकारी देखें",
                web_app={"url": WEBAPP_URL}
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    # आकर्षक मैसेज
    text = (
        f"नमस्ते {first_name} जी! 👋\n\n"
        "नंबर, आधार, UPI, व्हीकल, और सारी जानकारी एक जगह! 🚀\n"
        "नीचे बटन दबाकर ऐप खोलो और तुरंत इस्तेमाल शुरू करो!"
    )

    # अब सिर्फ स्पेसिफिक ग्रुप में रिस्पॉन्स देगा
    await update.message.reply_text(
        text,
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )

def main() -> None:
    """बॉट शुरू करने का मुख्य फंक्शन"""
    # Render पर event loop एरर फिक्स के लिए
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    application = Application.builder().token(TOKEN).build()

    # सभी टेक्स्ट मैसेज (कमांड्स सहित) को हैंडल करेगा
    application.add_handler(MessageHandler(filters.TEXT, handle_message))

    print("Bot started successfully! Waiting for messages...")
    logger.info("Bot is running...")

    # Polling शुरू
    application.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True  # पुराने मैसेज इग्नोर करेगा
    )

if __name__ == "__main__":
    main()
