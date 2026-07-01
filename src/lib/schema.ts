// JSON-LD-Builder. Es gibt keinen schema.org-Typ „Photographer" → LocalBusiness
// (+ ProfessionalService). Person für Mariluz trägt den 20-Jahre-E-E-A-T-Anker.
import { SITE, NAP, SAME_AS } from '../consts';

const businessId = `${SITE.url}/#business`;
const personId = `${SITE.url}/#mariluz`;

export function localBusiness(areaServed: string = NAP.areaServed) {
  return {
    '@context': 'https://schema.org',
    '@type': ['LocalBusiness', 'ProfessionalService'],
    '@id': businessId,
    name: SITE.name,
    url: SITE.url,
    image: `${SITE.url}/og-default.jpg`,
    telephone: NAP.phoneE164,
    email: NAP.email,
    address: {
      '@type': 'PostalAddress',
      streetAddress: NAP.street,
      postalCode: NAP.postalCode,
      addressLocality: NAP.city,
      addressRegion: NAP.region,
      addressCountry: NAP.country,
    },
    areaServed,
    founder: { '@id': personId },
    ...(SAME_AS.length ? { sameAs: SAME_AS } : {}),
  };
}

export function person() {
  return {
    '@context': 'https://schema.org',
    '@type': 'Person',
    '@id': personId,
    name: 'Mariluz Häfliger',
    alternateName: NAP.legalName,
    jobTitle: 'Fotografin & Videografin',
    worksFor: { '@id': businessId },
    knowsAbout: ['Hochzeitsfotografie', 'Quinceañera', 'Eventfotografie', 'Familienfotografie', 'Videografie'],
    description:
      'Fotografin und Videografin mit über 20 Jahren Erfahrung — begonnen als „Mariluz Producciones" in Lima, heute in der Deutschschweiz.',
    ...(SAME_AS.length ? { sameAs: SAME_AS } : {}),
  };
}

export function service(opts: {
  name: string;
  description: string;
  serviceType: string;
  areaServed?: string;
}) {
  return {
    '@context': 'https://schema.org',
    '@type': 'Service',
    name: opts.name,
    description: opts.description,
    serviceType: opts.serviceType,
    provider: { '@id': businessId },
    areaServed: opts.areaServed ?? NAP.areaServed,
  };
}
