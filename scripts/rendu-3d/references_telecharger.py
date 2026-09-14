"""
Telecharge les images du site actuel qui servent de references visuelles aux rendus 3D.

Entree : _DOCS/catalogue-site-actuel/images.csv (id_produit;produit;rang;url), lib/site-actuel.json, lib/catalogue.ts
Sortie : _DEPOT/images/site-actuel/<categorie>/<image>.jpeg (hors Git)
         _DEPOT/images/site-actuel/_index.json : image -> url, categorie, produits, rang, sha1, taille
Une image deja presente n'est pas retelechargee (reprise possible). Requetes espacees.
"""
import csv
import hashlib
import json
import re
import sys
import time
from pathlib import Path

import requests

PROJET = Path(__file__).resolve().parents[2]
DEST = PROJET / "_DEPOT" / "images" / "site-actuel"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/140.0 Safari/537.36 AciersGrosjean-refonte-references")
PAUSE = 0.6


def categories_refonte():
    """id produit du site actuel -> (slug refonte, categorie refonte)."""
    reel = json.loads((PROJET / "lib" / "site-actuel.json").read_text(encoding="utf-8"))
    ts = (PROJET / "lib" / "catalogue.ts").read_text(encoding="utf-8")
    cat = dict(re.findall(r'^\s*"([^"]+)": \{ slug: "[^"]+", nom: "(?:[^"\\]|\\.)*", categorie: "([^"]+)"', ts, re.M))
    return {d["id"]: (slug, cat.get(slug, "")) for slug, d in reel.items()}


def cle_image(url):
    """0003804_301d...e9837_625.jpeg -> 0003804_301d...e9837 (meme photo, taille differente)."""
    nom = url.rsplit("/", 1)[-1]
    return re.sub(r"_\d{2,4}(\.\w+)$", r"\1", nom).rsplit(".", 1)[0]


def main():
    par_id = categories_refonte()
    lignes = list(csv.DictReader(open(PROJET / "_DOCS/catalogue-site-actuel/images.csv", encoding="utf-8-sig"), delimiter=";"))
    images = {}
    for l in lignes:
        pid = int(l["id_produit"])
        cle = cle_image(l["url"])
        slug, categorie = par_id.get(pid, (None, ""))
        dossier = categorie.strip("/").replace("/", "-") if categorie else "hors-catalogue"
        im = images.setdefault(cle, {"url": None, "categorie": dossier, "produits": [], "rang": int(l["rang"])})
        # la version pleine taille (sans suffixe) est preferee
        if im["url"] is None or not re.search(r"_\d{2,4}\.\w+$", l["url"]):
            im["url"] = l["url"]
        if slug and slug not in im["produits"]:
            im["produits"].append(slug)
        im["rang"] = min(im["rang"], int(l["rang"]))
    print(f"{len(lignes)} adresses -> {len(images)} images distinctes", flush=True)
    if "--compter" in sys.argv:
        return

    index_f = DEST / "_index.json"
    DEST.mkdir(parents=True, exist_ok=True)
    index = json.loads(index_f.read_text(encoding="utf-8")) if index_f.exists() else {}
    session = requests.Session()
    session.headers.update({"User-Agent": UA})
    for n, (cle, im) in enumerate(sorted(images.items()), 1):
        dossier = DEST / im["categorie"]
        dossier.mkdir(parents=True, exist_ok=True)
        ext = im["url"].rsplit(".", 1)[-1].lower()
        cible = dossier / f"{cle}.{ext}"
        if not cible.exists():
            try:
                r = session.get(im["url"], timeout=60)
                time.sleep(PAUSE)
                if r.status_code != 200 or not r.headers.get("Content-Type", "").startswith("image"):
                    print(f"ECHEC {r.status_code} {im['url']}", flush=True)
                    continue
                cible.write_bytes(r.content)
            except requests.RequestException as e:
                print(f"ERREUR {e.__class__.__name__} {im['url']}", flush=True)
                continue
        contenu = cible.read_bytes()
        index[cle] = {**im, "fichier": str(cible.relative_to(DEST)).replace("\\", "/"),
                      "sha1": hashlib.sha1(contenu).hexdigest(), "octets": len(contenu)}
        if n % 50 == 0:
            index_f.write_text(json.dumps(index, ensure_ascii=False, indent=1), encoding="utf-8")
            print(f"{n}/{len(images)}", flush=True)
    index_f.write_text(json.dumps(index, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"FIN : {len(index)} images, {sum(v['octets'] for v in index.values()) / 1e6:.1f} Mo, "
          f"{len({v['sha1'] for v in index.values()})} contenus distincts", flush=True)


if __name__ == "__main__":
    main()
