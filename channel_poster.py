import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.client.session.aiohttp import AiohttpSession
from config import BOT_TOKEN, CHANNEL_ID
from handlers.alert_handler import get_all_alerts
from scraper.amazon import get_amazon_price
from scraper.flipkart import get_flipkart_price
from scraper.myntra import get_myntra_price
from scraper.ajio import get_ajio_price
from scraper.croma import get_croma_price
from scraper.meesho import get_meesho_price
from scraper.nykaa import get_nykaa_price
from scraper.reliancedigital import get_reliancedigital_price
from scraper.snapdeal import get_snapdeal_price
from scraper.tatacliq import get_tatacliq_price


async def post_best_deals():
    session = AiohttpSession()
    bot = Bot(token=BOT_TOKEN, parse_mode="HTML", session=session)
    # Removed unused Dispatcher instance

    alerts = get_all_alerts()
    posted_urls = set()  # Avoid duplicate posts

    for alert in alerts:
        platform = alert.get("platform")
        url = alert.get("url")
        user_target = alert.get("target_price")

        # Fetch latest price based on platform
        current_price = None
        if "amazon" in url:
            current_price = get_amazon_price(url)
        elif "flipkart" in url:
            current_price = get_flipkart_price(url)
        elif "myntra" in url:
            current_price = get_myntra_price(url)
        elif "ajio" in url:
            current_price = get_ajio_price(url)
        elif "croma" in url:
            current_price = get_croma_price(url)
        elif "meesho" in url:
            current_price = get_meesho_price(url)
        elif "nykaa" in url:
            current_price = get_nykaa_price(url)
        elif "reliancedigital" in url:
            current_price = get_reliancedigital_price(url)
        elif "snapdeal" in url:
            current_price = get_snapdeal_price(url)
        elif "tatacliq" in url:
            current_price = get_tatacliq_price(url)

        if current_price is None:
            continue  # Skip if price couldn't be fetched

        # Check if price is at or below target
        if current_price <= int(user_target) and url not in posted_urls:
            posted_urls.add(url)

            # Format and send message
            text = (
                f"🔔 <b>Price Drop Alert!</b>\n\n"
                f"📦 <b>Platform:</b> {platform}\n"
                f"💰 <b>New Price:</b> ₹{current_price}\n"
                f"🔗 <a href='{url}'>Click here to view product</a>\n\n"
                f"🔥 Buy before it’s gone!"
            )

            button = types.InlineKeyboardMarkup(inline_keyboard=[
                [types.InlineKeyboardButton(text="🛒 Buy Now", url=url)]
            ])

            try:
                await bot.send_message(chat_id=CHANNEL_ID, text=text, reply_markup=button, disable_web_page_preview=False)
            except Exception as e:
                print(f"❌ Error posting to channel: {e}")

    await bot.session.close()


if __name__ == "__main__":
    asyncio.run(post_best_deals())
