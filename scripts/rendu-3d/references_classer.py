"""
Classement des images de reference du site actuel, fait a l'oeil sur les planches contact
(_DEPOT/images/site-actuel/_planches, groupes de references_planches.py).

Types : photo (vraie photo du stock ou d'un produit), rendu (image de synthese), schema (dessin cote),
banque (image de banque ou generee, probable), ambiance (mise en situation du fabricant),
packshot (photo produit detouree / fabricant), rayon (photo prise en rayon), motif (dessin 2D), vide (sans image).

Sortie : _DOCS/rendus-3d/references.csv (une ligne par image) et _DOCS/rendus-3d/references-groupes.csv.
"""
import csv
import json
from collections import Counter
from pathlib import Path

PROJET = Path(__file__).resolve().parents[2]
DEST = PROJET / "_DEPOT" / "images" / "site-actuel"

# groupe : (type, filigrane, ce que l'image apprend)
C = {
    "G001": ("rendu", "", "ronds à béton crénelés, acier gris"),
    "G002": ("photo", "", "treillis soudés empilés, acier brut rouillé"),
    "G003": ("photo", "", "treillis soudés en pile, acier brut"),
    "G004": ("schema", "", "treillis : cotes A, B, C, D, E"),
    "G005": ("photo", "", "treillis en pile, extrémités peintes orange"),
    "G006": ("photo", "", "HEA en GPP : primaire rouge-brun mat"),
    "G007": ("schema", "", "section en I : A, B, C, D"),
    "G008": ("photo", "", "HEB en GPP, gros plan : primaire rouge-brun"),
    "G009": ("rendu", "", "IPE, acier gris uni (basse définition)"),
    "G010": ("photo", "", "IPE en GPP en pile : primaire rouge-brun, extrémités peintes"),
    "G011": ("schema", "", "section IPE : A, B, C, D"),
    "G012": ("photo", "", "UPN brutes : calamine noire, rouille légère, marques de peinture jaune-vert en bout"),
    "G013": ("schema", "", "section en U : A, B, C (ailes dessinées parallèles)"),
    "G014": ("rendu", "", "carrés pleins, acier gris"),
    "G015": ("schema", "", "carré plein : A, B"),
    "G016": ("schema", "", "profil en T : A, B, C — ERREUR du site actuel : aussi affiché sur une fiche carré plein"),
    "G017": ("rendu", "", "cornière égale, acier gris"),
    "G018": ("schema", "", "cornière : A, B, C"),
    "G019": ("banque", "", "cornières d'aspect galvanisé, basse définition : ne correspond pas à l'acier LAC"),
    "G020": ("photo", "", "cornières inégales : acier brut, calamine et rouille"),
    "G021": ("schema", "", "cornière inégale : A, B, C"),
    "G022": ("rendu", "", "fer T, acier gris"),
    "G023": ("photo", "", "fers T en vrac : acier brut, marques de peinture verte"),
    "G024": ("rendu", "", "large plat, acier sombre"),
    "G025": ("schema", "", "plat : A, B"),
    "G026": ("photo", "", "large plats en pile : calamine grise"),
    "G027": ("rendu", "", "plat, acier gris"),
    "G028": ("photo", "", "plats en pile : extrémités peintes jaune"),
    "G029": ("rendu", "", "rond plein, acier gris"),
    "G030": ("schema", "", "rond : A"),
    "G031": ("schema", "", "tôle : A, B, C"),
    "G032": ("banque", "", "surface corten rouillée, basse définition"),
    "G033": ("banque", "Adobe Stock (vu à la loupe)", "pile de tôles, même image que G035"),
    "G034": ("banque", "", "tôles brillantes en usine, image lissée"),
    "G035": ("banque", "Adobe Stock (visible)", "pile de tôles laminées"),
    "G036": ("photo", "", "tôle LaserpressPlus : marquage « LASERPRESSPLUS 240 »"),
    "G037": ("banque", "", "tôles brillantes, basse définition"),
    "G038": ("photo", "", "tôle larmée : relief en grains de riz croisés, acier brut"),
    "G039": ("photo", "", "tôle perforée à trous aléatoires (origine incertaine)"),
    "G040": ("motif", "", "perforation carrée (C10 U15)"),
    "G041": ("motif", "", "perforation ronde, grands trous"),
    "G042": ("motif", "", "perforation ronde, petits trous"),
    "G043": ("photo", "", "tôles quarto épaisses : calamine sombre"),
    "G044": ("rendu", "", "tube carré, acier gris"),
    "G045": ("photo", "", "tubes carrés en pile : acier noir brut, cordon de soudure non visible"),
    "G046": ("schema", "", "tube carré : A, B, C"),
    "G047": ("rendu", "", "tube rectangulaire, acier gris"),
    "G048": ("photo", "", "tubes rectangulaires en pile : acier brut"),
    "G049": ("schema", "", "tube rectangulaire : A, B, C"),
    "G050": ("rendu", "", "tube rond, acier gris"),
    "G051": ("schema", "", "tube rond : A, B"),
    "G052": ("banque", "", "tubes ronds en pile, basse définition"),
    "G053": ("photo", "", "cornières alu : aluminium brut mat clair"),
    "G054": ("photo", "", "plats alu : aluminium brut"),
    "G055": ("photo", "", "profil T alu : aluminium brut"),
    "G056": ("schema", "", "profil T : A, B, C"),
    "G057": ("photo", "", "profils U alu : paroi fine, aluminium brut"),
    "G058": ("schema", "", "profil U : A, B, C, D"),
    "G059": ("banque", "", "tôles alu brillantes, basse définition"),
    "G060": ("photo", "", "tôle alu striée : barres en diagonale (quintette)"),
    "G061": ("photo", "", "tubes carrés alu"),
    "G062": ("schema", "", "tube carré : A, B, C"),
    "G063": ("photo", "", "tubes rectangulaires alu"),
    "G064": ("schema", "", "tube rectangulaire : A, B, C"),
    "G065": ("photo", "", "tubes ronds alu"),
    "G066": ("vide", "", "vignette « NO IMAGE » du site actuel"),
    "G067": ("banque", "", "cornières inox brossé sur fond blanc, image lissée"),
    "G068": ("banque", "", "plats inox sur fond blanc, image lissée"),
    "G069": ("banque", "", "ronds inox sur fond blanc, image lissée"),
    "G070": ("banque", "", "tôles inox brossé, image lissée"),
    "G071": ("banque", "", "tubes carrés inox en pyramide sur fond blanc"),
    "G072": ("banque", "", "tubes rectangulaires inox sur fond blanc"),
    "G073": ("banque", "", "tubes ronds inox en pyramide sur fond blanc"),
    "G074": ("ambiance", "", "bordure corten au jardin"),
    "G075": ("ambiance", "", "bordure galvanisée au jardin"),
    "G076": ("packshot", "", "bordure : bande avec retour plié en tête (forme du 150/25)"),
    "G077": ("packshot", "", "clé de montage brides rapides, bandeau Grosjean"),
    "G078": ("packshot", "", "fixation bride 30 NV noir : vis, écrou, bride plastique noire"),
    "G079": ("packshot", "", "fixations brides 30 NV noir (50 pièces)"),
    "G080": ("packshot", "", "bride rapide inox"),
    "G081": ("packshot", "", "kit 12 serveurs Clogriff : cale plastique noire"),
    "G082": ("packshot", "", "kit 12 serveurs Clogriff en sachet"),
    "G083": ("ambiance", "", "panneau Plis 205 fil 5/4 RAL 6005 posé"),
    "G084": ("photo", "", "panneaux de clôture sur palette : vert foncé"),
    "G085": ("photo", "", "panneaux de clôture sur palettes"),
    "G086": ("photo", "", "panneaux de clôture sur palette"),
    "G087": ("ambiance", "", "poteau Clogriff 64 posé, RAL 6005"),
    "G088": ("ambiance", "", "poteau Cloplus 40 posé, RAL 6005, légende « (ALU) »"),
    "G089": ("packshot", "", "marches caillebotis perforées antidérapantes, logo Gi"),
    "G090": ("packshot", "", "marche caillebotis perforée, logo Gi"),
    "G091": ("packshot", "", "marche caillebotis à grille, logo Gi"),
    "G092": ("packshot", "", "caillebotis galvanisés en pile, logo Gi"),
    "G093": ("photo", "", "caillebotis galvanisés au dépôt"),
    "G094": ("photo", "aucun (vu à la loupe)", "marche perforée galvanisée : relief antidérapant, trou de fixation latéral (origine incertaine)"),
    "G095": ("photo", "aucun (vu à la loupe)", "caillebotis galvanisés en pile : maille rectangulaire, barres porteuses (origine incertaine)"),
    "G096": ("packshot", "", "meuleuse Flex : photo fabricant"),
    "G097": ("schema", "", "meuleuse Flex : plan coté fabricant"),
    "G098": ("packshot", "", "DL Chemicals Parasilico : cartouche détourée"),
    "G099": ("packshot", "", "DL Chemicals Parabond 600 : cartouche détourée"),
    "G100": ("packshot", "", "DL Chemicals Parabond 800 : cartouche détourée"),
    "G101": ("packshot", "", "DL Chemicals Parachim : cartouche détourée"),
    "G102": ("rayon", "", "cartouches Parachim en rayon"),
    "G103": ("packshot", "", "gamme Zinga : visuel fabricant"),
    "G104": ("packshot", "", "Zingatar / Zingatarfree : visuel fabricant"),
    "G105": ("packshot", "", "Zingasolv : visuel fabricant"),
    "G106": ("packshot", "", "Zingaspray : visuel fabricant"),
    "G107": ("packshot", "", "Zingaluspray : visuel fabricant"),
    "G108": ("rayon", "", "Zingatarfree en rayon"),
    "G109": ("rayon", "", "Zingasolv en rayon"),
    "G110": ("rayon", "", "Zinga 1 kg en rayon"),
    "G111": ("rayon", "", "Zingaspray en rayon"),
    "G112": ("rayon", "", "Zingaluspray en rayon"),
    "G113": ("rayon", "", "Zingatarfree 5 L en rayon"),
    "G114": ("banque", "", "pot de peinture générique gris-bleu (pas le produit)"),
    "G115": ("banque", "", "pot de peinture générique brun (pas le produit)"),
    "G116": ("banque", "", "pot de peinture générique blanc (pas le produit)"),
    "G117": ("banque", "", "pot de peinture générique noir (pas le produit)"),
    "G118": ("rayon", "", "étiquette All Meta Prim Coat"),
    "G119": ("rayon", "", "Vibol Prim Coat RAL 7016 en rayon"),
    "G120": ("rayon", "", "Vibol Prim Coat RAL 8012 5 L en rayon"),
    "G121": ("rayon", "", "Vibol Prim Coat en rayon"),
    "G122": ("rayon", "", "Vibol Prim Coat RAL 8012 1 L en rayon"),
    "G123": ("photo", "", "sachet de vis TH P5 6,3x55 + Vulca : tête hexagonale, rondelle EPDM, zingué blanc"),
    "G124": ("photo", "", "sachet de vis TH P5 6,3x100 + Vulca"),
    "G125": ("photo", "", "sachet de vis TH P5 6,3x76 : zingué jaune"),
    "G126": ("photo", "", "sachet de vis TH 6,3x100 Rapidbois + Vulca : zingué jaune"),
    "G127": ("photo", "", "sachet de vis TH 6,3x55 Rapidbois + Vulca"),
    "G128": ("photo", "", "sachet de vis TH 6,3x100 + Vulca"),
    "G129": ("rendu", "", "tasseaux imitation bois « Version Maxi » (fabricant)"),
    "G130": ("rendu", "", "tasseaux imitation bois en vue rapprochée (fabricant)"),
    "G131": ("ambiance", "", "bardage imitation bois posé (rendu fabricant)"),
    "G132": ("schema", "", "profil de tasseau coté : 40 mm, 37 mm, largeur 710 mm (fabricant)"),
    "G133": ("photo", "", "panneaux isolés en pile au dépôt : âme mousse crème, parements acier gris"),
    "G134": ("photo", "", "panneaux isolés en pile au dépôt"),
    "G135": ("rendu", "", "tôle profil 30.200.1000, gris (Grosjean)"),
    "G136": ("photo", "", "tôle profilée trapézoïdale, métal nu (origine incertaine)"),
    "G137": ("schema", "", "tôle profilée : longueur utile, longueur (Grosjean)"),
}


def main():
    groupes = json.loads((DEST / "_groupes.json").read_text(encoding="utf-8"))
    manquants = sorted(set(groupes) - set(C))
    if manquants:
        raise SystemExit(f"Groupes non classés : {manquants}")
    sortie = PROJET / "_DOCS" / "rendus-3d"
    sortie.mkdir(parents=True, exist_ok=True)
    with open(sortie / "references-groupes.csv", "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["groupe", "type", "filigrane", "apprend", "taille", "nb_images", "nb_produits", "categories", "image_reference"])
        for g, info in groupes.items():
            t, fil, note = C[g]
            w.writerow([g, t, fil, note, "x".join(map(str, info["taille"])), len(info["images"]),
                        len(info["produits"]), " | ".join(info["categories"]), info["reference"]])
    index = json.loads((DEST / "_index.json").read_text(encoding="utf-8"))
    par_fichier = {v["fichier"]: v for v in index.values()}
    with open(sortie / "references.csv", "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["image", "groupe", "type", "filigrane", "apprend", "categorie", "produits"])
        for g, info in groupes.items():
            t, fil, note = C[g]
            for fichier in info["images"]:
                im = par_fichier.get(fichier, {})
                w.writerow([fichier, g, t, fil, note, im.get("categorie", ""), " | ".join(im.get("produits", []))])
    print("groupes par type :", dict(Counter(C[g][0] for g in groupes)))


if __name__ == "__main__":
    main()
