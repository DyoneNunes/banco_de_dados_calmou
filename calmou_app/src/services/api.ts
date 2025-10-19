import axios from 'axios';

const IP_BACKEND = '192.168.18.164'; //casa do Dyone
//const IP_BACKEND = '192.168.27.119'; //Trabalho do Dyone
//const IP_BACKEND = '192.168.0.109'; //Trabalho do Dyone
//const IP_BACKEND = '10.10.87.116'; //Faesa
//const IP_BACKEND = '10.199.139.123r'; //Faesa
const PORTA_BACKEND = '5001';

const api = axios.create({
  baseURL: `http://${IP_BACKEND}:${PORTA_BACKEND}`
});

export default api;
