# signal_generator.py
from utils.data_fetcher import fetch_with_alternatives
from assets.eurusd_signal import generate_eurusd_signal
from assets.gold_signal import generate_gold_signal
from assets.usdjpy_signal import generate_usdjpy_signal
from assets.gbpusd_signal import generate_gbpusd_signal
from assets.btc_signal import generate_btcusd_signal  # ✅ FIXED
from assets.audusd_signal import generate_audusd_signal
from assets.usdcad_signal import generate_usdcad_signal
from assets.nzdusd_signal import generate_nzdusd_signal
from assets.sp500_signal import generate_sp500_signal

import time

def test_data_connection():
    """Test if we can fetch any data at all."""
    from utils.data_fetcher import test_yahoo_connection
    print("🔍 Testing Yahoo Finance connection...")
    return test_yahoo_connection()

def run_full_scan():
    print("🔍 Running all signal scans...")
    
    # Test connection first
    connection_ok = test_data_connection()
    if not connection_ok:
        print("⚠️ Yahoo Finance connection issues detected - using fallback data")

    # Add delay between each scan to avoid rate limiting
    scan_functions = [
        ("EURUSD", generate_eurusd_signal),
        ("GOLD", generate_gold_signal),
        ("USDJPY", generate_usdjpy_signal),
        ("GBPUSD", generate_gbpusd_signal),
        ("BTCUSD", generate_btcusd_signal),
        ("AUDUSD", generate_audusd_signal),
        ("USDCAD", generate_usdcad_signal),
        ("NZDUSD", generate_nzdusd_signal),
        ("SP500", generate_sp500_signal)
    ]

    for name, func in scan_functions:
        try:
            print(f"🔍 Scanning {name}...")
            func()
            # Add delay between scans to avoid overwhelming Yahoo Finance
            time.sleep(random.uniform(3, 6))  # Longer random delays
        except Exception as e:
            print(f"❌ {name} scan failed: {e}")
            continue  # Continue with next scan even if one fails

    print("✅ Full scan completed.")

# Embedded Telegram/Discord details (already in each alert file)
TELEGRAM_TOKEN = '8123034561:AAFUmL-YVT2uybFNDdl4U9eKQtz2w1f1dPo'
TELEGRAM_CHAT_ID = '5689209090'
DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/1398658870980644985/0fHPvafJv0Bi6uc0RzPITEzcKgqKt6znfhhrBy-4qFBas8BfxiTxjyFkVqtp_ctt-Ndt'

# Tag for tracking
#IRE_DID_THIS
