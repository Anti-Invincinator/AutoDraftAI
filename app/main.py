# app/main.py

from fastapi import FastAPI
from app.routes.predict import router as predict_router

app = FastAPI(
    title="AutoDraftAI",
    description="AI-powered system that extracts structures from images and generates DXF annotations.",
    version="0.1"
)

# Register prediction route
app.include_router(predict_router, prefix="/predict")
