# Custom Webscraper

Custom Webscraper is a testing script for rendering JS using Selenium and headless Chromedriver and scraping to relevant data. The test implementation uses a `bottles_list.csv` file to determine the names of rare alcohol bottles and search if they're available in my local ABC Liqour Store (#49)

A username and password are stored in a `secrets.txt` file to allow the script to send me an email if one of the bottles changes from being "Out of Stock" to "In Stock"

## Dependencies
Custom Webscraper uses Selenium and ChromeDriver to process webpages. Installation of these tools is covered elswhere and is device dependent. I am running on a Raspbery Pi 4

## Usage

I set up as a cronjob to run hourly as follows

`>> crontab -e`

and add the following line

`0 * * * * /usr/bin/python3 /home/pi/custom_webscraper/scraper.py`

where `/home/pi/custom_webscraper/scraper.py` is the location of the scraper script from this repository. Note that `bottle_list.csv` and `secrets.txt` will need to be in that same location to run correctly.

## License
[MIT](https://choosealicense.com/licenses/mit/)
