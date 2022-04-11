from pathlib import Path
from rdflib import Graph, Literal, RDF, Namespace, URIRef
from rdflib.namespace import FOAF, RDFS, XSD

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

    comp474_lecturesPath = os.path.join(
        ROOT_DIR, 'Data', 'Lectures', 'COMP474')
    comp6721_lecturePath = os.path.join(
        ROOT_DIR, 'Data', 'Lectures', 'COMP6721')
    topicsPath = os.path.join(ROOT_DIR, 'Data', 'Topics')

    # automated extraction of topics from slides and worksheets
    for idx, path in enumerate([comp474_lecturesPath, comp6721_lecturePath]):
        for lectureNum in range(1, 8):
            slideURI = URIRef(os.path.join(
                path, 'Slides', 'slides' + "%02d" % lectureNum + '.txt').replace('\\', '/'))
            worksheetURI = URIRef(os.path.join(path, 'Worksheets',
                                               'worksheet' + "%02d" % lectureNum + '.txt').replace('\\', '/'))
            labURI = URIRef(os.path.join(path, 'Labs', 'lab' + "%02d" %
                            lectureNum + '.txt').replace('\\', '/'))
            outlineURI = URIRef(os.path.join(
                path, 'CourseInfo', 'Outline' + '.txt').replace('\\', '/'))

            for source in [('slides', 'Slides'), ('worksheet', 'Worksheets'), ('lab', 'Labs'),
                           ('Outline', 'CourseInfo')]:
                if source[0] == 'Outline':
                    if lectureNum == 1:
                        filePath = os.path.join(
                            path, source[1], source[0] + '.txt')
                    else:
                        continue
                else:
                    filePath = os.path.join(
                        path, source[1], source[0] + "%02d" % lectureNum + '.txt')

                # extract topics from pdf
                topics = extract_ne(filePath)

                for i, topic in enumerate(topics):
                    if idx == 0:
                        uniqueID = str(hash(('COMP474' + topic)))[1:7]
                    else:
                        uniqueID = str(hash(('COMP6721' + topic)))[1:7]

                    # lookup dbpedia URI and label
                    dbpediaURI, dbpediaLabel = None, 'None'
                    try:
                        dbpediaURI, dbpediaLabel = DBLookup(topic)
                    except Exception:
                        print('bug')

                    try:
                        print(Path(filePath).stem, f'\ntopic{i} :', topic, '\ndbpediaURI', dbpediaURI,
                              '\ndbpedialabel :', dbpediaLabel, '\n')
                    except UnicodeEncodeError:
                        print(
                            'cant print in this python console, but it doesnt affect the rest of code')

                    if dbpediaURI is None:
                        continue

                    # convert URI to URIRef object
                    dbpediaURI = URIRef(dbpediaURI)

                    sourceURI = slideURI  # default value
                    if source[0] == 'slides':
                        sourceURI = slideURI
                    elif source[0] == 'worksheet':
                        sourceURI = worksheetURI
                    elif source[0] == 'lab':
                        sourceURI = labURI
                    elif source[0] == 'Outline':
                        sourceURI = outlineURI

                    # update graph
                    g.add((sourceURI, FOCU.covers, dbpediaURI))
                    g.add((dbpediaURI, RDF.type, FOCU.topic))
                    g.add((dbpediaURI, RDFS.label, Literal(
                        dbpediaLabel, datatype=XSD.string)))

    lectures_pathname = os.path.join(topicsPath, 'topics.ttl')
    g.serialize(lectures_pathname, format='turtle')
