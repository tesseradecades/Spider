__author__ = 'Nathan Evans'

import argparse

COMMAND = None
URL = None
CUSTOM_AUTH = None
COMMON_WORDS = None
VECTORS = None
SENSITIVE = None
RANDOM = None
SLOW = None

def main():
	argParser = argparse.ArgumentParser()
	argParser.add_argument("command",help="[discover | test]\n Discover - Output a comprehensive, human-readable list of all discovered inputs to the system. Techniques include both crawling and guessing.\n Test - Discover all inputs, then attempt a list of exploit vectors on those inputs. Report potential vulnerabilities.")
	argParser.add_argument("url",help="Url to run the fuzzer on.")
	argParser.add_argument("--custom-auth", help="--custom-auth=string Signal that the fuzzer should use hard-coded authentication for a specific application (e.g. dvwa).")
	argParser.add_argument("--common-words", help="--common-words=file Newline-delimited file of common words to be used in page guessing and input guessing.")
	argParser.add_argument("--vectors", help="--vectors=file Newline-delimited file of common exploits to vulnerabilities.")
	argParser.add_argument("--sensitive",help="--sensitive=file Newline-delimited file data that should never be leaked. It's assumed that this data is in the application's database (e.g. test data), but is not reported in any response.")
	argParser.add_argument("--random",help="--random=[true|false] When off, try each input to each page systematically. When on, choose a random page, then a random input field and test all vectors. Default: false.")
	argParser.add_argument("--slow",help="--slow=500 Number of milliseconds considered when a response is considered \"slow\". Default is 500 milliseconds")
	args = argParser.parse_args()
	
	global COMMAND
	COMMAND = args.command.lower()
	print(COMMAND)
	
	global URL
	URL = args.url
	if( URL[:16] == "http://localhost"):
		URL = ("http://127.0.0.1" + URL[17:])
	print(URL)

	global CUSTOM_AUTH
	CUSTOM_AUTH = args.custom_auth
	print(CUSTOM_AUTH)
	
	global VECTORS
	VECTORS = args.vectors
	print(VECTORS)
	
	global SENSITIVE
	SENSITIVE = args.sensitive
	print(SENSITIVE)
	
	global RANDOM
	RANDOM = args.random
	print(RANDOM)
	
	global SLOW
	SLOW = args.slow
	print(SLOW)
if __name__ == "__main__":
	main()
