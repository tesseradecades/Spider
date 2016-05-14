__author__="Nathan Evans"

import random, requests

def testPages(pages=[], vectors=[], sensitive=[], rand=False, slow=500):
	if(len(pages) == 0):
		return pages
	retList = []
	if(rand):
		testPage = pages[random.randrange(len(pages))]
		successfulVectors=[]
		for v in vectors:
			#get inputs here
			try:
				r = requests.get(testPage.url, timeout=(float(slow)/1000.0))
				#check if attack was successful here
			except requests.exceptions.ConnectTimeout:
				if( "Potential Denial of Service" not in successfulVectors):
					successfulVectors.append("Potential Denial of service")
		retList = [testPage]
		retList.append(successfulVectors)
	return retList