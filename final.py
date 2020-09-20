import argparse
from urllib.parse import urlparse

#TODO: import search and crawler instance

#Initialise and set parse flags
parser = argparse.ArgumentParser()
parser.add_argument("-d", dest="dork", help="SQL injection dork", type=str, metavar="inurl:example")
parser.add_argument("-e", dest="engine", help="search engine [Bing, Google, and Yahoo]", type=str, metavar="bing, google, yahoo")
parser.add_argument("-p", dest="page", help="number of websites to look for in search engine", type=int, default=10, metavar="100")
parser.add_argument("-t", dest="target", help="scan target website", type=str, metavar="www.example.com")
parser.add_argument('-r', dest="reverse", help="reverse domain", action='store_true')
parser.add_argument('-o', dest="output", help="output result into json", type=str, metavar="result.json")
parser.add_argument('-s', action='store_true', help="output search even if there are no results")


if __name__=='__main__':
	args= parser.parse_args()

	#find random SQLi by dork
	if args.dork != None and args.engine == None:
		print('Searching for website with given dork')

	#get website based on search engine
	if args.engine in ['bing', 'google', 'yahoo']:
		websites = eval(args.engine)