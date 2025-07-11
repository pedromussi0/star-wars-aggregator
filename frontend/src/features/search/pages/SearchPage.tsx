import { useSearchParams } from 'react-router-dom';
import { SearchResults } from '../components/SearchResults';

export function SearchPage() {
  const [searchParams] = useSearchParams();
  const hasQuery = searchParams.has('q');

  return (
    <div className="container mx-auto">
      {!hasQuery ? (
        <div className="text-center py-20">
          <h1 className="text-4xl font-bold text-yellow-400">Search the Galaxy</h1>
          <p className="text-lg text-gray-400 mt-2">
            Use the search bar above to find anything in the Star Wars universe.
          </p>
        </div>
      ) : (
        <SearchResults />
      )}
    </div>
  );
}