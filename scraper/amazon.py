import requests
from bs4 import BeautifulSoup

def scrape_amazon(url):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/115.0.0.0 Safari/537.36"
        )
    }

    try:
        page = requests.get(url, headers=headers, timeout=10)
        if page.status_code != 200:
            return None

        soup = BeautifulSoup(page.content, "html.parser")

        title = soup.select_one("#productTitle")
        price = (
            soup.select_one(".a-price .a-offscreen") or
            soup.select_one("#priceblock_ourprice") or
            soup.select_one("#priceblock_dealprice")
        )
        image = soup.select_one("#landingImage")

        if not (title and price and image):
            return None

        return {
            "name": title.get_text(strip=True),
            "price": price.get_text(strip=True),
            "image": image.get("src"),
            "site": "Amazon"
        }

    except Exception as e:
        return None
