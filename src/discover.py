__author__ = "Nathan Evans"

import guess, requests, threading, utility
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
A list of words to be used for guessing hidden urls and login credentials
"""
COMMON_WORDS = []

"""
The cookies gathered from crawling the web application. Should be passed to all
requests in this file to ensure the crawler remains logged in where necessary
"""
COOKIES = None#{'security': 'low'}

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
	for r in DISCOVERED:
		for u in ([r]+r.history):
			if(utility.unescape(url) == u.url):
				return True
	return False

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
	
	#Start the crawl with a single spiderLeg
	fstLeg = spiderLeg(url)
	spiderLegs.append(fstLeg)
	fstLeg.start()
	
	for l in spiderLegs:
		l.join()
	
	return DISCOVERED+[COOKIES]

"""
Recursively crawls through the web application, adding valid response objects
to DISCOVERED, as representations of the valid web pages it has found
"""
def crawlHelper(url):
	global COOKIES
	global DISCOVERED
	
	"""acquire the lock on DISCOVERED so that we may check whether the entered 
	url has already been discovered"""
	discoLock.acquire()
	
	#if the entered url has not been discovered yet
	if( not checkDiscoveredForUrl(url)):
		"""create a request object from the url and the cookies that have been
		found so far"""		
		r = requests.get(url, cookies=COOKIES)
		#in case of redirects, add all responses from r's history to DISCOVERED
		for x in r.history:
			if( not checkDiscoveredForUrl(x.url)):
				DISCOVERED.append(x)
		print(r.url)
		DISCOVERED.append(r)
		discoLock.release()
	
		global BASE_URL
		
		#for every anchor tag on the discovered page
		for a in utility.getAllOnPage(r.text, "a"):
		
			#get the url of the anchor tag
			joinUrl = urljoin(r.url, a.get('href'))
		
			testLen = len(BASE_URL) - 1
			#if the found url is an onsite link
			if((BASE_URL[:testLen] == joinUrl[:testLen]) & ("logout" not in joinUrl)):
				#see if any of the spiderLegs are sleeping threads
				inThread = findInactiveThread(spiderLegs)
				
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
		discoLock.release()

"""
Searches a list for sleeping threads

threadList - the list to be searched

return - if all threads in the list are alive, return -1, else return the index
of the first sleeping thread in the list
"""
def findInactiveThread(threadList=[]):
	i = 0
	for t in threadList:
		if(not t.isAlive()):
			return i
		i+=1
	return -1

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
			
			"""
			inThread = findInactiveThread(spiderLegs)
			if( inThread != -1):
				deadLeg = spiderLegs[inThread]
				deadLeg.startUrl = q.url
				deadLeg.run()
			else:
				newLeg = spiderLeg(q.url)
				spiderLegs.append(newLeg)
				newLeg.start()
			"""
	else:
		print("Couldn't find login params")
