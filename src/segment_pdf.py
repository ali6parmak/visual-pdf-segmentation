import sys
from PdfImages import PdfImages
from download_models import download_models


def get_segmentation(pdf_path: str):
    download_models()
    pdf_images: PdfImages = PdfImages.from_pdf_path(pdf_path)
    pdf_images.show_images(2)


if __name__ == '__main__':
    get_segmentation(sys.argv[1] if len(sys.argv) >= 2 else None)
