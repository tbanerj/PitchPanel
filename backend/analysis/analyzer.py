# analysis/voice_analyzer.py

import librosa
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

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

def analyze_singing_ai(file_path, reference_notes=None, sr=22050):
    y, sr = librosa.load(file_path, sr=sr)

    f0, _, _ = librosa.pyin(y, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'), sr=sr)
    times = librosa.times_like(f0)

    if reference_notes:
        ref_hz = [librosa.note_to_hz(note) for note in reference_notes]
        ref_interp = np.interp(times, np.linspace(0, times[-1], len(ref_hz)), ref_hz)
        deviation = np.abs(ref_interp - f0)
        mean_dev = np.nanmean(deviation)
        pitch_score = 9 if mean_dev < 15 else 6 if mean_dev < 30 else 3
    else:
        pitch_score = 5

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
    energy_threshold = np.median(rms) * 0.5
    dropouts = np.sum(rms < energy_threshold)
    breath_score = 9 if dropouts <= 3 else 6 if dropouts <= 8 else 3

    breath_fig, ax2 = plt.subplots(figsize=(10, 3))
    ax2.plot(librosa.times_like(rms), rms, label="RMS Energy", color="green")
    ax2.axhline(y=energy_threshold, color='red', linestyle='--', label="Low Threshold")
    ax2.set_title("Breath Support Analysis")
    ax2.set_xlabel("Time (s)")
    ax2.set_ylabel("Energy")
    ax2.legend()
    breath_plot = create_plot_image(breath_fig)

    centroid = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
    avg_centroid = np.mean(centroid)
    diction_score = 9 if avg_centroid > 2500 else 6 if avg_centroid > 1800 else 3

    pitch_fb = get_feedback(pitch_score, "pitch")
    breath_fb = get_feedback(breath_score, "breath")
    diction_fb = get_feedback(diction_score, "diction")

    feedback = {
        "pitch_score": pitch_score,
        "breath_score": breath_score,
        "diction_score": diction_score,
        "total_score": round((pitch_score + breath_score + diction_score) / 3, 1),
        "pitch_plot": pitch_plot,
        "breath_plot": breath_plot,
        "pitch_feedback": pitch_fb,
        "breath_feedback": breath_fb,
        "diction_feedback": diction_fb,
        "gpt_feedback": "GPT feedback temporarily disabled. Upgrade or re-enable later."
    }

    return feedback
