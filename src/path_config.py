from os.path import join
from pathlib import Path

PROJECT_ROOT_PATH = Path(__file__).parent.parent
MODELS_PATH = Path(join(PROJECT_ROOT_PATH, "models"))
WORD_GRIDS_PATH = Path(join(PROJECT_ROOT_PATH, "word_grids"))
IMAGES_ROOT_PATH = Path(join(PROJECT_ROOT_PATH, "images"))
JSONS_ROOT_PATH = Path(join(PROJECT_ROOT_PATH, "jsons"))
JSON_TEST_FILE_PATH = Path(join(JSONS_ROOT_PATH, "test.json"))