import { Link } from 'react-router-dom';

interface StatPillProps {
  to: string;
  children: React.ReactNode;
}

export function StatPill({ to, children }: StatPillProps) {
  return (
    <Link
      to={to}
      className="inline-block bg-gray-700 hover:bg-yellow-500 hover:text-black transition-colors duration-200 rounded-full px-3 py-1 text-sm font-semibold text-gray-200 mr-2 mb-2"
    >
      {children}
    </Link>
  );
}