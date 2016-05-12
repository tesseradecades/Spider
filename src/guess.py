__author__ = "Nathan Evans"


def findInput(findMe=[], inputs=[]):
	for i in inputs:
		if((i.get("name").lower() in findMe) | (i.get("class") in findMe) | (i.get("type") in findMe)):
			#print(i.get("name"))
			return i
	return None