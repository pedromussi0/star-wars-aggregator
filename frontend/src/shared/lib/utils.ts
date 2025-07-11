export const extractIdFromUrl = (url: string): string => {
    const matches = url.match(/\/(\d+)\/?$/);
    return matches ? matches[1] : '';
  };