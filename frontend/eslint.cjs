module.exports = {
    rules: {
      'import/no-restricted-paths': [
        'error',
        {
          zones: [
            {
              target: './src/features',
              from: './src/app',
            },
            {
              target: [
                  './src/components',
                  './src/hooks',
                  './src/lib',
                  './src/types',
                  './src/utils',
              ],
              from: ['./src/features', './src/app'],
            },
            {
              target: './src/features/search',
              from: './src/features',
              except: ['./search'],
            },
          ],
        },
      ],
    },
    settings: {
      'import/resolver': {
        typescript: {}, 
      },
    },
  };