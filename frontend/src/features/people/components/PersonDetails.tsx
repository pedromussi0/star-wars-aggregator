import { useParams } from 'react-router-dom';
import { usePersonDetails } from '../api/usePersonDetails';
import { LoadingSpinner } from '@/shared/ui/LoadingSpinner';
import { ErrorMessage } from '@/shared/ui/ErrorMessage';
import { StatPill } from '@/shared/ui/StatPill';
import { extractIdFromUrl } from '@/shared/lib/utils';

export function PersonDetails() {
  const { id } = useParams<{ id: string }>();
  const { data: person, isLoading, isError, error } = usePersonDetails(id!);

  if (isLoading) {
    return <LoadingSpinner />;
  }

  if (isError) {
    return <ErrorMessage message={error.message} />;
  }

  if (!person) {
    return <ErrorMessage message="Person not found." />;
  }

  const renderRelationshipList = (
    title: string,
    items: { url: string; name?: string; title?: string }[],
    basePath: string
  ) => (
    <div>
      <h3 className="text-lg font-semibold text-gray-300 mt-4 mb-2">{title}</h3>
      <div className="flex flex-wrap">
        {items.map((item) => (
          <StatPill
            key={item.url}
            to={`/${basePath}/${extractIdFromUrl(item.url)}`}
          >
            {item.name || item.title}
          </StatPill>
        ))}
      </div>
    </div>
  );

  return (
    <div className="bg-gray-800 rounded-lg shadow-lg p-6 md:p-8">
      <div className="text-center">
        <h1 className="text-4xl font-extrabold text-yellow-400 tracking-wider">
          {person.name}
        </h1>
      </div>

      <div className="border-t border-gray-700 my-6"></div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-4">
        <div>
          <strong className="text-gray-400">Height:</strong> {person.height} cm
        </div>
        <div>
          <strong className="text-gray-400">Mass:</strong> {person.mass} kg
        </div>
        <div>
          <strong className="text-gray-400">Gender:</strong> {person.gender}
        </div>
        {person.homeworld && (
          <div>
            <strong className="text-gray-400">Homeworld:</strong>{' '}
            <StatPill to={`/planets/${extractIdFromUrl(person.homeworld.url)}`}>
              {person.homeworld.name}
            </StatPill>
          </div>
        )}
      </div>

      <div className="border-t border-gray-700 my-6"></div>

      {renderRelationshipList('Films', person.films, 'films')}
      {renderRelationshipList('Species', person.species, 'species')}
      {renderRelationshipList('Vehicles', person.vehicles, 'vehicles')}
      {renderRelationshipList('Starships', person.starships, 'starships')}
    </div>
  );
} 