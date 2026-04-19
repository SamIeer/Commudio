import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { MessageSquare, Search, Filter, Trash2 } from 'lucide-react';
import Navbar from '../components/Navbar';
import RecordingCard from '../components/RecordingCard';
import Loader from '../components/Loader';
import { recordingsAPI } from '../api/axios';

const Dashboard = () => {
  const navigate = useNavigate();
  const [recordings, setRecordings] = useState([]);
  const [filteredRecordings, setFilteredRecordings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [deleteConfirm, setDeleteConfirm] = useState(null);
  const [deleting, setDeleting] = useState(false);

  useEffect(() => {
    fetchRecordings();
    
    // Auto-refresh every 10 seconds if there are processing recordings
    const interval = setInterval(() => {
      if (recordings.some(r => r.status === 'processing')) {
        fetchRecordings();
      }
    }, 10000);

    return () => clearInterval(interval);
  }, [recordings]);

  useEffect(() => {
    // Apply filters
    let filtered = recordings;

    // Filter by status
    if (statusFilter !== 'all') {
      filtered = filtered.filter(r => r.status === statusFilter);
    }

    // Filter by search query
    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase();
      filtered = filtered.filter(r => 
        r.id.toString().includes(query) ||
        (r.transcript && r.transcript.toLowerCase().includes(query)) ||
        (r.original_filename && r.original_filename.toLowerCase().includes(query))
      );
    }

    setFilteredRecordings(filtered);
  }, [recordings, searchQuery, statusFilter]);

  const fetchRecordings = async () => {
    try {
      const data = await recordingsAPI.getAll();
      setRecordings(data.recordings || []);
    } catch (err) {
      setError('Failed to load recordings');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    setDeleting(true);
    try {
      await recordingsAPI.delete(id);
      setRecordings(recordings.filter(r => r.id !== id));
      setDeleteConfirm(null);
    } catch (err) {
      setError('Failed to delete recording');
      console.error(err);
    } finally {
      setDeleting(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Your Recordings</h1>
          <p className="mt-2 text-gray-600">
            Track your progress and view analysis results
          </p>
        </div>

        {/* Search & Filter Bar */}
        <div className="mb-6 flex flex-col sm:flex-row gap-4">
          {/* Search */}
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input
              type="text"
              placeholder="Search recordings by ID, filename, or transcript..."
              className="input pl-10"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>

          {/* Status Filter */}
          <div className="flex items-center gap-2">
            <Filter className="w-5 h-5 text-gray-400" />
            <select
              className="input w-auto"
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
            >
              <option value="all">All Status</option>
              <option value="completed">Completed</option>
              <option value="processing">Processing</option>
              <option value="failed">Failed</option>
            </select>
          </div>
        </div>

        {/* Results Count */}
        {!loading && (
          <div className="mb-4 text-sm text-gray-600">
            Showing {filteredRecordings.length} of {recordings.length} recording(s)
          </div>
        )}

        {/* Error Message */}
        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg text-red-800">
            {error}
          </div>
        )}

        {/* Loading State */}
        {loading ? (
          <Loader size="lg" text="Loading recordings..." />
        ) : filteredRecordings.length === 0 ? (
          /* Empty State */
          <div className="card">
            <div className="p-12 text-center">
              <MessageSquare className="w-16 h-16 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                {searchQuery || statusFilter !== 'all' ? 'No matching recordings' : 'No recordings yet'}
              </h3>
              <p className="text-gray-600 mb-6">
                {searchQuery || statusFilter !== 'all' 
                  ? 'Try adjusting your search or filters' 
                  : 'Upload your first audio recording to get started'}
              </p>
              {!searchQuery && statusFilter === 'all' && (
                <button
                  onClick={() => navigate('/upload')}
                  className="btn-primary"
                >
                  Upload Recording
                </button>
              )}
            </div>
          </div>
        ) : (
          /* Recordings Grid */
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredRecordings.map((recording) => (
              <div key={recording.id} className="relative group">
                <RecordingCard recording={recording} />
                
                {/* Delete Button Overlay */}
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    setDeleteConfirm(recording.id);
                  }}
                  className="absolute top-4 right-4 p-2 bg-white rounded-lg shadow-md opacity-0 group-hover:opacity-100 transition-opacity hover:bg-red-50"
                  title="Delete recording"
                >
                  <Trash2 className="w-4 h-4 text-red-600" />
                </button>
              </div>
            ))}
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
                  Are you sure you want to delete Recording #{deleteConfirm}? This action cannot be undone.
                </p>
                <div className="flex gap-3">
                  <button
                    onClick={() => handleDelete(deleteConfirm)}
                    className="btn-primary bg-red-600 hover:bg-red-700 flex-1"
                    disabled={deleting}
                  >
                    {deleting ? 'Deleting...' : 'Yes, Delete'}
                  </button>
                  <button
                    onClick={() => setDeleteConfirm(null)}
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

export default Dashboard;