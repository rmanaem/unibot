import glob

from pathlib import Path
from rdflib import Graph, Literal, RDF, Namespace, URIRef, BNode
from rdflib.namespace import FOAF, RDFS, XSD, OWL
from PyPDF2 import PdfFileReader

from Utils.extractImages import extractImages
from Utils.extractVideos import extractVideos
from Utils.utils import extractFromPdf, getCourseId
from __init__ import ROOT_DIR
import os

if __name__ == '__main__':

    lecturesPath = os.path.join(ROOT_DIR, 'Data', 'Lectures')

    g = Graph()

    FOCU = Namespace("http://focu.io/schema#")
    FOCUDATA = Namespace("http://focu.io/data#")
    VIVO = Namespace("http://vivoweb.org/ontology/core#")
    VCARD = Namespace("http://www.w3.org/2006/vcard/ns#")

    g.bind("rdfs", RDFS)
    g.bind("rdf", RDF)
    g.bind("xsd", XSD)
    g.bind("foaf", FOAF)
    g.bind("focu", FOCU)
    g.bind("focudata", FOCUDATA)
    g.bind('vivo', VIVO)
    g.bind('vcard', VCARD)

    # add seeAlso to Lecture01 of comp474
    g.add(((URIRef(FOCUDATA + '005484_Lecture01')), RDFS.seeAlso,
           URIRef('https://www.coursehero.com/file/58197534/slides01pdf/')))

    # add outline and seeAlso to comp474
    comp474_uri = URIRef(FOCUDATA + 'courseID_005484')
    g.add((comp474_uri, FOCU.outline,
           URIRef(os.path.join(lecturesPath, 'COMP474', 'CourseInfo', 'Outline.pdf').replace('\\', '/'))))
    g.add((comp474_uri, RDFS.seeAlso,
           URIRef('https://aits.encs.concordia.ca/aits/public/top/courses/20194/05/COMP474.html')))

    # add outline to comp6721
    comp474_uri = URIRef(FOCUDATA + 'courseID_040353')
    g.add((comp474_uri, FOCU.outline,
           URIRef(os.path.join(lecturesPath, 'COMP6721', 'CourseInfo', 'Outline.pdf').replace('\\', '/'))))

    g.serialize(os.path.join(ROOT_DIR, 'Data', 'focudata.ttl'), format='turtle')
