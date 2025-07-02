import asyncio
from signal_generator import generate_signal
from utils.pairs import all_pairs
from utils.pairs import pair_buttons
from telegram import Bot
from dotenv import load_dotenv
import os
import random

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)

user_auto_mode = {}

async def auto_signal_loop(user_id):
    while user_auto_mode.get(user_id, False):
        pair = random.choice(list(pair_buttons.keys()))  # Only from valid pairs
        signal = await generate_signal(pair)

        if signal and float(signal['confidence'].replace('%', '')) >= 70:
            msg = f"""
🧠 Auto Signal (Live)
━━━━━━━━━━━━━━━━━━━━━━━
📊 Pair: {pair_buttons.get(pair, pair)}
📈 Direction: {signal['direction'].upper()}
📉 RSI: {signal['rsi']}
📏 Trend: {signal['trend']}
📦 Volume: {signal['volume']}
🧱 Support/Resistance: {signal['zone']}
🎯 Confidence: {signal['confidence']}

— Powered by Ankit Singh AI
━━━━━━━━━━━━━━━━━━━━━━━
"""
            try:
                await bot.send_message(chat_id=user_id, text=msg)
            except Exception as e:
                print(f"❌ Failed to send signal to {user_id}: {e}")
        
        await asyncio.sleep(45)  # Wait 45 sec then try again (to avoid overloading)

def enable_auto_for_user(user_id):
    user_auto_mode[user_id] = True

def disable_auto_for_user(user_id):
    user_auto_mode[user_id] = False

def is_auto_enabled(user_id):
    return user_auto_mode.get(user_id, False)
