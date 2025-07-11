import { useSearchParams } from 'react-router-dom';
import { useResources, type Resource } from '../api/useResources';
import { useResourceFilters } from '../hooks/useResourceFilters';
import { CategoryTabs } from '../components/CategoryTabs';
import { FilterPanel } from '../components/FilterPanel';
import { ResourceCard } from '../components/ResourceCard';
import { Pagination } from '@/shared/ui/Pagination';
import { LoadingSpinner } from '@/shared/ui/LoadingSpinner';
import { ErrorMessage } from '@/shared/ui/ErrorMessage';

export function BrowsePage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const { data, isLoading, isError, error, category, page, totalPages, filters } = useResources();
  const availableFilters = useResourceFilters(category);

  // --- Event Handlers to Update URL State ---
  const handleCategorySelect = (newCategory: string) => {
    setSearchParams({ category: newCategory, page: '1' });
  };

  const handleFilterChange = (name: string, value: string) => {
    const newParams = new URLSearchParams(searchParams);
    if (value) {
      newParams.set(name, value);
    } else {
      newParams.delete(name);
    }
    newParams.set('page', '1');
    setSearchParams(newParams);
  };

  const handlePageChange = (newPage: number) => {
    const newParams = new URLSearchParams(searchParams);
    newParams.set('page', String(newPage));
    setSearchParams(newParams);
  };

  return (
    <div>
      <h1 className="text-3xl font-bold text-yellow-400 mb-4">Browse Resources</h1>
      <CategoryTabs activeCategory={category} onSelectCategory={handleCategorySelect} />
      <FilterPanel
        availableFilters={availableFilters}
        activeFilters={filters}
        onFilterChange={handleFilterChange}
      />

      {isLoading && <LoadingSpinner text={`Loading ${category}...`} />}
      {isError && <ErrorMessage message={error.message} />}

      {!isLoading && !isError && data && (
        <>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {data.results.map((resource: Resource) => (
              <ResourceCard key={resource.url} resource={resource} category={category} />
            ))}
          </div>
          <Pagination
            currentPage={page}
            totalPages={totalPages}
            onPageChange={handlePageChange}
          />
        </>
      )}
    </div>
  );
}