# bot.py

import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
)
from dotenv import load_dotenv
from signal_generator import generate_signal
from quotex_api_handler import QuotexAPIHandler
from utils.pairs import all_pairs

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
QUOTEX_EMAIL = os.getenv("QUOTEX_EMAIL")
QUOTEX_PASSWORD = os.getenv("QUOTEX_PASSWORD")

# Initialize Quotex API
quotex = QuotexAPIHandler()

user_selected_pairs = {}

# 📍 /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("🧠 Signal Generator", callback_data="signal_generator")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Welcome to Quotex Signal Bot 🚀", reply_markup=reply_markup)

# 🧠 Handle button click for Signal Generator
async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "signal_generator":
        keyboard = []
        row = []
        for idx, pair in enumerate(all_pairs):
            row.append(InlineKeyboardButton(pair, callback_data=f"pair_{pair}"))
            if (idx + 1) % 3 == 0:
                keyboard.append(row)
                row = []
        if row:
            keyboard.append(row)

        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("📊 Select a trading pair:", reply_markup=reply_markup)

    elif query.data.startswith("pair_"):
        pair = query.data.replace("pair_", "")
        user_selected_pairs[query.from_user.id] = pair

        # 🔄 Generate signal from strategy
        signal_data = await generate_signal(pair)

        if not signal_data:
            await query.edit_message_text(f"⚠️ No valid signal found for {pair}. Try again later.")
            return

        msg = f"""
🧠 Signal Generator Result
━━━━━━━━━━━━━━━━━━━━━━━
📊 Pair: {pair}
📈 Direction: {signal_data['direction'].upper()}
📉 RSI: {signal_data['rsi']}
📏 Trend: {signal_data['trend']}
📦 Volume: {signal_data['volume']}
🧱 Support/Resistance: {signal_data['zone']}
🎯 Confidence: {signal_data['confidence']}

— Powered by Ankit Singh AI
━━━━━━━━━━━━━━━━━━━━━━━
Do you want to place this trade?
"""

        confirm_buttons = [
            [
                InlineKeyboardButton("✅ YES", callback_data="confirm_trade"),
                InlineKeyboardButton("❌ NO", callback_data="cancel_trade")
            ]
        ]
        await query.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(confirm_buttons))

    elif query.data == "confirm_trade":
        user_id = query.from_user.id
        pair = user_selected_pairs.get(user_id)

        if not pair:
            await query.edit_message_text("⚠️ No pair selected. Please try again.")
            return

        await query.edit_message_text(f"📤 Placing trade for {pair}...")

        # 🔐 Ensure connection
        if not quotex.connected:
            await quotex.connect(QUOTEX_EMAIL, QUOTEX_PASSWORD)
            await quotex.change_account("PRACTICE")  # or "REAL"

        trade_id = await quotex.place_trade(pair, "call", 10, 60)  # Default settings for demo

        if not trade_id:
            await query.edit_message_text("❌ Trade failed. Please try again.")
            return

        await asyncio.sleep(60)
        is_win, result = await quotex.check_result(pair, trade_id)

        if is_win:
            await query.edit_message_text(f"✅ TRADE RESULT:\n{pair} - CALL\n💰 Profit: +${result:.2f} (WIN) 🎉")
        else:
            await query.edit_message_text(f"❌ TRADE RESULT:\n{pair} - CALL\n📉 Loss: -${-result:.2f} (LOSS)")

    elif query.data == "cancel_trade":
        await query.edit_message_text("❌ Trade cancelled by user.")

# ▶️ Main bot entry
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_button))
    app.run_polling()
