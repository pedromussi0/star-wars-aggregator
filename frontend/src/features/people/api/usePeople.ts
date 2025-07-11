import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/shared/api/client';
import type { Person } from '../types';

interface ApiListResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

const fetchPeople = async (): Promise<ApiListResponse<Person>> => {
  const { data } = await apiClient.get('/people');
  return data;
};

export function usePeople() {
  return useQuery({
    queryKey: ['people'],
    queryFn: fetchPeople,
  });
} 