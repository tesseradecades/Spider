__author__="Nathan Evans"

from bs4 import BeautifulSoup

"""
A module of utility methods that are common across modules
"""
escapeDict = { "%3E": ">", "%3C": "<" }
unescapeDict = { ">" : "%3E", "<" : "%3C"}
def escape(eString=''):
	global escapeDict
	retString = eString
	for k in escapeDict:
		if(k in retString):
			holdMe = retString.split(k)
			retString = holdMe.join(escapeDict[k])
	return retString
"""
returns a list of objects representing all tags of the specified type on a page

txt = a string containing the page's html
tag = the kind of tag to return

"""
def getAllOnPage(txt='', tag=''):
	soup = BeautifulSoup(txt, "html.parser")
	return soup.find_all(tag)

"""
used to unescape characters in a string

uString = a string containing escaped characters
returns = a string containing all of the characters of uString, but unescaped
"""
def unescape(uString=''):
	global unescapeDict
	retString = ''
	for c in uString:
		if( unescapeDict.has_key(c) ):
			retString+=unescapeDict[c]
		else:
			retString+=c
	return retString