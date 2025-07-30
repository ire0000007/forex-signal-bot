# assets/us30_signal.py
from utils.data_fetcher import fetch_with_alternatives
from utils.generate_generic_signal import generate_generic_signal
from utils.alert_manager import send_alert

def generate_us30_signal():
    symbol = "^DJI"  # Dow Jones Index
    timeframe = "1h"

    df = fetch_with_alternatives(symbol, period="5d", interval=timeframe)
    if df is None or df.empty:
        print(f"❌ No data for {symbol}")
        return

    entry_data = generate_generic_signal(symbol, df)
    if entry_data:
        entry, sl, tp, score, components = entry_data
        send_alert(symbol, score, components, entry, sl, tp)
    else:
        print(f"❌ No valid signal for {symbol}")
