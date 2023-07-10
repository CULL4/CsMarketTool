import requests
from bs4 import BeautifulSoup
from currency_converter import CurrencyConverter
c = CurrencyConverter()
import time

items = []
def scrapeSA(): # scrapes item names of weapons with high volume/popularity from link(s) below
    HEADERS = {'User-Agent': 'Mozilla/5.0'}
    url = "https://csgo.steamanalyst.com/type/rifle/all/popular/"
    # url = "https://csgo.steamanalyst.com/type/rifle/all/volume/"

    r = requests.get(url, headers = HEADERS)
    soup = BeautifulSoup(r.text, 'html.parser') # if fails, use r.page_source instead

    divImg = soup.find_all('div', class_ = 'item-img') # Finds all <div class="item-img"
    for i in divImg:
        img = i.find('img') # goes into all divImg item and finds: <img alt="x" src="https://..."
        weapon = img.get('alt') # just grabs "x"
        if weapon is not None:
            weaponNoTm = weapon.replace('™','')
            items.append(weaponNoTm)
    # print(items)

buffLinkList = []
dNameAsKey = {}
def SaToBuff(): # takes item names from above def and gets their buff item ids
    with open('buffids.txt', encoding = 'utf-8') as id: # opens buffids txt file to turn it into dictionary
        for line in id:
            (key,value) = line.rstrip('\n').split(';')
            dNameAsKey[str(value)] = key
    for i in items:
        buffLinkList.append('https://buff.163.com/goods/' + dNameAsKey[i] + '?from=market#tab=selling') # takes list of items, compares to dictionary with ids, grabs item ID, turns into buff link for scrapingg
    # print(buffLinkList)


def scrapeBuff(): # scrapes item prices from buff, looks for items > 2.5% less $ then next highest priced listing
    HEADERS = {'User-Agent': 'Mozilla/5.0'}
    for i in buffLinkList:
        url = i

        r = requests.get(url, headers = HEADERS)
        soup = BeautifulSoup(r.text, 'html.parser')

        for x in soup.find_all('strong', class_='f_Strong', limit = 2): # debug with breakpoint here, chinese yuan currency sign broke program
            print(soup.get(x))






scrapeSA()
SaToBuff()
scrapeBuff()

    




