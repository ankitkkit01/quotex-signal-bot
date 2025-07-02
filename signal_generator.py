# signal_generator.py

from quotexpy.new import Quotex
import ta
import random

# Login properly
quotex = Quotex()
quotex.login(email="arhimanshya@gmail.com", password="12345678an")

def get_live_analysis(pair):
    # Replace with your real signal logic here
    return {
        "direction": random.choice(["call", "put"]),
        "rsi": round(random.uniform(40, 70), 2),
        "trend": random.choice(["UP", "DOWN"]),
        "volume": random.randint(500, 1000),
        "zone": random.choice(["Support", "Resistance"]),
        "confidence": f"{random.randint(70, 95)}%"
    }

async def generate_signal(pair):
    try:
        print(f"[Signal] Generating for {pair}")
        return get_live_analysis(pair)
    except Exception as e:
        print(f"[Signal] Error: {e}")
        return None
