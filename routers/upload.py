from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil
import os
from typing import List

router = APIRouter(prefix="/upload")

UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/single")
def upload_file(file: UploadFile = File(...)):
    file_ext = file.filename.split(".")[-1] in ("jpg", "jpeg", "png", "pdf")
    if not file_ext:
        raise HTTPException(status_code=400, detail="Invalid file type")

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"filename": file.filename, "path": file_path}
