#!/bin/bash

echo "🚀 Starting Price Tracker Bot..."

# Check if venv folder exists, if not create one
if [ ! -d "venv" ]; then
  echo "🛠️ Creating virtual environment..."
  python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
if [ -f requirements.txt ]; then
  echo "📦 Installing Python dependencies from requirements.txt..."
  pip install -r requirements.txt
else
  echo "⚠️ requirements.txt not found!"
fi

# Export environment variables from .env file if it exists
if [ -f .env ]; then
  echo "🔐 Loading environment variables from .env..."
  export $(grep -v '^#' .env | xargs)
else
  echo "⚠️ .env file not found!"
fi

# Start the bot
echo "🚀 Running bot.py..."
python3 bot.py
