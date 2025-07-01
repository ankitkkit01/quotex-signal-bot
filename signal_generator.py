import pandas as pd
import ta
from quotexpy.new import Quotex

# ✅ Use your actual credentials here
quotex = Quotex(email="ak19860570@gmail.com", password="12345678an")

# 🔌 Connect & fetch candles
async def fetch_candles(pair: str, timeframe: str = "1m", limit: int = 50):
    if not quotex.connected:
        status, reason = await quotex.connect()
        print(f"[DEBUG] Quotex connect: {status}, Reason: {reason}")
        if not status:
            return None

    success, data = await quotex.get_candles(pair, timeframe, limit)
    print(f"[DEBUG] Candle fetch for {pair}: {success}, Total candles: {len(data) if data else 0}")
    
    if not success or not data:
        return None

    df = pd.DataFrame(data)
    if df.empty or 'close' not in df.columns:
        print(f"[DEBUG] Data invalid or missing 'close' column for {pair}")
        return None

    return df

# 🎯 Signal generator with full trace
async def generate_signal(pair: str):
    df = await fetch_candles(pair)
    if df is None or len(df) < 20:
        print(f"[DEBUG] Not enough data for {pair}")
        return None

    # 📈 Add indicators
    df['rsi'] = ta.momentum.RSIIndicator(df['close'], window=14).rsi()
    df['sma100'] = df['close'].rolling(window=100).mean()

    latest = df.iloc[-1]
    rsi = latest['rsi']
    price = latest['close']
    sma100 = latest['sma100']
    trend = "bullish" if price > sma100 else "bearish"

    # 🧠 Log indicators
    print(f"[DEBUG] Pair: {pair}, RSI: {rsi:.2f}, Price: {price}, SMA100: {sma100}, Trend: {trend}")

    if pd.isna(rsi) or pd.isna(sma100):
        print(f"[DEBUG] RSI or SMA100 is NaN, skipping signal for {pair}")
        return None

    # ✅ Strategy logic
    if rsi < 30 and price > sma100:
        direction = "call"
        confidence = "High"
    elif rsi > 70 and price < sma100:
        direction = "put"
        confidence = "High"
    else:
        print(f"[DEBUG] No valid signal conditions met for {pair}")
        return None

    return {
        "direction": direction,
        "rsi": round(rsi, 2),
        "trend": trend,
        "volume": "N/A",
        "zone": "Support" if direction == "call" else "Resistance",
        "confidence": confidence
    }
