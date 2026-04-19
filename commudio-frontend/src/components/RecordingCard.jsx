import { useNavigate } from 'react-router-dom';
import { Clock, TrendingUp, MessageSquare, Loader2 } from 'lucide-react';
import { formatDate, formatDuration, getStatusColor } from '../utils/helpers';

const RecordingCard = ({ recording }) => {
  const navigate = useNavigate();

  const handleClick = () => {
    navigate(`/recordings/${recording.id}`);
  };

  return (
    <div
      onClick={handleClick}
      className="card hover:shadow-md transition-all cursor-pointer group"
    >
      <div className="p-6">
        {/* Header */}
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-900 group-hover:text-primary-600 transition-colors">
            Recording #{recording.id}
          </h3>
          <span className={`badge ${getStatusColor(recording.status)}`}>
            {recording.status}
          </span>
        </div>

        {/* Date */}
        <p className="text-sm text-gray-500 mb-4">
          {formatDate(recording.created_at)}
        </p>

        {/* Metrics */}
        <div className="space-y-2">
          {recording.duration_seconds && (
            <div className="flex items-center text-sm text-gray-600">
              <Clock className="w-4 h-4 mr-2 text-gray-400" />
              <span>Duration: {formatDuration(recording.duration_seconds)}</span>
            </div>
          )}

          {recording.words_per_minute !== null && recording.words_per_minute !== undefined && (
            <div className="flex items-center text-sm text-gray-900 font-medium">
              <TrendingUp className="w-4 h-4 mr-2 text-blue-500" />
              <span>{recording.words_per_minute} WPM</span>
            </div>
          )}

          {recording.filler_word_count !== null && recording.filler_word_count !== undefined && (
            <div className="flex items-center text-sm text-gray-900 font-medium">
              <MessageSquare className="w-4 h-4 mr-2 text-orange-500" />
              <span>{recording.filler_word_count} filler words</span>
            </div>
          )}

          {recording.status === 'processing' && (
            <div className="flex items-center text-sm text-gray-500 italic">
              <Loader2 className="w-4 h-4 mr-2 animate-spin" />
              <span>Processing...</span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default RecordingCard;