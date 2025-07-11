import { useFilms } from '../api/useFilms';
import { Link } from 'react-router-dom';
import { LoadingSpinner } from '@/shared/ui/LoadingSpinner';
import { ErrorMessage } from '@/shared/ui/ErrorMessage';
import { extractIdFromUrl } from '@/shared/lib/utils';

export function FilmList() {
  const { data, isLoading, isError, error } = useFilms();

  if (isLoading) {
    return <LoadingSpinner />;
  }

  if (isError) {
    return <ErrorMessage message={error.message} />;
  }

  return (
    <div>
      <h1 className="text-3xl font-bold text-yellow-400 mb-6">Films</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {data?.results.map((film) => (
          <Link
            key={film.url}
            to={`/films/${extractIdFromUrl(film.url)}`}
            className="bg-gray-800 rounded-lg shadow-lg p-6 hover:bg-gray-700 transition-all duration-200 transform hover:-translate-y-1"
          >
            <h2 className="text-xl font-bold text-yellow-400">
              Episode {film.episode_id}: {film.title}
            </h2>
            <p className="text-gray-400 mt-2">Directed by: {film.director}</p>
            <p className="text-gray-400">Released: {film.release_date}</p>
          </Link>
        ))}
      </div>
    </div>
  );
}