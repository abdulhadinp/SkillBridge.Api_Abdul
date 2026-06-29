import axios from 'axios';

// Base URL — matches ASP.NET Core API in development
const baseURL = 'http://localhost:5092';

// Public API (No token needed)
export const publicApi = axios.create({
  baseURL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Private API (With JWT token) — used for named imports
export const privateApi = axios.create({
  baseURL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Automatically add token to privateApi requests
privateApi.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Default export — single smart instance (auto-attaches token if present)
const api = axios.create({
  baseURL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;