from PIL import Image
from pdf2image import convert_from_path
from pdf_features.PdfFeatures import PdfFeatures


class PdfImages:
    def __init__(self, pdf_features: PdfFeatures, pdf_images: list[Image]):
        self.pdf_features: PdfFeatures = pdf_features
        self.pdf_images: list[Image] = pdf_images

    @staticmethod
    def from_pdf_path(pdf_path: str):
        pdf_features: PdfFeatures = PdfFeatures.from_pdf_path(pdf_path)
        pdf_images = convert_from_path(pdf_path, dpi=72)
        return PdfImages(pdf_features, pdf_images)
