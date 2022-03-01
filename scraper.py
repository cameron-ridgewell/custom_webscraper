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

def createWebDriver():
    print("generating options")
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
    print(status)

    print("setting up options")
    return webdriver.Chrome(options=chrome_options)

def isInStock(bottle_name):
    url = "https://www.abc.virginia.gov/products/all-products#q=" + urllib.parse.quote(bottle_name) + "&sort=relevancy&numberOfResults=12&f:Views=[49]"
    driver.get(url) 

    # this is just to ensure that the page is loaded
    time.sleep(5) 

    html = driver.page_source

    # this renders the JS code and stores all
    # of the information in static HTML code.

    soup = BeautifulSoup(html, "html.parser")

    search_results = soup.find_all('div',class_="col-sm-12 col-xs-8 pull-right-sm product-header")

    if len(search_results) > 0:
        return True
    else:
        return False

def sendEmail(body):
    with open("secrets.txt") as f:
        lines = f.readlines()
        username = lines[0].strip()
        password = lines[1].strip()
        print(f"USERNAME={username}, PASSWORD={password}")
        port = 465  # For SSL

        # Create a secure SSL context
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(username, password)
            message = body
            server.sendmail(username, username, message)

if __name__ == "__main__":
    # sendEmail("hello")
    with open('bottle_list.csv','r', newline='') as csvfile:
        bottle_list = csv.DictReader(csvfile)

        driver = createWebDriver()

        for row in bottle_list:
            stockStatus = "In Stock" if isInStock(row['title']) else "Out of Stock"
            print(row['title'].title() + ": " + stockStatus)


    driver.close() # closing the webdriver
    driver.quit()



