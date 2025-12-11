import os
import telebot
from telebot import types
from datetime import datetime

BOT_TOKEN = os.environ['BOT_TOKEN']
CHANNEL_LINK = os.environ.get('CHANNEL_LINK', 'https://t.me/+test')

bot = telebot.TeleBot(BOT_TOKEN)

def log(user_id, username=""):
    try:
        with open("users.log", "a") as f:
            f.write(f"{datetime.now()} | {user_id} | @{username}\n")
    except:
        pass

@bot.message_handler(commands=['start'])
def start(m):
    log(m.from_user.id, m.from_user.username)
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("NYC 70% OFF", callback_data="nyc"),
        types.InlineKeyboardButton("Miami 65% OFF", callback_data="miami"),
        types.InlineKeyboardButton("Vegas 75% OFF", callback_data="vegas"),
        types.InlineKeyboardButton("Orlando 60% OFF", callback_data="orlando"),
        types.InlineKeyboardButton("Luxury Hotels", callback_data="luxury"),
        types.InlineKeyboardButton("Airbnb Deals", callback_data="airbnb")
    )
    markup.add(types.InlineKeyboardButton("Join Channel – Live Deals", url=CHANNEL_LINK))

    text = f"""*USA CHEAP HOTELS & STAYS*

Welcome {m.from_user.first_name}!

*Today's Flash Deals (Dec 2025):*
• Hotels up to 75% OFF
• Last-minute promo codes
• Luxury & Airbnb discounts

cheap hotels usa • discount hotels usa • last minute deals"""

    bot.send_message(m.chat.id, text, reply_markup=markup, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda c: True)
def cb(c):
    deals = {
        "nyc": "*NEW YORK CITY*\nTimes Square from $69 · Manhattan from $129",
        "miami": "*MIAMI BEACH*\nOceanfront from $99 · 5★ from $149",
        "vegas": "*LAS VEGAS*\nBellagio/Caesars from $39/night",
        "orlando": "*ORLANDO DISNEY*\nHotels from $79 + free breakfast",
        "luxury": "*5★ LUXURY HOTELS*\nRitz-Carlton · Four Seasons flash sale",
        "airbnb": "*AIRBNB & VILLAS*\nExtra 15–30% off with codes"
    }
    if c.data in deals:
        mk = types.InlineKeyboardMarkup()
        mk.add(types.InlineKeyboardButton("Get Booking Links", url=CHANNEL_LINK))
        bot.edit_message_text(deals[c.data] + "\n\nJoin channel now!", c.message.chat.id, c.message.chat.id, reply_markup=mk, parse_mode='Markdown')
    bot.answer_callback_query(c.id)

print("Bot started successfully on Render!")
bot.infinity_polling()
