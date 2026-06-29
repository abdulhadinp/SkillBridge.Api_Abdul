import axios from 'axios';

// Base configuration
const baseURL = 'http://localhost:5092';

// Public API (No token needed)
export const publicApi = axios.create({
  baseURL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Private API (With JWT token)
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