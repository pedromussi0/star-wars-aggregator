import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/shared/api/client';
import type { Resource } from '@/features/browse/api/useResources'; 

const fetchResourceDetails = async (
  category: string,
  id: string
): Promise<Resource> => {
  const { data } = await apiClient.get(`/${category}/${id}`);
  return data;
};

export function useResourceDetails(category?: string, id?: string) {
  return useQuery({
    queryKey: ['resource', category, id],
    queryFn: () => fetchResourceDetails(category!, id!),
    // Only run the query if both category and id are present
    enabled: !!category && !!id,
  });
}