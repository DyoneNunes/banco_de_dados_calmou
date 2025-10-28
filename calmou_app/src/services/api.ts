import axios from 'axios';

//const IP_BACKEND = '192.168.18.166'; //casa do Dyone
//const IP_BACKEND = '192.168.27.119'; //Trabalho do Dyone
const IP_BACKEND = '192.168.0.109'; //Trabalho do Dyone
//const IP_BACKEND = '10.10.76.84'; //Faesa nat
//const IP_BACKEND = '10.199.139.123'; //Faesa
const PORTA_BACKEND = '5001';

const api = axios.create({
  baseURL: `http://${IP_BACKEND}:${PORTA_BACKEND}`
});

export default api;
