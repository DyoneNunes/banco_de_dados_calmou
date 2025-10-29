import axios from 'axios';
import { DeviceEventEmitter } from 'react-native';

const IP_BACKEND = '192.168.18.166'; //casa do Dyone
//const IP_BACKEND = '192.168.27.119'; //Trabalho do Dyone
//const IP_BACKEND = '10.10.72.199'; //Trabalho do Dyone
//const IP_BACKEND = '10.10.76.84'; //Faesa nat
//const IP_BACKEND = '10.199.139.123'; //Faesa
const PORTA_BACKEND = '5001';

const api = axios.create({
  baseURL: `http://${IP_BACKEND}:${PORTA_BACKEND}`,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  }
});

// Interceptor para adicionar token JWT e debug de requisições
api.interceptors.request.use(
  async (config) => {
    console.log('🌐 [API] Requisição:', config.method?.toUpperCase(), config.url);
    console.log('📦 [API] Dados enviados:', JSON.stringify(config.data));

    // Adiciona token JWT se existir
    try {
      const { getItemAsync } = await import('expo-secure-store');
      const token = await getItemAsync('access_token');

      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
        console.log('🔑 [API] Token JWT adicionado à requisição');
      }
    } catch (error) {
      console.warn('⚠️ [API] Não foi possível carregar token JWT:', error);
    }

    return config;
  },
  (error) => {
    console.error('❌ [API] Erro ao configurar requisição:', error);
    return Promise.reject(error);
  }
);

// Interceptor para debug de respostas e tratamento de token expirado
api.interceptors.response.use(
  (response) => {
    console.log('✅ [API] Resposta recebida:', response.status, response.config.url);
    console.log('📦 [API] Dados da resposta:', JSON.stringify(response.data));
    return response;
  },
  async (error) => {
    if (error.response) {
      console.error('❌ [API] Erro HTTP:', error.response.status, error.response.config.url);
      console.error('📦 [API] Dados do erro:', JSON.stringify(error.response.data));

      // Detecta token expirado ou inválido
      if (error.response.status === 401) {
        const errorData = error.response.data;

        if (errorData?.error === 'token_expired' || errorData?.error === 'token_invalid') {
          console.warn('🔓 [API] Token expirado/inválido - fazendo logout automático');

          // Limpa os tokens armazenados
          try {
            const { deleteItemAsync } = await import('expo-secure-store');
            await deleteItemAsync('access_token');
            await deleteItemAsync('user');
            console.log('🗑️ [API] Tokens removidos do armazenamento');
          } catch (cleanupError) {
            console.error('❌ [API] Erro ao limpar tokens:', cleanupError);
          }

          // Emite evento usando DeviceEventEmitter do React Native
          DeviceEventEmitter.emit('token-expired');
        }
      }
    } else if (error.request) {
      console.error('❌ [API] Erro de rede - sem resposta do servidor');
      console.error('🔗 [API] URL tentada:', error.config?.url);
    } else {
      console.error('❌ [API] Erro:', error.message);
    }
    return Promise.reject(error);
  }
);

export default api;
