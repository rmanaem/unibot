from pathlib import Path
from rdflib import Graph, Literal, RDF, Namespace, URIRef
from rdflib.namespace import FOAF, RDFS, XSD

from Utils.utils import extract_ne_list, spotlight_over_text
from __init__ import ROOT_DIR
import os

import warnings

warnings.filterwarnings("ignore")


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
            worksheetURI = URIRef(os.path.join(path, 'Worksheets', 'worksheet' + "%02d" % lectureNum + '.pdf').replace('\\', '/'))
            labURI = URIRef(os.path.join(path, 'Labs', 'lab' + "%02d" % lectureNum + '.pdf').replace('\\', '/'))
            outlineURI = URIRef(os.path.join(path, 'CourseInfo', 'Outline' + '.pdf').replace('\\', '/'))

            for source in [('slides', 'Slides'), ('worksheet', 'Worksheets'), ('lab', 'Labs'), ('Outline', 'CourseInfo')]:
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
                topics = extract_ne_list(spotlight_over_text(filePath))

                for i, topic in enumerate(topics):
                    dbpediaURI, dbpediaLabel = topic[0], topic[1]
                    dbpediaURI = URIRef(dbpediaURI)  # convert URI to URIRef object

                    print(Path(filePath).stem, f'\ntopic{i} :', topic, '\ndbpediaURI', dbpediaURI, '\ndbpedialabel :', dbpediaLabel, '\n')

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
                    g.add((dbpediaURI, RDFS.label, Literal(dbpediaLabel, datatype=XSD.string)))

    lectures_pathname = os.path.join(topicsPath, 'topics.ttl')
    g.serialize(lectures_pathname, format='turtle')
