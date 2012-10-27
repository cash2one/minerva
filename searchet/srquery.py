#!/usr/bin/python
# -*- coding: utf-8 -*-

##
# This class is created to provide a 
# simple data structure for each
# query after the query analysis
#
# @author Yuan Jin
# @contact jinyuan@baidu.com
# @created Sept. 24, 2012
# @updated Sept. 25, 2012
#

import sys
reload(sys)
sys.setdefaultencoding('UTF-8')

class Query:
	def __init__(self, query=None):
		self.query = query
		# key = entity name value = entity type
		self.token_entities = {}
		self.entity_tokens = {}
		self.feature_words = []
		# figure out an algorithm to compute the confidence
		self.confidence = None
		# feature_word entity_name
		self.pattern = ''

	def __str__(self):
		return str(self.token_entities)