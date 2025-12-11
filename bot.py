import telebot
from telebot import types

BOT_TOKEN = "8549761838:AAHvEf_D4Jv3MDFWdKp3ufJ-Mp0Til_v3HM"
CHANNEL_LINK = "https://t.me/YourAccommodationChannel"
LOG_FILE = "users.txt"

bot = telebot.TeleBot(BOT_TOKEN)

def log_user(user_id, username):
    try:
        with open(LOG_FILE, "r") as f:
            users = f.read().splitlines()
    except FileNotFoundError:
        users = []

    entry = f"{user_id} - {username}"
    if entry not in users:
        with open(LOG_FILE, "a") as f:
            f.write(entry + "\n")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    username = message.from_user.username or "NoUsername"
    log_user(user_id, username)

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📢 Join Channel", url=CHANNEL_LINK))
    bot.send_message(message.chat.id,
        f"👋 Welcome, {message.from_user.first_name}!\n"
        "Thanks for starting the **Accommodation US Bot**.\n"
        "We help you find the best stays in the United States.\n\n"
        "🔗 Join our channel for the latest deals and updates:",
        reply_markup=markup)

print("🤖 Bot is running...")
bot.polling()
