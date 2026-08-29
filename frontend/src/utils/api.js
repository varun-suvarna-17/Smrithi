import axios from 'axios';

// API Base URL
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

// Create axios instance
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle errors
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('auth_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// ==================== AUTH ENDPOINTS ====================
export const authAPI = {
  login: (email, password) =>
    apiClient.post('/auth/login', { username: email, password }),
  logout: () => {
    localStorage.removeItem('auth_token');
  },
};

// ==================== PATIENT ENDPOINTS ====================
export const patientAPI = {
  getProfile: (patientId) =>
    apiClient.get(`/patients/${patientId}`),
  updateProfile: (patientId, data) =>
    apiClient.put(`/patients/${patientId}`, data),
  getAll: () =>
    apiClient.get('/patients'),
};

// ==================== GAME ENDPOINTS ====================
export const gameAPI = {
  getAvailableGames: () =>
    apiClient.get('/games'),
  startGame: (gameId) =>
    apiClient.post(`/games/${gameId}/start`),
  recordAttempt: (patientId, gameId, data) =>
    apiClient.post(`/patients/${patientId}/games/${gameId}`, data),
  getGameHistory: (patientId, gameId) =>
    apiClient.get(`/patients/${patientId}/games/${gameId}/history`),
};

// ==================== PROGRESS ENDPOINTS ====================
export const progressAPI = {
  getProgress: (patientId) =>
    apiClient.get(`/progress/${patientId}`),
  getAnalytics: (patientId) =>
    apiClient.get(`/progress/${patientId}/analytics`),
  getMilestones: (patientId) =>
    apiClient.get(`/progress/${patientId}/milestones`),
};

// ==================== VOICE/TTS ENDPOINTS ====================
export const voiceAPI = {
  textToSpeech: (text, language = 'en') =>
    apiClient.post('/voice/tts', { text, language }, { responseType: 'blob' }),
  synthesizeAndPlay: async (text, language = 'en') => {
    try {
      const response = await voiceAPI.textToSpeech(text, language);
      const audio = new Audio(URL.createObjectURL(response.data));
      await audio.play();
      return audio;
    } catch (error) {
      console.error('Error playing audio:', error);
    }
  },
};

// ==================== REMINDER ENDPOINTS ====================
export const reminderAPI = {
  getReminders: (patientId) =>
    apiClient.get(`/reminders?patient_id=${patientId}`),
  createReminder: (data) =>
    apiClient.post('/reminders', data),
  completeReminder: (reminderId) =>
    apiClient.put(`/reminders/${reminderId}/complete`),
  deleteReminder: (reminderId) =>
    apiClient.delete(`/reminders/${reminderId}`),
};

// ==================== REPORT ENDPOINTS ====================
export const reportAPI = {
  generateReport: (patientId, period = 'weekly') =>
    apiClient.post(`/reports/${patientId}`, { period }),
  getReport: (patientId) =>
    apiClient.get(`/reports/${patientId}`),
  getReportHistory: (patientId) =>
    apiClient.get(`/reports/${patientId}/history`),
};

// ==================== ADAPTIVE ENDPOINTS ====================
export const adaptiveAPI = {
  evaluateDifficulty: (patientId) =>
    apiClient.post(`/adaptive/${patientId}/evaluate`),
  getAdaptiveSettings: (patientId) =>
    apiClient.get(`/adaptive/${patientId}/settings`),
};

// ==================== CAREGIVER ENDPOINTS ====================
export const caregiverAPI = {
  getProfile: () =>
    apiClient.get('/caregivers/profile'),
  getAssignedPatients: () =>
    apiClient.get('/caregivers/patients'),
  getDashboard: () =>
    apiClient.get('/caregivers/dashboard'),
};

// ==================== HELPER FUNCTIONS ====================
export const setAuthToken = (token) => {
  if (token) {
    localStorage.setItem('auth_token', token);
    apiClient.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  }
};

export const getAuthToken = () => {
  return localStorage.getItem('auth_token');
};

export const isAuthenticated = () => {
  return !!getAuthToken();
};

export default apiClient;
