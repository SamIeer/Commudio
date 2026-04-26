import axios from 'axios';

// Use environment variable or default to backend service name in Docker 
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor - attach token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor - handle 401
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  login: async (email, password) => {
    const formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);

    const response = await axios.post(`${API_BASE_URL}/auth/login`, formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
    return response.data;
  },

  getCurrentUser: async () => {
    const response = await api.get('/user/me');
    return response.data;
  },
};

// Recordings API
export const recordingsAPI = {
  getAll: async () => {
    const response = await api.get('/recordings/', {
      params: { skip: 0, limit: 100 },
    });
    return response.data;
  },

  getById: async (id) => {
    const response = await api.get(`/recordings/${id}`);
    return response.data;
  },

  upload: async (file) => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await api.post('/recordings/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  delete: async (id) => {
    await api.delete(`/recordings/${id}`);
  },
};

// Stats API
export const statsAPI = {
  getSummary: async () => {
    const response = await api.get('/recordings/stats/summary');
    return response.data;
  },

  getTrend: async () => {
    const response = await api.get('/recordings/stats/trend');
    return response.data;
  },
};

export default api;