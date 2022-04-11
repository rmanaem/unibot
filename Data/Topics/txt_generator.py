from pathlib import Path
import os
from __init__ import ROOT_DIR
from Utils.utils import extract_ne, pdf_to_text_tika, pdf_to_text_spacy


if __name__ == '__main__':

    comp474_lecturesPath = os.path.join(
        ROOT_DIR, 'Data', 'Lectures', 'COMP474')
    comp6721_lecturePath = os.path.join(
        ROOT_DIR, 'Data', 'Lectures', 'COMP6721')
    topicsPath = os.path.join(ROOT_DIR, 'Data', 'Topics')
    for idx, path in enumerate([comp474_lecturesPath, comp6721_lecturePath]):
        for lectureNum in range(1, 8):
            for source in [('slides', 'Slides'), ('worksheet', 'Worksheets'), ('lab', 'Labs'),
                           ('Outline', 'CourseInfo')]:
                if source[0] == 'Outline':
                    if lectureNum == 1:
                        filePath = os.path.join(
                            path, source[1], source[0] + '.pdf')
                    else:
                        continue
                else:
                    filePath = os.path.join(
                        path, source[1], source[0] + "%02d" % lectureNum + '.pdf')

                pdf_to_text_tika(filePath)
