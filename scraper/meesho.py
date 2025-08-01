import requests
from bs4 import BeautifulSoup

def scrape_meesho(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")

    try:
        title = soup.select_one("span.ProductTitle__Text").text
        price = soup.select_one("h4.ProductPrice__Price").text
        image = soup.select_one("img.Image__StyledImage-sc-1h8ic7x-0")["src"]
        return {"name": title, "price": price, "image": image, "site": "Meesho"}
    except:
        return None
