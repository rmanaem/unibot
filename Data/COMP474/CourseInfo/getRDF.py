import os

import pandas as pd
from rdflib import Graph, Literal, RDF, Namespace, URIRef
from rdflib.namespace import FOAF, RDFS, XSD
from __init__ import ROOT_DIR

if __name__ == '__main__':
    data_pathname = os.path.join(ROOT_DIR, 'Data')
    catalog_pathname = os.path.join(
        data_pathname, 'CourseInfo', 'course_catalog.csv')
    course_description_pathname = os.path.join(
        data_pathname, 'CourseInfo', 'course_description.csv')

    course_data = pd.read_csv(catalog_pathname,
                              delimiter=',',
                              encoding='unicode_escape')
    course_description = pd.read_csv(course_description_pathname,
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
        uri = URIRef(FOCUDATA + "courseID" + "_" + str(row['Course ID']))
        g.add((uri, VIVO.Identification, Literal(
            row['Course ID'], datatype=XSD.integer)))
        g.add((uri, VIVO.hasSubjectArea, Literal(
            row['Subject'], datatype=XSD.string)))
        g.add((uri, VIVO.Catalog, Literal(
            row['Catalog'], datatype=XSD.integer)))
        g.add((uri, VIVO.Title, Literal(
            row['Long Title'], datatype=XSD.string)))
        g.add((uri, VIVO.CourseCredits, Literal(
            row['Class Units'], datatype=XSD.integer)))
        g.add((uri, VIVO.shortDescription, Literal(
            row['Descr'], datatype=XSD.string)))

    # add outline and seeAlso to comp474
    comp474_uri = URIRef(FOCUDATA + str(5484))
    g.add((comp474_uri, VIVO.description,
           URIRef('file///' + os.path.join(data_pathname, 'CourseInfo', 'comp474_outline.pdf').replace('\\', '/'))))
    g.add((comp474_uri, RDFS.seeAlso,
           URIRef('https://aits.encs.concordia.ca/aits/public/top/courses/20194/05/COMP474.html')))

    g.serialize(os.path.join(data_pathname, 'CourseInfo',
                'CourseInfo.ttl'), format='turtle')
