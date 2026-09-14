"""
Controles automatiques des visuels 3D, sur toutes les images d'une ou plusieurs familles, avant la verification
independante (agent verificateur-rendus) et l'integration sur le site.

  python scripts/rendu-3d/controler_rendus.py poutrelle-ipe [poutrelle-hea ...]

Pour chaque famille (cle `famille` de scripts/rendu-3d/donnees/produits.json) :
- fichiers : <slug>.png (rendu brut), <slug>-caracteristiques.png/.webp/.controles.json par fiche,
  studio-<famille>.png et studio-<famille>-studio.png/.webp pour la categorie ;
- images finales en 1600 x 1200, WebP < 200 Ko ;
- piece entierement dans le cadre (rendu brut), et a gauche de la fiche technique sur le visuel caracteristiques ;
- photo studio : marges d'un blanc pur ;
- visuel caracteristiques : aucun probleme d'etiquette releve par habiller.py ; chaque texte ecrit = donnee sourcee
  non supposee ; meme valeur que la fiche produit du site (lib/catalogue.ts + lib/site-actuel.json).
Ecrit des planches contact (12 images) dans %LOCALAPPDATA%/SiteAciersGrosjean/rendu3d/controle/.
Code de sortie 1 s'il reste un ecart.
"""
import json
import os
import re
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFont

from habiller import FINITIONS, titre_image

ICI = Path(__file__).resolve().parent
PROJET = ICI.parents[1]
TRAVAIL = Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / "SiteAciersGrosjean" / "rendu3d"
FINAL, CONTROLE = TRAVAIL / "final", TRAVAIL / "controle"
LARGEUR, HAUTEUR, WEBP_MAX_KO = 1600, 1200, 200
COLONNE_FICHE = 0.655  # debut de la fiche technique (habiller.py)

# libelles des specifications de la page produit -> cles des donnees (plusieurs cles : « 100 × 50 mm »)
PAGE = {"Hauteur (h)": ["h"], "Largeur d'aile (b)": ["b"], "Épaisseur d'âme (tw)": ["tw"], "Épaisseur d'aile (tf)": ["tf"],
        "Ailes": ["a", "b"], "Section": ["h", "b"], "Largeur": ["b"], "Épaisseur": ["t"], "Diamètre": ["d"],
        "Diamètre extérieur": ["d"], "Surface": ["surface"], "Nuance": ["nuance"], "Norme": ["norme"]}
PAGE_PAR_SERIE = {"CARRE": {"Section": ["a", "a"]}, "TOLE": {"Format": ["L", "l"], "Épaisseur": ["e"]},
                  "TREILLIS": {"Maille": ["maille"], "Fil": ["d"], "Panneau": ["format"]},
                  "U-ALU": {"Section": ["b", "h", "b"], "Épaisseur": ["tw"]},
                  "TOLE-RELIEF": {"Format": ["L", "l"], "Épaisseur": ["e", "e_total"]},
                  "TOLE-PERFOREE": {"Format": ["L", "l"], "Épaisseur": ["e"]}}
COTES_AFFICHABLES = {"h", "b", "tw", "tf", "a", "t", "d", "L", "l", "e", "e_total", "nuance", "norme"}


def nombre(texte):
    m = re.search(r"-?\d+(?:[.,]\d+)?", str(texte))
    return float(m.group(0).replace(",", ".")) if m else None


def meme_valeur(a, b):
    na, nb = nombre(a), nombre(b)
    if isinstance(a, (int, float)) or isinstance(b, (int, float)):
        return na is not None and nb is not None and abs(na - nb) < 1e-6
    return str(a).strip() == str(b).strip()


def specs_page():
    """slug -> {libelle: valeur} tel qu'affiche par la page (specs du catalogue, poids et finition du site actuel)."""
    ts = (PROJET / "lib" / "catalogue.ts").read_text(encoding="utf-8")
    reel = json.loads((PROJET / "lib" / "site-actuel.json").read_text(encoding="utf-8"))
    desc = json.loads((PROJET / "lib" / "descriptions-site-actuel.json").read_text(encoding="utf-8"))
    pages = {}
    for m in re.finditer(r'^\s*"([^"]+)": \{ slug: .*?specs: \[(.*)\] \},$', ts, re.M):
        specs = dict(re.findall(r'\{ label: "([^"]+)", valeur: "([^"]*)" \}', m.group(2)))
        r = reel.get(m.group(1), {})
        specs.pop("Poids", None)  # remplace a la fusion quand le site actuel donne un poids
        for cle in r.get("specsRetirees", []):
            specs.pop(cle, None)
        if r.get("kg") is not None:
            specs["Poids"] = r["kg"]
        if r.get("finition"):
            specs["Finition"] = r["finition"]
        d = desc.get(m.group(1), {})  # la description est affichée sur la page, sous les spécifications
        specs["_texte"] = d.get("courte", "") + " " + " ".join(b.get("texte", " ".join(b.get("items", [])))
                                                             for b in d.get("blocs", []))
        pages[m.group(1)] = specs
    return pages


def cadre_piece(chemin):
    """Boite des pixels opaques du rendu brut (la piece, sans l'ombre)."""
    with Image.open(chemin) as img:
        alpha = img.convert("RGBA").split()[3]
    return alpha.point(lambda v: 255 if v >= 250 else 0).getbbox()


def part_noire(chemin, creux=False):
    """Part des pixels quasi noirs dans la silhouette de la pièce (rendu brut). Une géométrie cassée (faces
    retournées, arrondi plus grand que l'épaisseur) donne de grandes zones noires ; l'intérieur d'un tube est
    sombre à bon droit, d'où un seuil plus haut pour les sections creuses."""
    with Image.open(chemin) as img:
        rgba = img.convert("RGBA")
    r, g, b, a = rgba.split()
    clair = ImageChops.lighter(ImageChops.lighter(r, g), b)
    dans_piece = sum(1 for v in a.tobytes() if v >= 250)
    noirs = sum(1 for v, al in zip(clair.tobytes(), a.tobytes()) if al >= 250 and v <= 6)
    return noirs / max(dans_piece, 1)


def jours_rappel(chemin, points):
    """Écart en pixels entre le début de chaque ligne de rappel et le pixel de pièce le plus proche (transparence du
    rendu brut). Vérification indépendante des cornières : rappels à 67 px de la pièce sur les images rendues avant
    le correctif du jour. Distance au plus proche plutôt que le long du trait : sur les petites sections, le talon
    chanfreiné passe à côté du prolongement du trait. -> {clé: (jour ou None au-delà de la fenêtre, longueur)}"""
    with Image.open(chemin) as img:
        alpha = img.convert("RGBA").split()[3]
    jours = {}
    for cle, debut in points.items():
        fin = points.get(cle[:-len("_debut")] + "_fin") if cle.startswith("rappel_") and cle.endswith("_debut") else None
        if not fin:
            continue
        longueur = ((debut[0] - fin[0]) ** 2 + (debut[1] - fin[1]) ** 2) ** 0.5
        if longueur < 1:
            continue
        rayon = int(max(40, min(3 * longueur, 200)))
        x0, y0 = int(debut[0]) - rayon, int(debut[1]) - rayon
        cote = 2 * rayon + 1
        fenetre = alpha.crop((x0, y0, x0 + cote, y0 + cote)).tobytes()  # hors image : transparent
        meilleur = None
        for i, v in enumerate(fenetre):
            if v >= 250:
                yy, xx = divmod(i, cote)
                d2 = (x0 + xx - debut[0]) ** 2 + (y0 + yy - debut[1]) ** 2
                if meilleur is None or d2 < meilleur:
                    meilleur = d2
        jour = round(meilleur ** 0.5) if meilleur is not None and meilleur <= rayon * rayon else None
        jours[cle] = (jour, longueur)
    return jours


def marges_blanches(chemin, bande=16):
    with Image.open(chemin) as img:
        rgb = img.convert("RGB")
    w, h = rgb.size
    zones = [(0, 0, w, bande), (0, h - bande, w, h), (0, 0, bande, h), (w - bande, 0, w, h)]
    total = 0
    for z in zones:
        r, g, b = rgb.crop(z).split()
        total += sum(1 for v in ImageChops.darker(ImageChops.darker(r, g), b).tobytes() if v < 255)
    return total


def planches(famille, images):
    CONTROLE.mkdir(parents=True, exist_ok=True)
    for vieille in CONTROLE.glob(f"{famille}-planche-*.jpg"):
        vieille.unlink()
    tw, th, legende = 520, 390, 26
    police = ImageFont.load_default(size=16)
    for n in range(0, len(images), 12):
        lot = images[n:n + 12]
        lignes = (len(lot) + 2) // 3
        planche = Image.new("RGB", (3 * tw, lignes * (th + legende)), "white")
        d = ImageDraw.Draw(planche)
        for i, chemin in enumerate(lot):
            x, y = (i % 3) * tw, (i // 3) * (th + legende)
            with Image.open(chemin) as img:
                planche.paste(img.convert("RGB").resize((tw - 8, th - 6), Image.LANCZOS), (x + 4, y + 3))
            d.text((x + 6, y + th + 3), chemin.stem, fill=(60, 60, 60), font=police)
        planche.save(CONTROLE / f"{famille}-planche-{n // 12 + 1:02d}.jpg", quality=88)
    return sorted(CONTROLE.glob(f"{famille}-planche-*.jpg"))


def controler(famille, produits, pages):
    ecarts = []
    slugs = sorted(s for s, p in produits.items() if p["famille"] == famille)
    if not slugs:
        return [f"{famille} : aucune fiche dans produits.json"], []

    def fichier(nom):
        chemin = FINAL / nom
        if not chemin.exists():
            ecarts.append(f"{nom} : manquant")
            return None
        return chemin

    def image_finale(nom):
        png, webp = fichier(nom + ".png"), fichier(nom + ".webp")
        if png:
            with Image.open(png) as img:
                if img.size != (LARGEUR, HAUTEUR):
                    ecarts.append(f"{png.name} : {img.size[0]} x {img.size[1]} au lieu de {LARGEUR} x {HAUTEUR}")
        if webp and webp.stat().st_size > WEBP_MAX_KO * 1024:
            ecarts.append(f"{webp.name} : {webp.stat().st_size // 1024} Ko (> {WEBP_MAX_KO} Ko)")
        return png

    # photo studio de la categorie
    studio = f"studio-{famille}"
    images = []
    brut = fichier(studio + ".png")
    png = image_finale(studio + "-studio")
    if brut:
        x0, y0, x1, y1 = cadre_piece(brut) or (0, 0, LARGEUR, HAUTEUR)
        if x0 < LARGEUR * 0.02 or y0 < HAUTEUR * 0.02 or x1 > LARGEUR * 0.98 or y1 > HAUTEUR * 0.98:
            ecarts.append(f"{brut.name} : piece trop pres du bord ({x0}, {y0}, {x1}, {y1})")
    if png:
        images.append(png)
        n = marges_blanches(png)
        if n:
            ecarts.append(f"{png.name} : {n} pixels non blancs dans les marges")

    versions = set()  # empreintes du code de rendu (rendu_profil.py) des images de la famille
    for slug in slugs:
        p, nom = produits[slug], slug + "-caracteristiques"
        brut = fichier(slug + ".png")
        png = image_finale(nom)
        if png:
            images.append(png)
        if brut:
            x0, y0, x1, y1 = cadre_piece(brut) or (0, 0, LARGEUR, HAUTEUR)
            if x0 < LARGEUR * 0.02 or y0 < HAUTEUR * 0.02 or y1 > HAUTEUR * 0.98:
                ecarts.append(f"{slug} : piece trop pres du bord ({x0}, {y0}, {x1}, {y1})")
            if x1 > LARGEUR * (COLONNE_FICHE - 0.01):
                ecarts.append(f"{slug} : la piece deborde sous la fiche technique (x = {x1})")
            creux = p["valeurs"].get("serie", {}).get("valeur") in ("TC", "TR", "TUBE-ROND")
            noir = part_noire(brut, creux)
            if noir > (0.35 if creux else 0.02):
                ecarts.append(f"{slug} : {noir:.0%} de la piece en noir pur (geometrie cassee ?)")
            geo = FINAL / (slug + ".json")
            if geo.exists():
                infos = json.loads(geo.read_text(encoding="utf-8"))
                versions.add(infos.get("code"))
                for cle, (jour, longueur) in sorted(jours_rappel(brut, infos["points"]).items()):
                    if jour is None:
                        ecarts.append(f"{slug} : {cle} loin de toute piece (fenetre de recherche depassee)")
                    elif jour > 25 or jour > longueur / 2:
                        ecarts.append(f"{slug} : {cle} decollee de la piece ({jour} px pour un trait de {longueur:.0f} px)")
        ctrl = fichier(nom + ".controles.json")
        if not ctrl:
            continue
        c = json.loads(ctrl.read_text(encoding="utf-8"))
        ecarts += [f"{slug} : {pb}" for pb in c["problemes"]]
        titre = titre_image(p["nom"])
        if c["titre"] != titre:
            ecarts.append(f"{slug} : titre « {c['titre']} » au lieu de « {titre} »")
        valeurs = p["valeurs"]
        fiche = {label: ecrit for label, _, _, ecrit in c["fiche"]}
        for label, lettre, cle, ecrit in c["fiche"]:
            d = valeurs.get(cle)
            if not d:
                ecarts.append(f"{slug} : « {label} {ecrit} » ecrit sans donnee sourcee")
            elif d.get("supposee"):
                ecarts.append(f"{slug} : « {label} » affiche une valeur supposee")
            elif cle == "finition":
                if ecrit != FINITIONS.get(d["valeur"], d["valeur"]):
                    ecarts.append(f"{slug} : finition « {ecrit} » ≠ donnee « {d['valeur']} »")
            elif not meme_valeur(d["valeur"], ecrit):
                ecarts.append(f"{slug} : « {label} {ecrit} » ≠ donnee {d['valeur']}")
        for lettre, cle, ecrit in c["pastilles"]:
            d = valeurs.get(cle)
            if not d or d.get("supposee") or not meme_valeur(d["valeur"], ecrit):
                ecarts.append(f"{slug} : pastille {lettre} « {ecrit} » ≠ donnee {d and d['valeur']}")
        # l'image dit la meme chose que la page
        page = pages.get(slug)
        if page is None:
            ecarts.append(f"{slug} : fiche absente de lib/catalogue.ts")
            continue
        affiche = {cle for _, _, cle, _ in c["fiche"]} | {cle for _, cle, _ in c["pastilles"]}
        couvertes = set()
        serie = valeurs.get("serie", {}).get("valeur")
        for libelle, cles in {**PAGE, **PAGE_PAR_SERIE.get(serie, {})}.items():
            if libelle not in page:
                continue
            couvertes.update(cles)
            if cles in (["nuance"], ["norme"], ["surface"]):  # textes : égalité stricte
                if cles[0] not in affiche:
                    ecarts.append(f"{slug} : {libelle} « {page[libelle]} » sur la page, absente de l'image")
                elif valeurs[cles[0]]["valeur"] != page[libelle]:
                    ecarts.append(f"{slug} : {libelle} page « {page[libelle]} » ≠ image « {valeurs[cles[0]]['valeur']} »")
                continue
            nombres = [float(x.replace(",", ".")) for x in re.findall(r"\d+(?:[.,]\d+)?", str(page[libelle]))]
            attendus = []  # valeurs numériques, ou nombres contenus dans un texte (« 150 × 150 mm »)
            for k in cles:
                if k in valeurs:
                    val = valeurs[k]["valeur"]
                    attendus += ([float(x.replace(",", ".")) for x in re.findall(r"\d+(?:[.,]\d+)?", val)]
                                 if isinstance(val, str) else [val])
            if len(nombres) != len(attendus) or any(abs(n - a) > 1e-6 for n, a in zip(nombres, attendus)):
                ecarts.append(f"{slug} : {libelle} page « {page[libelle]} » ≠ image {attendus}")
        for cle in sorted(affiche & COTES_AFFICHABLES - couvertes):
            if cle in ("nuance", "norme") and str(valeurs[cle]["valeur"]) in page["_texte"]:
                continue  # écrite dans la description de la page
            ecarts.append(f"{slug} : « {cle} » sur l'image, absent de la page")
        if "Poids" in fiche and not meme_valeur(page.get("Poids"), fiche["Poids"]):
            ecarts.append(f"{slug} : poids page {page.get('Poids')} ≠ image {fiche['Poids']}")
        if "Finition" in fiche and fiche["Finition"] != FINITIONS.get(page.get("Finition"), page.get("Finition")):
            ecarts.append(f"{slug} : finition page {page.get('Finition')} ≠ image {fiche['Finition']}")
    if len(versions) > 1:  # reprise partielle : refaire la famille, ou au moins recalculer ses points (--points-seuls)
        ecarts.append(f"{famille} : visuels issus de {len(versions)} versions du code de rendu ({', '.join(sorted(str(v) for v in versions))})")
    return ecarts, planches(famille, images) if images else []


def main():
    familles = sys.argv[1:]
    if not familles:
        raise SystemExit(__doc__)
    produits = json.loads((ICI / "donnees" / "produits.json").read_text(encoding="utf-8"))
    pages = specs_page()
    total = 0
    for famille in familles:
        ecarts, fichiers = controler(famille, produits, pages)
        total += len(ecarts)
        n = sum(1 for p in produits.values() if p["famille"] == famille)
        print(f"== {famille} : {n} fiches + 1 photo studio | {len(ecarts)} ecart(s)")
        for e in ecarts:
            print("   -", e)
        for f in fichiers:
            print("   planche :", f)
    sys.exit(1 if total else 0)


if __name__ == "__main__":
    main()
