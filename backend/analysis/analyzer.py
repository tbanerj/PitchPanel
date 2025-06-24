import librosa
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
import os
import joblib
import subprocess
from sklearn.linear_model import LinearRegression
from scipy.signal import find_peaks, savgol_filter
from scipy.stats import pearsonr
import warnings
warnings.filterwarnings('ignore')

NOTE_FEEDBACK = {
    "pitch": [
        (0, 4, "Significant pitch issues. Focus on basic pitch matching and ear training."),
        (4, 6, "Moderate pitch problems. Practice with a tuner and sustained notes."),
        (6, 8, "Good pitch control with some drift. Work on interval accuracy."),
        (8, 10, "Excellent pitch accuracy and stability.")
    ],
    "breath": [
        (0, 4, "Poor breath support. Practice diaphragmatic breathing and long tones."),
        (4, 6, "Inconsistent breath control. Work on breath management and phrasing."),
        (6, 8, "Good breath support with minor inconsistencies."),
        (8, 10, "Excellent breath control and support.")
    ],
    "diction": [
        (0, 4, "Unclear articulation. Practice vowel shaping and consonant clarity."),
        (4, 6, "Moderate diction issues. Focus on vowel placement and consonant precision."),
        (6, 8, "Good diction with room for improvement in clarity."),
        (8, 10, "Clear, precise articulation and diction.")
    ]
}

def get_feedback(score, category):
    for low, high, msg in NOTE_FEEDBACK[category]:
        if low <= score < high:
            return msg
    return NOTE_FEEDBACK[category][-1][2]  # Return highest feedback if score is 10

def create_plot_image(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", dpi=150)
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode("utf-8")
    plt.close(fig)
    return f"data:image/png;base64,{encoded}"

def train_advanced_model():
    # More comprehensive training data with realistic singing scenarios
    X = np.array([
        # Perfect singing
        [10, 10, 10],
        [9.5, 9.5, 9.5],
        [9, 9, 9],
        
        # Good singing with minor issues
        [8, 8, 8],
        [8, 7, 8],
        [7, 8, 7],
        [7, 7, 8],
        
        # Average singing
        [7, 6, 7],
        [6, 7, 6],
        [6, 6, 7],
        [6, 6, 6],
        
        # Below average
        [5, 5, 5],
        [5, 4, 5],
        [4, 5, 4],
        [4, 4, 5],
        
        # Poor singing
        [3, 3, 3],
        [3, 2, 3],
        [2, 3, 2],
        [2, 2, 3],
        
        # Very poor
        [1, 1, 1],
        [1, 0, 1],
        [0, 1, 0]
    ])
    
    # Weighted total scores (pitch weighted more heavily)
    y = np.array([
        10.0, 9.8, 9.5,  # Perfect
        8.2, 7.8, 7.6, 7.4,  # Good
        6.8, 6.6, 6.4, 6.0,  # Average
        5.2, 4.8, 4.6, 4.4,  # Below average
        3.2, 2.8, 2.6, 2.4,  # Poor
        1.2, 0.8, 0.6       # Very poor
    ])
    
    model = LinearRegression()
    model.fit(X, y)
    joblib.dump(model, "advanced_score_model.joblib")
    return model

def get_advanced_model():
    try:
        return joblib.load("advanced_score_model.joblib")
    except:
        return train_advanced_model()

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

def analyze_pitch_accuracy(f0, times, reference_notes=None, sr=22050):
    """Comprehensive pitch analysis including accuracy, stability, and vibrato"""
    
    # Remove NaN values for analysis
    valid_mask = ~np.isnan(f0)
    f0_clean = f0[valid_mask]
    times_clean = times[valid_mask]
    
    if len(f0_clean) == 0:
        return 0, 0, 0, 0
    
    # 1. Pitch accuracy (if reference provided)
    if reference_notes:
        ref_hz = [float(librosa.note_to_hz(note)) for note in reference_notes]
        ref_interp = np.interp(times_clean, np.linspace(0, times_clean[-1], len(ref_hz)), ref_hz)
        deviation = np.abs(ref_interp - f0_clean)
        
        # Calculate accuracy score based on deviation
        cents_deviation = 1200 * np.log2(f0_clean / ref_interp)
        accuracy_score = np.clip(10 - np.mean(np.abs(cents_deviation)) / 10, 0, 10)
    else:
        deviation = np.zeros_like(f0_clean)
        accuracy_score = 7.0  # Neutral score when no reference
    
    # 2. Pitch stability (variance in pitch)
    pitch_variance = np.var(f0_clean)
    stability_score = np.clip(10 - pitch_variance / 1000, 0, 10)
    
    # 3. Vibrato analysis
    # Detect vibrato by looking for periodic variations
    if len(f0_clean) > 50:
        # Apply smoothing to isolate vibrato
        smooth_f0 = savgol_filter(f0_clean, min(51, len(f0_clean)//2*2+1), 3)
        vibrato_signal = f0_clean - smooth_f0
        
        # Calculate vibrato rate and extent
        if len(vibrato_signal) > 20:
            # Find peaks in vibrato signal
            peaks, _ = find_peaks(np.abs(vibrato_signal), height=np.std(vibrato_signal))
            if len(peaks) > 2:
                vibrato_rate = len(peaks) / (times_clean[-1] - times_clean[0])  # Hz
                vibrato_extent = np.std(vibrato_signal)
                
                # Score vibrato (5-7 Hz is ideal, 0.5-2 semitones extent)
                rate_score = np.clip(10 - abs(vibrato_rate - 6) * 2, 0, 10)
                extent_score = np.clip(10 - abs(vibrato_extent - 50) / 10, 0, 10)
                vibrato_score = (rate_score + extent_score) / 2
            else:
                vibrato_score = 5.0  # No clear vibrato
        else:
            vibrato_score = 5.0
    else:
        vibrato_score = 5.0
    
    # 4. Overall pitch score (weighted combination)
    pitch_score = (accuracy_score * 0.4 + stability_score * 0.3 + vibrato_score * 0.3)
    
    return pitch_score, accuracy_score, stability_score, vibrato_score

def analyze_breath_support(y, sr, rms):
    """Comprehensive breath support analysis"""
    
    # 1. Energy consistency
    rms_smooth = savgol_filter(rms, min(51, len(rms)//2*2+1), 3)
    energy_variance = np.var(rms_smooth)
    energy_consistency = np.clip(10 - energy_variance * 100, 0, 10)
    
    # 2. Breath dropouts (low energy regions)
    energy_threshold = np.percentile(rms, 20)
    dropouts = np.sum(rms < energy_threshold)
    dropout_ratio = dropouts / len(rms)
    dropout_score = np.clip(10 - dropout_ratio * 50, 0, 10)
    
    # 3. Phrase length analysis
    # Find sustained notes (regions with consistent energy)
    energy_diff = np.abs(np.diff(rms_smooth))
    sustained_regions = energy_diff < np.percentile(energy_diff, 30)
    
    # Calculate average phrase length
    phrase_lengths = []
    current_length = 0
    for sustained in sustained_regions:
        if sustained:
            current_length += 1
        elif current_length > 0:
            phrase_lengths.append(current_length)
            current_length = 0
    
    if phrase_lengths:
        avg_phrase_length = np.mean(phrase_lengths) / sr  # Convert to seconds
        phrase_score = np.clip(avg_phrase_length * 2, 0, 10)  # 5+ seconds is excellent
    else:
        phrase_score = 3.0
    
    # 4. Breath timing analysis
    # Look for natural breath patterns
    energy_peaks, _ = find_peaks(rms, height=np.percentile(rms, 70), distance=sr//4)
    if len(energy_peaks) > 1:
        peak_intervals = np.diff(energy_peaks) / sr
        timing_consistency = 1 / np.std(peak_intervals) if np.std(peak_intervals) > 0 else 0
        timing_score = np.clip(timing_consistency / 10, 0, 10)
    else:
        timing_score = 5.0
    
    # 5. Overall breath score
    breath_score = (energy_consistency * 0.3 + dropout_score * 0.3 + 
                   phrase_score * 0.2 + timing_score * 0.2)
    
    return breath_score, energy_consistency, dropout_score, phrase_score, timing_score

def analyze_diction_articulation(y, sr):
    """Comprehensive diction and articulation analysis"""
    
    # 1. Spectral centroid (brightness)
    centroid = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
    centroid_mean = np.mean(centroid)
    centroid_std = np.std(centroid)
    
    # Higher centroid indicates brighter, more articulated sound
    brightness_score = np.clip((centroid_mean - 1000) / 200, 0, 10)
    
    # 2. Spectral rolloff (high frequency content)
    rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]
    rolloff_mean = np.mean(rolloff)
    rolloff_score = np.clip((rolloff_mean - 2000) / 500, 0, 10)
    
    # 3. Onset strength (consonant clarity)
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    onset_score = np.clip(np.mean(onset_env) * 5, 0, 10)
    
    # 4. Zero crossing rate (articulation clarity)
    zcr = librosa.feature.zero_crossing_rate(y)[0]
    zcr_mean = np.mean(zcr)
    # Moderate ZCR is good for singing (not too high, not too low)
    zcr_score = np.clip(10 - abs(zcr_mean - 0.08) * 100, 0, 10)
    
    # 5. MFCC analysis (timbre characteristics)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    mfcc_std = np.std(mfcc, axis=1)
    # Higher variance in MFCC indicates more articulation
    articulation_score = np.clip(np.mean(mfcc_std) * 2, 0, 10)
    
    # 6. Spectral contrast (consonant-vowel distinction)
    contrast = librosa.feature.spectral_contrast(y=y, sr=sr)
    contrast_score = np.clip(np.mean(contrast) * 0.5, 0, 10)
    
    # 7. Overall diction score
    diction_score = (brightness_score * 0.2 + rolloff_score * 0.15 + 
                    onset_score * 0.25 + zcr_score * 0.15 + 
                    articulation_score * 0.15 + contrast_score * 0.1)
    
    return diction_score, brightness_score, rolloff_score, onset_score, zcr_score, articulation_score, contrast_score

def score_analysis_metrics(f0, times, y, sr, rms, reference_notes=None):
    """Main scoring function using improved analysis methods"""
    
    # Analyze each component
    pitch_score, acc_score, stab_score, vib_score = analyze_pitch_accuracy(f0, times, reference_notes, sr)
    breath_score, energy_score, dropout_score, phrase_score, timing_score = analyze_breath_support(y, sr, rms)
    diction_score, bright_score, rolloff_score, onset_score, zcr_score, artic_score, contrast_score = analyze_diction_articulation(y, sr)
    
    # Use advanced model for final scoring
    model = get_advanced_model()
    total_score = model.predict([[pitch_score, breath_score, diction_score]])[0]
    total_score = np.clip(total_score, 0, 10)
    
    return (pitch_score, breath_score, diction_score, total_score,
            acc_score, stab_score, vib_score,
            energy_score, dropout_score, phrase_score, timing_score,
            bright_score, rolloff_score, onset_score, zcr_score, artic_score, contrast_score)

def analyze_singing_ai(file_path, reference_notes=None, sr=22050):
    """Main analysis function with improved algorithms"""
    
    delete_after = not file_path.endswith(".wav")
    if delete_after:
        file_path = convert_to_wav(file_path)

    # Load audio
    y, sr = librosa.load(file_path, sr=sr)
    
    # Extract fundamental frequency with better parameters
    f0, voiced_flag, voiced_probs = librosa.pyin(
        y, 
        fmin=float(librosa.note_to_hz('C2')), 
        fmax=float(librosa.note_to_hz('C7')), 
        sr=sr,
        frame_length=2048,
        hop_length=512,
        fill_na=np.nan
    )
    times = librosa.times_like(f0, sr=sr, hop_length=512)
    
    # Extract features
    rms = librosa.feature.rms(y=y, hop_length=512)[0]
    centroid = librosa.feature.spectral_centroid(y=y, sr=sr, hop_length=512)[0]
    
    # Score analysis
    (pitch_score, breath_score, diction_score, total_score,
     acc_score, stab_score, vib_score,
     energy_score, dropout_score, phrase_score, timing_score,
     bright_score, rolloff_score, onset_score, zcr_score, artic_score, contrast_score) = score_analysis_metrics(
        f0, times, y, sr, rms, reference_notes
    )
    
    # Create visualizations
    # Pitch plot
    pitch_fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 6))
    
    # Main pitch contour
    ax1.plot(times, f0, label="Sung Pitch", color="blue", alpha=0.7)
    if reference_notes:
        ref_hz = [float(librosa.note_to_hz(note)) for note in reference_notes]
        ref_interp = np.interp(times, np.linspace(0, times[-1], len(ref_hz)), ref_hz)
        ax1.plot(times, ref_interp, label="Reference", linestyle="--", color="orange", linewidth=2)
    ax1.set_title(f"Pitch Analysis (Score: {pitch_score:.1f}/10)")
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("Frequency (Hz)")
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Pitch accuracy over time
    if reference_notes:
        deviation = np.abs(ref_interp - f0)
        cents_deviation = 1200 * np.log2(f0 / ref_interp)
        ax2.plot(times, cents_deviation, label="Pitch Deviation (cents)", color="red", alpha=0.7)
        ax2.axhline(y=0, color='black', linestyle='-', alpha=0.5)
        ax2.axhline(y=50, color='gray', linestyle='--', alpha=0.5, label="±50 cents")
        ax2.axhline(y=-50, color='gray', linestyle='--', alpha=0.5)
        ax2.set_ylabel("Deviation (cents)")
        ax2.set_xlabel("Time (s)")
        ax2.legend()
        ax2.grid(True, alpha=0.3)
    
    pitch_plot = create_plot_image(pitch_fig)
    
    # Breath support plot
    breath_fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 6))
    
    # Energy contour
    rms_times = librosa.times_like(rms, sr=sr, hop_length=512)
    ax1.plot(rms_times, rms, label="RMS Energy", color="green", alpha=0.7)
    energy_threshold = np.percentile(rms, 20)
    ax1.axhline(y=energy_threshold, color='red', linestyle='--', label="Low Energy Threshold")
    ax1.set_title(f"Breath Support Analysis (Score: {breath_score:.1f}/10)")
    ax1.set_ylabel("Energy")
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Energy consistency
    rms_smooth = savgol_filter(rms, min(51, len(rms)//2*2+1), 3)
    ax2.plot(rms_times, rms_smooth, label="Smoothed Energy", color="darkgreen", alpha=0.7)
    ax2.set_xlabel("Time (s)")
    ax2.set_ylabel("Smoothed Energy")
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    breath_plot = create_plot_image(breath_fig)
    
    # Diction plot
    diction_fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 6))
    
    # Spectral centroid
    centroid_times = librosa.times_like(centroid, sr=sr, hop_length=512)
    ax1.plot(centroid_times, centroid, label="Spectral Centroid", color="purple", alpha=0.7)
    ax1.set_title(f"Diction Analysis (Score: {diction_score:.1f}/10)")
    ax1.set_ylabel("Frequency (Hz)")
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Onset strength
    onset_env = librosa.onset.onset_strength(y=y, sr=sr, hop_length=512)
    onset_times = librosa.times_like(onset_env, sr=sr, hop_length=512)
    ax2.plot(onset_times, onset_env, label="Onset Strength", color="orange", alpha=0.7)
    ax2.set_xlabel("Time (s)")
    ax2.set_ylabel("Onset Strength")
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    diction_plot = create_plot_image(diction_fig)
    
    # Cleanup
    if delete_after:
        cleanup_temp_uploads()

    # Return comprehensive feedback
    feedback = {
        "pitch_score": round(pitch_score, 1),
        "breath_score": round(breath_score, 1),
        "diction_score": round(diction_score, 1),
        "total_score": round(total_score, 1),
        "pitch_plot": pitch_plot,
        "breath_plot": breath_plot,
        "diction_plot": diction_plot,
        "pitch_feedback": get_feedback(pitch_score, "pitch"),
        "breath_feedback": get_feedback(breath_score, "breath"),
        "diction_feedback": get_feedback(diction_score, "diction"),
        "detailed_scores": {
            "pitch": {
                "accuracy": round(float(acc_score), 1),
                "stability": round(float(stab_score), 1),
                "vibrato": round(float(vib_score), 1)
            },
            "breath": {
                "energy_consistency": round(float(energy_score), 1),
                "dropout_control": round(float(dropout_score), 1),
                "phrase_length": round(float(phrase_score), 1),
                "timing": round(float(timing_score), 1)
            },
            "diction": {
                "brightness": round(float(bright_score), 1),
                "high_frequency": round(float(rolloff_score), 1),
                "consonant_clarity": round(float(onset_score), 1),
                "articulation": round(float(artic_score), 1),
                "contrast": round(float(contrast_score), 1)
            }
        }
    }

    return feedback
