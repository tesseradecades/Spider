__author__ = "Nathan Evans"

"""
A method to "fuzzy search" all html objects in a given list for the first one
to nearly match any of the words in a given list of strings

findMe - a list of strings to be used for fuzzy searched for

inputs - a list of html objects to be searched through

returns - the first html object to nearly match any word in findMe. If none of
the objects in inputs nearly match, return None
"""
def findInput(findMe=[], inputs=[]):
	for i in inputs:
		if((i.get("name").lower() in findMe) | (i.get("class") in findMe) | (i.get("type") in findMe)):
			#print(i.get("name"))
			return i
	return None