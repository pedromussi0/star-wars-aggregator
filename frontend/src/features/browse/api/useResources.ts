import { useQuery, keepPreviousData } from '@tanstack/react-query';
import { useSearchParams } from 'react-router-dom';
import { apiClient } from '@/shared/api/client';
import { availableCategories } from '../hooks/useResourceFilters';

// A generic type for any resource item returned by the list endpoints
export interface Resource {
  url: string;
  [key: string]: unknown; 
}

interface PaginatedApiResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: Resource[];
}

const fetchResources = async (
  category: string,
  params: Record<string, string>,
): Promise<PaginatedApiResponse> => {
  const { data } = await apiClient.get(`/${category}`, { params });
  return data;
};

export function useResources() {
  const [searchParams] = useSearchParams();

  // --- Extract state from URL ---
  const category = searchParams.get('category') || availableCategories[0];
  const page = parseInt(searchParams.get('page') || '1', 10);
  const limit = 10; // Our page size
  const offset = (page - 1) * limit;

  // Extract all other query parameters to use as filters
  const filters: Record<string, string> = {};
  searchParams.forEach((value, key) => {
    if (key !== 'category' && key !== 'page') {
      filters[key] = value;
    }
  });

  // Construct the query parameters for the API call
  const apiParams = {
    ...filters,
    limit: String(limit),
    offset: String(offset),
  };

  // --- Data Fetching with TanStack Query ---
  const queryResult = useQuery({

    queryKey: ['resources', category, apiParams],
    queryFn: () => fetchResources(category, apiParams),
    placeholderData: keepPreviousData,
  });

  // --- Return derived state ---
  const totalPages = Math.ceil((queryResult.data?.count || 0) / limit);

  return {
    ...queryResult,
    data: queryResult.data,
    category,
    page,
    totalPages,
    filters,
  };
}