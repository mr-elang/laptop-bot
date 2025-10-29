from flask import Flask
import threading
import bot_gemini  # file bot kamu

app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 Laptop Bot is running on Render!"

def run_bot():
    try:
        print("🚀 Menjalankan bot di thread terpisah...")
        bot_gemini.main()
    except Exception as e:
        print("❌ Error menjalankan bot:", e)

if __name__ == "__main__":
    # Jalankan bot di thread terpisah agar Flask tetap hidup
    threading.Thread(target=run_bot).start()
    # Jalankan Flask di port yang diberikan oleh Render
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
