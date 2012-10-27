#!/usr/bin/python
# -*- coding: utf-8 -*-

##
# this script serves to get the ontologiucal types 
# of some keyword from AlchemyAPI
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

## imports and CONSTANTS
import sys
reload(sys)
sys.setdefaultencoding('UTF-8')

import AlchemyAPI
from BeautifulSoup import BeautifulSoup
from HTMLParser import HTMLParser
from srentity import Entity

API_KEY = "e4d1ccf978e557352d908b1debfe96bef6302234"


class AlchemyApiCategory:
    def __init__(self, keyword=None):
        self.keyword = keyword
    
    def entity_builder(self, entity=None):
        '''find out the type, text, name, subtypes'''
        entity_type = entity.find('type').text
        entity_text = entity.find('text').text
        
        entity_name = ''
        name = entity.find('name')
        if name:
            entity_name = name.text

        entity_subtypes = []
        subtypes = entity.findAll('subtype')
        if subtypes:
            for subtype in subtypes:
                entity_subtypes.append(subtype)

        return Entity(service='alchemyapi', entity_type=entity_type, entity_text=entity_text, entity_name=entity_name, entity_subtypes=entity_subtypes)

    def get_types(self, keyword=None):
        '''docs'''
        if not self.keyword:
            return None

        ## not accurate if length of keyword is less than 5? 
        #if len(keyword)<5:
        #    return None
        
        # Create a parameters object, and set some API call options
        self.params = AlchemyAPI.AlchemyAPI_NamedEntityParams()
        self.params.setDisambiguate(0)
        self.params.setQuotations(0)
        
        self.alchemyObj = AlchemyAPI.AlchemyAPI()
        self.alchemyObj.setAPIKey(API_KEY)

        result = self.alchemyObj.TextGetRankedNamedEntities(self.keyword)
        if result:
            soup = BeautifulSoup(result) 
            types = []
            # might be several entities
            entities = soup.findAll('entity')
            for e in entities:
                # return an entity instance
                types.append(self.entity_builder(e))
            return types
        else:
            return None