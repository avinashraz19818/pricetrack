
import requests
from bs4 import BeautifulSoup

def scrape_nykaa(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")

    try:
        title = soup.select_one("h1.css-1gc4x7i").text
        price = soup.select_one("span.css-111z9ua").text
        image = soup.select_one("img.css-11gn9r6")["src"]
        return {"name": title, "price": price, "image": image, "site": "Nykaa"}
    except:
        return None
