import { useRoutes } from 'react-router-dom';
import { SearchFeature } from '@/features/search/components/Search';

export const AppRouter = () => {
  const routes = useRoutes([
    { path: '/', element: <SearchFeature /> },
  ]);

  return routes;
};