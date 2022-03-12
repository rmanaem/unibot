import os

import pandas as pd
from rdflib import Graph, Literal, RDF, Namespace, URIRef
from rdflib.namespace import FOAF, RDFS, XSD
from __init__ import ROOT_DIR

if __name__ == '__main__':
    course_data = pd.read_csv('course_catalog.csv',
                              delimiter=',',
                              encoding='unicode_escape')
    course_description = pd.read_csv('course_description.csv',
                                     delimiter=',',
                                     encoding='unicode_escape')
    df = course_data.merge(course_description, how='left', on='Course ID')
    g = Graph()

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

    # Get Concordia courses' information
    for index, row in df.iterrows():
        uri = URIRef(FOCUDATA + str(row['Course ID']))
        g.add((uri, VIVO.Identification, Literal(row['Course ID'], datatype=XSD.integer)))
        g.add((uri, VIVO.hasSubjectArea, Literal(row['Subject'], datatype=XSD.string)))
        g.add((uri, VIVO.Catalog, Literal(row['Catalog'], datatype=XSD.integer)))
        g.add((uri, VIVO.Title, Literal(row['Long Title'], datatype=XSD.string)))
        g.add((uri, VIVO.CourseCredits, Literal(row['Class Units'], datatype=XSD.integer)))
        g.add((uri, VIVO.shortDescription, Literal(row['Descr'], datatype=XSD.string)))

    # add outline and seeAlso to comp474
    comp474_uri = URIRef(FOCUDATA + str(5484))
    g.add((comp474_uri, VIVO.description,
           URIRef('file///' + os.path.join(ROOT_DIR, 'Data', 'CourseInfo', 'comp474_outline.pdf').replace('\\', '/'))))
    g.add((comp474_uri, RDFS.seeAlso,
           URIRef('https://aits.encs.concordia.ca/aits/public/top/courses/20194/05/COMP474.html')))

    g.serialize('CourseInfo.ttl', format='turtle')
