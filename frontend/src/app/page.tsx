'use client';

import { useState } from 'react';
import { analyzeFile } from '../../lib/api';
import './page.module.css';

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [referenceNotes, setReferenceNotes] = useState('');
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async () => {
    if (!file) return;
    setLoading(true);
    try {
      const data = await analyzeFile(file, referenceNotes);
      setResult(data);
    } catch (err) {
      alert('Error analyzing file');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="analyzer-container">
      <h1 className="analyzer-title">🎤 VirtuOpera Vocal Analyzer</h1>

      <div className="input-group">
        <label className="input-label">Upload Singing Audio (.wav)</label>
        <input type="file" accept=".wav" onChange={(e) => setFile(e.target.files?.[0] || null)} />
      </div>

      <div className="input-group">
        <label className="input-label">Reference Notes (optional)</label>
        <input
          type="text"
          placeholder="e.g. C4,D4,E4"
          value={referenceNotes}
          onChange={(e) => setReferenceNotes(e.target.value)}
        />
      </div>

      <button onClick={handleAnalyze} disabled={loading || !file}>
        {loading ? 'Analyzing...' : 'Analyze'}
      </button>

      {result && (
        <div className="feedback-section">
          <div>
            <h2>🎯 Pitch Feedback</h2>
            <p>{result.pitch_score}/10 — {result.pitch_feedback}</p>
            <img src={result.pitch_plot} alt="Pitch Plot" />
          </div>
          <div>
            <h2>💨 Breath Feedback</h2>
            <p>{result.breath_score}/10 — {result.breath_feedback}</p>
            <img src={result.breath_plot} alt="Breath Plot" />
          </div>
          <div>
            <h2>🗣 Diction Feedback</h2>
            <p>{result.diction_score}/10 — {result.diction_feedback}</p>
          </div>
          <div className="score-highlight">⭐ Total Score: {result.total_score}/10</div>
        </div>
      )}
    </main>
  );
}
