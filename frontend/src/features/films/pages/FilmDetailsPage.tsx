import { DetailPageTemplate } from '@/shared/components/pages/DetailPageTemplate';
import { FilmDetails } from '../components/FilmDetails';

export function FilmDetailsPage() {
  return (
    <DetailPageTemplate>
      <FilmDetails />
    </DetailPageTemplate>
  );
}