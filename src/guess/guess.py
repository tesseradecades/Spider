__author__ = "Nathan Evans"

import leet
from bs4 import BeautifulSoup

"""
A method which compiles a dictionary of commonly occurring words in the
application being tested

r - a request object representing the page to be used in compilation

cWords - a dictionary representing words that have already been found
and their number of occurrences so far

return - a new dictionary containing words that appear more often than
the average word found so far
"""
def compileCommonWords(r=None, cWords={}):
	tagsToSearch = ["p", "label", "input", "h1", "h2", "h3", "h4", "h5", "h6", "li", "div"]
	soup = BeautifulSoup(r.text, "html.parser")
	words = []

	totalWords = 0
	for t in tagsToSearch:
		for o in soup.find_all(t):
			tWords = o.getText().split()
			words.extend(tWords)	
			totalWords += len(tWords)
	for w in words:
		if( w in cWords.keys()):
			cWords[w] += 1
		else:
			cWords[w] = 1

	avgOcc = totalWords / len(cWords)
	#print(avgOcc)
	tempWords = {}
	for k in cWords.keys():
		if(cWords[k] >= avgOcc):
			tempWords[k] = cWords[k]
	return tempWords
	
"""
A method to "fuzzy search" all html objects in a given list for the first one
to nearly match any of the words in a given list of strings

findMe - a list of strings to be used for fuzzy searched for

inputs - a list of html objects to be searched through

returns - the first html object to nearly match any word in findMe. If none of
the objects in inputs nearly match, return None
"""
def findInput(findMe=[], inputs=[]):
	fuzzList = fuzzWords(findMe)
	for i in inputs:
		if((i.get("name").lower() in fuzzList) | (i.get("class") in fuzzList) | (i.get("type") in fuzzList)):
			return i
	return None

"""
A method that takes in a list of strings and returns a list containing common 
mutations of those strings

words - a list of strings

returns - a list of common mutations of the strings in words
"""
def fuzzWords(words = []):
	ret = []
	for w in words:
		ret.append(w)
		ret.append(w.upper())
		l = w.lower()
		ret.append(l)
		ret.append(leet.leetEncode(w, "b"))
		ret.append(leet.leetEncode(l, "b"))
		ret.append(leet.leetEncode(w, "a"))
		ret.append(leet.leetEncode(w, "u"))
	return ret

#for testing purposes
def main():
	print(fuzzWords(["Password","Username"]))
	import requests
	print(compileCommonWords(requests.get("http://127.0.0.1/dvwa"),{"Web" : 99, "Quine" : 0}))
	
if __name__ == "__main__":
	main()