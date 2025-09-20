import React, { useState } from 'react';
import axios from 'axios';
import './UploadForm.css';

const UploadForm = ({ onDocumentUploaded }) => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      // Check if file is PDF
      if (selectedFile.type !== "application/pdf") {
        setError("Please select a PDF file only.");
        setFile(null);
        return;
      }
      setError(null);
      setFile(selectedFile);
      setResult(null);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setError("Please select a file first!");
      return;
    }

    setUploading(true);
    setError(null);
    setResult(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post("http://127.0.0.1:8000/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      
      if (res.data.status === "success") {
        setResult(res.data);
        onDocumentUploaded(res.data);
        // Reset file input
        setFile(null);
        document.getElementById('file-input').value = '';
      } else {
        setError(res.data.error || "Upload failed!");
      }
    } catch (err) {
      console.error(err);
      if (err.response?.data?.detail) {
        setError(err.response.data.detail);
      } else {
        setError("Upload failed! Please check if the backend server is running.");
      }
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="upload-form-container">
      <div className="upload-card">
        <h2>📤 Upload Document</h2>
        <p className="upload-subtitle">Upload your PDF documents and get AI-powered summaries!</p>
        
        <div className="upload-section">
          <div className="file-input-container">
            <input 
              type="file" 
              accept=".pdf"
              onChange={handleFileChange}
              className="file-input"
              id="file-input"
            />
            <label htmlFor="file-input" className="file-input-label">
              {file ? file.name : "Choose PDF File"}
            </label>
          </div>
          
          <button 
            onClick={handleUpload} 
            disabled={!file || uploading}
            className="upload-button"
          >
            {uploading ? "Processing..." : "Upload & Summarize"}
          </button>
        </div>

        {error && (
          <div className="error-message">
            ❌ {error}
          </div>
        )}

        {result && (
          <div className="result-section">
            <h3>📄 Document Summary</h3>
            <div className="file-info">
              <strong>File:</strong> {result.filename}
              <br />
              <strong>Text Length:</strong> {result.text_length} characters
            </div>
            
            <div className="summary-container">
              <h4>🤖 AI Summary</h4>
              <p className="summary-text">{result.summary}</p>
            </div>
            
            <div className="success-message">
              ✅ Document uploaded and processed successfully!
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default UploadForm;
