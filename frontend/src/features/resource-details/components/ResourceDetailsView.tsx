import type { Resource } from '@/features/browse/api/useResources';
import { StatPill } from '@/shared/ui/StatPill';
import { ErrorMessage } from '@/shared/ui/ErrorMessage';
// --- IMPORT THE CORRECT UTILITY ---
import { getRelativeResourcePath } from '@/shared/lib/utils';

// Configuration to map categories to their display properties
const detailConfig = {
  films: { title: 'title', fields: ['director', 'producer', 'release_date', 'episode_id'], relations: ['characters', 'planets', 'starships', 'vehicles', 'species'] },
  people: { title: 'name', fields: ['birth_year', 'gender', 'height', 'mass', 'hair_color', 'skin_color'], relations: ['films', 'starships', 'vehicles', 'species'] },
  planets: { title: 'name', fields: ['climate', 'terrain', 'population', 'gravity', 'diameter'], relations: ['residents', 'films'] },
  species: { title: 'name', fields: ['classification', 'language', 'average_lifespan'], relations: ['people', 'films'] },
  starships: { title: 'name', fields: ['model', 'manufacturer', 'starship_class', 'cost_in_credits'], relations: ['pilots', 'films'] },
  vehicles: { title: 'name', fields: ['model', 'manufacturer', 'vehicle_class', 'passengers'], relations: ['pilots', 'films'] },
};

type ResourceCategory = keyof typeof detailConfig;

function isValidCategory(category: string): category is ResourceCategory {
  return category in detailConfig;
}

interface ResourceDetailsViewProps {
  resource: Resource;
  category: string;
}

export function ResourceDetailsView({ resource, category }: ResourceDetailsViewProps) {
  if (!isValidCategory(category)) {
    return <ErrorMessage title="Invalid Category" message={`The category "${category}" does not exist.`} />;
  }

  const config = detailConfig[category];

  const renderRelationshipList = (title: string, items: unknown) => {
    if (!Array.isArray(items) || items.length === 0) return null;

    return (
      <div>
        <h3 className="text-xl font-semibold text-gray-300 mt-6 mb-3 border-b border-gray-600 pb-2 capitalize">{title}</h3>
        <div className="flex flex-wrap">
          {items.map((item: { url: string; name?: string; title?: string }) => {
            const relativePath = getRelativeResourcePath(item.url);

            return relativePath ? (
              <StatPill
                key={item.url}
                to={`/browse/${relativePath}`}
              >
                {item.name || item.title}
              </StatPill>
            ) : null;
          })}
        </div>
      </div>
    );
  };

  return (
    <div className="bg-gray-800 rounded-lg shadow-2xl p-6 md:p-8">
      <div className="text-center mb-6">
        <h1 className="text-4xl font-extrabold text-yellow-400 tracking-wider">
          {String(resource[config.title] || 'N/A')}
        </h1>
        <p className="text-gray-500 capitalize">{category.slice(0, -1)}</p>
      </div>

      <div className="border-t border-gray-700 my-6"></div>

      <div className="grid grid-cols-2 md:grid-cols-3 gap-x-8 gap-y-4">
        {config.fields.map(field => (
          <div key={field}>
            <strong className="block text-gray-400 text-sm capitalize">{field.replace('_', ' ')}</strong>
            <span className="text-lg">{String(resource[field] || 'N/A')}</span>
          </div>
        ))}
      </div>

      {config.relations.map(relation =>
        renderRelationshipList(relation, resource[relation])
      )}
    </div>
  );
}