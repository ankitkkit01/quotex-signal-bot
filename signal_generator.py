from quotexpy.new import Quotex
import random

# Initialize Quotex with your login
quotex = Quotex()

# Dummy RSI, Trend, Volume logic
def get_dummy_analysis(pair):
    return {
        "direction": random.choice(["call", "put"]),
        "rsi": round(random.uniform(30, 70), 2),
        "trend": random.choice(["UP", "DOWN", "SIDEWAYS"]),
        "volume": random.randint(100, 1000),
        "zone": random.choice(["Support", "Resistance"]),
        "confidence": f"{random.randint(65, 95)}%"
    }

# This will be used in bot.py
async def generate_signal(pair):
    try:
        print(f"[Signal] Generating signal for: {pair}")
        data = get_dummy_analysis(pair)
        return data
    except Exception as e:
        print(f"[Signal] Error generating signal: {e}")
        return None
