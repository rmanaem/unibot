import rdflib
import re
from pathlib import Path
from urllib.parse import urlparse
import pandas as pd
import requests
import simplejson
import spacy
from spacypdfreader import pdf_reader
from tika import parser


def insertToList(index, element, arr):
    newArr = arr[:]
    newArr.insert(index, element)
    return newArr


def sepWord(word):
    """
    separate a string at upper cases, i.e.: AlphaBetaABC -> Alpha Beta ABC
    :param word: string
    :return: string
    """
    return re.sub(r"((?<=[a-z])[A-Z]|[A-Z](?=[a-z]))", r" \1", word)


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


def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)


def locatePage(readerObj, string):
    pages = []
    for i in range(readerObj.getNumPages()):
        content = readerObj.getPage(i).extractText() + "\n"
        ResSearch = re.search(string, content)
        if ResSearch is not None:
            pages.append(i)
    return pages


def getYtURLs(readerObj):
    URLs = []
    for i in range(readerObj.getNumPages()):
        text = readerObj.getPage(i).extractText().split()
        for word in text:
            if 'youtube' in word and is_url(word):
                URLs.append(word)
    return URLs


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


def getCourseId(csvFile, courseName):
    """
    extracts courseID from a dataset given a courseName.
    n.b.: a better practice is to extract the courseID from the generated rdf graph instead of the original csvFile
    :param csvFile: csv
    :return: int
    """
    df = pd.read_csv(csvFile, delimiter=',',
                     encoding='unicode_escape', dtype={'Course ID': object})
    nameArr = re.split(r'(\d+)', courseName)[:2]
    return df.loc[(df['Subject'] == nameArr[0]) & (df['Catalog'] == nameArr[1])]['Course ID'].values[0]


def pdf_to_text_tika(path):
    text = parser.from_file(path)
    with open(path[:-3] + 'txt', 'w', encoding='utf-8') as f:
        f.write(text['content'])


def pdf_to_text_spacy(path):
    nlp = spacy.load("en_core_web_sm")
    doc = pdf_reader(path, nlp)
    text = ''
    for i in doc._.page_range:
        text += doc._.page(i).text
    with open(path[:-3] + 'text', 'w', encoding='utf-8') as f:
        f.write(text)


def extract_ne(path):
    nlp = spacy.load("en_core_web_sm")
    pos_tags = [
        "PERSON", "NORP", "FACILITY", "FAC", "ORG",
        "GPE", "LOC", "PRODUCT", "EVENT", "WORK_OF_ART",
        "LAW", "LANGUAGE", "DATE", "TIME", "PERCENT", "MONEY",
        "QUANTITY", "MISC", "EVT", "PROD", "DRV", "GPE_LOC",
        "GPE_ORG"
    ]

    text = ''
    with open(path, 'r') as f:
        text = f.read()

    print('Running spacy nlp for', Path(path))
    doc = nlp(text)
    named_entities = []
    for i in [(e.text, e.label_) for e in doc.ents]:
        if i[1] in pos_tags:
            named_entities.append(i[0])

    return set(named_entities)


def DBLookup(txt):
    """
    send text to spotlight and return dbpedia URI and dbpedia's label
    :param txt: string
    :return: URI and dbr rdfs:label
    """
    spot_light_url = "https://api.dbpedia-spotlight.org/en/annotate?text=%s" % txt
    headers = {
        'accept': 'application/json'
    }

    try:
        request = requests.get(url=spot_light_url, headers=headers)
        data = request.json()
        resources = data.get('Resources')

        if resources is None:
            return None, 'None'
        URI = resources[0]['@URI']

        g = rdflib.Graph()
        g.parse(URI)
        output = g.query(
            """
            SELECT ?label
            WHERE {
            ?uni rdfs:label ?label .
            FILTER(LANG(?label) = 'en') .
            }
            """
        )

        try:
            label = str(list(output)[0][0])
        except Exception:
            return None, 'None'

        return URI, label

    except simplejson.errors.JSONDecodeError:
        print(None)
        return None


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
                name = sepWord(name).split()
                return ' '.join(name)

        if choice == 'topics':
            topics = []
            for index in range(readerObj.getNumPages()):
                page = readerObj.getPage(index)
                text = page.extractText().split('\n')
                text = removeTableContents(text)

                if len(text) == 0:
                    continue

                # every encountered word is considered a topic (used in phase 1)
                for word in text:
                    if word != '' and word != 'Ł':
                        # remove special characters
                        newWord = re.sub('[^A-Za-z0-9]+', ' ', word)
                        # separate word at capital letters
                        newWord = sepWord(newWord)
                        if len(newWord) > 2:
                            topics.append(newWord)

            return list(set(topics))

        if choice == 'readings':
            # get reference page contents. Merge content if there exists >1 reference pages
            references = []
            for index in locatePage(readerObj, 'References'):
                page = readerObj.getPage(index)
                text = page.extractText().split('\n')

                # remove table of contents on the right side on each page
                references += removeTableContents(text)

            for index in range(readerObj.getNumPages()):
                page = readerObj.getPage(index)
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

                    # # separate a string at upper cases
                    # for index, element in enumerate(pure_text):
                    #     if not is_url(element):
                    #         pure_text[index] = sepWord(element).lstrip()

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
                                    lst[index - 2] = lst[index - 2] + \
                                        lst[index - 1]
                                    lst.remove(lst[index - 1])
                                    index = 0
                                    continue
                            # good case (either first element is string or second element is url)
                            index += 1

                    return required, supplemental
