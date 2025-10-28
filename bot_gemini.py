import sqlite3
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
import os

# --- Load API key dari file .env ---
load_dotenv("config/.env")

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# --- Konfigurasi Gemini API ---
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")


# --- Lokasi database ---
DB_PATH = "db/laptop.db"

# --- Fungsi untuk mencari laptop di database ---
def cari_laptop(kata_kunci):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        SELECT brand, model_name, cpu, ram, storage, gpu, price_idr, stock
        FROM laptop
        WHERE brand LIKE ? OR model_name LIKE ?
    """, (f'%{kata_kunci}%', f'%{kata_kunci}%'))
    hasil = cur.fetchall()
    conn.close()
    return hasil

# --- Fungsi untuk meminta jawaban dari Gemini ---
def tanya_gemini(prompt):
    response = model.generate_content(prompt)
    return response.text

# --- Handler Command /start ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Halo 👋! Saya asisten toko laptop.\n"
        "Ketik nama laptop atau pertanyaan seperti:\n"
        "🔹 'Apakah stok Asus Vivobook 15 masih ada?'\n"
        "🔹 'Laptop yang bagus buat desain grafis apa ya?'"
    )

# --- Handler Pesan Umum ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pesan_user = update.message.text
    data = cari_laptop(pesan_user)

    if data:  # Jika ditemukan di database
        jawaban = "Berikut laptop yang tersedia:\n\n"
        for row in data:
            brand, model_name, cpu, ram, storage, gpu, price_idr, stock = row
            jawaban += (
                f"💻 {brand} {model_name}\n"
                f"⚙️ CPU: {cpu}\n"
                f"🧠 RAM: {ram}\n"
                f"💾 Storage: {storage}\n"
                f"🎮 GPU: {gpu}\n"
                f"💰 Harga: Rp{price_idr:,.0f}\n"
                f"📦 Stok: {stock} unit\n\n"
            )
    else:
        # Jika tidak ada di database, gunakan AI Gemini
        prompt = (
            f"Kamu adalah asisten toko laptop yang ramah. "
            f"Jawab pertanyaan ini dengan sopan dan relevan: '{pesan_user}'"
        )
        jawaban = tanya_gemini(prompt)

    await update.message.reply_text(jawaban)

# --- Jalankan Bot ---
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Bot sedang berjalan...")
    app.run_polling()

if __name__ == "__main__":
    main()
