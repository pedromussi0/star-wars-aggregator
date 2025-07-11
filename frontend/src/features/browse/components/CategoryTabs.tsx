import { availableCategories } from '../hooks/useResourceFilters';

interface CategoryTabsProps {
  activeCategory: string;
  onSelectCategory: (category: string) => void;
}

export function CategoryTabs({ activeCategory, onSelectCategory }: CategoryTabsProps) {
  return (
    <div className="flex space-x-2 border-b-2 border-gray-700 mb-6 overflow-x-auto pb-2">
      {availableCategories.map((category) => (
        <button
          key={category}
          onClick={() => onSelectCategory(category)}
          className={`px-4 py-2 rounded-t-lg font-semibold capitalize transition-colors whitespace-nowrap ${
            activeCategory === category
              ? 'bg-gray-800 text-yellow-400 border-b-2 border-yellow-400'
              : 'text-gray-400 hover:bg-gray-700 hover:text-white'
          }`}
        >
          {category}
        </button>
      ))}
    </div>
  );
}