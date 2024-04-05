import cv2
import numpy as np
from PIL import Image
from pdf2image import convert_from_path
from pdf_features.PdfFeatures import PdfFeatures


class PdfImages:
    def __init__(self, pdf_features: PdfFeatures, pdf_images: list[Image]):
        self.pdf_features: PdfFeatures = pdf_features
        self.pdf_images: list[Image] = pdf_images

    def show_images(self, next_image_delay: int = 2):
        for image_index, image in enumerate(self.pdf_images):
            image_np = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            cv2.imshow(f'Page: {image_index+1}', image_np)
            cv2.waitKey(next_image_delay * 1000)
            cv2.destroyAllWindows()

    @staticmethod
    def from_pdf_path(pdf_path: str):
        pdf_features: PdfFeatures = PdfFeatures.from_pdf_path(pdf_path)
        pdf_images = convert_from_path(pdf_path, dpi=72)
        return PdfImages(pdf_features, pdf_images)
