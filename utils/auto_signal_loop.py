# utils/auto_signal_loop.py

import asyncio
import os
from signal_generator import generate_signal
from utils.pairs import pair_buttons  # Only flag-based pairs
from telegram import Bot
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)

# Store user auto mode status
user_auto_mode = {}

async def auto_signal_loop(user_id):
    while user_auto_mode.get(user_id, False):
        for pair in pair_buttons.keys():
            if not user_auto_mode.get(user_id, False):
                break  # Stop if auto mode is disabled

            signal = await generate_signal(pair)

            if signal and int(signal['confidence'].replace('%', '')) >= 70:
                msg = f"""
🧠 Auto Signal (Live)
━━━━━━━━━━━━━━━━━━━━━━━
📊 Pair: {pair_buttons[pair]}
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
                    print(f"[AutoSignal] Error sending message: {e}")
                await asyncio.sleep(2)  # Delay between pair checks
        await asyncio.sleep(60)  # 1-minute delay before re-scanning all pairs

# Enable/disable handlers
def enable_auto_for_user(user_id):
    user_auto_mode[user_id] = True

def disable_auto_for_user(user_id):
    user_auto_mode[user_id] = False

def is_auto_enabled(user_id):
    return user_auto_mode.get(user_id, False)
