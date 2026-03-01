import telebot
from telebot.types import KeyboardButton, ReplyKeyboardMarkup, WebAppInfo

# Replace with your bot token
TOKEN = '8726912419:AAFKSAkpmpM7EJlJZlj-CHzZzLXO8wUzylY'
WEB_APP_URL = 'https://ater-web-bot.vercel.app'

bot = telebot.TeleBot(TOKEN)

# List of commands to handle
COMMANDS = ['start', 'num', 'aadhar', 'vehicle']  # Add more commands here if needed, e.g., 'pan', 'dl'

@bot.message_handler(commands=COMMANDS)
def handle_commands(message):
    # Create a reply keyboard with a button that opens the web app
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    web_app_button = KeyboardButton("Open Web App", web_app=WebAppInfo(url=WEB_APP_URL))
    markup.add(web_app_button)
    
    # Send the reply message with the button
    bot.reply_to(message, "Click the button below to open the web app.", reply_markup=markup)

# Start polling for updates
if __name__ == '__main__':
    print("Bot is running...")
    bot.infinity_polling()
