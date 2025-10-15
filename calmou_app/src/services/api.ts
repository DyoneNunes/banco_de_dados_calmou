import axios from 'axios';

// Endereço IP da máquina onde o backend (Python) está rodando
const IP_BACKEND = '192.168.18.164'; 
const PORTA_BACKEND = '5001';

const api = axios.create({
  baseURL: `http://${IP_BACKEND}:${PORTA_BACKEND}`
});

export default api;