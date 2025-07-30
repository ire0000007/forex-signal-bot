# utils/volatility_utils.py
import numpy as np

def check_volatility(df, threshold=0.5):
    """
    Checks if the recent volatility exceeds a threshold.
    Returns True if volatility is acceptable, False otherwise.
    """
    try:
        df['returns'] = df['Close'].pct_change()
        volatility = np.std(df['returns'].dropna()) * 100  # Convert to percentage
        print(f"📊 Volatility for {df.columns.name}: {volatility:.2f}%")

        if volatility > threshold:
            print("❌ High volatility detected, signal rejected.")
            return False
        else:
            print("✅ Volatility within acceptable range.")
            return True
    except Exception as e:
        print(f"❌ Volatility check error: {str(e)}")
        return False
