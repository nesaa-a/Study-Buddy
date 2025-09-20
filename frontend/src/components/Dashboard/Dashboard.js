import React, { useState, useEffect } from 'react';
import axios from 'axios';
import UploadForm from '../Upload/UploadForm';
import DocumentList from '../Documents/DocumentList';
import UserProfile from '../Profile/UserProfile';
import './Dashboard.css';

const Dashboard = ({ user, onLogout }) => {
  const [activeTab, setActiveTab] = useState('upload');
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchDocuments();
  }, []);

  const fetchDocuments = async () => {
    try {
      setLoading(true);
      const response = await axios.get('http://127.0.0.1:8000/documents');
      setDocuments(response.data);
    } catch (error) {
      console.error('Error fetching documents:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDocumentUploaded = (newDocument) => {
    setDocuments([newDocument, ...documents]);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    delete axios.defaults.headers.common['Authorization'];
    onLogout();
  };

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <div className="header-content">
          <h1>📚 Study Buddy</h1>
          <div className="user-info">
            <span>Welcome, {user.username}!</span>
            <button onClick={handleLogout} className="logout-button">
              Logout
            </button>
          </div>
        </div>
      </header>

      <nav className="dashboard-nav">
        <button 
          className={`nav-button ${activeTab === 'upload' ? 'active' : ''}`}
          onClick={() => setActiveTab('upload')}
        >
          📤 Upload Document
        </button>
        <button 
          className={`nav-button ${activeTab === 'documents' ? 'active' : ''}`}
          onClick={() => setActiveTab('documents')}
        >
          📄 My Documents
        </button>
        <button 
          className={`nav-button ${activeTab === 'profile' ? 'active' : ''}`}
          onClick={() => setActiveTab('profile')}
        >
          👤 Profile
        </button>
      </nav>

      <main className="dashboard-main">
        {activeTab === 'upload' && (
          <UploadForm onDocumentUploaded={handleDocumentUploaded} />
        )}
        
        {activeTab === 'documents' && (
          <DocumentList 
            documents={documents} 
            loading={loading}
            onRefresh={fetchDocuments}
          />
        )}
        
        {activeTab === 'profile' && (
          <UserProfile user={user} />
        )}
      </main>
    </div>
  );
};

export default Dashboard;
