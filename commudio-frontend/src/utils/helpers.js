// Format date to readable string
export const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
};

// Format duration in seconds to MM:SS
export const formatDuration = (seconds) => {
  if (!seconds) return 'N/A';
  const mins = Math.floor(seconds / 60);
  const secs = Math.floor(seconds % 60);
  return `${mins}:${secs.toString().padStart(2, '0')}`;
};

// Get status badge color
export const getStatusColor = (status) => {
  const colors = {
    completed: 'badge-success',
    processing: 'badge-warning',
    failed: 'badge-error',
  };
  return colors[status] || 'badge-warning';
};

// Validate file type
export const isValidAudioFile = (file) => {
  const validTypes = ['audio/wav', 'audio/mpeg', 'audio/mp4', 'audio/x-m4a'];
  const validExtensions = ['.wav', '.mp3', '.m4a', '.mp4'];
  
  const extension = file.name.toLowerCase().slice(file.name.lastIndexOf('.'));
  return validTypes.includes(file.type) || validExtensions.includes(extension);
};

// Validate file size (max 25MB)
export const isValidFileSize = (file, maxSizeMB = 25) => {
  const maxSize = maxSizeMB * 1024 * 1024;
  return file.size <= maxSize;
};