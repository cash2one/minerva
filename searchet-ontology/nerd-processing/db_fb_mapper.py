#!/usr/local/bin/python

import werkzeug
import sys
reload(sys)
sys.setdefaultencoding('UTF-8')
import redis
REDIS_SERVER = '127.0.0.1'
rclient = redis.StrictRedis(REDIS_SERVER)


def freebase_process(dotted):
    splits = dotted.split('.')
    return '#%s' % splits[1]

def dbpedia_process(quoted):
    splitted_quoted = quoted.split(':')
    return werkzeug.url_unquote(splitted_quoted[1])

def main():
    f = open('sameAsFreebase.ttl', 'r')
    data = f.read().split('\n')
    f.close()

    total = len(data)
    f = open('db_fb_map', 'w')
    # data processing
    for i, d in enumerate(data):
        print '.. %i of %i' % (i+1, total)
        d = d.split(' ')
        if any(d):
            if 'dbpedia' in d[0]:
                dbpedia = dbpedia_process(d[0])
                if 'fb' in d[2]:
                    freebase = freebase_process(d[2])
                    f.write('%s %s' % (dbpedia, freebase) + '\n')
                    rclient.set(dbpedia, freebase)
    f.close()

if __name__ == '__main__':
    print 'processing ...'
    main()
    print 'done!'
