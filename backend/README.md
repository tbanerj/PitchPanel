# Vocal Analyzer Dev Guide

This guide explains the Python logic behind VirtuOpera’s vocal analysis engine. It provides an in-depth breakdown of the audio processing and scoring pipeline in `analyzer.py`.

---

## Overview

The program performs vocal analysis on `.wav` or `.webm` recordings. It evaluates three main categories:

- Pitch accuracy
- Breath support
- Diction clarity

Each category receives a score out of 10, and an ML model predicts a total score. Visual plots are also generated for pitch and breath.

---

## Imports
```python
import librosa          # For audio feature extraction
import numpy as np      # For numerical calculations
import matplotlib.pyplot as plt  # For plotting pitch/breath graphs
import io, base64       # For encoding plots to be returned via API
import os, joblib, subprocess    # For file I/O and model saving
from sklearn.linear_model import LinearRegression  # ML model
from scipy.signal import find_peaks               # Used in breath analysis
```

---

## Scoring Feedback Rules
```python
NOTE_FEEDBACK = {
  "pitch": [...],
  "breath": [...],
  "diction": [...]
}
```
This dictionary maps score ranges to personalized feedback for each vocal quality.

---

## Helper Functions

### `get_feedback(score, category)`
Returns the feedback message based on the score.

### `create_plot_image(fig)`
Encodes matplotlib figures as base64 PNGs to send via API.

### `train_simple_model()` / `get_basic_model()`
Creates or loads a simple linear regression model trained on synthetic data to calculate the total score based on pitch, breath, and diction scores.

### `convert_to_wav(input_path)`
Converts uploaded `.webm` or other formats to `.wav` using FFmpeg. Includes `-y` flag to auto-overwrite.

### `cleanup_temp_uploads()`
Deletes all files in the `temp_uploads/` directory after analysis to avoid clutter.

---

## `score_analysis_metrics(...)`

This is where individual vocal scores are calculated.

### **Pitch**
Uses the deviation of the fundamental frequency (`f0`) from reference notes (if provided). If reference is missing, default deviation is zero.

```python
good_ratio = np.sum(deviation < 30) / np.sum(~np.isnan(deviation))
```

Scoring rubric:
- >90% match = 10
- 75-90% = 8
- 50-75% = 6
- <50% = 4

### **Breath** (Hybrid Method)

Uses 5 features:
- Dropouts (low energy regions)
- RMS slope variance
- Zero crossing rate median
- RMS peak density (number of energy surges per second)

Scoring logic deducts from 10 based on thresholds:
```python
if dropouts > 20: -3
if slope_std > 0.01: -1
if zcr_median > 0.12: -1
if peak_density < 0.4: -1
```
Then the score is clipped between 0–10.

### **Diction** (Spectral + Rhythmic Clarity)

Uses:
- `centroid_mean` → brighter vowels
- `centroid_std` → vowel/consonant transitions
- `flux_var` → articulation dynamics

Scores are based on these features exceeding thresholds.

### **Total Score**
Predicted using the ML model:
```python
total_score = model.predict([[pitch_score, breath_score, diction_score]])
```

---

## `analyze_singing_ai()`
This is the main function called by the API.

### Steps:
1. **File Format Handling**
   - Converts to `.wav` if necessary
2. **Load Audio** using `librosa.load`
3. **Extract Features**:
   - `pyin()` for pitch/f0
   - `rms` for energy
   - `spectral_centroid` for diction
4. **Generate Plots** for pitch and breath
5. **Score & Feedback**: Uses `score_analysis_metrics()`
6. **Cleanup**: Deletes temp uploads
7. **Return JSON feedback**

---

## Final Thoughts

This module provides an explainable, hybrid vocal grading system. It uses:
- Signal processing for real-time musical features
- A simple machine learning model for total score
- Audio visualization for actionable insight

Future improvements could include:
- Neural models trained on real vocal coaching datasets
- Formant analysis for vowel shaping
- Pronunciation classification
- LLM integration for deeper natural feedback

---

For questions or contributions, feel free to open an issue or PR.
