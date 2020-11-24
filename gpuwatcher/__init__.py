from gpuwatcher.scrape import scrape
from gpuwatcher.scrapers import *

def run(file):
	links = open(file)
	scrape(links.readlines())