
import librosa
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
import os
import joblib
from sklearn.linear_model import LinearRegression

NOTE_FEEDBACK = {
    "pitch": [
        (0, 5, "Significant pitch issues. Try slow interval training and matching piano notes."),
        (5, 8, "Moderate drift. Practice with a tuner and sustained vowels."),
        (8, 11, "Excellent pitch control.")
    ],
    "breath": [
        (0, 5, "Work on long phrases and diaphragmatic support (lip trills, hissing)."),
        (5, 8, "Some inconsistency. Try longer sustained notes and breath timing."),
        (8, 11, "Solid breath support.")
    ],
    "diction": [
        (0, 5, "Practice vowel shaping and consonant exaggeration (e.g. tongue twisters)."),
        (5, 8, "Diction okay. Could improve final consonant clarity."),
        (8, 11, "Clear and bright diction.")
    ]
}

def get_feedback(score, category):
    for low, high, msg in NOTE_FEEDBACK[category]:
        if low <= score < high:
            return msg

def create_plot_image(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode("utf-8")
    plt.close(fig)
    return f"data:image/png;base64,{encoded}"

def train_simple_model():
    X = np.array([
        [9, 9, 9],
        [8, 7, 8],
        [6, 6, 7],
        [3, 4, 5],
        [5, 5, 5],
        [10, 10, 10],
        [7, 8, 6],
        [6, 9, 8]
    ])
    y = np.array([9.8, 8.3, 6.5, 4.5, 5.5, 10, 7.3, 7.9])
    model = LinearRegression()
    model.fit(X, y)
    joblib.dump(model, "basic_score_model.joblib")
    return model

def get_basic_model():
    try:
        return joblib.load("basic_score_model.joblib")
    except:
        return train_simple_model()

def score_analysis_metrics(deviation, rms, centroid):
    good_ratio = np.sum(deviation < 30) / np.sum(~np.isnan(deviation))
    if good_ratio > 0.9:
        pitch_score = 10
    elif good_ratio > 0.75:
        pitch_score = 8
    elif good_ratio > 0.5:
        pitch_score = 6
    else:
        pitch_score = 4

    energy_threshold = np.median(rms) * 0.5
    dropouts = np.sum(rms < energy_threshold)
    breath_score = 10 if dropouts <= 2 else 8 if dropouts <= 5 else 6 if dropouts <= 9 else 4

    avg_centroid = np.mean(centroid)
    diction_score = 10 if avg_centroid > 2500 else 8 if avg_centroid > 1800 else 6 if avg_centroid > 1200 else 4

    model = get_basic_model()
    total_score = round(min(model.predict([[pitch_score, breath_score, diction_score]])[0], 10), 1)

    return pitch_score, breath_score, diction_score, total_score

def analyze_singing_ai(file_path, reference_notes=None, sr=22050):
    y, sr = librosa.load(file_path, sr=sr)

    f0, _, _ = librosa.pyin(y, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'), sr=sr)
    times = librosa.times_like(f0)

    if reference_notes:
        ref_hz = [librosa.note_to_hz(note) for note in reference_notes]
        ref_interp = np.interp(times, np.linspace(0, times[-1], len(ref_hz)), ref_hz)
        deviation = np.abs(ref_interp - f0)
    else:
        ref_interp = None
        deviation = np.zeros_like(f0)

    pitch_fig, ax = plt.subplots(figsize=(10, 3))
    ax.plot(times, f0, label="Sung Pitch", color="blue")
    if reference_notes:
        ax.plot(times, ref_interp, label="Reference", linestyle="--", color="orange")
    ax.set_title("Pitch Contour")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Frequency (Hz)")
    ax.legend()
    pitch_plot = create_plot_image(pitch_fig)

    rms = librosa.feature.rms(y=y)[0]
    breath_fig, ax2 = plt.subplots(figsize=(10, 3))
    ax2.plot(librosa.times_like(rms), rms, label="RMS Energy", color="green")
    energy_threshold = np.median(rms) * 0.5
    ax2.axhline(y=energy_threshold, color='red', linestyle='--', label="Low Threshold")
    ax2.set_title("Breath Support Analysis")
    ax2.set_xlabel("Time (s)")
    ax2.set_ylabel("Energy")
    ax2.legend()
    breath_plot = create_plot_image(breath_fig)

    centroid = librosa.feature.spectral_centroid(y=y, sr=sr)[0]

    pitch_score, breath_score, diction_score, total_score = score_analysis_metrics(deviation, rms, centroid)

    feedback = {
        "pitch_score": pitch_score,
        "breath_score": breath_score,
        "diction_score": diction_score,
        "total_score": total_score,
        "pitch_plot": pitch_plot,
        "breath_plot": breath_plot,
        "pitch_feedback": get_feedback(pitch_score, "pitch"),
        "breath_feedback": get_feedback(breath_score, "breath"),
        "diction_feedback": get_feedback(diction_score, "diction")
    }

    return feedback
