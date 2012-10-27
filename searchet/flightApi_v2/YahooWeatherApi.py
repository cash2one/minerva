#!/usr/bin/python
# -*- coding: utf-8 -*-

##
# this script serves to get weather from yahoo
#
# @author Shudong Huang
# @contact kingsd.huang@gmail.com
# @created sep. 25, 2012
#

import urllib
from BeautifulSoup import BeautifulSoup
from pprint import pprint
import pywapi
import threading
import simplejson

location_id_url = 'http://xoap.weather.com/search/search?where='

def get_location_id(location):
    if not location:
        return ''
    query = location_id_url  + location
    res = urllib.urlopen(query).read()
    if not res:
        return ''
    soup = BeautifulSoup(res)
    id = soup.find('loc')
    if not id:
        return ''
    id = id['id']
    return id

def get_weather_info(location):
    id = get_location_id(location)
    result = pywapi.get_weather_from_yahoo(id, 'metric')
    if not result:
        return {}
    output = dict(result)
    return output

def get_weather_info_simple(location):
    try:
        rsk = get_weather_info(location)
        res = convert_to_simple(rsk)
    except Exception, e:
        return {}
    return res

def convert_to_simple(weather_dict):
    if not weather_dict:
        return {}
    
    output = {}
    output['condition']=weather_dict['condition']['text']
    output['temperature']=weather_dict['condition']['temp']
    output['pressure']=weather_dict['atmosphere']['pressure']
    output['humidity'] = weather_dict['atmosphere']['humidity']
    output['visibility']=weather_dict['atmosphere']['visibility']
    output['Wind'] = weather_dict['wind']['speed']
    output['forecast'] = weather_dict['forecasts'][0]['text']
    link  = weather_dict['link']
    links = link.split('*')
    if len(links)>=2:
        output['more_link'] = links[1]
    
    html_des = weather_dict['html_description']
    tag = str(html_des).split('\n')[1]
    start = tag.find('=')+2
    end = tag.find('/>')-1
    tag = tag[start:end]
    output['html_description'] = tag
    return output

class WeatherThread(threading.Thread):
    def __init__(self, location):
        threading.Thread.__init__(self)
        self.location = location
        self.result = {}

    def run(self):
        self.result = get_weather_info_simple(self.location)

if __name__ == "__main__": 
    
    #res = get_weather_info_simple("boston")
    weather = WeatherThread('boston')
    weather.start()
    weather.join(10000)
    pprint(weather.result)
   
    