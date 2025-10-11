import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, FileText, X, CheckCircle, AlertCircle, Loader } from 'lucide-react';
import { documentsAPI } from '../../services/api';
import toast from 'react-hot-toast';

const DocumentUpload = ({ onUploadSuccess }) => {
  const [uploading, setUploading] = useState(false);
  const [uploadedFiles, setUploadedFiles] = useState([]);

  const onDrop = useCallback(async (acceptedFiles) => {
    if (acceptedFiles.length === 0) return;

    const file = acceptedFiles[0];
    
    // Validate file type
    const allowedTypes = [
      'application/pdf',
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
      'text/plain'
    ];
    
    if (!allowedTypes.includes(file.type)) {
      toast.error('Please upload a PDF, DOCX, or TXT file');
      return;
    }

    // Validate file size (max 10MB)
    if (file.size > 10 * 1024 * 1024) {
      toast.error('File size must be less than 10MB');
      return;
    }

    setUploading(true);
    
    try {
      const response = await documentsAPI.upload(file);
      
      const uploadedFile = {
        id: Date.now(),
        name: file.name,
        size: file.size,
        type: file.type,
        status: 'success',
        message: response.message,
        file: response.file,
      };
      
      setUploadedFiles(prev => [uploadedFile, ...prev]);
      toast.success('Document uploaded successfully!');
      
      if (onUploadSuccess) {
        onUploadSuccess(uploadedFile);
      }
      
    } catch (error) {
      const failedFile = {
        id: Date.now(),
        name: file.name,
        size: file.size,
        type: file.type,
        status: 'error',
        message: error.response?.data?.error || 'Upload failed',
      };
      
      setUploadedFiles(prev => [failedFile, ...prev]);
      console.error('Upload error:', error);
    } finally {
      setUploading(false);
    }
  }, [onUploadSuccess]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'text/plain': ['.txt']
    },
    multiple: false,
    disabled: uploading,
  });

  const removeFile = (fileId) => {
    setUploadedFiles(prev => prev.filter(file => file.id !== fileId));
  };

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const getFileIcon = (type) => {
    if (type === 'application/pdf') {
      return <FileText className="h-8 w-8 text-red-500" />;
    } else if (type === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document') {
      return <FileText className="h-8 w-8 text-blue-500" />;
    } else {
      return <FileText className="h-8 w-8 text-gray-500" />;
    }
  };

  return (
    <div className="space-y-6">
      {/* Upload Area */}
      <div
        {...getRootProps()}
        className={`dropzone ${isDragActive ? 'active' : ''} ${uploading ? 'opacity-50 cursor-not-allowed' : ''}`}
      >
        <input {...getInputProps()} />
        <div className="flex flex-col items-center justify-center space-y-4">
          {uploading ? (
            <Loader className="h-12 w-12 text-primary-500 animate-spin" />
          ) : (
            <Upload className="h-12 w-12 text-gray-400" />
          )}
          
          <div className="text-center">
            {isDragActive ? (
              <p className="text-lg font-medium text-primary-600">
                Drop your document here...
              </p>
            ) : (
              <>
                <p className="text-lg font-medium text-gray-700">
                  {uploading ? 'Uploading...' : 'Upload your study document'}
                </p>
                <p className="text-sm text-gray-500 mt-1">
                  Drag and drop a PDF, DOCX, or TXT file here, or click to browse
                </p>
              </>
            )}
          </div>
          
          <div className="text-xs text-gray-400">
            Supported formats: PDF, DOCX, TXT • Max size: 10MB
          </div>
        </div>
      </div>

      {/* Uploaded Files List */}
      {uploadedFiles.length > 0 && (
        <div className="space-y-3">
          <h3 className="text-lg font-medium text-gray-900">Recent Uploads</h3>
          {uploadedFiles.map((file) => (
            <div
              key={file.id}
              className="flex items-center justify-between p-4 bg-gray-50 rounded-lg border"
            >
              <div className="flex items-center space-x-3">
                {getFileIcon(file.type)}
                <div>
                  <p className="font-medium text-gray-900">{file.name}</p>
                  <p className="text-sm text-gray-500">
                    {formatFileSize(file.size)}
                  </p>
                </div>
              </div>
              
              <div className="flex items-center space-x-3">
                {file.status === 'success' && (
                  <div className="flex items-center text-green-600">
                    <CheckCircle className="h-5 w-5 mr-1" />
                    <span className="text-sm">Uploaded</span>
                  </div>
                )}
                
                {file.status === 'error' && (
                  <div className="flex items-center text-red-600">
                    <AlertCircle className="h-5 w-5 mr-1" />
                    <span className="text-sm">Failed</span>
                  </div>
                )}
                
                <button
                  onClick={() => removeFile(file.id)}
                  className="text-gray-400 hover:text-gray-600 transition-colors"
                >
                  <X className="h-5 w-5" />
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Features Info */}
      <div className="bg-primary-50 rounded-lg p-4">
        <h4 className="font-medium text-primary-900 mb-2">What happens next?</h4>
        <ul className="text-sm text-primary-800 space-y-1">
          <li>• Your document will be processed and analyzed</li>
          <li>• AI will generate an automatic summary</li>
          <li>• You can create quizzes from the content</li>
          <li>• Chat with AI about your document</li>
        </ul>
      </div>
    </div>
  );
};

export default DocumentUpload;
