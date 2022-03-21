import os

import fitz
import io
from PIL import Image
from pathlib import Path

from __init__ import ROOT_DIR
import warnings

warnings.filterwarnings("ignore")


def extractImages(filepath, courseName):
    print('\nextracting images\n')
    pdf_file = fitz.open(filepath)

    with fitz.open(filepath) as pdf_file:
        for page_index in range(len(pdf_file)):

            page = pdf_file[page_index]

            for image_index, img in enumerate(page.getImageList(), start=1):
                # get image XREF
                xref = img[0]

                # extract image bytes
                base_image = pdf_file.extract_image(xref)
                image_bytes = base_image["image"]

                # get image extension
                image_ext = base_image["ext"]

                # load image to PIL
                image = Image.open(io.BytesIO(image_bytes))

                lectureName = Path(filepath).stem
                images0XDir = os.path.join(ROOT_DIR, 'Data', 'Lectures', courseName, 'OtherMaterial', 'Images', lectureName)

                # create nested folder if not exists
                Path(images0XDir).mkdir(parents=True, exist_ok=True)

                # export image
                path = os.path.join(images0XDir, f'page{page_index + 1}_image{image_index}.{image_ext}')
                image.save(open(path, "wb"))
