#!/usr/bin/python
# -*- coding: utf-8 -*-

##
# 
#
# @author Yuan Jin
# @contact jinyuan@baidu.com
#
# @created Sept. 24, 2012
# @updated Sept. 24, 2012
#

## imports and CONSTANTS
import sys
reload(sys)
sys.setdefaultencoding('UTF-8')

class Entity:
    '''docs'''
    def __init__(self, service='baidu', entity_type=None, entity_text=None, entity_name=None, entity_subtypes=None):
    	# text is the original query text
        self.entity_text = entity_text
        # name is the name from the service
        self.entity_name = entity_name

        self.entity_type = entity_type
        self.entity_subtypes = entity_subtypes
        
        # service means 
        # baidu
        # freebase
        # alchemyapi
        # ....
        self.service = service

    def __str__(self):
        output = {}
        output['name'] = str(self.entity_name)
        output['text'] = str(self.entity_text)
        output['type'] = str(self.entity_type)
        output['service'] = str(self.service)
        return str(output)