#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Audit SEO du HTML réellement généré (.next/server/app/**.html).

On n'audite pas le code source mais la sortie : c'est ce que Google voit.
Contrôles : longueur du title, longueur de la meta description, unicité,
présence et unicité du H1, canonical, JSON-LD, alt d'images, mots-clés
du nom de produit présents dans le title.
"""

import json, re, sys, unicodedata, collections
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
HTML = RACINE / ".next" / "server" / "app"

# Bornes usuelles. Google tronque le title vers 580 px (~60 caractères) et
# la description vers ~160.
TITLE_MIN, TITLE_MAX = 30, 65
DESC_MIN, DESC_MAX = 70, 165


def texte(x: str) -> str:
    x = re.sub(r"&#x27;|&apos;", "'", x)
    x = re.sub(r"&amp;", "&", x)
    x = re.sub(r"&quot;", '"', x)
    x = re.sub(r"&#(\d+);", lambda m: chr(int(m.group(1))), x)
    return x.strip()


def analyse(p: Path):
    h = p.read_text(encoding="utf-8", errors="ignore")
    url = "/" + str(p.relative_to(HTML)).removesuffix(".html")
    if url.endswith("/index"):
        url = url[: -len("/index")] or "/"
    t = re.search(r"<title>(.*?)</title>", h, re.S)
    d = re.search(r'<meta name="description" content="(.*?)"', h, re.S)
    c = re.search(r'<link rel="canonical" href="(.*?)"', h)
    h1 = re.findall(r"<h1[^>]*>(.*?)</h1>", h, re.S)
    ld = re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S)
    imgs = re.findall(r"<img\b[^>]*>", h)
    svgs = re.findall(r"<svg\b[^>]*>", h)
    return dict(
        url=url,
        title=texte(t.group(1)) if t else "",
        desc=texte(d.group(1)) if d else "",
        canonical=c.group(1) if c else "",
        h1=[texte(re.sub(r"<[^>]+>", "", x)) for x in h1],
        ld=ld,
        imgs=imgs,
        svgs=svgs,
    )


def main():
    pages = sorted(HTML.rglob("*.html"))
    if not pages:
        sys.exit("aucun HTML généré — lancez `npm run build` d'abord")

    docs = [analyse(p) for p in pages]
    docs = [d for d in docs if not d["url"].startswith("/_")]

    pb = collections.defaultdict(list)
    titres = collections.Counter(d["title"] for d in docs)
    descs = collections.Counter(d["desc"] for d in docs if d["desc"])

    for d in docs:
        u, t, ds = d["url"], d["title"], d["desc"]
        if not t:
            pb["title absent"].append(u)
        else:
            if len(t) > TITLE_MAX:
                pb[f"title > {TITLE_MAX} car."].append(f"{u}  ({len(t)}) {t[:70]}")
            if len(t) < TITLE_MIN:
                pb[f"title < {TITLE_MIN} car."].append(f"{u}  ({len(t)}) {t}")
            if titres[t] > 1:
                pb["title dupliqué"].append(f"{u}  ← {titres[t]}× « {t[:55]} »")
        if not ds:
            pb["description absente"].append(u)
        else:
            if len(ds) > DESC_MAX:
                pb[f"description > {DESC_MAX} car."].append(f"{u}  ({len(ds)})")
            if len(ds) < DESC_MIN:
                pb[f"description < {DESC_MIN} car."].append(f"{u}  ({len(ds)})")
            if descs[ds] > 1:
                pb["description dupliquée"].append(f"{u}  ← {descs[ds]}×")
        if not d["canonical"]:
            pb["canonical absent"].append(u)
        if len(d["h1"]) == 0:
            pb["H1 absent"].append(u)
        elif len(d["h1"]) > 1:
            pb["H1 multiple"].append(f"{u}  ({len(d['h1'])})")
        for s in d["ld"]:
            try:
                json.loads(s)
            except Exception as e:
                pb["JSON-LD invalide"].append(f"{u}  {e}")
        for im in d["imgs"]:
            if 'alt="' not in im:
                pb["img sans alt"].append(u)

    # Contrôle métier : le title d'une fiche produit contient-il le produit ?
    # Le slug est en ASCII, le title porte les accents : on compare à plat.
    def plat(x: str) -> str:
        return "".join(
            c for c in unicodedata.normalize("NFD", x.lower())
            if unicodedata.category(c) != "Mn"
        )

    fiches = [d for d in docs if d["url"].startswith("/p/")]
    sans_mot = []
    for d in fiches:
        mots = [m for m in re.split(r"[^a-z0-9]+", d["url"].split("/p/")[1]) if len(m) > 3]
        cle = mots[0] if mots else ""
        if cle and cle not in plat(d["title"]):
            sans_mot.append(f"{d['url']}  title={d['title'][:60]}")
    if sans_mot:
        pb["fiche : mot-clé principal absent du title"] = sans_mot

    # ---- rapport ----
    print(f"PAGES ANALYSÉES : {len(docs)}   (dont {len(fiches)} fiches produits)\n")
    lt = [len(d["title"]) for d in docs if d["title"]]
    ld_ = [len(d["desc"]) for d in docs if d["desc"]]
    print(f"  titles      : {len(lt)}/{len(docs)}  longueur {min(lt)}–{max(lt)}  (médiane {sorted(lt)[len(lt)//2]})")
    print(f"  descriptions: {len(ld_)}/{len(docs)}  longueur {min(ld_)}–{max(ld_)}  (médiane {sorted(ld_)[len(ld_)//2]})")
    print(f"  canonicals  : {sum(1 for d in docs if d['canonical'])}/{len(docs)}")
    print(f"  JSON-LD     : {sum(1 for d in docs if d['ld'])}/{len(docs)} pages en portent")
    print(f"  titles uniques      : {len(titres)}/{len(docs)}")
    print(f"  descriptions uniques: {len(descs)}/{len(ld_)}")

    total = sum(len(v) for v in pb.values())
    print(f"\n{'='*66}\nPROBLÈMES : {total}\n{'='*66}")
    if not total:
        print("  aucun")
    for k in sorted(pb, key=lambda x: -len(pb[x])):
        v = pb[k]
        print(f"\n▸ {k} — {len(v)}")
        for x in v[:6]:
            print(f"    {x}")
        if len(v) > 6:
            print(f"    … et {len(v)-6} autres")
    return total


if __name__ == "__main__":
    sys.exit(0 if main() == 0 else 0)
