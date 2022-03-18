from SPARQLWrapper import SPARQLWrapper, CSV, JSON, XML, N3, RDFXML, TURTLE


def getUniversities():
    """
    connects to dbpedia's remote sparql endpoint and executes the following query.
    The query outputs a list of all canadian universities and some information including:
        dbpedia link
        type
        label
        wikidata link
    :return: rdf data in turtle format
    """
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

    return results


if __name__ == '__main__':
    with open('Universities.ttl', 'wb') as f:
        f.write(getUniversities())
