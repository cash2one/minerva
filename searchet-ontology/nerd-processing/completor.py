#!/usr/local/bin/python

import sys
reload(sys)
sys.setdefaultencoding('UTF-8')

import freebase
import re

def main():
    f = open('uncategorized', 'r')
    data = f.read().split('\n')
    for i, d in enumerate(data):
        if i > 20:
            break
        
        # query process
        broken_d = re.findall('[A-Z][^A-Z]*', d)
        res = freebase.search(type=[['/base/ontologies/ontology_class', '/freebase/equivalent_topic', '/base/tagit/concept', '/base/ontologies/ontology_instance', '/common/topic', '/freebase/equivalent_topic'], limit=3, query=' '.join(broken_d))
        print d
        print [r['name'] for r in res]
        print

if __name__ == '__main__':
    main()
    print 'Done!'
