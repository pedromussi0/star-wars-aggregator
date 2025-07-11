// This function already exists
export const extractIdFromUrl = (url: string): string => {
    const matches = url.match(/\/(\d+)\/?$/);
    return matches ? matches[1] : '';
  };
  
  
  /**
   * Extracts the resource category and ID from a SWAPI URL.
   * Handles both absolute (http://...) and relative (/api/v1/...) URLs.
   * @param url The resource URL from the API.
   * @returns A string in the format "category/id", e.g., "films/1".
   *          Returns an empty string if the URL is invalid.
   */
  export const getRelativeResourcePath = (url: string): string => {
    if (!url) return '';
    try {
      // Use the URL constructor to easily parse the path
      const path = new URL(url, 'http://dummybase.com').pathname; // Dummy base allows parsing relative paths
      
      // Path will look like /api/v1/films/1/
      const parts = path.split('/').filter(part => part !== ''); // -> ['api', 'v1', 'films', '1']
      
      // We want the last two parts
      const category = parts[parts.length - 2];
      const id = parts[parts.length - 1];
  
      if (category && id) {
        return `${category}/${id}`;
      }
      return '';
    } catch (error) {
      console.error("Failed to parse resource URL:", url, error);
      return '';
    }
  };