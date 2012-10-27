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


class HotTrendsAnalysisAl:
    ''' docs '''
    def __init__(self):
        self.freebaseApi = FreebaseApi.FreebaseApi()
        self.alchemyApi = AlchemyApiCategory.AlchemyApiCategory() 
        self.nerd = nerd.nerd("/home/penser/Downloads/nerd-last.n3", format="n3")
        self.dp_pedia = DbPediaApi.DbPediaApi()
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
        result['query'] = keywords if keywords else 'None'
        
        result_alchemy = self.dp_pedia.Search(keywords)#self.alchemyApi.GetType(keywords)
        nerd_result = []
        for k in result_alchemy:
            self.make_stats(k, keywords)
            list = []
            list.append(k)
            res_types = self.nerd.get_subjects('equivalentClass', k)
            if res_types:
                #print res_types[0]
                type_str = str(res_types[0])
                key_strs = type_str.split('#')
                if len(key_strs)>1:
                    key_str = key_strs[1] 
                    list.append( key_strs[1])
                    res_subclasses = self.nerd.get_subClasses( key_strs[1], "subClassOf")
                    if res_subclasses:
                        s_type_str = str(res_subclasses[0])
                        s_key_strs = s_type_str.split('#')
                        if len(s_key_strs)>1:
                            list.append(s_key_strs[1])
                        else:
                            list.append("none")
                    else:
                        list.append("none")
                else:
                    list.append("none")
                    list.append("none") 
            else:
                list.append("none")
                list.append("none")         
                     #print res_subclasses[0]
            nerd_result.append(list)
        result['nerd'] = nerd_result
        return result
    
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
    hotRrends = HotTrendsAnalysisAl()
    result = hotRrends.analyze(LIMIT)
    hotRrends.print_out()
  
            
if __name__ == "__main__": 
    main()
