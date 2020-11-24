from gpuwatcher.scrape import Item, add
from bs4 import BeautifulSoup

def scrapeOverclockers(html):
	soup = BeautifulSoup(html, "html.parser")

	right = soup.find("div", {"class": "right"})

	header = right.find("h1")
	name = header.text.replace("\n", " ")[2:-1]

	button = right.find("input", {"id": "basketButton"})

	if button:
		return Item(name, True)

	return Item(name, False)

add("www.overclockers.co.uk", scrapeOverclockers)