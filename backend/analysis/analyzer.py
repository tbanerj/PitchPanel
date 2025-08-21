import librosa
from pathlib import Path
import sys
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
import os
import joblib
import glob
import subprocess
from sklearn.linear_model import LinearRegression
from scipy.signal import find_peaks, savgol_filter
from scipy.stats import pearsonr
import warnings
warnings.filterwarnings('ignore')
from scipy.spatial.distance import cdist
from librosa.sequence import dtw as librosa_dtw
import librosa.display  # <-- add this so create_diction_plot() works



NOTE_FEEDBACK = {
    "pitch": [
        (0, 4,  "Significant intonation drift. Work with slow reference tones; slide into pitch, then settle. Use short loops (1–2 bars) and hold the center of the note before adding any vibrato."),
        (4, 6,  "Moderate intonation issues. Sustain notes against a drone; aim for a steady center, then add gentle vibrato only after stability is achieved."),
        (6, 8,  "Generally stable pitch with occasional scoops. Practice interval targets: pause on the arrival pitch, then release. Use slow portamenti to lock centers."),
        (8, 10, "Accurate and steady. Maintain pitch centers on long tones; keep vibrato shallow and even after the pitch is locked.")
    ],
    "breath": [
        (0, 4,  "Airflow is uneven. Aim for lateral ribcage expansion on inhale; on exhale, think ‘pliable, flexible release’ so the air stays even. Try 8–10 second steady hiss exercises."),
        (4, 6,  "Inconsistent airflow. Practice silent, low inhalation with side expansion; keep the ribs gently buoyant during phrases. Use messa di voce on a single pitch."),
        (6, 8,  "Good airflow with minor dips. Plan breaths at phrase joints; use a slow count-out exhale (e.g., count to 12) to keep pressure even."),
        (8, 10, "Consistent, efficient airflow. Continue lateral expansion on inhale and supple release on exhale; lengthen phrases without pressing.")
    ],
    "diction": [
        (0, 4,  "Consonants blur and vowels shift. Isolate text on a single pitch (‘spoken on pitch’); shape pure vowels (i, e, a, o, u) before adding melody."),
        (4, 6,  "Some muddiness on fast text. Pop consonants at note onsets and keep vowels stable for the note’s duration. Try ‘vowel chains’ slowly, then add tempo."),
        (6, 8,  "Clear overall with a few swallowed consonants. Keep tongue forward on bright vowels and release final consonants cleanly."),
        (8, 10, "Crisp consonants and stable vowels. Maintain vowel purity through the note; add expressive consonant energy at boundaries.")
    ]
}


def extract_reference_pitches_from_sheetmusic(sheet_image_path):
    """
    Uses SheetVision to generate MIDI and extract pitch names from the MIDI file.
    Returns: List of pitch names like ['C4', 'E4', 'G4']
    """
    sheetvision_path = Path(__file__).parent / "SheetVision" / "main.py"
    midi_output_path = Path(__file__).parent / "SheetVision" / "output.mid"  # Adjust if SheetVision uses a different name

    try:
        # Run SheetVision and generate MIDI
        result = subprocess.run(
            [sys.executable, str(sheetvision_path), sheet_image_path],
            capture_output=True,
            text=True,
            check=True
        )

        # Load MIDI file
        if not midi_output_path.exists():
            print(f"[ERROR] MIDI output file not found at: {midi_output_path}")
            return []

        midi_data = pretty_midi.PrettyMIDI(str(midi_output_path))

        # Extract all pitch numbers (int), then convert to note names (e.g., 60 → 'C4')
        reference_notes = []
        for instrument in midi_data.instruments:
            for note in instrument.notes:
                note_name = librosa.midi_to_note(note.pitch)
                reference_notes.append(note_name)

        return reference_notes

    except subprocess.CalledProcessError as e:
        print(f"[ERROR] SheetVision failed:\n{e.stderr}")
        return []
    except Exception as e:
        print(f"[ERROR] MIDI extraction failed: {e}")
        return []

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
    """Remove all audio files from backend/temp_uploads/ after processing."""
    temp_dir = "backend/temp_uploads"
    audio_exts = ("*.wav", "*.webm", "*.mp3", "*.m4a", "*.ogg", "*.flac")  # add more if needed

    for ext in audio_exts:
        for f in glob.glob(os.path.join(temp_dir, ext)):
            try:
                os.remove(f)
                print(f"Deleted: {f}")
            except Exception as e:
                print(f"Error deleting {f}: {e}")

import numpy as np
import librosa
from scipy.signal import savgol_filter, butter, filtfilt

def analyze_pitch_accuracy(f0, times, reference_notes=None, sr=22050, debug=False):
    """
    Vibrato-aware pitch scoring.
    Returns:
      pitch_score, accuracy_score, stability_score, vibrato_score, debug_dict
    """
    # --- Clean ---
    valid_mask = ~np.isnan(f0)
    f0_clean = f0[valid_mask]
    times_clean = times[valid_mask]

    if len(f0_clean) < 10 or times_clean[-1] <= times_clean[0]:
        return 5.0, 5.0, 5.0, 5.0, {}

    # --- 1) Pitch center via smoothing (do not penalize vibrato) ---
    # Ensure odd window and at least 5
    win = min(101, len(f0_clean))
    if win % 2 == 0:
        win -= 1
    win = max(win, 5)
    smooth_f0 = savgol_filter(f0_clean, win, 3)

    # --- 2) Vibrato metrics on cents residuals ---
    # Convert residual to cents relative to the center
    ratio = np.clip(f0_clean / np.clip(smooth_f0, 1e-6, None), 1e-6, None)
    resid_cents = 1200.0 * np.log2(ratio)

    # Effective frame rate from time vector
    fs = len(resid_cents) / (times_clean[-1] - times_clean[0])

    # Band-pass 4–8 Hz to isolate musical vibrato
    low, high = 4.0, 8.0
    # Ensure filter is valid (Nyquist > high)
    nyq = fs / 2.0
    vib_band = resid_cents.copy()
    if nyq > high and len(resid_cents) > 10:
        b, a = butter(2, [low/nyq, high/nyq], btype='band')
        vib_band = filtfilt(b, a, resid_cents)

    vib_depth_cents = float(np.std(vib_band) * np.sqrt(2))  # ~peak depth from RMS
    vib_depth_cents = np.clip(vib_depth_cents, 0, 300)

    # Vibrato rate via FFT peak (4–8 Hz window)
    vib_rate_hz = np.nan
    if len(vib_band) > 16:
        freqs = np.fft.rfftfreq(len(vib_band), d=1.0/fs)
        mag = np.abs(np.fft.rfft(vib_band))
        band = (freqs >= low) & (freqs <= high)
        if np.any(band) and mag[band].sum() > 0:
            vib_rate_hz = float(freqs[band][np.argmax(mag[band])])

    # Score vibrato: ideal depth ~30–80 cents
    if 30 <= vib_depth_cents <= 80:
        vibrato_score = 10.0
    elif vib_depth_cents < 30:
        vibrato_score = max(0.0, 10.0 - (30 - vib_depth_cents) / 5.0)
    else:
        vibrato_score = max(0.0, 10.0 - (vib_depth_cents - 80) / 10.0)

    # --- 3) Stability of the center (not raw F0) ---
    # Use variance of smoothed center, normalized
    center_var = np.var(smooth_f0)
    stability_score = float(np.clip(10.0 - center_var / 500.0, 0.0, 10.0))

    # --- 4) Reference comparison (optional, use center vs reference) ---
    if reference_notes is not None and len(reference_notes) >= 2:
        ref_hz = np.array([float(librosa.note_to_hz(n)) for n in reference_notes], dtype=float)
        ref_time = np.linspace(0.0, times_clean[-1], len(ref_hz))
        ref_interp = np.interp(times_clean, ref_time, ref_hz)
        cents_dev = 1200.0 * np.log2(np.clip(smooth_f0 / np.clip(ref_interp, 1e-6, None), 1e-6, None))
        mean_abs_dev = float(np.nanmean(np.abs(cents_dev)))
        # 0–10 scale: ≤10–20 cents ~ top; 50 cents average ~ 0
        accuracy_score = float(np.clip(10.0 - (mean_abs_dev / 5.0), 0.0, 10.0))
    else:
        # No reference: accuracy from center stability + healthy vibrato
        # (lightly include interval smoothness)
        if len(smooth_f0) > 2:
            intervals = np.diff(smooth_f0)
            interval_var = np.var(np.abs(intervals))
            interval_score = float(np.clip(10.0 - interval_var / 1000.0, 0.0, 10.0))
        else:
            interval_score = 5.0
        accuracy_score = float(0.65 * stability_score + 0.25 * vibrato_score + 0.10 * interval_score)

    # --- 5) Combined pitch score ---
    pitch_score = float(0.7 * accuracy_score + 0.2 * stability_score + 0.1 * vibrato_score)

    debug_out = {}
    if debug:
        debug_out = {
            "vibrato_depth_cents": vib_depth_cents,
            "vibrato_rate_hz": vib_rate_hz,
            "center_variance": float(center_var),
            "frame_rate_hz": float(fs)
        }

    return pitch_score, accuracy_score, stability_score, float(vibrato_score), debug_out

def analyze_breath_support(y, sr, rms):
    """Comprehensive breath support analysis"""
    # 1. Energy consistency
    if len(rms) < 7:
        rms_smooth = rms  # Too short to smooth
    else:
        # Make sure window length is odd and <= len(rms)
        window_length = min(51, len(rms) if len(rms) % 2 == 1 else len(rms) - 1)
        rms_smooth = savgol_filter(rms, window_length, 3)

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
    """Enhanced diction and articulation analysis with better consonant detection"""
    
    # 1. Spectral centroid (brightness)
    centroid = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
    centroid_mean = np.mean(centroid)
    brightness_score = np.clip((centroid_mean - 1000) / 200, 0, 10)
    
    # 2. Spectral rolloff (high frequency content)
    rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr, roll_percent=0.95)[0]
    rolloff_mean = np.mean(rolloff)
    rolloff_score = np.clip((rolloff_mean - 2000) / 500, 0, 10)
    
    # 3. Enhanced onset detection for consonants
    onset_env = librosa.onset.onset_strength(y=y, sr=sr, aggregate=np.median)
    onset_frames = librosa.onset.onset_detect(onset_envelope=onset_env, sr=sr)
    
    # Calculate onset strength metrics
    if len(onset_frames) > 0:
        onset_strengths = onset_env[onset_frames]
        strong_onsets = np.sum(onset_strengths > np.percentile(onset_env, 75))
        onset_score = np.clip(strong_onsets / len(onset_frames) * 10, 0, 10)
    else:
        onset_score = 5.0  # Neutral score if no onsets detected
    
    # 4. Enhanced zero crossing rate analysis
    zcr = librosa.feature.zero_crossing_rate(y, frame_length=2048, hop_length=512)[0]
    zcr_mean = np.mean(zcr)
    zcr_var = np.var(zcr)
    
    # Higher variance indicates better consonant-vowel differentiation
    zcr_var_score = np.clip(zcr_var * 100, 0, 10)
    zcr_mean_score = np.clip(10 - abs(zcr_mean - 0.1) * 100, 0, 10)  # Ideal around 0.1
    zcr_score = (zcr_mean_score * 0.4 + zcr_var_score * 0.6)
    
    # 5. Enhanced MFCC analysis with delta features
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    mfcc_delta = librosa.feature.delta(mfcc)
    
    # Calculate articulation metrics
    mfcc_std = np.std(mfcc, axis=1)
    mfcc_delta_std = np.std(mfcc_delta, axis=1)
    
    # Combined articulation score
    articulation_score = np.clip(np.mean(mfcc_std) * 1.5 + np.mean(mfcc_delta_std) * 2, 0, 10)
    
    # 6. Enhanced spectral contrast with more bands
    contrast = librosa.feature.spectral_contrast(y=y, sr=sr, n_bands=6)
    contrast_score = np.clip(np.mean(contrast) * 0.6, 0, 10)
    
    # 7. New: Formant analysis for vowel clarity
    try:
        # Using a simple approximation of formant frequencies
        formant_ratio = np.mean(centroid) / np.mean(rolloff)
        formant_score = np.clip(10 - abs(formant_ratio - 0.4) * 20, 0, 10)
    except:
        formant_score = 5.0
    
    # 8. New: Harmonic-to-noise ratio for voice quality
    harmonic = librosa.effects.harmonic(y)
    percussive = librosa.effects.percussive(y)
    hnr = 10 * np.log10(np.mean(harmonic**2) / (np.mean(percussive**2) + 1e-10))
    hnr_score = np.clip(hnr / 5, 0, 10)  # 0-10 scale where higher is better
    
    # 9. New: Plosive detection (for consonant bursts)
    spectral_flatness = librosa.feature.spectral_flatness(y=y)[0]
    plosive_frames = np.where(spectral_flatness < np.percentile(spectral_flatness, 10))[0]
    plosive_score = np.clip(len(plosive_frames) / len(spectral_flatness) * 20, 0, 10)
    
    # Weighted overall diction score
    diction_score = (
        brightness_score * 0.15 + 
        rolloff_score * 0.15 +
        onset_score * 0.25 +
        zcr_score * 0.15 +
        articulation_score * 0.15 +
        contrast_score * 0.05 +
        formant_score * 0.05 +
        hnr_score * 0.03 +
        plosive_score * 0.02
    )
    
    return (
        diction_score, brightness_score, rolloff_score, 
        onset_score, zcr_score, articulation_score, 
        contrast_score, formant_score, hnr_score, plosive_score
    )

def create_diction_plot(y, sr, diction_score):
    """Enhanced diction visualization with more features"""
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 9))
    
    # Spectral features
    S = librosa.feature.melspectrogram(y=y, sr=sr)
    S_dB = librosa.power_to_db(S, ref=np.max)
    img = librosa.display.specshow(S_dB, x_axis='time', y_axis='mel', 
                                 sr=sr, fmax=8000, ax=ax1)
    ax1.set_title(f"Diction Analysis (Score: {diction_score:.1f}/10) - Spectrogram")
    fig.colorbar(img, ax=ax1, format='%+2.0f dB')
    
    # Onset strength
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    onset_times = librosa.times_like(onset_env, sr=sr)
    ax2.plot(onset_times, onset_env, label='Onset Strength', color='orange')
    ax2.set_ylabel('Strength')
    ax2.set_title('Consonant Detection')
    ax2.legend()
    
    # Zero crossing rate
    zcr = librosa.feature.zero_crossing_rate(y)[0]
    zcr_times = librosa.times_like(zcr, sr=sr)
    ax3.plot(zcr_times, zcr, label='Zero Crossing Rate', color='green')
    ax3.set_xlabel('Time (s)')
    ax3.set_ylabel('Rate')
    ax3.set_title('Articulation Clarity')
    ax3.legend()
    
    plt.tight_layout()
    return create_plot_image(fig)

def score_analysis_metrics(f0, times, y, sr, rms, reference_notes=None, debug=False):
    """Updated to handle enhanced diction analysis and pass debug flag"""
    
    # Analyze each component
    pitch_score, acc_score, stab_score, vib_score, dtw_debug = analyze_pitch_accuracy(f0, times, reference_notes, sr, debug=debug)
    breath_score, energy_score, dropout_score, phrase_score, timing_score = analyze_breath_support(y, sr, rms)
    
    # Enhanced diction analysis
    (diction_score, bright_score, rolloff_score, onset_score, 
     zcr_score, artic_score, contrast_score, formant_score, 
     hnr_score, plosive_score) = analyze_diction_articulation(y, sr)
    
    # Use advanced model for final scoring
    model = get_advanced_model()
    total_score = model.predict([[pitch_score, breath_score, diction_score]])[0]
    total_score = np.clip(total_score, 0, 10)
    
    return (pitch_score, breath_score, diction_score, total_score,
            acc_score, stab_score, vib_score,
            energy_score, dropout_score, phrase_score, timing_score,
            bright_score, rolloff_score, onset_score, zcr_score, 
            artic_score, contrast_score, formant_score, hnr_score, 
            plosive_score, dtw_debug)

def extract_reference_pitches_from_sheetmusic(sheet_image_path):
    """
    Simplified version of SheetVision integration.
    Extracts only the pitch names from a sheet music image.
    
    Returns: List of pitch names (e.g., ["C4", "E4", "G4", "C5"])
    """
    sheetvision_path = Path(__file__).parent / "SheetVision" / "main.py"
    
    try:
        result = subprocess.run(
            [sys.executable, str(sheetvision_path), sheet_image_path],
            capture_output=True,
            text=True,
            check=True
        )

        reference_notes = []
        for line in result.stdout.split('\n'):
            if "note" in line.lower():  # crude filter; adjust if needed
                parts = line.strip().split()
                if parts:
                    reference_notes.append(parts[0])  # Just the pitch name like "C4"
        
        return reference_notes

    except subprocess.CalledProcessError as e:
        print(f"SheetVision error: {e.stderr}")
        return []
    except Exception as e:
        print(f"Sheet music pitch extraction failed: {e}")
        return []


def analyze_singing_ai(file_path, reference_notes=None, sheet_image_path=None, sr=22050, debug=False):
    """Main analysis function for AI-based vocal feedback with optional reference pitch input from sheet music."""

    pitch_plot = None
    breath_plot = None
    diction_plot = None

    # Extract reference pitches from sheet music image if provided (commented out)
    # print(reference_notes)
    # if sheet_image_path and not reference_notes:
    #     reference_notes = extract_reference_pitches_from_sheetmusic(sheet_image_path)

    delete_after = not file_path.endswith(".wav")
    if delete_after:
        file_path = convert_to_wav(file_path)

    try:
        y, sr = librosa.load(file_path, sr=sr)

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
        rms = librosa.feature.rms(y=y, hop_length=512)[0]

        (pitch_score, breath_score, diction_score, total_score,
         acc_score, stab_score, vib_score,
         energy_score, dropout_score, phrase_score, timing_score,
         bright_score, rolloff_score, onset_score, zcr_score,
         artic_score, contrast_score, formant_score, hnr_score,
         plosive_score, dtw_debug) = score_analysis_metrics(
            f0, times, y, sr, rms, reference_notes, debug=debug
        )

        try:
            pitch_fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 6))
            ax1.plot(times, f0, label="Sung Pitch", color="blue", alpha=0.7)

            if reference_notes and len(reference_notes) >= 2:
                try:
                    ref_hz = [float(librosa.note_to_hz(note)) for note in reference_notes]
                    ref_interp = np.interp(times, np.linspace(0, times[-1], len(ref_hz)), ref_hz)

                    ax1.plot(times, ref_interp, label="Expected Pitch (Reference)", linestyle="--", color="orange", linewidth=2)

                    cents_deviation = 1200 * np.log2(f0 / ref_interp)
                    ax2.plot(times, cents_deviation, label="Pitch Deviation (cents)", color="red", alpha=0.7)
                    ax2.axhline(y=0, color='black', linestyle='-', alpha=0.5)
                    ax2.axhline(y=50, color='gray', linestyle='--', alpha=0.5, label="±50 cents")
                    ax2.axhline(y=-50, color='gray', linestyle='--', alpha=0.5)
                    ax2.set_ylabel("Deviation (cents)")
                    ax2.set_xlabel("Time (s)")
                    ax2.legend()
                    ax2.grid(True, alpha=0.3)
                except Exception as e:
                    print(f"[WARN] Could not plot reference notes: {e}")
            else:
                print("[INFO] No reference notes available — skipping expected pitch overlay.")

            ax1.set_title(f"Pitch Analysis (Score: {pitch_score:.1f}/10)")
            ax1.set_xlabel("Time (s)")
            ax1.set_ylabel("Frequency (Hz)")
            ax1.legend()
            ax1.grid(True, alpha=0.3)

            pitch_plot = create_plot_image(pitch_fig)
            plt.close(pitch_fig)
        except Exception as e:
            print(f"Error creating pitch plot: {e}")

        try:
            breath_fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 6))
            rms_times = librosa.times_like(rms, sr=sr, hop_length=512)
            ax1.plot(rms_times, rms, label="RMS Energy", color="green", alpha=0.7)
            energy_threshold = np.percentile(rms, 20)
            ax1.axhline(y=energy_threshold, color='red', linestyle='--', label="Low Energy Threshold")
            ax1.set_title(f"Breath Support Analysis (Score: {breath_score:.1f}/10)")
            ax1.set_ylabel("Energy")
            ax1.legend()
            ax1.grid(True, alpha=0.3)

            if len(rms) < 7:
                rms_smooth = rms
            else:
                window_len = min(51, len(rms) if len(rms) % 2 == 1 else len(rms) - 1)
                rms_smooth = savgol_filter(rms, window_len, 3)
            ax2.plot(rms_times, rms_smooth, label="Smoothed Energy", color="darkgreen", alpha=0.7)
            ax2.set_xlabel("Time (s)")
            ax2.set_ylabel("Smoothed Energy")
            ax2.legend()
            ax2.grid(True, alpha=0.3)

            breath_plot = create_plot_image(breath_fig)
            plt.close(breath_fig)
        except Exception as e:
            print(f"Error creating breath plot: {e}")

        try:
            diction_plot = create_diction_plot(y, sr, diction_score)
        except Exception as e:
            print(f"Error creating diction plot: {e}")

        cleanup_temp_uploads()

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
                    "spectral_contrast": round(float(contrast_score), 1),
                    "formant_clarity": round(float(formant_score), 1),
                    "voice_quality": round(float(hnr_score), 1),
                    "plosive_detection": round(float(plosive_score), 1)
                }
            },
            "reference_notes": reference_notes,
            "dtw_debug": dtw_debug,
        }

        return feedback

    except Exception as e:
        print(f"Error in analyze_singing_ai: {e}")
        raise
