__author__ = "Nathan Evans"

import output, requests, threading, utility
from guess import *
from urlparse import urljoin

"""
Holds the parameters for authorization. Should have a length of either 0 or 3.
If the length is anything else, parameters were passed to it incorrectly, so
check the file that was passed to --custom-auth
AUTH[0] == the name of the app to log into
AUTH[1] == the username that should be used for logging in
AUTH[2] == the password that should be used for logging in
"""
AUTH = []

"""
The url that the crawler should start on. Once the crawl begins, if a url is 
discovered that doesn't begin with the BASE_URL, it will be ignored
"""
BASE_URL = ''

"""
A list of words to be used for guessing hidden urls and login credentials
"""
COMMON_WORDS = []

COMPILED_WORDS = {}
cLock = threading.Lock()
"""
The cookies gathered from crawling the web application. Should be passed to all
requests in this file to ensure the crawler remains logged in where necessary
"""
COOKIES = None#{'security': 'low'}

"""
A list of response objects that were found to have urls that exist within the
web application being tested
"""
DISCOVERED = []

"""
A lock for the DISCOVERED, to ensure that different threads aren't attempting
to write to the list at the same time
"""
discoLock = threading.Lock()

"""
A list of guessed urls that returned an error message
"""
FAILED_URLS = []

fLock = threading.Lock()

OUTPUT_TREE = None

"""
The list of spiderLeg threads. Used for coordinating the threads
"""
spiderLegs = []

"""
A thread used for the actual crawling of the web application
"""
class spiderLeg(threading.Thread):
	def __init__(self, startUrl):
		threading.Thread.__init__(self)
		
		#The url which the spiderLeg should begin crawling from
		self.startUrl = startUrl
		
	def run(self):
		crawlHelper(self.startUrl)

"""
used to check if a url has already been discovered by the spider in its current
run of the web application being tested

url - the url to be checked

returns - a boolean, True if the url has already been found, False otherwise
"""
def checkDiscoveredForUrl(url):
	global DISCOVERED
	eUrl = utility.unescape(url)
	discoLock.acquire()
	for r in DISCOVERED:
		for u in ([r.response]+r.response.history):
			if(eUrl == u.url):
				discoLock.release()
				return True
	discoLock.release()
	fLock.acquire()
	for u in FAILED_URLS:
		if(eUrl == u):
			fLock.release()
			return True		
	fLock.release()
	return False

def compileOutputTree():
	global DISCOVERED
	if(len(DISCOVERED) > 1):
		sorted = DISCOVERED #sortOutputObjects(DISCOVERED)
		for s in sorted[1:]:
			sorted[0].addChildPage(s)
		return sorted[0]
	elif(len(DISCOVERED) == 1):
		return DISCOVERED[0]
	
def sortOutputObjects(outputObjects=[]):
	if(len(outputObjects)==0):
		return outputObjects
	
	pivot = outputObjects[len(outputObjects)/2]
	first = outputObjects[0]
	last = outputObjects[len(outputObjects)-1]
	less = []
	eq = []
	more = []
	if((first.response.url >= pivot.response.url) and (first.response.url <= last.response.url)):
		pivot = first
	elif((last.response.url >= pivot.response.url)and(last.response.url <= first.response.url)):
		pivot = last
	
	for o in outputObjects:
		if(o.response.url < pivot.response.url):
			less.append(o)
		elif(o.response.url > pivot.response.url):
			more.append(o)
		else:
			eq.append(o)
	return (sortOutputObjects(less) + eq + sortOutputObjects(more))
	
"""
A method to populate the global variables BASE_URL, AUTH, and COMMON_WORDS, and
initialize a spiderLeg to begin crawling the web application.

url - the url from which the spider should begin crawling the web application,
this will be assigned to BASE_URL

auth - a list containing the authorization parameters that the spider should use
if the list is empty, the spider will not attempt to log in to the system. This
will be assigned to AUTH

commonWords - a list of strings to be used for guessing hidden pages and login credentials,
this will be assigned to COMMON_WORDS

returns - a list containing DISCOVERED, and COOKIES

"""
def crawl(url, auth=[], commonWords=[]):
	#Assign globals
	global AUTH
	AUTH = auth
	global BASE_URL
	BASE_URL = url
	global COMMON_WORDS
	COMMON_WORDS = commonWords
	global DISCOVERED
	#Start the crawl with a single spiderLeg
	fstLeg = spiderLeg(url)
	spiderLegs.append(fstLeg)
	fstLeg.start()
	
	for l in spiderLegs:
		l.join()
	DISCOVERED = sortOutputObjects(DISCOVERED)
	retList = [compileOutputTree(), COOKIES]
	retList.append(DISCOVERED)
	return retList

"""
Recursively crawls through the web application, adding valid response objects
to DISCOVERED, as representations of the valid web pages it has found
"""
def crawlHelper(url=""):
	global COOKIES
	global DISCOVERED

	#if the entered url has not been discovered yet
	if( not checkDiscoveredForUrl(url)):
		"""create a request object from the url and the cookies that have been
		found so far"""		
		r = getResponse(url)
		if(not (r == None)):
			#in case of redirects, add all responses from r's history to DISCOVERED
			o = output.outputTree(r)
			for x in r.history:
				if( not checkDiscoveredForUrl(x.url)):
					discoLock.acquire()
					DISCOVERED.append(output.outputTree(x))
					discoLock.release()
			print("r:\t"+r.url)
			discoLock.acquire()
			DISCOVERED.append(o)#output.outputTree(r))
			discoLock.release()
		
			cLock.acquire()
			commonWords.compileCommonWords(r, COMPILED_WORDS)
			cLock.release()
		
			#TEST HERE
		
			global BASE_URL
			
			pagesToCrawl = []
			for a in utility.getAllOnPage(r.text, "a"):
				pagesToCrawl.append(a.get('href'))
			pagesToCrawl.extend(guess.compileUrlGuesses(r.url, COMPILED_WORDS))
			
			#for every anchor tag on the discovered page
			for a in pagesToCrawl:
			
				#get the url of the anchor tag
				joinUrl = urljoin(r.url, a)#a.get('href'))
			
				testLen = len(BASE_URL) - 1
				#if the found url is an onsite link
				if((BASE_URL[:testLen] == joinUrl[:testLen]) & ("logout" not in joinUrl)):
					#see if any of the spiderLegs are sleeping threads
					inThread = utility.findInactiveThread(spiderLegs)
					
					#if so, tell it to begin crawling from the found url
					if( inThread != -1):
						deadLeg = spiderLegs[inThread]
						deadLeg.startUrl = joinUrl
						deadLeg.run()
					else:
						"""otherwise, create a new one, and tell it to begin its crawl
						from the found url"""
						newLeg = spiderLeg(joinUrl)
						spiderLegs.append(newLeg)
						newLeg.start()
			#if we hae reached the login page of the web application, attempt to login
			if((len(AUTH) == 3) and ("/login" in r.url) and (("/"+AUTH[0]+"/") in r.url)):
				login(r)
	#otherwise, release the lock
	else:
		pass


def getResponse(url=""):
	r = None
	try:
		r = requests.get(url, cookies=COOKIES)
	except exception:
		fLock.acquire()
		FAILED_URLS.append(url)
		fLock.release()
	finally:
		return r

"""
attempt to log into the web application being tested from the url represented
by the given request object

r - a request object representing the page that the url should attempt to login
from
"""
def login(r):
	global AUTH
	global COOKIES
	
	#find all input and option fields on the page
	inputs = utility.getAllOnPage(r.text, "input")
	inputs+= utility.getAllOnPage(r.text, "option")
	
	"""of the above inputs, narrow them down to the ones that are most likely
	to be used for loggin in"""
	userPassLog = []
	userPassLog.append(guess.findInput( ["username", "user"], inputs))
	userPassLog.append(guess.findInput( ["password", "pass"], inputs))
	userPassLog.append(guess.findInput( ["login", "loginbutton"], inputs))
	
	#if we can determine which fields are for logging in
	if(not (None in userPassLog)):
		"""assign the appropriate credentials to the fields for usernames and
		passwords"""
		loginInfo = {
			userPassLog[0].get("name") : AUTH[1],
			userPassLog[1].get("name") : AUTH[2],
			userPassLog[2].get("name") : userPassLog[2].get("value")
		}

		with requests.Session() as s:
			#login with the appropriate credentials
			p = s.post(r.url, data=loginInfo)
			
			#get the cookie
			q = s.get(p.url, cookies=COOKIES)
			COOKIES = s.cookies.get_dict()
			print("SUCCESSFUL LOGIN")
			print(COOKIES)
			
			#continue crawling the app from the logged in perspective
			crawlHelper(q.url)
			print("LOGIN CRAWL ENDED")
	else:
		print("Couldn't find login params")
