import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/shared/api/client';
import type { PersonDetails } from '../types';

const fetchPersonDetails = async (id: string): Promise<PersonDetails> => {
  const { data } = await apiClient.get(`/people/${id}`);
  return data;
};

export function usePersonDetails(id: string) {
  return useQuery({
    queryKey: ['person', id],
    queryFn: () => fetchPersonDetails(id),
    enabled: !!id,
  });
} 