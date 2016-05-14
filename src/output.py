__author__ = "Nathan Evans"

import datetime

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
	out += "<li>"+"COOKIES:\t"+discovered[len(discovered)-1]+"</li>"
	return out

def compileTestOutput(tested):
	return ''