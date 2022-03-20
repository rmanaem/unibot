import glob

from pathlib import Path
from rdflib import Graph, Literal, RDF, Namespace, URIRef, BNode
from rdflib.namespace import FOAF, RDFS, XSD, OWL
from PyPDF2 import PdfFileReader

from Data.Courses.extractImages import extractImages
from Data.Courses.extractVideos import extractVideos
from Data.Courses.pdfOperations import extractFromPdf
from __init__ import ROOT_DIR
import os

if __name__ == '__main__':

    comp474_Lectures = os.path.join(ROOT_DIR, 'Data', 'Courses', 'COMP474', 'Lectures')

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

    slidesDir = os.path.join(comp474_Lectures, 'Slides')
    slidesCount = len(os.listdir(slidesDir))
    filepaths = [os.path.join(slidesDir, 'slides') + "%02d" % num + '.pdf' for num in range(1, slidesCount + 1)]

    courseName = 'COMP474'
    for filepath in filepaths:
        with open(filepath, mode='rb') as f:
            reader = PdfFileReader(f)
            lectureNum = extractFromPdf(reader, 'num')
            lectureName = extractFromPdf(reader, 'name')
            required, supplemental = extractFromPdf(reader, 'readings')

            print(lectureNum, lectureName)
            print('Required readings', required)
            print('Supplemental readings', supplemental, '\n\n')

            lectureURI = URIRef(FOCUDATA + 'Lecture' + str("%02d" % lectureNum))
            g.add((lectureURI, RDF.type, URIRef(FOCU.lecture)))

            slideURI = URIRef('file///' + os.path.join(ROOT_DIR, 'Data', 'Lectures', 'Slides',
                                                       'slides' + "%02d" % lectureNum + '.pdf').replace('\\', '/'))
            g.add((lectureURI, VIVO.contains, slideURI))
            g.add((slideURI, RDF.type, FOCU.slide))
            g.add((slideURI, RDFS.subClassOf, lectureURI))

            worksheetURI = URIRef('file///' + os.path.join(ROOT_DIR, 'Data', 'Lectures', 'Worksheets',
                                                           'worksheet' + "%02d" % lectureNum + '.pdf').replace('\\',
                                                                                                               '/'))
            g.add((lectureURI, VIVO.contains, worksheetURI))
            g.add((worksheetURI, RDF.type, FOCU.worksheet))
            g.add((worksheetURI, RDFS.subClassOf, lectureURI))

            lastReading = None
            for index, reading in enumerate(required):
                # the pattern in the reading array is: [title, URI, title, URI, ...]
                if index % 2 == 0:
                    lastReading = reading
                    continue

                readingsURI = URIRef(FOCUDATA + 'Readings' + str("%02d" % lectureNum))
                readingURI = URIRef(FOCUDATA + 'Reading' + str("%02d" % lectureNum))

                g.add((readingsURI, RDFS.subClassOf, lectureURI))
                g.add((readingsURI, VIVO.contains, readingURI))
                g.add((readingsURI, RDF.type, FOCU.readings))

                g.add((readingURI, RDFS.subClassOf, FOCUDATA.required))
                g.add((readingURI, VCARD.URL, URIRef(reading)))
                g.add((readingURI, VIVO.Title, Literal(lastReading)))
                g.add((readingURI, RDF.type, FOCU.reading))

            otherMaterialURI = URIRef(FOCUDATA + 'otherMaterial' + str("%02d" % lectureNum))
            g.add((lectureURI, VIVO.contains, URIRef(FOCU.otherMaterial)))
            g.add((otherMaterialURI, RDF.type, URIRef(FOCU.otherMaterial)))
            g.add((otherMaterialURI, RDFS.subClassOf, lectureURI))

            extractImages(filepath)
            folder = glob.glob(
                os.path.join(ROOT_DIR, 'Data', 'Lectures', 'OtherMaterial', 'Images', Path(filepath).stem, '*'))
            for image in folder:
                imageURI = URIRef(('file///' + image).replace('\\', '/'))
                g.add((otherMaterialURI, VIVO.contains, imageURI))
                g.add((imageURI, RDF.type, VIVO.Image))

            extractVideos(reader, courseName, lectureNum)
            folder = glob.glob(
                os.path.join(ROOT_DIR, 'Data', 'Lectures', 'OtherMaterial', 'Videos', Path(filepath).stem, '*'))
            for video in folder:
                videoURI = URIRef(('file///' + video).replace('\\', '/'))
                g.add((otherMaterialURI, VIVO.contains, videoURI))
                g.add((videoURI, RDF.type, VIVO.Video))

    g.add(((URIRef(FOCUDATA + 'Lecture01')), RDFS.seeAlso,
           URIRef('https://www.coursehero.com/file/58197534/slides01pdf/')))

    lectures_pathname = os.path.join(comp474_Lectures, 'Lectures.ttl')
    g.serialize(lectures_pathname, format='turtle')
