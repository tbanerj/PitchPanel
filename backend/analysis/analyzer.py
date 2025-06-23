import librosa
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
import os
import joblib
import subprocess
from sklearn.linear_model import LinearRegression
from scipy.signal import find_peaks

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

def convert_to_wav(input_path):
    output_path = os.path.splitext(input_path)[0] + "_converted.wav"
    try:
        subprocess.run([
            "ffmpeg", "-y", "-i", input_path, "-ar", "22050", "-ac", "1", output_path
        ], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return output_path
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to convert audio file: {e.stderr.decode()}") from e

def cleanup_temp_uploads():
    temp_dir = "temp_uploads"
    if os.path.exists(temp_dir):
        for f in os.listdir(temp_dir):
            path = os.path.join(temp_dir, f)
            try:
                if os.path.isfile(path):
                    os.remove(path)
            except Exception as e:
                print(f"Failed to delete {path}: {e}")

def score_analysis_metrics(deviation, f0, rms, centroid, flux, zcr, y, sr):
    # --- PITCH ---
    # Only consider voiced frames (where f0 is not NaN)
    voiced = ~np.isnan(f0)
    if np.sum(voiced) == 0:
        pitch_score = 0
    else:
        # Mean absolute deviation from reference (in Hz)
        mean_dev = np.nanmean(deviation[voiced])
        # Pitch stability (standard deviation of f0 in cents)
        cents = 1200 * np.log2(f0[voiced] / np.nanmean(f0[voiced]))
        pitch_stability = np.nanstd(cents)
        # Score: lower deviation and lower instability = higher score
        pitch_score = 10 - (mean_dev / 30) - (pitch_stability / 50)
        pitch_score = np.clip(pitch_score, 0, 10)

    # --- BREATH ---
    # RMS energy: count dropouts (frames below 15th percentile)
    energy_threshold = np.percentile(rms, 15)
    dropouts = np.sum(rms < energy_threshold)
    dropout_ratio = dropouts / len(rms)
    rms_var = np.std(rms)
    # Penalize for high dropout ratio and high variance
    breath_score = 10 - (dropout_ratio * 20) - (rms_var * 50)
    breath_score = np.clip(breath_score, 0, 10)

    # --- DICTION ---
    centroid_mean = float(np.mean(centroid))
    centroid_std = float(np.std(centroid))
    flux_var = float(np.std(flux))
    zcr_median = float(np.median(zcr))
    # Score: higher centroid, higher flux, higher zcr = better diction
    # Normalize each metric to [0, 1] based on typical singing values
    centroid_score = np.clip((centroid_mean - 1200) / 1200, 0, 1)
    flux_score = np.clip((flux_var - 0.01) / 0.07, 0, 1)
    zcr_score = np.clip((zcr_median - 0.03) / 0.09, 0, 1)
    diction_score = (centroid_score + flux_score + zcr_score) / 3 * 10
    diction_score = np.clip(diction_score, 0, 10)

    # --- TOTAL SCORE ---
    model = get_basic_model()
    total_score = round(float(min(model.predict([[pitch_score, breath_score, diction_score]])[0], 10)), 1)

    return pitch_score, breath_score, diction_score, total_score

def analyze_singing_ai(file_path, reference_notes=None, sr=22050):
    delete_after = not file_path.endswith(".wav")
    if delete_after:
        file_path = convert_to_wav(file_path)

    y, sr = librosa.load(file_path, sr=sr)

    # --- PITCH EXTRACTION ---
    f0, _, _ = librosa.pyin(y, fmin=float(librosa.note_to_hz('C2')), fmax=float(librosa.note_to_hz('C7')), sr=sr)
    times = librosa.times_like(f0)

    if reference_notes:
        ref_hz = [librosa.note_to_hz(note) for note in reference_notes]
        ref_interp = np.interp(times, np.linspace(0, times[-1], len(ref_hz)), ref_hz)
        deviation = np.abs(ref_interp - f0)
    else:
        ref_interp = None
        deviation = np.zeros_like(f0)

    # --- PITCH PLOT ---
    pitch_fig, ax = plt.subplots(figsize=(10, 3))
    ax.plot(times, f0, label="Sung Pitch", color="blue")
    if reference_notes and ref_interp is not None:
        ax.plot(times, ref_interp, label="Reference", linestyle="--", color="orange")
    ax.set_title("Pitch Contour")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Frequency (Hz)")
    ax.legend()
    pitch_plot = create_plot_image(pitch_fig)

    # --- BREATH (RMS) ---
    rms = librosa.feature.rms(y=y)[0]
    breath_fig, ax2 = plt.subplots(figsize=(10, 3))
    ax2.plot(librosa.times_like(rms), rms, label="RMS Energy", color="green")
    energy_threshold = np.percentile(rms, 15)
    ax2.axhline(y=energy_threshold, color='red', linestyle='--', label="Low Threshold")
    ax2.set_title("Breath Support Analysis")
    ax2.set_xlabel("Time (s)")
    ax2.set_ylabel("Energy")
    ax2.legend()
    breath_plot = create_plot_image(breath_fig)

    # --- DICTION (SPECTRAL) ---
    centroid = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
    flux = librosa.onset.onset_strength(y=y, sr=sr)
    zcr = librosa.feature.zero_crossing_rate(y)[0]

    # --- SCORING ---
    pitch_score, breath_score, diction_score, total_score = score_analysis_metrics(
        deviation, f0, rms, centroid, flux, zcr, y, sr
    )

    cleanup_temp_uploads()

    feedback = {
        "pitch_score": int(round(pitch_score)),
        "breath_score": int(round(breath_score)),
        "diction_score": int(round(diction_score)),
        "total_score": float(total_score),
        "pitch_plot": pitch_plot,
        "breath_plot": breath_plot,
        "pitch_feedback": get_feedback(int(round(pitch_score)), "pitch"),
        "breath_feedback": get_feedback(int(round(breath_score)), "breath"),
        "diction_feedback": get_feedback(int(round(diction_score)), "diction")
    }

    return feedback
