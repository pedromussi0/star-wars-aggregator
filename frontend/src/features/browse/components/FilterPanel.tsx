import React, { useState, useEffect } from 'react';
import { useDebouncedCallback } from '@/shared/hooks/useDebouncedCallback';
import type { FilterDefinition } from '../hooks/useResourceFilters';

interface FilterPanelProps {
  availableFilters: FilterDefinition[];
  activeFilters: Record<string, string>;
  onFilterChange: (name: string, value: string) => void;
}

export function FilterPanel({
  availableFilters,
  activeFilters,
  onFilterChange,
}: FilterPanelProps) {
  // Use local state for immediate input feedback
  const [localFilters, setLocalFilters] = useState(activeFilters);

  // Debounce the call to update the URL
  const debouncedOnFilterChange = useDebouncedCallback(onFilterChange, 500);

  // Sync local state if the active filters from the URL change
  useEffect(() => {
    setLocalFilters(activeFilters);
  }, [activeFilters]);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setLocalFilters((prev) => ({ ...prev, [name]: value }));
    debouncedOnFilterChange(name, value);
  };

  if (availableFilters.length === 0) {
    return null;
  }

  return (
    <div className="bg-gray-800 p-4 rounded-lg mb-6">
      <h3 className="text-lg font-semibold text-gray-200 mb-3">Filters</h3>
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        {availableFilters.map((filter) => (
          <div key={filter.name}>
            <label htmlFor={filter.name} className="block text-sm font-medium text-gray-400 mb-1">
              {filter.label}
            </label>
            <input
              type="text"
              id={filter.name}
              name={filter.name}
              value={localFilters[filter.name] || ''}
              onChange={handleInputChange}
              className="w-full px-3 py-2 text-gray-200 bg-gray-700 rounded-md focus:outline-none focus:ring-2 focus:ring-yellow-400"
              placeholder={`Filter by ${filter.label}...`}
            />
          </div>
        ))}
      </div>
    </div>
  );
}