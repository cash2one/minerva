#!/usr/bin/python
# -*- coding: utf-8 -*-

##
# this script serves to get flight informations
#
# @author Shudong Huang
# @contact kingsd.huang@gmail.com
# @created sep. 25, 2012
#

import urllib
import simplejson
from BeautifulSoup import BeautifulSoup
from pprint import pprint
import YahooWeatherApi
import threading

#https://api.flightstats.com/flex/connections/rest/v1/json/connecting/from/JFK/to/LHR/departing/2012/10/12?appId=1a532dfa&appKey=e21f32456d3dda4b81dd63de67899a1c
gateway = 'http://airportcode.riobard.com/search?'
appId = '1a532dfa'
appKey = 'e21f32456d3dda4b81dd63de67899a1c'
flight_base = 'https://api.flightstats.com/flex/connections/rest/v1/xml/connecting/'
api = '?appId=1a532dfa&appKey=e21f32456d3dda4b81dd63de67899a1c'

def search_airport_info(location):
    args = {}
    args['q'] = location
    args['fmt'] = 'JSON'
    args_enc = urllib.urlencode(args)
    query = gateway  + args_enc
    res = urllib.urlopen(query).read()
    output = simplejson.loads(res)
    return output;

def get_airport_code(airport_info):
    
    if not airport_info:
        return ''
    code = airport_info[0]['code']
    if not code:
        return ''
    return code

def search_flight(departure_loc, arrival_loc, year, month, day):
    departure = search_airport_info(departure_loc)
    arrival = search_airport_info(arrival_loc)
    departure_code = get_airport_code(departure)
    arrival_code = get_airport_code(arrival)
    print departure_code, arrival_code
    if not departure_code or not arrival_code:
        return "error can not find the city code!"
    
    date = '/departing/'+year+'/'+month+'/'+day
    schedule = 'from' + '/' + departure_code + '/' + 'to' + '/' + arrival_code
    query = flight_base + schedule + date + api
    print query
    res = urllib.urlopen(query).read()
    file = open('/home/penser/tmp/flight.xml', 'w')
    file.write(str(res))
    return get_flight_info(res);

def get_flight_info(source_xml):
    all_info = {}
    flight = {}
    airport = {}
    weather = {}
    airlines = {}
    airport_all = {}
    
    soup = BeautifulSoup(source_xml) 
    
    #decode airlines 
    airline_tab = soup.findAll('airline')
    for a in airline_tab:
        line = decode_airline(a)
        airlines.update(line) 
        
    #decode airport
    airport_tab = soup.findAll('airport')
    for a in airport_tab:
        port = decode_airport(a)
        airport_all.update(port) 
    
    #flight
    flight_tab = soup.find('flight')
    if not flight_tab:
        return all_info
    
    departureDate = flight_tab.find('departuredateto')
    departureTime = flight_tab.find('departuretime')
    arrivalTime = flight_tab.find('arrivaltime')
    distanceMiles = flight_tab.find('distancemiles')
    flightType = flight_tab.find('flighttype')
    if departureDate:
        flight["date"] = departureDate.string
    if departureDate:
        flight["departureTime"] = departureTime.string
    if departureDate:
        flight["arrivalTime"] = arrivalTime.string
    if departureDate:
        flight["distanceMiles"] = distanceMiles.string
    if departureDate:
        flight["flightType"] = flightType.string
        
    flightLegs = flight_tab.find('flightlegs')
    departureAirportFsCodeAll = flightLegs.findAll('departureairportfscode')
    arrivalAirportFsCodeAll = flightLegs.findAll('arrivalairportfscode')
    departureAirportFsCode = departureAirportFsCodeAll[0]
    arrivalAirportFsCode = arrivalAirportFsCodeAll[len(arrivalAirportFsCodeAll)-1]
    departureTerminal = flightLegs.find('departureterminal')
    arrivalTerminal = flightLegs.find('arrivalterminal')
    flightNumber = flightLegs.find('flightnumber')
    carrierFsCode = flightLegs.find('carrierfscode')
    
    if departureAirportFsCode:
        flight["departureAirportFsCode"] = departureAirportFsCode.string
    if arrivalAirportFsCode:
        flight["arrivalAirportFsCode"] = arrivalAirportFsCode.string
    if departureTerminal:
        flight["departureTerminal"] = departureTerminal.string
    if arrivalTerminal:
        flight["arrivalTerminal"] = arrivalTerminal.string
    if flightNumber:
        flight["airline_number"] = flightNumber.string
    if carrierFsCode:
        flight["carrierFsCode"] = carrierFsCode.string
        
    airline_name = airlines[flight["carrierFsCode"]]
    source_airport = airport_all[flight["departureAirportFsCode"]]
    destination_airport = airport_all[flight["arrivalAirportFsCode"]]
    
    if airline_name:
        flight["airline_name"] = airline_name["name"]
        flight["airline_phone_number"] = airline_name["phoneNumber"]
    
    airport_tmp = {}
    if source_airport:
        airport_tmp["source"] = source_airport
    if destination_airport:
        airport_tmp["destination"] = destination_airport
    if airport_tmp:
        flight["flight_info"] = airport_tmp
        
    return flight
   
def get_flight_weather_info(departure_loc, arrival_loc, year, month, day):
    weather = {}
    flight_info = search_flight(departure_loc, arrival_loc, year, month, day)
    src_weather_info = YahooWeatherApi.get_weather_info_simple(departure_loc)
    dst_weather_info = YahooWeatherApi.get_weather_info_simple(arrival_loc)
    weather['source'] = src_weather_info
    weather['destination'] = dst_weather_info
    flight_info['weather'] = weather
    flight_info['from'] = departure_loc
    flight_info['to'] = arrival_loc
    
    return flight_info
    

def decode_airline(airline_tab):
    res = {}
    info = {}
    fs = airline_tab.find('fs')
    name = airline_tab.find('name')
    phoneNumber = airline_tab.find('phonenumber')
    if not fs:
        return {}
    else:
        fs = fs.string
    if name:
        info['name'] = name.string
    if phoneNumber:
        info['phoneNumber'] = phoneNumber.string
    res[fs] = info
    return res

def decode_airport(airline_tab):
    res = {}
    info = {}
    fs = airline_tab.find('fs')
    name = airline_tab.find('name')
    street1 = airline_tab.find('street1')
    street2 = airline_tab.find('street2')
    city = airline_tab.find('city')
    cityCode = airline_tab.find('citycode')
    countryCode = airline_tab.find('countrycode')
    countryName = airline_tab.find('countryname')
    localtime = airline_tab.find('localtime')
    latitude = airline_tab.find('latitude')
    longitude = airline_tab.find('longitude')
    
    if not fs:
        return {}
    else:
        fs = fs.string
    if name:
        info['name'] = name.string
    if street1:
        info['street1'] = street1.string
    if street2:
        info['street2'] = street2.string
    if city:
        info['city'] = city.string
    if cityCode:
        info['cityCode'] = cityCode.string
    if countryCode:
        info['countryCode'] = countryCode.string
    if countryName:
        info['countryName'] = countryName.string
    if localtime:
        info['localtime'] = localtime.string
    if latitude:
        info['latitude'] = latitude.string
    if longitude:
        info['longitude'] = longitude.string
    if street1 and city and countryName:
        try:
            info['airport_address'] = info['street1'] + ' ' + info['city'] + ' ' + info['countryName']
            info['airport_short'] = fs
        except Exception, e:
            pass
    res[fs] = info
    return res

class FlightThread(threading.Thread):
    def __init__(self, departure_loc, arrival_loc, year, month, day):
        threading.Thread.__init__(self)
        self.departure_loc = departure_loc
        self.arrival_loc = arrival_loc
        self.year = year
        self.month = month
        self.day = day
        self.result = {}

    def run(self):
        self.result = search_flight(self.departure_loc, self.arrival_loc, self.year, self.month, self.day)
    
def get_flight_weather_info_by_thread(keywords):
    departure_loc='boston'
    arrival_loc='montreal'
    year='2012'
    month='10'
    day='1'
    
    if not len(keywords):
        return None
    elif len(keywords) == 2:
        departure_loc = keywords[0]
        arrival_loc = keywords[1]

    flightThread = FlightThread(departure_loc, arrival_loc, year, month, day)
    flightThread.start();
    scr_weather = YahooWeatherApi.WeatherThread(departure_loc)
    scr_weather.start()
    dst_weather = YahooWeatherApi.WeatherThread(arrival_loc)
    dst_weather.start()
    flightThread.join(10000)
    scr_weather.join(10000)
    dst_weather.join(10000)
    
    weather = {}
    flight_info = flightThread.result
    src_weather_info = scr_weather.result
    dst_weather_info = dst_weather.result
    weather['source'] = src_weather_info
    weather['destination'] = dst_weather_info
    flight_info['weather'] = weather
    flight_info['from'] = departure_loc
    flight_info['to'] = arrival_loc
    
    return flight_info

if __name__ == "__main__": 
    
    #res = search_airport_code('guilin')
    res = get_flight_weather_info_by_thread("beijing", "boston", '2012', '10', '1')
    pprint(res)
                
#    flight = res['appendix']
#    for key in flight:
#        for f in flight[key]:
#            for kk in f:
#                print kk, f[kk]
        #print key,  flight[key]
        
    #print res

