import asyncio
from telegram import Bot
from utils.pairs import all_pairs
from utils.auto_controller import is_auto_enabled
from signal_generator import generate_signal
import os

bot = Bot(token=os.getenv("BOT_TOKEN"))

async def auto_signal_loop():
    while True:
        try:
            for user_id in list(is_auto_enabled().keys()):
                if is_auto_enabled()[user_id]:
                    for pair in all_pairs:
                        signal = await generate_signal(pair)
                        if signal:
                            msg = f"""
