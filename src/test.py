__author__="Nathan Evans"

import random, requests, utility

def testPages(pages=[], vectors=[], sensitive=[], rand=False, slow=500):
	print("testPages")
	if(len(pages) == 0):
		print("no pages")
		return pages
	retList = []
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
		trueTestPages = pages[:len(pages)-1]
		for p in trueTestPages:
			retList.append(testPage(p, vectors, sensitive, slow, cookie))
	print retList
	return retList

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
