#!/usr/local/bin/python

import freebase
QUERY = {'id':None, 'name':None, 'guid':''}

import rdflib
g = rdflib.Graph()

import re
import string
import sys
reload(sys)
sys.setdefaultencoding('UTF-8')

FREEBASE_SCHEMA = 'http://schemas.freebaseapps.com/type?id='
INPUT = raw_input('enter the input file: ')
OUTPUT = raw_input('enter the outputfile: ')


def freebase_free_search(keyword):
    tokens = re.findall('[A-Z][^A-Z]*', keyword)
    return freebase.search(query=' '.join(tokens), limit=7)

def freebase_limited_search(keyword):
    tokens = re.findall('[A-Z][^A-Z]*', keyword)
    return freebase.search(type=['/freebase/type_profile', '/type/type'], limit=10, query=' '.join(tokens))

def freebase_type_conventor(fen): # fen: freebase entity name
    ''' change /book/english_author to BookEnglish_author'''
    tokens = fen.split('/')
    return ''.join([t.lower().capitalize() for t in tokens[1:]])

def freebase_remover(file_to_make):
    result = g.subject_objects(predicate=rdflib.term.URIRef('http://www.w3.org/2002/07/owl#equivalentClass'))
    for r in result:
        if FREEBASE_SCHEMA in r[1]:
            g.remove((r[0], rdflib.term.URIRef(u'http://www.w3.org/2002/07/owl#equivalentClass'), r[1]))
            g.commit()
    g,serialize(destination=file_to_make, format='n3', encoding='utf-8')

def main():
    ''' docs '''
    # read in n3 file
    g.parse(INPUT, format='n3')
    fb_namespace = rdflib.namespace.Namespace(FREEBASE_SCHEMA)
    g.bind('freebase', FREEBASE_SCHEMA)
    
    # uncategorized terms
    f = open('uncategorized', 'w')
    probable_db_items = g.subject_objects(predicate=rdflib.term.URIRef(u'http://www.w3.org/2002/07/owl#equivalentClass'))
    previous_success = None

    for current, c in enumerate(probable_db_items):
        if 'http://dbpedia.org/ontology/' in c[1]:
            freebase_type_added = False
            for cc in g.objects(subject=c[0], predicate=rdflib.term.URIRef(u'http://www.w3.org/2002/07/owl#equivalentClass')):
                if FREEBASE_SCHEMA in cc:
                    freebase_type_added = True
                    break
                    
            if not freebase_type_added:
                #get the dbpedia type name
                dbpedia_type = c[1].replace('http://dbpedia.org/ontology/', '')
                searchet_type = c[0].replace('http://searchet.baidu.com/ontology#', '')

                freebase_found = freebase_limited_search(dbpedia_type)
                candidate_types = dict((ff['name'], ff['id']) for ff in freebase_found)

                # just in case dbpedia_type doesn't work
                if not any(freebase_found) or dbpedia_type != searchet_type:
                    freebase_found = freebase_limited_search(searchet_type)
                    candidate_types.update(dict((ff['name'], ff['id']) for ff in freebase_found))
                    
                    #freebase_found = freebase_free_search(searchet_type)
                    #candidate_types.update(dict((ff['name'], ff['id']) for ff in freebase_found))

                # if anything really exists
                if any(candidate_types):
                    print '%i.%s / %s' % (current + 1, dbpedia_type, searchet_type)
                    for n, item in enumerate(candidate_types.iteritems()):
                        print '[%i] %s: %s' % (n, str(item[0]), str(item[1]))
                    choices = raw_input('enter nunbers (separated by comma), or \'no\', \'delete\', \'save\', \'input\': ').lower()

                    # 1. numbers
                    # 2. no answer
                    # 3. delete previous
                    # 4. save now
                    if ',' in choices or choices.strip().replace(',', '').replace(' ', '') in string.digits:
                        choice_list = [cs.strip() for cs in choices.split(',')]
                        print 'your choices: ', str(choice_list)
                        for choice in choice_list:
                            freebase_type = freebase_type_conventor(candidate_types.values()[int(choice)])
                            g.add((c[0], rdflib.term.URIRef(u'http://www.w3.org/2002/07/owl#equivalentClass'), fb_namespace[freebase_type]))
                            g.commit()

                            previous_success = (c[0], rdflib.term.URIRef(u'http://www.w3.org/2002/07/owl#equivalentClass'), fb_namespace[freebase_type])
                            print '%s is added!' % fb_namespace[freebase_type]
                    elif choices == 's' or choices == 'sa' or choices == 'sav' or choices == 'save':
                        f.write('%s\n' % dbpedia_type)
                        break
                    elif choices == 'd' or choices == 'de' or choices == 'del' or choices == 'dele' or choices == 'delet' or choices == 'delete':
                        if previous_success:
                            g.remove(previous_success)
                            g.commit()
                            print '%s is succussfully removed!' % previous_success[2]
                            previous_success = None
                    elif choices == 'i' or choices == 'in' or choices == 'int' or choices == 'inpu' or choices == 'input':
                        user_entered_type = raw_input('now input the type id: ')
                        freebase_type = freebase_type_conventor(user_entered_type)
                        g.add((c[0], rdflib.term.URIRef(u'http://www.w3.org/2002/07/owl#equivalentClass'), fb_namespace[freebase_type]))
                        g.commit()

                        previous_success = (c[0], rdflib.term.URIRef(u'http://www.w3.org/2002/07/owl#equivalentClass'), fb_namespace[freebase_type])
                        print '%s is added!' % fb_namespace[freebase_type]
                    else:
                        f.write('%s\n' % dbpedia_type)
                else:
                    f.write('%s\n' % dbpedia_type)
                # separate different items
                print
    f.close()
    g.serialize(destination=OUTPUT, format='n3', encoding='utf-8')

if __name__ == '__main__':
    main()
    print 'Done!'
