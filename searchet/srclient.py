#!/usr/bin/python
# -*- coding: utf-8 -*-

##
# this script serves to act as the gate
# to search different sources
#
# @author Yuan Jin
# @contact jinyuan@baidu.com
# @created Aug. 1, 2012
# @updated Sept. 26, 2012
#

# imports and CONSTANTS
import sys
reload(sys)
sys.setdefaultencoding('UTF-8')

from srdispatcher import QueryDispatcher

if __name__ == '__main__':
	user_input = raw_input('please input your query: ')
	dispatcher = QueryDispatcher(user_input)
	print dispatcher.dispatch()

