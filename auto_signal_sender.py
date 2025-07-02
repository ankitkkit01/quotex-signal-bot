# auto_signal_sender.py

import asyncio
from signal_generator import generate_signal
from utils.pairs import all_pairs
from utils.auto_controller import get_all_auto_users
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

async def auto_signal_loop(application):
    while True:
        print("[AutoMode] Checking all pairs for signals...")

        for pair in all_pairs:
            signal = await generate_signal(pair)
            if signal and int(signal["confidence"].replace('%','')) >= 75:
                msg = f"""
📡 Auto Signal Detected
━━━━━━━━━━━━━━━━━━━━━━━
📊 Pair: {pair}
📈 Direction: {signal['direction'].upper()}
📉 RSI: {signal['rsi']}
📏 Trend: {signal['trend']}
📦 Volume: {signal['volume']}
🧱 Support/Resistance: {signal['zone']}
🎯 Confidence: {signal['confidence']}

— Powered by Ankit Singh AI
━━━━━━━━━━━━━━━━━━━━━━━
"""

                # Send to all users with AutoMode enabled
                for user_id in get_all_auto_users():
                    try:
                        await application.bot.send_message(chat_id=user_id, text=msg)
                    except Exception as e:
                        print(f"[AutoMode] Failed to send signal to {user_id}: {e}")

        await asyncio.sleep(120)  # Wait 2 minutes before next scan
