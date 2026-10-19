import os
import time
import logging
from threading import Thread
from flask import Flask
import telebot

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ==========================================
# 1. FLASK KEEP-ALIVE SERVER
# ==========================================
app = Flask(__name__)

@app.route('/')
def home():
    return "Customer Support Bot is running!"

def run_flask():
    # Render assigns a dynamic port, defaulting to 8080 if running locally
    port = int(os.environ.get("PORT", 8080))
    # Disable Flask's default request logging to keep the console clean
    import logging as flask_logging
    flask_logging.getLogger('werkzeug').setLevel(flask_logging.ERROR)
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_flask)
    t.daemon = True
    t.start()

# ==========================================
# 2. TELEGRAM BOT LOGIC
# ==========================================
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN environment variable is missing.")

bot = telebot.TeleBot(TOKEN)

# In-memory dictionary: { user_id: timestamp_of_last_reply }
user_last_reply = {}
COOLDOWN_SECONDS = 30 * 60  # 30 minutes in seconds

@bot.message_handler(func=lambda message: True)
def handle_incoming_message(message):
    user_id = message.from_user.id
    current_time = time.time()

    # Check cooldown memory
    if user_id in user_last_reply:
        time_elapsed = current_time - user_last_reply[user_id]
        if time_elapsed < COOLDOWN_SECONDS:
            logger.info(f"Ignored message from {user_id} (Cooldown: {int(COOLDOWN_SECONDS - time_elapsed)}s left)")
            return

    # Update timestamp and reply
    user_last_reply[user_id] = current_time
    
    reply_text = (
        "✨ <b>Thanks for contacting Customer Support!</b>\n\n"
        "We have received your message. Our team is currently assisting other users, "
        "but we will get back to you within <b>2-3 hours</b>.\n\n"
        "<i>Thank you for your patience! 🙏</i>"
    )
    
    try:
        bot.reply_to(message, reply_text, parse_mode="HTML")
        logger.info(f"Sent auto-reply to {user_id}")
    except Exception as e:
        logger.error(f"Failed to send reply to {user_id}: {e}")

if __name__ == "__main__":
    logger.info("Starting Flask keep-alive server...")
    keep_alive()
    
    logger.info("Starting Telegram Bot...")
    # infinity_polling prevents the bot from crashing on minor connection errors
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
