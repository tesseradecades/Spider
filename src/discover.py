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
	r = requests.get(url)

	DISCOVERED.append(r)
	
	for u in getUrlsOnPage(r):
		print(u)

def getUrlsOnPage(r):
	links = []
	soup = BeautifulSoup(r.text, "html.parser")
	for u in soup.find_all('a'):
		link = urljoin(r.url, u.get('href'))
		links.append(link)
	return links