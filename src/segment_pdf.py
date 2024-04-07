import sys
from PdfImages import PdfImages
from download_models import download_models
from create_word_grid import create_word_grid
from get_json_annotations import get_annotations
from performance import get_performance
from predict import predict


def get_segmentation(pdf_path: str):
    download_models()
    pdf_images: PdfImages = PdfImages.from_pdf_path(pdf_path)
    create_word_grid(pdf_images.pdf_features)
    get_annotations(pdf_images)
    predict()
    get_performance(pdf_images.pdf_features.file_name)


if __name__ == '__main__':
    get_segmentation(sys.argv[1] if len(sys.argv) >= 2 else None)
    # get_segmentation(/home/ali/Desktop/pdf-labeled-data/pdfs/cejil8/document.pdf)
