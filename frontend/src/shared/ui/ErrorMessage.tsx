interface ErrorMessageProps {
  message: string;
  title?: string;
}

export function ErrorMessage({
  message,
  title = 'An Error Occurred',
}: ErrorMessageProps) {
  return (
    <div
      className="bg-red-900/40 border-l-4 border-red-500 text-red-200 p-4 rounded-md"
      role="alert"
    >
      <p className="font-bold text-red-100">{title}</p>
      <p>{message}</p>
    </div>
  );
}