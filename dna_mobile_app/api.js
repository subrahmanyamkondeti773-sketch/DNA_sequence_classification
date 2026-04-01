import axios from 'axios';
import * as SecureStore from 'expo-secure-store';

const BASE_URL = 'http://10.132.105.52:8000'; // Updated to machine's LAN IP for physical device testing

const api = axios.create({
    baseURL: BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Interceptor to add token to requests
api.interceptors.request.use(async (config) => {
    const token = await SecureStore.getItemAsync('userToken');
    if (token) {
        config.headers.Authorization = `Token ${token}`;
    }
    return config;
});

export const authApi = {
    login: async (username, password) => {
        const response = await api.post('/api/login/', { username, password });
        if (response.data.token) {
            await SecureStore.setItemAsync('userToken', response.data.token);
            await SecureStore.setItemAsync('userData', JSON.stringify(response.data.user));
        }
        return response.data;
    },
    logout: async () => {
        await SecureStore.deleteItemAsync('userToken');
        await SecureStore.deleteItemAsync('userData');
    },
    register: async (userData) => {
        const response = await api.post('/api/register/', userData);
        if (response.data.token) {
            await SecureStore.setItemAsync('userToken', response.data.token);
            await SecureStore.setItemAsync('userData', JSON.stringify(response.data.user));
        }
        return response.data;
    }
};

export const dnaApi = {
    getStats: async () => {
        const response = await api.get('/api/stats/');
        return response.data;
    },
    classify: async (sequence) => {
        const response = await api.post('/api/classify/', { sequence });
        return response.data;
    },
    getHistory: async () => {
        const response = await api.get('/api/history/');
        return response.data;
    }
};

export default api;
