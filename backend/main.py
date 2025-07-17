import os
import subprocess
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from analysis.analyzer import analyze_singing_ai
from typing import Optional
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Singing Analysis API",
    description="API for analyzing vocal performances",
    version="1.0.0"
)

# ====================== CORS Configuration ======================
# Environment-based CORS settings (adjust for production)
IS_DEVELOPMENT = os.getenv("ENVIRONMENT", "development") == "development"

ALLOWED_ORIGINS = [
    "http://localhost:443",  # Next.js default dev port
    "https://localhost:443",
    "http://127.0.0.1:443",
    "https://127.0.0.1:443",
    "https://pitchpanel.org",
    "http://192.168.0.111:3000", #Trinav computer
    "https://www.pitchpanel.org",
    "https://pitchpanel.org:8000",
    "http://pitchpanel.org:8000"

]



app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,  # Changed to True if using cookies/sessions
    allow_methods=["*"],  # You had only POST/OPTIONS - expand to all needed methods
    allow_headers=["*"],
    expose_headers=["*"]  # Changed from just Content-Disposition
)

# ====================== Constants & Helpers ======================
UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

def save_upload_file(upload_file: UploadFile, destination: str) -> None:
    """Save uploaded file with size validation and error handling"""
    try:
        # Check file size
        upload_file.file.seek(0, os.SEEK_END)
        file_size = upload_file.file.tell()
        upload_file.file.seek(0)
        
        if file_size > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail=f"File too large. Max size is {MAX_FILE_SIZE/1024/1024}MB"
            )

        with open(destination, "wb") as buffer:
            content = upload_file.file.read()
            buffer.write(content)
        logger.info(f"Saved file to {destination}")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error saving file {upload_file.filename}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Could not save file: {str(e)}"
        )

def convert_to_wav(input_path: str) -> str:
    """Convert audio file to standardized WAV format"""
    base, ext = os.path.splitext(input_path)
    wav_path = base + ".wav"

    if ext.lower() != ".wav":
        try:
            result = subprocess.run([
                "ffmpeg", "-y", "-i", input_path, 
                "-ar", "22050", "-ac", "1", "-sample_fmt", "s16",
                wav_path
            ], check=True, capture_output=True, text=True)
            
            logger.info(f"Converted {input_path} to WAV format")
            logger.debug(f"FFmpeg output: {result.stdout}")
            return wav_path
        except subprocess.CalledProcessError as e:
            logger.error(f"FFmpeg conversion failed: {e.stderr}")
            raise HTTPException(
                status_code=422,
                detail=f"Audio conversion failed: {e.stderr}"
            )
    return input_path

# ====================== API Endpoints ======================
@app.post("/analyze")
async def analyze_audio(
    audio_file: UploadFile = File(..., description="Audio file (WAV, MP3, etc.)"),
    sheet_music: Optional[UploadFile] = File(None, description="Optional sheet music (PNG, JPG)"),
    reference: Optional[str] = Form(None, description="Optional reference notes (comma-separated)")
):
    audio_path = None
    sheet_path = None
    
    try:
        # Validate audio file
        if not audio_file.filename:
            raise HTTPException(
                status_code=422,
                detail="Audio file must have a filename"
            )
            
        # Save and process audio
        audio_path = os.path.join(UPLOAD_DIR, audio_file.filename)
        save_upload_file(audio_file, audio_path)
        audio_path = convert_to_wav(audio_path)
        
        # Process sheet music if provided
        if sheet_music:
            if not sheet_music.filename:
                raise HTTPException(
                    status_code=422,
                    detail="Sheet music file must have a filename"
                )
                
            if not any(sheet_music.filename.lower().endswith(ext) 
                      for ext in ['.png', '.jpg', '.jpeg']):
                raise HTTPException(
                    status_code=422,
                    detail="Sheet music must be PNG or JPG"
                )
                
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
                raise HTTPException(
                    status_code=422,
                    detail=f"Invalid reference notes format: {str(e)}"
                )
        
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
        raise HTTPException(
            status_code=500,
            detail="Internal server error during analysis"
        )
    finally:
        # Cleanup files
        for path in [audio_path, sheet_path]:
            if path and os.path.exists(path):
                try:
                    os.remove(path)
                    logger.info(f"Cleaned up temporary file: {path}")
                except Exception as e:
                    logger.warning(f"Could not remove {path}: {str(e)}")

# ====================== Health Check ======================
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "environment": os.getenv("ENVIRONMENT", "development")
    }


@app.options("/analyze")
async def analyze_options():
    return {"message": "OK"}