#!/usr/bin/env python
#

__author__ = 'shudong.huang'
__version__ = '1.1'

import wap
import time
from BeautifulSoup import BeautifulSoup
import re
start = time.clock()

server = 'http://api.wolframalpha.com/v1/query.jsp'
appid = 'EJ5Y64-R8YTEGJHHK'
input = 'bill clinton'

scantimeout = '3.0'
podtimeout = '4.0'
formattimeout = '8.0'
async = 'True'

waeo = wap.WolframAlphaEngine(appid, server)

waeo.ScanTimeout = scantimeout
waeo.PodTimeout = podtimeout
waeo.FormatTimeout = formattimeout
waeo.Async = async

query = waeo.CreateQuery(input)

waeq = wap.WolframAlphaQuery(input, appid)
waeq.ScanTimeout = scantimeout
waeq.PodTimeout = podtimeout
waeq.FormatTimeout = formattimeout
waeq.Async = async
waeq.ToURL()

query = waeq.Query

result = waeo.PerformQuery(query)
print result
soup = BeautifulSoup(result) 
print '\n', "**********************************************", '\n'
res = soup.findAll('assumption')
#print res
for r in res:
    print r
    print '\n'

print '\n', "**********************************************", '\n'

res = soup.findAll('plaintext')
for r in res:
    meta = r.string
    print meta
    print '\n'

print '\n', "**********************************************", '\n'
res2 = soup.findAll('pod')
for r2 in res2:
    meta2 = r2.string
    print r2
    print '\n'
    





