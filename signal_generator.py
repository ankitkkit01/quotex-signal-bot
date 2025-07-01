import pandas as pd
import ta
from quotexpy.new import Quotex

# 👇 Initialize Quotex (replace credentials if needed)
quotex = Quotex(email="ak19860570@gmail.com", password="12345678an")

# 🕒 Fetch latest candles from Quotex
async def fetch_candles(pair: str, timeframe: str = "1m", limit: int = 50):
    success, data = await quotex.get_candles(pair, timeframe, limit)
    if not success or not data:
        return None

    df = pd.DataFrame(data)
    if df.empty or 'close' not in df.columns:
        return None
    return df

# 🧠 Signal Generator Logic (RSI + SMA100 based)
async def generate_signal(pair: str):
    df = await fetch_candles(pair)
    if df is None or len(df) < 20:
        print(f"[DEBUG] Not enough data for {pair}")
        return None

    # 📈 Indicators
    df['rsi'] = ta.momentum.RSIIndicator(df['close'], window=14).rsi()
    df['sma100'] = df['close'].rolling(window=100).mean()

    latest = df.iloc[-1]
    rsi = latest['rsi']
    price = latest['close']
    sma100 = latest['sma100']
    trend = "bullish" if price > sma100 else "bearish"

    if pd.isna(rsi) or pd.isna(sma100):
        return None

    # 🎯 Strategy: RSI oversold/overbought with SMA filter
    if rsi < 30 and price > sma100:
        direction = "call"
        confidence = "High"
    elif rsi > 70 and price < sma100:
        direction = "put"
        confidence = "High"
    else:
        return None  # No valid signal

    return {
        "direction": direction,
        "rsi": round(rsi, 2),
        "trend": trend,
        "volume": "N/A",
        "zone": "Support" if direction == "call" else "Resistance",
        "confidence": confidence
    }
