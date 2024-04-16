import json
from os import makedirs
from os.path import join
from pathlib import Path
from pdf_annotate import PdfAnnotator, Location, Appearance
from src.PdfImages import PdfImages
from src.configuration import D4LA_TYPES_TO_TOKEN_TYPES, COLOR_BY_TOKEN_TYPE
from src.path_config import PROJECT_ROOT_PATH


def hex_color_to_rgb(color: str):
    r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
    alpha = 1
    return r/255, g/255, b/255, alpha


def add_prediction_annotation(annotator: PdfAnnotator, annotation: dict, page_height: int):
    bbox = annotation['bbox']
    predicted_type = D4LA_TYPES_TO_TOKEN_TYPES[annotation['category_id']].name
    color = COLOR_BY_TOKEN_TYPE[D4LA_TYPES_TO_TOKEN_TYPES[annotation['category_id']]]
    left, top, right, bottom = bbox[0], page_height-bbox[1], bbox[0] + bbox[2], page_height-(bbox[1]+bbox[3])
    annotator.add_annotation('square',
                             Location(x1=left, y1=bottom, x2=right, y2=top, page=annotation['image_id']),
                             Appearance(stroke_color=hex_color_to_rgb(color))
                             )

    annotator.add_annotation('text',
                             Location(x1=left, y1=bottom, x2=left + 100,y2=top+bbox[3], page=annotation['image_id']),
                             Appearance(content=predicted_type, font_size=10, fill=hex_color_to_rgb(color))
                             )


def save_output_to_pdf(pdf_path: str, pdf_images: PdfImages):
    annotator = PdfAnnotator(pdf_path)
    annotations_path: str = join(str(PROJECT_ROOT_PATH), "model_output", "inference", "coco_instances_results.json")
    annotations = json.loads(Path(annotations_path).read_text())
    for annotation in annotations:
        if annotation["score"] < 0.5:
            continue
        add_prediction_annotation(annotator, annotation, pdf_images.pdf_images[annotation["image_id"]].height)
    pdf_outputs_path = join(PROJECT_ROOT_PATH, "pdf_outputs")
    makedirs(pdf_outputs_path, exist_ok=True)
    output_pdf_path = join(PROJECT_ROOT_PATH, "pdf_outputs", pdf_images.pdf_features.file_name + ".pdf")
    annotator.write(output_pdf_path)
