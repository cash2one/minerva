#!/usr/bin/python
# -*- coding: utf-8 -*-

##
#
#
# @author Yuan Jin
# @contact jinyuan@baidu.com
# @created Sept. 24, 2012
# @updated Sept. 25, 2012
#

import sys
reload(sys)
sys.setdefaultencoding('UTF-8')

from nltk import load_parser
from rdflib import Namespace, URIRef

# PATTERN = raw_input('enter pattern config file: ')
PATTERN = 'searchet.fcfg'
searchet = Namespace("http://searchet.baidu.com/ontology#")

class PatternLoader:
	def __init__(self, pattern):
		self.pattern = pattern
		self.c = load_parser(PATTERN)

	def pattern_converter(self):
		'''docs'''

	def load(self):
		'''docs'''
		# print str(self.c.nbest_parse(self.pattern))
		return '_'.join(self.c.nbest_parse(self.pattern)[0].node['SEM'])
