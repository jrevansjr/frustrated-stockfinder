#Libraries from internet example, although I don't utilize implicit wait, I have libraries commented out below for potential future development
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import random
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from pushover import Client
from xsxDataDict import clientName, tokenName, headers, driverPath
from Sites import sites

client = Client(clientName, api_token=tokenName)

class Stockfinder:
    def __init__(self):
        # chose not to utilize a proxy or various chrome options but have listed below potential options
        # PROXY = "socks5://IP Adress"
        chrome_options = Options()
        chrome_options.add_argument("--incognito") 
        # chrome_options.add_argument('--no-sandbox') 
        # chrome_options.add_argument("--headless") can alternatively options.headless = True
        self.driver = webdriver.Chrome(driverPath, options=chrome_options)

    def selenium(self, source, url, target, selector):
        # some websites block requests or don't explicitly list if item is sold out, selenium is method chosen for these websites
        self.driver.get(url)
        wait = WebDriverWait(self.driver, 5)
        # close microsoft popup
        if source == "microsoft":
            self.closePop()
        # some websites are easier to identify target by class rather than just id
        if selector == "id":
            try:
                button = wait.until(EC.visibility_of_element_located((By.ID, target)))
            except:
                print("INCORRECT ID LOCATOR")
                return "ERROR"
        elif selector == "css":
            try:
                button = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, target)))
            except:
                print("INCORRECT CSS LOCATOR")
                return "ERROR"
        elif selector == "xpath":
            try:
                button = wait.until(EC.visibility_of_element_located((By.XPATH,target)))
            except:
                print("INCORRECT XPATH LOCATOR")
                return "ERROR"
        else:
                print("SELECTOR ERROR")    
                return "ERROR"
        # checks if add to cart button is enabled
        if button.is_enabled() == True:
            return "IN STOCK"
        else:
            return "OUT OF STOCK"

    def api(self, url, section, target, selector):
        # some websites utilizes Captchas or explicitly list if an item is in stock. 
        # need to spoof header to get specific product data.
        page = requests.get(url, headers = headers)
        pageSoup = BeautifulSoup(page.content, 'html.parser')
        # some websites filtering product header is easier by css, section could be fleshed out better
        if selector=="id":
            results = pageSoup.find(id=section)
        elif selector=="css":
            results = pageSoup.find(class_=section)
        else:
            print("SELECTOR ERROR")
            return "ERROR"
        # occasionally website will return an error when called, resolved by next loop
	if results.getText() is None:
            print("SOUP ERROR WILL RESOLVE NEXT CALL")
            return "ERROR"
        # some websites are not consistant and may utilize a variety of tags in their product header to indicate stock (eg. pick up, in stock, add to cart). Option to search for various targets
        if type(target) == str:
            target = [target]
        # loops throughh all potential targets to find a hit
        hits = 0
	for i in target:
            hits = hits + int(i in results.getText())
        if hits > 0:
            return "IN STOCK"
        else:
            return "OUT OF STOCK"
        
    def diagnostics(self, scrapeType, source, url):
        # diagnostics to take snapshot of page to improve code
        if scrapeType == "selenium":
            diagnosticsText = self.driver.page_source
        else:
            diagnosticsText = requests.get(url,headers=headers).text
        # saves file in USER folder
        with open("diagnostics.htm",'w',encoding="utf-8") as f:
            f.write(diagnosticsText)
            f.close()

    def sendMessage(self, link, location):
        client.send_message(link, title=location)
    
    def closePop(self):
        try:
            wait = WebDriverWait(self.driver, 5)
            wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='c-dialog f-flow']/div[@class='sfw-dialog']/div['c-glyph glyph-cancel']"))).click()
        except:
            pass
    
def main():
    sf = Stockfinder()
    
    finder = False
    while finder == False:
        print('Current run time: ', datetime.now())
        for site in sites:
            #determines if selenium or requests library is needed to scrape website
            if site.get("type") == "selenium":
                returnStatus = sf.selenium(site.get("source"),site.get("url"),site.get("target"),site.get("selector"))
            elif site.get("type") == "api":
                returnStatus = sf.api(site.get("url"),site.get("section"),site.get("target"),site.get("selector"))
            else:
                returnStatus = "ERROR"
           
            #notifies user via pushover app if either function returns an in stock response
            if returnStatus == "OUT OF STOCK":
                print("no Stock: "+site.get("source") + ", "+site.get("item"))
            elif returnStatus == "ERROR":
                print("ERROR: "+site.get("source")+","+site.get("item")+","+site.get("url"))
            else:
                sf.sendMessage(site.get("url"), "IN STOCK: "+site.get("source").upper()+", "+site.get("item").upper())
                print("IN STOCK: "+site.get("source").upper()+", "+site.get("item").upper())
                sf.diagnostics(site.get("type"),site.get("source"),site.get("url"))
                finder = True
        # sleeps random interval between 30 and 90 seconds then restarts
        time.sleep(random.uniform(30,120))
    sf.driver.quit()

if __name__ == "__main__":
	main()
