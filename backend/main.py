# main.py
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from analysis.analyzer import analyze_singing_ai
import tempfile
import os

app = FastAPI()

# Allow frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # adjust for prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze_audio(file: UploadFile = File(...), reference: str = Form(None)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(await file.read())
        file_path = tmp.name

    reference_notes = reference.split(",") if reference else None
    results = analyze_singing_ai(file_path, reference_notes)

    os.remove(file_path)  # Clean up

    return results
