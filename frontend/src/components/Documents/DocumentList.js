import React from 'react';
import './DocumentList.css';

const DocumentList = ({ documents, loading, onRefresh }) => {
  if (loading) {
    return (
      <div className="document-list-container">
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p>Loading your documents...</p>
        </div>
      </div>
    );
  }

  if (documents.length === 0) {
    return (
      <div className="document-list-container">
        <div className="empty-state">
          <h3>📄 No Documents Yet</h3>
          <p>Upload your first PDF document to get started with Study Buddy!</p>
          <button onClick={onRefresh} className="refresh-button">
            Refresh
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="document-list-container">
      <div className="document-list-header">
        <h2>📄 My Documents</h2>
        <button onClick={onRefresh} className="refresh-button">
          🔄 Refresh
        </button>
      </div>
      
      <div className="documents-grid">
        {documents.map((doc) => (
          <div key={doc.id} className="document-card">
            <div className="document-header">
              <h3 className="document-title">{doc.filename}</h3>
              <span className="document-date">
                {new Date(doc.created_at).toLocaleDateString()}
              </span>
            </div>
            
            <div className="document-info">
              <div className="info-item">
                <strong>Size:</strong> {doc.file_size ? `${Math.round(doc.file_size / 1024)} KB` : 'Unknown'}
              </div>
              <div className="info-item">
                <strong>Text Length:</strong> {doc.original_content?.length || 0} characters
              </div>
            </div>
            
            {doc.summary && (
              <div className="document-summary">
                <h4>📝 Summary</h4>
                <p className="summary-text">{doc.summary}</p>
              </div>
            )}
            
            <div className="document-actions">
              <button className="action-button view-button">
                👁️ View Details
              </button>
              <button className="action-button study-button">
                📚 Start Study Session
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default DocumentList;
