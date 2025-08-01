import json
import os
import requests
from bs4 import BeautifulSoup
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# -------------------- Alert Storage --------------------
ALERT_FILE = "alerts.json"
alerts = {}  # Initialize global alerts dictionary

def save_alerts_to_file():
    try:
        with open(ALERT_FILE, "w") as f:
            json.dump(alerts, f, indent=2)
    except Exception as e:
        print(f"[ERROR] Saving alerts: {e}")

def load_alerts_from_file():
    global alerts
    if os.path.exists(ALERT_FILE):
        try:
            with open(ALERT_FILE, "r") as f:
                alerts = json.load(f)
        except Exception as e:
            print(f"[ERROR] Loading alerts: {e}")
# -------------------------------------------------------

# ------------------- Amazon Price ----------------------
def get_price_amazon(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept-Language": "en-US,en;q=0.9",
    }
    try:
        page = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(page.content, "html.parser")

        title = soup.find(id="productTitle")
        title = title.get_text().strip() if title else "Product"

        price_whole = soup.select_one(".a-price .a-offscreen")
        price = price_whole.get_text().replace("₹", "").replace(",", "").strip() if price_whole else "0"

        return title, float(price)
    except Exception as e:
        print(f"[ERROR] get_price_amazon: {e}")
        return None, None
# --------------------------------------------------------

# -------------------- Set Alert -------------------------
def set_alert(user_id, url, target_price):
    title, current_price = get_price_amazon(url)
    if not title or not current_price:
        return False, "❌ Product not found or unable to fetch data. Please check the URL."

    alert = {"url": url, "price": target_price, "title": title}
    if str(user_id) not in alerts:
        alerts[str(user_id)] = []
    alerts[str(user_id)].append(alert)

    save_alerts_to_file()  # Save after setting

    return True, f"✅ Alert set for:\n**{title}**\nCurrent Price: ₹{current_price}\nTarget Price: ₹{target_price}"
# ---------------------------------------------------------

# ------------------- Check Alerts ------------------------
def check_alerts(app):
    for user_id, user_alerts in list(alerts.items()):
        for alert in user_alerts[:]:  # use a copy of the list
            title, current_price = get_price_amazon(alert["url"])
            if current_price and current_price <= alert["price"]:
                try:
                    app.send_message(
                        chat_id=int(user_id),
                        text=f"📢 Price Drop Alert!\n\n**{title}**\nCurrent Price: ₹{current_price}\nTarget Price: ₹{alert['price']}\n\n🔗 [View Product]({alert['url']})",
                        reply_markup=InlineKeyboardMarkup(
                            [[InlineKeyboardButton("🔗 Open Link", url=alert["url"])]]
                        ),
                        disable_web_page_preview=True
                    )
                    user_alerts.remove(alert)  # remove sent alert
                    save_alerts_to_file()
                except Exception as e:
                    print(f"[ERROR] sending alert to {user_id}: {e}")
# ---------------------------------------------------------
