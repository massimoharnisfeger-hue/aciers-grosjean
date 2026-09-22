"""Balayage responsive du site rendu, dans un vrai Chromium (Playwright).

Pour chaque URL et chaque largeur, la page est ouverte, deroulee jusqu'en bas
(pour declencher les chargements paresseux), puis mesuree en lecture seule :

- debordement horizontal : `scrollWidth` contre `innerWidth`, avec les elements
  coupables (ceux qui depassent le bord droit ou gauche de la fenetre) ;
- cibles tactiles trop petites : liens, boutons et champs visibles dont la boite
  fait moins de 24 px de haut ou de large (minimum WCAG 2.2, critere 2.5.8) ;
- textes trop petits : elements visibles avec un texte propre sous 12 px ;
- erreurs console, erreurs de page, reponses reseau en echec sur l'origine.

Avec `--interactif`, quelques parcours sont joues aux largeurs mobiles :
ouverture du menu, recherche, filtre du tableau produits, formulaire de devis.

Les resultats vont HORS du depot : JSON et captures dans
`%LOCALAPPDATA%\\SiteAciersGrosjean\\qa-responsive\\<horodatage>\\` (ou `--out`).
Le depot est public et les captures ne sont pas des livrables.

Usage :
    python scripts/qa/balayage-responsive.py --urls gabarits.txt
    python scripts/qa/balayage-responsive.py --urls gabarits.txt --widths 320,375,768
    python scripts/qa/balayage-responsive.py --urls gabarits.txt --captures --interactif

Prerequis : `npm run build` puis `npm run start` (port 3000), et Playwright
Python avec Chromium (`pip install playwright && playwright install chromium`).
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

BASE_DEFAUT = "http://127.0.0.1:3000"
LARGEURS_DEFAUT = [320, 360, 375, 390, 414, 600, 768, 820, 834, 1024, 1280]

# Lecture seule : aucune ecriture dans le DOM, aucune navigation.
MESURE_JS = r"""
() => {
  const W = window.innerWidth;
  const doc = document.documentElement;
  const visible = (el) => {
    const r = el.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) return false;
    const s = getComputedStyle(el);
    // `sr-only` : present pour le lecteur d'ecran, rogne a 1 x 1 px pour l'oeil
    // et le doigt. Sa cible visible est l'etiquette qui le designe (galerie
    // produit, 22/09 : deux « cibles » de 1 x 1 remontees a tort par fiche).
    if (s.clip === 'rect(0px, 0px, 0px, 0px)') return false;
    return s.visibility !== 'hidden' && s.display !== 'none' && s.opacity !== '0';
  };
  const decrire = (el) => {
    const r = el.getBoundingClientRect();
    const txt = (el.innerText || el.getAttribute('aria-label') || el.getAttribute('alt') || '').trim().replace(/\s+/g, ' ').slice(0, 40);
    const cls = (typeof el.className === 'string' ? el.className : '').split(/\s+/).slice(0, 4).join('.');
    return { tag: el.tagName.toLowerCase(), cls, txt, w: Math.round(r.width), h: Math.round(r.height), l: Math.round(r.left), r: Math.round(r.right) };
  };
  // 1. debordement : elements dont la boite sort de la fenetre
  const coupables = [];
  for (const el of document.body.querySelectorAll('*')) {
    if (coupables.length >= 8) break;
    const r = el.getBoundingClientRect();
    if (r.width === 0) continue;
    const s = getComputedStyle(el);
    if (s.position === 'fixed') continue;
    if (r.right > W + 1 || r.left < -1) {
      // un enfant d'un conteneur a defilement horizontal volontaire n'est pas un coupable
      let p = el.parentElement, volontaire = false;
      while (p && p !== document.body) {
        const ps = getComputedStyle(p);
        if (/(auto|scroll)/.test(ps.overflowX) && p.scrollWidth > p.clientWidth) { volontaire = true; break; }
        if (/hidden|clip/.test(ps.overflowX)) { volontaire = true; break; }
        p = p.parentElement;
      }
      if (!volontaire) coupables.push(decrire(el));
    }
  }
  // 2. cibles tactiles < 24 px
  const petites = [];
  let nbPetites = 0;
  for (const el of document.querySelectorAll('a[href], button, input, select, textarea, [role=button]')) {
    if (!visible(el)) continue;
    if (el.type === 'hidden') continue;
    const r = el.getBoundingClientRect();
    if (r.height < 24 || r.width < 24) { nbPetites++; if (petites.length < 12) petites.push(decrire(el)); }
  }
  // 3. textes < 12 px (elements avec texte direct)
  let nbTextes = 0; const textes = [];
  for (const el of document.body.querySelectorAll('*')) {
    if (!el.childNodes.length) continue;
    let direct = false;
    for (const n of el.childNodes) if (n.nodeType === 3 && n.textContent.trim()) { direct = true; break; }
    if (!direct || !visible(el)) continue;
    const fs = parseFloat(getComputedStyle(el).fontSize);
    if (fs < 12) { nbTextes++; if (textes.length < 6) textes.push({ ...decrire(el), fs }); }
  }
  return {
    scrollWidth: doc.scrollWidth, innerWidth: W, coupables,
    cibles_petites: nbPetites, exemples_cibles: petites,
    textes_petits: nbTextes, exemples_textes: textes,
    hauteur: doc.scrollHeight,
  };
}
"""


def sortie_utf8():
    for flux in (sys.stdout, sys.stderr):
        try:
            flux.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass


def derouler(page):
    """Descend jusqu'en bas par paliers, puis remonte : declenche le paresseux."""
    hauteur = page.evaluate("document.documentElement.scrollHeight")
    y = 0
    while y < hauteur:
        y += 600
        page.evaluate(f"window.scrollTo(0, {y})")
        page.wait_for_timeout(60)
        hauteur = page.evaluate("document.documentElement.scrollHeight")
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(150)


def mesurer_page(page, base, chemin, largeur, captures, dossier, journal):
    """Mesure une page a une largeur. `journal` recoit console, erreurs et reseau du contexte."""
    for cle in journal:
        journal[cle].clear()
    page.set_viewport_size({"width": largeur, "height": 800})
    reponse = page.goto(base + chemin, wait_until="networkidle", timeout=45000)
    derouler(page)
    mesure = page.evaluate(MESURE_JS)
    mesure.update({
        "url": chemin, "largeur": largeur, "statut": reponse.status if reponse else None,
        "console": list(journal["console"])[:10], "erreurs_page": list(journal["erreurs"])[:5],
        "reseau": list(journal["reseau"])[:10],
        "debordement": mesure["scrollWidth"] > mesure["innerWidth"],
    })
    if captures:
        nom = (chemin.strip("/").replace("/", "_") or "accueil") + f"_{largeur}.png"
        page.screenshot(path=str(dossier / nom), full_page=True)
    return mesure


def parcours_interactifs(page, base, largeur, resultats):
    """Quelques gestes essentiels sur mobile. Chaque etape note PASS/FAIL, sans jamais ecrire."""
    def noter(nom, ok, detail=""):
        resultats.append({"parcours": nom, "largeur": largeur, "ok": bool(ok), "detail": detail})

    page.set_viewport_size({"width": largeur, "height": 800})
    # Menu mobile
    page.goto(base + "/", wait_until="networkidle")
    bouton = page.get_by_role("button", name="Ouvrir le menu")
    if bouton.count():
        bouton.first.click()
        page.wait_for_timeout(400)
        lien = page.get_by_role("link", name="Devis en 24h")
        visibles = [i for i in range(lien.count()) if lien.nth(i).is_visible()]
        noter("menu mobile s'ouvre et montre le CTA", len(visibles) > 0, f"{len(visibles)} CTA visible(s)")
        deb = page.evaluate("document.documentElement.scrollWidth > window.innerWidth")
        noter("menu ouvert sans debordement", not deb)
        page.get_by_role("button", name="Fermer le menu").first.click()
        page.wait_for_timeout(400)
    else:
        noter("menu mobile : bouton trouve", False)
    # Recherche
    page.goto(base + "/recherche", wait_until="networkidle")
    champ = page.locator("input[type=search], input[type=text]").first
    if champ.count():
        champ.fill("tube")
        page.wait_for_timeout(800)
        n = page.locator("a[href^='/p/']").count()
        noter("recherche 'tube' donne des fiches", n > 0, f"{n} lien(s) produit")
    else:
        noter("recherche : champ trouve", False)
    # Filtre du tableau produits (cartes sur mobile)
    page.goto(base + "/acier/armatures-beton", wait_until="networkidle")  # les puces n'existent qu'avec plusieurs familles
    avant = page.locator("a[href^='/p/']").count()
    puces = page.locator("button.whitespace-nowrap")
    if puces.count() > 1:
        puces.nth(1).click()
        page.wait_for_timeout(400)
        apres = page.locator("a[href^='/p/']").count()
        noter("filtre produits change la liste", apres != avant, f"{avant} -> {apres}")
    else:
        noter("filtre produits : puces presentes", puces.count() >= 1, f"{puces.count()} puce(s)")
    # Formulaire de devis : remplissage et envoi (la route repond 503 sans SMTP -> secours messagerie)
    page.goto(base + "/devis", wait_until="networkidle")
    page.fill("input[name=nom]", "Controle Responsive")
    page.fill("input[name=email]", "controle@example.invalid")
    page.fill("textarea[name=details]", "Demande fictive du balayage responsive, a ignorer.")
    bouton = page.get_by_role("button", name="Envoyer ma demande de devis")
    noter("devis : bouton actif une fois le formulaire valide", bouton.is_enabled())
    bouton.click()
    page.wait_for_timeout(1500)
    texte = page.locator("main").inner_text()
    noter("devis : etat final affiche (envoye ou messagerie)", ("Demande envoy" in texte) or ("messagerie" in texte.lower()))


def main():
    sortie_utf8()
    ap = argparse.ArgumentParser()
    ap.add_argument("--urls", required=True, help="fichier texte, un chemin par ligne")
    ap.add_argument("--widths", default=",".join(map(str, LARGEURS_DEFAUT)))
    ap.add_argument("--base", default=BASE_DEFAUT)
    ap.add_argument("--out", default=None)
    ap.add_argument("--captures", action="store_true", help="capture pleine page par URL et largeur")
    ap.add_argument("--interactif", action="store_true", help="joue les parcours mobiles (320, 375, 414)")
    args = ap.parse_args()

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Playwright Python absent : pip install playwright && playwright install chromium")
        return 2

    chemins = [l.strip() for l in Path(args.urls).read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")]
    largeurs = [int(x) for x in args.widths.split(",")]
    horodatage = datetime.now().strftime("%Y%m%d-%H%M")
    dossier = Path(args.out) if args.out else Path(os.environ.get("LOCALAPPDATA", ".")) / "SiteAciersGrosjean" / "qa-responsive" / horodatage
    dossier.mkdir(parents=True, exist_ok=True)

    resultats, parcours = [], []
    journal = {"console": [], "erreurs": [], "reseau": []}
    debut = time.monotonic()
    with sync_playwright() as p:
        navigateur = p.chromium.launch()
        contexte = navigateur.new_context(device_scale_factor=1, has_touch=True, is_mobile=False)
        page = contexte.new_page()
        page.on("console", lambda m: journal["console"].append(m.text) if m.type in ("error", "warning") else None)
        page.on("pageerror", lambda e: journal["erreurs"].append(str(e)))
        page.on("response", lambda r: journal["reseau"].append(f"{r.status} {r.url}") if r.status >= 400 and r.url.startswith(args.base) else None)
        for chemin in chemins:
            for largeur in largeurs:
                try:
                    m = mesurer_page(page, args.base, chemin, largeur, args.captures, dossier, journal)
                except Exception as e:  # une page qui plante est un resultat, pas une panne du balayage
                    m = {"url": chemin, "largeur": largeur, "statut": None, "erreur_balayage": str(e)[:200], "debordement": None}
                resultats.append(m)
                drapeaux = []
                if m.get("debordement"): drapeaux.append(f"DEBORDEMENT {m['scrollWidth']}>{m['innerWidth']}")
                if m.get("cibles_petites"): drapeaux.append(f"cibles<24px:{m['cibles_petites']}")
                if m.get("textes_petits"): drapeaux.append(f"textes<12px:{m['textes_petits']}")
                if m.get("erreurs_page") or m.get("console"): drapeaux.append(f"console:{len(m.get('console', []))}+{len(m.get('erreurs_page', []))}")
                if m.get("reseau"): drapeaux.append(f"reseau:{len(m['reseau'])}")
                if m.get("erreur_balayage"): drapeaux.append("ERREUR " + m["erreur_balayage"][:60])
                print(f"{chemin:<70} {largeur:>5}  {m.get('statut')}  {'  '.join(drapeaux) or 'ok'}", flush=True)
        if args.interactif:
            for largeur in (320, 375, 414):
                try:
                    parcours_interactifs(page, args.base, largeur, parcours)
                except Exception as e:
                    parcours.append({"parcours": "exception", "largeur": largeur, "ok": False, "detail": str(e)[:200]})
            for r in parcours:
                print(f"PARCOURS {r['largeur']:>4}  {'PASS' if r['ok'] else 'FAIL'}  {r['parcours']}  {r['detail']}")
        navigateur.close()

    (dossier / "resultats.json").write_text(json.dumps({"mesures": resultats, "parcours": parcours}, ensure_ascii=False, indent=1), encoding="utf-8")
    nb_deb = sum(1 for r in resultats if r.get("debordement"))
    print(f"\n{len(resultats)} mesures, {nb_deb} debordement(s), {sum(1 for r in parcours if not r['ok'])} parcours en echec, {time.monotonic() - debut:.0f} s")
    print("resultats :", dossier)
    return 1 if nb_deb or any(not r["ok"] for r in parcours) else 0


if __name__ == "__main__":
    sys.exit(main())
