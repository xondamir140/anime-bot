from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import json

# === JSON fayldan anime ma'lumotlarini yuklash ===
with open("anime_data.json", "r", encoding="utf-8") as f:
    anime_data = json.load(f)

# === /start buyrug'i ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(studio, callback_data=f"studio_{studio}")]
        for studio in anime_data.keys()
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "👋 Salom! Qaysi dublyaj studiyasini tanlaysiz?",
        reply_markup=reply_markup
    )

# === Tanlovlarni boshqarish ===
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # Dublyaj studiyasi tanlanganda
    if data.startswith("studio_"):
        studio = data.replace("studio_", "")
        keyboard = [
            [InlineKeyboardButton("Telegram", callback_data=f"platform_{studio}_telegram")],
            [InlineKeyboardButton("YouTube", callback_data=f"platform_{studio}_youtube")],
            [InlineKeyboardButton("Sayt", callback_data=f"platform_{studio}_site")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text=f"🎧 Siz {studio} studiyasini tanladingiz.\nQayerda ko‘rmoqchisiz?",
            reply_markup=reply_markup
        )

    # Platforma tanlanganda
    elif data.startswith("platform_"):
        _, studio, platform = data.split("_")
        keyboard = [
            [InlineKeyboardButton(anime, callback_data=f"anime_{studio}_{anime}")]
            for anime in anime_data[studio].keys()
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text=f"🎬 {studio} studiyasidagi animelar ro‘yxati:",
            reply_markup=reply_markup
        )

    # Anime tanlanganda
    elif data.startswith("anime_"):
        _, studio, anime = data.split("_", 2)
        info = anime_data[studio][anime]
        text = (
            f"🎞 <b>{anime}</b>\n"
            f"🇯🇵 {info['japanese']}\n"
            f"🇬🇧 {info['english']}\n"
            f"🇷🇺 {info['russian']}\n"
            f"📅 Yaratilgan yili: {info['year']}\n\n"
            f"Sezonni tanlang:"
        )
        keyboard = [
            [InlineKeyboardButton(season, callback_data=f"season_{studio}_{anime}_{season}")]
            for season in info["seasons"].keys()
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text=text, reply_markup=reply_markup, parse_mode="HTML"
        )

    # Sezon tanlanganda
    elif data.startswith("season_"):
        _, studio, anime, season = data.split("_", 3)
        episodes = anime_data[studio][anime]["seasons"][season]
        text = f"📺 <b>{anime}</b> — {season}\n\n"
        for ep in episodes:
            text += f"🎥 <a href='{ep['link']}'>{ep['name']}</a>\n"
        await query.edit_message_text(text=text, parse_mode="HTML")

# === Botni ishga tushirish ===
async def main():
    app = ApplicationBuilder().token("8115689920:AAGpSQnpo-i5OusuiLGe1MXjiJzzM4nGAME").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_callback))

    print("🤖 Bot ishga tushdi...")
    await app.run_polling()

if __name__ == "__main__":
    import nest_asyncio
    import asyncio

    nest_asyncio.apply()
    asyncio.get_event_loop().run_until_complete(main())
from flask import Flask
import threading

app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host="0.0.0.0", port=8080)

threading.Thread(target=run).start()