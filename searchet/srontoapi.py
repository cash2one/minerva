#!/usr/bin/python
# -*- coding: utf-8 -*-

##
#
# @author Shudong Huang
# @contact v_huangshudong@baidu.com
#
# @reviewer Yuan Jin
# @contact jinyuan@baidu.com
#
# @created Sept. 6, 2012
# @updated Sept. 24, 2012
#

import sys
reload(sys)
sys.setdefaultencoding('UTF-8')

import rdflib
from rdflib import Graph, URIRef, Namespace

rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")
owl = Namespace("http://www.w3.org/2002/07/owl#")
alchemyapi = Namespace("http://www.alchemyapi.com/api/entity/types.html#")
dbpedia = Namespace("http://dbpedia.org/ontology/")
opencalais = Namespace("http://www.opencalais.com/documentation/calais-web-service-api/api-metadata/entity-index-and-definitions#")
zemanta = Namespace("http://developer.zemanta.com/docs/entity_type/")
searchet = Namespace("http://searchet.baidu.com/ontology#")
freebase = Namespace("http://schemas.freebaseapps.com/type?id=")

    
class SearchetOntology:
    '''docs'''
    def __init__(self, source=None, format=None):
        self.graph = Graph()
        self.graph.parse(source, format=format)

    def get_searchet_class(self, triple_object=None):
        '''find the equivalent searchet class'''
        res = self.graph.subjects(predicate=URIRef(owl['equivalentClass']), object=triple_object)
        result = []
        for r in res:
            result.append(r)

        # temporary measure
        if result:
            return result[0]
        else:
            return None

    def get_parent_class(self, triple_subject=None):
        '''find the parent class via subClassOf'''
        res = self.graph.objects(subject=triple_subject, predicate=URIRef(rdfs['subClassOf']))
        result = []
        for r in res:
            result.append(r)

        # temporary measure
        if result:
            return result[0]
        else:
            return None
    
    def get_pedigree(self, namespace=None, keyword=None):
        '''find the parent of parent of ... parent of the keyword'''
        ns = Namespace(namespace)
        searchet_class = self.get_searchet_class(URIRef(ns[keyword]))
        
        parent_class = self.get_parent_class(searchet_class)
        current_class = parent_class
        if parent_class:
            while parent_class:
                current_class = parent_class
                parent_class = self.get_parent_class(parent_class)
            return current_class
        else: # if nothing is the parent, itself is the top class
            return searchet_class


