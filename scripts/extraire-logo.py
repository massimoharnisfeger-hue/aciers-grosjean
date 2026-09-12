#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extrait le logo officiel Aciers Grosjean depuis la charte graphique PDF
(AciersGrojean_Charte_graphique_def-02.pdf, page 2, déclinaison à plat).

Pourquoi pas page.get_svg_image() : il exporte toute la page clippée, images
raster base64 comprises — 566 Ko pour un logo. On reconstruit donc le SVG
depuis les commandes de tracé, ce qui donne un fichier propre de quelques Ko
dont on maîtrise la couleur et le viewBox.

Sortie :
    public/logo.svg        version encre #333642, pour fond blanc
    public/logo-blanc.svg  version blanche, pour le pied de page sombre
    app/icon.svg           monogramme seul, pour l'onglet du navigateur
"""

import sys
from pathlib import Path

import pymupdf

PDF = Path(sys.argv[1] if len(sys.argv) > 1 else
           "/root/.claude/uploads/60ae7e8a-02ec-55b3-a28b-f1d0fa40a449/"
           "d0a35a1e-AciersGrojean_Charte_graphique_def-02.pdf")
RACINE = Path(__file__).resolve().parent.parent

# Déclinaison à plat de la page 2, repérée par sa boîte englobante.
ZONE = pymupdf.Rect(78.2, 310.2, 292.2, 387.9)

ENCRE = "#333642"   # Pantone 432 C — la valeur de la charte, pas celle du PDF
BLANC = "#FFFFFF"


def nb(v: float) -> str:
    """Nombre compact : 3 décimales, sans zéros inutiles."""
    s = f"{v:.3f}".rstrip("0").rstrip(".")
    return s if s not in ("-0", "") else "0"


def chemin_svg(dessin, dx: float, dy: float) -> str:
    """Convertit les commandes de tracé PyMuPDF en attribut d= SVG."""
    out = []
    pos = None
    for it in dessin["items"]:
        k = it[0]
        if k == "l":
            p1, p2 = it[1], it[2]
            if pos != (p1.x, p1.y):
                out.append(f"M{nb(p1.x - dx)} {nb(p1.y - dy)}")
            out.append(f"L{nb(p2.x - dx)} {nb(p2.y - dy)}")
            pos = (p2.x, p2.y)
        elif k == "c":
            p1, p2, p3, p4 = it[1], it[2], it[3], it[4]
            if pos != (p1.x, p1.y):
                out.append(f"M{nb(p1.x - dx)} {nb(p1.y - dy)}")
            out.append(
                f"C{nb(p2.x - dx)} {nb(p2.y - dy)} {nb(p3.x - dx)} {nb(p3.y - dy)} "
                f"{nb(p4.x - dx)} {nb(p4.y - dy)}"
            )
            pos = (p4.x, p4.y)
        elif k == "re":
            r = it[1]
            out.append(
                f"M{nb(r.x0 - dx)} {nb(r.y0 - dy)}H{nb(r.x1 - dx)}"
                f"V{nb(r.y1 - dy)}H{nb(r.x0 - dx)}Z"
            )
            pos = None
        elif k == "qu":
            q = it[1]
            pts = [q.ul, q.ur, q.lr, q.ll]
            out.append("M" + " L".join(f"{nb(p.x - dx)} {nb(p.y - dy)}" for p in pts) + "Z")
            pos = None
    if dessin.get("closePath"):
        out.append("Z")
    return "".join(out)


def construire(dessins, zone: pymupdf.Rect, couleur: str, titre: str) -> str:
    dx, dy = zone.x0, zone.y0
    w, h = zone.width, zone.height
    corps = []
    for g in dessins:
        d = chemin_svg(g, dx, dy)
        if not d:
            continue
        regle = ' fill-rule="evenodd"' if g.get("even_odd") else ' fill-rule="nonzero"'
        corps.append(f'<path d="{d}"{regle}/>')
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {nb(w)} {nb(h)}" '
        f'role="img" aria-label="{titre}">\n'
        f"  <title>{titre}</title>\n"
        f'  <g fill="{couleur}">\n    ' + "\n    ".join(corps) + "\n  </g>\n</svg>\n"
    )


def main() -> None:
    doc = pymupdf.open(PDF)
    page = doc[1]
    sel = [
        g for g in page.get_drawings()
        if ZONE.y0 - 5 < g["rect"].y0 and g["rect"].y1 < ZONE.y1 + 5 and g["rect"].x1 < ZONE.x1 + 5
    ]
    if not sel:
        raise SystemExit("aucun tracé trouvé dans la zone du logo")

    union = pymupdf.Rect(sel[0]["rect"])
    for g in sel:
        union |= g["rect"]

    (RACINE / "public").mkdir(exist_ok=True)
    (RACINE / "public" / "logo.svg").write_text(
        construire(sel, union, ENCRE, "Aciers Grosjean"), encoding="utf-8")
    (RACINE / "public" / "logo-blanc.svg").write_text(
        construire(sel, union, BLANC, "Aciers Grosjean"), encoding="utf-8")

    # Monogramme : les tracés de la partie gauche (le « Gi »).
    coupure = union.x0 + union.width * 0.36
    mono = [g for g in sel if g["rect"].x1 <= coupure]
    if mono:
        um = pymupdf.Rect(mono[0]["rect"])
        for g in mono:
            um |= g["rect"]
        cote = max(um.width, um.height) * 1.35
        cadre = pymupdf.Rect(
            um.x0 - (cote - um.width) / 2, um.y0 - (cote - um.height) / 2,
            um.x0 - (cote - um.width) / 2 + cote, um.y0 - (cote - um.height) / 2 + cote,
        )
        svg = construire(mono, cadre, "#FFD500", "Aciers Grosjean")
        svg = svg.replace(
            "<title>",
            f'<rect width="{nb(cote)}" height="{nb(cote)}" rx="{nb(cote * 0.17)}" fill="#333642"/>\n  <title>',
        )
        (RACINE / "app" / "icon.svg").write_text(svg, encoding="utf-8")

    print(f"logo      : {len(sel)} tracés, {union.width:.1f} × {union.height:.1f} pt")
    print(f"monogramme: {len(mono)} tracés")
    for f in ("public/logo.svg", "public/logo-blanc.svg", "app/icon.svg"):
        p = RACINE / f
        if p.exists():
            print(f"  {f:24s} {p.stat().st_size / 1024:.1f} Ko")


if __name__ == "__main__":
    main()
