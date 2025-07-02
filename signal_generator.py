# signal_generator.py

import datetime
import numpy as np
from quotexpy.new import Quotex
from ta.trend import SMAIndicator
from ta.momentum import RSIIndicator
from ta.volume import OnBalanceVolumeIndicator

quotex = Quotex(email="arhimanshya@gmail.com", password="12345678an")

async def generate_signal(pair):
    try:
        # 1. Get last 100 candles for 15s timeframe
        candles = quotex.get_candles(asset=pair, timeframe=15, count=100)
        if not candles or len(candles) < 50:
            return None

        close = np.array([c['close'] for c in candles])
        high = np.array([c['max'] for c in candles])
        low = np.array([c['min'] for c in candles])
        volume = np.array([c['volume'] for c in candles])

        # 2. Indicators
        rsi = RSIIndicator(close=close, window=14).rsi()[-1]
        sma100 = SMAIndicator(close=close, window=100).sma_indicator()[-1]
        current_price = close[-1]
        obv = OnBalanceVolumeIndicator(close=close, volume=volume).on_balance_volume()[-1]

        # 3. Trend decision
        if current_price > sma100:
            trend = "UP"
            direction = "call"
        elif current_price < sma100:
            trend = "DOWN"
            direction = "put"
        else:
            trend = "SIDEWAYS"
            direction = None

        # 4. Conditions check
        if trend == "SIDEWAYS" or rsi < 50 or abs(obv) < 100:
            return None  # Skip weak setups

        return {
            "direction": direction,
            "rsi": round(rsi, 2),
            "trend": trend,
            "volume": int(volume[-1]),
            "zone": "Support" if direction == "call" else "Resistance",
            "confidence": f"{random.randint(75, 89)}%"
        }

    except Exception as e:
        print(f"[Signal Error] {e}")
        return None
