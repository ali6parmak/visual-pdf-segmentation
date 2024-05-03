import shutil

import cv2
import numpy as np
from os import makedirs
from os.path import join
from pathlib import Path
from PIL import Image
from pdf2image import convert_from_path
from pdf_features.PdfFeatures import PdfFeatures
from path_config import IMAGES_ROOT_PATH


class PdfImages:
    def __init__(self, pdf_features: PdfFeatures, pdf_images: list[Image]):
        self.pdf_features: PdfFeatures = pdf_features
        self.pdf_images: list[Image] = pdf_images
        self.save_images()

    def show_images(self, next_image_delay: int = 2):
        for image_index, image in enumerate(self.pdf_images):
            image_np = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            cv2.imshow(f'Page: {image_index + 1}', image_np)
            cv2.waitKey(next_image_delay * 1000)
            cv2.destroyAllWindows()

    def save_images(self):
        makedirs(IMAGES_ROOT_PATH, exist_ok=True)
        for image_index, image in enumerate(self.pdf_images):
            image_name = f'{self.pdf_features.file_name}_{image_index}.jpg'
            image.save(join(IMAGES_ROOT_PATH, image_name))

    @staticmethod
    def remove_images():
        shutil.rmtree(IMAGES_ROOT_PATH)

    @staticmethod
    def from_pdf_path(pdf_path: str):
        pdf_features: PdfFeatures = PdfFeatures.from_pdf_path(pdf_path)
        pdf_features.file_name = Path(pdf_path).parent.name
        pdf_images = convert_from_path(pdf_path, dpi=72)
        return PdfImages(pdf_features, pdf_images)
