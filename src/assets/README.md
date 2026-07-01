# Bilder — wohin damit?

Zwei Orte, klare Regel:

## 1. `src/assets/…`  → HIER kommen (fast) alle Fotos rein
Diese Bilder laufen durch Astros **Bild-Pipeline** (`<Image>` / `<Picture>`):
automatische AVIF/WebP-Konvertierung, responsive Grössen (`srcset`),
Breite/Höhe gesetzt (kein Layout-Springen/CLS), Hashing fürs Caching.
→ Das ist der richtige Ort für Portfolio-, Hero- und Service-Bilder.

Struktur nach Anlass:
```
src/assets/
  hochzeit/     quinceanera/   familie/
  taufe/        event/         schwangerschaft/
  video/ (Thumbnails/Poster)   about/ (Portrait Mariluz)
  hero/ (Startseiten-Bilder)
```

**Verwendung im Code:**
```astro
---
import { Image } from 'astro:assets';
import bild from '../assets/hochzeit/basel-01.jpg';
---
<Image src={bild} alt="Hochzeit in Basel — Trauung im Freien" widths={[400, 800, 1200]} />
```

## 2. `public/…`  → nur Fixe-URL-Assets
Wird **unverändert** ausgeliefert, keine Optimierung. Nur für:
`favicon.svg`, `og-default.jpg` (Social-Vorschau), `robots.txt`, `_headers`.
Keine Portfolio-Fotos hierher — die verlieren sonst die Optimierung.

## Vor dem Hochladen
- **Web-Grösse exportieren:** lange Kante ~2000–2500 px, JPEG Q80. KEINE RAWs / 20-MB-Originale
  ins Git — Astro macht daraus die kleinen responsiven Varianten.
- **Dateiname sprechend:** `basel-hochzeit-standesamt-01.jpg` (hilft Bild-SEO).
- **alt-Text = Anlass + Ort** (SEO + Barrierefreiheit).
- **Foto-Freigabe (revDSG):** abgebildete Personen nur mit Einwilligung veröffentlichen.

## Später: Decap CMS
Wenn Mariluz selbst Bilder pflegt, konfigurieren wir Decaps Media-Folder
(Entscheid dann: `src/assets` mit Optimierung vs. `public/uploads` einfacher).
Bis dahin: Bilder hierher legen und im Code via `<Image>` einbinden.
