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