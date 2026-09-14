"""
Inventaire du catalogue de www.aciersgrosjean.be (nopCommerce).

Etape 1 - exploration : sitemap + menu + categories + pagination + liens internes.
Chaque page HTML est gardee dans html/ : relancer le script reprend sans re-telecharger.
Sorties : pages.json (toutes les pages vues), produits_bruts.json, categories_brutes.json.
"""
import hashlib
import json
import os
import re
import sys
import time
import xml.etree.ElementTree as ET
from collections import deque
from pathlib import Path
from urllib.parse import parse_qsl, quote, unquote, urlencode, urljoin, urlsplit, urlunsplit

import requests
from bs4 import BeautifulSoup

BASE = "https://www.aciersgrosjean.be"
HOTE = "www.aciersgrosjean.be"
# Donnees de travail (cache HTML, JSON intermediaires) hors OneDrive et hors Git.
ICI = Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / "SiteAciersGrosjean" / "crawl"
ICI.mkdir(parents=True, exist_ok=True)
CACHE = ICI / "html"
CACHE.mkdir(exist_ok=True)
DELAI = 0.8
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/140.0 Safari/537.36 AciersGrosjean-refonte-inventaire")

session = requests.Session()
session.headers.update({"User-Agent": UA, "Accept-Language": "fr-BE,fr;q=0.9"})

EXTENSIONS_FICHIERS = re.compile(r"\.(pdf|jpe?g|png|gif|webp|svg|ico|css|js|xml|zip|docx?|xlsx?|mp4|txt)$", re.I)
CHEMINS_EXCLUS = re.compile(
    r"^/(login|register|logout|cart|wishlist|customer|passwordrecovery|newsletter|compareproducts|"
    r"changecurrency|changelanguage|changetaxtype|checkout|onepagecheckout|order|returnrequest|"
    r"privatemessages|boards|backinstocksubscribe|subscribenewsletter|eucookielawaccept|"
    r"addproducttocart|shoppingcart|uploadfile|install|admin|bin|files|t-popup|rss)(/|$)", re.I)
PARAMS_GARDES = {"pagenumber", "pagesize"}


def journal(msg):
    print(time.strftime("%H:%M:%S"), msg, flush=True)


# ---------- robots.txt (motifs avec * et $) ----------
def charger_robots():
    motifs = []
    try:
        texte = session.get(BASE + "/robots.txt", timeout=30).text
    except requests.RequestException:
        return motifs
    for ligne in texte.splitlines():
        if ligne.lower().startswith("disallow:"):
            p = ligne.split(":", 1)[1].strip()
            if p:
                rx = "^" + re.escape(p).replace(r"\*", ".*").replace(r"\$", "$")
                motifs.append(re.compile(rx, re.I))
    return motifs


ROBOTS = charger_robots()


def interdit(chemin_et_requete):
    return any(m.match(chemin_et_requete) for m in ROBOTS)


# ---------- URLs ----------
def cle_et_url(href, depuis=BASE + "/"):
    """Renvoie (cle canonique, url a demander) ou (None, None) si hors perimetre."""
    if not href:
        return None, None
    href = href.strip()
    if href.startswith(("mailto:", "tel:", "javascript:", "#")):
        return None, None
    absolu = urljoin(depuis, href)
    sp = urlsplit(absolu)
    if sp.scheme not in ("http", "https") or sp.netloc.lower() not in (HOTE, "aciersgrosjean.be"):
        return None, None
    chemin = unquote(sp.path) or "/"
    if EXTENSIONS_FICHIERS.search(chemin) or CHEMINS_EXCLUS.match(chemin):
        return None, None
    params = sorted((k.lower(), v) for k, v in parse_qsl(sp.query) if k.lower() in PARAMS_GARDES)
    if params and dict(params).get("pagenumber") == "1":
        params = [(k, v) for k, v in params if k != "pagenumber"]
    requete = urlencode(params)
    if interdit(sp.path + ("?" + sp.query if sp.query else "")) and not params:
        return None, None
    cle = chemin.rstrip("/").lower() or "/"
    if requete:
        cle += "?" + requete
    url = urlunsplit(("https", HOTE, quote(chemin, safe="/-._~!$&'()*+,;=:@"), requete, ""))
    return cle, url


def fichier_cache(cle):
    return CACHE / (hashlib.sha1(cle.encode("utf-8")).hexdigest() + ".html")


def telecharger(cle, url):
    f = fichier_cache(cle)
    meta_f = f.with_suffix(".json")
    if f.exists() and meta_f.exists():
        return json.loads(meta_f.read_text(encoding="utf-8")), f.read_text(encoding="utf-8")
    for essai in range(3):
        try:
            r = session.get(url, timeout=40)
            break
        except requests.RequestException as e:
            journal(f"  erreur reseau ({e.__class__.__name__}), nouvel essai")
            time.sleep(5 * (essai + 1))
    else:
        return {"url": url, "statut": 0, "url_finale": url}, ""
    time.sleep(DELAI)
    meta = {"url": url, "statut": r.status_code, "url_finale": r.url,
            "type_contenu": r.headers.get("Content-Type", "")}
    texte = r.text if "html" in meta["type_contenu"] else ""
    f.write_text(texte, encoding="utf-8")
    meta_f.write_text(json.dumps(meta, ensure_ascii=False), encoding="utf-8")
    return meta, texte


# ---------- analyse ----------
def txt(el):
    return re.sub(r"\s+", " ", el.get_text(" ", strip=True)).strip() if el else ""


def type_page(soup):
    page = soup.select_one("div.page")
    classes = page.get("class", []) if page else []
    for c in classes:
        if c != "page":
            return c
    return "inconnu"


def fil_ariane(soup, url):
    miettes = []
    for li in soup.select(".breadcrumb li"):
        a = li.select_one("a")
        nom = txt(li).rstrip("/").strip()
        if not nom:
            continue
        miettes.append({"nom": nom, "url": urljoin(url, a["href"]) if a and a.get("href") else None})
    return miettes


def json_ld(soup, type_voulu):
    for s in soup.find_all("script"):
        contenu = s.string or s.get_text() or ""
        if f'"@type":"{type_voulu}"' not in contenu.replace(" ", ""):
            continue
        debut = contenu.find("{")
        if debut < 0:
            continue
        try:
            return json.loads(contenu[debut:contenu.rfind("}") + 1])
        except json.JSONDecodeError:
            continue
    return None


def prix_num(texte):
    m = re.search(r"(\d[\d .  ]*,\d+|\d[\d .  ]*)\s*€", texte or "")
    if not m:
        return None
    brut = re.sub(r"[ .  ]", "", m.group(1)).replace(",", ".")
    try:
        return float(brut)
    except ValueError:
        return None


def en_float(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def analyser_produit(soup, url):
    bloc = soup.select_one("div[data-productid]")
    pid = int(bloc["data-productid"]) if bloc and bloc.get("data-productid", "").isdigit() else None
    ld = json_ld(soup, "Product") or {}
    offre = ld.get("offers") or {}
    if isinstance(offre, list):
        offre = offre[0] if offre else {}
    prix_el = soup.select_one(".overview .product-price") or soup.select_one(".product-price")
    prix_texte = txt(prix_el)
    variantes = []
    for dl in soup.select(".attributes dl"):
        for dt in dl.select("dt"):
            dd = dt.find_next_sibling("dd")
            options = [txt(o) for o in dd.select("option") if o.get("value") not in (None, "", "0")] if dd else []
            options += [txt(l) for l in dd.select("li label")] if dd else []
            variantes.append({"attribut": txt(dt).rstrip(":* ").strip(), "options": options})
    lignes_variantes = []
    for ligne in soup.select(".product-variant-list .product-variant-line"):
        lignes_variantes.append({
            "id": ligne.get("data-productid"),
            "nom": txt(ligne.select_one(".variant-name")),
            "sku": txt(ligne.select_one(".sku .value")),
            "prix": txt(ligne.select_one(".product-price")),
        })
    specs = {}
    for tr in soup.select(".product-specs-box tr"):
        cellules = tr.select("td")
        if len(cellules) >= 2:
            specs[txt(cellules[0])] = txt(cellules[1])
    images = []
    for img in soup.select(".picture-gallery img"):
        for attr in ("data-fullsize", "data-defaultsize", "src"):
            if img.get(attr):
                images.append(urljoin(url, img[attr]))
                break
    if not images and ld.get("image"):
        images = [ld["image"]] if isinstance(ld["image"], str) else list(ld["image"])
    images = list(dict.fromkeys(images))
    pdfs = []
    for el in soup.select("a[href], iframe[src]"):
        lien = el.get("href") or el.get("src") or ""
        if ".pdf" in lien.lower():
            pdfs.append({"url": urljoin(url, quote(unquote(lien), safe="/:-._~")),
                         "libelle": txt(el) or unquote(lien).rsplit("/", 1)[-1]})
    pdfs = list({p["url"]: p for p in pdfs}.values())
    lies = []
    for it in soup.select(".related-products-grid .product-item, .also-purchased-products-grid .product-item"):
        a = it.select_one(".product-title a")
        lies.append({"id": it.get("data-productid"), "nom": txt(a), "url": urljoin(url, a["href"]) if a else None})
    return {
        "id": pid,
        "nom": txt(soup.select_one(".product-name h1")) or (ld.get("name") or "").strip(),
        "fil_ariane": fil_ariane(soup, url),
        "sku": ld.get("sku") or txt(soup.select_one(".sku .value")),
        "reference_fabricant": txt(soup.select_one(".manufacturer-part-number .value")),
        "gtin": txt(soup.select_one(".gtin .value")),
        "marque": [txt(a) for a in soup.select(".manufacturers a")],
        "prix_texte": prix_texte,
        "prix_ttc": prix_num(prix_texte) if prix_texte else en_float(offre.get("price")),
        "ancien_prix": txt(soup.select_one(".old-product-price")),
        "prix_degressifs": [txt(tr) for tr in soup.select(".tier-prices tr")],
        "disponibilite": txt(soup.select_one(".availability .stock .value")) or offre.get("availability", ""),
        "variantes_attributs": variantes,
        "variantes_groupees": lignes_variantes,
        "specifications": specs,
        "description_courte": txt(soup.select_one(".short-description")),
        "description_longue": txt(soup.select_one(".full-description")),
        "images": images,
        "pdfs": pdfs,
        "produits_lies": lies,
        "tags": [txt(a) for a in soup.select(".product-tags-list a")],
        "meta_titre": txt(soup.select_one("title")),
        "meta_description": (soup.select_one('meta[name="description"]') or {}).get("content", ""),
    }


def analyser_categorie(soup, url):
    produits = []
    for it in soup.select(".products-container .product-item"):
        a = it.select_one(".product-title a")
        produits.append({"id": it.get("data-productid"), "nom": txt(a),
                         "url": urljoin(url, a["href"]) if a and a.get("href") else None,
                         "prix": txt(it.select_one(".prices"))})
    sous = [{"nom": txt(a), "url": urljoin(url, a["href"])} for a in soup.select(".sub-category-item .title a")]
    return {"nom": txt(soup.select_one(".page-title h1")) or txt(soup.select_one("h1")),
            "fil_ariane": fil_ariane(soup, url), "sous_categories": sous, "produits": produits,
            "pager": [urljoin(url, a["href"]) for a in soup.select(".pager a[href]")]}


# ---------- exploration ----------
def urls_sitemap():
    r = session.get(BASE + "/sitemap.xml", timeout=40)
    racine = ET.fromstring(r.content)
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    return [u.find("s:loc", ns).text for u in racine.findall("s:url", ns)]


def main():
    depart = time.time()
    file_attente = deque()
    vus = {}
    sitemap = urls_sitemap()
    journal(f"sitemap : {len(sitemap)} URLs, robots : {len(ROBOTS)} regles")

    def ajouter(href, depuis, origine):
        cle, url = cle_et_url(href, depuis)
        if cle and cle not in vus:
            vus[cle] = {"url": url, "origine": origine}
            file_attente.append(cle)

    ajouter(BASE + "/", BASE + "/", "depart")
    for u in sitemap:
        ajouter(u, BASE + "/", "sitemap")

    produits, categories, pages = {}, {}, {}
    n = 0
    while file_attente:
        cle = file_attente.popleft()
        url = vus[cle]["url"]
        meta, html = telecharger(cle, url)
        n += 1
        entree = {"url": url, "url_finale": meta.get("url_finale"), "statut": meta.get("statut"),
                  "origine": vus[cle]["origine"], "type": None}
        if not html:
            entree["type"] = "non-html-ou-erreur"
            pages[cle] = entree
            continue
        soup = BeautifulSoup(html, "lxml")
        tp = type_page(soup)
        entree["type"] = tp
        pages[cle] = entree
        base_liens = meta.get("url_finale") or url

        if tp == "product-details-page":
            p = analyser_produit(soup, base_liens)
            p["url"] = base_liens
            p["cle"] = cle
            p["origine_decouverte"] = vus[cle]["origine"]
            identifiant = p["id"] if p["id"] is not None else "sans-id:" + cle
            if identifiant in produits:
                produits[identifiant].setdefault("autres_urls", []).append(base_liens)
            else:
                produits[identifiant] = p
        elif tp in ("category-page", "manufacturer-page"):
            c = analyser_categorie(soup, base_liens)
            c["url"] = base_liens
            c["type"] = tp
            categories[cle] = c
            for lien in c["pager"]:
                if "pagenumber" in dict(parse_qsl(urlsplit(lien).query)):
                    ajouter(lien, base_liens, "pagination")

        # decouverte : tous les liens internes de la page (menu, contenus, produits lies)
        for a in soup.select("a[href]"):
            ajouter(a["href"], base_liens, f"lien:{tp}")
        soup.decompose()  # libere l'arbre HTML tout de suite (PC charge en memoire)

        if n % 25 == 0:
            journal(f"{n} pages lues, {len(file_attente)} en attente, {len(produits)} produits, "
                    f"{len(categories)} pages categorie ({int(time.time() - depart)} s)")

    (ICI / "pages.json").write_text(json.dumps(pages, ensure_ascii=False, indent=1), encoding="utf-8")
    (ICI / "produits_bruts.json").write_text(json.dumps(list(produits.values()), ensure_ascii=False, indent=1), encoding="utf-8")
    (ICI / "categories_brutes.json").write_text(json.dumps(categories, ensure_ascii=False, indent=1), encoding="utf-8")
    types = {}
    for p in pages.values():
        types[p["type"]] = types.get(p["type"], 0) + 1
    journal(f"FIN exploration : {n} pages, {len(produits)} produits, types = {types}")


if __name__ == "__main__":
    sys.exit(main())
