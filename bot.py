import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, MessageHandler, filters, ContextTypes

BOT_TOKEN = "8726912419:AAFKSAkpmpM7EJlJZlj-CHzZzLXO8wUzylY"
WEB_APP_URL = "https://ater-web-bot.vercel.app"

TRIGGER_COMMANDS = {
    "/start", "/num", "/aadhar", "/vehicle", "/upi", "/aadhar_family"
}

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

async def handle_trigger(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message
    if not message or not message.text:
        return

    # कमांड एक्सट्रैक्ट (केस insensitive + बॉट मेंशन अगर हो)
    text = message.text.strip().lower()
    command = text.split()[0].rstrip('@' + context.bot.username.lower())  # अगर @botname के साथ कमांड हो

    if command in TRIGGER_COMMANDS:
        reply_text = (
            "नमस्ते ATER CYBER जी! 👋\n\n"
            "नंबर, आधार, UPI, व्हीकल, और सारी जानकारी एक जगह! 🚀\n"
            "नीचे बटन दबाकर ऐप खोलो! 🔥"
        )

        keyboard = [
            [
                InlineKeyboardButton(
                    text="ATER INFO ऐप खोलें 🔥🔥",
                    web_app=WebAppInfo(url=WEB_APP_URL)
                )
            ],
            [
                InlineKeyboardButton(
                    text="पूरी जानकारी देखें ℹ️",
                    callback_data="full_info"  # अगर क्लिक पर कुछ करना हो
                )
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await message.reply_text(
            reply_text,
            reply_markup=reply_markup,
            parse_mode="HTML"  # या MarkdownV2, इमोजी के लिए अच्छा
        )

        # ऑप्शनल: यूजर का मैसेज डिलीट (क्योंकि बॉट एडमिन है)
        # await message.delete()

def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()

    # सिर्फ कमांड्स पर (ग्रुप + प्राइवेट दोनों)
    application.add_handler(
        MessageHandler(filters.COMMAND, handle_trigger)
    )

    # अगर कमांड @botname के साथ भी हैंडल करना हो
    # application.add_handler(MessageHandler(filters.Regex(r'^/'), handle_trigger))

    print("बॉट शुरू हो रहा है...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
