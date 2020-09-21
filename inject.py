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

ua = UserAgent().random

parser = argparse.ArgumentParser(
    description='Argument parser for dork-scanner')
parser.add_argument(
    '-S', '--search', help='String to be searched for', default='1')
parser.add_argument(
    '-E', '--engine', help='Search engine to be used', default='google')
parser.add_argument(
    '-P', '--page', help='Number of pages to search in', default='1')
parser.add_argument('-Pr', '--process',
                    help='Number of parallel processes', default='1')
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
        return ch2


def dorkScan():
    try:
        string = results.search
        engine = results.engine
        page   = results.page
        proc    = int( results.process  )
    except:
        print(" * * Error * * Arguments missing")
        exit(0)
    start_time = time.time()
    result = []
    pages = []
    websites=[]

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
        x=printf(set(result))
        websites.append(x)

    print ("\n")
    print ("#"*50)
    print( " Number of urls : {}" . format( str( len( result ) ) ))
    print( " Finished in : {} s" . format( str( int( time.time() - start_time ) )))
    print ("#"*50)
    return websites

if __name__ == '__main__':
    websites = dorkScan()
    print(len(websites))
    print(websites)
    

