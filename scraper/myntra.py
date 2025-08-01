import requests
from bs4 import BeautifulSoup

def scrape_myntra(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")

    try:
        title = soup.select_one("h1.pdp-title").text + " " + soup.select_one("h1.pdp-name").text
        price = soup.select_one("span.pdp-price").text
        image = soup.select_one("img.image-grid-image")["src"]
        return {"name": title, "price": price, "image": image, "site": "Myntra"}
    except:
        return None
