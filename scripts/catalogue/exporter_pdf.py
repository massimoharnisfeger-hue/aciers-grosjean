#!/usr/bin/env python3
"""Exporte le catalogue en PDF A4 depuis la page /catalogue/imprimer.

À lancer quand le catalogue est validé (ADR-0010). Prérequis, sur le poste :
`.env.local` avec `CATALOGUE_LOCAL=oui`, puis `npm run build` ; Playwright
Python avec Chromium ; pypdf. Rien n'est écrit dans le dépôt : le PDF va dans
`_DEPOT/documents/catalogue/` (OneDrive, hors Git).

Comment :
  1. démarre `next start` sur un port libre (jamais 3000 : leçon L-050) ;
  2. ouvre la page, attend chaque image, passe en média d'impression ;
  3. premier rendu PDF pour lire, page par page (pypdf), où tombent les
     ouvertures de chapitre (ligne « Chapitre n ») et les titres de famille ;
  4. écrit ces numéros dans le sommaire (`data-page-de`), puis rend la
     couverture sans pied de page et le corps avec pied de page numéroté ;
  5. assemble les deux (pypdf).

Les images passent par l'optimiseur de Next en WebP : l'AVIF est refusé aux
requêtes d'images, parce que l'encodeur local bloque sur certains fichiers
(constat du 23/09, rapport du catalogue).

Usage :
    python scripts/catalogue/exporter_pdf.py
    python scripts/catalogue/exporter_pdf.py --sortie C:/chemin/catalogue.pdf
"""

import argparse
import re
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import unicodedata
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path

RACINE = Path(__file__).resolve().parents[2]
NEXT = RACINE / "node_modules" / "next" / "dist" / "bin" / "next"
PAGE_CONSTRUITE = RACINE / ".next" / "server" / "app" / "catalogue" / "imprimer.html"
ENV_LOCAL = RACINE / ".env.local"
SORTIE = RACINE / "_DEPOT" / "documents" / "catalogue"
MARGES = {"top": "14mm", "bottom": "16mm", "left": "12mm", "right": "12mm"}
DELAI_IMAGES_MS = 300_000


def sortie_utf8():
    for flux in (sys.stdout, sys.stderr):
        try:
            flux.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass


def drapeau_local() -> bool:
    if not ENV_LOCAL.exists():
        return False
    return re.search(r"^\s*CATALOGUE_LOCAL\s*=\s*oui\s*$", ENV_LOCAL.read_text(encoding="utf-8"), re.M) is not None


def port_libre() -> int:
    with socket.socket() as prise:
        prise.bind(("127.0.0.1", 0))
        return prise.getsockname()[1]


def demarrer(port: int) -> subprocess.Popen:
    node = shutil.which("node")
    if node is None:
        raise SystemExit("node est introuvable dans le PATH.")
    processus = subprocess.Popen([node, str(NEXT), "start", "-p", str(port)], cwd=RACINE,
                                 stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    limite = time.monotonic() + 40
    while time.monotonic() < limite:
        if processus.poll() is not None:
            raise SystemExit("`next start` s'est arrêté avant de répondre.")
        try:
            urllib.request.urlopen(f"http://127.0.0.1:{port}/catalogue/imprimer", timeout=2).read(1)
            return processus
        except urllib.error.HTTPError:
            return processus
        except OSError:
            time.sleep(0.3)
    processus.terminate()
    raise SystemExit("le serveur n'a pas répondu en 40 s.")


def normaliser(texte: str) -> str:
    texte = unicodedata.normalize("NFKC", texte).replace("\ufb01", "fi").replace("\ufb02", "fl")
    return re.sub(r"\s+", " ", texte).strip()


def lignes_des_pages(pdf: Path) -> list[list[str]]:
    from pypdf import PdfReader

    return [[normaliser(l) for l in (p.extract_text() or "").splitlines() if normaliser(l)] for p in PdfReader(str(pdf)).pages]


def numeros_de_page(pages: list[list[str]], structure: list[dict]) -> dict[str, int]:
    """{ancre: numéro de page 1-based}. Un titre non retrouvé reste absent : mieux un blanc qu'un faux numéro."""
    trouves: dict[str, int] = {}
    depuis = 0
    for chapitre in structure:
        marque = f"Chapitre {chapitre['numero']}"
        debut = next((i for i in range(depuis, len(pages)) if marque in pages[i]), None)
        if debut is None:
            continue
        trouves[f"chapitre-{chapitre['slug']}"] = debut + 1
        curseur = debut + 1
        for famille in chapitre["familles"]:
            nom = normaliser(famille["nom"])
            page = next((i for i in range(curseur, len(pages)) if nom in pages[i]), None)
            if page is not None:
                trouves[famille["ancre"]] = page + 1
                curseur = page
        depuis = debut + 1
    return trouves


def exporter(base: str, cible: Path) -> tuple[int, int]:
    from playwright.sync_api import sync_playwright
    from pypdf import PdfReader, PdfWriter

    edition = date.today().strftime("%B %Y")
    pied = (
        '<div style="width:100%;font-family:Arial,sans-serif;font-size:7.5px;color:#7a7e88;'
        'padding:0 12mm;display:flex;justify-content:space-between;">'
        f"<span>Aciers Grosjean — Catalogue produits — édition {edition}</span>"
        '<span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>'
    )
    with tempfile.TemporaryDirectory() as dossier, sync_playwright() as pw:
        tmp = Path(dossier)
        navigateur = pw.chromium.launch()
        contexte = navigateur.new_context(viewport={"width": 794, "height": 1123}, device_scale_factor=1)
        contexte.route("**/_next/image**", lambda route: route.continue_(
            headers={**route.request.headers, "accept": "image/webp,image/*,*/*;q=0.8"}))
        page = contexte.new_page()
        page.goto(base + "/catalogue/imprimer", wait_until="load", timeout=180_000)
        page.wait_for_function(
            "Array.from(document.images).every((i) => i.complete && i.naturalWidth > 0)", timeout=DELAI_IMAGES_MS
        )
        page.emulate_media(media="print")
        structure = page.evaluate(
            """() => Array.from(document.querySelectorAll('[data-chapitre-doc]')).map((c) => ({
                 slug: c.dataset.chapitreDoc, numero: Number(c.dataset.numero),
                 familles: Array.from(c.querySelectorAll('[data-famille-doc]')).map((f) => ({ancre: f.dataset.familleDoc, nom: f.dataset.nom}))
               }))"""
        )
        commun = dict(format="A4", print_background=True, margin=MARGES)

        premier = tmp / "passe-1.pdf"
        page.pdf(path=str(premier), display_header_footer=True, header_template="<span></span>", footer_template=pied, **commun)
        pages = lignes_des_pages(premier)
        numeros = numeros_de_page(pages, structure)
        page.evaluate(
            "(m) => { for (const [k, v] of Object.entries(m)) document.querySelectorAll(`[data-page-de=\"${k}\"]`).forEach((e) => { e.textContent = String(v); }); }",
            numeros,
        )

        couverture = tmp / "couverture.pdf"
        corps = tmp / "corps.pdf"
        page.pdf(path=str(couverture), page_ranges="1", display_header_footer=False, **commun)
        page.pdf(path=str(corps), page_ranges=f"2-{len(pages)}", display_header_footer=True,
                 header_template="<span></span>", footer_template=pied, **commun)
        navigateur.close()

        assembleur = PdfWriter()
        for morceau in (couverture, corps):
            for p in PdfReader(str(morceau)).pages:
                assembleur.add_page(p)
        cible.parent.mkdir(parents=True, exist_ok=True)
        with cible.open("wb") as f:
            assembleur.write(f)
        return len(pages), len(numeros)


def main() -> int:
    sortie_utf8()
    ap = argparse.ArgumentParser()
    ap.add_argument("--sortie", help="fichier PDF à écrire (défaut : _DEPOT/documents/catalogue/…)")
    args = ap.parse_args()

    if not drapeau_local():
        raise SystemExit("`.env.local` ne porte pas CATALOGUE_LOCAL=oui : le catalogue n'est pas construit.")
    if not PAGE_CONSTRUITE.exists():
        raise SystemExit("page /catalogue/imprimer absente du build : lancer `npm run build`.")
    cible = Path(args.sortie) if args.sortie else SORTIE / f"catalogue-produits-aciers-grosjean-{date.today():%Y-%m}.pdf"

    port = port_libre()
    serveur = demarrer(port)
    try:
        nb_pages, nb_numeros = exporter(f"http://127.0.0.1:{port}", cible)
    finally:
        serveur.terminate()
        try:
            serveur.wait(timeout=10)
        except subprocess.TimeoutExpired:
            serveur.kill()
    print(f"PDF : {cible}\n{nb_pages} pages, {cible.stat().st_size / 1024 / 1024:.1f} Mo, {nb_numeros} entrées de sommaire numérotées")
    return 0


if __name__ == "__main__":
    sys.exit(main())
