#scp ./scraper.py pi@pi:/home/pi/custom_webscraper/scraper.py
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By as By
from selenium.common.exceptions import NoSuchElementException


import os  # I think it's better to use subprocess for this. but quick code for example
import time
import urllib.parse
import csv
import re

#email tools 
import smtplib, ssl
from email.mime.text import MIMEText

CSV_FILENAME = 'bottle_list.csv'
SECRETS_FILENAME = 'secrets.txt'
ANGELSENVY_URL = 'https://www.abc.virginia.gov/products/bourbon/angels-envy-port-barrel-bourbon?productSize=0'
HIGHWEST_URL = 'https://www.abc.virginia.gov/products/rye/high-west-whiskey-double-rye?productSize=0'
LOGIN_URL = 'https://www.abc.virginia.gov/sso/gateway/login.do'


def createWebDriver():
    chrome_options = Options()
    # ChromeDriver is just AWFUL because every version or two it breaks unless you pass cryptic arguments
    #AGRESSIVE: options.setPageLoadStrategy(PageLoadStrategy.NONE); # https:#www.skptricks.com/2018/08/timed-out-receiving-message-from-renderer-selenium.html
    chrome_options.add_argument("start-maximized"); # https:#stackoverflow.com/a/26283818/1689770
    chrome_options.add_argument("enable-automation"); # https:#stackoverflow.com/a/43840128/1689770
    chrome_options.add_argument("--headless"); # only if you are ACTUALLY running headless
    chrome_options.add_argument("--no-sandbox"); #https:#stackoverflow.com/a/50725918/1689770
    chrome_options.add_argument("--disable-infobars"); #https:#stackoverflow.com/a/43840128/1689770
    chrome_options.add_argument("--disable-dev-shm-usage"); #https:#stackoverflow.com/a/50725918/1689770
    chrome_options.add_argument("--disable-browser-side-navigation"); #https:#stackoverflow.com/a/49123152/1689770
    chrome_options.add_argument("--disable-gpu"); #https:#stackoverflow.com/questions/51959986/how-to-solve-selenium-chromedriver-timed-out-receiving-message-from-renderer-exc

    # chrome_options.add_argument("--disable-extensions"); # disabling extensions
    # chrome_options.add_argument("--no-sandbox"); # Bypass OS security model
    # chrome_options.add_argument("--remote-debugging-port=9222")  # this


    status = os.system('systemctl is-active --quiet chromium-driver')
    # print(status)

    print("Setting up options")
    return webdriver.Chrome(options=chrome_options)

def login(driver):
    __location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
    with open(os.path.join(__location__, SECRETS_FILENAME),'r') as f:
        lines = f.readlines()
        username = lines[2].strip()
        password = lines[3].strip()

        print("Logging in")
        driver.get(LOGIN_URL)
        # print(driver.page_source)
        username_box = driver.find_element("id","login_loginId")
        password_box = driver.find_element("id","login_password")

        username_box.send_keys(username)
        password_box.send_keys(password)

        login_button = driver.find_element("id","login__execute")
        login_button.submit()

def isInStock(bottle_name, bottle_url):
    print("Fetching " + bottle_name + "... ", end='')
    driver.get(bottle_url)

    xpath = "//td[@data-title='Inventory']"
    try:
        inventory_count = driver.find_element(By.XPATH,xpath)
        print(re.search(r'\d+', inventory_count.text).group(0))
        return int(re.search(r'\d+', inventory_count.text).group(0)) > 0
    except NoSuchElementException:
        print("0\n" + bottle_name + " is not held in inventory")
        return False

def writeStocktoFile(bottle_stock):
    with open(os.path.join(__location__, CSV_FILENAME),'w') as f:
        f.write(bottle_stock)
        f.close()


def sendEmail(body):
    with open(os.path.join(__location__, SECRETS_FILENAME),'r') as f:
        lines = f.readlines()
        username = lines[0].strip()
        password = lines[1].strip()

        port = 465  # For SSL

        # Create a secure SSL context
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(username, password)

            msg = MIMEText(body)
            msg['Subject'] = body.title()
            msg['From'] = username
            msg['To'] = username
            server.sendmail(username, username, msg.as_string())

if __name__ == "__main__":
    try:
        driver = createWebDriver()
        bottle_list_output = ''

        login(driver)

        __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))
        with open(os.path.join(__location__, CSV_FILENAME),'r', newline='') as csvfile:
            bottle_list_input = csv.DictReader(csvfile)
            
            fieldnames = ['title','stock','url']
            bottle_list_output = fieldnames[0] + ',' + fieldnames[1] + ',' + fieldnames[2] + '\n'
            
            # Only send emails for things that were previously out of Stock
            for row in bottle_list_input:
                bottle_url = row['url']

                stockStatus = 'In Stock' if isInStock(row['title'],row['url']) else 'Out of Stock'
                if (row['stock'] == 'Out of Stock') and (stockStatus == 'In Stock'):
                    sendEmail(row['title'] + " is In Stock!")
                bottle_list_output = bottle_list_output + row['title'] + ',' + stockStatus + ',' + bottle_url + '\n'
            
            #Update CSV file
            writeStocktoFile(bottle_list_output)
    finally:
        driver.close() # closing the webdriver
        driver.quit()



