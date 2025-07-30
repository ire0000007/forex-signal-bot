# utils/data_fetcher.py
import yfinance as yf
import time
import random
from datetime import datetime
import requests

def fetch_data_with_retry(symbol, period="5d", interval="1h", max_retries=3):
    """
    Fetch data with retry logic and rate limiting to avoid Yahoo Finance blocks.
    """
    for attempt in range(max_retries):
        try:
            print(f"📊 Fetching data for {symbol} (attempt {attempt + 1}/{max_retries})")
            
            # Add random delay to avoid rate limiting
            delay = random.uniform(2, 5)  # Increased delay
            time.sleep(delay)
            
            # Create ticker object with custom headers
            ticker = yf.Ticker(symbol)
            
            # Try different periods if 5d fails
            periods_to_try = [period, "1d", "2d"] if period == "5d" else [period]
            
            for test_period in periods_to_try:
                try:
                    # Fetch data with timeout and custom session
                    df = ticker.history(
                        period=test_period, 
                        interval=interval, 
                        timeout=15,
                        prepost=False,
                        auto_adjust=True,
                        back_adjust=False
                    )
                    
                    if df is not None and not df.empty and len(df) >= 10:
                        print(f"✅ Data fetched successfully for {symbol} (period: {test_period}, rows: {len(df)})")
                        return df
                    else:
                        print(f"⚠️ Insufficient data for {symbol} with period {test_period}")
                        
                except Exception as period_error:
                    print(f"⚠️ Period {test_period} failed for {symbol}: {str(period_error)}")
                    continue
                
        except Exception as e:
            print(f"❌ Error fetching {symbol} (attempt {attempt + 1}): {str(e)}")
            
            if attempt < max_retries - 1:
                # Exponential backoff with jitter
                wait_time = (2 ** attempt) + random.uniform(2, 5)
                print(f"⏳ Waiting {wait_time:.1f}s before retry...")
                time.sleep(wait_time)
    
    print(f"❌ Failed to fetch data for {symbol} after {max_retries} attempts")
    return None

def get_alternative_symbols():
    """
    Alternative symbol mappings in case primary symbols fail.
    """
    return {
        'EURUSD=X': ['EURUSD', 'EUR=X'],
        'GBPUSD=X': ['GBPUSD', 'GBP=X'],
        'USDJPY=X': ['USDJPY', 'JPY=X'],
        'AUDUSD=X': ['AUDUSD', 'AUD=X'],
        'USDCAD=X': ['USDCAD', 'CAD=X'],
        'NZDUSD=X': ['NZDUSD', 'NZD=X'],
        'GC=F': ['XAUUSD=X', 'GOLD'],  # Gold alternatives
        'BTC-USD': ['BTCUSD=X', 'BTC'],
        '^GSPC': ['SPY', '^SPX'],
        '^DJI': ['DIA', 'YM=F'],
        'ETH-USD': ['ETHUSD=X', 'ETH']
    }

def create_mock_data(symbol):
    """
    Create mock data when Yahoo Finance is completely unavailable.
    This ensures the bot continues running even without real data.
    """
    try:
        import pandas as pd
        import numpy as np
        
        print(f"🔧 Creating mock data for {symbol} (Yahoo Finance unavailable)")
        
        # Generate mock price data
        dates = pd.date_range(end=datetime.now(), periods=50, freq='1H')
        base_price = 1.1000 if 'USD' in symbol else 2000.0  # Different base for different assets
        
        # Generate realistic price movement
        np.random.seed(hash(symbol) % 2**32)  # Consistent seed per symbol
        returns = np.random.normal(0, 0.001, 50)  # Small random returns
        prices = [base_price]
        
        for ret in returns[1:]:
            prices.append(prices[-1] * (1 + ret))
        
        df = pd.DataFrame({
            'Open': prices,
            'High': [p * (1 + abs(np.random.normal(0, 0.0005))) for p in prices],
            'Low': [p * (1 - abs(np.random.normal(0, 0.0005))) for p in prices],
            'Close': prices,
            'Volume': [random.randint(10000, 100000) for _ in prices]
        }, index=dates)
        
        print(f"✅ Mock data created for {symbol} ({len(df)} rows)")
        return df
        
    except Exception as e:
        print(f"❌ Failed to create mock data for {symbol}: {e}")
        return None

def fetch_with_alternatives(primary_symbol, period="5d", interval="1h"):
    """
    Try primary symbol first, then alternatives, then mock data if all fail.
    """
    # Try primary symbol first
    df = fetch_data_with_retry(primary_symbol, period, interval)
    if df is not None and not df.empty:
        return df
    
    # Try alternative symbols
    alternatives = get_alternative_symbols().get(primary_symbol, [])
    for alt_symbol in alternatives:
        print(f"🔄 Trying alternative symbol: {alt_symbol}")
        df = fetch_data_with_retry(alt_symbol, period, interval, max_retries=2)  # Fewer retries for alternatives
        if df is not None and not df.empty:
            return df
    
    # If all real data fails, create mock data to keep bot running
    print(f"⚠️ All data sources failed for {primary_symbol}, using mock data")
    return create_mock_data(primary_symbol)

def test_yahoo_connection():
    """
    Test if Yahoo Finance is accessible at all.
    """
    try:
        test_ticker = yf.Ticker("AAPL")
        test_data = test_ticker.history(period="1d", interval="1h", timeout=10)
        if test_data is not None and not test_data.empty:
            print("✅ Yahoo Finance connection test passed")
            return True
        else:
            print("❌ Yahoo Finance connection test failed - no data")
            return False
    except Exception as e:
        print(f"❌ Yahoo Finance connection test failed: {e}")
        return False