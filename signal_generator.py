from quotexpy.new import Quotex

# Dummy function — aapke actual analysis functions se replace karein
def get_rsi(pair): return 42.5
def get_trend(pair): return "DOWN"
def get_volume(pair): return 865
def get_support_resistance(pair): return "Support"

# Initialize Quotex
quotex = Quotex()

# Signal Generator with Confidence Score
async def generate_signal(pair):
    try:
        print(f"[Signal] Generating signal for: {pair}")
        
        rsi = get_rsi(pair)
        trend = get_trend(pair)
        volume = get_volume(pair)
        zone = get_support_resistance(pair)

        score = 0
        if 30 <= rsi <= 70:
            score += 25
        if trend in ["UP", "DOWN"]:
            score += 25
        if volume > 400:
            score += 25
        if zone in ["Support", "Resistance"]:
            score += 25

        confidence = score
        if confidence < 60:
            return None  # signal skip if weak

        direction = "call" if trend == "UP" else "put"

        return {
            "direction": direction,
            "rsi": round(rsi, 2),
            "trend": trend,
            "volume": volume,
            "zone": zone,
            "confidence": confidence
        }

    except Exception as e:
        print(f"[Signal] Error generating signal: {e}")
        return None
