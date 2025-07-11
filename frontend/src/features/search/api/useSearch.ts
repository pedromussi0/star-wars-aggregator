import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/shared/api/client';
import { extractIdFromUrl } from '@/shared/lib/utils';
import type { SearchApiResponse, SearchResultItem, UnifiedSearchResult } from '../types';

const transformToUnifiedResult = (item: SearchResultItem): UnifiedSearchResult => {
  const resourceType = item.type;
  const url = `/browse/${resourceType}/${extractIdFromUrl(item.url)}`;
  let title = '';
  const summary: Record<string, string> = {};

  switch (item.type) {
    case 'films':
      title = item.title;
      summary['Director'] = item.director;
      summary['Release Date'] = item.release_date;
      break;
    case 'people':
      title = item.name;
      summary['Birth Year'] = item.birth_year;
      summary['Gender'] = item.gender;
      break;
    case 'planets':
      title = item.name;
      summary['Climate'] = item.climate;
      summary['Population'] = item.population;
      break;
    case 'species':
      title = item.name;
      summary['Classification'] = item.classification;
      summary['Language'] = item.language;
      break;
    case 'starships':
      title = item.name;
      summary['Model'] = item.model;
      summary['Class'] = item.starship_class;
      break;
    case 'vehicles':
      title = item.name;
      summary['Model'] = item.model;
      summary['Class'] = item.vehicle_class;
      break;
  }

  return { resourceType, title, url, summary };
};

const searchAll = async (query: string): Promise<UnifiedSearchResult[]> => {
  if (!query) return [];
  // The API response is typed with your detailed SearchApiResponse
  const { data } = await apiClient.get<SearchApiResponse>(`/search?q=${query}`);
  // We map over the results and transform each one
  return data.results.map(transformToUnifiedResult);
};

export function useSearch(query: string) {
  return useQuery({
    queryKey: ['search', query],
    queryFn: () => searchAll(query),
    enabled: !!query,
  });
}