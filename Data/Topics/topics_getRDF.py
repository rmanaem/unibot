from pathlib import Path
from rdflib import Graph, Literal, RDF, Namespace, URIRef, BNode
from rdflib.namespace import FOAF, RDFS, XSD, OWL

from Utils.utils import extract_ne, DBLookup
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
    comp6721_lecturePath = os.path.join(ROOT_DIR, 'Data', 'Lectures', 'COMP6721')
    topicsPath = os.path.join(ROOT_DIR, 'Data', 'Topics')

    # automated extraction of topics from slides and worksheets
    for idx, path in enumerate([comp474_lecturesPath, comp6721_lecturePath]):
        for lectureNum in range(1, 8):
            slideURI = URIRef(os.path.join(path, 'Slides', 'slides' + "%02d" % lectureNum + '.pdf').replace('\\', '/'))
            worksheetURI = URIRef(os.path.join(path, 'Worksheets',
                                               'worksheet' + "%02d" % lectureNum + '.pdf').replace('\\', '/'))
            labURI = URIRef(os.path.join(path, 'Labs', 'lab' + "%02d" % lectureNum + '.pdf').replace('\\', '/'))

            for source in [('slides', 'Slides'), ('worksheet', 'Worksheets'), ('lab', 'Labs')]:
                filePath = os.path.join(
                    path, source[1], source[0] + "%02d" % lectureNum + '.pdf')

                # with open(filePath, mode='rb') as f:
                # initialize reader
                # reader = PdfFileReader(f)

                # extract topics from pdf
                topics = extract_ne(filePath)

                # for None topics
                # if not topics:
                #     print('Skipped')
                #     continue

                for i, topic in enumerate(topics):
                    if idx == 0:
                        uniqueID = str(hash(('COMP474' + topic)))[1:7]
                    else:
                        uniqueID = str(hash(('COMP6721' + topic)))[1:7]

                    topicURI = URIRef(FOCUDATA + 'topic' + uniqueID)

                    dbpediaURI = DBLookup(topic)
                    print(Path(filePath).stem, f'\ntopic{i}', ':', topic, '\ndbpediaURI', dbpediaURI, '\n')

                    if DBLookup(topic) is None:
                        continue

                    # lookup dbpedia URI
                    dbpediaURI = URIRef(DBLookup(topic))

                    sourceURI = slideURI  # default value
                    if source[0] == 'slides':
                        sourceURI = slideURI
                    elif source[0] == 'worksheets':
                        sourceURI = worksheetURI
                    elif source[0] == 'labs':
                        sourceURI = labURI

                    # update graph
                    g.add((sourceURI, FOCU.covers, topicURI))
                    g.add((topicURI, RDF.type, FOCU.topic))
                    g.add((topicURI, OWL.sameAs, dbpediaURI))
                    g.add((topicURI, RDFS.label, Literal(topic, datatype=XSD.string)))

    lectures_pathname = os.path.join(topicsPath, 'topics.ttl')
    g.serialize(lectures_pathname, format='turtle')
