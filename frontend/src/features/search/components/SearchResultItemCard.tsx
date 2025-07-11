import { Card } from '@/shared/ui/Card';
import type { UnifiedSearchResult } from '../types';

interface SearchResultItemCardProps {
  item: UnifiedSearchResult;
}

export function SearchResultItemCard({ item }: SearchResultItemCardProps) {
  return (
    <Card to={item.url}>
      <Card.Title>{item.title}</Card.Title>
      <Card.Body>
        <p className="text-sm text-yellow-500 uppercase font-bold tracking-wider mb-2">
          {item.resourceType}
        </p>
        {Object.entries(item.summary).map(([key, value]) => (
          <div key={key} className="text-sm truncate">
            <span className="font-semibold text-gray-400">{key}: </span>
            <span className="text-gray-300">{value}</span>
          </div>
        ))}
      </Card.Body>
    </Card>
  );
}