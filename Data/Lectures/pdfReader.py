from SPARQLWrapper import SPARQLWrapper, CSV, JSON, XML, N3, RDFXML, TURTLE
from rdflib import Graph, Literal, RDF, Namespace, URIRef, BNode
from rdflib.namespace import FOAF, RDFS, XSD, OWL
from PyPDF2 import PdfFileReader
from __init__ import ROOT_DIR
import os
import re
from urllib.parse import urlparse
import pandas as pd


def locatePage(readerObj, string):
    pages = []
    for i in range(readerObj.getNumPages()):
        content = readerObj.getPage(i).extractText() + "\n"
        ResSearch = re.search(string, content)
        if ResSearch is not None:
            pages.append(i)
    return pages


def insertToList(index, element, arr):
    newArr = arr[:]
    newArr.insert(index, element)
    return newArr


def is_float(element) -> bool:
    try:
        float(element)
        return True
    except ValueError:
        return False


def is_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def removeTableContents(arr):
    # remove table of contents on the right side on each page
    flag = False
    new_arr = []
    for word in arr:
        if is_float(word):
            flag = True
        if flag is True:
            new_arr.append(word)

    if len(new_arr) >= 2:
        if new_arr[1] == 'Outline':
            return []
    return new_arr


def extractFromPdf(readerObj, choice):
    page = readerObj.getPage(0)
    text = page.extractText()
    text_arr = text.split()

    for index, word in enumerate(text_arr):
        if choice == 'num':
            if re.search('^Lecture', word):
                return int(word[-1])

        if choice == 'name':
            if re.search('^Lecture', word):
                name = text_arr[index + 1]
                # Split a string at uppercase letters
                name = re.sub(r"((?<=[a-z])[A-Z]|[A-Z](?=[a-z]))", r" \1", name).split()
                return ' '.join(name)

        if choice == 'readings':

            # get reference page contents. Merge content if there exists >1 reference pages
            references = []
            for index in locatePage(readerObj, 'References'):
                page = reader.getPage(index)
                text = page.extractText().split('\n')

                # remove table of contents on the right side on each page
                references += removeTableContents(text)

            for index in range(readerObj.getNumPages()):
                page = reader.getPage(index)
                text = page.extractText().split('\n')

                # remove table of contents on the right side on each page
                pure_text = removeTableContents(text)

                # only look at the readingMaterial page
                if "ReadingMaterial" in pure_text:
                    required = []
                    supplemental = []

                    # remove redundant strings
                    for element in pure_text:
                        if is_float(element) or 'Ł' in element or element == '':
                            pure_text.remove(element)

                    # split "string,URL" into a string and a URL if possible
                    arr = []
                    for element in pure_text:
                        if ',' in element:
                            if '[' in element and ']' in element and '(' in element and ')' in element:
                                arr.append(element)
                            else:
                                split = element.split(',')
                                arr.append(split[0])
                                if split[1] != '':
                                    arr.append(split[1])
                        else:
                            arr.append(element)
                    pure_text = arr.copy()

                    # # split a string at upper cases
                    # for index, element in enumerate(pure_text):
                    #     if not is_url(element):
                    #         pure_text[index] = re.sub(r"((?<=[a-z])[A-Z]|[A-Z](?=[a-z]))", r" \1", element).lstrip()

                    flag = None
                    for element in pure_text:
                        if 'required' == element.lower():
                            flag = 'required'
                            continue
                        elif 'supplemental' == element.lower():
                            flag = 'supplemental'
                            continue

                        if flag == 'required':
                            required.append(element)
                        elif flag == 'supplemental':
                            supplemental.append(element)

                    for lst in [required, supplemental]:
                        for idx, element in enumerate(lst):
                            if not is_url(element):

                                # if adjacent element at (index + 1) is a URL, don't lookup references
                                if idx < len(lst) - 1:
                                    if is_url(lst[idx + 1]):
                                        continue

                                # get first word (is always the referenced word, i.e.: 'Yu14')
                                word = re.sub(r'\W+', ' ', element).split()[0]

                                # find the url reference to the above word in the references page and append the url
                                # into the "required" (or "supplemental") list
                                matchingURL = False
                                flag = False
                                for reference in references:
                                    if word in reference:
                                        flag = True

                                    if flag is True and is_url(reference):
                                        if matchingURL is False:
                                            url = reference

                                            # remove a full stop from urls, if exists
                                            if reference[-1] == '.':
                                                url = reference[:-1]

                                            # remove all text after comma, if exists
                                            url = url.split(',')[0]

                                            lst.insert(idx + 1, url)
                                            matchingURL = True

                    # merge two adjacent splits of a URL
                    for lst in [required, supplemental]:
                        flag = True
                        index = 0
                        while flag:
                            if index == len(lst) - 1:
                                flag = False
                            if index % 2 == 1:
                                # bad case (second element is string)
                                if not is_url(lst[index]):
                                    lst[index - 2] = lst[index - 2] + lst[index - 1]
                                    lst.remove(lst[index - 1])
                                    index = 0
                                    continue
                            # good case (either first element is string or second element is url)
                            index += 1

                    return required, supplemental


if __name__ == '__main__':

    g = Graph()
    g.parse('../schema.ttl')
    g.parse('http://vivoweb.org/ontology/core', format='xml')

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

    currDir = os.path.join(ROOT_DIR, 'Data', 'Lectures', 'Slides')
    slidesCount = len(os.listdir(currDir))
    filepaths = [os.path.join(currDir, 'slides') + "%02d" % num + '.pdf' for num in range(1, slidesCount + 1)]

    for filepath in filepaths:
        with open(filepath, mode='rb') as f:
            reader = PdfFileReader(f)
            lectureNum = extractFromPdf(reader, 'num')
            lectureName = extractFromPdf(reader, 'name')
            required, supplemental = extractFromPdf(reader, 'readings')

            print(lectureNum, lectureName)
            print('required', required)
            print('supplemental', supplemental, '\n\n')

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

                readingURI = URIRef(FOCUDATA + 'Reading' + str("%02d" % lectureNum))
                g.add((readingURI, VIVO.contains, BNode()))

                g.add((BNode(), RDFS.subClassOf, FOCUDATA.required))
                g.add((BNode(), VCARD.URL, URIRef(reading)))
                g.add((BNode(), VIVO.Title, Literal(lastReading)))

    g.add(((URIRef(FOCUDATA + 'Lecture01')), RDFS.seeAlso,
           URIRef('https://www.coursehero.com/file/58197534/slides01pdf/')))
