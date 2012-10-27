#!/usr/bin/python
# -*- coding: utf-8 -*-

##
#
# @author Yuan Jin
# @contact jinyuan@baidu.com
# @created Sept. 26, 2012
# @updated Sept. 26, 2012
#

# imports and CONSTANTS
import sys
reload(sys)
sys.setdefaultencoding('UTF-8')

import freebase
import HTMLParser
import os
import re
import simplejson
import string
import threading
import urllib2
import web

sys.path.append('/var/www/cgi-bin')
more_tag_template = '''<a href="http://en.wikipedia.org/wiki/index.html?curid=%s" target="_blank"> more</a>'''
tpl_dir = '/var/www/html/templates/'


class Format_Summary(threading.Thread):
    def __init__(self, summary_id):
        threading.Thread.__init__(self)
        self.summary_id = summary_id
        self.result = ''

    def run(self):
        introduction = freebase.raw(self.summary_id)
        self.result = introduction

class Format_WikiURL(threading.Thread):
    def __init__(self, freebase_id):
        threading.Thread.__init__(self)
        self.freebase_id = freebase_id
        self.result = ''

    def run(self):
        query = [{'id':'%s' % self.freebase_id, 'wiki_en:key':{'/type/key/namespace':'/wikipedia/en_id', 'value':None, 'optional':True}}]
        response = freebase.mqlread(query)
        if response[0] and 'wiki_en:key' in response[0]:
            wiki_id = str(response[0]['wiki_en:key']['value'])
            self.result = more_tag_template % wiki_id
        else:
            self.result = ''

def format(item_ids, searches):
    result = {}
    query = [{"master_property": [{}], "source": {"id": ''}, "target": [{}], "target_value": [{}], "type": "/type/link"}]

    def format_image(image_id):
        if image_id:
            return "http://img.freebase.com/api/trans/image_thumb%s?maxheight=300&mode=fit&maxwidth=150" % image_id
        else:
            return None

    def format_properties(properties, prop_key, prop_value):
        ''' incremental '''
        if not properties:
            properties = {}

        if prop_value:
            if prop_key in properties:
                if prop_value not in properties[prop_key]:
                    properties[prop_key].append(prop_value)
            else:
                properties[prop_key] = []
                properties[prop_key].append(prop_value)

        return properties

    def query_parser(item_id):
        # summary, photo and properties
        query[0]['source']['id'] = item_id
        response = freebase.mqlread(query)

        summary = ''
        image = ''
        name = ''
        more_url = ''
        # key:string value:dedup list
        properties = {}
        t_format_summary = None
        t_format_wikiurl = Format_WikiURL(item_id)
        t_format_wikiurl.start()

        for r in response:
            # summary
            if r['master_property'][0]['id'] == '/common/topic/article':
                t_format_summary = Format_Summary(r['target'][0]['id'])
                t_format_summary.start()
            # image
            elif r['master_property'][0]['id'] == '/common/topic/image':
                image = format_image(r['target'][0]['id'])
            # properties
            else:
                if r['target_value'] and r['target_value'][0]:
                    if r['master_property'][0]['name'] == 'Name':
                        if r['target'][0]['name'] != 'English':
                            continue
                    properties = format_properties(properties, r['master_property'][0]['name'], r['target_value'][0]['value'])
                elif r['target'] and r['target'][0]:
                    properties = format_properties(properties, r['master_property'][0]['name'], r['target'][0]['name'])
                else:
                    properties = format_properties(properties, r['master_property'][0]['name'], '')

        if t_format_summary:
            t_format_summary.join()
            t_format_wikiurl.join()
            if t_format_summary.result:
                summary = t_format_summary.result

            if t_format_wikiurl.result:
                more_url = t_format_wikiurl.result

            if 'Name' in properties:
                name = properties.pop('Name')[0]
            if 'Permission' in properties:
                properties.pop('Permission')
            if 'Type' in properties:
                properties.pop('Type')
            if 'Hero image ID' in properties:
                properties.pop('Hero image ID')
        else:
            summary = ''
            image = ''
            name = ''
            more_url = ''
            properties = {}

        return summary, image, name, more_url, properties
    
    # currently support only one item_id
    filled_values = {}
    if item_ids:
        for item_id in item_ids:
            s, i, n, m, p = query_parser(item_id)

            filled_values['title'] = n
            filled_values['image'] = i

            # flatten the properties
            property_table = []
            for k, v in p.iteritems():
                if len(property_table) < 7:
                    property_table.append((str(k), ', '.join(['%s' % el for el in v])))
                else:
                    break
            filled_values['attrs'] = property_table

            # flatten the common search results
            searches_table = []
            for search in searches:
                title = search['title']
                url = search['url']
                content = search['content']
                searches_table.append((title, url , content))
            filled_values['goog_results'] = searches_table

            filled_values['description'] = ''
            filled_values['images'] = ''
            filled_values['keywords'] = ''
            filled_values['more_link'] = ''

            if i: #take the with_photo_template
                clean = re.sub(r'</?\w+[^>]*>', '', s.strip()).split()
                length = len(clean)

                if length > 50:
                    s = '%s ...' % ' '.join(clean[:50])
                else:
                    s = ' '.join(clean)
            else:
                clean = re.sub(r'</?\w+[^>]*>', '', s.strip()).split()
                length = len(clean)

                if length > 70:
                    s = '%s ...' % ' '.join(clean[:70])
                else:
                    s = ' '.join(clean)
            filled_values['summary'] = s

            render = web.template.render(tpl_dir, base='base', globals=filled_values)
            return render.index()
    # can hardly find any structured information
    else:
        filled_values = {}
        filled_values['title'] = ''
        filled_values['image'] = ''
        filled_values['summary'] = ''
        filled_values['attrs'] = ''
        filled_values['description'] = ''
        filled_values['images'] = ''
        filled_values['keywords'] = ''
        filled_values['more_link'] = ''

        searches_table = []
        for search in searches:
            title = search['title']
            url = search['url']
            content = search['content']
            searches_table.append((title, url , url, content))
        filled_values['goog_results'] = searches_table

        render = web.template.render(tpl_dir, base='base', globals=filled_values)
        return render.index()

# independent search tasks
class Freebase_Keys(threading.Thread):
    def __init__(self, query):
        threading.Thread.__init__(self)
        self.query = query
        self.result = []

    def run(self):
        data = freebase.mqlread(self.query)
        # only one id is necessary
        if data and 'id' in data:
            self.result.append(data['id'][0]['value'])

class Freebase_Search(threading.Thread):
    def __init__(self, keyword):
        threading.Thread.__init__(self)
        self.keyword = keyword
        self.result = []

    def run(self):
        data = freebase.search(query=self.keyword, limit=3)
        if data:
            # several ids are necessary as the result of fact that the key search cannot find results
            self.result = [d['id'] for d in data if 'id' in d]

class Google_Search(threading.Thread):
    def __init__(self, keyword):
        threading.Thread.__init__(self)
        self.keyword = keyword.replace(' ', '%20')
        self.result = []

    def run(self):
        query = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=%s' % self.keyword
        response = urllib2.urlopen(query)
        json = simplejson.loads(response.read())
        self.result = json['responseData']['results']

def text_process(query, keyword):
    t_freebase_key = Freebase_Keys(query)
    t_freebase_search = Freebase_Search(keyword)
    t_google = Google_Search(keyword)

    t_freebase_key.start()
    t_freebase_search.start()
    t_google.start()

    # at least freebase keys search and google should finish
    t_freebase_key.join()
    t_google.join()

    # assuming google would always find some results
    if t_freebase_key.result:
        print t_freebase_key.result
        return t_freebase_key.result, t_google.result
    else:
        t_freebase_search.join()
        return t_freebase_search.result, t_google.result

def search(query):
    '''string process'''
    keywords = []
    if not len(query):
        return None
    elif len(query):
        keywords = query[0].split()

    def text_to_lower_capitalized(keyword):
        # the key might be all lower-cased letters
        lower_cased = '_'.join(token.strip() for token in keyword.lower().split())
        # or capitalized
        capitalized = '_'.join(token.strip() for token in keyword.title().split())
        return lower_cased, capitalized

    output_lower = []
    output_capitalized = []
    output_plain = []
    for key in keywords:
        whitelist = string.letters + string.digits + ' '
        keyword = re.sub("[^0-9a-zA-Z]", " ", key).strip()

        lower, capitalized = text_to_lower_capitalized(keyword)
        output_lower.append(lower)
        output_capitalized.append(capitalized)
        output_plain.append(keyword.strip())

    query = {'key|=':['_'.join(output_lower), '_'.join(output_capitalized)], 'id':[{}], 'limit':1}
    structured, natural = text_process(query, ' '.join(output_plain))
    return str(format(structured, natural))