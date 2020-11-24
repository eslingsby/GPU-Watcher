from gpuwatcher.scrape import Item, add
from bs4 import BeautifulSoup

def scrapeScan(html):
	soup = BeautifulSoup(html, "html.parser")

	header = soup.find("h1", {"itemprop": "name"})
	name = header.text

	button = soup.find("div", {"class": "buyButton"})

	if button:
		return Item(name, True)

	return Item(name, False)

add("www.scan.co.uk", scrapeScan)