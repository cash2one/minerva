#!/usr/loca/bin/python

from pymongo.connection import Connection
from pymongo.database import Database
from pymongo.collection import Collection
import FreebaseApi
import AlchemyApiCategory
import SearchetOntology
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
#miss entities
MISS_ENTITIES = "/home/penser/tmp/miss.txt"
# number of queries
LIMIT = 780
# threshold to cut off unusual types
THRESHOLD = 1

class EntityExtractionNew:
    alchemyapi = "http://www.alchemyapi.com/api/entity/types.html#"
    dbpedia_owl = "http://dbpedia.org/ontology/"
    zemanta = "http://developer.zemanta.com/docs/entity_type/"
    searchet = "http://searchet.baidu.com/ontology#"
    freebase_owl = "http://schemas.freebaseapps.com/type?id="

    ''' docs '''
    def __init__(self):
        self.freebaseApi = FreebaseApi.FreebaseApi()
        self.alchemyApi = AlchemyApiCategory.AlchemyApiCategory() 
        self.dbpediaApi = DbPediaApi.DbPediaApi()
        self.ontology = SearchetOntology.SearchetOntology("/home/penser/Downloads/searchet_v2.n3", format="n3")
        # statistical container
        self.counter = {} 
        
        stat_paper = open(LOG_FILE, 'w')
        stat_paper.close()
        
        miss = open(MISS_ENTITIES, 'w')
        miss.close()

    def print_out(self):
        ''' docs '''
        stat_paper = open(STAT_PAPER, 'w')
        sort_counter = {}
        for key, value in sorted(self.counter.iteritems(), key=lambda (k,v): (len(v),k)):
            sort_counter[key]=value
            if len(value) >= THRESHOLD:
                stat_paper.write('%s: %i\n' % (key, len(value)))

        self.counter
        stat_paper.close()
    
    def print_log(self, keywords, dist):
        stat_paper = open(LOG_FILE, 'aw')
        stat_paper.write("\n"+keywords+"\n"+str(dist)+"\n")
        stat_paper.close()
        
    def print_miss(self, keywords, value):
        miss = open(MISS_ENTITIES, 'aw')
        miss.write(keywords+"\n"+','.join(value)+"\n\n")
        miss.close()

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
        freebase_map = {}      
        queries = {}
        nerd_result = []
        result_freebase = []
        try:
            result_freebase_in = self.freebaseApi.GetTypeId(keywords)
            result_freebase = self.freebaseApi.get_type_connect(result_freebase_in)
            for i, k in enumerate(result_freebase):
                freebase_map[k] = result_freebase_in[i]
                #print k, result_freebase_in[i]
        except Exception, e:
            print 'freebase error!!!'
        result_alchemy = self.alchemyApi.GetType(keywords)
        result_dbpedia = self.dbpediaApi.Search(keywords)
        if result_freebase:
            for f in result_freebase:
                queries[f] = self.freebase_owl 
        if result_alchemy:
             for f in result_alchemy:
                queries[f] = self.alchemyapi 
        if result_dbpedia:
             for f in result_dbpedia:
                queries[f] = self.dbpedia_owl
        
        miss_queries = []
        for key in queries:
            meta = self.ontology.getAllClass(queries[key], key)
            if meta:
                nerd_result.append(meta)
                #for m in meta:
                    #self.make_stats(m, keywords)
            elif queries[key]==self.freebase_owl:
                miss_queries.append(freebase_map[key])
                
        top_list = []
        for s in nerd_result:
            if s:
                l = len(s)
                tag = s[l-1]
                top_list.append(tag)
        top_set = set(top_list)
        for s in top_set:
            self.make_stats(s, keywords)
                             
        if miss_queries:
            self.print_miss(keywords, miss_queries)
            
        return self.singleLog(nerd_result)
    
    def singleLog(self, list):
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
    hotRrends = EntityExtractionNew()
    #result= hotRrends.analyze_query("stock")
    #print result
    try:
        result = hotRrends.analyze(LIMIT)
    except Exception, e:
        pass
    hotRrends.print_out()
  
            
if __name__ == "__main__": 
    main()
