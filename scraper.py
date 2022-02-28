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

print("generating options")
chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
#chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox") # linux only
chrome_options.add_argument("--headless")
chrome_options.headless = True # also works

status = os.system('systemctl is-active --quiet chromium-driver')
print(status)

print("setting up options")
driver = webdriver.Chrome(options=chrome_options)

#url of the page we want to scrape
with open('bottle_list.csv','r', newline='') as csvfile:
    bottle_list = csv.DictReader(csvfile)

#with open('bottle_list.csv','w', newline='') as csvfile_out:
#    fieldnames = ['title','stock']
#    output_bottle_list = csv.DictWriter(csvfile,fieldnames=fieldnames)
#    output_bottle_list.writeheader()

    for row in bottle_list:
#        print(row['title'])
        url = "https://www.abc.virginia.gov/products/all-products#q=" + urllib.parse.quote(row['title']) + "&sort=relevancy&numberOfResults=12&f:Views=[49]"
#        print(url)
        driver.get(url) 

# this is just to ensure that the page is loaded
        time.sleep(5) 

        html = driver.page_source

        # this renders the JS code and stores all
        # of the information in static HTML code.
  
        # Now, we could simply apply bs4 to html variable
        soup = BeautifulSoup(html, "html.parser")

        search_results = soup.find_all('div',class_="col-sm-12 col-xs-8 pull-right-sm product-header")

        stock_status = ""
        print(row['title'].capitalize(), end=': ')
        if len(search_results) > 0:
            print("In Stock")
            stock_status = "In Stock"
        else:
            print("Out of Stock")
            stock_status = "Out of Stock"

driver.close() # closing the webdriver
driver.quit()
