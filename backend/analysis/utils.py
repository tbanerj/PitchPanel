# Add this to your analysis code (or a new utils.py file)
import sys
from pathlib import Path

def extract_notes_from_sheetmusic(sheet_image_path):
    """
    Uses SheetVision to extract notes from sheet music image
    Returns: list of note names (e.g., ["C4", "D4", "E4"]) and their durations
    """
    sheetvision_path = Path(__file__).parent / "SheetVision" / "main.py"
    
    try:
        # Run SheetVision as a subprocess
        result = subprocess.run(
            [sys.executable, str(sheetvision_path), sheet_image_path],
            capture_output=True,
            text=True
        )
        
        # Parse SheetVision's output
        notes = []
        for line in result.stdout.split('\n'):
            if "note" in line.lower():  # Example line: "C4 4,8" (note + duration)
                parts = line.strip().split()
                if len(parts) >= 2:
                    notes.append({
                        "pitch": parts[0],  # Note name
                        "duration": parts[1]  # Duration code
                    })
        return notes
    
    except Exception as e:
        print(f"Sheet music analysis failed: {e}")
        return None