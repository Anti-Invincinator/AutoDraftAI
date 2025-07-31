# app/services/inference.py

from ultralytics import YOLO
import os
import uuid

# Load the model once globally
model = YOLO("app/models/yolov8/soda_best.pt") 

def run_inference(image_path: str, output_dir: str = "dxf_outputs") -> tuple:
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Run inference
    results = model(image_path)

    # Save annotated image
    annotated_path = os.path.join(output_dir, f"{uuid.uuid4()}_annotated.jpg")
    results[0].save(filename=annotated_path)

    # Extract predictions
    predictions = []
    for box in results[0].boxes:
        cls_id = int(box.cls.item())
        label = model.names[cls_id]
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        predictions.append({
            "label": label,
            "bbox": [x1, y1, x2, y2]
        })

    return predictions, annotated_path
