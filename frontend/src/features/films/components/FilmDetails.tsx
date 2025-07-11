import { useParams } from 'react-router-dom';
import { useFilmDetails } from '../api/useFilmDetails';
import { LoadingSpinner } from '@/shared/ui/LoadingSpinner';
import { ErrorMessage } from '@/shared/ui/ErrorMessage';
import { StatPill } from '@/shared/ui/StatPill';
import { extractIdFromUrl } from '@/shared/lib/utils';

export function FilmDetails() {
  const { id } = useParams<{ id: string }>();
  const { data: film, isLoading, isError, error } = useFilmDetails(id!);

  if (isLoading) {
    return <LoadingSpinner />;
  }

  if (isError) {
    return <ErrorMessage message={error.message} />;
  }

  if (!film) {
    return <ErrorMessage message="Film not found." />;
  }

  const renderRelationshipList = (
    title: string,
    items: { url: string; name?: string; title?: string }[]
  ) => (
    <div>
      <h3 className="text-lg font-semibold text-gray-300 mt-4 mb-2">{title}</h3>
      <div className="flex flex-wrap">
        {items.map((item) => (
          <StatPill
            key={item.url}
            to={`/${item.url.split('/')[4]}/${extractIdFromUrl(item.url)}`}
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
          {film.title}
        </h1>
        <p className="text-lg text-gray-400 mt-1">Episode {film.episode_id}</p>
      </div>

      <div className="border-t border-gray-700 my-6"></div>

      <div className="max-w-2xl mx-auto">
        <h2 className="text-2xl font-bold text-yellow-300 mb-4 font-serif italic text-center">
          Opening Crawl
        </h2>
        <p className="text-lg leading-relaxed text-yellow-200 whitespace-pre-wrap">
          {film.opening_crawl}
        </p>
      </div>

      <div className="border-t border-gray-700 my-6"></div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-4">
        <div>
          <strong className="text-gray-400">Director:</strong> {film.director}
        </div>
        <div>
          <strong className="text-gray-400">Producer:</strong> {film.producer}
        </div>
        <div>
          <strong className="text-gray-400">Release Date:</strong> {film.release_date}
        </div>
      </div>

      <div className="border-t border-gray-700 my-6"></div>

      {renderRelationshipList('Characters', film.characters)}
      {renderRelationshipList('Planets', film.planets)}
      {renderRelationshipList('Starships', film.starships)}
      {renderRelationshipList('Vehicles', film.vehicles)}
      {renderRelationshipList('Species', film.species)}
    </div>
  );
}