__author__ = 'Nathan Evans'

import argparse, discover, output, threading

CUSTOM_AUTH = []
COMMON_WORDS = []
VECTORS = []
SENSITIVE = []
RANDOM = False
SLOW = 500

def main():
	argParser = argparse.ArgumentParser()
	argParser.add_argument("command",help="[discover | test]\n Discover - Output a comprehensive, human-readable list of all discovered inputs to the system. Techniques include both crawling and guessing.\n Test - Discover all inputs, then attempt a list of exploit vectors on those inputs. Report potential vulnerabilities.")
	argParser.add_argument("url",help="Url to run the fuzzer on.")
	argParser.add_argument("--custom-auth", help="--custom-auth=string Signal that the fuzzer should use hard-coded authentication for a specific application (e.g. dvwa).")
	argParser.add_argument("--common-words", type=argparse.FileType(mode='r'), help="--common-words=file Newline-delimited file of common words to be used in page guessing and input guessing.")
	argParser.add_argument("--vectors", type=argparse.FileType(mode='r'), help="--vectors=file Newline-delimited file of common exploits to vulnerabilities.")
	argParser.add_argument("--sensitive", type=argparse.FileType(mode='r'), help="--sensitive=file Newline-delimited file data that should never be leaked. It's assumed that this data is in the application's database (e.g. test data), but is not reported in any response.")
	argParser.add_argument("--random", type=bool, help="--random=[true|false] When off, try each input to each page systematically. When on, choose a random page, then a random input field and test all vectors. Default: false.")
	argParser.add_argument("--slow", type=int, help="--slow=500 Number of milliseconds considered when a response is considered \"slow\". Default is 500 milliseconds")
	args = argParser.parse_args()

	url = args.url
	if( url[:16] == "http://localhost"):
		url = ("http://127.0.0.1" + url[17:])
	
	global CUSTOM_AUTH
	if(args.custom_auth):
		CUSTOM_AUTH.append(args.custom_auth)
		f = open('../res/customauths/'+args.custom_auth+'.txt', 'r')
		for word in f:
			CUSTOM_AUTH.append(word.rstrip())
		
	global COMMON_WORDS
	if(args.common_words):
		for word in args.common_words:
			COMMON_WORDS.append(word.rstrip())
		
	global VECTORS
	if(args.vectors):
		for word in args.vectors:
			VECTORS.append(word.rstrip())
		
	global SENSITIVE
	if(args.sensitive):
		for word in args.sensitive:
			SENSITIVE.append(word.rstrip())
		
	global RANDOM
	if(type(args.random) is str):
		if(args.random.lower() == 'true'):
			RANDOM = True
	
	global SLOW
	if(args.slow):
		SLOW = args.slow
	
	runCommand(args.command.lower(), url)
	
def runCommand(command, url):
	if(command=="discover"):
		global CUSTOM_AUTH
		global COMMON_WORDS
		
		found = ['discover']
		found.append(discover.crawl(url, auth=CUSTOM_AUTH, commonWords=COMMON_WORDS))
<<<<<<< HEAD
		#print found
=======
>>>>>>> ad8b648204617059648b9b83b7ff206c771dc583
		output.output(found)
	elif(command=="test"):
		print("test")
	else:
		print("Invalid command:\t"+command+"\nTry discover or test")


if __name__ == "__main__":
	main()
