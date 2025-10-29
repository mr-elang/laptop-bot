from flask import Flask
import threading
import bot_gemini  # file bot kamu

app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 Laptop Bot is running on Railway!"

def run_bot():
    try:
        print("🚀 Menjalankan bot di thread terpisah...")
        bot_gemini.main()
    except Exception as e:
        print("❌ Error menjalankan bot:", e)

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
