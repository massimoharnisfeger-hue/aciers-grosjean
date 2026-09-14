"""
Planches contact des images de reference (site actuel), pour les classer a l'oeil.

Les images identiques ou quasi identiques (meme photo reutilisee sur plusieurs fiches) sont regroupees
par empreinte perceptuelle : chaque groupe n'apparait qu'une fois, avec son numero (G001...).

Entree : _DEPOT/images/site-actuel/_index.json
Sorties : _DEPOT/images/site-actuel/_groupes.json   groupe -> images, categories, produits, taille
          _DEPOT/images/site-actuel/_planches/planche-NN.jpg  (24 vignettes numerotees par planche)
"""
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

PROJET = Path(__file__).resolve().parents[2]
DEST = PROJET / "_DEPOT" / "images" / "site-actuel"
VIGNETTE, COLONNES, PAR_PLANCHE = 250, 6, 24


def empreinte(img):
    """dHash 16x16 : robuste aux redimensionnements et a la compression JPEG."""
    g = ImageOps.grayscale(img).resize((17, 16), Image.LANCZOS)
    px = list(g.getdata())
    bits = 0
    for y in range(16):
        for x in range(16):
            bits = (bits << 1) | (px[y * 17 + x] > px[y * 17 + x + 1])
    return bits


def main():
    index = json.loads((DEST / "_index.json").read_text(encoding="utf-8"))
    infos, illisibles, par_contenu = [], [], {}
    for cle, im in index.items():
        if im["sha1"] in par_contenu:  # contenu identique deja lu : meme empreinte
            infos.append({**par_contenu[im["sha1"]], "cle": cle, **im})
            continue
        try:
            with Image.open(DEST / im["fichier"]) as img:
                img = img.convert("RGB")
                lu = {"hash": empreinte(img), "taille": img.size}
        except (OSError, ValueError):
            illisibles.append(im["fichier"])
            continue
        par_contenu[im["sha1"]] = lu
        infos.append({**lu, "cle": cle, **im})
    if illisibles:
        print(f"{len(illisibles)} image(s) illisible(s) :", illisibles)
    # regroupement : distance de Hamming <= 12 bits sur 256
    groupes = []
    for info in sorted(infos, key=lambda i: -i["taille"][0] * i["taille"][1]):
        for g in groupes:
            if bin(g["hash"] ^ info["hash"]).count("1") <= 12:
                g["images"].append(info)
                break
        else:
            groupes.append({"hash": info["hash"], "images": [info]})
    groupes.sort(key=lambda g: (sorted({i["categorie"] for i in g["images"]})[0], min(i["rang"] for i in g["images"])))

    sortie = {}
    for n, g in enumerate(groupes, 1):
        ref = g["images"][0]  # la plus grande
        sortie[f"G{n:03d}"] = {
            "reference": ref["fichier"], "taille": list(ref["taille"]),
            "images": [i["fichier"] for i in g["images"]],
            "categories": sorted({i["categorie"] for i in g["images"]}),
            "produits": sorted({p for i in g["images"] for p in i["produits"]}),
            "rang_min": min(i["rang"] for i in g["images"]),
        }
    (DEST / "_groupes.json").write_text(json.dumps(sortie, ensure_ascii=False, indent=1), encoding="utf-8")

    planches = DEST / "_planches"
    planches.mkdir(exist_ok=True)
    for vieille in planches.glob("*.jpg"):
        vieille.unlink()
    police = ImageFont.load_default(size=15)
    noms = list(sortie)
    for p in range(0, len(noms), PAR_PLANCHE):
        lot = noms[p:p + PAR_PLANCHE]
        lignes = (len(lot) + COLONNES - 1) // COLONNES
        planche = Image.new("RGB", (COLONNES * VIGNETTE, lignes * (VIGNETTE + 34)), "white")
        d = ImageDraw.Draw(planche)
        for i, nom in enumerate(lot):
            g = sortie[nom]
            with Image.open(DEST / g["reference"]) as img:
                img = ImageOps.contain(img.convert("RGB"), (VIGNETTE - 8, VIGNETTE - 8))
            x, y = (i % COLONNES) * VIGNETTE, (i // COLONNES) * (VIGNETTE + 34)
            planche.paste(img, (x + (VIGNETTE - img.width) // 2, y + (VIGNETTE - img.height) // 2))
            cat = g["categories"][0].split("-", 1)[-1][:24]
            d.text((x + 4, y + VIGNETTE), f"{nom} {g['taille'][0]}x{g['taille'][1]} ×{len(g['produits'])}", fill="black", font=police)
            d.text((x + 4, y + VIGNETTE + 16), cat, fill=(90, 90, 90), font=police)
        planche.save(planches / f"planche-{p // PAR_PLANCHE + 1:02d}.jpg", quality=85)
    print(f"{len(index)} images -> {len(sortie)} groupes -> {(len(noms) + PAR_PLANCHE - 1) // PAR_PLANCHE} planches")


if __name__ == "__main__":
    main()
