import axios from 'axios';

// Cambia la IP y el puerto según tu configuración local
const API_URL = process.env.EXPO_PUBLIC_API_URL; // backend Spring Boot
const PYTHON_URL = process.env.EXPO_PUBLIC_PYTHON_URL; // microservicio Python

// Instancia para Spring Boot
export const springApi = axios.create({
  baseURL: API_URL,
  headers: { 'Content-Type': 'application/json' }
});

// Instancia para Python
export const pythonApi = axios.create({
  baseURL: PYTHON_URL,
  headers: { 'Content-Type': 'multipart/form-data' }
});

export default springApi;