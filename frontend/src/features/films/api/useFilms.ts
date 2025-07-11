import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/shared/api/client';
import type { Film } from '../types';

interface ApiListResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

const fetchFilms = async (): Promise<ApiListResponse<Film>> => {
  const { data } = await apiClient.get('/films');
  return data;
};

export function useFilms() {
  return useQuery({
    queryKey: ['films'],
    queryFn: fetchFilms,
  });
}