import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

export function SearchBar() {
  const [query, setQuery] = useState('');
  const navigate = useNavigate();

  // This useEffect hook implements the debouncing logic
  useEffect(() => {
    // Wait for 500ms after the user stops typing
    const timerId = setTimeout(() => {
      if (query) {
        // Navigate to a dedicated search page with the query in the URL
        navigate(`/search?q=${encodeURIComponent(query)}`);
      }
    }, 500);

    // This cleanup function clears the timer if the user starts typing again
    return () => {
      clearTimeout(timerId);
    };
  }, [query, navigate]); // Rerun effect only if query or navigate changes

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setQuery(event.target.value);
  };

  return (
    <div className="w-full">
      <input
        type="search"
        placeholder="Search for characters, films, planets..."
        value={query}
        onChange={handleChange}
        className="w-full px-4 py-2 text-gray-200 bg-gray-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-yellow-400 focus:border-transparent"
      />
    </div>
  );
}