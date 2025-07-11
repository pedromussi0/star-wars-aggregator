import { Link, useSearchParams } from 'react-router-dom';
import { SearchResults } from '../components/SearchResults';

export function SearchPage() {
  const [searchParams] = useSearchParams();
  const hasQuery = searchParams.has('q') && searchParams.get('q') !== '';

  return (
    <div className="container mx-auto">
      {!hasQuery ? (
        <div className="text-center py-20 px-6">
          <h1 className="text-4xl md:text-5xl font-bold text-yellow-400">Search the Galaxy</h1>
          <p className="text-lg text-gray-400 mt-4 max-w-2xl mx-auto">
            Use the search bar above for specific queries or explore categories in depth.
          </p>
          <div className="mt-8">
            <Link
              to="/browse?category=films&page=1"
              className="inline-block bg-yellow-500 text-black font-bold text-lg px-8 py-4 rounded-lg shadow-lg hover:bg-yellow-400 transform hover:-translate-y-1 transition-all"
            >
              Or, Browse All Resources
            </Link>
          </div>
        </div>
      ) : (
        <SearchResults />
      )}
    </div>
  );
}