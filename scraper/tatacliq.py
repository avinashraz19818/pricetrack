import requests
from bs4 import BeautifulSoup

def scrape_tatacliq(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")

    try:
        title = soup.select_one("h1.pdp-title").text.strip()
        price = soup.select_one("span.price").text.strip()
        image = soup.select_one("img.pdp-thumbnail-image")["src"]
        return {"name": title, "price": price, "image": image, "site": "TataCliq"}
    except:
        return None
