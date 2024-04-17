import sys
from PdfImages import PdfImages
from download_models import download_models
from create_word_grid import create_word_grid
from get_json_annotations import get_annotations
from predict import predict
from get_most_probable_pdf_segments import get_most_probable_pdf_segments
from save_output_to_pdf import save_output_to_pdf


def get_segmentation(pdf_paths: list[str]):
    download_models()
    pdf_images_list: list[PdfImages] = [PdfImages.from_pdf_path(pdf_path) for pdf_path in pdf_paths]
    create_word_grid([pdf_images.pdf_features for pdf_images in pdf_images_list])
    get_annotations(pdf_images_list)
    predict()
    get_most_probable_pdf_segments([pdf_images.pdf_features for pdf_images in pdf_images_list])
    save_output_to_pdf(pdf_paths, pdf_images_list)


if __name__ == '__main__':
    get_segmentation(sys.argv[1:] if len(sys.argv) >= 2 else None)
