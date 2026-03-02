import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

# अपना बॉट का exact username डालो (BotFather से देखो, @ के बिना)
BOT_USERNAME = "aterinfobot"  # ←←← यहाँ बदलो !! उदाहरण: ATERINFOBOT या जो भी है

BOT_TOKEN = "8726912419:AAFOm3dCKXGp2YFVxj3DoEe2AUyw_XR8jo4"

# startapp पैरामीटर – आप चाहें तो बदल सकते हो, या "" खाली रखो
# इससे आपके ऐप में Telegram.WebApp.initDataUnsafe.start_param मिलेगा
STARTAPP_PARAM = "open_from_group"

# यह लिंक क्लिक पर Mini App खोलेगा
WEB_APP_LINK = "https://ater-web-bot.vercel.app"

TRIGGER_COMMANDS = ["start", "num", "aadhar", "vehicle", "upi", "aadhar_family"]

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def handle_trigger(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.message.text:
        return

    # कमांड निकालो (ग्रुप में @botname के साथ भी)
    command = update.message.text.split()[0].lower().lstrip('/')
    if '@' in command:
        command = command.split('@')[0]

    if command in TRIGGER_COMMANDS:
        message_text = (
            "नमस्ते ATER CYBER जी! 👋\n\n"
            "नंबर, आधार, UPI, व्हीकल, और सारी जानकारी एक जगह! 🚀\n"
            "नीचे बटन दबाकर ऐप खोलो! 🔥"
        )

        keyboard = [
            [
                InlineKeyboardButton(
                    text="ATER INFO ऐप खोलें 🔥🔥",
                    url="https://ater-web-bot.vercel.app" # ← यहाँ url यूज करो, web_app नहीं !
                )
            ],
            [
                InlineKeyboardButton(
                    text="पूरी जानकारी देखें ℹ️",
                    callback_data="full_info"  # अगर callback हैंडल करना है तो अलग handler बनाओ
                )
            ]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        try:
            await update.message.reply_text(
                message_text,
                reply_markup=reply_markup
            )
            # ऑप्शनल: यूजर का मैसेज डिलीट करो (ग्रुप क्लीन रखने के लिए)
            # await update.message.delete()
        except Exception as e:
            logger.error(f"Error sending reply: {e}")

def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()

    # सभी कमांड्स हैंडल करो
    application.add_handler(CommandHandler(TRIGGER_COMMANDS, handle_trigger))

    print("बॉट शुरू हो रहा है... ग्रुप में बटन अब URL से खोलेगा")
    application.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
