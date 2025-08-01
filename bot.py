import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.enums import ParseMode
from aiogram.filters import Command
from config import BOT_TOKEN, CHANNEL_ID
from utils.price_suggester import suggest_prices
from scraper.amazon import scrape_amazon
from scraper.flipkart import scrape_flipkart
from scraper.myntra import scrape_myntra
from handlers.alert_handler import save_alerts_to_file

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# Temporary in-memory user context for alert price setting
user_context = {}


# ------------------ FORCE JOIN CHECK ------------------ #
async def check_subscription(user_id):
    try:
        member = await bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False


# ------------------ /start Command ------------------ #
@dp.message(Command("start"))
async def start_handler(message: Message):
    user_id = message.from_user.id
    joined = await check_subscription(user_id)
    if not joined:
        join_btn = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🔔 Join Our Channel", url=f"https://t.me/c/{str(CHANNEL_ID).replace('-100', '')}")]
            ]
        )
        await message.answer("🚨 To use this bot, please join our deals channel first!", reply_markup=join_btn)
        return

    await message.answer("👋 Welcome to Price Tracker Bot!\n\nJust send me any product link from Flipkart, Amazon, or Myntra to get started.")


# ------------------ Product Link Handler ------------------ #
@dp.message(F.text.contains("amazon.in") | F.text.contains("flipkart.com") | F.text.contains("myntra.com"))
async def handle_product_link(message: Message):
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
        await message.answer("❌ Sorry, I couldn't fetch prices for this product.")
        return

    response = f"📦 <b>{product_name}</b>\n\n🔍 <b>Available On:</b>\n"
    buttons = []

    for platform, price, url in prices:
        response += f"{platform}: ₹{price}\n"
        buttons.append([
            InlineKeyboardButton(f"🛒 {platform} - Buy Now", url=url),
            InlineKeyboardButton(f"⏰ Set Alert - {platform}", callback_data=f"alert|{platform}|{price}|{url}")
        ])

    markup = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer(response, reply_markup=markup)


# ------------------ Alert Button Callback ------------------ #
@dp.callback_query(F.data.startswith("alert|"))
async def handle_alert_btn(callback_query: CallbackQuery):
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


# ------------------ Alert Price Input ------------------ #
@dp.message(F.text.regexp(r"^\d+$"))
async def set_alert_price(message: Message):
    data = user_context.get(message.from_user.id)
    if not data:
        return  # Not a reply to alert setup

    target_price = int(message.text)
    save_alert(message.from_user.id, data["platform"], data["url"], target_price)
    await message.answer(f"✅ Alert set! You'll be notified when price drops to ₹{target_price} or below.")
    user_context.pop(message.from_user.id, None)  # Clear context


# ------------------ Fallback for Other Text ------------------ #
@dp.message()
async def fallback(message: Message):
    await message.answer("❗ Please send a valid product link from Amazon, Flipkart, or Myntra.")


# ------------------ Main ------------------ #
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
