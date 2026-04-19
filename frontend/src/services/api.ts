import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const getTasks = async (userId: string) => {
  const response = await api.get('/api/tasks');
  return response.data;
};

export const createTask = async (userId: string, task: { title: string; description?: string; priority?: string; due_date?: string }) => {
  const response = await api.post('/api/tasks', task);
  return response.data;
};

export const getTaskById = async (userId: string, taskId: string) => {
  const response = await api.get(`/api/tasks/${taskId}`);
  return response.data;
};

export const updateTask = async (userId: string, taskId: string, task: Partial<{ title: string; description?: string; priority?: string; due_date?: string; is_completed?: boolean }>) => {
  const response = await api.put(`/api/tasks/${taskId}`, task);
  return response.data;
};

export const toggleTaskCompletion = async (userId: string, taskId: string, isCompleted: boolean) => {
  const response = await api.patch(`/api/tasks/${taskId}`, { is_completed: isCompleted });
  return response.data;
};

export const deleteTask = async (userId: string, taskId: string) => {
  await api.delete(`/api/tasks/${taskId}`);
};
