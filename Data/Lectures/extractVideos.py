import os
from pathlib import Path
from pytube import YouTube

from Data.Lectures.pdfOperations import getYtURLs
from __init__ import ROOT_DIR


def extractVideos(readerObj):
    URLs = getYtURLs(readerObj)
    SAVE_PATH = os.path.join(ROOT_DIR, 'Data', 'Lectures', 'OtherMaterial', 'Videos')
    Path(SAVE_PATH).mkdir(parents=True, exist_ok=True)

    for url in URLs:
        try:
            yt = YouTube(url)
            yt.streams.first().download(SAVE_PATH)
            print('\nextracting videos\n')

        except (Exception,):
            print("Can't download video from youtube")
            continue
