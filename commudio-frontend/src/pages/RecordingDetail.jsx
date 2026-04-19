import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, Clock, TrendingUp, MessageSquare, CheckCircle2, XCircle, AlertCircle, Edit2, Trash2, Save, X } from 'lucide-react';
import Navbar from '../components/Navbar';
import Loader from '../components/Loader';
import { recordingsAPI } from '../api/axios';
import { formatDate, formatDuration, getStatusColor } from '../utils/helpers';

const RecordingDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();

  const [recording, setRecording] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [isEditing, setIsEditing] = useState(false);
  const [customName, setCustomName] = useState('');
  const [deleteConfirm, setDeleteConfirm] = useState(false);
  const [deleting, setDeleting] = useState(false);

  useEffect(() => {
    fetchRecording();

    // Auto-refresh every 5 seconds if processing
    const interval = setInterval(() => {
      if (recording?.status === 'processing') {
        fetchRecording();
      }
    }, 5000);

    return () => clearInterval(interval);
  }, [id, recording?.status]);

  const fetchRecording = async () => {
    try {
      const data = await recordingsAPI.getById(id);
      setRecording(data);
      setCustomName(data.custom_name || data.original_filename || `Recording #${data.id}`);
    } catch (err) {
      setError('Failed to load recording');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleSaveName = () => {
    // In a real app, you'd call an API to update the name
    // For now, just update locally
    setRecording({ ...recording, custom_name: customName });
    setIsEditing(false);
  };

  const handleDelete = async () => {
    setDeleting(true);
    try {
      await recordingsAPI.delete(id);
      navigate('/');
    } catch (err) {
      setError('Failed to delete recording');
      console.error(err);
    } finally {
      setDeleting(false);
    }
  };

  const getStatusIcon = (status) => {
    const icons = {
      completed: CheckCircle2,
      processing: Loader,
      failed: XCircle,
    };
    return icons[status] || AlertCircle;
  };

  const StatusIcon = recording ? getStatusIcon(recording.status) : null;

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <Loader size="lg" text="Loading recording..." />
        </div>
      </div>
    );
  }

  if (error || !recording) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="card">
            <div className="p-12 text-center">
              <AlertCircle className="w-16 h-16 text-red-500 mx-auto mb-4" />
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                Recording not found
              </h3>
              <p className="text-gray-600 mb-6">{error}</p>
              <button onClick={() => navigate('/')} className="btn-primary">
                Back to Dashboard
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Back Button */}
        <button
          onClick={() => navigate('/')}
          className="flex items-center text-gray-600 hover:text-gray-900 mb-6 transition-colors"
        >
          <ArrowLeft className="w-4 h-4 mr-2" />
          Back to Dashboard
        </button>

        {/* Header with Edit/Delete Actions */}
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-6">
          <div className="flex-1">
            {isEditing ? (
              <div className="flex items-center gap-2">
                <input
                  type="text"
                  value={customName}
                  onChange={(e) => setCustomName(e.target.value)}
                  className="input text-2xl font-bold"
                  autoFocus
                />
                <button
                  onClick={handleSaveName}
                  className="p-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
                  title="Save"
                >
                  <Save className="w-5 h-5" />
                </button>
                <button
                  onClick={() => {
                    setIsEditing(false);
                    setCustomName(recording.custom_name || recording.original_filename || `Recording #${recording.id}`);
                  }}
                  className="p-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors"
                  title="Cancel"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>
            ) : (
              <div className="flex items-center gap-2">
                <h1 className="text-3xl font-bold text-gray-900">
                  {customName}
                </h1>
                <button
                  onClick={() => setIsEditing(true)}
                  className="p-2 text-gray-400 hover:text-gray-600 transition-colors"
                  title="Edit name"
                >
                  <Edit2 className="w-5 h-5" />
                </button>
              </div>
            )}
            <p className="text-gray-600 mt-1">{formatDate(recording.created_at)}</p>
          </div>

          <div className="flex items-center gap-3">
            <span className={`badge flex items-center gap-1 ${getStatusColor(recording.status)}`}>
              {StatusIcon && <StatusIcon className="w-3 h-3" />}
              {recording.status}
            </span>
            <button
              onClick={() => setDeleteConfirm(true)}
              className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
              title="Delete recording"
            >
              <Trash2 className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Metrics Cards */}
        {recording.status === 'completed' && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <div className="card p-6">
              <div className="flex items-center text-gray-600 mb-2">
                <TrendingUp className="w-4 h-4 mr-2" />
                <span className="text-sm font-medium">Words Per Minute</span>
              </div>
              <p className="text-3xl font-bold text-gray-900">
                {recording.words_per_minute || 'N/A'}
              </p>
              <p className="text-xs text-gray-500 mt-1">
                {recording.words_per_minute > 150 ? 'Fast pace' : 
                 recording.words_per_minute > 100 ? 'Good pace' : 'Slow pace'}
              </p>
            </div>

            <div className="card p-6">
              <div className="flex items-center text-gray-600 mb-2">
                <MessageSquare className="w-4 h-4 mr-2" />
                <span className="text-sm font-medium">Filler Words</span>
              </div>
              <p className="text-3xl font-bold text-gray-900">
                {recording.filler_word_count ?? 'N/A'}
              </p>
              <p className="text-xs text-gray-500 mt-1">
                {recording.filler_word_count < 5 ? 'Excellent!' : 
                 recording.filler_word_count < 15 ? 'Good job' : 'Needs work'}
              </p>
            </div>

            <div className="card p-6">
              <div className="flex items-center text-gray-600 mb-2">
                <Clock className="w-4 h-4 mr-2" />
                <span className="text-sm font-medium">Duration</span>
              </div>
              <p className="text-3xl font-bold text-gray-900">
                {recording.duration_seconds ? formatDuration(recording.duration_seconds) : 'N/A'}
              </p>
              <p className="text-xs text-gray-500 mt-1">Recording length</p>
            </div>
          </div>
        )}

        {/* Transcript */}
        {recording.transcript && (
          <div className="card mb-6">
            <div className="p-6">
              <h2 className="text-xl font-bold text-gray-900 mb-2">Transcript</h2>
              <p className="text-sm text-gray-600 mb-4">
                Auto-generated transcription of your recording
              </p>
              <div className="prose max-w-none">
                <p className="text-gray-900 leading-relaxed whitespace-pre-wrap">
                  {recording.transcript}
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Feedback */}
        {recording.feedback_text && (
          <div className="card mb-6">
            <div className="p-6">
              <h2 className="text-xl font-bold text-gray-900 mb-2">AI Feedback</h2>
              <p className="text-sm text-gray-600 mb-4">
                Personalized insights to improve your communication
              </p>
              <div className="space-y-3">
                {recording.feedback_text.split('\n').filter(line => line.trim()).map((line, index) => (
                  <p key={index} className="text-gray-800 leading-relaxed">
                    {line}
                  </p>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Processing State */}
        {recording.status === 'processing' && (
          <div className="card">
            <div className="p-12 text-center">
              <Loader size="lg" />
              <h3 className="text-lg font-semibold text-gray-900 mt-4 mb-2">
                Processing your recording...
              </h3>
              <p className="text-gray-600">
                This usually takes 10-30 seconds. The page will auto-refresh.
              </p>
            </div>
          </div>
        )}

        {/* Failed State */}
        {recording.status === 'failed' && (
          <div className="card border-red-200">
            <div className="p-12 text-center">
              <XCircle className="w-16 h-16 text-red-500 mx-auto mb-4" />
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                Processing failed
              </h3>
              <p className="text-gray-600 mb-6">
                We couldn't process this recording. Please try uploading again.
              </p>
              <button onClick={() => navigate('/upload')} className="btn-primary">
                Upload New Recording
              </button>
            </div>
          </div>
        )}

        {/* Delete Confirmation Modal */}
        {deleteConfirm && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
            <div className="card max-w-md w-full">
              <div className="p-6">
                <h3 className="text-lg font-bold text-gray-900 mb-2">
                  Delete Recording?
                </h3>
                <p className="text-gray-600 mb-6">
                  Are you sure you want to delete "{customName}"? This action cannot be undone.
                </p>
                <div className="flex gap-3">
                  <button
                    onClick={handleDelete}
                    className="btn-primary bg-red-600 hover:bg-red-700 flex-1"
                    disabled={deleting}
                  >
                    {deleting ? 'Deleting...' : 'Yes, Delete'}
                  </button>
                  <button
                    onClick={() => setDeleteConfirm(false)}
                    className="btn-secondary flex-1"
                    disabled={deleting}
                  >
                    Cancel
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default RecordingDetail;