import axios from 'axios';
import { env } from '@/config'; 

export const apiClient = axios.create({
  baseURL: env.VITE_API_BASE_URL,
});