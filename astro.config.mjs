import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';
import sitemap from '@astrojs/sitemap';

// Mariluz Fotografía — mariluzfotografia.ch
// CH-DE (Swiss German) at the site root, Spanish under /es/.
// The root locale code is 'de'; the layout hard-sets <html lang="de-CH"> and
// the hreflang tags to de-CH / es / x-default. Swiss number formatting uses the
// straight apostrophe (1'500 CHF), so smartypants stays off.
export default defineConfig({
  site: 'https://mariluzfotografia.ch',
  trailingSlash: 'always',
  output: 'static',
  i18n: {
    defaultLocale: 'de',
    locales: ['de', 'es'],
    routing: {
      prefixDefaultLocale: false,
    },
  },
  integrations: [sitemap()],
  markdown: {
    smartypants: false,
  },
  vite: {
    plugins: [tailwindcss()],
  },
});
