import { usePeople } from '../api/usePeople';
import { Link } from 'react-router-dom';
import { LoadingSpinner } from '@/shared/ui/LoadingSpinner';
import { ErrorMessage } from '@/shared/ui/ErrorMessage';
import { extractIdFromUrl } from '@/shared/lib/utils';
import type { Person } from '../types';

export function PersonList() {
  const { data, isLoading, isError, error } = usePeople();

  if (isLoading) {
    return <LoadingSpinner />;
  }

  if (isError) {
    return <ErrorMessage message={error.message} />;
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {data?.results.map((person: Person) => (
        <Link
          key={person.url}
          to={`/people/${extractIdFromUrl(person.url)}`}
          className="bg-gray-800 rounded-lg shadow-lg p-6 hover:bg-gray-700 transition-all duration-200 transform hover:-translate-y-1"
        >
          <h2 className="text-xl font-bold text-yellow-400">{person.name}</h2>
          <p className="text-gray-400 mt-2">Gender: {person.gender}</p>
          <p className="text-gray-400">Height: {person.height} cm</p>
          <p className="text-gray-400">Mass: {person.mass} kg</p>
        </Link>
      ))}
    </div>
  );
} 