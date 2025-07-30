# telegram_listener.py
from telebot import TeleBot
from utils.config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID
from signal_generator import run_full_scan
import threading

bot = TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    if str(message.chat.id) == TELEGRAM_CHAT_ID:
        bot.reply_to(message, "🤖 Forex Bot Ready! Use /scan to run signal check.")

@bot.message_handler(commands=['scan'])
def handle_scan(message):
    if str(message.chat.id) == TELEGRAM_CHAT_ID:
        bot.reply_to(message, "🔍 Scanning all assets...")
        threading.Thread(target=run_full_scan).start()

def run_telegram_command_listener():
    bot.polling(none_stop=True)
