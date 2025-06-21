import os
import subprocess
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from analysis.analyzer import analyze_singing_ai

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def convert_to_wav(uploaded_file: UploadFile, file_path: str) -> str:
    with open(file_path, "wb") as f:
        f.write(uploaded_file.file.read())

    base, ext = os.path.splitext(file_path)
    wav_path = base + ".wav"

    if ext.lower() != ".wav":
        subprocess.run([
            "ffmpeg", "-i", file_path, "-ar", "22050", "-ac", "1", wav_path
        ], check=True)
        return wav_path
    return file_path

@app.post("/analyze")
async def analyze(
    file: UploadFile = File(...),
    reference: str = Form(default=None)
):
    file_ext = os.path.splitext(file.filename)[1]
    raw_path = os.path.join(UPLOAD_DIR, file.filename)

    try:
        file_path = convert_to_wav(file, raw_path)
        ref_notes = reference.split(",") if reference else None
        result = analyze_singing_ai(file_path, reference_notes=ref_notes)
        return result
    except Exception as e:
        return {"error": str(e)}
