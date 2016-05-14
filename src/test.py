__author__="Nathan Evans"

import random, requests, utility

def testPages(pages=[], vectors=[], sensitive=[], rand=False, slow=500):
	print("testPages")
	if(len(pages) == 0):
		print("no pages")
		return pages
	retList = []
	if(rand):
		print("True rando")
		testPage = pages[random.randrange(len(pages)-1)]
		retList = [testPage]
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
		retList.append(successfulVectors)
	print retList
	return retList

def checkAttackSuccess(r, sensitive=[]):
	return True
