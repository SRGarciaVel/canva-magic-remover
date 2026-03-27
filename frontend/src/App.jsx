import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import { useDropzone } from 'react-dropzone';
import { motion, AnimatePresence } from 'framer-motion';
import { Upload, Download, Copy, Check, Loader2, Wand2, History } from 'lucide-react';
import confetti from 'canvas-confetti';
import './App.css';

const API_BASE = "http://localhost:8000";

function App() {
  const [originalUrl, setOriginalUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [copied, setCopied] = useState(false);

  useEffect(() => { fetchHistory(); }, []);

  const fetchHistory = async () => {
    try {
      const res = await axios.get(`${API_BASE}/history/`);
      setHistory(res.data);
    } catch (e) { console.error(e); }
  };

  const processImage = async (imageFile) => {
    setLoading(true);
    setResult(null);
    const formData = new FormData();
    formData.append('file', imageFile);
    try {
      const res = await axios.post(`${API_BASE}/process/`, formData);
      setResult(res.data.url);
      confetti({ particleCount: 150, spread: 70, origin: { y: 0.6 } });
      fetchHistory();
    } catch (e) { alert("Error en el servidor"); }
    finally { setLoading(false); }
  };

  const handleDownload = async () => {
    const response = await fetch(result);
    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `diseno_madrina_${Date.now()}.png`);
    document.body.appendChild(link);
    link.click();
    link.remove();
  };

  const copyToClipboard = async () => {
    const response = await fetch(result);
    const blob = await response.blob();
    const item = new ClipboardItem({ "image/png": blob });
    await navigator.clipboard.write([item]);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const onDrop = useCallback(files => {
    if (files[0]) {
      setOriginalUrl(URL.createObjectURL(files[0]));
      processImage(files[0]);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop, accept: {'image/*': []}, multiple: false });

  return (
    <div className="app-container">
      <header style={{ textAlign: 'center', marginBottom: '48px' }}>
        <h1 style={{ fontSize: '2.5rem', fontWeight: 900, color: '#1e293b' }}>
          Mágica Canva Studio <Wand2 size={32} color="#8b3dff" />
        </h1>
        <p style={{ color: '#64748b' }}>Eliminación de fondos</p>
      </header>

      <div className="glass-panel">
        <div {...getRootProps()} className={`dropzone ${isDragActive ? 'active' : ''}`} 
             style={{ border: '2px dashed #e2e8f0', borderRadius: '24px', padding: '40px', textAlign: 'center', cursor: 'pointer' }}>
          <input {...getInputProps()} />
          {loading ? (
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '16px' }}>
              <Loader2 className="spin" size={40} color="#8b3dff" />
              <p style={{ color: '#8b3dff', fontWeight: 600 }}>La IA está trabajando...</p>
            </div>
          ) : (
            <div>
              <div style={{ background: '#f5f3ff', width: '48px', height: '48px', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 16px' }}>
                <Upload size={24} color="#8b3dff" />
              </div>
              <p style={{ fontSize: '1.1rem', fontWeight: 600, color: '#475569' }}>Arrastra una imagen o presiona Ctrl+V</p>
            </div>
          )}
        </div>

        <AnimatePresence>
          {result && (
            <div className="comparison-container">
              <div className="preview-card">
                <span className="label">Original</span>
                <div className="img-wrapper">
                  <img src={originalUrl} alt="Original" />
                </div>
              </div>
              <div className="preview-card">
                <span className="label">Resultado</span>
                <div className="img-wrapper checkerboard">
                  <img src={result} alt="Resultado" />
                </div>
              </div>
            </div>
          )}
        </AnimatePresence>

        {result && (
          <div className="actions">
            <button onClick={copyToClipboard} className="btn-primary">
              {copied ? <Check size={20} /> : <Copy size={20} />}
              {copied ? "¡Copiado!" : "Copiar para Canva"}
            </button>
            <button onClick={handleDownload} className="btn-secondary">
              <Download size={20} /> Guardar en PC
            </button>
          </div>
        )}
      </div>

      <footer style={{ maxWidth: '1000px', margin: '60px auto 0' }}>
        <h3 style={{ display: 'flex', alignItems: 'center', gap: '10px', fontSize: '1.1rem', color: '#1e293b' }}>
          <History size={20} /> Historial Reciente
        </h3>
        <div className="history-grid">
          {history.map(item => (
            <div key={item.id} className="history-item" onClick={() => { setResult(`${API_BASE}/outputs/${item.file_path}`); setOriginalUrl(null); }}>
              <img src={`${API_BASE}/outputs/${item.file_path}`} style={{ width: '100%', height: '100%', objectFit: 'contain' }} />
            </div>
          ))}
        </div>
      </footer>
    </div>
  );
}

export default App;