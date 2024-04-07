import json
from os import makedirs
from os.path import join
from pathlib import Path
from PIL import Image
from paragraph_extraction_trainer.PdfSegment import PdfSegment
from paragraph_extraction_trainer.load_labeled_data import load_labeled_data
from PdfImages import PdfImages
from configuration import PDF_LABELED_DATA_ROOT_PATH, REVERSED_CATEGORIES, CATEGORIES
from path_config import PROJECT_ROOT_PATH


def get_one_annotation(index, image_id, segment: PdfSegment):
    return {'segmentation': [],
            'area': 1,
            'iscrowd': 0,
            'score': 1,
            'image_id': image_id,
            'bbox': [segment.bounding_box.left, segment.bounding_box.top, segment.bounding_box.width,
                     segment.bounding_box.height],
            'category_id': REVERSED_CATEGORIES[segment.segment_type],
            'id': index}


def get_annotations(pdf_images: PdfImages):
    makedirs(join(PROJECT_ROOT_PATH, "jsons"), exist_ok=True)
    pdfs_paragraphs_tokens = load_labeled_data(PDF_LABELED_DATA_ROOT_PATH, "test")

    annotations = list()
    images = list()
    height_width = list()

    index = 0
    for pdf_paragraphs_tokens in pdfs_paragraphs_tokens:
        if pdf_paragraphs_tokens.pdf_features.file_name != pdf_images.pdf_features.file_name:
            continue
        for paragraph in pdf_paragraphs_tokens.paragraphs:
            if not paragraph.tokens:
                continue
            image_id = f'{pdf_paragraphs_tokens.pdf_features.file_name}_{paragraph.tokens[0].page_number - 1}'

            if image_id not in images:
                images.append(image_id)
                im = Image.open(join(PROJECT_ROOT_PATH, "images", f'{image_id}.jpg'))
                width, height = im.size
                height_width.append((width, height))

            annotations.append(
                get_one_annotation(index, images.index(image_id), PdfSegment.from_pdf_tokens(paragraph.tokens)))

            index += 1

    images_dict = [{"id": i,
                    "file_name": x + '.jpg', 'width': height_width[images.index(x)][0],
                    'height': height_width[images.index(x)][1]
                    } for i, x in enumerate(images)]

    categories_dict = [{"id": value, "name": key} for key, value in CATEGORIES.items()]
    coco_dict = {"images": images_dict,
                 "categories": categories_dict,
                 "annotations": annotations}

    Path(join(PROJECT_ROOT_PATH, "jsons", "test.json")).write_text(json.dumps(coco_dict))


if __name__ == '__main__':
    get_annotations()
