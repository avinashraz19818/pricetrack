import requests
from bs4 import BeautifulSoup

def scrape_croma(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")

    try:
        title = soup.select_one("h1.title").text
        price = soup.select_one("span.amount").text
        image = soup.select_one("img.product-image")["src"]
        return {"name": title, "price": price, "image": image, "site": "Croma"}
    except:
        return None
