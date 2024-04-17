import json
import pickle
from os.path import join, exists
from pathlib import Path
from time import time
from typing import Optional

from paragraph_extraction_trainer.PdfParagraphTokens import PdfParagraphTokens
from paragraph_extraction_trainer.PdfSegment import PdfSegment
from paragraph_extraction_trainer.load_labeled_data import load_labeled_data
from pdf_features.PdfFeatures import PdfFeatures
from pdf_features.PdfToken import PdfToken
from pdf_features.Rectangle import Rectangle
from pdf_token_type_labels.Label import Label
from pdf_token_type_labels.TokenType import TokenType
from tqdm import tqdm
from configuration import PDF_LABELED_DATA_ROOT_PATH, D4LA_TYPES_TO_TOKEN_TYPES
from path_config import PROJECT_ROOT_PATH, JSON_TEST_FILE_PATH

TRUTH_SEGMENTS_PICKLE_PATH = join(PROJECT_ROOT_PATH, "models", "truth_segments.pickle")
PREDICTION_SEGMENTS_PICKLE_PATH = join(PROJECT_ROOT_PATH, "models", "prediction_segments.pickle")

SCORE_PER_CATEGORY_PICKLE_PATH = join(PROJECT_ROOT_PATH, "models", "score_per_category.pickle")
COUNT_PER_CATEGORY_PICKLE_PATH = join(PROJECT_ROOT_PATH, "models", "count_per_category.pickle")


def load_predictions_per_pdf() -> (dict[str, list[PdfSegment]], dict[str, list[PdfSegment]]):
    truth_segments_per_pdf = dict()
    prediction_segments_per_pdf = dict()

    with open(TRUTH_SEGMENTS_PICKLE_PATH, "rb") as f:
        truth_segments: list[PdfSegment] = pickle.load(f)

    with open(PREDICTION_SEGMENTS_PICKLE_PATH, "rb") as f:
        prediction_segments: list[PdfSegment] = pickle.load(f)

    for truth_segment in truth_segments:
        truth_segments_per_pdf.setdefault(truth_segment.pdf_name, []).append(truth_segment)

    for prediction_segment in prediction_segments:
        prediction_segments_per_pdf.setdefault(prediction_segment.pdf_name, []).append(prediction_segment)

    return truth_segments_per_pdf, prediction_segments_per_pdf


def get_prediction_from_truth(
        truth_segment: PdfSegment, predictions_segments: list[PdfSegment]
) -> (Optional[PdfSegment], int):
    max_intersection_pdf_segment = None
    max_intersection_percentage = 0

    for prediction_segment in predictions_segments:
        if prediction_segment.page_number != truth_segment.page_number:
            continue

        intersection_percentage = truth_segment.bounding_box.get_intersection_percentage(prediction_segment.bounding_box)

        if intersection_percentage > max_intersection_percentage:
            max_intersection_pdf_segment = prediction_segment
            max_intersection_percentage = intersection_percentage

    return max_intersection_pdf_segment, int(max_intersection_percentage)


def get_pdf_name_labels(scale: float = 1) -> dict[str, list[Label]]:
    # json_path = join(PROJECT_ROOT_PATH, "model_output", "inference", "coco_instances_results.json")
    json_path = join(PROJECT_ROOT_PATH, "model_output", "inference", "coco_instances_results.json")
    annotations = json.loads(Path(json_path).read_text())

    json_path = JSON_TEST_FILE_PATH
    coco_truth = json.loads(Path(json_path).read_text())

    images_names = {value["id"]: value["file_name"] for value in coco_truth["images"]}

    pdf_name_labels = dict()
    for annotation in annotations:
        pdf_name = images_names[annotation["image_id"]][:-4]
        category_id = D4LA_TYPES_TO_TOKEN_TYPES[annotation["category_id"]]

        label = Label(
            left=int(annotation["bbox"][0] * scale),
            top=int(annotation["bbox"][1] * scale),
            width=int(annotation["bbox"][2] * scale),
            height=int(annotation["bbox"][3] * scale),
            label_type=category_id.get_index(),
            metadata=str(round(float(annotation['score']) * 100))
        )

        pdf_name_labels.setdefault(pdf_name, list()).append(label)

    return pdf_name_labels

def get_vgt_predictions(file_name: str):
    pdf_name_labels: dict[str, list[Label]] = get_pdf_name_labels()
    pdfs_paragraphs_tokens: list[PdfParagraphTokens] = load_labeled_data(PDF_LABELED_DATA_ROOT_PATH, "test")
    test_pdf_features: list[PdfFeatures] = [x.pdf_features for x in pdfs_paragraphs_tokens if x.pdf_features.file_name == file_name]
    label_segments = get_segments_from_labels(pdf_name_labels, test_pdf_features)

    label_list_token = get_most_probable(test_pdf_features, label_segments)

    most_probable_pdf_segments: list[PdfSegment] = list()
    for label, tokens_list in label_list_token.items():
        prediction_pdf_segment = PdfSegment.from_pdf_tokens(tokens_list, label.pdf_name)
        prediction_pdf_segment.text_content = label.text_content
        prediction_pdf_segment.segment_type = label.segment_type
        most_probable_pdf_segments.append(prediction_pdf_segment)

    with open(PREDICTION_SEGMENTS_PICKLE_PATH, mode="wb") as file:
        pickle.dump(most_probable_pdf_segments, file)


def get_segments_from_labels(pdf_name_labels, test_pdf_features):
    label_segments: list[PdfSegment] = list()
    for pdf_features in test_pdf_features:
        file_name = pdf_features.file_name
        for page in pdf_features.pages:
            labels = pdf_name_labels[f"{file_name}_{page.page_number-1}"]
            for label in labels:
                label_segments.append(
                    PdfSegment(page_number=page.page_number,
                               bounding_box=get_rectangle_from_label(label),
                               text_content=label.metadata,
                               segment_type=TokenType.from_index(label.label_type),
                               pdf_name=pdf_features.file_name))

    print("sorting")
    label_segments = sorted(label_segments, key=lambda x: float(x.text_content), reverse=True)
    print("sorted")
    return label_segments


def get_most_probable(pdfs_features: list[PdfFeatures], labels_pdfs_segments: list[PdfSegment]):
    label_list_token: dict[PdfSegment, list[PdfToken]] = dict()
    for pdf_features in tqdm(pdfs_features):
        for page in pdf_features.pages:
            page_labels_pdf_segment = [x for x in labels_pdfs_segments if x.pdf_name == pdf_features.file_name and x.page_number == page.page_number]
            for token_page, token in pdf_features.loop_tokens():
                if token_page.page_number != page.page_number:
                    continue

                best_score: float = 0
                best_label: PdfSegment | None = None
                for label in page_labels_pdf_segment:
                    if float(label.text_content) > best_score and label.bounding_box.get_intersection_percentage(token.bounding_box):
                        best_score = float(label.text_content)
                        best_label = label
                        if best_score >= 99:
                            break

                if best_label:
                    label_list_token.setdefault(best_label, list()).append(token)
                else:
                    token.content = "0"
                    token.token_type = TokenType.HEADER
                    label_list_token[PdfSegment.from_pdf_tokens([token], pdf_features.file_name)] = [token]

    return label_list_token


def get_rectangle_from_label(label):
    label_rectangle = Rectangle.from_width_height(label.left, label.top, label.width, label.height)
    return label_rectangle


def save_scores(file_name: str):
    score_per_category = {x: 0 for x in TokenType}
    count_per_category = {x: 0 for x in TokenType}

    error_segmentation = {x: 0 for x in TokenType}
    error_token_type = {x: 0 for x in TokenType}

    truth_segments_per_pdf, prediction_segments_per_pdf = load_predictions_per_pdf()

    for pdf_name, truth_segments in tqdm(truth_segments_per_pdf.items()):
        if pdf_name != file_name:
            continue
        predictions_segments = prediction_segments_per_pdf[pdf_name]
        for truth_segment in truth_segments:
            prediction_segment, intersection_percentage = get_prediction_from_truth(truth_segment, predictions_segments)

            if intersection_percentage == 100 and truth_segment.segment_type == prediction_segment.segment_type:
                score_per_category[truth_segment.segment_type] += 1

            if intersection_percentage == 100 and truth_segment.segment_type != prediction_segment.segment_type:
                error_token_type[truth_segment.segment_type] += 1

            if intersection_percentage != 100:
                error_segmentation[truth_segment.segment_type] += 1

            count_per_category[truth_segment.segment_type] += 1

    print("error_segmentation")
    print({x.value: v for x, v in error_segmentation.items() if v != 0})
    print("error_token_type")
    print({x.value: v for x, v in error_token_type.items() if v != 0})
    with open(SCORE_PER_CATEGORY_PICKLE_PATH, mode="wb") as file:
        pickle.dump(score_per_category, file)

    with open(COUNT_PER_CATEGORY_PICKLE_PATH, mode="wb") as file:
        pickle.dump(count_per_category, file)


def print_scores():
    with open(SCORE_PER_CATEGORY_PICKLE_PATH, "rb") as f:
        score_per_category: dict[TokenType, int] = pickle.load(f)

    with open(COUNT_PER_CATEGORY_PICKLE_PATH, "rb") as f:
        count_per_category: dict[TokenType, int] = pickle.load(f)

    accuracies = list()
    for token_type in TokenType:
        if count_per_category[token_type]:
            accuracy = round(100 * score_per_category[token_type] / count_per_category[token_type], 2)
            accuracies.append(accuracy)
            print(token_type.value, f"{accuracy}%")

    print("Average", f"{round(sum(accuracies) / len(accuracies), 2)}%")


def get_truth_segments():
    pdfs_paragraphs_tokens = load_labeled_data(PDF_LABELED_DATA_ROOT_PATH, "test")

    truth_segments: list[PdfSegment] = [
        PdfSegment.from_pdf_tokens(paragraph.tokens, paragraph_token.pdf_features.file_name)
        for paragraph_token in pdfs_paragraphs_tokens
        for paragraph in paragraph_token.paragraphs
    ]

    with open(TRUTH_SEGMENTS_PICKLE_PATH, mode="wb") as file:
        pickle.dump(truth_segments, file)


def get_performance(file_name: str):
    if not exists(TRUTH_SEGMENTS_PICKLE_PATH):
        get_truth_segments()
    start = time()
    print("start")
    get_vgt_predictions(file_name)
    save_scores(file_name)
    print_scores()
    print("finished in", round(time() - start, 1), "seconds")


if __name__ == "__main__":
    get_performance()
