#!/usr/bin/python
# -*- coding: utf-8 -*-

##
#
#
# @author Yuan Jin
# @contact jinyuan@baidu.com
# @created Sept. 25, 2012
# @updated Sept. 25, 2012
#

import sys
reload(sys)
sys.setdefaultencoding('UTF-8')

from srtagger import QueryTagger
from srloader import PatternLoader
import srtasklib

class QueryDispatcher:
	'''docs'''
	def __init__(self, query):
		self.query = query

	def dispatch(self):
		tagger_client = QueryTagger(self.query)
		# this returns a srquery instance
		tagged_query = tagger_client.tag()
		loader_client = PatternLoader(tagged_query.pattern)
		task_name = loader_client.load()

		# call the task
		return eval('srtasklib.%s' % task_name)(tagged_query.token_entities.keys())