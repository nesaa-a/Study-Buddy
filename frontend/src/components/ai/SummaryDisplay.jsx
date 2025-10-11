import React, { useState, useEffect } from 'react';
import { FileText, Copy, Check, Sparkles, Clock, BookOpen } from 'lucide-react';
import toast from 'react-hot-toast';

const SummaryDisplay = ({ document, summary, onGenerateSummary }) => {
  const [copied, setCopied] = useState(false);
  const [summaryLength, setSummaryLength] = useState('medium');
  const [isGenerating, setIsGenerating] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(summary);
      setCopied(true);
      toast.success('Summary copied to clipboard!');
      setTimeout(() => setCopied(false), 2000);
    } catch (error) {
      toast.error('Failed to copy summary');
    }
  };

  const handleGenerateSummary = async (length) => {
    if (!document) return;
    
    setIsGenerating(true);
    try {
      await onGenerateSummary(document.id, length);
      setSummaryLength(length);
    } catch (error) {
      toast.error('Failed to generate summary');
    } finally {
      setIsGenerating(false);
    }
  };

  const getSummaryLengthLabel = (length) => {
    switch (length) {
      case 'short': return 'Short (1-2 paragraphs)';
      case 'medium': return 'Medium (3-4 paragraphs)';
      case 'long': return 'Long (5+ paragraphs)';
      default: return 'Medium';
    }
  };

  if (!document) {
    return (
      <div className="card text-center py-12">
        <FileText className="h-12 w-12 text-gray-400 mx-auto mb-4" />
        <h3 className="text-lg font-medium text-gray-900 mb-2">No document selected</h3>
        <p className="text-gray-500">
          Select a document to view or generate its AI summary
        </p>
      </div>
    );
  }

  return (
    <div className="card">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center space-x-3">
          <div className="bg-primary-100 p-2 rounded-lg">
            <Sparkles className="h-6 w-6 text-primary-600" />
          </div>
          <div>
            <h2 className="text-xl font-semibold text-gray-900">AI Summary</h2>
            <p className="text-sm text-gray-500">{document.filename}</p>
          </div>
        </div>
        
        {summary && (
          <button
            onClick={handleCopy}
            className="flex items-center space-x-2 px-3 py-2 text-sm text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-lg transition-colors"
          >
            {copied ? (
              <>
                <Check className="h-4 w-4" />
                <span>Copied!</span>
              </>
            ) : (
              <>
                <Copy className="h-4 w-4" />
                <span>Copy</span>
              </>
            )}
          </button>
        )}
      </div>

      {/* Summary Length Controls */}
      <div className="mb-6">
        <h3 className="text-sm font-medium text-gray-700 mb-3">Summary Length</h3>
        <div className="flex space-x-2">
          {['short', 'medium', 'long'].map((length) => (
            <button
              key={length}
              onClick={() => handleGenerateSummary(length)}
              disabled={isGenerating}
              className={`px-4 py-2 text-sm font-medium rounded-lg transition-colors ${
                summaryLength === length
                  ? 'bg-primary-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              } ${isGenerating ? 'opacity-50 cursor-not-allowed' : ''}`}
            >
              {getSummaryLengthLabel(length)}
            </button>
          ))}
        </div>
      </div>

      {/* Summary Content */}
      <div className="space-y-4">
        {isGenerating ? (
          <div className="flex items-center justify-center py-12">
            <div className="text-center">
              <div className="loading-spinner mx-auto mb-4"></div>
              <p className="text-gray-600">Generating AI summary...</p>
              <p className="text-sm text-gray-500 mt-1">
                This may take a few moments
              </p>
            </div>
          </div>
        ) : summary ? (
          <div className="prose max-w-none">
            <div className="bg-gray-50 rounded-lg p-6">
              <div className="flex items-center space-x-2 mb-4">
                <BookOpen className="h-5 w-5 text-primary-600" />
                <span className="text-sm font-medium text-gray-700">
                  AI-Generated Summary
                </span>
                <span className="text-xs text-gray-500">
                  ({summary.split(' ').length} words)
                </span>
              </div>
              <div className="text-gray-800 leading-relaxed whitespace-pre-wrap">
                {summary}
              </div>
            </div>
          </div>
        ) : (
          <div className="text-center py-12">
            <Sparkles className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              Generate AI Summary
            </h3>
            <p className="text-gray-500 mb-6">
              Click on a summary length above to generate an AI-powered summary of your document
            </p>
            <button
              onClick={() => handleGenerateSummary('medium')}
              disabled={isGenerating}
              className="btn-primary"
            >
              Generate Summary
            </button>
          </div>
        )}
      </div>

      {/* Summary Stats */}
      {summary && (
        <div className="mt-6 pt-6 border-t border-gray-200">
          <div className="grid grid-cols-3 gap-4 text-center">
            <div>
              <div className="text-2xl font-bold text-primary-600">
                {summary.split(' ').length}
              </div>
              <div className="text-sm text-gray-500">Words</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-secondary-600">
                {summary.split('.').length - 1}
              </div>
              <div className="text-sm text-gray-500">Sentences</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-gray-600">
                {Math.ceil(summary.split(' ').length / 200)}
              </div>
              <div className="text-sm text-gray-500">Min Read</div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default SummaryDisplay;
