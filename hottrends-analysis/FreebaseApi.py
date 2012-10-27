#!/usr/bin/python
# -*- coding: utf-8 -*-

##
# this script serves to get the type of keywords
# @author Shudong Huang
# @contact v_huangshudong@baidu.com
# @created Oct. 6, 2012
#

import json
import urllib
import freebase

class FreebaseApi:
    def __init__(self):
        pass
    
    def GetType(self, keyword):
        if not keyword:
            return [[],[]]
        #search for the id
        data = freebase.search(keyword, limit=1)
        if not data:
            return [[],[]]
        item_id = [d['id'] for d in data if 'id' in d][0]
        query = {"id":item_id, "type":[{}]}
        response = freebase.mqlread(query)
        types = response['type']
        
        names = []
        base_names = []
        for k in types:
            names.append(k['name'])
            type_x = ''.join(k['id']).split('/');
            if len(type_x)>1:
                base_names.append(type_x[1])
        names_set = set(names)
        base_names_set = set(base_names)
        names = []
        base_names = []
        for y in names_set:
            names.append(y)
        for y in base_names_set:
            base_names.append(y)
            
        all_list = []
        all_list.append(names)
        all_list.append(base_names)
        return all_list


if __name__ == "__main__":  
    freebaseApi = FreebaseApi()
    type = freebaseApi.GetType("bill clinton")
    for k in type:
        print k
    print type
    
    '''  if len(types)>=2:
            return types
        elif len(types)>=1:
            return types
        else:
            return 'none'  '''
'''
API_KEY = 'AIzaSyBt2fyoAJ20gy9CCTJGqTFQZiK7CLMkaLg'
service_url = 'https://www.googleapis.com/freebase/v1/topic'
topic_id = '/m/0d6lp'
params = {
  'key': API_KEY,
  'filter': 'suggest'
}
url = service_url + topic_id + '?' + urllib.urlencode(params)
result = urllib.urlopen(url).read()
print result
pass
topic = json.loads(result)

for property in topic['property']:
  print property + ':'
  for value in topic['property'][property]['values']:
    print ' - ' + value['text']
    
    '''