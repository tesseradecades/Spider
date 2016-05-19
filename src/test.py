__author__="Nathan Evans"

import random, requests, utility

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
def testPages(pages=[], vectors=[], sensitive=[], rand=False, slow=500):
	print("testPages")
	if(len(pages) == 0):
		print("no pages")
		return pages
	retList = []
	
	#get the necessary cookie in case the spider needs to be logged in
	cookie = pages[len(pages)-1]
	if(rand):
		print("True rando")
		tP = pages[random.randrange(len(pages)-1)]
		retList.append(testPage(tP, vectors, sensitive, slow, cookie))
		"""retList = [testPage]
		successfulVectors=[]
		for v in vectors:
			#get inputs here
			iPuts = utility.getAllOnPage(testPage.text, "input")
			iPuts += utility.getAllOnPage(testPage.text, "options")
			
			if(len(iPuts) == 0):
				break
			i = iPuts[random.randrange(len(iPuts))]
			
			try:
				r = requests.post(testPage.url, data={i.get('name'):v}, timeout=(float(slow)/1000.0), cookies=pages[len(pages)-1])
				#check if attack was successful here
				if(checkAttackSuccess(r, sensitive)):
					successfulVectors.append(i.get('name')+":\t"+v)
				
			except requests.exceptions.ConnectTimeout:
				if( not ("Potential Denial of Service" in successfulVectors)):
					successfulVectors.append("Potential Denial of Service")
			except requests.exceptions.ReadTimeout:
				if( not ("Potential Denial of Service" in successfulVectors)):
					successfulVectors.append("Potential Denial of Service")
		if(len(successfulVectors)==0):
			successfulVectors.append("No successful attacks")
		retList.append(successfulVectors)"""
	else:
		#a list conataining pages w/o the cookies
		trueTestPages = pages[:len(pages)-1]
		for p in trueTestPages:
			retList.append(testPage(p, vectors, sensitive, slow, cookie))
	print retList
	return retList

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
def testPage(tP, vectors=[], sensitive=[], slow=500.0, cook=''):
	print("Test page:\t"+tP.url)
	retList = [tP]
	dosExcept = "Potential Denial of Service"
	successfulVectors=[]
	iPuts = utility.getAllOnPage(tP.text, "input")
	iPuts+= utility.getAllOnPage(tP.text, "options")
	
	for v in vectors:
		print("vector:\t"+v)
		for i in iPuts:
			iName = str(i.get('name'))
			#print("input:\t"+str(iName))
			try:
				print("try")
				
				r = requests.post(tP.url, data={iName:v}, timeout=(float(slow)/1000.0), cookies=cook)
				if(checkAttackSuccess(r, sensitive)):
					successfulVectors.append(iName+":\t"+v)
			except requests.exceptions.ConnectTimeout:
				if( not dosExcept in successfulVectors):
					successfulVectors.append(dosExcept)
			except requests.exceptions.ReadTimeout:
				if( not dosExcept in successfulVectors):
					successfulVectors.append(dosExcept)
	if(len(successfulVectors)==0):
		successfulVectors.append("No Successful Attacks")
	retList.append(successfulVectors)
	return retList

def checkAttackSuccess(r, sensitive=[]):
	print("checkAttackSuccess")
	return True
