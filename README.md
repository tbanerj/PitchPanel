# PitchPanel

PitchPanel is a full-stack vocal analysis web application that gives singers automated feedback on pitch accuracy, breath support, diction, and overall vocal performance.

Users can upload or record an audio sample, optionally provide reference notes, and receive numerical scores, written feedback, and visual analysis plots.

## Live Application

- Website: https://getpitchpanel.org
- Temporary Vercel URL: https://pitch-panel-2uwn.vercel.app
- API documentation: available at `/docs` on the deployed backend

> The custom domain may not work until its DNS configuration is completed.

## Overview

Traditional vocal coaching can be expensive, difficult to access, and limited to occasional lessons. PitchPanel is designed as an accessible practice tool that gives singers immediate feedback between coaching sessions.

PitchPanel is an educational prototype and is not intended to replace feedback from a qualified vocal instructor.

## Features

- Upload an existing audio recording
- Record singing directly in the browser
- Convert supported audio formats using FFmpeg
- Enter optional reference notes such as `C4,D4,E4`
- Analyze vocal pitch and pitch stability
- Evaluate breath-energy consistency
- Estimate diction clarity using spectral audio features
- Generate scores from 0–10
- Display pitch and breath-analysis plots
- Return personalized written feedback
- Health-check and interactive API documentation

## Technology Stack

### Frontend

- Next.js 15
- React 19
- TypeScript
- Tailwind CSS
- Axios
- Vercel

### Backend

- Python 3.11
- FastAPI
- Uvicorn
- Librosa
- NumPy
- SciPy
- Matplotlib
- Scikit-learn
- OpenCV
- FFmpeg
- Docker
- Google Cloud Run

## Deployment Architecture

```text
User
  |
  v
Next.js frontend
Hosted on Vercel
  |
  | HTTPS multipart request
  v
FastAPI backend
Hosted on Google Cloud Run
  |
  v
FFmpeg + Librosa + SciPy analysis
```

The frontend and backend are deployed separately:

- Vercel hosts the Next.js application in `frontend/`
- Google Cloud Run hosts the containerized FastAPI application in `backend/`
- `NEXT_PUBLIC_API_URL` tells the frontend where to reach the backend
- `ALLOWED_ORIGINS` controls which frontend domains may access the API

## Project Structure

```text
PitchPanel/
├── backend/
│   ├── analysis/
│   │   └── analyzer.py          # Core vocal-analysis logic
│   ├── main.py                  # FastAPI application and API routes
│   ├── requirements.txt         # Python dependencies
│   └── Dockerfile               # Cloud Run container configuration
│
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   └── product/
│   │   │       └── page.tsx     # Vocal analyzer interface
│   │   └── components/
│   ├── lib/
│   │   └── api.ts               # Backend API client
│   ├── public/
│   └── package.json
│
├── newfrontend/                 # Earlier Svelte prototype
└── README.md
```

## Running Locally

### Requirements

Install the following first:

- Node.js 20 or later
- Python 3.11
- FFmpeg
- Git

### 1. Clone the repository

```bash
git clone https://github.com/tbanerj/PitchPanel.git
cd PitchPanel
```

### 2. Run the backend

```bash
cd backend

python3 -m venv .venv
source .venv/bin/activate
```

On Windows:

```powershell
.venv\Scripts\activate
```

Install the Python dependencies:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Start FastAPI:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at:

```text
http://localhost:8000
```

Interactive API documentation:

```text
http://localhost:8000/docs
```

Health check:

```text
http://localhost:8000/health
```

### 3. Run the frontend

Open a second terminal:

```bash
cd frontend
npm install
```

Create `frontend/.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Start the development server:

```bash
npm run dev
```

Open:

```text
http://localhost:3000
```

## Running the Backend with Docker

Build the container from the repository root:

```bash
docker build -t pitchpanel-api ./backend
```

Run it locally:

```bash
docker run --rm \
  -p 8000:8080 \
  -e PORT=8080 \
  -e ENVIRONMENT=development \
  -e ALLOWED_ORIGINS=http://localhost:3000 \
  pitchpanel-api
```

## Environment Variables

### Frontend

| Variable | Description | Example |
|---|---|---|
| `NEXT_PUBLIC_API_URL` | Public URL of the FastAPI backend | `http://localhost:8000` |

### Backend

| Variable | Description | Example |
|---|---|---|
| `ENVIRONMENT` | Current application environment | `production` |
| `ALLOWED_ORIGINS` | Comma-separated frontend origins allowed by CORS | `https://getpitchpanel.org` |
| `PORT` | Port used by the deployed container | `8080` |

Example production CORS value:

```env
ALLOWED_ORIGINS=https://getpitchpanel.org,https://www.getpitchpanel.org,https://pitch-panel-2uwn.vercel.app
```

## API Endpoints

### Health check

```http
GET /health
```

Example response:

```json
{
  "status": "healthy",
  "environment": "production"
}
```

### Analyze audio

```http
POST /analyze
```

The endpoint accepts `multipart/form-data` containing:

| Field | Required | Description |
|---|---:|---|
| `audio_file` | Yes | Singing recording |
| `reference` | No | Comma-separated reference notes |
| `sheet_music` | No | Experimental sheet-music image input |

## How the Analysis Works

### Pitch

Pitch is estimated from the recording's fundamental-frequency contour. Pitch stability, vibrato characteristics, and optional reference-note alignment contribute to the pitch score.

### Breath support

Breath feedback is estimated using RMS energy patterns, energy consistency, and low-energy dropouts across the performance.

### Diction

Diction clarity is estimated using spectral audio characteristics. This is an experimental approximation and is not equivalent to a linguistic or professional vocal assessment.

### Overall score

Individual analysis values are combined into an overall score from 0–10 using the project's scoring model.

## Current Limitations

- Scores are generated by an experimental model and have not been professionally validated
- Results can vary depending on microphone quality and background noise
- Reference notes do not currently represent full musical rhythm or timing
- Diction analysis uses indirect acoustic features
- Sheet-music processing remains experimental
- Cloud Run may take additional time to respond after a period of inactivity

## Planned Improvements

- Train the scoring model using human-rated vocal samples
- Improve phoneme- and formant-based diction analysis
- Add accounts and progress history
- Add recording comparisons over time
- Improve sheet-music and MusicXML support
- Add multilingual vocal feedback
- Improve mobile recording support
- Add automated tests and deployment checks

## Contributors

PitchPanel was developed collaboratively by:

- Trinav Banerjee
- Project contributors listed in the GitHub repository

## License

This project is licensed under the MIT License.

PitchPanel is intended for educational and personal practice purposes.
