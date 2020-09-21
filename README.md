inject
===

### Massive SQL injection scanner  
**Features**  
1. multiple domain scanning with SQL injection dork by Bing, Google, or Yahoo
2. targetted scanning by providing specific domain (with crawling)
3. reverse domain scanning

> both SQLi scanning and domain info checking are done in multiprocessing  
> so the script is super fast at scanning many urls

> quick tutorial & screenshots are shown at the bottom  
> project contribution tips at the bottom  

---

**Installation**  
1. git clone https://github.com/Shree3245/sqlInject.git


> Dependencies  
> - [bs4](https://pypi.python.org/pypi/bs4)  
> - [termcolor](https://pypi.python.org/pypi/termcolor)  
> - [google](https://pypi.python.org/pypi/google)
> - [nyawc](https://pypi.python.org/pypi/nyawc/)

**Pre-installed Systems**  
- [BlackArch Linux](https://blackarch.org/scanner.html) ![BlackArch](https://raw.githubusercontent.com/BlackArch/blackarch-artwork/master/logo/logo-38-49.png)

---
### Quick Tutorial  
**1. Multiple domain scanning with SQLi dork**  
- it simply search multiple websites from given dork and scan the results one by one
```python
python(3) inject.py -D <SQLI DORK> -e <SEARCH ENGINE>  
python(3) inject.py -D "inurl:index.php?id=" -e google  
```

**2. Targetted scanning**  
- can provide only domain name or specifc url with query params
- if only domain name is provided, it will crawl and get urls with query
- then scan the urls one by one
```python
python inject.py -T <URL>  
python inject.py -T www.example.com  
python inject.py -T www.example.com/index.php?id=1  
```

**3. Reverse domain and scanning**  
- do reverse domain and look for websites that hosted on same server as target url
```python
python inject.py -T <URL> -R
```

**4. Dumping scanned result**
- you can dump the scanned results as json by giving this argument
```python
python inject.py -D <SQLI DORK> -E <SEARCH ENGINE> -O result.json
```

**View help**  
```python
python inject.py --help

usage: inject.py [-h] [-D] [-E] [-P] [-T] [-R]

optional arguments:
  -h, --help  show this help message and exit
  -D         SQL injection dork
  -E         search engine [google bing or baidu]
  -P         number of websites to look for in search engine
  -T         scan target website
  -R          reverse domain
```

---
### screenshots
![1](https://raw.githubusercontent.com/Shree3245/inject/master/screenshots/1.png)
![2](https://raw.githubusercontent.com/Shree3245/inject/master/screenshots/2.png)
![3](https://raw.githubusercontent.com/Shree3245/inject/master/screenshots/3.png)
![4](https://raw.githubusercontent.com/Shree3245/inject/master/screenshots/4.png)

---

### Development
**TODO**  
1. POST form SQLi vulnerability testing
