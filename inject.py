import argparse
from urllib.parse import urlparse
from component import search
from multiprocessing import Pool, TimeoutError, cpu_count
from functools import partial
# TODO: init engine instance and crawler instance

parser = argparse.ArgumentParser()
parser.add_argument("-d", dest="dork", help="SQL injection dork",
                    type=str, metavar="inurl:example")
parser.add_argument("-e", dest="engine",
                    help="search engine [Bing, Google, and Yahoo]", type=str, metavar="bing, google, yahoo")
parser.add_argument("-p", dest="page", help="number of websites to look for in search engine",
                    type=int, default=10, metavar="100")
parser.add_argument("-t", dest="target", help="scan target website",
                    type=str, metavar="www.example.com")
parser.add_argument('-r', dest="reverse",
                    help="reverse domain", action='store_true')
parser.add_argument('-o', dest="output",
                    help="output result into json", type=str, metavar="result.json")
parser.add_argument('-s', action='store_true',
                    help="output search even if there are no results")


def printf(lista):
    for i in lista:
        link = str(i)
        ch = link.replace("%3F", "?")
        ch2 = ch.replace("%3D", "=")
        print(" " + ch2)


if __name__ == '__main__':
    args = parser.parse_args()
    string = args.search
    engine = args.engine
    pages = args.page
    proc = int(args.process)

    # find random SQLi by dork
    if args.dork != None and args.engine != None:
        print('Searching for websites with given dork')
        start_time = time.time()
        result = []
        pages = []
        # Get websites based on search engine
        for i in range(int(pages)):
            pages.append(p*10)
            p = Pool(proc)
            print("#"*50)
            print("Searching for: {} in {} page(s) of {} with {} process(es)".format(
                str(string), str(page), str(engine), str(proc)))
            print("#"*50)
            print("\n")
            request = partial(search, engine, string)
            listAll = p.map(request, pages)

        for p in listAll:
            result += [u for u in p]
            printf(set(result))

        print("\n")
        print("#"*50)
        print(" Number of urls : {}" . format(str(len(result))))
        print(" Finished in : {} s" . format(
            str(int(time.time() - start_time))))
        print("#"*50)
