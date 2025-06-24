# PitchPanel Vocal Analyzer

**PitchPanel** is a web-based vocal analysis tool designed for singers to receive immediate feedback on pitch accuracy, breath support, and diction quality based on audio recordings. It uses signal processing (via `librosa`) and a simple ML model to generate scores and personalized suggestions.

---

## 🔍 Problem Statement & Solution Overview

### Problem

Despite the benefits of vocal training, quality vocal coaching remains out of reach for many people due to several key barriers:

- **Lack of Accessibility**: Vocal lessons are often expensive and locked behind high paywalls.
- **Limited Feedback**: Students often only receive feedback once a week, leading to poor practice habits.
- **Geographic & Physical Barriers**: Individuals in rural areas or with disabilities may find it difficult to attend in-person lessons.
- **Beginners Face Uncertainty**: Many don’t know where to start or lack tools to guide early practice.
- **Language & Musical Literacy Barriers**: Assumes access to Western music notation and English instruction.

### Solution

**PitchPanel** is a digital vocal coaching assistant that provides:

- **Standalone feedback for beginners**, or
- **Supplemental feedback for students** between traditional lessons.

It combines real-time vocal analysis, ML-based scoring, and personalized feedback into a lightweight web app.

---

## 🚀 Features

- Upload `.wav` recordings of singing
- Optional reference notes (e.g. `C4,D4,E4`)
- Extracts pitch contour, energy envelope, and spectral centroid
- Scores pitch, breath, and diction from 0–10
- Predicts total score using an ML regression model
- Returns helpful text feedback and visual plots
- Built with:
  - **FastAPI** (Python backend)
  - **Next.js** (React frontend)
  - **Librosa** + **Matplotlib**
  - **Scikit-learn** for ML scoring

---

## 📁 Project Structure

```
backend/
├── main.py                  # FastAPI app
├── analysis/
│   └── voice_analyzer.py    # Core audio analysis logic
├── basic_score_model.joblib # Saved ML regression model
├── requirements.txt
frontend/
├── src/
│   ├── app/
│   │   ├── page.tsx         # Main UI
│   └── lib/api.ts           # Frontend API handler
├── public/
├── styles/Analyzer.css      # Custom CSS (if used)
```

---

## ⚙️ Setup Instructions

### 1. Backend (FastAPI)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn main:app --reload
```

API will be available at: `http://localhost:8000/docs`

### 2. Frontend (Next.js)

```bash
cd newfrontend
npm install
npm run dev
```

App will run at: `http://localhost:3000`

---

## 🧪 How to Use

1. Upload a `.wav` audio file of your singing
2. (Optional) Enter reference notes like `C4,D4,E4`
3. Click **Analyze**
4. View:
   - Pitch plot vs reference
   - RMS energy curve (breath)
   - Feedback messages
   - Total vocal score (0–10)

---

## 🧠 How Scoring Works

| Feature      | Method                           | Criteria                   |
|--------------|----------------------------------|----------------------------|
| **Pitch**    | Compare `f0` to reference notes  | Deviation < 30 Hz          |
| **Breath**   | RMS dropouts below threshold     | Few dropouts = better      |
| **Diction**  | Spectral centroid average        | Higher = clearer diction   |
| **Total**    | ML prediction (LinearRegression) | Based on all audio features |

---

## 📦 Dependencies

**Backend**:
- `fastapi`
- `uvicorn`
- `librosa`
- `numpy`
- `matplotlib`
- `scikit-learn`
- `joblib`

**Frontend**:
- `tailwindcss`
- `vite`
- `axios`
- `svelte`

[//]: # (- Optional: `tailwindcss` or plain CSS)

---

## 🌱 Future Improvements

- Train ML model with human-rated samples
- Use formant tracking for diction clarity
- Add user dashboard and progress tracking
- Integrate sheet music reading (MusicXML, PDF)
- Build multilingual support for global reach
- Implement AI-powered vocal advice generation

---

## 📜 License

MIT License. Built for educational and personal vocal feedback purposes.
