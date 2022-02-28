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
keywords = ["eagle rare","high west double rye","blanton","sazerac rye"]
url = "https://www.abc.virginia.gov/products/all-products#q=" + urllib.parse.quote(keywords[1]) + "&sort=relevancy&numberOfResults=12&f:Views=[49]"
print(url)


print("creating webdriver")
# initiating the webdriver. Parameter includes the path of the webdriver.
#driver = webdriver.Chrome() 
driver.get(url) 
  
# this is just to ensure that the page is loaded
time.sleep(5) 
  
html = driver.page_source
  
# this renders the JS code and stores all
# of the information in static HTML code.
  
# Now, we could simply apply bs4 to html variable
soup = BeautifulSoup(html, "html.parser")

search_results = soup.find_all('div',class_="col-sm-12 col-xs-8 pull-right-sm product-header")

if len(search_results) > 0:
  print("Out of Stock")
  
driver.close() # closing the webdriver
driver.quit()
