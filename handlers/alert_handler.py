import requests
from bs4 import BeautifulSoup
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

alerts = {}  # Format: {user_id: [{'url': ..., 'price': ..., 'title': ...}, ...]}

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


def set_alert(user_id, url, target_price):
    title, current_price = get_price_amazon(url)
    if not title or not current_price:
        return False, "❌ Product not found or unable to fetch data. Please check the URL."

    alert = {"url": url, "price": target_price, "title": title}
    if user_id not in alerts:
        alerts[user_id] = []
    alerts[user_id].append(alert)

    return True, f"✅ Alert set for:\n**{title}**\nCurrent Price: ₹{current_price}\nTarget Price: ₹{target_price}"


def check_alerts(app):
    for user_id, user_alerts in alerts.items():
        for alert in user_alerts:
            title, current_price = get_price_amazon(alert["url"])
            if current_price and current_price <= alert["price"]:
                try:
                    app.send_message(
                        chat_id=user_id,
                        text=f"📢 Price Drop Alert!\n\n**{title}**\nCurrent Price: ₹{current_price}\nTarget Price: ₹{alert['price']}\n\n🔗 [View Product]({alert['url']})",
                        reply_markup=InlineKeyboardMarkup(
                            [[InlineKeyboardButton("🔗 Open Link", url=alert["url"])]]
                        ),
                        disable_web_page_preview=True
                    )
                    user_alerts.remove(alert)  # Remove alert after notifying
                except Exception as e:
                    print(f"[ERROR] sending alert to {user_id}: {e}")
