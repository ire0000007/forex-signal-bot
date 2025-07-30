# telegram_bot.py

import telebot
import os
from utils.config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID
from utils.trade_logger import get_logged_trades_summary

bot = telebot.TeleBot(TELEGRAM_TOKEN)

def send_telegram_message(message):
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)
    except Exception as e:
        print(f"❌ Telegram send error: {e}")

def send_daily_summary():
    try:
        summary = get_logged_trades_summary()
        message = f"📊 Daily Signal Summary\n\n{summary}\n#IRE_DID_THIS"
        send_telegram_message(message)
    except Exception as e:
        print(f"❌ Summary error: {e}")

# Optional: listen for basic /start or /summary commands
@bot.message_handler(commands=['start', 'summary'])
def handle_commands(message):
    if message.text == "/summary":
        send_daily_summary()
    else:
        bot.reply_to(message, "✅ Signal bot is running.\nUse /summary for today's signals.")

def start_bot():
    print("📩 Telegram command listener started...")
    bot.infinity_polling()
