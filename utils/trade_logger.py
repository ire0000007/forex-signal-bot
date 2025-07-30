# utils/trade_logger.py

import os
from datetime import datetime

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

def log_signal(symbol, action, score, confidence, entry, sl, tp, components):
    """
    Logs the signal details to a log file.
    """
    log_file = os.path.join(LOG_DIR, f"{symbol.replace('=', '')}_signals.log")
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    
    log_message = (
        f"{timestamp} | {symbol} {action} Signal\n"
        f"Score: {score} | Confidence: {confidence}\n"
        f"Entry: {entry} | SL: {sl} | TP: {tp}\n"
        f"Components: {components}\n"
        f"{'-'*50}\n"
    )

    with open(log_file, "a") as f:
        f.write(log_message)

    print(f"📄 Signal logged: {symbol} | {action} | {score} | {confidence}")

def get_logged_trades_summary():
    """
    Returns a summary of today's logged trades.
    """
    try:
        today = datetime.utcnow().strftime("%Y-%m-%d")
        summary_lines = []
        
        if not os.path.exists(LOG_DIR):
            return "No trades logged today."
        
        for filename in os.listdir(LOG_DIR):
            if filename.endswith('_signals.log'):
                filepath = os.path.join(LOG_DIR, filename)
                with open(filepath, 'r') as f:
                    content = f.read()
                    if today in content:
                        lines = content.split('\n')
                        today_signals = [line for line in lines if today in line and '|' in line]
                        if today_signals:
                            symbol = filename.replace('_signals.log', '')
                            summary_lines.append(f"{symbol}: {len(today_signals)} signals")
        
        if summary_lines:
            return "\n".join(summary_lines)
        else:
            return "No trades logged today."
    except Exception as e:
        return f"Error generating summary: {e}"