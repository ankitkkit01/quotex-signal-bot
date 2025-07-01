from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import os
from dotenv import load_dotenv

from signal_generator import generate_signal
from quotex_api_handler import QuotexAPIHandler
from utils.pairs import all_pairs

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
QUOTEX_EMAIL = os.getenv("QUOTEX_EMAIL")
QUOTEX_PASSWORD = os.getenv("QUOTEX_PASSWORD")

quotex = QuotexAPIHandler()
user_selected_pairs = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("🧠 Signal Generator", callback_data="signal_generator")]]
    await update.message.reply_text("Welcome to Quotex Signal Bot 🚀", reply_markup=InlineKeyboardMarkup(keyboard))

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    # existing button logic...

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_button))
    app.run_polling()
