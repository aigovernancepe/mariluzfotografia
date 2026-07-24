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
 *
 * `exclude`: Dateinamen (oder Pfad-Teilstrings), die übersprungen werden — z. B.
 * ein Bild, das schon als Hero derselben Seite dient, damit es nicht doppelt
 * erscheint: `toGallery(glob, 'Schwangerschaft', ['schwangerschaft_01'])`.
 */
export function toGallery(
  glob: Record<string, { default: ImageMetadata }>,
  label: string,
  exclude: string[] = [],
): GalleryImage[] {
  return Object.entries(glob)
    .filter(([path]) => !exclude.some((ex) => path.includes(ex)))
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([, mod]) => ({
      src: mod.default,
      alt: `${label} — Mariluz Fotografía`,
    }));
}
