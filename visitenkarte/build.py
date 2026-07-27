#!/usr/bin/env python3
"""
Baut die digitale Visitenkarte von Mariluz Fotografía.

  python3 visitenkarte/build.py

Erzeugt aus karte.template.html + assets/:
  karte.html                       – eigenständige HTML-Datei (Vorschau im Browser)
  out/visitenkarte-druck.pdf       – 2 Seiten, 91×61 mm (85×55 mm + 3 mm Anschnitt)
  out/vorderseite.png              – Endformat 85×55 mm, ~300 dpi
  out/rueckseite.png
  out/share-vorderseite.png        – 1080×1080, für WhatsApp / Instagram
  out/share-rueckseite.png
  out/share-beide.png              – 1080×1350, beide Seiten untereinander
"""

import base64
import mimetypes
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
OUT = ROOT / "out"
QUELLEN = ROOT / "quellen"          # von Mariluz gelieferte Originale
FOTOPOOL = ROOT.parent / "src" / "assets"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# Karten-Geometrie
CARD_MM = (91, 61)          # inkl. 3 mm Anschnitt ringsum
BLEED_MM = 3
PX_PER_MM = 12              # 12 px/mm ≈ 305 dpi
CSS_PX_PER_MM = 1 / 0.264583
DSF = PX_PER_MM * 0.264583  # device scale factor für Chrome

# Markenfarben (für die Share-Hintergründe)
NAVY = "#1f2640"
IVORY = "#faf7f2"
SAND = "#efe9dd"
HAIRLINE = "#c2a24e"

# ---------------------------------------------------------------- Kollage ---
# Die fünf Kacheln der Vorderseite (links → rechts).
#   quelle : Pfad, "pool/..." = Fotopool der Website, "quellen/..." = Original von Mariluz
#   crop   : Ausschnitt im Original (x, y, w, h) — Seitenverhältnis 0.75,
#            das ist der *sichtbare* Teil der Kachel nach dem Schnitt.
#   rand   : an welcher Kartenkante die Kachel liegt (bekommt dort Anschnitt-Zugabe)
#
# Wichtig: oben (und aussen bei Kachel 1/5) gehen 3 mm an den Anschnitt verloren.
# Der Build hängt dort eine gespiegelte Zugabe an, statt Motiv zu opfern — im
# Endformat bleibt damit genau der hier definierte Ausschnitt stehen.
TILES = [
    {"name": "foto-1-schwangerschaft.jpg",  "quelle": "pool/schwangerschaft/schwangerschaft-02.jpg",
     "crop": (0, 140, 578, 770),    "rand": "links",
     "alt": "Schwangere Frau in Weiss am Meer"},
    {"name": "foto-2-hochzeit.jpg",         "quelle": "quellen/hochzeit-strand.jpeg",
     "crop": (512, 0, 1024, 1365),  "rand": None,
     "alt": "Brautpaar küsst sich am Strand"},
    {"name": "foto-3-baby.jpg",             "quelle": "quellen/baby-haarband.jpeg",
     "crop": (96, 0, 576, 768),     "rand": None,
     "alt": "Lachendes Baby mit rosa Haarband"},
    {"name": "foto-4-kindergeburtstag.jpg", "quelle": "quellen/kindergeburtstag-luciana.jpeg",
     "crop": (0, 30, 1170, 1560),   "rand": None,
     "alt": "Kindergeburtstag mit Luftballonbogen"},
    # Ausschnitt auf die Quinceañera, der Hauseingang (Holztür, blau-weisse
    # Fensterläden, Steintreppe) bleibt als Schweizer Kontext im Bild.
    {"name": "foto-5-quinceanera.jpg",      "quelle": "quellen/quinceanera-hauseingang.jpg",
     "crop": (380, 430, 420, 560),  "rand": "rechts",
     "alt": "Quinceañera im pinken Kleid vor einem Schweizer Hauseingang"},
]

TILE_VIS = (520, 694)   # sichtbarer Teil einer Kachel in px (≈ 16.5 × 22 mm)
TILE_BLEED_PX = 95      # 3 mm Anschnitt in derselben Auflösung


def data_uri(name: str) -> str:
    path = ASSETS / name
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode()


def resolve(quelle: str) -> pathlib.Path:
    kind, _, rest = quelle.partition("/")
    return (FOTOPOOL if kind == "pool" else QUELLEN) / rest


def build_tiles() -> None:
    """Kachel-Bilder erzeugen: Ausschnitt + gespiegelte Anschnitt-Zugabe."""
    vw, vh = TILE_VIS
    b = TILE_BLEED_PX
    for t in TILES:
        x, y, w, h = t["crop"]
        args = [str(resolve(t["quelle"])), "-auto-orient",
                "-crop", f"{w}x{h}+{x}+{y}", "+repage",
                "-resize", f"{vw}x{vh}!",
                # Zugabe oben
                "(", "+clone", "-crop", f"{vw}x{b}+0+0", "+repage", "-flip", ")",
                "+swap", "-append"]
        if t["rand"] == "links":
            args += ["(", "+clone", "-crop", f"{b}x{vh + b}+0+0", "+repage", "-flop", ")",
                     "+swap", "+append"]
        elif t["rand"] == "rechts":
            args += ["(", "+clone", "-crop", f"{b}x{vh + b}+{vw - b}+0", "+repage", "-flop", ")",
                     "+append"]
        args += ["-quality", "92", str(ASSETS / t["name"])]
        magick(*args)


def build_html() -> pathlib.Path:
    tpl = (ROOT / "karte.template.html").read_text()
    subs = {
        "{{FONTS}}": (ASSETS / "fonts.css").read_text(),
        "{{LOGO_HELL}}": data_uri("logo-hell.png"),
        "{{LOGO_DUNKEL}}": data_uri("logo-dunkel.png"),
        "{{QR_WEB}}": data_uri("qr-web.png"),
        "{{QR_INSTA}}": data_uri("qr-instagram.png"),
        "{{QR_FB}}": data_uri("qr-facebook.png"),
    }
    for i, t in enumerate(TILES, 1):
        subs[f"{{{{FOTO{i}}}}}"] = data_uri(t["name"])
        subs[f"{{{{ALT{i}}}}}"] = t["alt"]
    for k, v in subs.items():
        tpl = tpl.replace(k, v)
    target = ROOT / "karte.html"
    target.write_text(tpl)
    return target


def chrome(*args: str) -> None:
    subprocess.run(
        [CHROME, "--headless", "--disable-gpu", "--no-sandbox",
         "--hide-scrollbars", "--virtual-time-budget=8000", *args],
        check=True, capture_output=True,
    )


def magick(*args: str) -> None:
    subprocess.run(["magick", *args], check=True)


def render_pdf(html: pathlib.Path) -> None:
    chrome("--no-pdf-header-footer", f"--print-to-pdf={OUT / 'visitenkarte-druck.pdf'}",
           f"file://{html}?clean=1")


def render_side(html: pathlib.Path, side: str, name: str) -> pathlib.Path:
    """Screenshot einer Seite → auf Endformat (ohne Anschnitt) beschnitten.

    Chrome erzwingt in Headless eine Mindest-Viewport-Breite (~500 CSS px).
    Darum grosszügig rendern, die Karte per body.export oben links fixieren
    und den Kartenbereich exakt herausschneiden.
    """
    raw = OUT / f"_raw-{side}.png"
    chrome(f"--screenshot={raw}", "--window-size=800,600",
           f"--force-device-scale-factor={DSF}", f"file://{html}?only={side}")

    full_w, full_h = CARD_MM[0] * PX_PER_MM, CARD_MM[1] * PX_PER_MM
    bleed = BLEED_MM * PX_PER_MM
    trim_w, trim_h = full_w - 2 * bleed, full_h - 2 * bleed
    target = OUT / name
    magick(str(raw),
           "-crop", f"{full_w}x{full_h}+0+0", "+repage",          # Karte inkl. Anschnitt
           "-crop", f"{trim_w}x{trim_h}+{bleed}+{bleed}", "+repage",  # auf Endformat
           "-density", "300", "-units", "PixelsPerInch", str(target))
    raw.unlink()
    return target


def card_layer(card: pathlib.Path, width: int) -> list:
    """Karte auf Breite skaliert, mit goldener Haarlinie als Kante."""
    return ["(", str(card), "-resize", f"{width}x",
            "-bordercolor", HAIRLINE, "-border", "2", ")"]


def share_square(card: pathlib.Path, name: str, bg: str) -> None:
    """Karte mittig auf 1080×1080 Fläche – zum Verschicken."""
    w = 900
    h = round(w * (CARD_MM[1] - 2 * BLEED_MM) / (CARD_MM[0] - 2 * BLEED_MM))
    x, y = (1080 - w) // 2 - 2, (1080 - h) // 2 - 2
    magick("-size", "1080x1080", f"xc:{bg}",
           *card_layer(card, w), "-geometry", f"+{x}+{y}", "-composite",
           "-quality", "92", str(OUT / name))


def share_both(front: pathlib.Path, back: pathlib.Path, name: str) -> None:
    """Beide Seiten untereinander, 1080×1350 (Instagram-Hochformat)."""
    w, gap = 880, 44
    h = round(w * (CARD_MM[1] - 2 * BLEED_MM) / (CARD_MM[0] - 2 * BLEED_MM))
    x = (1080 - w) // 2 - 2
    y_front = (1350 - (2 * h + gap)) // 2 - 2
    y_back = y_front + h + gap
    magick("-size", "1080x1350", f"xc:{SAND}",
           *card_layer(front, w), "-geometry", f"+{x}+{y_front}", "-composite",
           *card_layer(back, w), "-geometry", f"+{x}+{y_back}", "-composite",
           "-quality", "92", str(OUT / name))


def main() -> None:
    if not pathlib.Path(CHROME).exists():
        sys.exit(f"Chrome nicht gefunden: {CHROME}")
    if not shutil.which("magick"):
        sys.exit("ImageMagick (magick) nicht gefunden – brew install imagemagick")

    OUT.mkdir(exist_ok=True)
    build_tiles()
    print("→ Kollagen-Kacheln zugeschnitten")
    html = build_html()
    print("→ karte.html gebaut")

    render_pdf(html)
    print("→ out/visitenkarte-druck.pdf")

    front = render_side(html, "front", "vorderseite.png")
    back = render_side(html, "back", "rueckseite.png")
    print("→ out/vorderseite.png / out/rueckseite.png")

    share_square(front, "share-vorderseite.png", SAND)
    share_square(back, "share-rueckseite.png", NAVY)
    share_both(front, back, "share-beide.png")
    print("→ out/share-*.png")


if __name__ == "__main__":
    main()
