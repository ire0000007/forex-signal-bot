# main.py
from signal_generator import run_full_scan
from scheduler import start_schedulers
from telegram_listener import run_telegram_command_listener
from flask import Flask
import threading
import logging

logging.basicConfig(level=logging.INFO)

# Run Telegram command listener in a thread
threading.Thread(target=run_telegram_command_listener, daemon=True).start()
print("📩 Telegram command listener started...")

# Start daily summary and scan schedulers
start_schedulers()
print("🕒 Daily summary scheduled at 22:00 UTC.")

# Start initial full scan immediately
print("🚀 Signal scan started:")
try:
    run_full_scan()
except Exception as e:
    print(f"❌ Initial scan failed: {e}")
    print("⚠️ Bot will continue with scheduled scans...")

# Start Flask web server (for Railway keep-alive)
app = Flask(__name__)

@app.route('/')
def home():
    return "📡 Forex Signal Bot Running"

if __name__ == '__main__':
    print("🌐 Flask server running...")
    app.run(host='0.0.0.0', port=8080)
