# app/routes/predict.py

from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
import os
import uuid
import hashlib

from app.services.inference import run_inference
from app.services.cad_generator import generate_dxf_from_boxes

router = APIRouter()

@router.post("/")
async def predict(image: UploadFile = File(...)):
    # Generate file hash to avoid storing duplicates
    content = await image.read()
    image_hash = hashlib.md5(content).hexdigest()
    ext = os.path.splitext(image.filename)[-1]
    filename = f"{image_hash}{ext}"
    save_path = os.path.join("data", "sample_images", filename)

    # Only save if not already present
    if not os.path.exists(save_path):
        with open(save_path, "wb") as buffer:
            buffer.write(content)

    # Run YOLOv8 inference
    boxes, annotated_path = run_inference(save_path)

    dxf_path = generate_dxf_from_boxes(boxes)

    return {
        "predictions": boxes,
        "annotated_image": annotated_path,
        "dxf_file": dxf_path
    }

