from os.path import join
from pathlib import Path

PROJECT_ROOT_PATH = Path(__file__).parent.parent
MODELS_PATH = join(PROJECT_ROOT_PATH, "models")
WORD_GRIDS_PATH = join(PROJECT_ROOT_PATH, "word_grids")
