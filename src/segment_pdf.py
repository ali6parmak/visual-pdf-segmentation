import argparse
from typing import AnyStr

from PdfImages import PdfImages
from configuration import service_logger
from data_model.SegmentBox import SegmentBox
from create_word_grid import create_word_grid, remove_word_grids
from get_json_annotations import get_annotations
from predict import predict, predict_doclaynet, pdf_content_to_pdf_path
from get_most_probable_pdf_segments import get_most_probable_pdf_segments


def get_segmentation(model_name: str, pdf_paths: list[str]):
    service_logger.info(f'Creating PDF images')
    pdf_images_list: list[PdfImages] = [PdfImages.from_pdf_path(pdf_path) for pdf_path in pdf_paths]
    create_word_grid([pdf_images.pdf_features for pdf_images in pdf_images_list])
    get_annotations(pdf_images_list)
    predict(model_name)

    predicted_segments = get_most_probable_pdf_segments(model_name, pdf_images_list, False)
    return [SegmentBox.from_pdf_segment(pdf_segment).to_dict() for pdf_segment in predicted_segments]


def remove_files():
    PdfImages.remove_images()
    remove_word_grids()


def get_segmentation_doclaynet(file: AnyStr):
    pdf_path = pdf_content_to_pdf_path(file)
    service_logger.info(f'Creating PDF images')
    pdf_images_list: list[PdfImages] = [PdfImages.from_pdf_path(pdf_path)]
    create_word_grid([pdf_images.pdf_features for pdf_images in pdf_images_list])
    get_annotations(pdf_images_list)
    predict_doclaynet()
    remove_files()
    predicted_segments = get_most_probable_pdf_segments("doclaynet", pdf_images_list, False)
    return [SegmentBox.from_pdf_segment(pdf_segment).to_dict() for pdf_segment in predicted_segments]


def get_args():
    parser = argparse.ArgumentParser(description="Process PDF segmentation")
    parser.add_argument("pdf_paths", nargs="+", help="List of PDF file paths")
    parser.add_argument("--model_name", default="doclaynet", choices=["D4LA", "doclaynet", "publaynet", "docbank"], help="Model name (default: doclaynet).")
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = get_args()
    get_segmentation(model_name=args.model_name, pdf_paths=args.pdf_paths)
