# Visitenkarte — Mariluz Fotografía

Zweiseitige Visitenkarte im Standardformat **85 × 55 mm**.
Vorderseite: Foto-Kollage + Logo + Kontakt + Leistungen (DE/ES).
Rückseite: QR-Codes zu Website, Instagram, Facebook.

## Bauen

```bash
python3 visitenkarte/build.py
```

Braucht Google Chrome (Rendering) und ImageMagick (`brew install imagemagick`).

## Ergebnisse in `out/`

| Datei | Zweck |
|---|---|
| `visitenkarte-druck.pdf` | Druckerei. 2 Seiten, je 91 × 61 mm = Endformat + 3 mm Anschnitt ringsum |
| `vorderseite.png`, `rueckseite.png` | Endformat 85 × 55 mm, 1020 × 660 px (~300 dpi), ohne Anschnitt |
| `share-vorderseite.png`, `share-rueckseite.png` | 1080 × 1080, für WhatsApp / Instagram-Feed |
| `share-beide.png` | 1080 × 1350, beide Seiten untereinander |

`karte.html` im Projektordner ist die fertige, eigenständige Karte (Schriften und
Bilder als Data-URI eingebettet) — im Browser öffnen für die Vorschau, die rote
Strichlinie markiert die Schnittkante. `karte.template.html` ist die Vorlage mit
`{{PLATZHALTER}}` und allein nicht anzeigbar.

## Etwas ändern

**Texte, Farben, Layout** → `karte.template.html`, danach neu bauen.
Kontaktdaten stammen aus `src/consts.ts` (NAP), sind hier aber fest eingetragen —
bei einer Adress- oder Nummernänderung beide Stellen anfassen.

**Fotos der Kollage** → `TILES` in `build.py`. Pro Kachel:

```python
{"name": "foto-2-taufe.jpg",          # Zieldatei in assets/
 "quelle": "quellen/taufe.jpeg",      # "pool/…" = src/assets/…, "quellen/…" = Original hier
 "crop": (1585, 0, 1950, 2600),       # x, y, Breite, Höhe im Original — Verhältnis 3:4
 "rand": None,                        # "links" / "rechts" bei der ersten / letzten Kachel
 "alt": "Junge im weissen Taufgewand"}
```

Der `crop` ist der **sichtbare** Teil nach dem Schnitt. Die 3 mm Anschnitt hängt
der Build als gespiegelten Streifen an (oben, bei Kachel 1 und 5 zusätzlich
aussen) — deshalb muss kein Motiv für den Anschnitt geopfert werden, und es wird
kein Kopf angeschnitten. Verhältnis Breite:Höhe des Crops immer **0,75** halten,
sonst verzerrt das Bild.

**QR-Ziele** → in `build.py` sind die QR-PNGs vorgeneriert in `assets/`. Neu erzeugen:

```bash
qrencode -t PNG -o visitenkarte/assets/qr-web.png -s 24 -m 0 -l M \
  --foreground=1F2640 "https://mariluzfotografia.ch/"
```

Aktuelle Ziele: `mariluzfotografia.ch`, `instagram.com/mariluz_fotografia`,
`facebook.com/bodasmariluz` (aufgelöst aus dem Share-Link). Alle drei mit 29
Modulen und Fehlerkorrektur M — bei 20 mm Kantenlänge gut scannbar; geprüft mit
`zbarimg` auch aus stark verkleinerten Renderings.

## Für die Druckerei

- Datei: `out/visitenkarte-druck.pdf`, Endformat 85 × 55 mm, **3 mm Anschnitt enthalten**, keine Schnittmarken.
- Empfehlung: 350 g/m², matt — die navy Vollfläche wirkt darauf ruhiger als glänzend.
- Das PDF ist **RGB**. Online-Druckereien konvertieren selbst nach CMYK; verlangt
  eine klassische Druckerei CMYK/ICC-Profil, muss das PDF vorher konvertiert
  werden (z. B. in Acrobat oder mit Ghostscript). Das Navy #1f2640 und das Gold
  #c2a24e verschieben sich dabei leicht ins Stumpfe — bei kritischem Anspruch
  einen Proof anfordern.
- Textränder liegen 5 mm von der Schnittkante entfernt, die Fotos laufen randabfallend.
