# utils/alert_manager.py

import requests

# === YOUR ALERT SETTINGS ===
TELEGRAM_TOKEN = '8123034561:AAFUmL-YVT2uybFNDdl4U9eKQtz2w1f1dPo'
TELEGRAM_CHAT_ID = '5689209090'
DISCORD_WEBHOOK = 'https://discord.com/api/webhooks/1398658870980644985/0fHPvafJv0Bi6uc0RzPITEzcKgqKt6znfhhrBy-4qFBas8BfxiTxjyFkVqtp_ctt-Ndt'

# === Scoring Thresholds ===
def get_confidence_level(score):
    if score >= 5:
        return "🟢 High"
    elif score >= 3:
        return "🟠 Medium"
    else:
        return "🔴 Low"

def format_signal_message(symbol, score, components, entry, sl, tp):
    confidence = get_confidence_level(score)
    comp_text = "\n".join([f"{k}: {v}" for k, v in components.items()])
    message = (
        f"#{symbol} Signal Alert\n"
        f"{confidence} Confidence ({score}/6)\n\n"
        f"{comp_text}\n\n"
        f"📈 Entry: {entry:.4f}\n"
        f"🛡 SL: {sl:.4f} | 🎯 TP: {tp:.4f}\n\n"
        f"#IRE_DID_THIS"
    )
    return message

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message
    }
    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print("✅ Telegram alert sent.")
        else:
            print(f"❌ Telegram error: {response.text}")
    except Exception as e:
        print(f"❌ Telegram alert failed: {e}")

def send_discord_alert(message):
    payload = {"content": message}
    try:
        response = requests.post(DISCORD_WEBHOOK, json=payload)
        if response.status_code == 204 or response.status_code == 200:
            print("✅ Discord alert sent.")
        else:
            print(f"❌ Discord error: {response.text}")
    except Exception as e:
        print(f"❌ Discord alert failed: {e}")

def send_alert(symbol, score, components, entry, sl, tp):
    """
    Sends formatted alert to Telegram and Discord with individual parameters.
    
    Args:
        symbol (str): Trading symbol
        score (int): Signal score
        components (dict): Signal components
        entry (float): Entry price
        sl (float): Stop loss
        tp (float): Take profit
    """
    try:
        message = format_signal_message(symbol, score, components, entry, sl, tp)
        send_telegram_alert(message)
        send_discord_alert(message)
    except Exception as e:
        print(f"❌ Alert dispatch error: {e}")
