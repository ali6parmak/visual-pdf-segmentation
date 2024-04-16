import json
import pickle
from os.path import join
from pathlib import Path
from paragraph_extraction_trainer.PdfSegment import PdfSegment
from pdf_features.PdfFeatures import PdfFeatures
from pdf_features.PdfToken import PdfToken
from pdf_features.Rectangle import Rectangle
from src.Prediction import Prediction
from src.path_config import PROJECT_ROOT_PATH

PREDICTION_SEGMENTS_PICKLE_PATH = join(PROJECT_ROOT_PATH, "model_output", "predicted_segments.pickle")


def get_prediction_from_annotation(annotation, images_names, vgt_predictions_dict):
    pdf_name = images_names[annotation["image_id"]][:-4]
    category_id = annotation["category_id"]
    bounding_box = Rectangle.from_width_height(left=int(annotation["bbox"][0]), top=int(annotation["bbox"][1]),
                                               width=int(annotation["bbox"][2]), height=int(annotation["bbox"][3]))
    prediction = Prediction(
        bounding_box=bounding_box,
        category_id=category_id,
        score=round(float(annotation['score']) * 100, 2)
    )
    vgt_predictions_dict.setdefault(pdf_name, list()).append(prediction)


def get_vgt_predictions() -> dict[str, list[Prediction]]:
    model_output_json_path = join(str(PROJECT_ROOT_PATH), "model_output", "inference", "coco_instances_results.json")
    annotations = json.loads(Path(model_output_json_path).read_text())

    test_json_path = join(str(PROJECT_ROOT_PATH), "jsons", "test.json")
    coco_truth = json.loads(Path(test_json_path).read_text())

    images_names = {value["id"]: value["file_name"] for value in coco_truth["images"]}

    vgt_predictions_dict = dict()
    for annotation in annotations:
        get_prediction_from_annotation(annotation, images_names, vgt_predictions_dict)

    return vgt_predictions_dict


def find_best_prediction_for_token(page_pdf_name, token, vgt_predictions_dict, most_probable_tokens_by_predictions):
    best_score: float = 0
    most_probable_prediction: Prediction | None = None
    for prediction in vgt_predictions_dict[page_pdf_name]:
        if prediction.score > best_score and prediction.bounding_box.get_intersection_percentage(
                token.bounding_box):
            best_score = prediction.score
            most_probable_prediction = prediction
            if best_score >= 99:
                break
    if most_probable_prediction:
        most_probable_tokens_by_predictions.setdefault(most_probable_prediction, list()).append(token)
    else:
        dummy_prediction = Prediction(bounding_box=token.bounding_box, category_id=11, score=0.0)
        most_probable_tokens_by_predictions.setdefault(dummy_prediction, list()).append(token)


def get_pdf_segments_for_page(page, pdf_name, page_pdf_name, vgt_predictions_dict):
    most_probable_pdf_segments_for_page: list[PdfSegment] = []
    most_probable_tokens_by_predictions: dict[Prediction, list[PdfToken]] = {}
    for token in page.tokens:
        find_best_prediction_for_token(page_pdf_name, token, vgt_predictions_dict, most_probable_tokens_by_predictions)

    for prediction, tokens in most_probable_tokens_by_predictions.items():
        new_segment = PdfSegment.from_pdf_tokens(tokens, pdf_name)
        new_segment.segment_type = prediction.category_id
        most_probable_pdf_segments_for_page.append(new_segment)

    return most_probable_pdf_segments_for_page


def get_most_probable_pdf_segments(pdf_features: PdfFeatures):
    most_probable_pdf_segments: list[PdfSegment] = []
    vgt_predictions_dict = get_vgt_predictions()
    for page in pdf_features.pages:
        page_pdf_name = pdf_features.file_name + "_" + str(page.page_number-1)
        page_segments = get_pdf_segments_for_page(page, pdf_features.file_name, page_pdf_name, vgt_predictions_dict)
        most_probable_pdf_segments.extend(page_segments)

    with open(PREDICTION_SEGMENTS_PICKLE_PATH, mode="wb") as file:
        pickle.dump(most_probable_pdf_segments, file)
