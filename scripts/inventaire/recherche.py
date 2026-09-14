"""Controle de completude : la recherche du site renvoie-t-elle des produits absents de l'inventaire ?"""
import json
import os
import time
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit

import requests
from bs4 import BeautifulSoup

# Donnees de travail (cache HTML, JSON intermediaires) hors OneDrive et hors Git.
ICI = Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / "SiteAciersGrosjean" / "crawl"
ICI.mkdir(parents=True, exist_ok=True)
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/140.0 Safari/537.36 AciersGrosjean-refonte-inventaire")
TERMES = ["acier", "inox", "alu", "tôle", "tube", "vis", "poteau", "panneau", "coupe", "vasque"]

connus = {p["id"] for p in json.loads((ICI / "produits_bruts.json").read_text(encoding="utf-8"))}
session = requests.Session()
session.headers.update({"User-Agent": UA})
resultats = {}
tous = set()
for terme in TERMES:
    ids, page, pages = [], 1, 0
    while True:
        params = {"q": terme, "pagesize": 9}
        if page > 1:
            params["pagenumber"] = page
        r = session.get("https://www.aciersgrosjean.be/search?" + urlencode(params), timeout=40)
        time.sleep(1.5)
        pages += 1
        soup = BeautifulSoup(r.text, "lxml")
        for it in soup.select(".search-results .product-item, .products-container .product-item"):
            if (it.get("data-productid") or "").isdigit():
                ids.append(int(it["data-productid"]))
        suivantes = [int(dict(parse_qsl(urlsplit(a["href"]).query)).get("pagenumber", 0))
                     for a in soup.select(".pager a[href]")]
        soup.decompose()
        if not suivantes or max(suivantes) <= page or pages > 60:
            break
        page += 1
    ids = sorted(set(ids))
    tous |= set(ids)
    resultats[terme] = {"pages": pages, "nb": len(ids), "ids_inconnus": sorted(set(ids) - connus)}
    print(f"{terme:12s} {len(ids):4d} produits sur {pages} page(s), inconnus : {resultats[terme]['ids_inconnus']}", flush=True)

resultats["_bilan"] = {"ids_trouves_par_la_recherche": len(tous), "ids_inconnus": sorted(tous - connus),
                      "connus_jamais_trouves_par_la_recherche": len(connus - tous)}
(ICI / "recherche.json").write_text(json.dumps(resultats, ensure_ascii=False, indent=1), encoding="utf-8")
print("BILAN", resultats["_bilan"])
