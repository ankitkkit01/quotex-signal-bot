# bot.py

import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
)
from dotenv import load_dotenv
from signal_generator import generate_signal
from utils.pairs import pair_buttons
from utils.auto_controller import enable_auto_mode, disable_auto_mode, is_auto_enabled
from quotexpy.new import Quotex
from auto_signal_sender import start_auto_signal_loop

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
quotex = Quotex()
user_selected_pairs = {}

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("🧠 Signal Generator", callback_data="signal_generator")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Welcome to Quotex Signal Bot 🚀", reply_markup=reply_markup)

# /startauto command
async def start_auto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    enable_auto_mode(user_id)
    await update.message.reply_text("✅ Auto Mode Activated! You'll now receive signals automatically.")
    asyncio.create_task(start_auto_signal_loop(update, context))

# /stopauto command
async def stop_auto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    disable_auto_mode(user_id)
    await update.message.reply_text("🛑 Auto Mode Stopped. You will no longer receive automatic signals.")

# Handle buttons
async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "signal_generator":
        keyboard, row = [], []
        for idx, pair_code in enumerate(pair_buttons.keys()):
            display_name = pair_buttons[pair_code]
            row.append(InlineKeyboardButton(display_name, callback_data=f"pair_{pair_code}"))
            if (idx + 1) % 3 == 0:
                keyboard.append(row)
                row = []
        if row:
            keyboard.append(row)
        await query.edit_message_text("📊 Select a trading pair:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data.startswith("pair_"):
        pair = query.data.replace("pair_", "")
        user_selected_pairs[query.from_user.id] = pair

        signal_data = await generate_signal(pair)
        if not signal_data:
            await query.edit_message_text(f"⚠️ No valid signal found for {pair}. Try again later.")
            return

        flagged_pair = pair_buttons.get(pair, pair)

        msg = f"""
🧠 Signal Generator Result
━━━━━━━━━━━━━━━━━━━━━━━
📊 Pair: {flagged_pair}
📈 Direction: {signal_data['direction'].upper()}
📉 RSI: {signal_data['rsi']}
📏 Trend: {signal_data['trend']}
📦 Volume: {signal_data['volume']}
🧱 Support/Resistance: {signal_data['zone']}
🎯 Confidence: {signal_data['confidence']}

— Powered by Ankit Singh AI
━━━━━━━━━━━━━━━━━━━━━━━
"""
        await query.edit_message_text(msg)

# Run the bot
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("startauto", start_auto))
    app.add_handler(CommandHandler("stopauto", stop_auto))
    app.add_handler(CallbackQueryHandler(handle_button))
    app.run_polling()
