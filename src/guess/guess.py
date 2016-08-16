__author__ = "Nathan Evans"

import commonWords, leet

fileExt = ['.jsp', ".html", ".asp"]

def compileUrlGuesses(url="", cWords={}):
	guesses = []
	totalWords = 0
	commonlyUsed = []
	
	words = cWords.keys()
	for k in words:
		totalWords+=cWords[k]
	#the total number of words used divided by the number of unique words
	avgOcc = totalWords / len(cWords)
	
	for k in words:
		if(cWords[k] >= avgOcc):
			commonlyUsed.append(k)
	
	"""for k in commonlyUsed:
		guesses.append(url+"/"+k)"""	
	return guesses

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
	print(commonWords.compileCommonWords(requests.get("http://127.0.0.1/dvwa"),{"Web" : 99, "Quine" : 0}))
	
if __name__ == "__main__":
	main()