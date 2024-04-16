import sys
from PdfImages import PdfImages
from download_models import download_models
from create_word_grid import create_word_grid
from get_json_annotations import get_annotations
from predict import predict
from src.get_most_probable_pdf_segments import get_most_probable_pdf_segments
from src.save_output_to_pdf import save_output_to_pdf


def get_segmentation(pdf_path: str):
    download_models()
    pdf_images: PdfImages = PdfImages.from_pdf_path(pdf_path)
    create_word_grid(pdf_images.pdf_features)
    get_annotations(pdf_images)
    predict()
    get_most_probable_pdf_segments(pdf_images.pdf_features)
    save_output_to_pdf(pdf_path, pdf_images)


if __name__ == '__main__':
    get_segmentation(sys.argv[1] if len(sys.argv) >= 2 else None)
