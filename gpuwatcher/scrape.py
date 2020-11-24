from gpuwatcher.notify import notify

from urllib.parse import urlparse
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from collections import namedtuple
from datetime import datetime

Item = namedtuple("Item", "name stock")

addedScrapers = {}

def add(url, function):
	addedScrapers[url] = function

def scrape(links):
	for link in links:		
		url = urlparse(link.replace("\n", ""))

		if url.hostname not in addedScrapers:
			continue

		timestamp = datetime.now().strftime("%d/%m/%Y - %H:%m:%S:%f")

		try:
			request = Request(url.geturl(), headers={"User-Agent": ""})
			page = urlopen(request)

			item = addedScrapers[url.hostname](page.read())

			if item.stock == False:
				continue

			# do the thing
			print(item.name)

		except HTTPError as error:
			print(f"{timestamp}\n{error.reason}\n{url.geturl()}\n")
		except URLError as error:
			print(f"{timestamp}\n{error.reason}\n{url.geturl()}\n")