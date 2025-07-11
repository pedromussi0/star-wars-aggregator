import React from 'react';

interface ListPageTemplateProps {
  title: string;
  children: React.ReactNode;
}

export function ListPageTemplate({ title, children }: ListPageTemplateProps) {
  return (
    <div>
      <h1 className="text-3xl font-bold text-yellow-400 mb-6 border-b-2 border-yellow-400/30 pb-2">{title}</h1>
      {children}
    </div>
  );
}