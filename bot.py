import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, MessageHandler, filters, ContextTypes

BOT_TOKEN = "8726912419:AAFKSAkpmpM7EJlJZlj-CHzZzLXO8wUzylY"
WEB_APP_URL = "https://ater-web-bot.vercel.app"

# ट्रिगर कमांड्स (केस इंसेंसिटिव)
TRIGGER_COMMANDS = {"/start", "/num", "/aadhar", "/vehicle", "/upi", "/aadhar_family"}

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

async def handle_trigger(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.message.text:
        return

    text = update.message.text.strip().lower().split()[0]  # पहला शब्द

    if text in TRIGGER_COMMANDS:
        # वो खूबसूरत मैसेज
        message_text = (
            "नमस्ते ATER CYBER जी! 👋\n\n"
            "नंबर, आधार, UPI, व्हीकल, और सारी जानकारी एक जगह! 🚀\n"
            "नीचे बटन दबाकर ऐप खोलो! 🔥"
        )

        # दो बटन: एक web app, दूसरा info (या जो चाहो)
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
                    callback_data="full_info"  # अगर क्लिक पर कुछ करना हो तो हैंडल कर सकते हो, अभी सिर्फ दिखाने के लिए
                )
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            message_text,
            reply_markup=reply_markup,
            parse_mode="Markdown"  # इमोजी और फॉर्मेटिंग के लिए अच्छा काम करता है
        )

        # ऑप्शनल: यूजर का ओरिजिनल मैसेज डिलीट कर दो (अगर बॉट एडमिन है)
        # await update.message.delete()

def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(
        MessageHandler(filters.TEXT & filters.Regex(r'^/'), handle_trigger)
    )  # सिर्फ कमांड्स पर ट्रिगर (/ से शुरू होने वाले)

    print("बॉट शुरू हो रहा है...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
