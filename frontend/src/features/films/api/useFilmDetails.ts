import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/shared/api/client';
import type { FilmDetails } from '../types';

const fetchFilmDetails = async (id: string): Promise<FilmDetails> => {
  const { data } = await apiClient.get(`/films/${id}`);
  return data;
};

export function useFilmDetails(id: string) {
  return useQuery({
    queryKey: ['film', id],
    queryFn: () => fetchFilmDetails(id),
    enabled: !!id,
  });
}