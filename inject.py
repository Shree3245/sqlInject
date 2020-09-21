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
    '-E', '--engine', help='Search engine to be used', default='google')
parser.add_argument(
    '-P', '--page', help='Number of pages to search in', default='1')
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

def singlescan(url):
    """instance to scan single targeted domain"""

    if parse.urlparse(url).query != '':
        result = scanner.scan([url])
        if result != []:
            # scanner.scan print if vulnerable
            # therefore exit
            return result

        else:
            print("")  # move carriage return to newline
            std.stdout("no SQL injection vulnerability found")
            option = std.stdin("do you want to crawl and continue scanning? [Y/N]", ["Y", "N"], upper=True)

            if option == 'N':
                return False

    # crawl and scan the links
    # if crawl cannot find links, do some reverse domain
    std.stdout("going to crawl {}".format(url))
    urls = crawler.crawl(url)

    if not urls:
        std.stdout("found no suitable urls to test SQLi")
        #std.stdout("you might want to do reverse domain")
        return False

    std.stdout("found {} urls from crawling".format(len(urls)))
    vulnerables = scanner.scan(urls)

    if vulnerables == []:
        std.stdout("no SQL injection vulnerability found")
        return False

    return vulnerables


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
    website = []
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
        website.append(set(result))

    print ("\n")
    print ("#"*50)
    print( " Number of urls : {}" . format( str( len( result ) ) ))
    print( " Finished in : {} s" . format( str( int( time.time() - start_time ) )))
    print ("#"*50)
    return website

    

if __name__ == '__main__':
    if results.dork != None and results.engine != None:
        websites = dscan()
        vulnerables = scanner.scan(websites)
        if not vulnerables:
            if results.store:
                print('saved as searches.txt')
                with open('searches.txt','w+') as f:
                    f.write(websites)
            print('asdf')
            exit(0)
            
        print("scanning server information")
        vulnerableUrls = [result[0] for result in vulnerables]
        table_data = serverinfo.check(vulnerableUrls)
        
        for result, info in zip(vulnerables,table_data):
            info.insert(1,result[1])
        
        print(table_data)
        print(len(table_data))
        
    elif results.target != None and results.reverse:
        std.stdout("finding domains with same server as {}".format(results.target))
        domains = reverseip.reverseip(results.target)

        if domains == []:
            std.stdout("no domain found with reversing ip")
            exit(0)

        # if there are domains
        std.stdout("found {} websites".format(len(domains)))

        # ask whether user wants to save domains
        std.stdout("scanning multiple websites with crawling will take long")
        option = std.stdin("do you want save domains? [Y/N]", ["Y", "N"], upper=True)

        if option == 'Y':
            std.stdout("saved as domains.txt")
            std.dump(domains, "domains.txt")

        # ask whether user wants to crawl one by one or exit
        option = std.stdin("do you want start crawling? [Y/N]", ["Y", "N"], upper=True)

        if option == 'N':
            exit(0)

        vulnerables = []
        for domain in domains:
            vulnerables_temp = singlescan(domain)
            if vulnerables_temp:
                vulnerables += vulnerables_temp

        std.stdout("finished scanning all reverse domains")
        if vulnerables == []:
            std.stdout("no vulnerables webistes from reverse domains")
            exit(0)

        std.stdout("scanning server information")

        vulnerableurls = [result[0] for result in vulnerables]
        table_data = serverinfo.check(vulnerableurls)
        # add db name to info
        for result, info in zip(vulnerables, table_data):
            info.insert(1, result[1])  # database name

        std.fullprint(table_data)
        
    elif results.target:
        vulnerables = singlescan(results.target)

        if not vulnerables:
            exit(0)

        # show domain information of target urls
        print("getting server info of domains can take a few mins")
        table_data = serverinfo.check([results.target])

        print(table_data)
        print ("")  # give space between two table
        print(vulnerables)
        exit(0)
        
    else:
        parser.print_help()
    
    if args.output != None:
        std.dumpjson(table_data, args.output)
        std.stdout("Dumped result into %s" % args.output)
                    
    
        