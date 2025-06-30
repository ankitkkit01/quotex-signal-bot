# signal_generator.py

import random
import requests
import pandas as pd
import numpy as np
from ta.momentum import RSIIndicator
from ta.trend import SMAIndicator

async def generate_signal(pair):
    try:
        # Convert Quotex format (EUR/USD -> EURUSD)
        symbol = pair.replace("/", "")

        # Get 1-minute candle data (last 100)
        url = f"https://api.binance.com/api/v3/klines?symbol={symbol.upper()}USDT&interval=1m&limit=100"
        response = requests.get(url)
        data = response.json()

        if not data or "code" in data:
            return None

        df = pd.DataFrame(data, columns=[
            'timestamp', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_asset_volume', 'trades',
            'taker_buy_base', 'taker_buy_quote', 'ignore'
        ])
        df['close'] = df['close'].astype(float)
        df['high'] = df['high'].astype(float)
        df['low'] = df['low'].astype(float)
        df['volume'] = df['volume'].astype(float)

        # Indicators
        rsi = RSIIndicator(df['close'], window=14).rsi()
        sma = SMAIndicator(df['close'], window=100).sma_indicator()

        # Support & Resistance zones (last 20 candles)
        recent_highs = df['high'].iloc[-20:]
        recent_lows = df['low'].iloc[-20:]
        resistance = recent_highs.max()
        support = recent_lows.min()
        last_price = df['close'].iloc[-1]

        zone = "Middle"
        if abs(last_price - resistance) < 0.02:
            zone = "Resistance"
        elif abs(last_price - support) < 0.02:
            zone = "Support"

        # Volume Spike
        recent_volume = df['volume'].iloc[-20:]
        vol_spike = df['volume'].iloc[-1] > recent_volume.mean()

        # Direction logic
        direction = "call" if rsi.iloc[-1] < 30 and last_price > sma.iloc[-1] else "put" if rsi.iloc[-1] > 70 and last_price < sma.iloc[-1] else None
        if not direction:
            return None

        # Confidence
        confidence = "HIGH" if vol_spike and zone in ["Support", "Resistance"] else "MEDIUM"

        return {
            "direction": direction,
            "rsi": round(rsi.iloc[-1], 2),
            "trend": "UP" if last_price > sma.iloc[-1] else "DOWN",
            "volume": "High" if vol_spike else "Normal",
            "zone": zone,
            "confidence": confidence
        }

    except Exception as e:
        print(f"Error generating signal: {e}")
        return None
