import requests
import re
import sys
import time
import os
import argparse
from bs4 import BeautifulSoup
from functools import partial
from multiprocessing import Pool, TimeoutError, cpu_count
from fake_useragent import UserAgent
from pprint import pprint
from urllib import parse
from src import std
from src import scanner
from scan import scan_sql_injection as scan
from src import reverseip
from src import serverinfo
from src import web
from src.crawler import Crawler

crawler = Crawler()
ua = UserAgent().random

parser = argparse.ArgumentParser(
    description='Argument parser for dork-scanner')
parser.add_argument(
    '-D', '--dork', help='String to be searched for')
parser.add_argument(
    '-E', '--engine', help='Search engine to be used', default='bing')
parser.add_argument(
    '-P', '--page', help='Number of pages to search in', default='10')
parser.add_argument('-Pr', '--process',
                    help='Number of parallel processes', default='1')
parser.add_argument("-T", dest="target", help="scan target website", type=str, metavar="www.example.com")
parser.add_argument('-R', dest="reverse", help="reverse domain", action='store_true')
parser.add_argument('-O', dest="output", help="output result into json", type=str, metavar="result.json")
parser.add_argument('-S', dest="store", action='store_true', help="output search even if there are no results")

results = parser.parse_args(sys.argv[1:])

engineDict = {
    'google': {
        'link': 'http://www.google.com/search',
        'tags': {
            'options': 'cite',
            'attr': {
                'class': 'iUh30'
            }
        }
    },

    'bing': {
        'link': 'https://www.bing.com/search',
        'tags': {
            'options': 'li',
            'attr': 'b_algo'
        }
    },

    'baidu': {
        'payload': {
            'q': 'string',
            'first': 'start'
        },
        'link': 'http://www.baidu.com/s',
        'tags': {
            'options': 'h3',
            'attr': 't'
        }
    },
}


def search(engine, string, start):
    engineSearch = engineDict[engine]
    urls = []
    payload = { 'q' : string, 'start' : start }
    headers = {'User-agent': ua}
    req = requests.get(engineSearch['link'],
                       payload, headers=headers)
    soup = BeautifulSoup(req.text, 'html.parser')
    tags = soup.findAll(engineSearch['tags']
                        ['options'], engineSearch['tags']['attr'])

    for tag in tags:
        try:
            if engine == 'google':
                urls.append(tag.text)
            elif engine == 'bing':
                urls.append(tag.find('a').attrs['href'])
            else:
                urlu = tag.find('a').attrs['href']
                link = requests.get(urlu)
                urls.append(link.url)
        except:
            continue
    return urls

def printf(lista): 
    for i in lista:
        link = str(i)
        ch = link.replace("%3F", "?")
        ch2 = ch.replace("%3D","=")
        print( " " + ch2 )


def dscan():
    try:
        print(results)
        string = results.dork
        engine = results.engine
        page   = results.page
        proc    = int( results.process  )
    except:
        print(" * * Error * * Arguments missing")
        exit(0)
    start_time = time.time()
    result = []
    pages = []
    for p in range(int(page)):
        pages.append(p*10)
        p = Pool(proc)
        print("#"*50)
        print ("Searching for: {} in {} page(s) of {} with {} process(es)".format(str(string),str(page),str(engine),str(proc)))
        print ("#"*50)
        print ("\n")
        request = partial(search,engine,string)
        listAll = p.map(request,pages)
    
    for p in listAll:
        result += [u for u in p]
        printf(set(result))

    print ("\n")
    print ("#"*50)
    print( " Number of urls : {}" . format( str( len( result ) ) ))
    print( " Finished in : {} s" . format( str( int( time.time() - start_time ) )))
    print ("#"*50)
    return listAll

    

if __name__ == '__main__':
    if results.dork != None and results.engine != None:
        websites = dscan()
        print('asdf')
        print([website.split(">")[0] for website in websites[0]])
        if results.engine == 'google':
            vulnerables = [scan(website.split(" > ")[0]) for website in websites[0]]
            
        elif results.engine == 'bing':
            vulnerables = [scan(website.split(" > ")[0]) for website in websites[0]]
        print(vulnerables)
        
        
    elif results.target:
        vulnerables = scan(results.target)

        if not vulnerables:
            exit(0)

        # show domain information of target urls
        print("getting server info of domains can take a few mins")
        
        
    else:
        parser.print_help()
    exit(0)
    
    if args.output != None:
        std.dumpjson(table_data, args.output)
        std.stdout("Dumped result into %s" % args.output)
                    
    
        