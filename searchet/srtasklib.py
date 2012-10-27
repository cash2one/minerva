#!/usr/bin/python
# -*- coding: utf-8 -*-

##
#
#
# @author Yuan Jin
# @contact jinyuan@baidu.com
# @created Sept. 27, 2012
# @updated Sept. 27, 2012
#

import sys
reload(sys)
sys.setdefaultencoding('UTF-8')

def show_profile_person(keywords):
	'''docs'''
	import srsingleentity
	return srsingleentity.search(keywords)

def show_profile_work(work):
	'''docs'''
	print work

def show_airline_itinerary_with_cities(keywords):
	'''docs'''
	sys.path.append('flightApi_v2')
	import FlightApi
	return FlightApi.get_flight_weather_info_by_thread(keywords)


def show_itinerary_with_cities(keywords):
	'''docs'''
	return show_airline_itinerary_with_cities(keywords)

