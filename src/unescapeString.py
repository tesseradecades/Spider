__author__="Nathan Evans"

swapDict = { ">" : "%3E", "<" : "%3C"}

def unescape(uString):
	retString = ''
	for c in uString:
		if( swapDict.has_key(c) ):
			retString+=swapDict[c]
		else:
			retString+=c
	return retString