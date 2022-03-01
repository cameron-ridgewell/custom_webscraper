#### This program scrapes naukri.com's page and gives our result as a 
#### list of all the job_profiles which are currently present there. 
  
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

import os  # I think it's better to use subprocess for this. but quick code for example
import time
import urllib.parse
import csv

#email tools 
import smtplib, ssl
from email.mime.text import MIMEText

CSV_FILENAME = 'bottle_list.csv'
SECRETS_FILENAME = 'secrets.txt'
URL_PREFIX = 'https://www.abc.virginia.gov/products/all-products#q='
URL_SUFFIX = '&sort=relevancy&numberOfResults=12&f:Views=[49]'

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

    status = os.system('systemctl is-active --quiet chromium-driver')
    # print(status)

    print("Setting up options")
    return webdriver.Chrome(options=chrome_options)

def isInStock(bottle_name):
    url = URL_PREFIX + urllib.parse.quote(bottle_name) + URL_SUFFIX
    print("Fetching " + bottle_name + "... ", end='')
    driver.get(url)

    # this is just to ensure that the page is loaded
    time.sleep(5) 

    html = driver.page_source

    # this renders the JS code and stores all
    # of the information in static HTML code.

    soup = BeautifulSoup(html, "html.parser")

    search_results = soup.find_all('div',class_="col-sm-12 col-xs-8 pull-right-sm product-header")
    
    print("Done")
    if len(search_results) > 0:
        return True
    else:
        return False

def writeStocktoFile(bottle_stock):
    f = open(CSV_FILENAME, "w")
    f.write(bottle_stock)
    f.close()


def sendEmail(body):
    with open(SECRETS_FILENAME) as f:
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
    driver = createWebDriver()
    bottle_list_output = ''

    with open(CSV_FILENAME,'r', newline='') as csvfile:
        bottle_list_input = csv.DictReader(csvfile)
        
        fieldnames = ['title','stock']
        bottle_list_output = fieldnames[0] + ',' + fieldnames[1] + '\n'
        
        # Only send emails for things that were previously out of Stock
        for row in bottle_list_input:
            stockStatus = 'In Stock' if isInStock(row[fieldnames[0]]) else 'Out of Stock'
            if (row['stock'] == 'Out of Stock') and (stockStatus == 'In Stock'):
                sendEmail(row['title'] + " is In Stock!")
                pass
            bottle_list_output = bottle_list_output + row['title'] + ',' + stockStatus + '\n'
        #Updae CSV file
        writeStocktoFile(bottle_list_output)

    driver.close() # closing the webdriver
    driver.quit()



