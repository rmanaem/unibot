import os
from pathlib import Path
from pytube import YouTube

from Data.Courses.pdfOperations import getYtURLs
from __init__ import ROOT_DIR


def extractVideos(readerObj, course_name, lecture_num):
    URLs = getYtURLs(readerObj)
    SAVE_PATH = os.path.join(ROOT_DIR, 'Data', 'Courses', course_name, 'Lectures', 'OtherMaterial', 'Videos',
                             "slides%02d" % lecture_num)
    Path(SAVE_PATH).mkdir(parents=True, exist_ok=True)

    for url in URLs:
        try:
            yt = YouTube(url)
            yt.streams.first().download(SAVE_PATH)
            print('\nextracting videos\n')

        except (Exception,):
            print("Can't download video from youtube")
            continue
