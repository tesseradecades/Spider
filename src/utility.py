__author__="Nathan Evans"

from bs4 import BeautifulSoup

"""
A module of utility methods that are common across modules
"""

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
	swapDict = { ">" : "%3E", "<" : "%3C"}
	retString = ''
	for c in uString:
		if( swapDict.has_key(c) ):
			retString+=swapDict[c]
		else:
			retString+=c
	return retString