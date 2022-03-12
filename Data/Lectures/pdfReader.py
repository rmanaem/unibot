from PyPDF2 import PdfFileReader
from __init__ import ROOT_DIR
import os
import re


def extractFromPdf(readerObj, choice):
    page = readerObj.getPage(0)
    text = page.extractText()
    text_arr = text.split()
    for index, word in enumerate(text_arr):
        if choice == 'num':
            if re.search('^Lecture', word):
                return word[-1]
        if choice == 'name':
            if re.search('^Lecture', word):
                name = text_arr[index + 1]
                # Split a string at uppercase letters
                name = re.sub(r"([A-Z])", r" \1", name).split()
                return ' '.join(name)


if __name__ == '__main__':
    currDir = os.path.join(ROOT_DIR, 'Data', 'Lectures', 'Slides')
    slidesCount = len(os.listdir(currDir))
    filepaths = [os.path.join(currDir, 'slides') + "%02d" % num + '.pdf' for num in range(1, slidesCount + 1)]

    for filepath in filepaths:
        with open(filepath, mode='rb') as f:
            reader = PdfFileReader(f)
            lectureNum = extractFromPdf(reader, 'num')
            lectureName = extractFromPdf(reader, 'name')
            print(lectureNum, lectureName)
