__author__ = "Nathan Evans"

import datetime

class outputTree():
	def __init__(self, r):
		self.response = r
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
	o = open("../output/"+found[0]+datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d%H%M%S")+".html",'w')
	
	if( found[0] == 'discover'):
		o.write(compileDiscoverOutput(found[1]))
	elif( found[0] == 'test'):
		o.write(compileTestOutput(found[1]))
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