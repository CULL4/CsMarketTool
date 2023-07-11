import pickle
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from currency_converter import CurrencyConverter
c = CurrencyConverter()

items = []
def scrapeSA(): # scrapes item names of weapons with high volume/popularity from link(s) below
    HEADERS = {'User-Agent': 'Mozilla/5.0'}
    url = "https://csgo.steamanalyst.com/type/rifle/all/popular/"
    #url = "https://csgo.steamanalyst.com/type/rifle/all/volume/"

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
    with open('assets/buffids.txt', encoding = 'utf-8') as id: # opens buffids txt file to turn it into dictionary
        for line in id:
            (key,value) = line.rstrip('\n').split(';')
            dNameAsKey[str(value)] = key
    for i in items:
        buffLinkList.append('https://buff.163.com/goods/' + dNameAsKey[i] + '?from=market#tab=selling&page_num=1') # takes list of items, compares to dictionary with ids, grabs item ID, turns into buff link for scrapingg
    # print(buffLinkList)


def scrapeBuff(): # scrapes item prices from buff, looks for items > 2.5% less $ then next highest priced listing
    headOption = webdriver.ChromeOptions()
    headOption.add_experimental_option('excludeSwitches', ['enable-logging'])
    #headOption.add_argument("--headless")
    for i in buffLinkList:
        driver = webdriver.Chrome(options=headOption)
        cookies = pickle.load(open("assets/cookies.pkl", "rb"))
        driver.execute_cdp_cmd('Network.enable', {})               #tbh i have no idea how this works, but it does. 
        for cookie in cookies:                                     #uses cookies to login to selenium tabs on buff
            driver.execute_cdp_cmd('Network.setCookie', cookie)
        driver.execute_cdp_cmd('Network.disable', {})

        driver.get(i)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        left = soup.find_all('td','t_Left', limit = 8)
        cnyList = []
        for x in left:
            strong = x.find('strong','f_Strong')
            if strong:
                cnyList.append(strong.get_text().replace('¥','').replace(' ',''))
                if len(cnyList) == 2:
                    perc = ((float(cnyList[1])-float(cnyList[0]))/(float(cnyList[0])+float(cnyList[1]))/2)*100
                    if perc > 2.5:
                        print('Found ' + str(perc) + " % profit: " + i)
                    else:
                        print('no good: ' + str(perc))
                    cnyList = []
        #driver.close()


    

scrapeSA()
SaToBuff()
scrapeBuff()

    




