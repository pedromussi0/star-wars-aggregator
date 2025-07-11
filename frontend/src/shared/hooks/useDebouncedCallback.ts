import { useEffect, useMemo, useRef } from 'react';
import { debounce } from 'lodash';

/**
 * A custom hook that returns a debounced version of a callback function.
 * This is crucial for performance optimization on inputs that trigger API calls.
 * @param callback The function to be debounced.
 * @param delay The debounce delay in milliseconds.
 * @returns The memoized, debounced callback function, typed as the original function.
 */
// eslint-disable-next-line @typescript-eslint/no-explicit-any
export function useDebouncedCallback<T extends (...args: any[]) => any>(
  callback: T,
  delay: number
): T {
  const callbackRef = useRef<T>(callback);

  useEffect(() => {
    callbackRef.current = callback;
  });

  return useMemo(() => {
    const debounced = debounce((...args: Parameters<T>) => {
      callbackRef.current(...args);
    }, delay);

    // --- THIS IS THE FIX ---
    // This double assertion is the intentional and correct way to handle this.
    // 1. `debounced as unknown`: We first cast the DebouncedFunc to `unknown`, telling TypeScript to "forget" its specific type.
    // 2. `... as T`: Now that it's a type-neutral `unknown`, we can safely assert it to be the generic function type `T`.
    return (debounced as unknown) as T;
  }, [delay]);
}