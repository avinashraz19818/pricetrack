import requests
from bs4 import BeautifulSoup

def scrape_ajio(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")

    try:
        title = soup.select_one("div.product-title").text
        price = soup.select_one("div.price .prod-sp").text
        image = soup.select_one("img#previewImage")["src"]
        return {"name": title, "price": price, "image": image, "site": "AJIO"}
    except:
        return None
