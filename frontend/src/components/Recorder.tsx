'use client';

import { useState, useRef, ChangeEvent } from 'react';

export default function Recorder({ 
  onRecordingComplete, 
  onSheetMusicUpload 
}: { 
  onRecordingComplete: (blob: Blob) => void,
  onSheetMusicUpload?: (file: File) => void 
}) {
  const [recording, setRecording] = useState(false);
  const [sheetMusicFile, setSheetMusicFile] = useState<File | null>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<Blob[]>([]);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream, {
        mimeType: 'audio/webm'
      });

      chunksRef.current = [];

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          chunksRef.current.push(event.data);
        }
      };

      mediaRecorder.onstop = () => {
        const audioBlob = new Blob(chunksRef.current, { type: 'audio/webm' });
        onRecordingComplete(audioBlob);
        stream.getTracks().forEach(track => track.stop());
      };

      mediaRecorderRef.current = mediaRecorder;
      mediaRecorder.start();
      setRecording(true);
    } catch (err) {
      alert("Microphone access denied or not supported.");
      console.error(err);
    }
  };

  const stopRecording = () => {
    mediaRecorderRef.current?.stop();
    setRecording(false);
  };

  const handleSheetMusicUpload = (e: ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      const file = files[0];
      if (file.type.match('image.*')) {
        setSheetMusicFile(file);
        if (onSheetMusicUpload) {
          onSheetMusicUpload(file);
        }
      } else {
        alert('Please upload an image file (JPEG, PNG)');
      }
    }
  };

  const triggerFileInput = () => {
    fileInputRef.current?.click();
  };

  return (
    <div style={{ marginTop: '1rem', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
      <div style={{ display: 'flex', gap: '1rem' }}>
        <button onClick={recording ? stopRecording : startRecording}>
          {recording ? 'Stop Recording' : 'Start Recording'}
        </button>
        
        {/* <button 
          onClick={triggerFileInput}
          style={{ backgroundColor: sheetMusicFile ? '#e0f7fa' : undefined }}
        >
          {sheetMusicFile ? 'Sheet Music Uploaded' : 'Upload Sheet Music'}
        </button> */}
        
        <input
          type="file"
          ref={fileInputRef}
          onChange={handleSheetMusicUpload}
          accept="image/*"
          style={{ display: 'none' }}
        />
      </div>
      
      {sheetMusicFile && (
        <div style={{ 
          padding: '0.5rem',
          border: '1px solid #ddd',
          borderRadius: '4px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between'
        }}>
          <span>{sheetMusicFile.name}</span>
          <button 
            onClick={() => {
              setSheetMusicFile(null);
              if (fileInputRef.current) fileInputRef.current.value = '';
            }}
            style={{ marginLeft: '0.5rem' }}
          >
            ×
          </button>
        </div>
      )}
    </div>
  );
}