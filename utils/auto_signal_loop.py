import asyncio
from signal_generator import generate_signal
from utils.pairs import pair_buttons
from telegram import Bot
from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)

user_auto_mode = {}

async def auto_signal_loop(user_id):
    while user_auto_mode.get(user_id, False):
        for pair_code in pair_buttons.keys():
            signal = await generate_signal(pair_code)

            if signal:
                msg = f"""
🧠 Auto Signal (Live)
━━━━━━━━━━━━━━━━━━━━━━━
📊 Pair: {pair_buttons.get(pair_code)}
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
                    print(f"[Auto Signal Error] {e}")
                await asyncio.sleep(180)  # wait 3 minutes after a valid signal
                break  # break loop to wait before checking again

        await asyncio.sleep(5)  # Small pause before checking again

def enable_auto_for_user(user_id):
    user_auto_mode[user_id] = True

def disable_auto_for_user(user_id):
    user_auto_mode[user_id] = False

def is_auto_enabled(user_id):
    return user_auto_mode.get(user_id, False)
