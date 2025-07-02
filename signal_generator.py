from quotexpy.new import Quotex
import pandas as pd
import numpy as np
import ta

# ✅ Initialize Quotex instance (already logged-in in main bot)
quotex = Quotex()

# ✅ Main Live Strategy Function
async def generate_signal(pair: str):
    try:
        print(f"[Live Signal] Analyzing: {pair}")

        # 🕒 Fetch 15s candles (get 60 candles = 15min data)
        candles = quotex.get_candles(pair, interval="15S", count=60)

        if not candles or len(candles) < 20:
            print(f"[Live Signal] Not enough data for {pair}")
            return None

        # 📊 Prepare dataframe
        df = pd.DataFrame(candles)
        df.rename(columns={"open": "Open", "close": "Close", "high": "High", "low": "Low", "volume": "Volume"}, inplace=True)

        # ✅ Add RSI
        df["rsi"] = ta.momentum.RSIIndicator(close=df["Close"], window=14).rsi()
        rsi = round(df["rsi"].iloc[-1], 2)

        # ✅ Trend detection (simple SMA comparison)
        df["sma_short"] = df["Close"].rolling(window=5).mean()
        df["sma_long"] = df["Close"].rolling(window=20).mean()
        if df["sma_short"].iloc[-1] > df["sma_long"].iloc[-1]:
            trend = "UP"
        elif df["sma_short"].iloc[-1] < df["sma_long"].iloc[-1]:
            trend = "DOWN"
        else:
            trend = "SIDEWAYS"

        # ✅ Volume spike detection
        recent_volume = df["Volume"].iloc[-1]
        avg_volume = df["Volume"].rolling(window=20).mean().iloc[-1]
        volume_strength = "High" if recent_volume > avg_volume else "Normal"

        # ✅ Support/Resistance logic
        last_close = df["Close"].iloc[-1]
        recent_lows = df["Low"].rolling(window=20).min().iloc[-1]
        recent_highs = df["High"].rolling(window=20).max().iloc[-1]

        if last_close <= recent_lows + 0.0003:
            zone = "Support"
        elif last_close >= recent_highs - 0.0003:
            zone = "Resistance"
        else:
            zone = "Neutral"

        # ✅ Final signal decision
        if trend == "UP" and rsi < 70 and zone == "Support":
            direction = "call"
        elif trend == "DOWN" and rsi > 30 and zone == "Resistance":
            direction = "put"
        else:
            direction = None

        if not direction:
            return None

        confidence = "75%" if volume_strength == "High" else "65%"

        return {
            "direction": direction,
            "rsi": rsi,
            "trend": trend,
            "volume": recent_volume,
            "zone": zone,
            "confidence": confidence
        }

    except Exception as e:
        print(f"[Live Signal] Error for {pair}: {e}")
        return None
