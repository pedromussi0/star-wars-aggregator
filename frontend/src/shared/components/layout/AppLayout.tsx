import { Link, Outlet } from 'react-router-dom';
import { SearchBar } from '@/features/search/components/SearchBar';

export function AppLayout() {
  return (
    <div className="min-h-screen bg-gray-900 text-white font-sans">
      <header className="bg-gray-800 border-b border-gray-700 shadow-lg sticky top-0 z-10">
        <nav className="container mx-auto px-4 py-3 flex justify-between items-center gap-4">
          <div className="flex items-center gap-4">
            <Link to="/" className="text-2xl font-bold text-yellow-400">
              Star Wars DB
            </Link>
            <Link
              to="/browse?category=films&page=1"
              className="px-4 py-2 bg-gray-700 text-white font-semibold rounded-lg hover:bg-yellow-500 hover:text-black transition-colors"
            >
              Browse
            </Link>
          </div>
          <div className="w-full max-w-md">
            <SearchBar />
          </div>
        </nav>
      </header>
      <main className="container mx-auto p-4 md:p-6">
        <Outlet />
      </main>
    </div>
  );
}