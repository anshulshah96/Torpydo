import os,certifi,requests
import os
import sys
import bencoder

def main(args=None):
	if args is None:
		args = sys.argv[1:]

	file_dir = args[0]
	if os.path.exists(file_dir):
	    fh = open(file_dir,'r')
	    print fh.read()
	    
if __name__ == "__main__":
	main()



# d = bencoder.decode(f)
# del d[b"info"][b"pieces"]
# from pprint import pprint
# pprint(d)


# def test():
# 	os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
# test()
# r = requests.get('https://www.google.com')