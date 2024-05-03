
import sys
import tempfile
import uuid
from os.path import join
from pathlib import Path

import torch
from fastapi import FastAPI, HTTPException, UploadFile, File

from configuration import service_logger
from src.segment_pdf import get_segmentation

app = FastAPI()

service_logger.info(f'Is PyTorch using GPU: {torch.cuda.is_available()}')


def get_file_path(file_name, extension):
    return join(tempfile.gettempdir(), file_name + "." + extension)


def pdf_content_to_pdf_path(file_content):
    file_id = str(uuid.uuid1())

    pdf_path = Path(get_file_path(file_id, "pdf"))
    pdf_path.write_bytes(file_content)

    return pdf_path


@app.get("/")
async def info():
    return sys.version


@app.post("/get_paragraphs")
async def get_paragraphs(file: UploadFile = File(...)):
    try:
        service_logger.info(f"Processing file: {file.filename}")
        pdf_path = pdf_content_to_pdf_path(file.file.read())
        return get_segmentation(model_name="doclaynet", pdf_paths=[str(pdf_path)])
    except Exception:
        service_logger.error("Error", exc_info=1)
        raise HTTPException(status_code=422, detail="Error extracting paragraphs")