import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import { AppLayout } from '@/shared/components/layout/AppLayout';
import { FilmDetailsPage } from '@/features/films/pages/FilmDetailsPage';
import { FilmListPage } from '@/features/films/pages/FilmListPage';
import { SearchPage } from '@/features/search/pages/SearchPage'; 
import { PeopleListPage } from '@/features/people/pages/PeopleListPage';
import { PersonDetailsPage } from '@/features/people/pages/PersonDetailsPage';
import { BrowsePage } from '@/features/browse/pages/BrowsePage'; 


const router = createBrowserRouter([
  {
    path: '/',
    element: <AppLayout />,
    children: [
      {
        index: true,
        element: <SearchPage />, 
      },
      {
        path: 'search', 
        element: <SearchPage />,
      },
      {
        path: 'browse', 
        element: <BrowsePage />,
      },
      {
        path: 'films',
        element: <FilmListPage />,
      },
      {
        path: 'films/:id',
        element: <FilmDetailsPage />,
      },
      {
        path: 'people',
        element: <PeopleListPage />,
      },
      {
        path: 'people/:id',
        element: <PersonDetailsPage />,
      },
    ],
  },
]);

export function AppRouter() {
  return <RouterProvider router={router} />;
}