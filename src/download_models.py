import shutil
from os import makedirs, rename, listdir
from os.path import join, exists
from urllib.request import urlretrieve
from huggingface_hub import snapshot_download
from config import MODELS_PATH


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
    print("Embedding model is being downloaded")
    revision = "95bd33f5b96be185feae70a6a7b8953051deb699"
    snapshot_download(repo_id="microsoft/layoutlm-base-uncased", revision=revision, cache_dir=MODELS_PATH)

    shutil.rmtree(join(MODELS_PATH, ".locks"))
    rename(join(MODELS_PATH, "models--microsoft--layoutlm-base-uncased"), model_path)

    revision_path = join(model_path, "snapshots", revision)
    for file in listdir(revision_path):
        shutil.move(join(revision_path, file), join(model_path, file))

    shutil.rmtree(join(model_path, "blobs"))
    shutil.rmtree(join(model_path, "snapshots"))


def download_models():
    makedirs(MODELS_PATH, exist_ok=True)
    download_vgt_model()
    download_embedding_model()
