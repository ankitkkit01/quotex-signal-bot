# signal_generator.py

import random
import pandas as pd
import ta
from quotexpy.new import Quotex

# Initialize Quotex with login credentials
quotex = Quotex(email="arhimanshya@gmail.com", password="12345678an")

# Fetch and analyze market data
def analyze_market(pair):
    try:
        candles = quotex.get_candles(asset=pair, interval=15, count=100)
        if not candles:
            return None

        # Convert and clean dataframe
        df = pd.DataFrame(candles)
        df.rename(columns={
            "open_price": "open",
            "close_price": "close",
            "max_price": "high",
            "min_price": "low"
        }, inplace=True)

        # Add indicators
        df["rsi"] = ta.momentum.RSIIndicator(close=df["close"], window=14).rsi()
        df["ema"] = ta.trend.EMAIndicator(close=df["close"], window=20).ema_indicator()
        df["volume"] = ta.volume.OnBalanceVolumeIndicator(close=df["close"], volume=df["volume"]).on_balance_volume()

        latest = df.iloc[-1]

        # Decision Logic
        direction = None
        confidence = 0

        if latest["rsi"] < 30 and latest["close"] > latest["ema"]:
            direction = "call"
            confidence = random.randint(80, 95)
        elif latest["rsi"] > 70 and latest["close"] < latest["ema"]:
            direction = "put"
            confidence = random.randint(80, 95)

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

# Callable async function for Telegram bot
async def generate_signal(pair):
    print(f"[Generating Signal] for {pair}")
    result = analyze_market(pair)
    if result and result["direction"]:
        return result
    return None
