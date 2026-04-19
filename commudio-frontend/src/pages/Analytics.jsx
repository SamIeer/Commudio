import { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { TrendingUp, MessageSquare, Clock, FileAudio } from 'lucide-react';
import Navbar from '../components/Navbar';
import Loader from '../components/Loader';
import { statsAPI } from '../api/axios';

const Analytics = () => {
  const [stats, setStats] = useState(null);
  const [trend, setTrend] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [statsData, trendData] = await Promise.all([
        statsAPI.getSummary(),
        statsAPI.getTrend(),
      ]);
      setStats(statsData);
      setTrend(trendData);
    } catch (err) {
      console.error('Failed to fetch analytics:', err);
    } finally {
      setLoading(false);
    }
  };

  // Prepare chart data
  const chartData = trend?.trend.map(point => ({
    date: new Date(point.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
    wpm: point.wpm,
    fillers: point.filler_count,
  })) || [];

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <Loader size="lg" text="Loading analytics..." />
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Analytics Dashboard</h1>
          <p className="mt-2 text-gray-600">
            Track your progress and communication improvements
          </p>
        </div>

        {/* Stats Overview */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="card p-6">
            <div className="flex items-center justify-between mb-4">
              <span className="text-sm font-medium text-gray-600">Total Recordings</span>
              <FileAudio className="w-5 h-5 text-gray-400" />
            </div>
            <p className="text-3xl font-bold text-gray-900">{stats?.total_recordings || 0}</p>
            <p className="text-xs text-gray-500 mt-1">
              {stats?.completed_recordings || 0} completed
            </p>
          </div>

          <div className="card p-6">
            <div className="flex items-center justify-between mb-4">
              <span className="text-sm font-medium text-gray-600">Average WPM</span>
              <TrendingUp className="w-5 h-5 text-gray-400" />
            </div>
            <p className="text-3xl font-bold text-gray-900">
              {stats?.average_wpm?.toFixed(1) || '0'}
            </p>
            <p className="text-xs text-gray-500 mt-1">Words per minute</p>
          </div>

          <div className="card p-6">
            <div className="flex items-center justify-between mb-4">
              <span className="text-sm font-medium text-gray-600">Avg. Filler Words</span>
              <MessageSquare className="w-5 h-5 text-gray-400" />
            </div>
            <p className="text-3xl font-bold text-gray-900">
              {stats?.average_filler_count?.toFixed(1) || '0'}
            </p>
            <p className="text-xs text-gray-500 mt-1">Per recording</p>
          </div>

          <div className="card p-6">
            <div className="flex items-center justify-between mb-4">
              <span className="text-sm font-medium text-gray-600">Practice Time</span>
              <Clock className="w-5 h-5 text-gray-400" />
            </div>
            <p className="text-3xl font-bold text-gray-900">
              {stats?.total_practice_time_minutes?.toFixed(0) || '0'}
            </p>
            <p className="text-xs text-gray-500 mt-1">Minutes total</p>
          </div>
        </div>

        {/* Status Breakdown */}
        {stats && (
          <div className="card mb-8">
            <div className="p-6">
              <h2 className="text-xl font-bold text-gray-900 mb-2">Recording Status</h2>
              <p className="text-sm text-gray-600 mb-6">
                Breakdown of your recordings by status
              </p>
              <div className="grid grid-cols-3 gap-4">
                <div className="text-center p-6 bg-green-50 rounded-xl border border-green-100">
                  <p className="text-3xl font-bold text-green-600">
                    {stats.completed_recordings}
                  </p>
                  <p className="text-sm text-gray-600 mt-1">Completed</p>
                </div>
                <div className="text-center p-6 bg-yellow-50 rounded-xl border border-yellow-100">
                  <p className="text-3xl font-bold text-yellow-600">
                    {stats.processing_recordings}
                  </p>
                  <p className="text-sm text-gray-600 mt-1">Processing</p>
                </div>
                <div className="text-center p-6 bg-red-50 rounded-xl border border-red-100">
                  <p className="text-3xl font-bold text-red-600">
                    {stats.failed_recordings}
                  </p>
                  <p className="text-sm text-gray-600 mt-1">Failed</p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Charts */}
        {chartData.length > 0 ? (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* WPM Trend */}
            <div className="card p-6">
              <h2 className="text-xl font-bold text-gray-900 mb-2">Speaking Pace Over Time</h2>
              <p className="text-sm text-gray-600 mb-6">Words per minute trend</p>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                  <XAxis
                    dataKey="date"
                    tick={{ fill: '#6b7280', fontSize: 12 }}
                    stroke="#9ca3af"
                  />
                  <YAxis
                    tick={{ fill: '#6b7280', fontSize: 12 }}
                    stroke="#9ca3af"
                  />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: 'white',
                      border: '1px solid #e5e7eb',
                      borderRadius: '0.5rem',
                    }}
                  />
                  <Legend />
                  <Line
                    type="monotone"
                    dataKey="wpm"
                    stroke="#0284c7"
                    strokeWidth={2}
                    name="WPM"
                    dot={{ fill: '#0284c7', r: 4 }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>

            {/* Filler Words Trend */}
            <div className="card p-6">
              <h2 className="text-xl font-bold text-gray-900 mb-2">Filler Words Over Time</h2>
              <p className="text-sm text-gray-600 mb-6">Track your improvement</p>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                  <XAxis
                    dataKey="date"
                    tick={{ fill: '#6b7280', fontSize: 12 }}
                    stroke="#9ca3af"
                  />
                  <YAxis
                    tick={{ fill: '#6b7280', fontSize: 12 }}
                    stroke="#9ca3af"
                  />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: 'white',
                      border: '1px solid #e5e7eb',
                      borderRadius: '0.5rem',
                    }}
                  />
                  <Legend />
                  <Line
                    type="monotone"
                    dataKey="fillers"
                    stroke="#f59e0b"
                    strokeWidth={2}
                    name="Filler Words"
                    dot={{ fill: '#f59e0b', r: 4 }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>
        ) : (
          <div className="card">
            <div className="p-12 text-center">
              <TrendingUp className="w-16 h-16 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                No trend data yet
              </h3>
              <p className="text-gray-600">
                Complete more recordings to see your progress over time
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Analytics;