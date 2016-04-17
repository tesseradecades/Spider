__author__ = "Nathan Evans"

import requests

DISCOVERED = None

def crawl(url, auth=[], commonWords=[]):
	global DISCOVERED
	DISCOVERED = requests.get(url)
	print(DISCOVERED)
	print(auth)
	print(commonWords)