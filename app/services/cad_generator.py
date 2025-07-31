# app/services/cad_generator.py

import ezdxf
import uuid
import os

def generate_dxf_from_boxes(boxes: list, output_dir="dxf_outputs") -> str:
    doc = ezdxf.new()
    msp = doc.modelspace()

    for box in boxes:
        label = box["label"]
        x1, y1, x2, y2 = box["bbox"]

        # Draw rectangle
        msp.add_lwpolyline([
            (x1, y1), (x2, y1), (x2, y2), (x1, y2), (x1, y1)
        ], close=True)

        # Add label text
        msp.add_text(label, dxfattribs={
            "height": 10,
            "insert": (x1, y1)  # Fixed position
        })

    os.makedirs(output_dir, exist_ok=True)
    dxf_path = os.path.join(output_dir, f"{uuid.uuid4()}_output.dxf")
    doc.saveas(dxf_path)

    return dxf_path
