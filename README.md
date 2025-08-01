# 📦 Price Tracker & Alert Telegram Bot

A powerful Telegram bot that helps you **track prices of products from e-commerce sites** (like Amazon, Flipkart, etc.) and notifies you when the price drops! 🛒📉

---

## ✨ Features

- 🔍 Track product prices via URL
- 📤 Instant alerts when price drops
- 🔁 Set desired price to get notified
- 💾 Save tracked items per user
- 🧾 Inline button interface — no commands!
- 📊 Built using Python + Pyrogram + BeautifulSoup

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/price-tracker-bot.git
cd price-tracker-bot
```

### 2. Create virtual environment (Optional but recommended)

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install requirements

```bash
pip install -r requirements.txt
```

---

## 🛠 Environment Variables

Create a `.env` file and add the following:

```
BOT_TOKEN=your_telegram_bot_token
API_ID=your_api_id
API_HASH=your_api_hash
OWNER_USERNAME=@your_username
```

---

## ▶️ Start the Bot

```bash
bash start.sh
```

Or directly:

```bash
python bot.py
```

---

## 🖥 Hosting (Heroku/Railway)

### ⚙️ `Procfile`

```
worker: bash start.sh
```

---

## 👤 Admin Commands

| Command | Description |
|--------|-------------|
| `/start` | Start the bot |
| `/myalerts` | View your saved alerts |
| `/clearalerts` | Remove all alerts |
| `/help` | Show help panel |

---

## 💡 Notes

- Supports **Amazon**, **Flipkart**, and more (can be extended).
- Use `requests + BeautifulSoup` for scraping.
- Safe for deployment on any server or VPS.

---

## 📸 Screenshots

_Coming soon..._

---

## 👨‍💻 Developer

Made with ❤️ by **[Aviii](https://t.me/aviii56)**

---

## 📜 License

MIT © 2025 Aviii
