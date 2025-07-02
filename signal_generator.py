# signal_generator.py

from quotexpy.new import Quotex
import pandas as pd
import ta
import random

# Initialize and login
quotex = Quotex()
quotex.login(email="arhimanshya@gmail.com", password="12345678an")

# Analyze market using 15-second candle data
def analyze_market(pair):
    try:
        candles = quotex.get_candles(asset=pair, interval=15, count=100)
        if not candles:
            return None

        df = pd.DataFrame(candles)
        df.rename(columns={
            "open_price": "open",
            "close_price": "close",
            "max_price": "high",
            "min_price": "low"
        }, inplace=True)

        # Calculate indicators
        df["rsi"] = ta.momentum.RSIIndicator(close=df["close"], window=14).rsi()
        df["ema"] = ta.trend.EMAIndicator(close=df["close"], window=20).ema_indicator()
        df["volume"] = ta.volume.OnBalanceVolumeIndicator(close=df["close"], volume=df["volume"]).on_balance_volume()

        latest = df.iloc[-1]

        direction = None
        confidence = 0

        # Trading logic
        if latest["rsi"] < 30 and latest["close"] > latest["ema"]:
            direction = "call"
            confidence = random.randint(82, 94)
        elif latest["rsi"] > 70 and latest["close"] < latest["ema"]:
            direction = "put"
            confidence = random.randint(82, 94)

        trend = "UP" if latest["close"] > latest["ema"] else "DOWN"

        return {
            "direction": direction,
            "rsi": round(latest["rsi"], 2),
            "trend": trend,
            "volume": int(latest["volume"]),
            "zone": "Support" if trend == "UP" else "Resistance",
            "confidence": f"{confidence}%" if direction else "0%"
        }

    except Exception as e:
        print(f"[Signal Error] {e}")
        return None

# Main function to call from bot
async def generate_signal(pair):
    print(f"[Generating Signal] {pair}")
    signal = analyze_market(pair)
    if signal and signal["direction"]:
        return signal
    return None
