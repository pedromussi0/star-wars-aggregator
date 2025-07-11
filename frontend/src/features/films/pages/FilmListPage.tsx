import { ListPageTemplate } from '@/shared/components/pages/ListPageTemplate';
import { FilmList } from '../components/FilmList';

export function FilmListPage() {
  return (
    <ListPageTemplate title="Films">
      <FilmList />
    </ListPageTemplate>
  );
}