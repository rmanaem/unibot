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

        g.bind("rdfs", RDFS)
        g.bind("rdf", RDF)
        g.bind("xsd", XSD)
        g.bind("foaf", FOAF)
        g.bind("focu", FOCU)
        g.bind("focudata", FOCUDATA)
        g.bind('vivo', VIVO)
        g.bind('vcard', VCARD)

        print(courseName, '\n\n')
        courseNamePath = os.path.join(lecturesParentDir, courseName)

        slidesDir = os.path.join(courseNamePath, 'Slides')
        slidesCount = len(os.listdir(slidesDir))
        filepaths = [os.path.join(slidesDir, 'slides') + "%02d" % num + '.pdf' for num in range(1, slidesCount + 1)]

        for index, filepath in enumerate(filepaths):
            with open(filepath, mode='rb') as f:
                reader = PdfFileReader(f)
                lectureNum = index + 1 if courseName == 'COMP6721' else extractFromPdf(reader, 'num')
                lectureName = 'Lecture' if courseName == 'COMP6721' else extractFromPdf(reader, 'name')
                courseID = str(getCourseId(course_catalog, courseName))

                print(lectureNum, lectureName)

                required, supplemental = [], []
                if courseName != 'COMP6721':
                    required, supplemental = extractFromPdf(reader, 'readings')
                    print('Required readings', required)
                    print('Supplemental readings', supplemental, '\n\n')

                lectureURI = URIRef(FOCUDATA + courseID + '_Lecture' + str("%02d" % lectureNum))
                g.add((lectureURI, RDF.type, URIRef(FOCU.lecture)))

                slideURI = URIRef('file///' + os.path.join(courseNamePath, 'Slides',
                                                           'slides' + "%02d" % lectureNum + '.pdf').replace('\\', '/'))
                g.add((lectureURI, VIVO.contains, slideURI))
                g.add((slideURI, RDF.type, FOCU.slide))
                g.add((slideURI, RDFS.subClassOf, lectureURI))

                worksheetURI = URIRef('file///' + os.path.join(courseNamePath, 'Worksheets',
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

                    readingsURI = URIRef(FOCUDATA + courseID + '_Readings' + str("%02d" % lectureNum))
                    readingURI = URIRef(FOCUDATA + courseID + '_Reading' + str("%02d" % lectureNum))

                    g.add((readingsURI, RDFS.subClassOf, lectureURI))
                    g.add((readingsURI, VIVO.contains, readingURI))
                    g.add((readingsURI, RDF.type, FOCU.readings))

                    g.add((readingURI, RDFS.subClassOf, FOCUDATA.required))
                    g.add((readingURI, VCARD.URL, URIRef(reading)))
                    g.add((readingURI, VIVO.Title, Literal(lastReading)))
                    g.add((readingURI, RDF.type, FOCU.reading))

                if courseName != 'COMP6721':
                    otherMaterialURI = URIRef(FOCUDATA + courseID + '_otherMaterial' + str("%02d" % lectureNum))
                    g.add((lectureURI, VIVO.contains, URIRef(FOCU.otherMaterial)))
                    g.add((otherMaterialURI, RDF.type, URIRef(FOCU.otherMaterial)))
                    g.add((otherMaterialURI, RDFS.subClassOf, lectureURI))

                    extractImages(filepath, courseName)
                    folder = glob.glob(
                        os.path.join(courseNamePath, 'OtherMaterial', 'Images', Path(filepath).stem, '*'))
                    for image in folder:
                        imageURI = URIRef(image.replace('\\', '/').replace(' ', '_'))
                        g.add((otherMaterialURI, VIVO.contains, imageURI))
                        g.add((imageURI, RDF.type, VIVO.Image))

                    extractVideos(reader, courseName, lectureNum)
                    folder = glob.glob(
                        os.path.join(courseNamePath, 'OtherMaterial', 'Videos', Path(filepath).stem, '*'))
                    for video in folder:
                        videoURI = URIRef(video.replace('\\', '/').replace(' ', '_'))
                        g.add((otherMaterialURI, VIVO.contains, videoURI))
                        g.add((videoURI, RDF.type, VIVO.Video))

                lectures_pathname = os.path.join(courseNamePath, courseName + '.ttl')
                g.serialize(lectures_pathname, format='turtle')
