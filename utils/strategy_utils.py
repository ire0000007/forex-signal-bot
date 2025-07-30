# utils/strategy_utils.py

import pandas as pd
import numpy as np

def calculate_rsi(df, period=14):
    """
    Calculate RSI (Relative Strength Index).
    """
    delta = df['Close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=period, min_periods=1).mean()
    avg_loss = loss.rolling(window=period, min_periods=1).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_macd(df, fast=12, slow=26, signal=9):
    """
    Calculate MACD (Moving Average Convergence Divergence).
    """
    ema_fast = df['Close'].ewm(span=fast, min_periods=1).mean()
    ema_slow = df['Close'].ewm(span=slow, min_periods=1).mean()
    macd = ema_fast - ema_slow
    signal_line = macd.ewm(span=signal, min_periods=1).mean()
    return macd, signal_line

def analyze_candle(df):
    """
    Analyze the last candle for bullish/bearish signal.
    """
    last = df.iloc[-1]
    open_price = last['Open']
    close_price = last['Close']
    candle_type = "bullish" if close_price > open_price else "bearish"
    return candle_type

def evaluate_indicators(df):
    """
    Evaluate RSI, MACD, and Candle for signal scoring.
    
    Returns:
        dict: Scores and details for each indicator.
    """
    components = {}
    score = 0

    try:
        rsi_series = calculate_rsi(df)
        latest_rsi = rsi_series.iloc[-1]
        if latest_rsi < 30:
            components['RSI'] = 'Oversold'
            score += 1
        elif latest_rsi > 70:
            components['RSI'] = 'Overbought'
            score += 1
        else:
            components['RSI'] = 'Neutral'

    except Exception as e:
        components['RSI'] = f"Error: {e}"

    try:
        macd, signal_line = calculate_macd(df)
        if macd.iloc[-1] > signal_line.iloc[-1]:
            components['MACD'] = 'Bullish'
            score += 1
        else:
            components['MACD'] = 'Bearish'

    except Exception as e:
        components['MACD'] = f"Error: {e}"

    try:
        candle = analyze_candle(df)
        components['Candle'] = candle.capitalize()
        if candle == 'bullish':
            score += 1
    except Exception as e:
        components['Candle'] = f"Error: {e}"

    return score, components
