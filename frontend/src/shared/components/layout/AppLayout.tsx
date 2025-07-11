import { Outlet } from 'react-router-dom';
import { SearchBar } from '@/features/search/components/SearchBar';

export function AppLayout() {
  return (
    <div className="min-h-screen bg-gray-900 text-white font-sans">
      <header className="bg-gray-800 border-b border-gray-700 shadow-lg sticky top-0 z-10">
        <nav className="container mx-auto px-4 py-3 flex justify-between items-center">
          <a href="/" className="text-2xl font-bold text-yellow-400">
            Star Wars DB
          </a>
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