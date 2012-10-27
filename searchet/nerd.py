#!/usr/bin/python

import rdflib
from rdflib import Graph, URIRef
rdf = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
rdfs = "http://www.w3.org/2000/01/rdf-schema#"
owl = "http://www.w3.org/2002/07/owl#"  
alchemyapi = "http://www.alchemyapi.com/api/entity/types.html#"
dbpedia_owl = "http://dbpedia.org/ontology/"
extractiv = "http://wiki.extractiv.com/w/page/29179775/Entity-Extraction#"
opencalais = "http://www.opencalais.com/documentation/calais-web-service-api/api-metadata/entity-index-and-definitions#"
wikimeta = "http://www.wikimeta.com/"
zemanta = "http://developer.zemanta.com/docs/entity_type/"
nerd = "http://nerd.eurecom.fr/ontology#"
searchet = "http://searchet.baidu.com/ontology#"
freebase = "http://schemas.freebaseapps.com/type?id="
    
class nerd:
    def __init__(self, source, format):
        self.source = source
        self.format = format
        self.graph = Graph()
        self.result = self.graph.parse(source, format=format)

    def get_subjects(self, predicate, object):
        res = self.graph.subjects(predicate=URIRef(owl+predicate), object=URIRef(alchemyapi+object))
        result = []
        for k in res:
            result.append(k)
        return result
        # return self.graph.subjects(predicate, object)
    def get_subClasses(self, subject, predicate):
        res = self.graph.objects(subject=URIRef("http://searchet.baidu.com/ontology#"+subject), predicate=URIRef("http://www.w3.org/2000/01/rdf-schema#"+predicate))
        result = []
        for k in res:
            result.append(k)
        return result
    
    def getAllClass(self, keywords):
        key_list = []
        res = self.get_subjects('equivalentClass', keywords)
        while res:
            tstr = res[0].split('#')
            if len(tstr)>1:
                key_list.append(tstr[1])
                res = self.get_subClasses(tstr[1], "subClassOf")
        return key_list    

if __name__ == "__main__": 
    
    nerd_in = nerd("/home/penser/Downloads/searchet_v2.n3", format="n3")
    
    result = nerd_in.get_subjects("equivalentClass", "Athlete")
    for s in result:
         print s
    
    result = nerd_in.get_subClasses("TennisPlayer", "subClassOf")
    for s in result:
         print s
    
    """g = Graph()
    result = g.parse("/home/penser/Downloads/nerd-last.n3", format="n3")
    for stmt in g.subjects(predicate=URIRef("http://www.w3.org/2002/07/owl#"+"equivalentClass"), object=URIRef("http://www.alchemyapi.com/api/entity/types.html#Person")):
        print stmt
    """
    #for stmt in nerd_instance.graph.subject_objects(URIRef("http://www.w3.org/2002/07/owl#equivalentClass")):
     #   print stmt
    
