import React, { useState, useEffect } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { 
  Upload, 
  FileText, 
  Brain, 
  MessageSquare, 
  Plus, 
  TrendingUp,
  Clock,
  BookOpen
} from 'lucide-react';
import { Link } from 'react-router-dom';
import DocumentUpload from '../documents/DocumentUpload';
import DocumentList from '../documents/DocumentList';
import SummaryDisplay from '../ai/SummaryDisplay';
import QuizGenerator from '../quiz/QuizGenerator';
import AIChat from '../chat/AIChat';
import { summaryAPI, documentsAPI } from '../../services/api';

const Dashboard = () => {
  const { user } = useAuth();
  const [selectedDocument, setSelectedDocument] = useState(null);
  const [activeTab, setActiveTab] = useState('overview');
  const [documents, setDocuments] = useState([]);
  const [generatedSummary, setGeneratedSummary] = useState('');
  const [showLengthModal, setShowLengthModal] = useState(false);
  const [pendingDocForSummary, setPendingDocForSummary] = useState(null);

  const handleDocumentSelect = async (document) => {
    try {
      // Always fetch full document including text content
      const fullDoc = await documentsAPI.getDocument(document.id);
      setSelectedDocument(fullDoc);
    } catch (e) {
      console.error('Failed to fetch document details:', e);
      setSelectedDocument(document); // fallback so UI still updates
    }
  };

  const handleUploadSuccess = async (uploadedFile) => {
    // Refresh server documents to obtain real IDs
    try {
      const response = await documentsAPI.getMyDocuments();
      const serverDocs = response.documents || [];
      setDocuments(serverDocs);

      // Try to find the just-uploaded document by filename; fallback to most recent
      const matched = serverDocs.find((d) => d.filename === uploadedFile.name) || serverDocs[0] || null;
      if (!matched) return;

      // Fetch full document details (with content)
      try {
        const fullDoc = await documentsAPI.getDocument(matched.id);
        setSelectedDocument(fullDoc);
      } catch {
        setSelectedDocument(matched);
      }
      setActiveTab('summary');

      // Open modal to choose length
      setPendingDocForSummary(matched);
      setShowLengthModal(true);
    } catch (e) {
      console.error('Post-upload flow failed:', e);
    }
  };

  const handleGenerateWithLength = async (length) => {
    try {
      if (!pendingDocForSummary) return;
      // Ensure we have text content
      let text = pendingDocForSummary.content;
      if (!text) {
        try {
          const fullDoc = await documentsAPI.getDocument(pendingDocForSummary.id);
          text = fullDoc.content;
        } catch (e) {
          console.error('Unable to load document content for summary:', e);
        }
      }

      if (!text) {
        console.warn('No text content available for summary.');
        return;
      }

      const data = await summaryAPI.generate(pendingDocForSummary.id, text, length);
      if (data.summary) {
        setGeneratedSummary(data.summary);
      }
    } catch (e) {
      console.error('Summary generation failed:', e);
    } finally {
      setShowLengthModal(false);
      setPendingDocForSummary(null);
    }
  };

  const handleGenerateQuiz = (document) => {
    setSelectedDocument(document);
    setActiveTab('quiz');
  };

  const handleStartChat = (document) => {
    setSelectedDocument(document);
    setActiveTab('chat');
  };

  const tabs = [
    { id: 'overview', name: 'Overview', icon: BookOpen },
    { id: 'upload', name: 'Upload', icon: Upload },
    { id: 'documents', name: 'Documents', icon: FileText },
    { id: 'summary', name: 'Summary', icon: TrendingUp },
    { id: 'quiz', name: 'Quiz', icon: Brain },
    { id: 'chat', name: 'Chat', icon: MessageSquare },
  ];

  const renderTabContent = () => {
    switch (activeTab) {
      case 'overview':
        return <OverviewTab user={user} documents={documents} />;
      case 'upload':
        return <DocumentUpload onUploadSuccess={handleUploadSuccess} />;
      case 'documents':
        return (
          <DocumentList
            onDocumentSelect={handleDocumentSelect}
            onGenerateQuiz={handleGenerateQuiz}
            onStartChat={handleStartChat}
          />
        );
      case 'summary':
        return (
          <SummaryDisplay
            document={selectedDocument}
            summary={generatedSummary}
            onGenerateSummary={async (docId, length) => {
              try {
                // Ensure we have text; fetch full doc if needed
                let text = selectedDocument?.content;
                if (!text) {
                  try {
                    const fullDoc = await documentsAPI.getDocument(docId);
                    text = fullDoc?.content;
                  } catch (e) {
                    console.error('Failed to fetch full document for summary:', e);
                  }
                }

                if (!text) {
                  alert("❗ Document text not loaded. Make sure the document includes text content.");
                  return;
                }

                const data = await summaryAPI.generate(docId, text, length);
                console.log("📄 Summary API response:", data);

                if (data.summary) {
                  setGeneratedSummary(data.summary);
                } else {
                  alert("⚠️ No summary found:\n\n" + (data.error || "Unknown error"));
                }
              } catch (err) {
                console.error("❌ Error generating summary:", err);
                alert("Error connecting to backend. Check console for details.");
              }
            }}
          />
        );
      case 'quiz':
        return <QuizGenerator document={selectedDocument} />;
      case 'chat':
        return <AIChat document={selectedDocument} />;
      default:
        return <OverviewTab user={user} documents={documents} />;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">
            Welcome back, {user?.name}! 👋
          </h1>
          <p className="mt-2 text-gray-600">
            Ready to continue your learning journey with AI?
          </p>
        </div>

        {/* Tab Navigation */}
        <div className="mb-8">
          <div className="border-b border-gray-200">
            <nav className="-mb-px flex space-x-8 overflow-x-auto">
              {tabs.map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center space-x-2 whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                    activeTab === tab.id
                      ? 'border-primary-500 text-primary-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  <tab.icon className="h-5 w-5" />
                  <span>{tab.name}</span>
                </button>
              ))}
            </nav>
          </div>
        </div>

        {/* Tab Content */}
        <div className="animate-fade-in">
          {renderTabContent()}
        </div>

        {/* Summary Length Modal */}
        {showLengthModal && (
          <div className="fixed inset-0 z-50 flex items-center justify-center">
            <div className="absolute inset-0 bg-black/40" onClick={() => { setShowLengthModal(false); setPendingDocForSummary(null); }}></div>
            <div className="relative bg-white rounded-lg shadow-xl w-full max-w-md mx-4 p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Choose summary length</h3>
              <p className="text-sm text-gray-600 mb-4">Select how detailed you want the AI summary to be.</p>
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 mb-6">
                <button onClick={() => handleGenerateWithLength('short')} className="btn-secondary">Short</button>
                <button onClick={() => handleGenerateWithLength('medium')} className="btn-primary">Medium</button>
                <button onClick={() => handleGenerateWithLength('long')} className="btn-secondary">Long</button>
              </div>
              <div className="flex justify-end">
                <button onClick={() => { setShowLengthModal(false); setPendingDocForSummary(null); }} className="btn-secondary">Cancel</button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

// Overview Tab Component
const OverviewTab = ({ user, documents }) => {
  const stats = [
    {
      name: 'Documents Uploaded',
      value: documents.length,
      icon: FileText,
      color: 'text-blue-600',
      bgColor: 'bg-blue-100',
    },
    {
      name: 'Quizzes Taken',
      value: '0', // This would come from actual data
      icon: Brain,
      color: 'text-purple-600',
      bgColor: 'bg-purple-100',
    },
    {
      name: 'AI Conversations',
      value: '0', // This would come from actual data
      icon: MessageSquare,
      color: 'text-green-600',
      bgColor: 'bg-green-100',
    },
    {
      name: 'Study Time',
      value: '0h 0m', // This would come from actual data
      icon: Clock,
      color: 'text-orange-600',
      bgColor: 'bg-orange-100',
    },
  ];

  const quickActions = [
    {
      title: 'Upload New Document',
      description: 'Add a PDF, DOCX, or TXT file to get started',
      icon: Upload,
      color: 'bg-primary-600',
      href: '#upload',
    },
    {
      title: 'Generate Quiz',
      description: 'Create a quiz from your documents',
      icon: Brain,
      color: 'bg-purple-600',
      href: '#quiz',
    },
    {
      title: 'Chat with AI',
      description: 'Ask questions about your documents',
      icon: MessageSquare,
      color: 'bg-green-600',
      href: '#chat',
    },
  ];

  return (
    <div className="space-y-8">
      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat) => (
          <div key={stat.name} className="card">
            <div className="flex items-center">
              <div className={`p-3 rounded-lg ${stat.bgColor}`}>
                <stat.icon className={`h-6 w-6 ${stat.color}`} />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">{stat.name}</p>
                <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Quick Actions */}
      <div>
        <h2 className="text-xl font-semibold text-gray-900 mb-6">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {quickActions.map((action) => (
            <div
              key={action.title}
              className="card-hover group"
              onClick={() => {
                // Handle navigation to specific tab
                const tabId = action.href.replace('#', '');
                // This would need to be passed up to parent component
                console.log('Navigate to:', tabId);
              }}
            >
              <div className={`w-12 h-12 ${action.color} rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition-transform`}>
                <action.icon className="h-6 w-6 text-white" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                {action.title}
              </h3>
              <p className="text-gray-600">
                {action.description}
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* Recent Activity */}
      <div>
        <h2 className="text-xl font-semibold text-gray-900 mb-6">Recent Activity</h2>
        <div className="card">
          {documents.length > 0 ? (
            <div className="space-y-4">
              {documents.slice(0, 3).map((doc) => (
                <div key={doc.id} className="flex items-center space-x-4 p-4 bg-gray-50 rounded-lg">
                  <FileText className="h-8 w-8 text-gray-400" />
                  <div className="flex-1">
                    <p className="font-medium text-gray-900">{doc.name}</p>
                    <p className="text-sm text-gray-500">Uploaded recently</p>
                  </div>
                  <div className="flex space-x-2">
                    <button className="p-2 text-gray-400 hover:text-primary-600 hover:bg-primary-50 rounded-lg transition-colors">
                      <Brain className="h-4 w-4" />
                    </button>
                    <button className="p-2 text-gray-400 hover:text-green-600 hover:bg-green-50 rounded-lg transition-colors">
                      <MessageSquare className="h-4 w-4" />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-8">
              <FileText className="h-12 w-12 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">No documents yet</h3>
              <p className="text-gray-500 mb-4">
                Upload your first document to get started with AI-powered learning
              </p>
              <button
                onClick={() => {
                  // Navigate to upload tab
                  console.log('Navigate to upload');
                }}
                className="btn-primary flex items-center space-x-2 mx-auto"
              >
                <Plus className="h-5 w-5" />
                <span>Upload Document</span>
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
