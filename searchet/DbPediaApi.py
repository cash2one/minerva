import urllib
from urllib import urlopen
from BeautifulSoup import BeautifulSoup
import sys
from HTMLParser import HTMLParser

rul_base = "http://lookup.dbpedia.org/api/search.asmx/KeywordSearch?QueryClass=&QueryString="
books = ['Maid for the Billionaire', 'Fools Rush In', 'In the Garden of Temptation', 'Gone Girl: A Novel', 'Coloring Book Kit by Royal Magic ']

class DbPediaApi:
    
    def __init__(self):
        pass
    def Search(self, keywords):
        u = urlopen(rul_base+keywords)
        result = u.read()
        f = open("/home/penser/tmp/dbpediadata.txt", "w")
        f.write(str(result))
        #print result
        soup = BeautifulSoup(result) 
        labels = soup.findAll('label')
        classes = soup.findAll('class')
        all_label = []
        for c in classes:
            k = c.find("label")
            if k:
                all_label.append(k.string.capitalize())
                
        return self.Deduplication(all_label)


    def Deduplication(self, list):
        lset = set(list)
        list = []
        for y in lset:
            list.append(y)
        return list
            
if __name__ == "__main__": 
    
    api = DbPediaApi()
    result = api.Search("stock price")
    for k in result:
        print k
    
    
    
    
    
    
    
    
    