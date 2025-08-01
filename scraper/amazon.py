import requests
from bs4 import BeautifulSoup

def scrape_amazon(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")

    try:
        title = soup.select_one("#productTitle").get_text(strip=True)
        price = soup.select_one(".a-price .a-offscreen").get_text(strip=True)
        image = soup.select_one("#landingImage")["src"]
        return {"name": title, "price": price, "image": image, "site": "Amazon"}
    except:
        return None 

