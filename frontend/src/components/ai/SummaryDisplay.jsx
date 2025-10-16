import React, { useState } from 'react';
import { FileText, Copy, Check, Sparkles, BookOpen } from 'lucide-react';
import toast from 'react-hot-toast';

const SummaryDisplay = ({ document, summary, onGenerateSummary }) => {
  const [copied, setCopied] = useState(false);
  const [summaryLength, setSummaryLength] = useState('medium');
  const [isGenerating, setIsGenerating] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(summary);
      setCopied(true);
      toast.success('Summary copied!');
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      toast.error('Failed to copy summary.');
    }
  };

  const handleGenerate = async (length) => {
    if (!document) {
      toast.error('Please select a document first.');
      return;
    }
    setIsGenerating(true);
    try {
      await onGenerateSummary(document.id, length);
      setSummaryLength(length);
    } catch (err) {
      toast.error('Error generating summary.');
    } finally {
      setIsGenerating(false);
    }
  };

  if (!document) {
    return (
      <div className="card text-center py-12">
        <FileText className="h-12 w-12 text-gray-400 mx-auto mb-4" />
        <h3 className="text-lg font-medium text-gray-900 mb-2">No document selected</h3>
        <p className="text-gray-500">Select a document to generate its summary.</p>
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

      {/* Length Buttons */}
      <div className="mb-6">
        <h3 className="text-sm font-medium text-gray-700 mb-3">Choose summary length:</h3>
        <div className="flex flex-wrap gap-2">
          {['short', 'medium', 'long'].map((length) => (
            <button
              key={length}
              onClick={() => handleGenerate(length)}
              disabled={isGenerating}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                summaryLength === length
                  ? 'bg-primary-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              } ${isGenerating ? 'opacity-50 cursor-not-allowed' : ''}`}
            >
              {length.charAt(0).toUpperCase() + length.slice(1)}
            </button>
          ))}
        </div>
      </div>

      {/* Summary Display */}
      {isGenerating ? (
        <div className="flex flex-col items-center py-12 text-center">
          <div className="loading-spinner mb-4"></div>
          <p className="text-gray-600">Generating AI summary...</p>
          <p className="text-sm text-gray-500">Please wait a few seconds.</p>
        </div>
      ) : summary ? (
        <div className="bg-gray-50 p-6 rounded-lg border">
          <div className="flex items-center space-x-2 mb-3">
            <BookOpen className="h-5 w-5 text-primary-600" />
            <span className="font-medium text-gray-700">AI-Generated Summary</span>
          </div>
          <p className="text-gray-800 leading-relaxed whitespace-pre-wrap">{summary}</p>
        </div>
      ) : (
        <div className="text-center py-12">
          <Sparkles className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No summary yet</h3>
          <p className="text-gray-500 mb-4">
            Click “Generate” to get an AI-powered summary of this document.
          </p>
          <button
            onClick={() => handleGenerate('medium')}
            className="btn-primary px-4 py-2 rounded-lg"
          >
            Generate Summary
          </button>
        </div>
      )}
    </div>
  );
};

export default SummaryDisplay;
