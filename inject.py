import argparse
from urllib.parse import urlparse
from component.search import search
from multiprocessing import Pool, TimeoutError, cpu_count
from functools import partial
# TODO: init engine instance and crawler instance

parser = argparse.ArgumentParser()
parser.add_argument("-d", dest="dork", help="SQL injection dork",
                    type=str, metavar="inurl:example")
parser.add_argument("-e", dest="engine",
                    help="search engine [Bing, Google, and Yahoo]", type=str, metavar="bing, google, yahoo")
parser.add_argument("-p", dest="page", help="number of websites to look for in search engine",
                    type=int, default=1, metavar="100")
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
    string = args.dork
    engine = args.engine
    pages = args.page

    # find random SQLi by dork
    if args.dork != None and args.engine != None:
        print('Searching for websites with given dork')
        result = []
        page = []
        # Get websites based on search engine
        for i in range(int(pages)):
            page.append(i*10)
            i = Pool(1)
            print("#"*50)
            print("Searching for: {} in {} page(s) of {}".format(
                str(string), str(pages), str(engine)))
            print("#"*50)
            print("\n")

            request = search(engine, string, pages)

        for p in listAll:
            result += [u for u in p]
            printf(set(result))

        print("\n")
        print("#"*50)
        print(" Number of urls : {}" . format(str(len(result))))
        print("#"*50)

    else:
        print('invalide search engine')
