#!/usr/local/bin/

import freebase
QUERY = {'id':None, 'name':None, 'guid':''}

import rdflib
g = rdflib.Graph()

import re
import redis
rclient = redis.StrictRedis('127.0.0.1')

import sys
reload(sys)
sys.setdefaultencoding('UTF-8')

INPUT = raw_input('enter the input file: ')
OUTPUT = raw_input('enter the outputfile: ')


def freebase_free_search(keyword):
    tokens = re.findall('[A-Z][^A-Z]*', keyword)
    return freebase.search(query=' '.join(tokens), limit=5)

def freebase_limited_search(keyword):
    tokens = re.findall('[A-Z][^A-Z]*', keyword)
    return freebase.search(type=['/base/ontologies/ontology_class', '/freebase/equivalent_topic', '/base/tagit/concept', '/base/ontologies/ontology_instance', '/common/topic', '/freebase/equivalent_topic'], limit=3, query=' '.join(tokens))

def main():
    ''' docs '''
    # read in n3 file
    g.parse(INPUT, format='n3')
    fb_namespace = rdflib.namespace.Namespace('http://rdf.freebase.com/ns/')
    g.bind('freebase', 'http://rdf.freebase.com/ns/')
    
    # uncategorized terms
    f = open('uncategorized', 'w')

    for c in g.subject_objects(predicate=rdflib.term.URIRef(u'http://www.w3.org/2002/07/owl#equivalentClass')):
        if 'http://dbpedia.org/ontology/' in c[1]:
            freebase_type_added = False
            for cc in g.objects(subject=c[0], predicate=rdflib.term.URIRef(u'http://www.w3.org/2002/07/owl#equivalentClass')):
                if 'http://rdf.freebase.com/ns/' in cc:
                    freebase_type_added = True
                    break
                    
            if not freebase_type_added:
                #get the dbpedia type name
                dbpedia_type = c[1].replace('http://dbpedia.org/ontology/', '')
                searchet_type = c[0].replace('http://searchet.baidu.com/ontology#', '')
                freebase_guid = rclient.get(dbpedia_type)

                if freebase_guid:
                    # find the freebase type name
                    QUERY['guid'] = freebase_guid
                    fb_feedback = freebase.mqlread(QUERY)
                    
                    # corresponding to id
                    freebase_type = ''
                    # corresponding to name
                    freebase_type_name = ''
                    if 'id' in fb_feedback:
                        freebase_type = '.'.join(fb_feedback['id'].split('/')[1:])
                        freebase_type_name = fb_feedback['name']
                    
                    # add freebase type to the ontology
                    if freebase_type:
                        if dbpedia_type != freebase_type_name or searchet_type != freebase_type_name:
                            print '%s // %s' % (dbpedia_type, freebase_type)
                            choice = raw_input('confirmed y/n?: ').lower()
                            if choice == 'y' or choice == 'yes':
                                g.add((c[0], rdflib.term.URIRef(u'http://www.w3.org/2002/07/owl#equivalentClass'), fb_namespace[freebase_type]))
                                g.commit()
                            else:
                                freebase_found = freebase_limited_search(dbpedia_type)
                                candidate_type_names = [c['name'] for c in freebase_found]
                                if candidate_type_names:
                                    choice = raw_input('[%s] enter nunber or \'no\': ' % ', '.join(['%s(%i)' % (t, i) for i, t in enumerate(candidate_type_names)])).lower()
                                    # show all the types
                                    if choice != 'n' and choice != 'no':
                                        if 'type' in freebase_found[int(choice)]:
                                            for t in freebase_found[int(choice)]['type']:
                                                print ': %s' % t['id']
                                    else:
                                        f.write('%s\n' % dbpedia_type)
                                    print
                                else:
                                    f.write('%s\n' % dbpedia_type)
                        else:
                            g.add((c[0], rdflib.term.URIRef(u'http://www.w3.org/2002/07/owl#equivalentClass'), fb_namespace[freebase_type]))
                            g.commit()
                else: # cannot find a linked freebase type
                    freebase_found = freebase_limited_search(dbpedia_type)
                    candidate_type_names = [c['name'] for c in freebase_found]
                    if candidate_type_names:
                        print dbpedia_type
                        choice = raw_input('[%s] enter nunber or \'no\': ' % ', '.join(['%s(%i)' % (t, i) for i, t in enumerate(candidate_type_names)])).lower()
                        # show all the types
                        if choice != 'n' and choice != 'no':
                            if 'type' in freebase_found[int(choice)]:
                                for t in freebase_found[int(choice)]['type']:
                                    print ': %s' % t['id']
                        else:
                            f.write('%s\n' % dbpedia_type)
                        print
                    else:
                        f.write('%s\n' % dbpedia_type)
    f.close()
    g.serialize(destination=OUTPUT, format='n3', encoding='utf-8')

if __name__ == '__main__':
    main()
    print 'Done!'
