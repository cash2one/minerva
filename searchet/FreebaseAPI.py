#!/usr/bin/python
# -*- coding: utf-8 -*-

##
# this script serves to get the ontologiucal types 
# of some keyword from Freebase
#
# @author Shudong Huang
# @contact v_huangshudong@baidu.com
#
# @reviewer Yuan Jin
# @contact jinyuan@baidu.com
#
# @created Sept. 6, 2012
# @updated Sept. 24, 2012
#

import sys
reload(sys)
sys.setdefaultencoding('UTF-8')

import freebase
from srentity import Entity


class FreebaseAPI:
    '''docs'''
    def __init__(self, keyword=None):
        self.keyword = keyword

    def id_converter(self, fid=None):
        '''docs'''
        tokens = fid.split('/')
        return ''.join([t.lower().capitalize() for t in tokens[1:]])

    def key_processor(self, text=None):
        '''Michelle_Obama --> michelle obama'''
        return text.replace('_', ' ').lower()

    def entity_builder(self, entity=None):
        '''docs'''
        entity_type = []
        types = entity['type']
        for t in types:
            # only certain types are allowed
            if '/freebase/type_profile' in t['type'] and '/type/type' in t['type']:
                entity_type.append(self.id_converter(t['id']))
        entity_type = list(set(entity_type))

        entity_text = []
        keys = entity['key']
        for k in keys:
            entity_text.append(self.key_processor(k))
        entity_text = list(set(entity_text))

        entity_name = entity['name']

        return Entity(service='freebase', entity_type=entity_type, entity_text=entity_text, entity_name=entity_name)
    
    def get_types(self):
        '''docs'''
        if not self.keyword:
            return None

        # search for the id
        data = freebase.search(self.keyword, limit=1)
        if data:
            item_id = [d['id'] for d in data if 'id' in d][0]

            query = {"id":item_id, "type":[{}], 'key':[], 'name':None}
            response = freebase.mqlread(query)
            
            return self.entity_builder(response)
        else:
            return None