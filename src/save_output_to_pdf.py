import pickle
from os import makedirs
from os.path import join
from paragraph_extraction_trainer.PdfSegment import PdfSegment
from pdf_annotate import PdfAnnotator, Location, Appearance
from PdfImages import PdfImages
from configuration import CATEGORY_BY_ID, COLOR_BY_CATEGORY
from path_config import PROJECT_ROOT_PATH


def hex_color_to_rgb(color: str):
    r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
    alpha = 1
    return r/255, g/255, b/255, alpha


def add_prediction_annotation(annotator: PdfAnnotator, predicted_segment: PdfSegment, page_height: int):
    bbox = predicted_segment.bounding_box
    predicted_type = CATEGORY_BY_ID[predicted_segment.segment_type]
    color = COLOR_BY_CATEGORY[predicted_type]
    left, top, right, bottom = bbox.left, page_height-bbox.top, bbox.left + bbox.width, page_height-(bbox.top+bbox.height)
    annotator.add_annotation('square',
                             Location(x1=left, y1=bottom, x2=right, y2=top, page=predicted_segment.page_number-1),
                             Appearance(stroke_color=hex_color_to_rgb(color))
                             )

    annotator.add_annotation('text',
                             Location(x1=left, y1=bottom, x2=left + 100,y2=top+bbox.height, page=predicted_segment.page_number-1),
                             Appearance(content=predicted_type, font_size=10, fill=hex_color_to_rgb(color))
                             )


def get_predicted_segments() -> list[PdfSegment]:
    predicted_segments_path = join(str(PROJECT_ROOT_PATH), "model_output", "predicted_segments.pickle")
    with open(predicted_segments_path, "rb") as f:
        return pickle.load(f)


def save_output_to_pdf(pdf_path: str, pdf_images: PdfImages):
    annotator = PdfAnnotator(pdf_path)
    predicted_segments: list[PdfSegment] = get_predicted_segments()
    for predicted_segment in predicted_segments:
        page_height = pdf_images.pdf_features.pages[predicted_segment.page_number-1].page_height
        add_prediction_annotation(annotator, predicted_segment, page_height)
    pdf_outputs_path = join(PROJECT_ROOT_PATH, "pdf_outputs")
    makedirs(pdf_outputs_path, exist_ok=True)
    output_pdf_path = join(PROJECT_ROOT_PATH, "pdf_outputs", pdf_images.pdf_features.file_name + ".pdf")
    annotator.write(output_pdf_path)
