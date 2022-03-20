import os

import numpy as np
import pandas as pd
from rdflib import Graph, Literal, RDF, Namespace, URIRef
from rdflib.namespace import FOAF, RDFS, XSD
from __init__ import ROOT_DIR


if __name__ == '__main__':

    students_pathname = os.path.join(ROOT_DIR, 'Data', 'Students')
    first_pathname = os.path.join(students_pathname, 'first.txt')
    last_pathname = os.path.join(students_pathname, 'last.txt')
    np.random.seed(0)
    count = 900

    # Generate the information for students
    first = pd.read_csv(first_pathname, sep="\n").sample(
        n=count).transpose().values.tolist()[0]
    last = pd.read_csv("last.txt", sep="\n").sample(
        n=count).transpose().values.tolist()[0]
    ids = np.random.randint(40000000, 50000000, count)
    df = pd.DataFrame({'Firstname': first, 'Lastname': last,
                      'ID': ids, 'University': 'Concordia_University'})

    FOCU = Namespace("http://focu.io/schema#")
    FOCUDATA = Namespace("http://focu.io/data#")
    DBR = Namespace("http://dbpedia.org/resource/")
    DBO = Namespace("http://dbpedia.org/ontology/")
    VIVO = Namespace("http://vivoweb.org/ontology/core#")

    g = Graph()
    g.bind("rdfs", RDFS)
    g.bind("rdf", RDF)
    g.bind("xsd", XSD)
    g.bind("foaf", FOAF)
    g.bind("dbr", DBR)
    g.bind("dbo", DBO)
    g.bind("focu", FOCU)
    g.bind("focudata", FOCUDATA)
    g.bind('vivo', VIVO)

    for index, row in df.iterrows():
        uri = URIRef(FOCUDATA + 'studentID_' + str(row['ID']))
        uni_uri = URIRef(DBR+row['University'])
        g.add((uri, RDF.type, VIVO.Student))
        g.add((uri,  VIVO.identification, Literal(str(row['ID']))))
        g.add((uri, FOAF.givenName, Literal(row['Firstname'])))
        g.add((uri, FOAF.familyName, Literal(row['Lastname'])))
        g.add((uri, FOCU.studentAt, uni_uri))
        g.add((uri, FOAF.mbox, Literal(
            row['Firstname'][:1] + '_' + row['Lastname'] + '@' + row['University'] + '.com')))

    g.serialize('Students.ttl', format='turtle')
