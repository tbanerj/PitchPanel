'use client';

import { useState } from 'react';
import { analyzeFile } from '../../lib/api';
import Recorder from '../components/Recorder';

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [recordedFile, setRecordedFile] = useState<File | null>(null);
  const [referenceNotes, setReferenceNotes] = useState('');
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async (inputFile?: File) => {
    const fileToAnalyze = inputFile || file || recordedFile;
    if (!fileToAnalyze) return;
    setLoading(true);
    try {
      const analysis = await analyzeFile(fileToAnalyze, referenceNotes);
      setResult(analysis);
    } catch (err) {
      alert('Error analyzing file');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col justify-center items-center bg-gradient-to-br from-white to-purple-100 px-4 py-12">
      <main className="analyzer-container">
        <h1 className="analyzer-title">Vocal Analyzer</h1>

        <div className="input-group">
          <label className="input-label" htmlFor="fileUpload">
            Upload Audio File
          </label>
          <input
            id="fileUpload"
            type="file"
            accept="audio/*"
            onChange={(e) => setFile(e.target.files?.[0] || null)}
          />
        </div>

        <div className="input-group">
          <label className="input-label" htmlFor="referenceInput">
            Reference Notes
          </label>
          <input
            id="referenceInput"
            type="text"
            placeholder="e.g. C4,D4,E4"
            value={referenceNotes}
            onChange={(e) => setReferenceNotes(e.target.value)}
          />
        </div>

        <div className="input-group">
          <label className="input-label">Record Audio</label>
          <Recorder
            onRecordingComplete={(blob) => {
              const newFile = new File([blob], 'recording.webm', { type: 'audio/webm' });
              setRecordedFile(newFile);
            }}
          />
          {recordedFile && (
            <audio controls className="mt-2 w-full">
              <source src={URL.createObjectURL(recordedFile)} type="audio/webm" />
              Your browser does not support the audio element.
            </audio>
          )}
        </div>

        <button
          onClick={() => handleAnalyze()}
          disabled={loading || !(file || recordedFile)}
        >
          {loading ? 'Analyzing...' : 'Analyze'}
        </button>

        {result && (
          <div className="feedback-section">
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

            <div className="score-highlight">
              Total Score: {result.total_score}/10
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
