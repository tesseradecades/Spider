__author__ = "Nathan Evans"

import datetime

def output(found=[]):
	o = open("../output/"+datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d%H%M%S")+".html",'w')
	o.write(str(found))
	o.close()