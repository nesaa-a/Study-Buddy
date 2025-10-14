import React, { useState, useEffect } from 'react';
import { FileText, Download, MessageSquare, Brain, Calendar, MoreVertical } from 'lucide-react';
import { documentsAPI } from '../../services/api';
import toast from 'react-hot-toast';

const DocumentList = ({ onDocumentSelect, onGenerateQuiz, onStartChat }) => {
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedDocument, setSelectedDocument] = useState(null);

  useEffect(() => {
    fetchDocuments();
  }, []);

  const fetchDocuments = async () => {
    try {
      setLoading(true);
      const response = await documentsAPI.getMyDocuments();
      setDocuments(response.documents || []);
    } catch (error) {
      console.error('Error fetching documents:', error);
      toast.error('Failed to load documents');
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  };

  const formatFileSize = (bytes) => {
    if (!bytes) return 'Unknown';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

 const getFileIcon = (filename) => {
  if (!filename || typeof filename !== "string") {
    return <FileText className="h-6 w-6 text-gray-400" />; // default icon
  }

  const extension = filename.split('.').pop().toLowerCase();
  switch (extension) {
    case 'pdf':
      return <FileText className="h-6 w-6 text-red-500" />;
    case 'docx':
    case 'doc':
      return <FileText className="h-6 w-6 text-blue-500" />;
    case 'txt':
      return <FileText className="h-6 w-6 text-gray-500" />;
    default:
      return <FileText className="h-6 w-6 text-gray-400" />;
  }
};
  const handleDocumentClick = (document) => {
    setSelectedDocument(document);
    if (onDocumentSelect) {
      onDocumentSelect(document);
    }
  };

  const handleGenerateQuiz = (document) => {
    if (onGenerateQuiz) {
      onGenerateQuiz(document);
    }
  };

  const handleStartChat = (document) => {
    if (onStartChat) {
      onStartChat(document);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="loading-spinner"></div>
        <span className="ml-3 text-gray-600">Loading documents...</span>
      </div>
    );
  }

  if (documents.length === 0) {
    return (
      <div className="text-center py-12">
        <FileText className="h-12 w-12 text-gray-400 mx-auto mb-4" />
        <h3 className="text-lg font-medium text-gray-900 mb-2">No documents yet</h3>
        <p className="text-gray-500 mb-4">
          Upload your first document to get started with AI-powered learning
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-semibold text-gray-900">
          My Documents ({documents.length})
        </h2>
        <button
          onClick={fetchDocuments}
          className="text-sm text-primary-600 hover:text-primary-700 font-medium"
        >
          Refresh
        </button>
      </div>

      <div className="grid gap-4">
        {documents.map((document) => (
          <div
            key={document.id}
            className={`card-hover ${
              selectedDocument?.id === document.id ? 'ring-2 ring-primary-500' : ''
            }`}
            onClick={() => handleDocumentClick(document)}
          >
            <div className="flex items-start justify-between">
              <div className="flex items-start space-x-4 flex-1">
                <div className="flex-shrink-0">
                  {getFileIcon(document.filename)}
                </div>
                
                <div className="flex-1 min-w-0">
                  <h3 className="text-lg font-medium text-gray-900 truncate">
                    {document.filename}
                  </h3>
                  
                  <div className="flex items-center space-x-4 mt-2 text-sm text-gray-500">
                    <div className="flex items-center">
                      <Calendar className="h-4 w-4 mr-1" />
                      {formatDate(document.upload_date)}
                    </div>
                    <div>
                      {formatFileSize(document.file_size)}
                    </div>
                  </div>
                  
                  {document.summary && (
                    <p className="mt-3 text-sm text-gray-600 line-clamp-2">
                      {document.summary}
                    </p>
                  )}
                </div>
              </div>

              <div className="flex items-center space-x-2 ml-4">
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    handleGenerateQuiz(document);
                  }}
                  className="p-2 text-gray-400 hover:text-primary-600 hover:bg-primary-50 rounded-lg transition-colors"
                  title="Generate Quiz"
                >
                  <Brain className="h-5 w-5" />
                </button>
                
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    handleStartChat(document);
                  }}
                  className="p-2 text-gray-400 hover:text-secondary-600 hover:bg-secondary-50 rounded-lg transition-colors"
                  title="Chat with AI"
                >
                  <MessageSquare className="h-5 w-5" />
                </button>
                
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    // Handle download
                  }}
                  className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-50 rounded-lg transition-colors"
                  title="Download"
                >
                  <Download className="h-5 w-5" />
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default DocumentList;
