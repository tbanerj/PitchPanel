'use client';

import { useState } from 'react';
import { analyzeFile } from '../../../lib/api';
import Recorder from '../../components/Recorder';
import styles from './product.module.css';

export default function ProductPage() {
  const [file, setFile] = useState<File | null>(null);
  const [recordedFile, setRecordedFile] = useState<File | null>(null);
  const [sheetMusicFile, setSheetMusicFile] = useState<File | null>(null); // NEW
  const [referenceNotes, setReferenceNotes] = useState('');
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async (inputFile?: File) => {
    const fileToAnalyze = inputFile || file || recordedFile;
    if (!fileToAnalyze) return;
    setLoading(true);
    try {
      const analysis = await analyzeFile(fileToAnalyze, {
        referenceNotes,
        sheetMusic: sheetMusicFile || undefined,
      });
      setResult(analysis);
    } catch (err) {
      alert('Error analyzing file');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.pageWrapper}>
      <main className={styles.analyzerContainer}>
        <h1 className={styles.analyzerTitle}>Vocal Analyzer</h1>

        <div className={styles.inputGroup}>
          <label htmlFor="fileUpload">Upload Audio File</label>
          <input
            id="fileUpload"
            type="file"
            accept="audio/*"
            onChange={(e) => setFile(e.target.files?.[0] || null)}
          />
        </div>

        <div className={styles.inputGroup}>
          <label htmlFor="referenceInput">Reference Notes</label>
          <input
            id="referenceInput"
            type="text"
            placeholder="e.g. C4,D4,E4"
            value={referenceNotes}
            onChange={(e) => setReferenceNotes(e.target.value)}
          />
        </div>

        <div className={styles.inputGroup}>
          <label>Record Audio</label>
          <Recorder
            onRecordingComplete={(blob) => {
              const newFile = new File([blob], 'recording.webm', { type: 'audio/webm' });
              setRecordedFile(newFile);
            }}
            onSheetMusicUpload={setSheetMusicFile} // NEW
          />
          {recordedFile && (
            <audio controls className={styles.audioPreview}>
              <source src={URL.createObjectURL(recordedFile)} type="audio/webm" />
              Your browser does not support the audio element.
            </audio>
          )}
        </div>

        <button
          onClick={() => handleAnalyze()}
          disabled={loading || !(file || recordedFile)}
          className={styles.analyzeButton}
        >
          {loading ? 'Analyzing...' : 'Analyze'}
        </button>

        {result && (
          <div className={styles.feedbackSection}>
            <div>
              <h2>Pitch Feedback</h2>
              <p>{result.pitch_score}/10 — {result.pitch_feedback}</p>
              <img src={result.pitch_plot} alt="Pitch Plot" />
            </div>

            <div>
              <h2>Breath Feedback</h2>
              <p>{result.breath_score}/10 — {result.breath_feedback}</p>
              <img src={result.breath_plot} alt="Breath Plot" />
            </div>

            <div>
              <h2>Diction Feedback</h2>
              <p>{result.diction_score}/10 — {result.diction_feedback}</p>
            </div>

            <div className={styles.totalScore}>
              Total Score: {result.total_score}/10
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
