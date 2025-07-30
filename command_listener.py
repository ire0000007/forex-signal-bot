# command_listener.py

import telebot

# === Telegram credentials ===
TELEGRAM_TOKEN = '8123034561:AAFUmL-YVT2uybFNDdl4U9eKQtz2w1f1dPo'
CHAT_ID = '5689209090'

bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.chat.id, "👋 Bot is online and ready. Type /help for commands.")

@bot.message_handler(commands=['status'])
def status_handler(message):
    bot.send_message(message.chat.id, "📊 Bot Status: Running.\n📈 Signals will be sent automatically.")

@bot.message_handler(commands=['help'])
def help_handler(message):
    bot.send_message(message.chat.id, "🛠 Available Commands:\n/start - Start bot\n/status - Bot status\n/help - Show this menu")

def run_telegram_command_listener():
    print("📩 Telegram command listener started...")
    bot.infinity_polling()
