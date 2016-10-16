__author__ = "Nathan Evans"

from bs4 import BeautifulSoup

"""
A method which compiles a dictionary of commonly occurring words in the
application being tested

r - a request object representing the page to be used in compilation

cWords - a dictionary representing words that have already been found
and their number of occurrences so far

"""
def compileCommonWords(r=None, cWords={}):
	tagsToSearch = ["p", "label", "input", "h1", "h2", "h3", "h4", "h5", "h6", "li", "div"]
	soup = BeautifulSoup(r.text, "html.parser")
	ignored = ["a", "the", "this", "that"]
	words = []

	totalWords = 0
	for t in tagsToSearch:
		for o in soup.find_all(t):
			tWords = o.getText().split()
			words.extend(tWords)	
			totalWords += len(tWords)
	for w in words:
		if(not (w in ignored)):
			if( w in cWords.keys()):
				cWords[w] += 1
			else:
				cWords[w] = 1

	"""avgOcc = totalWords / len(cWords)
	#print(avgOcc)
	tempWords = {}
	for k in cWords.keys():
		if(cWords[k] >= avgOcc):
			tempWords[k] = cWords[k]
	return tempWords"""
	return cWords