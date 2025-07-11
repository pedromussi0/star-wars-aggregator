import React from 'react';
import ReactDOM from 'react-dom/client';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { AppRouter } from './router'; 
import './styles/index.css'; 

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      
      staleTime: 1000 * 60 * 5, // 5 minutes
      refetchOnWindowFocus: false, 
    },
  },
});

const rootElement = document.getElementById('root');
if (!rootElement) {
  throw new Error("Failed to find the root element with id 'root'");
}

ReactDOM.createRoot(rootElement).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <AppRouter />
    </QueryClientProvider>
  </React.StrictMode>,
);