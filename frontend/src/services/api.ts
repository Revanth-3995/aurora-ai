import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
});

export const sendChatMessage = async (message: string) => {
  const response = await api.post('/chat', { message });
  return response.data;
};

export const performResearch = async (query: string, maxResults: number = 5, saveToMemory: boolean = false) => {
  const response = await api.post('/research', { query, max_results: maxResults, save_to_memory: saveToMemory });
  return response.data;
};

export const uploadDocument = async (file: File) => {
  const formData = new FormData();
  formData.append('file', file);
  const response = await api.post('/documents/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return response.data;
};

export const askDocument = async (question: string) => {
  const response = await api.post('/documents/ask', { question });
  return response.data;
};

export const scheduleEvent = async (title: string, date: string, time: string, description: string = '') => {
  const response = await api.post('/calendar', { title, date, time, description });
  return response.data;
};

export const getAnalytics = async () => {
  const response = await api.get('/analytics');
  return response.data;
};

export const getWorkflowHistory = async () => {
  const response = await api.get('/analytics/workflow-history');
  return response.data;
};
