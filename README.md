# Spider
Improvement on the Fuzzer Project from SWEN-331 (Engineering Secure Software)

usage: spider.py [-h] [--custom-auth CUSTOM_AUTH]
                 [--common-words COMMON_WORDS] [--vectors VECTORS]
                 [--sensitive SENSITIVE] [--random RANDOM] [--slow SLOW]
                 command url

positional arguments:
  command               [discover | test] Discover - Output a comprehensive,
                        human-readable list of all discovered inputs to the
                        system. Techniques include both crawling and guessing.
                        Test - Discover all inputs, then attempt a list of
                        exploit vectors on those inputs. Report potential
                        vulnerabilities.
  url                   Url to run the fuzzer on.

optional arguments:
  -h, --help            show this help message and exit
  --custom-auth CUSTOM_AUTH
                        --custom-auth=string Signal that the fuzzer should use
                        hard-coded authentication for a specific application
                        (e.g. dvwa).
  --common-words COMMON_WORDS
                        --common-words=file Newline-delimited file of common
                        words to be used in page guessing and input guessing.
  --vectors VECTORS     --vectors=file Newline-delimited file of common
                        exploits to vulnerabilities.
  --sensitive SENSITIVE
                        --sensitive=file Newline-delimited file data that
                        should never be leaked. It's assumed that this data is
                        in the application's database (e.g. test data), but is
                        not reported in any response.
  --random RANDOM       --random=[true|false] When off, try each input to each
                        page systematically. When on, choose a random page,
                        then a random input field and test all vectors.
                        Default: false.
  --slow SLOW           --slow=500 Number of milliseconds considered when a
                        response is considered "slow". Default is 500
                        milliseconds


# TODO
Discover
	Custom Authentication
	Page Discovery
		Link Discovery
		Page Guessing
	Input Discovery
		Parse URLs
		Form Parameters
		Cookies
PageTesting
	Lack of Sanitization
	Sensitive Data Leaked
	Delayed Response
	HTTP Response Codes
