from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from collections import namedtuple
from datetime import datetime

Item = namedtuple("Item", "name stock")

def scrapeOverclockers(html):
	soup = BeautifulSoup(html, "html.parser")

	right = soup.find("div", {"class": "right"})

	header = right.find("h1")
	name = header.text.replace("\n", " ")[2:-1]

	button = right.find("input", {"id": "basketButton"})

	if button:
		return Item(name, True)

	return Item(name, False)

def scrapeScan(html):
	soup = BeautifulSoup(html, "html.parser")

	header = soup.find("h1", {"itemprop": "name"})
	name = header.text

	button = soup.find("div", {"class": "buyButton"})

	if button:
		return Item(name, True)

	return Item(name, False)

scrapers = {
	"www.scan.co.uk": scrapeScan,
	"www.overclockers.co.uk": scrapeOverclockers
}

if __name__ == "__main__":
	links = open("links.txt")

	for link in links.readlines():		
		url = urlparse(link.replace("\n", ""))

		if url.hostname not in scrapers:
			continue

		timestamp = datetime.now().strftime("%d/%m/%Y - %H:%m:%S:%f")

		try:
			request = Request(url.geturl(), headers={"User-Agent": ""})
			page = urlopen(request)

			item = scrapers[url.hostname](page.read())

			if item.stock == False:
				continue

			# do the thing
			print(item.name)

		except HTTPError as error:
			print(f"{timestamp}\n{error.reason}\n{url.geturl()}\n")
		except URLError as error:
			print(f"{timestamp}\n{error.reason}\n{url.geturl()}\n")