import { useSearchParams } from 'react-router-dom';
import { useSearch } from '../api/useSearch';
import { SearchResultItemCard } from './SearchResultItemCard';
import { LoadingSpinner } from '@/shared/ui/LoadingSpinner';
import { ErrorMessage } from '@/shared/ui/ErrorMessage';

export function SearchResults() {
  const [searchParams] = useSearchParams();
  const query = searchParams.get('q') || '';

  // Use our powerful, refined useSearch hook
  const { data: results, isLoading, isError, error } = useSearch(query);

  if (isLoading) {
    return <LoadingSpinner text={`Searching for "${query}"...`} />;
  }

  if (isError) {
    return <ErrorMessage message={`Failed to fetch search results: ${error.message}`} />;
  }

  if (!results || results.length === 0) {
    return <p className="text-center text-gray-400">No results found for "{query}".</p>;
  }

  return (
    <div>
      <h2 className="text-2xl font-semibold mb-4 text-gray-300">
        Results for <span className="text-white font-bold">"{query}"</span>
      </h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {results.map((item) => (
          <SearchResultItemCard key={item.url} item={item} />
        ))}
      </div>
    </div>
  );
}