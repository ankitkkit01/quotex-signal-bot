# bot.py

import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from dotenv import load_dotenv
from signal_generator import generate_signal
from utils.pairs import pair_buttons

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
user_selected_pairs = {}

# Start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("🧠 Signal Generator", callback_data="signal_generator")]]
    await update.message.reply_text("🚀 Welcome to Quotex Signal Bot", reply_markup=InlineKeyboardMarkup(keyboard))

# Button Handling
async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "signal_generator":
        keyboard, row = [], []
        for idx, code in enumerate(pair_buttons.keys()):
            row.append(InlineKeyboardButton(pair_buttons[code], callback_data=f"pair_{code}"))
            if (idx + 1) % 3 == 0:
                keyboard.append(row)
                row = []
        if row:
            keyboard.append(row)
        await query.edit_message_text("📊 Select Pair:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data.startswith("pair_"):
        pair = query.data.replace("pair_", "")
        user_selected_pairs[query.from_user.id] = pair
        signal = await generate_signal(pair)

        if not signal:
            await query.edit_message_text(f"⚠️ No valid signal for {pair}.")
            return

        flagged = pair_buttons.get(pair, pair)
        msg = f"""
🧠 Signal Generator Result
━━━━━━━━━━━━━━━━━━━━━━━
📊 Pair: {flagged}
📈 Direction: {signal['direction'].upper()}
📉 RSI: {signal['rsi']}
📏 Trend: {signal['trend']}
📦 Volume: {signal['volume']}
🧱 Zone: {signal['zone']}
🎯 Confidence: {signal['confidence']}
━━━━━━━━━━━━━━━━━━━━━━━
— Powered by Ankit Singh AI
"""
        await query.edit_message_text(msg)

# App
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_button))
    app.run_polling()
