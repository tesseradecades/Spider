__author__ = "Nathan Evans"

import guess, requests
from bs4 import BeautifulSoup
from urlparse import urljoin

AUTH = []
DISCOVERED = []
COMMON_WORDS = []
COOKIES = None


def crawl(url, auth=[], commonWords=[]):
	global AUTH
	AUTH = auth
	
	global COMMON_WORDS
	COMMON_WORDS = commonWords
	
	crawlHelper(url)
	return DISCOVERED

def crawlHelper(url):
	global COOKIES
	global DISCOVERED
	if( not checkDiscoveredForUrl(url)):
		r = requests.get(url, cookies=COOKIES)
		COOKIES = r.cookies.get_dict()
		
		DISCOVERED.append(r)
	
		for u in getUrlsOnPage(r):
			testLen = len(r.url) - 1
			if(r.url[:testLen] == u[:testLen]):
				print(u)
				crawlHelper(u)
		if(AUTH):
			login(r)
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

def login(r):
	global AUTH
	if( AUTH[0] in r.url):
		inputs = getInputsOnPage(r)
		userPassLog = []
		userPassLog.append(guess.findInput( ["username", "user"], inputs))
		userPassLog.append(guess.findInput( ["password", "pass"], inputs))
		userPassLog.append(guess.findInput( ["login", "loginbutton"], inputs))
		if(None not in userPassLog):
			global COOKIES
			loginInfo = {
				userPassLog[0].get("name") : AUTH[1],
				userPassLog[1].get("name") : AUTH[2],
				userPassLog[2].get("name") : userPassLog[2].get("value")
			}
			with requests.Session() as s:
				p = s.post(r.url, data=loginInfo, cookies=COOKIES)
				q = s.get(p.url, cookies=COOKIES)
				COOKIES = s.cookies.get_dict()
				crawlHelper(q.url)"""
				print("\n\n\nLOGGED IN SUCCESSFULLY!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n\n")
				for x in userPassLog:
					print("\n\n")
					print(x)
				quit()"""
				
		else:
			print("Couldn't find login params")

def getInputsOnPage(r):
	inputs = []
	soup = BeautifulSoup(r.text, "html.parser")
	for i in (soup.find_all('input')+soup.find_all('option')):
		inputs.append(i)
	return inputs