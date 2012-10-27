#!/usr/loca/bin/python

from pymongo.connection import Connection
from pymongo.database import Database
from pymongo.collection import Collection
import FreebaseApi
import AlchemyApiCategory
import nerd
import DbPediaApi

# constants and globals
MONGO_CON = '107.22.242.25:27017'
mongo_con = Connection(MONGO_CON)
MONGO_DB = 'queries'
mongo_db = Database(mongo_con, MONGO_DB)
MONGO_COL = 'hott_rends'
mongo_col = Collection(mongo_db, MONGO_COL)

# for specific data
LOG_FILE = '/home/penser/tmp/specifics.txt'
# for simple data
STAT_PAPER = '/home/penser/tmp/stats.txt'
# number of queries
LIMIT = 420
# threshold to cut off unusual types
THRESHOLD = 2


class EntityExtraction:
    ''' docs '''
    def __init__(self):
        self.freebaseApi = FreebaseApi.FreebaseApi()
        self.alchemyApi = AlchemyApiCategory.AlchemyApiCategory() 
        self.dbpediaApi = DbPediaApi.DbPediaApi()
        self.nerd = nerd.nerd("/home/penser/Downloads/nerd-last.n3", format="n3")
        # statistical container
        self.counter = {} 
        
        stat_paper = open(LOG_FILE, 'w')
        head = """----------------------------------------------------------\n the first item is the type from alchemy
               \n the second item is the nerd type    /n the third item is the subClass of nerd \n"""
        stat_paper.write(head + "\n")
        stat_paper.close()

    def print_out(self):
        ''' docs '''
        stat_paper = open(STAT_PAPER, 'w')
        from collections import OrderedDict
        sorted_counter = OrderedDict(sorted(self.counter.items(), key=lambda x: x[1], reverse=True)) 

        # print out the stats
        for k, v in sorted_counter.iteritems():
            if len(v) > THRESHOLD:
                stat_paper.write('%s: %i\n' % (k, len(v)))
        stat_paper.close()
    
    def print_log(self, keywords, dist):
        stat_paper = open(LOG_FILE, 'aw')
        stat_paper.write("\n"+keywords+"\n"+str(dist)+"\n")
        stat_paper.close()

    def make_stats(self, key, value):
        ''' docs '''
        if key in self.counter:
            self.counter[key].append(value)
        else:
            self.counter[key] = [value]
        
    def analyze_query(self, keywords):
        ''' docs '''
        result = {}
         # make a note of the keywords        
        queries = []
        nerd_result = []
        result_freebase = self.freebaseApi.GetType(keywords)
        result_alchemy = self.alchemyApi.GetType(keywords)
        result_dbpedia = self.dbpediaApi.Search(keywords)
        if result_freebase:
            if result_freebase[0]:
                queries.extend(result_freebase[0])
        if result_alchemy:
            queries.extend(result_alchemy)
        if result_dbpedia:
            queries.extend(result_dbpedia)
        
        for q in queries:
            meta = self.nerd.getAllClass(q)
            if meta:
                nerd_result.append(meta)
                for m in meta:
                    self.make_stats(m, keywords)
        return self.SingleLog(nerd_result)
    
    def SingleLog(self, list):
        po = '_'
        tmp_list = []
        tmp_result = []
        for l in list:
            tmp_str = ''
            for i, t in enumerate(l):
                if i>0:
                    tmp_str = tmp_str + po
                tmp_str = tmp_str + t
            tmp_list.append(tmp_str)
            #print tmp_str
            
        for i,k in enumerate(tmp_list):
            is_find = False
            for j, le in enumerate(tmp_list):
                if k != le and le.find(k)>=0:
                    is_find = True
            if not is_find:
                tmp_result.append(k)
        mset = set(tmp_result)
        tmp_result = []
        for m in mset:
            tmp_result.append(m)
        return tmp_result
  
    def analyze(self, limit):
        ''' docs '''
        queries = mongo_col.find()
        results = {}

        for i in xrange(0, limit):
            query = queries[i]
            keywords = query['query']
            res = self.analyze_query(keywords)
            results[keywords] = res
            print '%i of %i ....: %s' % (i + 1, LIMIT, query['query'])
            print res
            print
            self.print_log(keywords, res)
        return results
            
def main():
    ''' docs '''
    output = open(LOG_FILE, "w")
    hotRrends = EntityExtraction()
    result = hotRrends.analyze(LIMIT)
    hotRrends.print_out()
  
            
if __name__ == "__main__": 
    main()
