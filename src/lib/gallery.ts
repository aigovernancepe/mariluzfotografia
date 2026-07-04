import type { ImageMetadata } from 'astro';

export interface GalleryImage {
  src: ImageMetadata;
  alt: string;
}

/**
 * Wandelt das Ergebnis eines `import.meta.glob(..., { eager: true })` in eine
 * sortierte Galerie-Liste um. Aufruf-Beispiel in einer Seite:
 *
 *   const glob = import.meta.glob<{ default: ImageMetadata }>(
 *     '../assets/hochzeit/*.{jpg,jpeg,png,webp,avif}', { eager: true },
 *   );
 *   const bilder = toGallery(glob, 'Hochzeitsfotografie');
 *
 * Der Glob-Pfad muss ein statisches Literal relativ zur Seite sein (Vite-Regel).
 */
export function toGallery(
  glob: Record<string, { default: ImageMetadata }>,
  label: string,
): GalleryImage[] {
  return Object.entries(glob)
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([, mod]) => ({
      src: mod.default,
      alt: `${label} — Mariluz Fotografía`,
    }));
}
