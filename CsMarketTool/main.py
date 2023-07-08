import requests
from bs4 import BeautifulSoup

def Rifle():
    HEADERS = {'User-Agent': 'Mozilla/5.0'}
    urlRifle = "https://csgo.steamanalyst.com/type/rifle/all/popular/"

    r = requests.get(urlRifle, headers = HEADERS)
    soup = BeautifulSoup(r.text, 'html.parser') # if fails, use r.page_source instead

    divImg = soup.find_all('div', class_ = 'item-img') # Finds all <div class="item-img"

    for item in divImg:
        img = item.find('img') # goes into all divImg item and finds: <img alt="x" src="https://..."
        weapon = img.get('alt') # just grabs "x"
        if weapon is not None:
            print (weapon)
        
# need to add def for other skin categories (pistols, smgs, sniper, cases)
# & ability to filter by price (doesn't show in url)

Rifle()