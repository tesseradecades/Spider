__author__ = "Nathan Evans"

import datetime, utility

class outputTree():
	def __init__(self, r):
		self.response = r
		self.redirects = []
		for x in self.response.history:
			if(x.url != self.response.url):
				self.redirects.append(x.url)
		self.vulnerabilities = []
		self.childPages = []
	def addChildPage(self, cP):
		stored = False
		for c in self.childPages:
			if(c.response.url in cP.response.url):
				c.addChildPage(cP)
				stored = True
				break
		if((not stored) and (self.response.url in cP.response.url)):
			self.childPages.append(cP)
	
	def printTree(self):
		print(self.response.url)
		for c in self.childPages:
			c.printTree()
			
def output(found=[]):
	print("\nFOUND\n"+str(found))
	o = open("../output/"+found[0]+datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d%H%M%S")+".html",'w')
	o.write(compileOutput(found[1]))
	o.close()

def compileDiscoverOutput(discovered):
	out = ''
	for r in discovered[:len(discovered)-1]:
		pg = "<li>"+r.url+"</li>"
		out = out + pg
	out += "<li>"+"COOKIES:\t"+str(discovered[len(discovered)-1])+"</li>"
	return out

def compileTestOutput(tested):
	return ''

def compileOutput(found=[]):
	out = "COOKIES:\t"+str(found[1])+"\n"
	out+="<ul>"+compileOutputHelper(found[0])
	out+="</ul>" 
	return out
def compileOutputHelper(outputLeaf):
	retString = "URL: "+outputLeaf.response.url+"<br/>"
	retString+= "Redirects:<br/><ol>"
	for r in outputLeaf.redirects:
		retString+="<li>"+r+"</li>"
	retString+="</ol>"
	retString+= "Vulnerabilies:<br/><ol>"
	for v in outputLeaf.vulnerabilities:
		retString+= "<li>"+utility.escape(v)+"</li>"
	retString+="</ol>"
	retString+="Child Pages:<br/><ol>"
	for c in outputLeaf.childPages:
		retString+="<li>"+compileOutputHelper(c)+"</li>"
	retString+="</ol>"
	return retString