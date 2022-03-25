from pathlib import Path
from rdflib import Graph, Literal, RDF, Namespace, URIRef, BNode
from rdflib.namespace import FOAF, RDFS, XSD, OWL
from PyPDF2 import PdfFileReader

from Utils.utils import extractFromPdf, DBLookup
from __init__ import ROOT_DIR
import os

if __name__ == '__main__':

    g = Graph()

    FOCU = Namespace("http://focu.io/schema#")
    FOCUDATA = Namespace("http://focu.io/data#")
    VIVO = Namespace("http://vivoweb.org/ontology/core#")
    VCARD = Namespace("http://www.w3.org/2006/vcard/ns#")
    BIBO = Namespace('http://purl.org/ontology/bibo/')
    DBR = Namespace('http://dbpedia.org/resource/')

    g.bind("rdfs", RDFS)
    g.bind("rdf", RDF)
    g.bind("xsd", XSD)
    g.bind("foaf", FOAF)
    g.bind("focu", FOCU)
    g.bind("focudata", FOCUDATA)
    g.bind('vivo', VIVO)
    g.bind('vcard', VCARD)
    g.bind('bibo', BIBO)

    comp474_lecturesPath = os.path.join(ROOT_DIR, 'Data', 'Lectures', 'COMP474')
    topicsPath = os.path.join(ROOT_DIR, 'Data', 'Topics')

    # automated extraction of topics from slides and worksheets
    for lectureNum in range(1, 8):
        slideURI = URIRef(os.path.join(comp474_lecturesPath, 'Slides',
                                       'slides' + "%02d" % lectureNum + '.pdf').replace('\\', '/'))
        worksheetURI = URIRef(os.path.join(comp474_lecturesPath, 'Worksheets',
                                           'worksheet' + "%02d" % lectureNum + '.pdf').replace('\\', '/'))

        for source in [('slides', 'Slides'), ('worksheet', 'Worksheets')]:
            filePath = os.path.join(comp474_lecturesPath, source[1], source[0] + "%02d" % lectureNum + '.pdf')
            with open(filePath, mode='rb') as f:

                # initialize reader
                reader = PdfFileReader(f)

                # extract topics from pdf
                topics = extractFromPdf(reader, 'topics')
                for i, topic in enumerate(topics):
                    uniqueID = str(hash(('COMP474' + topic)))[1:7]
                    topicURI = URIRef(FOCUDATA + 'topic' + uniqueID)

                    dbpediaURI = DBLookup(topic)
                    print(Path(filePath).stem, f'\ntopic{i}', ':', topic, '\ndbpediaURI', dbpediaURI, '\n')
                    if DBLookup(topic) is None:
                        continue

                    dbpediaURI = URIRef(DBLookup(topic))

                    sourceURI = slideURI if source[0] == 'slides' else worksheetURI
                    g.add((sourceURI, FOCU.covers, topicURI))
                    g.add((topicURI, RDF.type, FOCU.topic))
                    g.add((topicURI, OWL.sameAs, dbpediaURI))
                    g.add((topicURI, RDFS.label, Literal(topic, datatype=XSD.string)))

    lectures_pathname = os.path.join(topicsPath, 'topics.ttl')
    g.serialize(lectures_pathname, format='turtle')
