import React from 'react';

interface DetailPageTemplateProps {
  children: React.ReactNode;
}

export function DetailPageTemplate({ children }: DetailPageTemplateProps) {
  return <div className="mx-auto max-w-5xl">{children}</div>;
}