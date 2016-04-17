__author__ = "Nathan Evans"

import requests
from bs4 import BeautifulSoup
from urlparse import urljoin

AUTH = []
DISCOVERED = []
COMMON_WORDS = []


def crawl(url, auth=[], commonWords=[]):
	global AUTH
	AUTH = auth
	print(AUTH)
	global COMMON_WORDS
	COMMON_WORDS = commonWords
	print(COMMON_WORDS)
	crawlHelper(url)
	return DISCOVERED

def crawlHelper(url):
	global DISCOVERED
	if( not checkDiscoveredForUrl(url)):
		r = requests.get(url)

		DISCOVERED.append(r)
	
		for u in getUrlsOnPage(r):
			testLen = len(r.url) - 1
			if(r.url[:testLen] == u[:testLen]):
				print(u)
				crawlHelper(u)
	else:
		print("\nAlready discovered:\t"+url+"\n")
			
def getUrlsOnPage(r):
	links = []
	soup = BeautifulSoup(r.text, "html.parser")
	for u in soup.find_all('a'):
		link = urljoin(r.url, u.get('href'))
		links.append(link)
	return links

def checkDiscoveredForUrl(url):
	global DISCOVERED
	for r in DISCOVERED:
		if(r.url == url):
			return True
	return False