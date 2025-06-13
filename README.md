
# 🎤 VirtuOpera Vocal Analyzer

VirtuOpera is a web-based vocal analysis tool designed for singers to receive immediate feedback on pitch accuracy, breath support, and diction quality based on audio recordings. It uses signal processing (via `librosa`) and a simple ML model to generate scores and personalized suggestions.

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
cd frontend
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

| Feature   | Method                        | Criteria |
|-----------|-------------------------------|----------|
| **Pitch** | Compare `f0` to reference     | Deviation < 30 Hz |
| **Breath**| RMS dropouts below threshold  | Few dropouts = better |
| **Diction**| Spectral centroid average     | Higher = clearer diction |
| **Total Score** | ML prediction using LinearRegression |

---

## 📦 Dependencies

Backend:
- `fastapi`, `uvicorn`
- `librosa`, `numpy`, `matplotlib`
- `scikit-learn`, `joblib`

Frontend:
- `next`, `react`, `axios`
- Optional: `tailwindcss` or plain CSS

---

## 🧠 Future Improvements

- Train ML model with real human-rated examples
- Use formant tracking for better diction
- Add chart visualizations (radar/bar)
- Allow audio download and history saving

---

## 📜 License

MIT License. Built for educational and personal vocal feedback purposes.
