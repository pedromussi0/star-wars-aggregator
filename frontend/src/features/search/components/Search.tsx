import React, { useState } from 'react';
import { useSearch } from '../api/useSearch'; 
import { SearchResultItemCard } from './SearchResultItemCard'; 
import { type SearchParams } from '../types';

export const SearchFeature = () => {
  const [query, setQuery] = useState('skywalker'); 
  
  const [searchParams, setSearchParams] = useState<SearchParams>({ q: 'skywalker', limit: 10 });

  const { data, isLoading, isError, error } = useSearch(searchParams);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    setSearchParams({ ...searchParams, q: query });
  };

  return (
    <div className="p-4 max-w-2xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">SWAPI Unified Search</h1>
      <form onSubmit={handleSearch} className="flex gap-2 mb-4">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search for 'skywalker', 'tatooine', etc..."
          className="border p-2 rounded w-full focus:ring-2 focus:ring-blue-500 focus:outline-none"
        />
        <button
          type="submit"
          disabled={isLoading}
          className="bg-blue-500 text-white p-2 rounded hover:bg-blue-600 disabled:bg-gray-400"
        >
          {isLoading ? 'Searching...' : 'Search'}
        </button>
      </form>

      {isError && <p className="text-red-500">Error: {error.message}</p>}

      {data && (
        <div>
          <h2 className="text-xl font-semibold">
            Results ({data.count})
          </h2>
          <ul className="border rounded mt-2">
            {data.results.map((item) => (
              <SearchResultItemCard key={item.url} item={item} />
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};