# scheduler.py

from apscheduler.schedulers.background import BackgroundScheduler
from signal_generator import run_full_scan
from telegram_bot import send_daily_summary
import time

def start_schedulers():
    scheduler = BackgroundScheduler(timezone="UTC")
    scheduler.add_job(run_full_scan, "interval", minutes=30)  # Signal scan every 30 minutes
    scheduler.add_job(send_daily_summary, "cron", hour=22, minute=0)  # Daily summary at 22:00 UTC
    scheduler.start()
    print("🕒 Signal scan scheduled every 30 minutes and daily summary at 22:00 UTC.")
    return scheduler

if __name__ == "__main__":
    print("🚀 Starting Forex Signal Bot...")
    from telegram_listener import run_telegram_command_listener
    import threading
    
    # Start Telegram listener in background
    threading.Thread(target=run_telegram_command_listener, daemon=True).start()
    
    scheduler = start_schedulers()

    try:
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print("🛑 Bot stopped.")
