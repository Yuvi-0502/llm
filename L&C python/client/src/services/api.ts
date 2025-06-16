import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add a request interceptor to add the auth token to requests
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

// Add a response interceptor to handle errors
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

export const authAPI = {
  login: (email: string, password: string) =>
    api.post('/auth/login', { email, password }),
  signup: (username: string, email: string, password: string) =>
    api.post('/auth/signup', { username, email, password }),
};

export const newsAPI = {
  getNews: (category?: string) =>
    api.get('/news', { params: { category } }),
  searchNews: (query: string) =>
    api.get('/news/search', { params: { query } }),
  saveArticle: (articleId: number) =>
    api.post(`/news/${articleId}/save`),
  getSavedArticles: () =>
    api.get('/news/saved'),
};

export const adminAPI = {
  getExternalServers: () =>
    api.get('/admin/external-servers'),
  createExternalServer: (data: any) =>
    api.post('/admin/external-servers', data),
  updateExternalServer: (id: number, data: any) =>
    api.put(`/admin/external-servers/${id}`, data),
  deleteExternalServer: (id: number) =>
    api.delete(`/admin/external-servers/${id}`),
};

export const notificationAPI = {
  getPreferences: () =>
    api.get('/notifications/preferences'),
  updatePreferences: (data: any) =>
    api.put('/notifications/preferences', data),
};

export default api; 