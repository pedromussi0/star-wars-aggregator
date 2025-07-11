import { useMemo } from 'react';

// Defines the shape of a filter that our UI can render
export interface FilterDefinition {
  name: string; 
  label: string; 
}

// A map of resource categories to their available filters
const filterConfig: Record<string, FilterDefinition[]> = {
  films: [
    { name: 'director', label: 'Director' },
    { name: 'producer', label: 'Producer' },
  ],
  people: [
    { name: 'name', label: 'Name' },
    { name: 'gender', label: 'Gender' },
  ],
  planets: [
    { name: 'name', label: 'Name' },
    { name: 'climate', label: 'Climate' },
    { name: 'terrain', label: 'Terrain' },
  ],
  species: [
    { name: 'name', label: 'Name' },
    { name: 'classification', label: 'Classification' },
    { name: 'language', label: 'Language' },
  ],
  starships: [
    { name: 'name', label: 'Name' },
    { name: 'manufacturer', label: 'Manufacturer' },
    { name: 'starship_class', label: 'Starship Class' },
  ],
  vehicles: [
    { name: 'name', label: 'Name' },
    { name: 'manufacturer', label: 'Manufacturer' },
    { name: 'vehicle_class', label: 'Vehicle Class' },
  ],
};

export const availableCategories = Object.keys(filterConfig);

// A simple hook to retrieve the filter definitions for a given category
export function useResourceFilters(category: string) {
  return useMemo(() => filterConfig[category] || [], [category]);
}