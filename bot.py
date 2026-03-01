# bot.py
import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, CallbackQueryHandler, filters, ContextTypes

TOKEN = "8726912419:AAGPKnKRpweDu6fwYfXXc7oe5pYKNLZWcqc"
WEBAPP_URL = "https://ater-web-bot.vercel.app"

# ←←← अपना ग्रुप ID यहां डालें
GROUP_ID = -1002581209098

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

    # बटन callback_data के साथ (क्लिक पर हैंडल करेंगे)
    keyboard = [
        [InlineKeyboardButton("🔥 ATER INFO ऐप खोलें 🔥", callback_data="open_webapp")],
        
    reply_markup = InlineKeyboardMarkup(keyboard)

    text = (
        f"HELLO {first_name} ! 👋\n\n"
        "NUMBER, AADHAR, UPI, VEHICLE, TELEGRAM,  And all the information in one place! 🚀\n"
        "Click button open tha app"
    )

    await update.message.reply_text(
        text,
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()  # क्लिक को एकनॉलेज करें

    if query.data == "open_webapp":
        user_id = query.from_user.id
        # यूजर को प्राइवेट मैसेज भेजें जिसमें Web App बटन हो
        keyboard = [
            [InlineKeyboardButton("🔥 ATER WEB INFO OPEN 🔥", web_app={"url": WEBAPP_URL})]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        text = "Click button open the app 🚀"

        try:
            await context.bot.send_message(
                chat_id=user_id,
                text=text,
                reply_markup=reply_markup,
                disable_web_page_preview=True
            )
        except Exception as e:
            logger.error(f"प्राइवेट मैसेज भेजने में एरर: {e}")
            # अगर प्राइवेट मैसेज नहीं जा सकता (यूजर ने बॉट स्टार्ट नहीं किया), तो ग्रुप में मैसेज
            await query.edit_message_text("कृपया पहले बॉट को प्राइवेट में स्टार्ट करें (/start) फिर दोबारा ट्राई करें!")

def main() -> None:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    application = Application.builder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT, handle_message))
    application.add_handler(CallbackQueryHandler(handle_callback))

    print("Bot started successfully!")
    logger.info("Bot is running...")

    application.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True
    )

if __name__ == "__main__":
    main()
