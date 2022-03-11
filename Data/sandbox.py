from SPARQLWrapper import SPARQLWrapper, CSV, JSON, XML, N3, RDFXML, TURTLE
from rdflib import Graph, Literal, RDF, Namespace
from rdflib.namespace import FOAF, RDFS, XSD


if __name__ == '__main__':
    g = Graph()
    g.parse('schema.ttl', format='n3')

    FOCU = Namespace("http://focu.io/schema#")
    FOCUDATA = Namespace("http://focu.io/data#")
    DBR = Namespace("http://dbpedia.org/resource/")
    DBO = Namespace("http://dbpedia.org/ontology/")
    VIVO = Namespace("http://vivoweb.org/ontology/core#")

    g.bind("rdfs", RDFS)
    g.bind("rdf", RDF)
    g.bind("xsd", XSD)
    g.bind("foaf", FOAF)
    g.bind("dbr", DBR)
    g.bind("dbo", DBO)
    g.bind("focu", FOCU)
    g.bind("focudata", FOCUDATA)
    g.bind('vivo', VIVO)

    # Get all canadian universities' information
    query = """
            @prefix vivo: <http://vivoweb.org/ontology/core#> .
            CONSTRUCT{
            ?dbp_uri rdf:type vivo:University ;
            rdfs:label ?name ;
            owl:sameAs ?wd_uri .
            }
            WHERE {
                {?dbp_uri rdf:type dbo:EducationalInstitution} 
                    UNION
                {?dbp_uri rdf:type schema:CollegeOrUniversity} .
                
                dbr:List_of_universities_in_Canada dbo:wikiPageWikiLink ?dbp_uri .
                ?dbp_uri rdfs:label ?name .
                ?dbp_uri owl:sameAs ?wd_uri .
                
                FILTER(regex(str(?wd_uri), "www.wikidata.org"))
                FILTER(lang(?name) = 'en')
            } ORDER BY ?name
            """

    sparql = SPARQLWrapper('http://dbpedia.org/sparql')
    sparql.setQuery(query)

    sparql.setReturnFormat(N3)
    results = sparql.query().convert()
    print(results)

    with open('test.txt', 'wb') as f:
        f.write(results)
