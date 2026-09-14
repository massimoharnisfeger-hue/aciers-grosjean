#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Génère lib/catalogue.ts à partir de l'inventaire réel du site
(AG_annexe_inventaire_URLs.csv, 665 URLs crawlées).

Source de vérité : la colonne URL_cible_recommandee du CSV donne, pour chaque
page, l'URL propre de destination définie par le blueprint (section 46).
On ne réinvente donc ni l'arborescence ni les slugs : on les lit.

Ce qui est *calculé* ici et pas lu : les poids (formules normalisées, densité
par matière) et les prix indicatifs (poids × tarif au kilo par famille,
calibré sur les prix publics connus). Tout le reste vient du crawl.
"""

import csv, io, json, re, sys, unicodedata, collections
from pathlib import Path

CSV = Path(sys.argv[1] if len(sys.argv) > 1 else
           "/root/.claude/uploads/60ae7e8a-02ec-55b3-a28b-f1d0fa40a449/"
           "47111c3e-AG_annexe_inventaire_URLs.csv")
OUT = Path(__file__).resolve().parent.parent / "lib" / "catalogue.ts"

# --------------------------------------------------------------------------
# Univers : les 6 catégories racines réelles + leur habillage éditorial
# --------------------------------------------------------------------------

UNIVERS = {
    "acier": dict(
        nom="Acier",
        accroche="La matière de structure, brute ou protégée",
        intro="L'acier de construction couvre l'essentiel des besoins : ossature, ferronnerie, "
              "armature, couverture. Brut à l'intérieur ou sous peinture, galvanisé dès que "
              "l'ouvrage est exposé. C'est la matière la plus disponible, la plus facile à "
              "souder et la mieux placée en prix.",
        titreSeo="Acier S235 — poutrelles, tubes, tôles, profilés et armatures",
        descSeo="Tout l'acier de construction en stock : poutrelles IPE HEA HEB UPN, tubes, tôles, "
                "cornières, plats, ronds à béton et treillis. Découpe aux cotes, retrait le jour même.",
        art="poutrelles", densite=7.85, tarif=1.12,
    ),
    "aluminium": dict(
        nom="Aluminium",
        accroche="Trois fois plus léger, jamais de rouille",
        intro="Le profilé aluminium s'impose dès que le poids compte ou que la structure doit "
              "rester nue. Il s'usine et se perce très facilement, se plie à froid, et sa couche "
              "d'alumine le protège naturellement. Il se soude en revanche au TIG ou au MIG, "
              "pas à l'électrode.",
        titreSeo="Aluminium — profilés, tubes et tôles coupés à la demande",
        descSeo="Aluminium 6060 et 5754 : cornières, plats, profils U et T, tubes carrés, "
                "rectangulaires et ronds, tôles planes et striées. Léger, inoxydable, anodisable.",
        art="cornieres-plats", densite=2.70, tarif=6.20,
    ),
    "inox": dict(
        nom="Inox",
        accroche="Ce qui reste dehors sans rouiller",
        intro="L'inox ne rouille pas : le chrome forme en surface une couche d'oxyde qui se "
              "reconstitue seule à chaque rayure. Le 304 brossé couvre la majorité des usages "
              "extérieurs et alimentaires ; le 316L s'impose en bord de mer et en milieu chloré.",
        titreSeo="Inox 304 brossé — tubes, tôles, plats et cornières sur mesure",
        descSeo="Inox 304 grain 320 : tubes ronds, carrés et rectangulaires, tôles planes, plats, "
                "cornières et ronds pleins. Garde-corps, cuisine professionnelle, extérieur.",
        art="tubes", densite=8.00, tarif=5.20,
    ),
    "toiture-bardage": dict(
        nom="Toiture & bardage",
        accroche="Fermer et couvrir, isolé ou non",
        intro="Tôles profilées, panneaux sandwich isolés, panneaux-tuile et bardage à clins. "
              "Toutes les longueurs se coupent à la demande, et les teintes RAL courantes sont "
              "tenues en stock permanent.",
        titreSeo="Toiture et bardage acier — bac acier, panneaux isolés, panneau-tuile",
        descSeo="Tôles profilées, panneaux sandwich isolés Eurocopre, panneau-tuile et bardage "
                "imitation bois. Longueurs sur mesure, teintes RAL en stock. 4 dépôts.",
        art="toles", densite=7.85, tarif=1.55,
    ),
    "jardin-cloture": dict(
        nom="Jardin & clôture",
        accroche="Délimiter, masquer, aménager",
        intro="Panneaux rigides, poteaux, fixations et bordures : de quoi monter une clôture "
              "complète et dessiner un jardin. Tout est galvanisé ou thermolaqué — rien ne se "
              "repeint.",
        titreSeo="Clôture rigide et bordure de jardin — panneaux, poteaux, fixations",
        descSeo="Panneaux rigides 3D, poteaux Cloplus, brides et fixations en RAL 7016, 9005 et "
                "6005, bordures corten et galvanisées. Vendus à l'unité, retrait en dépôt.",
        art="poteaux-cloture", densite=7.85, tarif=1.90,
    ),
    "quincaillerie": dict(
        nom="Quincaillerie & ferronnerie",
        accroche="Ce qui assemble, protège et finit",
        intro="Visserie, caillebotis et marches, galvanisation à froid, primaires anticorrosion, "
              "colles et étanchéité. Les consommables qu'on oublie de commander et qui arrêtent "
              "un chantier — ils sont en stock permanent.",
        titreSeo="Quincaillerie acier — visserie, caillebotis, zinc et primaires",
        descSeo="Vis autoforantes, caillebotis galvanisés et marches, ZINGA galvanisation à froid, "
                "primaires anticorrosion RAL, colles et mastics. Retrait le jour même.",
        art="visserie", densite=7.85, tarif=1.30,
    ),
}

# --------------------------------------------------------------------------
# Habillage éditorial des familles (niveau 2)
# --------------------------------------------------------------------------

FAMILLES_TXT = {
    "acier/poutrelles": ("IPE, IPN, HEA, HEB, UPN — la structure porteuse",
        "Profilés normalisés laminés à chaud. L'IPE porte en flexion sur de longues portées ; "
        "les HEA et HEB, plus larges d'aile, reprennent la compression et font les poteaux ; "
        "l'UPN se boulonne à plat en rive."),
    "acier/tubes": ("L'ossature creuse, légère et rigide",
        "À poids égal, le tube est plus rigide que le plein. Carré pour souder d'équerre sans "
        "préparation, rectangulaire pour porter dans un sens, rond pour les mains courantes."),
    "acier/toles": ("Couvrir, habiller, fermer",
        "Laminée à chaud pour les pièces structurelles, à froid pour la précision, larmée pour "
        "l'antidérapant, galvanisée pour l'extérieur, corten pour la patine, perforée pour ventiler."),
    "acier/profiles": ("Le fer de ferronnerie",
        "Cornières, plats, larges plats, fers T, ronds et carrés pleins. La matière première du "
        "ferronnier : ça se perce, ça se cintre et ça se soude sans préparation."),
    "acier/armatures-beton": ("Ce qui arme le béton",
        "Ronds à béton crénelés laminés à chaud ou à froid, treillis soudés et treillis à "
        "dépassants. Panneaux au format chantier, coupe et façonnage sur plan."),
    "aluminium/profiles": ("Profilés aluminium 6060",
        "Cornières, plats, profils U et T, carrés pleins. Se coupent à la scie à métaux, se "
        "percent sans effort et ne demandent aucune protection."),
    "aluminium/toles": ("Tôles aluminium planes et striées",
        "Habillage, capotage, signalétique pour la plane ; marchepieds, planchers de remorque "
        "et seuils pour la striée."),
    "aluminium/tubes": ("Tubes aluminium",
        "Carrés, rectangulaires et ronds. Trois fois plus légers que l'acier à section égale : "
        "le choix des structures qu'on déplace ou qu'on porte."),
    "inox/profiles": ("Profilés inox 304",
        "Cornières égales, plats et ronds pleins en 304 brossé, pour la ferronnerie exposée qui "
        "ne se repeint jamais."),
    "inox/toles": ("Tôles inox 304 brossées",
        "Grain 320, film de protection posé. Crédences, plans de travail, habillages de cuisine "
        "professionnelle et plaques de propreté."),
    "inox/tubes": ("Tubes inox 304",
        "Ronds, carrés et rectangulaires en 304 brossé grain 320 : mains courantes, garde-corps, "
        "ossatures exposées en permanence."),
    "toiture-bardage/toles-profilees": ("Bac acier non isolé",
        "Grande portée entre pannes, pose rapide par recouvrement, longueurs sur mesure. "
        "Avec ou sans feutre régulateur de condensation."),
    "toiture-bardage/panneaux-isoles": ("Panneaux sandwich",
        "Isolation et couverture en une seule pose. Le panneau ECO 30 mm est tenu en stock "
        "permanent de 260 à 710 cm."),
    "toiture-bardage/panneau-tuile": ("L'aspect tuile, le poids de l'acier",
        "Le rendu d'une couverture en tuiles pour une fraction du poids et une pose bien plus "
        "rapide. Isolé ou non isolé."),
    "toiture-bardage/bardage": ("Habiller une façade",
        "Bardage à clins et parement imitation bois. La finition posée telle quelle, sans "
        "peinture de chantier."),
    "jardin-cloture/clotures": ("La clôture complète",
        "Panneaux rigides, poteaux et fixations dans les mêmes teintes RAL. On commande la ligne "
        "entière d'un coup, rien ne dépareille."),
    "jardin-cloture/amenagement": ("Dessiner le jardin",
        "Bordures corten et galvanisées pour séparer la pelouse du massif d'un trait net."),
    "quincaillerie/protection-chimie": ("Protéger le métal",
        "Galvanisation à froid ZINGA, primaires anticorrosion aux teintes RAL, colles et mastics "
        "d'étanchéité. Ce qui fait tenir un ouvrage dans le temps."),
}

# Habillage des catégories feuilles dépourvues de texte : généré depuis le nom.
CATEG_TXT = {
    "acier/poutrelles/ipe": "Profil en I à ailes parallèles : le meilleur rendement en flexion sur longue portée. C'est le profil des linteaux et des planchers.",
    "acier/poutrelles/hea": "Profil H allégé : ailes larges pour la compression, âme fine pour le poids. Le compromis des poteaux et des ossatures courantes.",
    "acier/poutrelles/heb": "Profil H lourd, section quasi carrée : le plus résistant à encombrement égal. Poteaux, reprises de charge, portiques.",
    "acier/poutrelles/upn": "Profil en U à ailes inclinées : chevêtres, rives de plancher, encadrements. Se boulonne à plat sans usinage.",
    "acier/poutrelles/hem": "Profil H renforcé, la série la plus lourde. Disponible sur commande, nous consulter pour les délais.",
    "acier/tubes/tube-carre": "Le tube d'ossature par défaut : quatre faces planes qui se soudent d'équerre sans préparation.",
    "acier/tubes/tube-rectangulaire": "La rigidité se concentre dans le sens de la hauteur. Le profil des traverses et des poutres de portail.",
    "acier/tubes/tube-rond": "Mains courantes, barrières, mobilier et structures cintrées. Série légère en acier brut.",
    "acier/toles/tole-laminee-a-chaud": "Tôle de construction S235JR : platines, goussets, pièces structurelles découpées au plan.",
    "acier/toles/tole-laminee-a-froid": "Surface plus lisse et tolérances plus serrées que le laminé à chaud. Pour ce qui se voit ou s'emboîte.",
    "acier/toles/tole-larmee": "Motif damier en relief laminé dans la masse : planchers techniques, marches, passerelles, seuils.",
    "acier/toles/tole-galvanisee": "Revêtement de zinc appliqué en continu : elle part dehors sans peinture ni traitement complémentaire.",
    "acier/toles/tole-corten": "L'acier qui se protège en rouillant. La patine se stabilise en 6 à 18 mois, puis fait barrière.",
    "acier/toles/tole-quarto": "Forte épaisseur laminée sur quarto : grande résistance mécanique pour les pièces lourdes.",
    "acier/toles/tole-perforee": "Perforations rondes, carrées ou aléatoires : ventilation, brise-vue, habillage de façade, protection de machine.",
    "acier/toles/tole-electrozinguee": "Zingage électrolytique fin, surface régulière : pour l'intérieur et les pièces peintes ensuite.",
    "acier/toles/tole-decapee": "Calamine retirée : meilleure usinabilité et meilleure accroche de la peinture.",
    "acier/profiles/corniere-egale": "La pièce de renfort universelle : cadre, support, raidisseur, bordure. La plus demandée du catalogue.",
    "acier/profiles/corniere-inegale": "Ailes de largeurs différentes : la grande aile porte, la petite se fixe. Rives, seuils, supports asymétriques.",
    "acier/profiles/plat": "Le fer plat de ferronnerie : portails, grilles, pièces de liaison, platines.",
    "acier/profiles/large-plat": "Au-delà de 150 mm de largeur, le plat devient un large plat : semelles, platines de forte section.",
    "acier/profiles/rond-plein": "Barre ronde pleine laminée : barreaudage, axes, tiges, pièces tournées. Encaisse la torsion.",
    "acier/profiles/carre-plein": "Barreaudage décoratif, grilles de défense, ferronnerie traditionnelle.",
    "acier/profiles/fer-t": "Profil en T laminé : encadrements, séparations, renforts d'angle plat.",
    "acier/armatures-beton/rond-a-beton-lamine-a-chaud": "Barre crénelée haute adhérence B500B : l'armature des poutres, poteaux et chaînages coulés en place.",
    "acier/armatures-beton/rond-a-beton-lamine-a-froid": "Crénelage obtenu à froid, pour les petits diamètres et les armatures légères.",
    "acier/armatures-beton/treillis-soudes": "Panneaux d'armature pour dalles, chapes et terrasses. Format chantier 5 × 2 m.",
    "acier/armatures-beton/treillis-soudes-depassants": "Fils dépassants pour recouvrir les panneaux entre eux sans recoupe. Format 5,95 × 2,35 m.",
}

# --------------------------------------------------------------------------
# Poids : tables normalisées et formules
# --------------------------------------------------------------------------

PROFILS = {  # série -> { hauteur: (h, b, tw, tf, kg/m) }
 "IPE": {80:(80,46,3.8,5.2,6.0),100:(100,55,4.1,5.7,8.1),120:(120,64,4.4,6.3,10.4),
   140:(140,73,4.7,6.9,12.9),160:(160,82,5.0,7.4,15.8),180:(180,91,5.3,8.0,18.8),
   200:(200,100,5.6,8.5,22.4),220:(220,110,5.9,9.2,26.2),240:(240,120,6.2,9.8,30.7),
   270:(270,135,6.6,10.2,36.1),300:(300,150,7.1,10.7,42.2),330:(330,160,7.5,11.5,49.1),
   360:(360,170,8.0,12.7,57.1),400:(400,180,8.6,13.5,66.3),450:(450,190,9.4,14.6,77.6),
   500:(500,200,10.2,16.0,90.7),550:(550,210,11.1,17.2,106.0),600:(600,220,12.0,19.0,122.0)},
 "HEA": {100:(96,100,5.0,8.0,16.7),120:(114,120,5.0,8.0,19.9),140:(133,140,5.5,8.5,24.7),
   160:(152,160,6.0,9.0,30.4),180:(171,180,6.0,9.5,35.5),200:(190,200,6.5,10.0,42.3),
   220:(210,220,7.0,11.0,50.5),240:(230,240,7.5,12.0,60.3),260:(250,260,7.5,12.5,68.2),
   280:(270,280,8.0,13.0,76.4),300:(290,300,8.5,14.0,88.3),320:(310,300,9.0,15.5,97.6),
   340:(330,300,9.5,16.5,105.0),360:(350,300,10.0,17.5,112.0),400:(390,300,11.0,19.0,125.0)},
 "HEB": {100:(100,100,6.0,10.0,20.4),120:(120,120,6.5,11.0,26.7),140:(140,140,7.0,12.0,33.7),
   160:(160,160,8.0,13.0,42.6),180:(180,180,8.5,14.0,51.2),200:(200,200,9.0,15.0,61.3),
   220:(220,220,9.5,16.0,71.5),240:(240,240,10.0,17.0,83.2),260:(260,260,10.0,17.5,93.0),
   280:(280,280,10.5,18.0,103.0),300:(300,300,11.0,19.0,117.0),320:(320,300,11.5,20.5,127.0),
   340:(340,300,12.0,21.5,134.0),360:(360,300,12.5,22.5,142.0),400:(400,300,13.5,24.0,155.0)},
 "UPN": {50:(50,25,5.0,7.0,5.59),65:(65,42,5.5,7.5,7.09),80:(80,45,6.0,8.0,8.64),
   100:(100,50,6.0,8.5,10.6),120:(120,55,7.0,9.0,13.4),140:(140,60,7.0,10.0,16.0),
   160:(160,65,7.5,10.5,18.8),180:(180,70,8.0,11.0,22.0),200:(200,75,8.5,11.5,25.3),
   220:(220,80,9.0,12.5,29.4),240:(240,85,9.5,13.0,33.2),260:(260,90,10.0,14.0,37.9),
   280:(280,95,10.0,15.0,41.8),300:(300,100,10.0,16.0,46.2)},
 "IPN": {80:(80,42,3.9,5.9,5.94),100:(100,50,4.5,6.8,8.34),120:(120,58,5.1,7.7,11.1),
   140:(140,66,5.7,8.6,14.3),160:(160,74,6.3,9.5,17.9),180:(180,82,6.9,10.4,21.9),
   200:(200,90,7.5,11.3,26.2),220:(220,98,8.1,12.2,31.1),240:(240,106,8.7,13.1,36.2)},
}

CONGE = 1.013  # congé de raccordement des cornières et profils laminés

NUM = r"(\d+(?:[.,]\d+)?)"


def f(x):
    return float(str(x).replace(",", "."))


def dims_de(nom):
    """Extrait la première suite de cotes AxBxC / AxB du nom."""
    m = re.search(NUM + r"\s*[x×]\s*" + NUM + r"\s*[x×]\s*" + NUM, nom, re.I)
    if m:
        return [f(m.group(1)), f(m.group(2)), f(m.group(3))]
    m = re.search(NUM + r"\s*[x×]\s*" + NUM, nom, re.I)
    if m:
        return [f(m.group(1)), f(m.group(2))]
    return []


def suite_cotes(nom):
    """Tous les nombres de la première suite AxBx…xN du nom : « 40x40x40x2mm » -> [40, 40, 40, 2]."""
    m = re.search(NUM + r"(?:\s*[x×]\s*" + NUM + r")+", nom, re.I)
    return [f(x) for x in re.findall(NUM, m.group(0))] if m else []


def diametre_de(nom):
    m = re.search(NUM + r"\s*mm\s+de\s+diam", nom, re.I) or \
        re.search(r"diam[èe]tre\s+" + NUM, nom, re.I) or \
        re.search(r"(?:^|\s)(?:rond\s+(?:plein\s+)?lisse\s+)" + NUM + r"\s*mm", nom, re.I)
    return f(m.group(1)) if m else None


def poids_et_specs(cat_path, nom, densite):
    """Retourne (kg, unite_poids, unite_vente, unite_courte, [specs])."""
    d = dims_de(nom)
    specs = []
    seg = cat_path.split("/")[-1]

    # --- poutrelles : table normalisée ---
    m = re.search(r"\b(IPE|IPN|HEA|HEB|HEM|UPN)\s*(\d+)", nom, re.I)
    if m:
        serie, h = m.group(1).upper(), int(m.group(2))
        t = PROFILS.get(serie, {}).get(h)
        if t:
            hh, b, tw, tf, kg = t
            specs = [("Hauteur (h)", f"{hh:g} mm"), ("Largeur d'aile (b)", f"{b:g} mm"),
                     ("Épaisseur d'âme (tw)", f"{tw:g} mm".replace(".", ",")),
                     ("Épaisseur d'aile (tf)", f"{tf:g} mm".replace(".", ",")),
                     ("Nuance", "S235JR — EN 10025-2"), ("Procédé", "Laminé à chaud"),
                     ("Longueur standard", "6 m ou 12 m — découpe aux cotes")]
            return kg, "kg/m", "au mètre", "€/m", specs
        return None, "", "au mètre", "€/m", [("Série", serie), ("Hauteur", f"{h} mm"),
                                             ("Nuance", "S235JR"), ("Disponibilité", "Sur commande")]

    # --- tôles vendues à la plaque : L x l x e ---
    if "tole" in seg or "tôle" in nom.lower()[:6] or seg.startswith("tole"):
        if len(d) == 3 and d[0] >= 500:
            L, l, e = d
            # épaisseur larmée « 3/5 » : on retient la base
            m2 = re.search(NUM + r"\s*/\s*" + NUM + r"\s*mm", nom)
            base = f(m2.group(1)) if m2 else e
            kgm2 = round(base * densite, 2)
            kg = round(kgm2 * (L / 1000) * (l / 1000), 1)
            # l'oxycoupage ne s'applique qu'à l'acier : jamais sur l'aluminium ni l'inox
            decoupe = ("Cisaillage aux cotes" if cat_path.startswith(("/aluminium", "/inox"))
                       else "Cisaillage ou oxycoupage aux cotes")
            specs = [("Format", f"{L:g} × {l:g} mm"),
                     ("Épaisseur", (f"{m2.group(1)}/{m2.group(2)} mm" if m2 else f"{e:g} mm").replace(".", ",")),
                     ("Masse surfacique", f"{kgm2:.2f} kg/m²".replace(".", ",")),
                     ("Découpe", decoupe)]
            return kg, "kg/plaque", "à la plaque", "€/pce", specs

    # --- profilés au mètre ---
    if "corniere" in seg:
        if len(d) == 3:
            a, b, e = d
            kg = round((a + b - e) * e * densite * CONGE / 1000, 2)
            specs = [("Ailes", f"{a:g} × {b:g} mm"), ("Épaisseur", f"{e:g} mm")]
            return kg, "kg/m", "au mètre", "€/m", specs
    if seg in ("plat", "large-plat") or re.match(r"^(plat|large plat)\b", nom, re.I):
        if len(d) >= 2:
            l, e = d[0], d[1]
            kg = round(l * e * densite / 1000, 2)
            specs = [("Largeur", f"{l:g} mm"), ("Épaisseur", f"{e:g} mm")]
            return kg, "kg/m", "au mètre", "€/m", specs
    if "rond-plein" in seg or re.match(r"^rond (plein |)lisse", nom, re.I):
        dia = diametre_de(nom) or (d[0] if d else None)
        if dia:
            kg = round(dia * dia * densite * 3.1416 / 4 / 1000, 2)
            return kg, "kg/m", "au mètre", "€/m", [("Diamètre", f"{dia:g} mm")]
    if "carre-plein" in seg:
        if d:
            a = d[0]
            kg = round(a * a * densite / 1000, 2)
            return kg, "kg/m", "au mètre", "€/m", [("Section", f"{a:g} × {a:g} mm")]
    if "fer-t" in seg:
        if len(d) >= 2:
            a, e = d[0], d[1]
            kg = round((2 * a - e) * e * densite * CONGE / 1000, 2)
            return kg, "kg/m", "au mètre", "€/m", [("Section", f"{a:g} × {a:g} mm"), ("Épaisseur", f"{e:g} mm")]
    if "profil-u" in seg:
        # « 40x40x40x2mm » : aile × âme × aile × épaisseur ; dims_de n'en lit que trois
        cotes = suite_cotes(nom)
        if len(cotes) >= 2:
            a, e = cotes[0], cotes[-1]
            kg = round((3 * a - 2 * e) * e * densite / 1000, 2)
            section = " × ".join(f"{x:g}" for x in cotes[:-1])
            return kg, "kg/m", "au mètre", "€/m", [("Section", f"{section} mm"), ("Épaisseur", f"{e:g} mm")]
    if "profil-t" in seg:
        if len(d) >= 2:
            a, e = d[0], d[-1]
            kg = round((2 * a - e) * e * densite / 1000, 2)
            return kg, "kg/m", "au mètre", "€/m", [("Section", f"{a:g} × {a:g} mm"), ("Épaisseur", f"{e:g} mm")]
    if "tube-carre" in seg and len(d) == 3:
        a, _, e = d
        kg = round(4 * (a - e) * e * densite / 1000 * 0.97, 2)
        return kg, "kg/m", "au mètre", "€/m", [("Section", f"{a:g} × {a:g} mm"), ("Épaisseur", f"{e:g} mm")]
    if "tube-rectangulaire" in seg and len(d) == 3:
        a, b, e = d
        kg = round(2 * (a + b - 2 * e) * e * densite / 1000 * 0.97, 2)
        return kg, "kg/m", "au mètre", "€/m", [("Section", f"{a:g} × {b:g} mm"), ("Épaisseur", f"{e:g} mm")]
    if "tube-rond" in seg:
        mm = re.search(NUM + r"(?:\(\d+\))?\s*[x×]\s*" + NUM, nom)
        if mm:
            dia, e = f(mm.group(1)), f(mm.group(2))
            kg = round((dia - e) * e * densite * 3.1416 / 1000, 2)
            return kg, "kg/m", "au mètre", "€/m", [("Diamètre extérieur", f"{dia:g} mm".replace(".", ",")),
                                                   ("Épaisseur", f"{e:g} mm".replace(".", ","))]
    if "rond-a-beton" in seg:
        dia = diametre_de(nom)
        if dia:
            kg = round(dia * dia * 0.00617, 2)
            return kg, "kg/m", "au mètre", "€/m", [("Diamètre", f"{dia:g} mm"),
                                                   ("Nuance", "B500B — haute adhérence"),
                                                   ("Surface", "Crénelée")]
    if "treillis" in seg and len(d) == 3:
        maille_a, maille_b, fil = d
        kgm2 = 2 * (1000 / maille_a) * (fil * fil * 0.00617)
        mf = re.search(NUM + r"\s*m\s*[x×]\s*" + NUM + r"\s*m", nom, re.I)
        specs = [("Maille", f"{maille_a:g} × {maille_b:g} mm"), ("Fil", f"{fil:g} mm"),
                 ("Nuance", "B500A"),
                 ("Masse surfacique", f"{kgm2:.2f} kg/m²".replace(".", ","))]
        if mf:
            L, l = f(mf.group(1)), f(mf.group(2))
            specs.insert(3, ("Panneau", f"{mf.group(1)} × {mf.group(2)} m"))
            return round(kgm2 * L * l, 1), "kg/panneau", "au panneau", "€/pce", specs
        return round(kgm2, 2), "kg/m²", "au m²", "€/m²", specs

    return None, "", "à l'unité", "€/pce", ([("Dimensions", " × ".join(f"{x:g}" for x in d) + " mm")] if d else [])


# Tarif au kilo et prix plancher, par préfixe de chemin (le plus long gagne).
# Les trois premières lignes sont calibrées sur les prix publics réels du site :
#   cornière 40×40×4 → 2,42 kg/m × 1,178 = 2,85 €/m
#   tube carré 40×40×2 → 2,31 kg/m × 1,385 = 3,20 €/m
#   tôle lisse 2 mm   → 15,7 kg/m² × 1,18  = 18,50 €/m²
TARIFS = [
    ("/acier/profiles/corniere",        1.178, 1.60),
    ("/acier/tubes",                    1.385, 2.20),
    ("/acier/toles/tole-corten",        2.60, 18.00),
    ("/acier/toles/tole-galvanisee",    1.55, 14.00),
    ("/acier/toles",                    1.18, 12.00),
    ("/acier/profiles/plat",            1.30, 1.95),
    ("/acier/profiles/large-plat",      1.30, 3.50),
    ("/acier/profiles",                 1.25, 1.50),
    ("/acier/poutrelles",               1.05, 6.00),
    ("/acier/armatures-beton",          1.15, 3.00),
    ("/acier",                          1.15, 1.60),
    ("/aluminium/toles",                6.80, 18.00),
    ("/aluminium",                      6.20, 5.00),
    ("/inox/toles",                     5.60, 25.00),
    ("/inox",                           5.20, 6.00),
    ("/toiture-bardage",                1.55, 12.00),
    ("/jardin-cloture",                 1.90, 8.00),
    ("/quincaillerie",                  1.30, 2.00),
]


def arrondi(v):
    pas = 0.05 if v < 20 else 0.1
    return round(round(v / pas) * pas, 2)


def prix_de(chemin, kg, unite):
    if kg is None:
        return None
    tarif, mini = 1.20, 2.00
    best = -1
    for pref, t, m in TARIFS:
        if chemin.startswith(pref) and len(pref) > best:
            tarif, mini, best = t, m, len(pref)
    return arrondi(max(mini, kg * tarif))


# --------------------------------------------------------------------------
# Lecture du CSV
# --------------------------------------------------------------------------

rows = list(csv.DictReader(io.open(CSV, encoding="utf-8-sig"), delimiter=";"))
produits = [r for r in rows if r["Type"] == "product"
            and r["URL_cible_recommandee"].startswith("/p/")]
cats = [r for r in rows if r["Type"] in ("category", "subcategory")]

# titre SEO réel relevé par catégorie cible
titres = {}
metas = {}
for r in cats:
    cible = r["URL_cible_recommandee"]
    if cible.startswith("/") and r["Title"]:
        titres.setdefault(cible, r["Title"])

# Regroupe les produits par chemin de catégorie cible (celui de leur parent)
parent_cible = {}
for r in cats:
    parent_cible[r["Page"]] = r["URL_cible_recommandee"]

groupes = collections.defaultdict(list)
orphelins = []
for r in produits:
    chemin = parent_cible.get(r["Parent"])
    if not chemin or not chemin.startswith("/") or chemin.count("/") < 2:
        orphelins.append(r)
        continue
    groupes[chemin].append(r)

# --------------------------------------------------------------------------
# Construction de l'arbre
# --------------------------------------------------------------------------

def slugify(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()
    return re.sub(r"-{2,}", "-", s)


noeuds = {}   # chemin complet -> dict
for chemin in sorted(groupes):
    parts = chemin.strip("/").split("/")
    for i in range(1, len(parts) + 1):
        p = "/" + "/".join(parts[:i])
        if p not in noeuds:
            noeuds[p] = dict(chemin=p, segment=parts[i - 1], enfants=[], produits=[])

for chemin, lst in groupes.items():
    noeuds[chemin]["produits"] = lst

for p, n in noeuds.items():
    parent = p.rsplit("/", 1)[0]
    if parent and parent in noeuds:
        noeuds[parent]["enfants"].append(p)

# nom lisible d'un nœud : celui de la catégorie du CSV qui pointe dessus
noms = {}
for r in cats:
    c = r["URL_cible_recommandee"]
    if c in noeuds and c not in noms:
        noms[c] = r["H1_ou_nom"] or r["Page"]

LIBELLES = {
    "toles": "Tôles", "tubes": "Tubes", "profiles": "Profilés", "poutrelles": "Poutrelles",
    "armatures-beton": "Armatures béton", "toles-profilees": "Tôles profilées",
    "panneaux-isoles": "Panneaux isolés", "panneau-tuile": "Panneau-tuile", "bardage": "Bardage",
    "clotures": "Clôtures", "amenagement": "Aménagement", "visserie": "Visserie",
    "protection-chimie": "Protection & chimie", "caillebotis-marches": "Caillebotis & marches",
    "outillage": "Outillage", "ipe": "Poutrelle IPE", "hea": "Poutrelle HEA", "heb": "Poutrelle HEB",
    "upn": "Poutrelle UPN", "hem": "Poutrelle HEM",
    "tube-carre": "Tube carré", "tube-rectangulaire": "Tube rectangulaire", "tube-rond": "Tube rond",
    "corniere-egale": "Cornière égale", "corniere-inegale": "Cornière inégale", "plat": "Plat",
    "large-plat": "Large plat", "rond-plein": "Rond plein", "carre-plein": "Carré plein",
    "fer-t": "Fer T", "profil-u": "Profil U", "profil-t": "Profil T",
    "tole-plane": "Tôle plane", "tole-striee": "Tôle striée",
    "tole-plane-304-brossee": "Tôle plane 304 brossée",
    "panneaux-rigides": "Panneaux rigides", "poteaux": "Poteaux", "fixations": "Fixations",
    "bordures": "Bordures", "galvanisation-a-froid": "Galvanisation à froid",
    "colles-etancheite": "Colles & étanchéité", "peintures-primaires": "Peintures & primaires",
    "imitation-bois": "Imitation bois", "profil-30-200-1000": "Profil 30.200.1000",
    "eurocopre-monolamiera-eco": "Panneau ECO Eurocopre",
    "rond-a-beton-lamine-a-chaud": "Rond à béton laminé à chaud",
    "rond-a-beton-lamine-a-froid": "Rond à béton laminé à froid",
    "treillis-soudes": "Treillis soudés", "treillis-soudes-depassants": "Treillis à dépassants",
    "toles": "Tôles", "tole-corten": "Tôle corten", "tole-galvanisee": "Tôle galvanisée",
    "tole-laminee-a-chaud": "Tôle laminée à chaud", "tole-laminee-a-froid": "Tôle laminée à froid",
    "tole-larmee": "Tôle larmée", "tole-perforee": "Tôle perforée", "tole-quarto": "Tôle quarto",
    "tole-electrozinguee": "Tôle électrozinguée", "tole-decapee": "Tôle décapée",
}


def libelle(n):
    """Nom court, pour la navigation et le fil d'Ariane.

    Le crawl stocke souvent un titre SEO à rallonge dans H1_ou_nom
    (« Produits longs : cornières, fers U et T, plats & ronds »).
    Illisible dans un menu : le libellé maison passe donc devant, et on ne
    retombe sur le nom du crawl que s'il est court et sans séparateur SEO.
    """
    seg = n["segment"]
    if seg in LIBELLES:
        return LIBELLES[seg]
    brut = noms.get(n["chemin"], "")
    if brut and len(brut) <= 32 and not any(c in brut for c in "|:–—"):
        return brut
    return seg.replace("-", " ").capitalize()


def titre_long(n):
    """H1 de la page : le titre riche du crawl, nettoyé.

    Le crawl ramène des titres construits pour la balise <title>, avec un
    séparateur et la marque (« … | Aciers Grosjean »). Dans un H1 c'est une
    faute : on coupe au séparateur.
    """
    brut = noms.get(n["chemin"], "").split("|")[0].strip(" -–—")
    return brut if brut and len(brut) > len(libelle(n)) else libelle(n)


# --------------------------------------------------------------------------
# Émission TypeScript
# --------------------------------------------------------------------------

def js(s):
    return json.dumps(s, ensure_ascii=False)


out = []
w = out.append
w("""/**
 * Catalogue Aciers Grosjean — GÉNÉRÉ, NE PAS ÉDITER À LA MAIN.
 *
 * Source : AG_annexe_inventaire_URLs.csv (crawl réel du site, 665 URLs).
 * Générateur : scripts/generer-catalogue.py
 *
 * L'arborescence et les slugs viennent de la colonne URL_cible_recommandee
 * du crawl : ce sont les URLs propres définies par le blueprint (section 46),
 * pas une invention. Les noms de produits sont ceux du site réel.
 *
 * Poids et prix : ceux du site actuel aciersgrosjean.be (lib/site-actuel.json, fusionné en
 * bas de fichier). Les valeurs calculées ci-dessous ne servent que si le site n'en donne pas.
 */

export type Spec = { label: string; valeur: string };

export type Produit = {
  slug: string;
  nom: string;
  categorie: string;
  univers: string;
  kg: number | null;
  unitePoids: string;
  unite: string;
  uniteCourte: string;
  prix: number | null;
  specs: Spec[];
  /** Relevé sur le site actuel (lib/site-actuel.json). */
  prixTtc?: number | null;
  /** Longueurs standard proposées, en mètres. */
  longueurs?: number[];
  finition?: string | null;
  pdfs?: DocumentPdf[];
  idSiteActuel?: number;
  urlSiteActuel?: string;
};

export type DocumentPdf = { fichier: string; titre: string };

export type Noeud = {
  chemin: string;
  segment: string;
  /** Nom court, pour la navigation et le fil d'Ariane. */
  nom: string;
  /** Titre long affiché en H1 de la page. */
  h1: string;
  univers: string;
  accroche: string;
  titreSeo: string;
  enfants: string[];
  produits: string[];
};

export type Univers = {
  slug: string;
  nom: string;
  accroche: string;
  intro: string;
  titreSeo: string;
  descSeo: string;
  art: string;
  enfants: string[];
};
""")

# produits
w("export const produits: Record<string, Produit> = {")
nprod = 0
vus = set()
for chemin, lst in sorted(groupes.items()):
    univers = chemin.strip("/").split("/")[0]
    dens = UNIVERS[univers]["densite"]
    for r in sorted(lst, key=lambda x: x["Page"]):
        slug = r["URL_cible_recommandee"][len("/p/"):]
        if slug in vus:
            continue
        vus.add(slug)
        nom = r["H1_ou_nom"] or r["Page"]
        kg, up, unite, uc, specs = poids_et_specs(chemin, nom, dens)
        prix = prix_de(chemin, kg, unite)
        sp = list(specs)
        if univers == "inox" and not any(k == "Nuance" for k, _ in sp):
            sp.append(("Nuance", "304 (1.4301) — brossé grain 320"))
        if univers == "aluminium" and not any(k == "Alliage" for k, _ in sp):
            sp.append(("Alliage", "6060 T66"))
        if kg is not None:
            sp.append(("Poids", f"{kg:.2f} {up}".replace(".", ",")))
        w(f'  {js(slug)}: {{ slug: {js(slug)}, nom: {js(nom)}, categorie: {js(chemin)}, '
          f'univers: {js(univers)}, kg: {kg if kg is not None else "null"}, unitePoids: {js(up)}, '
          f'unite: {js(unite)}, uniteCourte: {js(uc)}, '
          f'prix: {prix if prix is not None else "null"}, specs: ['
          + ", ".join("{ label: %s, valeur: %s }" % (js(a), js(b)) for a, b in sp) + "] },")
        nprod += 1
w("};\n")

# noeuds
w("export const noeuds: Record<string, Noeud> = {")
for chemin in sorted(noeuds):
    n = noeuds[chemin]
    univers = chemin.strip("/").split("/")[0]
    rel = chemin.strip("/")
    accroche, intro = FAMILLES_TXT.get(rel, ("", ""))
    if not intro:
        intro = CATEG_TXT.get(rel, "")
    nom = libelle(n)
    h1 = titre_long(n)
    brut_seo = titres.get(chemin, "")
    # L'audit reprochait des titres réduits au seul nom (« Inox », « Produit long ») :
    # 3e position sur « inox » pour 22 visites. On les réécrit pour donner envie de cliquer.
    if len(brut_seo) >= 28 and brut_seo.lower() != nom.lower():
        seo = brut_seo
    else:
        seo = f"{h1} — en stock, coupé sur mesure"
    pslugs = sorted(r["URL_cible_recommandee"][len("/p/"):] for r in n["produits"])
    w(f'  {js(chemin)}: {{ chemin: {js(chemin)}, segment: {js(n["segment"])}, nom: {js(nom)}, '
      f'h1: {js(h1)}, univers: {js(univers)}, accroche: {js(accroche or intro)}, '
      f'titreSeo: {js(seo)}, '
      f'enfants: {js(sorted(n["enfants"]))}, produits: {js(pslugs)} }},')
w("};\n")

# univers
w("export const univers: Univers[] = [")
for slug, u in UNIVERS.items():
    enfants = sorted(p for p in noeuds if p.strip("/").split("/")[0] == slug and p.count("/") == 2)
    w(f'  {{ slug: {js(slug)}, nom: {js(u["nom"])}, accroche: {js(u["accroche"])}, '
      f'intro: {js(u["intro"])}, titreSeo: {js(u["titreSeo"])}, descSeo: {js(u["descSeo"])}, '
      f'art: {js(u["art"])}, enfants: {js(enfants)} }},')
w("];\n")

w("""
export const universBySlug = (s: string) => univers.find((u) => u.slug === s);
export const noeudByChemin = (c: string) => noeuds[c];
export const produitBySlug = (s: string) => produits[s];

export const tousProduits = Object.values(produits);
export const totalProduits = tousProduits.length;
export const totalNoeuds = Object.keys(noeuds).length;

/** Tous les produits sous un chemin, en descendant l'arbre. */
export function produitsSous(chemin: string): Produit[] {
  const n = noeuds[chemin];
  if (!n) return [];
  const directs = n.produits.map((s) => produits[s]).filter(Boolean);
  return [...directs, ...n.enfants.flatMap(produitsSous)];
}

/** Fil d'Ariane : liste des nœuds parents d'un chemin, racine d'abord. */
export function ancetres(chemin: string): Noeud[] {
  const parts = chemin.replace(/^\\//, "").split("/");
  const out: Noeud[] = [];
  for (let i = 1; i <= parts.length; i++) {
    const n = noeuds["/" + parts.slice(0, i).join("/")];
    if (n) out.push(n);
  }
  return out;
}

import { formatPrix } from "./format";
export { formatPrix };

/** Prix d'entrée sous un chemin. */
export function prixMini(chemin: string) {
  const p = produitsSous(chemin).map((x) => x.prix).filter((x): x is number => x !== null);
  if (!p.length) return null;
  return Math.min(...p);
}

// ---------------------------------------------------------------------------
// Données réelles du site actuel (scripts/inventaire/integrer.py) : prix HTVA et TVAC,
// poids, unité de vente, longueurs, finition et fiches techniques.
import siteActuel from "./site-actuel.json";

type DonneesSiteActuel = {
  id: number;
  url: string;
  prixTtc: number | null;
  prixHtva: number | null;
  kg: number | null;
  remplacerPoids: boolean;
  unite: string;
  uniteCourte: string;
  unitePoids: string;
  longueurs: number[];
  finition: string | null;
  pdfs: DocumentPdf[];
  specsRetirees: string[];
};

for (const [slug, r] of Object.entries(siteActuel as unknown as Record<string, DonneesSiteActuel>)) {
  const p = produits[slug];
  if (!p) continue;
  p.prix = r.prixHtva;
  p.prixTtc = r.prixTtc;
  p.unite = r.unite;
  p.uniteCourte = r.uniteCourte;
  p.unitePoids = r.unitePoids;
  if (r.remplacerPoids) p.kg = r.kg;
  p.longueurs = r.longueurs;
  p.finition = r.finition;
  p.pdfs = r.pdfs;
  p.idSiteActuel = r.id;
  p.urlSiteActuel = r.url;
  p.specs = p.specs.filter((s) => s.label !== "Poids" && !r.specsRetirees.includes(s.label));
  if (p.kg !== null) {
    const valeur = p.kg.toLocaleString("fr-BE", { maximumFractionDigits: 2 });
    p.specs.push({ label: "Poids", valeur: `${valeur} ${p.unitePoids || "kg"}` });
  }
}
""")

OUT.write_text("\n".join(out), encoding="utf-8")
print(f"écrit {OUT}")
print(f"  produits : {nprod}")
print(f"  noeuds   : {len(noeuds)}")
print(f"  orphelins écartés : {len(orphelins)}")
sansprix = sum(1 for chemin, lst in groupes.items() for r in lst
               if poids_et_specs(chemin, r['H1_ou_nom'] or r['Page'],
                                 UNIVERS[chemin.strip('/').split('/')[0]]['densite'])[0] is None)
print(f"  sans prix (sur devis) : {sansprix}")
