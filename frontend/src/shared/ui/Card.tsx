import React from 'react';
import { Link, type To } from 'react-router-dom';

interface CardProps {
  children: React.ReactNode;
  to?: To | string;
  className?: string;
}

const CardTitle = ({ children }: { children: React.ReactNode }) => (
  <h2 className="text-xl font-bold text-yellow-400 mb-2 truncate">{children}</h2>
);

const CardBody = ({ children }: { children: React.ReactNode }) => (
  <div className="text-gray-300">{children}</div>
);

const CardFooter = ({ children }: { children: React.ReactNode }) => (
  <div className="mt-4 pt-4 border-t border-gray-700">{children}</div>
);


export function Card({ children, to, className = '' }: CardProps) {
  const cardContent = (
    <div
      className={`bg-gray-800 rounded-lg shadow-lg p-4 md:p-6 transition-all duration-200 transform hover:-translate-y-1 hover:shadow-yellow-400/20 ${className}`}
    >
      {children}
    </div>
  );

  if (!to) {
    return cardContent;
  }

  const isExternal = typeof to === 'string' && to.startsWith('http');

  if (isExternal) {
    return (
      <a
        href={to}
        target="_blank"
        rel="noopener noreferrer"
        className="block focus:outline-none focus:ring-2 focus:ring-yellow-400 rounded-lg"
      >
        {cardContent}
      </a>
    );
  }
  return (
    <Link
      to={to}
      className="block focus:outline-none focus:ring-2 focus:ring-yellow-400 rounded-lg"
    >
      {cardContent}
    </Link>
  );
}

Card.Title = CardTitle;
Card.Body = CardBody;
Card.Footer = CardFooter;