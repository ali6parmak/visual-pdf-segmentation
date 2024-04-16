import json
from os import makedirs
from os.path import join
from pathlib import Path
from PIL import Image
from pdf_features.PdfToken import PdfToken
from PdfImages import PdfImages
from configuration import REVERSED_CATEGORIES, CATEGORIES
from path_config import PROJECT_ROOT_PATH


def save_annotations_json(annotations: list, height_width: list, images: list):
    images_dict = [{"id": i,
                    "file_name": x + '.jpg', 'width': height_width[images.index(x)][0],
                    'height': height_width[images.index(x)][1]
                    } for i, x in enumerate(images)]

    categories_dict = [{"id": value, "name": key} for key, value in CATEGORIES.items()]

    coco_dict = {"images": images_dict,
                 "categories": categories_dict,
                 "annotations": annotations}

    Path(join(PROJECT_ROOT_PATH, "jsons", "test.json")).write_text(json.dumps(coco_dict))


def get_annotation(index: int, image_id: str, token: PdfToken):
    return {'area': 1,
            'iscrowd': 0,
            'score': 1,
            'image_id': image_id,
            'bbox': [token.bounding_box.left, token.bounding_box.top, token.bounding_box.width,
                     token.bounding_box.height],
            'category_id': REVERSED_CATEGORIES[token.token_type],
            'id': index}


def get_annotations(pdf_images: PdfImages):
    makedirs(join(PROJECT_ROOT_PATH, "jsons"), exist_ok=True)

    annotations = list()
    images = list()
    height_width = list()
    index = 0

    for page in pdf_images.pdf_features.pages:
        image_id = f'{pdf_images.pdf_features.file_name}_{page.page_number - 1}'
        images.append(image_id)
        im = Image.open(join(PROJECT_ROOT_PATH, "images", f'{image_id}.jpg'))
        width, height = im.size
        height_width.append((width, height))

        for token in page.tokens:
            annotations.append(get_annotation(index, image_id, token))
            index += 1

    save_annotations_json(annotations, height_width, images)
