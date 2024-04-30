from os import makedirs
from os.path import join
from pdf_annotate import PdfAnnotator, Location, Appearance
from PdfImages import PdfImages
from configuration import CATEGORY_BY_ID, COLOR_BY_CATEGORY, DOCLAYNET_TYPE_BY_ID, DOCLAYNET_COLOR_BY_TYPE, PUBLAYNET_COLOR_BY_TYPE, PUBLAYNET_TYPE_BY_ID, DOCBANK_COLOR_BY_TYPE, DOCBANK_TYPE_BY_ID
from path_config import PROJECT_ROOT_PATH


def hex_color_to_rgb(color: str):
    r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
    alpha = 1
    return r/255, g/255, b/255, alpha


def add_prediction_annotation(annotator, predicted_segment, page_height, category_by_id, color_by_category):
    bbox = predicted_segment.bounding_box
    predicted_type = category_by_id[predicted_segment.segment_type]
    color = color_by_category[predicted_type]
    left, top, right, bottom = bbox.left, page_height-bbox.top, bbox.left + bbox.width, page_height-(bbox.top+bbox.height)
    annotator.add_annotation('square',
                             Location(x1=left, y1=bottom, x2=right, y2=top, page=predicted_segment.page_number-1),
                             Appearance(stroke_color=hex_color_to_rgb(color))
                             )

    annotator.add_annotation('text',
                             Location(x1=left, y1=bottom, x2=left + 100,y2=top+bbox.height, page=predicted_segment.page_number-1),
                             Appearance(content=predicted_type, font_size=10, fill=hex_color_to_rgb(color))
                             )


def get_colors_and_categories(model_name: str):
    if model_name == "doclaynet":
        return DOCLAYNET_TYPE_BY_ID, DOCLAYNET_COLOR_BY_TYPE
    if model_name == "publaynet":
        return PUBLAYNET_TYPE_BY_ID, PUBLAYNET_COLOR_BY_TYPE
    if model_name == "docbank":
        return DOCBANK_TYPE_BY_ID, DOCBANK_COLOR_BY_TYPE
    return CATEGORY_BY_ID, COLOR_BY_CATEGORY


def save_output(model_name: str, annotator, pdf_images):
    output_pdf_path = join(PROJECT_ROOT_PATH, f"pdf_outputs_{model_name}", pdf_images.pdf_features.file_name + ".pdf")
    annotator.write(output_pdf_path)


def save_output_to_pdf(model_name: str, pdf_paths: list[str], pdf_images_list: list[PdfImages], predicted_segments):
    pdf_outputs_path = join(PROJECT_ROOT_PATH, f"pdf_outputs_{model_name}")
    makedirs(pdf_outputs_path, exist_ok=True)
    category_by_id, color_by_category = get_colors_and_categories(model_name)
    for pdf_path, pdf_images in zip(pdf_paths, pdf_images_list):
        annotator = PdfAnnotator(pdf_path)
        predicted_segments_for_pdf = [segment for segment in predicted_segments if segment.pdf_name == pdf_images.pdf_features.file_name]
        for predicted_segment in predicted_segments_for_pdf:
            page_height = pdf_images.pdf_features.pages[predicted_segment.page_number-1].page_height
            add_prediction_annotation(annotator, predicted_segment, page_height, category_by_id, color_by_category)
        save_output(model_name, annotator, pdf_images)
