#!/usr/loca/bin/python

from pymongo.connection import Connection
from pymongo.database import Database
from pymongo.collection import Collection
import FreebaseApi
import AlchemyApiCategory

# constants and globals
MONGO_CON = '107.22.242.25:27017'
mongo_con = Connection(MONGO_CON)
MONGO_DB = 'queries'
mongo_db = Database(mongo_con, MONGO_DB)
MONGO_COL = 'hott_rends'
mongo_col = Collection(mongo_db, MONGO_COL)

# for specific data
LOG_FILE = '/home/jinyuan/Downloads/hottrends-script/specifics.txt'
# for simple data
STAT_PAPER = '/home/jinyuan/Downloads/hottrends-script/stats.txt'
# number of queries
LIMIT = 435
# threshold to cut off unusual types
THRESHOLD = 20


class HotTrendsAnalysis:
    ''' docs '''
    def __init__(self):
        self.freebaseApi = FreebaseApi.FreebaseApi()
        self.alchemyApi = AlchemyApiCategory.AlchemyApiCategory() 
        # statistical container
        self.counter = {} 

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

    def make_stats(self, key, value):
        ''' docs '''
        if key in self.counter:
            self.counter[key].append(value)
        else:
            self.counter[key] = [value]
        
    def analyze_query(self, keywords):
        ''' docs '''
        result = {}
        result_freebase = self.freebaseApi.GetType(keywords)
        result_alchemy = self.alchemyApi.GetType(keywords)

        # make a note of the keywords        
        result['query'] = keywords if keywords else 'None'

        # the name of the type
        if any(result_freebase[0]):
            result['freebase name'] = ', '.join(result_freebase[0])
            for cat in result_freebase[0]:
                self.make_stats(cat, keywords)
        else:
            result['freebase name'] = 'None'
        
        # the key of the type
        filter_freebase = ['user', 'common', 'base']
        if any(result_freebase[1]):
            result_freebase[1] = list(set(result_freebase[1]).difference(set(filter_freebase)))
            result['freebase base'] = ', '.join(result_freebase[1])
            for cat in result_freebase[1]:
                self.make_stats(cat, keywords)
        else:
            result['freebase base'] = 'None'

        # tags from alchmeyapi
        if any(result_alchemy):
            result['alchemy'] =  ', '.join(result_alchemy)
            for cat in result_alchemy:
                self.make_stats(cat, keywords)
        else:
            result['alchemy'] = 'None'
       
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
            print
        
        self.print_out()        
        return results
            
def main():
    ''' docs '''
    output = open(LOG_FILE, "w")
    hotRrends = HotTrendsAnalysis()
    result = hotRrends.analyze(LIMIT)
  
    for i, key in enumerate(result):
        output.write("\n ")
        tag = result[key]
        if tag:
            for key in tag:
                output.write("\n  ")
                output.write(str(tag[key]))
    output.close()
            
if __name__ == "__main__": 
    main()
