import asyncio
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import BOT_TOKEN, CHANNEL_ID
from utils.price_suggester import suggest_prices
from scraper.amazon import get_amazon_price
from scraper.flipkart import get_flipkart_price
from scraper.myntra import get_myntra_price
from handlers.alert_handler import save_alert

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

# Temporary in-memory user context for alert price setting
user_context = {}

# ------------------ FORCE JOIN CHECK ------------------ #
async def check_subscription(user_id):
    try:
        member = await bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    joined = await check_subscription(user_id)
    if not joined:
        join_btn = InlineKeyboardMarkup().add(
            InlineKeyboardButton("🔔 Join Our Channel", url=f"https://t.me/c/{str(CHANNEL_ID).replace('-100', '')}"),
        )
        await message.answer("🚨 To use this bot, please join our deals channel first!", reply_markup=join_btn)
        return

    await message.answer("👋 Welcome to Price Tracker Bot!\n\nJust send me any product link from Flipkart, Amazon, or Myntra to get started.")


# ------------------ PRODUCT LINK HANDLER ------------------ #
@dp.message_handler(lambda message: any(x in message.text for x in ['amazon.in', 'flipkart.com', 'myntra.com']))
async def handle_product_link(message: types.Message):
    link = message.text
    product_name = "Example Product"  # Optional: add scraping for dynamic title

    prices = []
    if "amazon" in link:
        price = get_amazon_price(link)
        if price:
            prices.append(("Amazon", price, link))
    elif "flipkart" in link:
        price = get_flipkart_price(link)
        if price:
            prices.append(("Flipkart", price, link))
    elif "myntra" in link:
        price = get_myntra_price(link)
        if price:
            prices.append(("Myntra", price, link))

    if not prices:
        await message.reply("❌ Sorry, I couldn't fetch prices for this product.")
        return

    response = f"📦 <b>{product_name}</b>\n\n🔍 <b>Available On:</b>\n"
    buttons = InlineKeyboardMarkup(row_width=2)

    for platform, price, url in prices:
        response += f"{platform}: ₹{price}\n"
        buttons.add(
            InlineKeyboardButton(f"🛒 {platform} - Buy Now", url=url),
            InlineKeyboardButton(f"⏰ Set Alert - {platform}", callback_data=f"alert|{platform}|{price}|{url}")
        )

    await message.answer(response, reply_markup=buttons)


# ------------------ ALERT BUTTON HANDLER ------------------ #
@dp.callback_query_handler(lambda c: c.data.startswith("alert|"))
async def handle_alert_btn(callback_query: types.CallbackQuery):
    _, platform, price, url = callback_query.data.split("|")
    suggested = suggest_prices(int(price))

    suggest_text = "\n".join([f"🔹 ₹{p}" for p in suggested])
    await callback_query.message.answer(
        f"💡 <b>Set Alert</b>\n\nCurrent Price on {platform}: ₹{price}\n\n"
        f"🧠 Suggested Alert Prices:\n{suggest_text}\n\n"
        f"👉 Please reply with your target price (just the number)."
    )

    # Save context temporarily
    user_context[callback_query.from_user.id] = {
        "platform": platform,
        "url": url,
        "current_price": price
    }


@dp.message_handler(lambda message: message.text.isdigit())
async def set_alert_price(message: types.Message):
    data = user_context.get(message.from_user.id)
    if not data:
        return  # Not a reply to alert setup

    target_price = int(message.text)
    save_alert(message.from_user.id, data["platform"], data["url"], target_price)
    await message.reply(f"✅ Alert set! You'll be notified when price drops to ₹{target_price} or below.")

    user_context.pop(message.from_user.id, None)  # Clear context


# ------------------ DEFAULT HANDLER ------------------ #
@dp.message_handler()
async def fallback(message: types.Message):
    await message.reply("❗ Please send a valid product link from Amazon, Flipkart, or Myntra.")


# ------------------ MAIN ------------------ #
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
