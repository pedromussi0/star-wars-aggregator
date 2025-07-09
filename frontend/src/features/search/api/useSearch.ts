import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/axios';
import { type SearchApiResponse, type SearchParams } from '../types';

const searchSwapi = async (params: SearchParams): Promise<SearchApiResponse> => {
  const { data } = await apiClient.get('/search', { params }); 
  return data;
};

export const useSearch = (params: SearchParams) => {
  return useQuery({

    queryKey: ['search', params],
    queryFn: () => searchSwapi(params),
    enabled: !!params.q,
  });
};