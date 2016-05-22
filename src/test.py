__author__="Nathan Evans"

import random, requests, threading, utility

"""
a list of messages you would expect to see if the system being tested caught
you when you tried to hack it
"""
caughtHackingList = ["Hacking attempt detected and logged."]

"""
A method to see if the system being tested has successfully caught the spider
trying to test it.
tP - a response object representing the page that has been tested
r - the response object that was created when testing the page
return - an integer value. -1 if the spider was not caught hacking, else, the
index of the output message in caughtHackingList
"""
def caughtHacking(tP, r):
	if(r == None):
		return False
	i = 0
	for c in caughtHackingList:
		before = tP.text.lower().split(c.lower())
		after = r.text.lower().split(c.lower())
		if(len(before) != len(after)):
			return i
		i+=1
	return -1

"""
A method to check if a particular attack was successful
tP - a response object representing the page that has been tested
r - the response object that was created when testing the page
return - a boolean value, True if the attack was successful, else False
"""
def checkAttackSuccess(tP, r, sensitive=[]):
	#print("checkAttackSuccess")
	if(r == None):
		return False
	for word in sensitive:
		before = tP.text.split(word)
		after = r.text.split(word)
		if(len(before) != len(after)):
			return True
		
	return False

def recursiveTestPage(testTree, vectors=[], sensitive=[], slow=500.0, cook=''):
	print("to be implemented later")
	
"""
tests a single page for the vulnerabilities represented by a list of vectors
tP - the page to be tested
vectors - the list of vectors to test on the page
sensitive - a list of strings that. None of these strings should appear on the
test page unless one of the tested attack vectors is successful in attacking
the application
slow - the number of milliseconds that the spider should wait before a response
should be considered too slow. Should the response time exceed this amount, the
web page will be noted as having a potential denial of service vulnerability
cook - the cookies the may be needed to remain logged into the system while
testing
returns - a 2-D list representation of the test page and any attack vectors
that were successful. ex) [response, ["Potential Denial of Service", "'or'1'=='1',..."]]
"""
def testPage(tP, iPuts=[], vectors=[], sensitive=[], slow=500.0, cook=''):
	print("Test page:\t"+tP.response.url)
	retList = [tP]
	dosExcept = "Potential Denial of Service"
	successfulVectors=[]
	"""
	iPuts = utility.getAllOnPage(tP.text, "input")
	iPuts+= utility.getAllOnPage(tP.text, "options")"""
	if(len(iPuts)==0):
		successfulVectors.append("no input fields to attack")
	time_out = (float(slow)/1000.0)
	#print(time_out)
	#print(cook)
	print("BROKEN BEFORE FOR LOOP")
	for v in vectors:
		#print("vector:\t"+v)
		for i in iPuts:
			iName = str(i.get('name'))
			#print("input:\t"+str(iName))
			r=None
			try:
				r = requests.post(tP.response.url, data={iName:v}, timeout=(float(slow)/1000.0), cookies=cook)
			except requests.exceptions.ConnectTimeout:
				if( not dosExcept in successfulVectors):
					successfulVectors.append(dosExcept)
			except requests.exceptions.ReadTimeout:
				if( not dosExcept in successfulVectors):
					successfulVectors.append(dosExcept)
			caught = caughtHacking(tP.response, r)
			if(checkAttackSuccess(tP.response, r, sensitive)):
				print("SUCCESSFUL VECTOR!")
				successfulVectors.append(iName+":    "+v)
			elif(caught != -1):
				print(caughtHackingList[caught])
				successfulVectors.append("Caught Hacking input:"+iName+" with vector:"+v)
	print("BROKEN AFTER FOR LOOP")
	if(len(successfulVectors)==0):
		successfulVectors.append("No Successful Attacks")
	tP.vulnerabilities=successfulVectors

"""
tests a given list of web pages for common vulnerabilities
pages - a list of response objects representing web pages
vectors - a list of input vulnerabilities to test for
sensitive - a list of strings that should only be visible on the web page if a
vector has successfully attacked the application
rand - a boolean value to determine whether to randomly test a single input
field on a single web page for a single vector (if True), or to test every
field on every web page for every vector in vectors (if False)
slow - the number of milliseconds that the spider should wait before a response
should be considered too slow. Should the response time exceed this amount, the
web page will be noted as having a potential denial of service vulnerability
returns - a 3-D list representing the tested pages and the vulnerabilities they
were found to have. ex) [[response, ["Potential Denial of Service", "'or'1'=='1'", ...]]]
"""
def testPages(pagesAndCookies=[], vectors=[], sensitive=[], rand=False, slow=500):
	print("testPages")
	if(len(pagesAndCookies) == 0):
		print("no pages")
		return pagesAndCookies
	retList = []
	
	discoTree = pagesAndCookies[0]
	#get the necessary cookie in case the spider needs to be logged in
	cookie = pagesAndCookies[1]
	discoList = pagesAndCookies[2]
	if(rand):
		print("True rando")
		tP = random.choice(discoList)#[random.randrange(len(discoList)-1)]
		iPuts = utility.getAllOnPage(tP.response.text, "input")
		iPuts+= utility.getAllOnPage(tP.response.text, "options")
		if(len(iPuts) > 0):
			iPuts = [random.choice(iPuts)]
		else:
			iPuts = []
		testVector = random.choice(vectors)#[random.randrange(len(vectors)-1)]
		testPage(tP, iPuts, [testVector], sensitive, slow, cookie)
		print("LOOKING FOR TP VULNS HERE")
		print(tP.vulnerabilities)
		retList = [tP]+pagesAndCookies[1:]
	else:
		recusiveTestPage(discoTree, vectors, sensitive, slow, cookie)
		retList
	return retList