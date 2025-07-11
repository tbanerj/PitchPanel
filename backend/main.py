import os
import subprocess
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from analysis.analyzer import analyze_singing_ai
from typing import Optional
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

def save_upload_file(upload_file: UploadFile, destination: str) -> None:
    """Save uploaded file to destination with error handling"""
    try:
        with open(destination, "wb") as buffer:
            content = upload_file.file.read()
            buffer.write(content)
        logger.info(f"Saved file to {destination}")
    except Exception as e:
        logger.error(f"Error saving file {upload_file.filename}: {str(e)}")
        raise

def convert_to_wav(input_path: str) -> str:
    """Convert audio file to WAV format with standardized parameters"""
    base, ext = os.path.splitext(input_path)
    wav_path = base + ".wav"

    if ext.lower() != ".wav":
        try:
            subprocess.run([
                "ffmpeg", "-y", "-i", input_path, 
                "-ar", "22050", "-ac", "1", "-sample_fmt", "s16",
                wav_path
            ], check=True, capture_output=True)
            logger.info(f"Converted {input_path} to WAV format")
            return wav_path
        except subprocess.CalledProcessError as e:
            logger.error(f"FFmpeg conversion failed: {e.stderr.decode()}")
            raise RuntimeError(f"Audio conversion failed: {e.stderr.decode()}")
    return input_path

@app.post("/analyze")
async def analyze(
    audio_file: UploadFile = File(..., description="Audio file (WAV, MP3, etc.)"),
    sheet_music: Optional[UploadFile] = File(None, description="Optional sheet music image (PNG, JPG)"),
    reference: Optional[str] = Form(None, description="Optional reference notes as comma-separated values")
):
    audio_path = None
    sheet_path = None
    
    try:
        # Validate audio file
        if not audio_file.filename:
            raise HTTPException(status_code=422, detail="Audio file must have a filename")
            
        # Save audio file
        audio_path = os.path.join(UPLOAD_DIR, audio_file.filename)
        save_upload_file(audio_file, audio_path)
        
        # Convert to WAV if needed
        audio_path = convert_to_wav(audio_path)
        
        # Process sheet music if provided
        if sheet_music:
            if not sheet_music.filename:
                raise HTTPException(status_code=422, detail="Sheet music file must have a filename")
                
            if not any(sheet_music.filename.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg']):
                raise HTTPException(status_code=422, detail="Sheet music must be PNG or JPG")
                
            sheet_path = os.path.join(UPLOAD_DIR, sheet_music.filename)
            save_upload_file(sheet_music, sheet_path)
        
        # Process reference notes
        ref_notes = None
        if reference:
            try:
                ref_notes = [note.strip() for note in reference.split(",") if note.strip()]
                if not ref_notes:
                    raise ValueError("No valid notes provided")
            except Exception as e:
                raise HTTPException(status_code=422, detail=f"Invalid reference notes format: {str(e)}")
        
        # Run analysis
        result = analyze_singing_ai(
            file_path=audio_path,
            reference_notes=ref_notes,
            sheet_image_path=sheet_path
        )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Cleanup files
        for path in [audio_path, sheet_path]:
            if path and os.path.exists(path):
                try:
                    os.remove(path)
                    logger.info(f"Cleaned up temporary file: {path}")
                except Exception as e:
                    logger.warning(f"Could not remove temporary file {path}: {str(e)}")