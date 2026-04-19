import { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { Upload, FileAudio, CheckCircle, XCircle } from 'lucide-react';
import Navbar from '../components/Navbar';
import { recordingsAPI } from '../api/axios';
import { isValidAudioFile, isValidFileSize } from '../utils/helpers';

const UploadPage = () => {
  const navigate = useNavigate();
  const fileInputRef = useRef(null);

  const [selectedFile, setSelectedFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [status, setStatus] = useState('idle'); // idle, success, error
  const [errorMessage, setErrorMessage] = useState('');
  const [recordingId, setRecordingId] = useState(null);

  const handleFileSelect = (e) => {
    const file = e.target.files?.[0];
    if (!file) return;

    // Validate file
    if (!isValidAudioFile(file)) {
      setErrorMessage('Please select a valid audio file (.wav, .mp3, .m4a)');
      setStatus('error');
      return;
    }

    if (!isValidFileSize(file)) {
      setErrorMessage('File size must be less than 25MB');
      setStatus('error');
      return;
    }

    setSelectedFile(file);
    setStatus('idle');
    setErrorMessage('');
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    setUploading(true);
    setStatus('idle');
    setErrorMessage('');

    try {
      const response = await recordingsAPI.upload(selectedFile);
      setRecordingId(response.recording_id);
      setStatus('success');

      // Redirect after 2 seconds
      setTimeout(() => {
        navigate('/');
      }, 2000);
    } catch (err) {
      setErrorMessage(err.response?.data?.detail || 'Failed to upload file');
      setStatus('error');
    } finally {
      setUploading(false);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const file = e.dataTransfer.files?.[0];
    if (file) {
      const input = fileInputRef.current;
      if (input) {
        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(file);
        input.files = dataTransfer.files;
        handleFileSelect({ target: input });
      }
    }
  };

  const handleClear = () => {
    setSelectedFile(null);
    setStatus('idle');
    setErrorMessage('');
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />

      <div className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Upload Recording</h1>
          <p className="mt-2 text-gray-600">
            Upload an audio file to analyze your speech patterns
          </p>
        </div>

        {/* Upload Card */}
        <div className="card">
          <div className="p-6 space-y-6">
            {/* File Input Info */}
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-1">
                Select Audio File
              </h3>
              <p className="text-sm text-gray-600">
                Supported formats: WAV, MP3, M4A (max 25MB)
              </p>
            </div>

            {/* Drop Zone */}
            <div
              onDragOver={handleDragOver}
              onDrop={handleDrop}
              onClick={() => fileInputRef.current?.click()}
              className="border-2 border-dashed border-gray-300 rounded-xl p-12 text-center cursor-pointer hover:border-primary-400 hover:bg-primary-50/30 transition-all"
            >
              <input
                ref={fileInputRef}
                type="file"
                accept=".wav,.mp3,.m4a,.mp4,audio/*"
                onChange={handleFileSelect}
                className="hidden"
              />

              <Upload className="w-12 h-12 text-gray-400 mx-auto mb-4" />

              {selectedFile ? (
                <div className="space-y-2">
                  <FileAudio className="w-8 h-8 text-primary-600 mx-auto" />
                  <p className="font-medium text-gray-900">{selectedFile.name}</p>
                  <p className="text-sm text-gray-600">
                    {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                  </p>
                </div>
              ) : (
                <div>
                  <p className="text-lg font-medium text-gray-900 mb-2">
                    Drag & drop your audio file here
                  </p>
                  <p className="text-sm text-gray-600">or click to browse</p>
                </div>
              )}
            </div>

            {/* Status Messages */}
            {status === 'success' && (
              <div className="flex items-center gap-3 p-4 bg-green-50 border border-green-200 rounded-lg">
                <CheckCircle className="w-5 h-5 text-green-600 flex-shrink-0" />
                <div className="flex-1">
                  <p className="font-medium text-green-900">Upload successful!</p>
                  <p className="text-sm text-green-700">
                    Recording #{recordingId} is being processed. Redirecting...
                  </p>
                </div>
              </div>
            )}

            {status === 'error' && (
              <div className="flex items-center gap-3 p-4 bg-red-50 border border-red-200 rounded-lg">
                <XCircle className="w-5 h-5 text-red-600 flex-shrink-0" />
                <div className="flex-1">
                  <p className="font-medium text-red-900">Upload failed</p>
                  <p className="text-sm text-red-700">{errorMessage}</p>
                </div>
              </div>
            )}

            {/* Actions */}
            <div className="flex gap-3">
              <button
                onClick={handleUpload}
                disabled={!selectedFile || uploading}
                className="btn-primary flex-1"
              >
                {uploading ? 'Uploading...' : 'Upload & Analyze'}
              </button>

              {selectedFile && !uploading && (
                <button onClick={handleClear} className="btn-secondary">
                  Clear
                </button>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default UploadPage;