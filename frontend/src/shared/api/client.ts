import axios from 'axios';
import { env } from '@/config'; // Assuming you have an env setup for this

// Note: If you don't have a sophisticated `env` setup,
// you can directly use the Vite environment variable like this:
// const baseURL = import.meta.env.VITE_API_BASE_URL;

export const apiClient = axios.create({
  baseURL: env.VITE_API_BASE_URL,
});