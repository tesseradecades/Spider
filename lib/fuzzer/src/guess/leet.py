__author__ = "Nathan Evans"

basicLeet = { "A" : "4", "E" : "3", "G" : "6", "I" : "1", "O" : "0", "S" : "5", "T" : "7"}

advancedLeet = { "A" : "4", "B" : "|3", "C" : "(", "D" : "|)", "E" : "3", 
"F" : "|=", "G" : "9", "H" : "|-|", "I" : "!", "J" : "_|", "K" : "|<", 
"L" : "|_", "M" : "/\\", "N" : "|\\|", "O" : "0", "P" : "|D", "Q" : "q", 
"R" : "|2", "S" : "5", "T" : "7", "U" : "(_)", "V" : "\\/", "W" : "\\/\\/", 
"X" : "><", "Y" : "`/", "Z" : "2"}

ultimateLeet = { "A" : "4", "B" : "8", "C" : "(", "D" : "|)", "E" : "3", 
"F" : "|#", "G" : "6", "H" : "|-|", "I" : "!", "J" : "_)", "K" : "|(", 
"L" : "1", "M" : "|\\/|", "N" : "|\\|", "O" : "0", "P" : "|>", "Q" : "?", 
"R" : "|2", "S" : "5", "T" : "+", "U" : "|_|", "V" : "\\/", "W" : "\\|/", 
"X" : "%", "Y" : "`/", "Z" : "7_"}

"""
A method that takes in a string and outputs the l33t speak equivalent

s - the string to be encoded

m - the mode to use for encoding. "b" = basic l33t, "a" = advanced l33t
and "u" = ultimate l33t

returns a string
"""
def leetEncode( s = "", m = ""):
	ret = ""
	mDict = {}
	
	if(m == "u"):
		mDict = ultimateLeet
	elif( m == "a" ):
		mDict = advancedLeet
	elif( m == "b" ):
		mDict = basicLeet
	else:
		return s
	
	for c in s:
		d = c.upper()
		if(d in mDict.keys()):
			ret+= mDict[d]
		else:
			ret+= c
	return ret

def main():
	print(leetEncode("Hello World!", "b"))
	print(leetEncode("Hello World!", "a"))
	print(leetEncode("Hello World!", "u"))

if __name__ == "__main__":
	main()