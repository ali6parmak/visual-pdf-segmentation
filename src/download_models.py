from os import makedirs
from os.path import join, exists
from urllib.request import urlretrieve
from huggingface_hub import snapshot_download
from path_config import MODELS_PATH


def download_vgt_model():
    model_path = join(MODELS_PATH, "D4LA_VGT_model.pth")
    if exists(model_path):
        return
    print("VGT model is being downloaded")
    download_link = "https://github.com/AlibabaResearch/AdvancedLiterateMachinery/releases/download/v1.3.0-VGT-release/D4LA_VGT_model.pth"
    urlretrieve(download_link, model_path)


def download_embedding_model():
    model_path = join(MODELS_PATH, "layoutlm-base-uncased")
    if exists(model_path):
        return
    makedirs(model_path, exist_ok=True)
    print("Embedding model is being downloaded")
    snapshot_download(repo_id="microsoft/layoutlm-base-uncased", local_dir=model_path, local_dir_use_symlinks=False)


def download_models():
    makedirs(MODELS_PATH, exist_ok=True)
    download_vgt_model()
    download_embedding_model()
