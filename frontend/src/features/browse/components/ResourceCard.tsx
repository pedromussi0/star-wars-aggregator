import { Card } from '@/shared/ui/Card';
import { extractIdFromUrl } from '@/shared/lib/utils';
import type { Resource } from '../api/useResources';

interface ResourceCardProps {
  resource: Resource;
  category: string;
}

// Helper to get primary and secondary details based on category
const getResourceDetails = (resource: Resource, category: string) => {
  const na = 'N/A';
  switch (category) {
    case 'films':
      return {
        primary: `Director: ${resource.director ?? na}`,
        secondary: `Released: ${resource.release_date ?? na}`,
      };
    case 'people':
      return {
        primary: `Birth Year: ${resource.birth_year ?? na}`,
        secondary: `Gender: ${resource.gender ?? na}`,
      };
    case 'planets':
      return {
        primary: `Climate: ${resource.climate ?? na}`,
        secondary: `Terrain: ${resource.terrain ?? na}`,
      };
    case 'species':
      return {
        primary: `Classification: ${resource.classification ?? na}`,
        secondary: `Language: ${resource.language ?? na}`,
      };
    case 'starships':
      return {
        primary: `Model: ${resource.model ?? na}`,
        secondary: `Class: ${resource.starship_class ?? na}`,
      };
    case 'vehicles':
        return {
          primary: `Model: ${resource.model ?? na}`,
          secondary: `Class: ${resource.vehicle_class ?? na}`,
        };
    default:
      return { primary: '', secondary: '' };
  }
};

export function ResourceCard({ resource, category }: ResourceCardProps) {
  const id = extractIdFromUrl(resource.url);
  const potentialTitle = resource.title || resource.name;
  const title = typeof potentialTitle === 'string' ? potentialTitle : 'Untitled Resource';
  const details = getResourceDetails(resource, category);

  return (
    <Card to={`/${category}/${id}`}>
      <Card.Title>{title}</Card.Title>
      <Card.Body>
        <p className="text-gray-400 truncate">{details.primary}</p>
        <p className="text-gray-400 truncate">{details.secondary}</p>
      </Card.Body>
    </Card>
  );
}