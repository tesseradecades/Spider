__author__ = "Nathan Evans"

import guess, requests, threading, unescapeString
from bs4 import BeautifulSoup
from urlparse import urljoin

AUTH = []
BASE_URL = ''
discoLock = threading.Lock()
DISCOVERED = []
COMMON_WORDS = []
COOKIES = None

spiderLegs = []

class spiderLeg(threading.Thread):
	def __init__(self, startUrl):
		threading.Thread.__init__(self)
		self.startUrl = startUrl
		
	def run(self):
		#print spiderLegs
		crawlHelper(self.startUrl)

def crawl(url, auth=[], commonWords=[]):
	global AUTH
	AUTH = auth
	
	global BASE_URL
	BASE_URL = url
	
	global COMMON_WORDS
	COMMON_WORDS = commonWords
	
	fstLeg = spiderLeg(url)
	spiderLegs.append(fstLeg)
	fstLeg.start()
	
	for l in spiderLegs:
		l.join()
	return DISCOVERED

def crawlHelper(url):
	global COOKIES
	global DISCOVERED
	discoLock.acquire()
	if( not checkDiscoveredForUrl(url)):
		#print("CRAWL HELPER")
		r = requests.get(url, cookies=COOKIES)
		for x in r.history:
			if( not checkDiscoveredForUrl(x.url)):
				DISCOVERED.append(x)
		#print(r.url)
		DISCOVERED.append(r)
		discoLock.release()
	
		global BASE_URL
		for u in getUrlsOnPage(r):
			testLen = len(BASE_URL) - 1
			if((BASE_URL[:testLen] == u[:testLen]) & ("logout" not in u)):
				inThread = findInactiveThread(spiderLegs)
				if( inThread != -1):
					deadLeg = spiderLegs[inThread]
					deadLeg.startUrl = u
					deadLeg.run()
				else:
					newLeg = spiderLeg(u)
					spiderLegs.append(newLeg)
					newLeg.start()
		if((len(AUTH) == 3) and ("/login" in r.url) and (("/"+AUTH[0]+"/") in r.url)):
			login(r)
	else:
		discoLock.release()

			
def findInactiveThread(threadList):
	i = 0
	for t in threadList:
		if(not t.isAlive()):
			return i
		i+=1
	return -1
			
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
		for u in ([r]+r.history):
			if(unescapeString.unescape(url) == u.url):
				return True
	return False

def login(r):
	global AUTH
	global COOKIES
	inputs = getInputsOnPage(r)
	userPassLog = []
	userPassLog.append(guess.findInput( ["username", "user"], inputs))
	userPassLog.append(guess.findInput( ["password", "pass"], inputs))
	userPassLog.append(guess.findInput( ["login", "loginbutton"], inputs))
	if(not (None in userPassLog)):
		loginInfo = {
			userPassLog[0].get("name") : AUTH[1],
			userPassLog[1].get("name") : AUTH[2],
			userPassLog[2].get("name") : userPassLog[2].get("value")
		}

		with requests.Session() as s:
			p = s.post(r.url, data=loginInfo)
			q = s.get(p.url, cookies=COOKIES)
			COOKIES = s.cookies.get_dict()
			print("LOGIN")
			print(COOKIES)
			crawlHelper(q.url)
			print("LOGIN CRAWL ENDED")			
	else:
		print("Couldn't find login params")

def getInputsOnPage(r):
	inputs = []
	soup = BeautifulSoup(r.text, "html.parser")
	for i in (soup.find_all('input')+soup.find_all('option')):
		inputs.append(i)
	return inputs
