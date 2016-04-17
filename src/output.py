__author__ = "Nathan Evans"

import datetime

def output(found=[]):
	o = open("../output/"+datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d%H%M%S")+".html",'w')
	
	if( found[0] == 'discover'):
		o.write(compileDiscoverOutput(found[1]))
	elif( found[0] == 'test'):
		o.write(compileTestOutput(found[1]))
	o.close()

def compileDiscoverOutput(discovered):
	out = ''
	for r in discovered:
		pg = "<li>"+r.url+"</li>"
		out = out + pg
	return out

def compileTestOutput(tested):
	return ''