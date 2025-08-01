import requests
from bs4 import BeautifulSoup

def scrape_flipkart(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")

    try:
        title = soup.select_one("span.B_NuCI").text
        price = soup.select_one("div._30jeq3").text
        image = soup.select_one("img._396cs4._2amPTt._3qGmMb")["src"]
        return {"name": title, "price": price, "image": image, "site": "Flipkart"}
    except:
        return None
