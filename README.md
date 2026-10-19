# Telegram Customer Support Auto-Reply Bot

A lightweight, in-memory auto-reply bot built with Python. It automatically responds to users with a beautifully formatted support message, then enforces a 30-minute cooldown per user to prevent spam. 

It includes a threaded Flask web server to satisfy Render's port-binding requirements and allow pinging via UptimeRobot.

## Deployment on Render

1. Go to your [Render Dashboard](https://dashboard.render.com/) and create a new **Web Service** (not a Background Worker, because we need to expose the Flask port).
2. Connect your GitHub repository containing these files.
3. Use the following configurations:
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python main.py`
4. Go to the **Environment** tab and add your variable:
   - Key: `TELEGRAM_BOT_TOKEN`
   - Value: `your_telegram_bot_token_here`
5. Save and deploy.

## Keeping it awake with UptimeRobot

Render spins down free Web Services after 15 minutes of inactivity. To prevent this:
1. Copy the `.onrender.com` URL from your Render dashboard (e.g., `https://my-support-bot.onrender.com`).
2. Go to [UptimeRobot](https://uptimerobot.com/).
3. Add a new **HTTP(s) Monitor**.
4. Paste your Render URL.
5. Set the monitoring interval to **5 minutes** and save. 

The UptimeRobot pings the Flask server, keeping the Telegram polling thread alive 24/7.
