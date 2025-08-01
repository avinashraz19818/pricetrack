import requests
from bs4 import BeautifulSoup

def scrape_snapdeal(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")

    try:
        title = soup.select_one("h1.pdp-e-i-head").text
        price = soup.select_one("span.payBlkBig").text
        image = soup.select_one("img.cloudzoom")["src"]
        return {"name": title, "price": "₹" + price, "image": image, "site": "Snapdeal"}
    except:
        return None
