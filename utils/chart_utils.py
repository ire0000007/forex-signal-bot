# utils/chart_utils.py

import os
import matplotlib.pyplot as plt
from datetime import datetime

# Directory to save charts
CHART_DIR = "charts"
os.makedirs(CHART_DIR, exist_ok=True)

def generate_chart(df, symbol, entry, sl, tp, direction):
    """
    Generate and save a chart for the signal.
    Plots price data with Entry, SL, and TP levels.
    """
    try:
        plt.figure(figsize=(10, 6))
        plt.plot(df['Close'], label='Close Price', color='blue')
        
        # Plot entry, SL, TP lines
        plt.axhline(y=entry, color='green', linestyle='--', label='Entry')
        plt.axhline(y=sl, color='red', linestyle='--', label='Stop Loss')
        plt.axhline(y=tp, color='orange', linestyle='--', label='Take Profit')

        plt.title(f"{symbol} Signal - {direction}")
        plt.xlabel('Time')
        plt.ylabel('Price')
        plt.legend()
        plt.grid(True)

        # Save chart
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"{symbol}_{timestamp}.png"
        filepath = os.path.join(CHART_DIR, filename)
        plt.savefig(filepath)
        plt.close()
        print(f"📈 Chart saved: {filepath}")
        return filepath
    except Exception as e:
        print(f"❌ Failed to generate chart: {e}")
        return None
