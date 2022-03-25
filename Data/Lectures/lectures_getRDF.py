import glob
import hashlib

from pathlib import Path
from rdflib import Graph, Literal, RDF, Namespace, URIRef, BNode
from rdflib.namespace import FOAF, RDFS, XSD, OWL
from PyPDF2 import PdfFileReader

from Utils.extractImages import extractImages
from Utils.extractVideos import extractVideos
from Utils.utils import extractFromPdf, getCourseId, DBLookup
from __init__ import ROOT_DIR
import os

if __name__ == '__main__':

    courses = os.path.join(ROOT_DIR, 'Data', 'Courses')
    course_catalog = os.path.join(courses, 'course_catalog.csv')

    lecturesParentDir = os.path.join(ROOT_DIR, 'Data', 'Lectures')
    courseNames = [name for name in os.listdir(lecturesParentDir) if
                   os.path.isdir(os.path.join(lecturesParentDir, name)) and name != '__pycache__']

    for courseName in courseNames:

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

        print(courseName, '\n\n')
        courseNamePath = os.path.join(lecturesParentDir, courseName)

        slidesDir = os.path.join(courseNamePath, 'Slides')
        slidesCount = len(os.listdir(slidesDir))
        filepaths = [os.path.join(slidesDir, 'slides') + "%02d" % num + '.pdf' for num in range(1, slidesCount + 1)]

        for index, filepath in enumerate(filepaths):
            with open(filepath, mode='rb') as f:

                # initialize pdf reader
                reader = PdfFileReader(f)

                # automatic extraction of lecture slides information (name, number)
                lectureNum = index + 1 if courseName != 'COMP474' else extractFromPdf(reader, 'num')
                lectureName = 'Lecture' + str(lectureNum) if courseName != 'COMP474' else extractFromPdf(reader, 'name')
                print(lectureNum, lectureName)

                # get courseID from catalog
                courseID = str(getCourseId(course_catalog, courseName))

                # automatic extraction of readings from lecture slides
                required, supplemental = [], []
                if courseName == 'COMP474':
                    required, supplemental = extractFromPdf(reader, 'readings')
                    print('Required readings', required)
                    print('Supplemental readings', supplemental, '\n\n')

                # connect lectureURI to courseURI
                lectureURI = URIRef(FOCUDATA + courseID + '_Lecture' + str("%02d" % lectureNum))
                courseURI = URIRef(FOCUDATA + 'courseID_' + courseID)
                g.add((lectureURI, VIVO.Title, Literal(lectureName, datatype=XSD.string)))
                g.add((lectureURI, BIBO.number, Literal(lectureNum, datatype=XSD.integer)))
                g.add((courseURI, FOCU.hasContent, lectureURI))
                g.add((lectureURI, RDF.type, URIRef(FOCU.lecture)))

                # slideURI
                slideURI = URIRef(os.path.join(courseNamePath, 'Slides',
                                               'slides' + "%02d" % lectureNum + '.pdf').replace('\\', '/'))
                g.add((lectureURI, VIVO.contains, slideURI))
                g.add((slideURI, RDF.type, FOCU.slide))
                g.add((slideURI, RDFS.subClassOf, lectureURI))

                # worksheetURI
                worksheetURI = URIRef(os.path.join(courseNamePath, 'Worksheets',
                                                   'worksheet' + "%02d" % lectureNum + '.pdf').replace('\\', '/'))
                g.add((lectureURI, VIVO.contains, worksheetURI))
                g.add((worksheetURI, RDF.type, FOCU.worksheet))
                g.add((worksheetURI, RDFS.subClassOf, lectureURI))

                # readingURI
                readingsURI = URIRef(FOCUDATA + courseID + '_Readings' + str("%02d" % lectureNum))
                g.add((readingsURI, RDFS.subClassOf, lectureURI))
                g.add((lectureURI, VIVO.contains, readingsURI))
                g.add((readingsURI, RDF.type, FOCU.readings))

                # [title, URI, title, URI, ...] becomes [(title, URI), (title, URI), (...]
                it = iter(required)
                required = list(zip(it, it))

                it = iter(supplemental)
                supplemental = list(zip(it, it))

                # including required readings in graph
                for index, reading in enumerate(required):
                    readingURI = URIRef(FOCUDATA + courseID + '_req_readings' + str("%02d" % lectureNum) + str(
                        "_reading%02d" % (index + 1)))

                    g.add((readingsURI, VIVO.contains, readingURI))

                    g.add((readingURI, RDFS.subClassOf, FOCUDATA.required))
                    g.add((readingURI, VCARD.URL, URIRef(reading[1])))
                    g.add((readingURI, VIVO.Title, Literal(reading[0])))
                    g.add((readingURI, RDF.type, FOCU.reading))

                    g.add((readingURI, BIBO.number, Literal(index, datatype=XSD.integer)))

                # including supplemental readings in graph
                for index, reading in enumerate(supplemental):
                    readingURI = URIRef(FOCUDATA + courseID + '_sup_readings' + str("%02d" % lectureNum) + str(
                        "_reading%02d" % (index + 1)))

                    g.add((readingsURI, VIVO.contains, readingURI))

                    g.add((readingURI, RDFS.subClassOf, FOCUDATA.supplemental))
                    g.add((readingURI, VCARD.URL, URIRef(reading[1])))
                    g.add((readingURI, VIVO.Title, Literal(reading[0])))
                    g.add((readingURI, RDF.type, FOCU.reading))

                    g.add((readingURI, BIBO.number, Literal(index, datatype=XSD.integer)))

                # automated extraction of other material (videos & images)
                if courseName == 'COMP474':
                    otherMaterialURI = URIRef(FOCUDATA + courseID + '_otherMaterial' + str("%02d" % lectureNum))
                    g.add((lectureURI, VIVO.contains, otherMaterialURI))
                    g.add((otherMaterialURI, RDF.type, FOCU.otherMaterial))
                    g.add((otherMaterialURI, RDFS.subClassOf, lectureURI))

                    # extracting images and including absolute path (URIs) in graph
                    extractImages(filepath, courseName)
                    folder = glob.glob(
                        os.path.join(courseNamePath, 'OtherMaterial', 'Images', Path(filepath).stem, '*'))
                    for image in folder:
                        imageURI = URIRef(image.replace('\\', '/').replace(' ', '_'))
                        g.add((otherMaterialURI, VIVO.contains, imageURI))
                        g.add((imageURI, RDF.type, VIVO.Image))

                    # extracting videos and including absolute path (URIs) in graph
                    extractVideos(reader, courseName, lectureNum)
                    folder = glob.glob(
                        os.path.join(courseNamePath, 'OtherMaterial', 'Videos', Path(filepath).stem, '*'))
                    for video in folder:
                        videoURI = URIRef(video.replace('\\', '/').replace(' ', '_'))
                        g.add((otherMaterialURI, VIVO.contains, videoURI))
                        g.add((videoURI, RDF.type, VIVO.Video))

                lectures_pathname = os.path.join(courseNamePath, courseName + '.ttl')
                g.serialize(lectures_pathname, format='turtle')
