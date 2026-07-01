// Zentrale Site-Konstanten. NAP = kanonische Wahrheit (muss Schema + GBP + Zitate matchen).
// Firma noch nicht gegründet → vorerst natürliche Person; Business-Name/UID nach Gründung.

export const SITE = {
  name: 'Mariluz Fotografía',
  domain: 'mariluzfotografia.ch',
  url: 'https://mariluzfotografia.ch',
  tagline_de: 'Foto & Video für Ihre schönsten Momente',
  tagline_es: 'Foto y video para tus momentos más especiales',
} as const;

// NAP — Master Copy (siehe clients/mariluz/CLAUDE.md)
export const NAP = {
  legalName: 'Mariluz Medina Cacsire de Häfliger',
  street: 'Neue Bahnhofsstrasse 17',
  postalCode: '5737',
  city: 'Menziken',
  region: 'Aargau',
  country: 'CH',
  phoneE164: '+41762227304',
  phoneDisplay: '076 222 27 04',
  email: 'mariluzhafliger@gmail.com', // TODO: auf kontakt@mariluzfotografia.ch umstellen
  areaServed: 'Deutschschweiz',
} as const;

// sameAs — sobald live eintragen (Instagram, GBP, Facebook)
export const SAME_AS: string[] = [
  // 'https://www.instagram.com/...',
  // 'https://g.page/...',
];

export const NAV_DE = [
  { label: 'Hochzeit', href: '/hochzeitsfotograf/' },
  { label: 'Familie', href: '/familienfotografie/' },
  { label: 'Schwangerschaft', href: '/schwangerschaftsfotos/' },
  { label: 'Events', href: '/eventfotografie/' },
  { label: 'Video', href: '/video/' },
  { label: 'Portfolio', href: '/portfolio/' },
  { label: 'Über mich', href: '/ueber-mich/' },
  { label: 'Kontakt', href: '/kontakt/' },
] as const;

export const NAV_ES = [
  { label: 'Quinceañera', href: '/es/fotografo-quinceanera/' },
  { label: 'Bodas', href: '/es/fotografo-bodas/' },
  { label: 'Bautizo', href: '/es/fotografo-bautizo/' },
  { label: 'Familiar', href: '/es/fotografo-familiar/' },
  { label: 'Sobre mí', href: '/es/sobre-mi/' },
  { label: 'Contacto', href: '/es/contacto/' },
] as const;
