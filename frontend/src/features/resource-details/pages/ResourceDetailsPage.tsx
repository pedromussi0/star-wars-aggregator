import { useParams } from 'react-router-dom';
import { useResourceDetails } from '../api/useResourceDetails';
import { ResourceDetailsView } from '../components/ResourceDetailsView';
import { DetailPageTemplate } from '@/shared/components/pages/DetailPageTemplate';
import { LoadingSpinner } from '@/shared/ui/LoadingSpinner';
import { ErrorMessage } from '@/shared/ui/ErrorMessage';

export function ResourceDetailsPage() {
  // useParams will get category and id from the URL: /browse/:category/:id
  const { category, id } = useParams<{ category: string; id: string }>();
  const { data, isLoading, isError, error } = useResourceDetails(category, id);

  return (
    <DetailPageTemplate>
      {isLoading && <LoadingSpinner />}
      {isError && <ErrorMessage message={(error as Error).message} />}
      {data && <ResourceDetailsView resource={data} category={category!} />}
    </DetailPageTemplate>
  );
}