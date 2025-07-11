import { ListPageTemplate } from '@/shared/components/pages/ListPageTemplate';
import { PersonList } from '../components/PersonList';

export function PeopleListPage() {
  return (
    <ListPageTemplate title="People">
      <PersonList />
    </ListPageTemplate>
  );
} 