

import AlchemyAPI
from BeautifulSoup import BeautifulSoup
import sys
from HTMLParser import HTMLParser

api_Key = "c6fac7d54308715f4c02b13ee6323225e7c2d80b"
class AlchemyApiCategory:
    def __init__(self):
        pass
    def GetType(self, keywords):
        if not keywords:
            return []
        if len(keywords)<5:
            return []
        self.keywords = keywords
        self.apiKey = api_Key
        # Create a parameters object, and set some API call options
        self.params = AlchemyAPI.AlchemyAPI_NamedEntityParams()
        self.params.setDisambiguate(0)
        self.params.setQuotations(0)
        
        self.alchemyObj = AlchemyAPI.AlchemyAPI()
        self.alchemyObj.setAPIKey(self.apiKey)
        result = ""
        try:
            result = self.alchemyObj.TextGetRankedNamedEntities(self.keywords)
        except Exception, e:
            return []
        #print result
        soup = BeautifulSoup(result) 
        allType = []
        type = soup.find('type')
        if type:
            allType.append(type.string)
        
        subTypes = soup.find('disambiguated')
        if not subTypes:
            return allType
        #subTypes.__str__()

        for k in subTypes:
            soup2 = BeautifulSoup(k.__str__())
            str = ''.join(k.__str__())
            #print str
            if(str.__contains__('subtype')):
                allType.append(k.string)
        return allType

if __name__ == "__main__": 
    alchemyApi = AlchemyApiCategory()
    type = alchemyApi.GetType("bill clinton")
    print type

'''
    keyword = "china"
    alchemyObj = AlchemyAPI.AlchemyAPI()
    alchemyObj.setAPIKey(api_Key)
    result = alchemyObj.TextGetCategory(keyword)
    print '\n TextGetCategory  \n'
    print(result)
    result = alchemyObj.TextGetRankedNamedEntities(keyword)
    print '\n TextGetRankedNamedEntities  \n'
    print result
    result = alchemyObj.TextGetRelations(keyword);  
    print '\n TextGetRelations  \n'
    print(result)
    result = alchemyObj.TextGetRankedKeywords(keyword);
    print '\n TextGetRankedKeywords  \n'
    print(result)
    print(result)
    
    '''


