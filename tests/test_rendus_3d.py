"""Controles des modeles 3D des fiches (scripts/rendu-3d) : les defauts vus par le proprietaire.

Audit qualite du 23/09, apres relecture du catalogue par le proprietaire : « parfois c'est beaucoup
trop epais, parfois il y a des arrondis alors qu'il n'y a pas d'arrondis ». Deux causes dans le code,
corrigees le meme jour (`_DOCS/rendus-3d/audit-qualite.md`, D1 et D2). Ces controles lisent le source :
ni Blender ni rendu, ils tournent aussi en CI.

V1 - Aretes vives. Le chanfrein d'arete d'un profile ne depasse jamais 2 % de la paroi la plus fine de
     sa section, ni 0,6 mm ; aucun sur une tole. Le chanfrein fixe de 0,6 mm valait 10 % du cote d'un
     carre de 6 et 20 % d'un plat de 3 : l'arete devenait un arrondi que le produit n'a pas. Et le rendu
     applique la regle : sans l'appel a `regler_chanfrein`, le modificateur garde sa largeur de creation.
V2 - Piece entiere (ADR-0011). Sur la fiche, la barre rendue est le troncon cadre de 6,25 fois la plus grande
     cote, vu en entier : rien ne sort du cadre ; la photo studio garde 7 fois la plus grande section. Le 23/09,
     une barre 4 fois plus longue qui filait hors du cadre et un studio a 18 fois avaient change la vue ; le
     proprietaire, le 24/09 : « je veux vraiment avoir l'entierete de la piece », « les memes vues ».
V3 - Mesure de ce qui est servi. Le controle « photo studio ±N niveaux » de `controler_rendus.py` mesure une
     barre en debord sur sa partie servie (a gauche de 0,615 W), jamais sur la partie cachee sous la fiche
     incrustee : sur les plats, cette partie cachee donnait −31 (seuil 30) a des images justes.
V4 - Meme regle, verifiee sur le resultat : une barre synthetique dont la partie cachee est claire mesure la
     teinte de sa partie servie. Exige Pillow ; sans lui (CI), il se declare ignore.
V5 - Le `.json` d'une photo studio note la longueur de chaque piece : sans elle, la verification independante
     ne controlait la longueur commune des barres qu'en ajustant une camera sur l'image (16/09, puis deux fois
     le 23/09).
V6 - Une etiquette ne se pose jamais entre les deux rappels d'une autre cote, ni a moins de 6 px d'un de ses
     traits : sur le tube rectangulaire 50x20x2 (23/09), « t 2 mm » se lisait comme la valeur de b.
V7 - Sur un tube au flanc clair (aluminium, inox), l'etiquette t posee sur le flanc reste contre la section :
     sur le tube alu 60x30x3 (23/09), elle partait a 350 px de sa pince. Exige Pillow ; sans lui, ignore.
V8 - Sur l'aluminium, un rayon de forme suppose de plus d'un quart d'epaisseur cite la photo du stock qui le
     justifie : les valeurs usuelles reprises de l'acier dessinaient des arrondis absents du produit (23/09).
V9 - La coupe se distingue de la face longue voisine d'au moins 8 niveaux : la coupe claire de l'inox sortait a
     4 niveaux sur les plats (23/09). Structure toujours verifiee ; mesure sur image synthetique avec Pillow.
V10 - Meme regle pour les tubes : paroi opposee des tubes carres et rectangulaires, anneau des tubes ronds contre
     leur flanc (tubes inox, 24/09 : 176 contre 183 ; V9 excluait les tubes).
V11 - Aucune section pleine n'a plus de 20 px de noir pur dans la partie servie : bouchons de nervures des ronds a
     beton dans le plan de la coupe, 297 px sur le 12 mm (24/09), invisibles au controle « part de noir pur ».
V12 - Profil U : la coupe de l'aile basse se distingue du fond du U vu au-dessus d'elle d'au moins 8 niveaux. U alu,
     24/09 (verification independante) : coupe a 149-155 contre 156-157 pour le fond, epaisseur de l'aile illisible ;
     V9 ne mesure que l'ame, a la rangee de la pince.
V13 - Le cadre de la piece sur une fiche tient dans le recadrage du site (`recadrer_visuels.CADRE`), a 0,005 de
     l'image au moins de chaque bord. Le cadre des fiches (0,62 de large, 14/09) depassait la coupe du site (0,615,
     22/09) : invisible tant que le chanfrein fixe arrondissait le bout de la barre ; avec les aretes vives de l'audit,
     le coin du bout arriere touchait le cadre et le site en coupait 6 a 8 px (carre plein, 24/09) : une barre
     « coupee » de nouveau, alors que le proprietaire veut la piece entiere (ADR-0011).
V14 - La composition de chaque photo studio de barres (les fiches rendues cote a cote) est versionnee dans
     `donnees/studios.json`, et `preparer_rendus.py studio-famille` la relit. Elle ne vivait que dans l'atelier du PC
     (`<famille>.studio.json`, scripts de seance) : le 24/09, une seance web devant rendre les « trios d'origine »
     (ADR-0011) a du les retrouver en comparant des silhouettes aux anciennes images.
V15 - Posee sur le blanc, la piece garde l'anticrenelage de son bord : seule l'ombre du sol est allegee. Tout pixel
     d'alpha < 250 etait traite en ombre (x 0,55) : bord 64 niveaux trop clair, en escalier, sur toutes les images
     habillees (large plat, 24/09, verification independante). Mesure sur image synthetique avec Pillow.
"""

import ast
import contextlib
import importlib.util
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

RACINE = Path(__file__).resolve().parents[1]
RENDU = RACINE / "scripts" / "rendu-3d"
PRODUITS = RENDU / "donnees" / "produits.json"
BARRES_ATTENDUES = {"PLAT", "CARRE", "ROND", "ROND-BETON", "L", "T", "TC", "TR", "TUBE-ROND", "I", "U"}
# cadrage des fiches valide le 14/09 et garde par l'audit du 23/09 (6,25 fois la plus grande cote, plafond
# 500 mm) : il fixe la taille de la section et la place des cotes. Il ne change qu'apres un nouvel essai a la
# taille reelle, juge sur la planche avant / apres ; ce controle rougit pour le rappeler.
RATIO_VALIDE = 6.25


def charger_preparer():
    spec = importlib.util.spec_from_file_location("preparer_rendus_controle", RENDU / "preparer_rendus.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def arbre_du_rendu():
    return ast.parse((RENDU / "rendu_profil.py").read_text(encoding="utf-8"))


def fonction_de(fichier, nom):
    """Une fonction pure d'un script qui importe bpy ou Pillow et ne se charge pas partout (CI sans Pillow)."""
    for noeud in ast.parse((RENDU / fichier).read_text(encoding="utf-8")).body:
        if isinstance(noeud, ast.FunctionDef) and noeud.name == nom:
            espace = {}
            exec(compile(ast.Module(body=[noeud], type_ignores=[]), fichier, "exec"), espace)
            return espace[nom]
    return None


def fonction_du_rendu(nom):
    return fonction_de("rendu_profil.py", nom)


def pieces_du_catalogue(preparer):
    """(slug, piece de fiche) pour chaque produit que le preparateur sait modeliser.

    Les fiches sans modele 3D (produits chimiques, accessoires) n'ont pas les cotes d'une section :
    `piece()` leve une KeyError, elles n'ont ni chanfrein ni cadrage a controler."""
    produits = json.loads(PRODUITS.read_text(encoding="utf-8"))
    pieces = []
    for slug, produit in sorted(produits.items()):
        try:
            pc, _ = preparer.piece(produit, 500, RATIO_VALIDE)
        except KeyError:
            continue
        pieces.append((slug, pc))
    return pieces


def paroi_la_plus_fine(pc):
    """Epaisseur de matiere la plus fine de la section : paroi d'un tube ou d'une corniere, ame ou aile
    d'une poutrelle, epaisseur d'un plat, cote d'un carre ou diametre d'un rond."""
    parois = [pc[k] for k in ("t", "tw", "tf") if pc.get(k)]
    return min(parois) if parois else min(pc["h"], pc["b"])


class ModelesSource(unittest.TestCase):
    """V1-V11 : ce que le code des modeles et de leur habillage garantit, sans Blender."""

    @classmethod
    def setUpClass(cls):
        cls.preparer = charger_preparer()
        cls.pieces = pieces_du_catalogue(cls.preparer)

    def test_v1_le_chanfrein_reste_une_arete_vive(self):
        self.assertGreater(len(self.pieces), 300, "le preparateur ne modelise presque plus rien : controle sans objet")
        largeur_chanfrein = fonction_du_rendu("largeur_chanfrein")
        self.assertIsNotNone(largeur_chanfrein, "rendu_profil.py n'a pas de largeur_chanfrein : chanfrein fixe de 0,6 mm ?")
        fautifs = []
        for slug, pc in self.pieces:
            largeur = largeur_chanfrein(pc)
            if pc["type"] == "TOLE":
                if largeur:
                    fautifs.append(f"{slug} : tole chanfreinee de {largeur} mm")
            elif largeur > min(0.6, 0.02 * paroi_la_plus_fine(pc)) + 1e-9:
                fautifs.append(f"{slug} : chanfrein de {largeur} mm pour une paroi de {paroi_la_plus_fine(pc)} mm")
        if fautifs:
            self.fail(f"{len(fautifs)} arete(s) arrondie(s) : {fautifs[:5]}")

        appels = [n for n in ast.walk(arbre_du_rendu())
                  if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "regler_chanfrein"]
        self.assertTrue(appels, "rendu_profil.py n'appelle jamais regler_chanfrein : les profiles gardent 0,6 mm")

    def test_v2_la_piece_entiere_reste_dans_le_cadre(self):
        """ADR-0011 : les vues d'avant l'audit du 23/09. Chaque barre est rendue sur le tronçon cadré de 6,25 fois la
        plus grande cote (plafond 500 mm), vue en entier ; la photo studio garde 7 fois la plus grande section.

        23/09 : la barre rendue 4 fois plus longue que le tronçon cadré sortait de l'image, et le studio passait à
        18 fois ; le propriétaire, le 24/09 : « je veux vraiment avoir l'entièreté de la pièce et pas juste une coupe
        à moitié faite », « que tu laisses exactement les mêmes vues comme il y avait »."""
        self.assertEqual(getattr(self.preparer, "RATIO_STUDIO", 7), 7,
                         "photo studio a plus de 7 fois la plus grande section : la vue d'origine a change (ADR-0011)")
        barres = [(slug, pc) for slug, pc in self.pieces if pc["type"] in BARRES_ATTENDUES]
        self.assertGreater(len(barres), 100, "presque aucune barre dans le catalogue : controle sans objet")
        with tempfile.TemporaryDirectory() as dossier:
            sortie = Path(dossier) / "parametres.json"
            argv = sys.argv
            sys.argv = ["preparer_rendus.py", str(sortie), "car", *[slug for slug, _ in barres]]
            try:
                with contextlib.redirect_stdout(io.StringIO()):  # « <sortie> : N rendus »
                    self.preparer.main()
            finally:
                sys.argv = argv
            rendus = {r["slug"]: r["pieces"][0] for r in json.loads(sortie.read_text(encoding="utf-8"))}
        fautifs = []
        for slug, pc in barres:
            rendu = rendus[slug]
            cadre = rendu.get("longueur_cadre", rendu["longueur"])
            if cadre != pc["longueur"]:
                fautifs.append(f"{slug} : troncon cadre {cadre} mm au lieu de {pc['longueur']} (la section change de taille)")
            elif rendu["longueur"] != cadre:
                fautifs.append(f"{slug} : barre de {rendu['longueur']} mm pour un cadre de {cadre} (elle sort de l'image)")
        if fautifs:
            self.fail(f"{len(fautifs)} barre(s) qui ne tiennent pas entieres dans le cadre : {fautifs[:5]}")

    def test_v3_une_barre_en_debord_se_mesure_sur_la_partie_servie(self):
        """Le contrôle « photo studio ±N niveaux » (controler_rendus.py) mesure une fiche en débord sur la partie
        de la barre que le site sert (à gauche de 0,615 W), pas sur la partie cachée sous la fiche incrustée.

        Plats, 23/09 : écart de −31 (seuil 30) sur des images justes. Le corps de la barre mesuré jusqu'au bord de
        l'image montait de 85 à 92 avec la barre longue, par sa partie cachée ; la photo studio n'avait pas changé
        (60 → 59). Sur la partie servie : −23 avant comme après l'audit (carré plein : −13 → −15)."""
        arbre = ast.parse((RENDU / "controler_rendus.py").read_text(encoding="utf-8"))
        fonctions = {n.name: n for n in arbre.body if isinstance(n, ast.FunctionDef)}
        mesure = fonctions.get("luminance_piece")
        self.assertIsNotNone(mesure, "controler_rendus.py n'a plus de luminance_piece")
        self.assertIn("x_max", [a.arg for a in mesure.args.args + mesure.args.kwonlyargs],
                      "luminance_piece ne sait pas limiter la mesure a la partie servie")
        appels = [n for n in ast.walk(fonctions.get("controler", ast.Module(body=[], type_ignores=[])))
                  if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "luminance_piece"
                  and any(k.arg == "x_max" for k in n.keywords)]
        self.assertTrue(appels, "controler() mesure les fiches en debord sur toute la barre, partie cachee comprise")

    def test_v4_la_partie_cachee_de_la_barre_ne_compte_pas(self):
        """V3 vérifie la structure ; V4, le résultat : une barre dont la partie servie est gris 80 et la partie
        cachée gris 200 mesure 80. Exige Pillow (absent de la CI) : sans lui, le contrôle se déclare ignoré."""
        try:
            from PIL import Image
        except ImportError:
            self.skipTest("Pillow absent : V3 garde la structure du controle")
        if str(RENDU) not in sys.path:
            sys.path.insert(0, str(RENDU))  # controler_rendus importe habiller
        import controler_rendus

        image = Image.new("RGBA", (1600, 1200), (0, 0, 0, 0))
        image.paste((150, 150, 150, 255), (100, 500, 300, 900))   # face coupée, à gauche
        image.paste((80, 80, 80, 255), (300, 400, 984, 800))      # corps servi, jusqu'à 0,615 W
        image.paste((200, 200, 200, 255), (984, 300, 1600, 700))  # corps caché sous la fiche incrustée
        with tempfile.TemporaryDirectory() as dossier:
            chemin = Path(dossier) / "barre.png"
            image.save(chemin)
            servie = controler_rendus.luminance_piece(chemin, moitie_arriere=True, x_max=0.615)[0]
            entiere = controler_rendus.luminance_piece(chemin, moitie_arriere=True)[0]
        self.assertAlmostEqual(servie, 80, delta=1, msg="la partie cachee de la barre compte dans la mesure servie")
        self.assertGreater(entiere, 120, "sans x_max, la mesure doit rester celle de toute la barre")

    def test_v5_la_photo_studio_note_la_longueur_de_chaque_piece(self):
        """Le `.json` d'une photo studio garde la longueur de chaque pièce, pas seulement sa section.

        Trois vérifications indépendantes (16/09 ; plats et larges plats, 23/09) n'ont pu contrôler la longueur
        commune des barres du studio qu'en ajustant une caméra sur l'image : le `.json` ne notait que type, h et b."""
        trouve = False
        for noeud in ast.walk(arbre_du_rendu()):
            if not isinstance(noeud, ast.Dict):
                continue
            cles = {k.value: v for k, v in zip(noeud.keys, noeud.values) if isinstance(k, ast.Constant)}
            mode = cles.get("mode")
            if not (isinstance(mode, ast.Constant) and mode.value == "studio" and "pieces" in cles):
                continue
            trouve = True
            pieces = cles["pieces"]
            modele = pieces.elt if isinstance(pieces, ast.ListComp) else None
            cles_piece = {k.value for k in getattr(modele, "keys", []) if isinstance(k, ast.Constant)}
            self.assertIn("longueur", cles_piece, "le .json de la photo studio ne note pas la longueur des pieces")
        self.assertTrue(trouve, "rendu_profil.py n'ecrit plus le .json de la photo studio (mode studio, pieces)")

    def test_v6_une_etiquette_ne_se_lit_pas_comme_la_valeur_d_une_autre_cote(self):
        """L'habillage refuse une étiquette posée entre les deux rappels d'une autre cote, ou à moins de 6 px d'un de
        ses traits.

        Tube rectangulaire 50x20x2, 23/09 (vérification indépendante) : l'étiquette t, descendue sous le tube, se
        posait entre les rappels de b, au-dessus de son trait, pendant que l'étiquette b passait sous le trait :
        « t 2 mm » se lisait comme la valeur de b. Les contrôles d'habillage ne regardaient que les chevauchements
        d'étiquettes. Coordonnées relevées dans le sidecar de l'image fautive."""
        entre = fonction_de("habiller.py", "etiquette_entre_rappels")
        touche = fonction_de("habiller.py", "etiquette_touche_trait")
        self.assertIsNotNone(entre, "habiller.py ne sait pas voir une etiquette entre les rappels d'une autre cote")
        self.assertIsNotNone(touche, "habiller.py ne sait pas voir une etiquette qui touche un trait")
        rappels_b = (((295.22, 900.03), (300.69, 1000.49)), ((439.26, 926.83), (442.69, 1029.27)))
        boite_t = (363, 921, 467, 961)  # centre (415, 941), comme sur l'image refusée
        flanc = (520, 700, 624, 740)  # même étiquette posée sur le flanc du tube, à droite de la section
        self.assertTrue(entre(boite_t, *rappels_b), "l'etiquette t entre les rappels de b n'est pas vue")
        self.assertFalse(entre(flanc, *rappels_b), "une etiquette hors des rappels est refusee a tort")
        self.assertTrue(touche(boite_t, rappels_b[1]), "l'etiquette posee sur le rappel droit de b n'est pas vue")
        self.assertTrue(touche((446, 950, 550, 990), rappels_b[1]), "une etiquette a 4 px d'un rappel n'est pas vue")
        self.assertFalse(touche(flanc, rappels_b[1]), "une etiquette loin des traits est refusee a tort")

    def test_v7_l_etiquette_t_d_un_tube_clair_reste_pres_de_sa_section(self):
        """Sur un tube dont le flanc est clair (aluminium, inox), l'étiquette t posée sur le flanc reste contre la
        section, pas au bout de la barre.

        Tube rectangulaire alu 60x30x3, 23/09 : `place_t_tube()` cherchait la fin de la paroi opposée au premier pixel
        sombre ; sur l'aluminium, le flanc est aussi clair que la face sciée, l'étiquette partait à 350 px de sa pince,
        au bout d'un trait qui traversait toute la face. Tube synthétique : paroi gauche 100-110, cavité 110-200, paroi
        droite 200-210, flanc clair 210-900. Exige Pillow ; sans lui (CI), il se déclare ignoré."""
        try:
            from PIL import Image
        except ImportError:
            self.skipTest("Pillow absent : habiller.py ne se charge pas")
        if str(RENDU) not in sys.path:
            sys.path.insert(0, str(RENDU))
        import habiller

        clair = Image.new("L", (1600, 1200), 0)
        for x0, x1, v in ((100, 110, 200), (110, 200, 30), (200, 210, 200), (210, 900, 180)):
            clair.paste(v, (x0, 300, x1, 700))
        ancien, traces = habiller.CLAIR, len(habiller.TRACES)
        habiller.CLAIR = clair
        try:
            centre = habiller.place_t_tube((100, 500), (110, 500), 50)
        finally:
            habiller.CLAIR = ancien
            del habiller.TRACES[traces:]
        self.assertLess(centre[0] - 50, 260, f"etiquette t posee a x = {centre[0] - 50:.0f}, loin de sa section")
        self.assertGreater(centre[0] - 50, 210, "etiquette t posee sur la paroi opposee")

    def test_v8_un_rayon_suppose_d_un_profil_alu_cite_la_photo_du_stock(self):
        """Sur un profilé ou un tube aluminium, un rayon de forme « supposé » de plus d'un quart d'épaisseur cite la
        photo du stock qui le justifie.

        23/09 : r1 = t/2 des cornières alu et r1 = 0,75 t des tubes carrés et rectangulaires alu, valeurs usuelles
        reprises de l'acier, dessinaient des arrondis que les photos du stock du site (G053, G061, G063) n'ont pas : la
        plainte du propriétaire, « des arrondis alors qu'il n'y a pas d'arrondis ». Vus par deux vérifications
        indépendantes, pas par les contrôles."""
        produits = json.loads(PRODUITS.read_text(encoding="utf-8"))
        fautifs, vus = [], 0
        for slug, p in sorted(produits.items()):
            if not p["famille"].startswith("aluminium-"):
                continue
            v = p["valeurs"]
            epaisseurs = [v[k]["valeur"] for k in ("t", "tw") if isinstance(v.get(k, {}).get("valeur"), (int, float))]
            if not epaisseurs:
                continue
            t = min(epaisseurs)
            for k in ("r", "r1", "r2"):
                d = v.get(k)
                if not d or not d.get("supposee"):
                    continue
                vus += 1
                if d["valeur"] > 0.25 * t + 1e-9 and "photo" not in d["source"]:
                    fautifs.append(f"{slug} : {k} = {d['valeur']} mm pour t = {t} ({d['source']})")
        self.assertGreater(vus, 20, "presque aucun rayon suppose sur l'aluminium : controle sans objet")
        if fautifs:
            self.fail(f"{len(fautifs)} rayon(s) suppose(s) sans photo du stock : {fautifs[:4]}")

    def test_v9_la_coupe_se_distingue_de_la_face_longue(self):
        """La face sciée se distingue de la face longue voisine d'au moins 8 niveaux : sinon la section ne se lit plus.

        Plat inox 20x3, 23/09 au soir : la coupe claire (base 0,58) sortait à 179 contre 183 pour la face longue, section
        à peine visible en vignette ; l'essai qui l'avait fait adopter ne montrait pas de plat inox. `controler_rendus.py`
        mesure l'écart sur la rangée de la pince du rendu brut (`contraste_coupe`) et refuse moins de 8 niveaux. Pièce
        synthétique : coupe à 179 entre les points de pince, face longue à 183 à droite, puis à 150. Exige Pillow."""
        arbre = ast.parse((RENDU / "controler_rendus.py").read_text(encoding="utf-8"))
        fonctions = {n.name: n for n in arbre.body if isinstance(n, ast.FunctionDef)}
        self.assertIn("contraste_coupe", fonctions, "controler_rendus.py ne mesure pas le contraste de la coupe")
        appels = [n for n in ast.walk(fonctions.get("controler", ast.Module(body=[], type_ignores=[])))
                  if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "contraste_coupe"]
        self.assertTrue(appels, "controler() ne controle pas le contraste de la coupe")
        try:
            from PIL import Image
        except ImportError:
            self.skipTest("Pillow absent : la structure du controle est verifiee, pas la mesure")
        if str(RENDU) not in sys.path:
            sys.path.insert(0, str(RENDU))
        import controler_rendus

        for longue, attendu in ((183, 4), (150, 29)):
            image = Image.new("RGBA", (400, 300), (0, 0, 0, 0))
            image.paste((179, 179, 179, 255), (100, 50, 130, 250))       # face sciée entre les points de pince
            image.paste((longue, longue, longue, 255), (130, 50, 300, 250))  # face longue voisine
            with tempfile.TemporaryDirectory() as dossier:
                chemin = Path(dossier) / "plat.png"
                image.save(chemin)
                coupe, face = controler_rendus.contraste_coupe(chemin, (100, 150), (130, 150))
            self.assertAlmostEqual(abs(face - coupe), attendu, delta=1, msg="mesure du contraste de la coupe fausse")

    def test_v10_la_paroi_d_un_tube_se_distingue_de_son_flanc(self):
        """Tubes carrés, rectangulaires et ronds : la coupe se distingue du flanc voisin d'au moins 8 niveaux.

        Tubes inox, 23/09 au soir (vérification indépendante) : paroi opposée de la coupe à 176 contre 183 pour le flanc,
        anneau des tubes ronds au ton du corps sur son arc droit ; V9 excluait les tubes. Tube carré : la paroi pincée
        donne sur la cavité, on mesure la paroi d'en face (`contraste_paroi_opposee`). Tube synthétique : paroi gauche
        100-110, cavité 110-200, paroi droite 200-210 à 176, flanc 210-400 à 183. Exige Pillow pour la mesure."""
        arbre = ast.parse((RENDU / "controler_rendus.py").read_text(encoding="utf-8"))
        fonctions = {n.name: n for n in arbre.body if isinstance(n, ast.FunctionDef)}
        self.assertIn("contraste_paroi_opposee", fonctions, "controler_rendus.py ne mesure pas la paroi opposee d'un tube")
        appels = [n for n in ast.walk(fonctions.get("controler", ast.Module(body=[], type_ignores=[])))
                  if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "contraste_paroi_opposee"]
        self.assertTrue(appels, "controler() ne controle pas le contraste de la coupe des tubes")
        try:
            from PIL import Image
        except ImportError:
            self.skipTest("Pillow absent : la structure du controle est verifiee, pas la mesure")
        if str(RENDU) not in sys.path:
            sys.path.insert(0, str(RENDU))
        import controler_rendus

        image = Image.new("RGBA", (500, 300), (0, 0, 0, 0))
        for x0, x1, v in ((100, 110, 200), (110, 200, 30), (200, 210, 176), (210, 400, 183)):
            image.paste((v, v, v, 255), (x0, 50, x1, 250))
        with tempfile.TemporaryDirectory() as dossier:
            chemin = Path(dossier) / "tube.png"
            image.save(chemin)
            paroi, flanc = controler_rendus.contraste_paroi_opposee(chemin, (100, 150), (110, 150))
        self.assertAlmostEqual(abs(flanc - paroi), 7, delta=1, msg="mesure de la paroi opposee fausse")

    def test_v11_aucun_noir_pur_sur_une_section_pleine(self):
        """Une section pleine (rond, carré, plat, cornière, profil) n'a pas de noir pur (RVB ≤ 12) dans la partie servie,
        au-delà de 20 pixels.

        Ronds à béton, 24/09 : les bouchons des nervures longitudinales, dans le plan même de la coupe, faisaient deux
        demi-disques noirs sur la face sciée (297 px sur le 12 mm, 1 avant l'audit) ; le chanfrein de 0,6 mm les masquait.
        Le contrôle « part de noir pur » (plus de 2 % de la pièce) ne les voyait pas : 0,02 à 0,11 %. Exige Pillow pour
        la mesure (image synthétique : 150 px noirs dans la partie servie, 400 au-delà de 0,615 W)."""
        arbre = ast.parse((RENDU / "controler_rendus.py").read_text(encoding="utf-8"))
        fonctions = {n.name: n for n in arbre.body if isinstance(n, ast.FunctionDef)}
        self.assertIn("noir_pur_servi", fonctions, "controler_rendus.py ne compte pas le noir pur de la partie servie")
        appels = [n for n in ast.walk(fonctions.get("controler", ast.Module(body=[], type_ignores=[])))
                  if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "noir_pur_servi"]
        self.assertTrue(appels, "controler() ne controle pas le noir pur des sections pleines")
        try:
            from PIL import Image
        except ImportError:
            self.skipTest("Pillow absent : la structure du controle est verifiee, pas la mesure")
        if str(RENDU) not in sys.path:
            sys.path.insert(0, str(RENDU))
        import controler_rendus

        image = Image.new("RGBA", (1600, 1200), (0, 0, 0, 0))
        image.paste((90, 90, 90, 255), (200, 300, 900, 800))   # la pièce, calamine
        image.paste((5, 5, 5, 255), (300, 500, 315, 510))       # 150 px de noir pur dans la partie servie
        image.paste((0, 0, 0, 255), (1100, 500, 1120, 520))     # 400 px noirs sous la fiche incrustée : pas servis
        with tempfile.TemporaryDirectory() as dossier:
            chemin = Path(dossier) / "rond.png"
            image.save(chemin)
            self.assertEqual(controler_rendus.noir_pur_servi(chemin), 150, "comptage du noir pur servi faux")

    def test_v12_l_aile_basse_du_u_se_distingue_du_fond(self):
        """Profil U : la coupe de l'aile basse se distingue du fond du U, vu au-dessus d'elle, d'au moins 8 niveaux.

        U alu, 24/09 (vérification indépendante de la reprise) : avec la coupe claire de l'aluminium (0,50), l'aile basse
        sortait à 149–155 contre 156–157 pour le fond du U (1 à 4 niveaux sur les 4 fiches) : son épaisseur ne se lisait
        plus. V9 mesure à la rangée de la pince, donc sur l'âme, et ne l'a pas vu. `contraste_aile_basse` mesure, sur la
        colonne des points de l'aile haute, la bande du bas de la pièce de l'épaisseur de l'aile haute contre le fond
        au-dessus. Pièce synthétique : aile basse 300-316 à 152, fond 200-300 à 156 puis 180. Exige Pillow."""
        arbre = ast.parse((RENDU / "controler_rendus.py").read_text(encoding="utf-8"))
        fonctions = {n.name: n for n in arbre.body if isinstance(n, ast.FunctionDef)}
        self.assertIn("contraste_aile_basse", fonctions, "controler_rendus.py ne mesure pas l'aile basse des profils U")
        appels = [n for n in ast.walk(fonctions.get("controler", ast.Module(body=[], type_ignores=[])))
                  if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "contraste_aile_basse"]
        self.assertTrue(appels, "controler() ne controle pas l'aile basse des profils U")
        try:
            from PIL import Image
        except ImportError:
            self.skipTest("Pillow absent : la structure du controle est verifiee, pas la mesure")
        if str(RENDU) not in sys.path:
            sys.path.insert(0, str(RENDU))
        import controler_rendus

        for fond, attendu in ((156, 4), (180, 28)):
            image = Image.new("RGBA", (500, 400), (0, 0, 0, 0))
            image.paste((150, 150, 150, 255), (200, 100, 300, 116))      # aile haute, coupée (points de pince à x = 250)
            image.paste((fond, fond, fond, 255), (200, 116, 300, 300))   # fond du U vu au-dessus de l'aile basse
            image.paste((152, 152, 152, 255), (200, 300, 300, 316))      # aile basse, coupée, en bas de la pièce
            with tempfile.TemporaryDirectory() as dossier:
                chemin = Path(dossier) / "u.png"
                image.save(chemin)
                coupe, face = controler_rendus.contraste_aile_basse(chemin, (250, 100), (250, 116))
            self.assertAlmostEqual(abs(face - coupe), attendu, delta=1, msg="mesure de l'aile basse du U fausse")

    def test_v13_la_fiche_tient_dans_le_recadrage_du_site(self):
        """Le cadre de la pièce d'une fiche (`boite` de `rendu_profil.py`, en coordonnées de caméra : u depuis la
        gauche, v depuis le bas) tient dans le recadrage servi par le site, à 0,005 de l'image de chaque bord.

        24/09, carré plein refait aux vues d'origine (ADR-0011) : le cadre de la pièce allait jusqu'à 0,62 de la
        largeur, le site coupe à 0,615. Avant l'audit, le chanfrein fixe de 0,6 mm arrondissait le bout de la barre,
        qui restait dans l'image ; avec les arêtes vives, le coin du bout arrière atteint le cadre et 6 à 8 px
        disparaissaient à la coupe : le bout de la barre ne se voyait plus. La photo studio n'est pas recadrée."""
        marge = 0.005
        arbre = ast.parse((RENDU / "recadrer_visuels.py").read_text(encoding="utf-8"))
        cadre_site = next(ast.literal_eval(n.value) for n in arbre.body if isinstance(n, ast.Assign)
                          and any(isinstance(c, ast.Name) and c.id == "CADRE" for c in n.targets))
        x0, y0, x1, y1 = cadre_site
        boites = []
        for noeud in ast.walk(arbre_du_rendu()):
            if not (isinstance(noeud, ast.If) and "caracteristiques" in ast.unparse(noeud.test)):
                continue
            for enfant in noeud.body:  # la branche de la fiche seulement : le `else` final est la photo studio
                for appel in ast.walk(enfant):
                    if (isinstance(appel, ast.Call) and isinstance(appel.func, ast.Attribute) and appel.func.attr == "get"
                            and len(appel.args) == 2 and isinstance(appel.args[0], ast.Constant)
                            and appel.args[0].value == "boite"):
                        boites.append(ast.literal_eval(appel.args[1]))
        self.assertGreaterEqual(len(boites), 3, "cadres des fiches introuvables dans rendu_profil.py : controle sans objet")
        fautifs = []
        for u0, v0, u1, v1 in boites:
            haut, bas = 1 - v1, 1 - v0  # v compte depuis le bas de l'image, le recadrage depuis le haut
            if u0 < x0 + marge or u1 > x1 - marge or haut < y0 + marge or bas > y1 - marge:
                fautifs.append(f"cadre {(u0, v0, u1, v1)} hors du recadrage du site {cadre_site} (marge {marge})")
        self.assertEqual(fautifs, [], "la piece d'une fiche peut etre coupee par le site : " + "; ".join(fautifs))

    def test_v14_la_composition_des_photos_studio_est_versionnee(self):
        """Chaque photo studio servie d'une famille de barres a sa composition dans `donnees/studios.json` : des fiches
        de la famille, trois au plus, d'une même finition ; et le préparateur la relit (`studio-famille`).

        ADR-0011 demande de rendre à nouveau les photos studio avec leur « trio de tailles d'origine ». Le 24/09, la
        séance web chargée de le faire ne l'a trouvé nulle part dans le dépôt : il vivait dans l'atelier du PC
        (`<famille>.studio.json`, `serie_audit.py`) ; il a fallu le retrouver en comparant des silhouettes aux
        anciennes images."""
        chemin = RENDU / "donnees" / "studios.json"
        self.assertTrue(chemin.exists(), "donnees/studios.json absent : la composition des photos studio n'est pas versionnee")
        compositions = json.loads(chemin.read_text(encoding="utf-8"))
        produits = json.loads(PRODUITS.read_text(encoding="utf-8"))
        with open(RACINE / "_DOCS" / "rendus-3d" / "inventaire-visuels.csv", encoding="utf-8-sig") as f:
            studios = [ligne.split(";")[0].removeprefix("studio-") for ligne in f if ";studio;" in ligne]
        fautifs = []
        for famille in studios:
            slugs = sorted(s for s, p in produits.items() if p["famille"] == famille)
            if not slugs:
                continue
            try:
                pc, _ = self.preparer.piece(produits[slugs[0]], 900, 1000)
            except KeyError:
                continue
            if pc["type"] not in BARRES_ATTENDUES:
                continue
            composition = compositions.get(famille)
            if not composition:
                fautifs.append(f"{famille} : composition absente")
                continue
            etrangers = [s for s in composition if s not in slugs]
            finitions = {self.preparer.piece(produits[s], 900, 1000)[1] for s in composition if s in produits}
            if etrangers or not 1 <= len(composition) <= 3 or len(finitions) > 1:
                fautifs.append(f"{famille} : {composition} (hors famille {etrangers}, finitions {finitions})")
        self.assertEqual(fautifs, [], f"{len(fautifs)} photo(s) studio sans composition versionnee : {fautifs[:6]}")
        source = (RENDU / "preparer_rendus.py").read_text(encoding="utf-8")
        self.assertIn('"studio-famille"', source, "preparer_rendus.py ne relit pas donnees/studios.json (studio-famille)")
        self.assertIn("studios.json", source, "preparer_rendus.py ne relit pas donnees/studios.json")

    def test_v15_le_bord_de_la_piece_reste_net_sur_le_blanc(self):
        """Posée sur le blanc, la pièce garde l'anticrénelage de son bord : un pixel que la pièce ne couvre qu'en
        partie sort comme une composition normale du rendu brut ; seule l'ombre du sol est allégée, y compris la part
        d'ombre d'un pixel mixte (bord de la pièce posé sur son ombre).

        Large plat, 24/09 (vérification indépendante) : `rendu_sur_blanc()` (habiller.py) traitait tout pixel d'alpha
        < 250 comme de l'ombre (× 0,55) ; le bord de la pièce ressortait 64 niveaux trop clair en médiane, en escalier,
        sur toutes les images habillées, fiches et photos studio — visible dès qu'on agrandit l'image servie de 2400 px.
        Dans le rendu brut, l'ombre est noire et le bord a la couleur de la pièce : la part de pièce d'un pixel se lit.
        `lisere_bord` (controler_rendus.py) le mesure sur chaque image servie. Exige Pillow pour la mesure."""
        arbre = ast.parse((RENDU / "controler_rendus.py").read_text(encoding="utf-8"))
        fonctions = {n.name: n for n in arbre.body if isinstance(n, ast.FunctionDef)}
        self.assertIn("lisere_bord", fonctions, "controler_rendus.py ne mesure pas le bord de la piece servie")
        appels = [n for n in ast.walk(fonctions.get("controler", ast.Module(body=[], type_ignores=[])))
                  if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "lisere_bord"]
        self.assertGreaterEqual(len(appels), 2, "controler() ne mesure pas le bord de la piece des fiches et du studio")
        try:
            from PIL import Image
        except ImportError:
            self.skipTest("Pillow absent : la structure du controle est verifiee, pas la mesure")
        if str(RENDU) not in sys.path:
            sys.path.insert(0, str(RENDU))
        import controler_rendus
        import habiller

        brut = Image.new("RGBA", (400, 300), (0, 0, 0, 0))
        brut.paste((0, 0, 0, 100), (100, 201, 300, 260))     # ombre du sol : noire, semi-transparente
        brut.paste((80, 80, 80, 255), (100, 100, 300, 200))  # la pièce, opaque, gris 80
        brut.paste((80, 80, 80, 128), (100, 99, 300, 100))   # bord sur le fond : la pièce couvre la moitié du pixel
        brut.paste((57, 57, 57, 178), (100, 200, 300, 201))  # bord sur l'ombre : moitié pièce, moitié ombre (100)
        with tempfile.TemporaryDirectory() as dossier:
            chemin = Path(dossier) / "piece.png"
            brut.save(chemin)
            blanc = habiller.rendu_sur_blanc(chemin, fondu=0)
            gris = blanc.convert("L")
            servie = Path(dossier) / "servie.png"
            blanc.convert("RGB").save(servie)
            ancien = brut.copy()  # bord traité en ombre, comme avant le 24/09
            ancien.paste((80, 80, 80, 70), (100, 99, 300, 100))
            ancien = Image.alpha_composite(Image.new("RGBA", brut.size, (255, 255, 255, 255)), ancien).convert("RGB")
            servie_ancienne = Path(dossier) / "ancienne.png"
            ancien.save(servie_ancienne)
            ecart_bon = controler_rendus.lisere_bord(chemin, servie)
            ecart_ancien = controler_rendus.lisere_bord(chemin, servie_ancienne)
        # composition normale du bord : 80 x 0,5 + 255 x 0,5 ; avant le 24/09, 207
        self.assertAlmostEqual(gris.getpixel((200, 99)), 167, delta=3, msg="le bord de la piece sort eclairci (lisere)")
        # ombre seule : allégée à 0,55, comme avant
        self.assertAlmostEqual(gris.getpixel((200, 230)), 200, delta=2, msg="l'ombre du sol n'est plus allegee")
        # pixel mixte : la part de pièce (40) garde sa couleur, la part d'ombre est allégée
        self.assertAlmostEqual(gris.getpixel((200, 200)), 140, delta=4, msg="le bord pose sur l'ombre est mal compose")
        self.assertIsNotNone(ecart_bon, "lisere_bord ne trouve aucun pixel de bord a mesurer")
        self.assertLess(abs(ecart_bon), 5, "lisere_bord signale un bord juste")
        self.assertGreater(ecart_ancien, 20, "lisere_bord ne voit pas le bord eclairci d'avant le 24/09")


if __name__ == "__main__":
    unittest.main()
