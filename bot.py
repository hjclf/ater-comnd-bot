import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

# आपका बोट टोकन यहाँ है
API_TOKEN = '8726912419:AAEKfzfbDfOkYLOGGqjGSpPN6zrnuOC1u5c'
WEB_APP_URL = 'https://ater-web-bot.vercel.app'

# Logging सेटअप
logging.basicConfig(level=logging.INFO)

# बोट और डिस्पैचर सेटअप
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# रिप्लाई मैसेज का फॉर्मेट
REPLY_TEXT = (
    "नमस्ते **{name}** जी! 👋\n\n"
    "नंबर, आधार, UPI, व्हीकल, और सारी\n"
    "जानकारी एक जगह! 🚀\n"
    "नीचे बटन दबाकर ऐप खोलो!"
)

def get_keyboard():
    """बटन सेटअप"""
    markup = InlineKeyboardMarkup(row_width=1)
    
    # Web App बटन
    web_app_btn = InlineKeyboardButton(
        text="🔥 ATER INFO ऐप खोलें 🔥",
        web_app=WebAppInfo(url=WEB_APP_URL)
    )
    
    # जानकारी वाला बटन
    info_btn = InlineKeyboardButton(
        text="ℹ️ पूरी जानकारी देखें",
        callback_data="view_info"
    )
    
    markup.add(web_app_btn, info_btn)
    return markup

# जब कोई भी कमांड (/) भेजे तो यह फंक्शन चलेगा
@dp.message_handler(lambda message: message.text.startswith('/'))
async def send_welcome(message: types.Message):
    user_name = message.from_user.full_name
    
    # फोटो में दिखाए गए स्टाइल में रिप्लाई
    await message.reply(
        REPLY_TEXT.format(name=user_name),
        reply_markup=get_keyboard(),
        parse_mode="Markdown"
    )

if __name__ == '__main__':
    print("बोट चालू हो गया है...")
    executor.start_polling(dp, skip_updates=True)
