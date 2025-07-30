# utils/session_utils.py

from datetime import datetime

# Define trading sessions in UTC
SESSION_TIMES = {
    'tokyo': (0, 9),      # 00:00 - 09:00 UTC
    'london': (8, 17),    # 08:00 - 17:00 UTC
    'new york': (13, 22)  # 13:00 - 22:00 UTC
}

def get_current_session():
    """Return the current session name based on UTC time."""
    now_utc = datetime.utcnow()
    current_hour = now_utc.hour

    for session_name, (start_hour, end_hour) in SESSION_TIMES.items():
        if start_hour <= current_hour < end_hour:
            return session_name
    return 'closed'

def check_session(allowed_sessions):
    """Check if the current session is in the allowed list."""
    current_session = get_current_session()
    print(f"🕒 Current session: {current_session.capitalize()} | Allowed: {allowed_sessions}")
    return current_session in allowed_sessions
