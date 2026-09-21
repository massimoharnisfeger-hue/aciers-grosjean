"""Controles de l'index des sources.

`_DOCS/INDEX.md` declare qui fait autorite sur quoi. Un index qui vieillit sans
qu'on s'en apercoive est pire qu'une absence d'index : on s'y fie.

Ces controles garantissent trois choses : les chemins cites existent, aucun
fichier n'est declare deux fois comme source d'autorite, et les liens entre
documents du depot menent quelque part.
"""

import re
import unittest
from pathlib import Path

RACINE = Path(__file__).resolve().parents[1]
INDEX = RACINE / "_DOCS" / "INDEX.md"

EXTENSIONS = (".md", ".ts", ".tsx", ".json", ".mjs", ".py", ".csv", ".yml", ".ps1")
LIEN_MARKDOWN = re.compile(r"\[[^\]]+\]\(([^)]+)\)")

EXCLUS = (".git", "node_modules", "__pycache__", ".claude/skills", ".agents/skills")


def lignes_de_tableau(texte: str) -> list[list[str]]:
    """Cellules des lignes de tableau, en-tetes et separateurs exclus."""
    lignes = []
    for ligne in texte.splitlines():
        depouillee = ligne.strip()
        if not depouillee.startswith("|"):
            continue
        cellules = [c.strip() for c in depouillee.strip("|").split("|")]
        if len(cellules) != 4:
            continue
        if cellules[0] in ("Fait", "") or set(cellules[0]) <= {"-", ":"}:
            continue
        lignes.append(cellules)
    return lignes


def chemins(cellule: str) -> list[str]:
    """Chemins cites entre accents graves dans une cellule."""
    trouves = []
    for brut in re.findall(r"`([^`]+)`", cellule):
        if "/" in brut or brut.endswith(EXTENSIONS):
            trouves.append(brut)
    return trouves


def markdown_du_projet() -> list[Path]:
    fichiers = []
    for chemin in RACINE.rglob("*.md"):
        relatif = chemin.relative_to(RACINE).as_posix()
        if any(relatif.startswith(exclu) for exclu in EXCLUS):
            continue
        fichiers.append(chemin)
    return fichiers


class IndexTests(unittest.TestCase):
    def setUp(self):
        self.texte = INDEX.read_text(encoding="utf-8") if INDEX.exists() else ""
        self.lignes = lignes_de_tableau(self.texte)

    def test_l_index_existe_et_contient_des_sources(self):
        self.assertTrue(
            INDEX.exists(),
            "_DOCS/INDEX.md declare qui fait autorite sur quoi : il doit exister.",
        )
        self.assertGreaterEqual(
            len(self.lignes),
            10,
            "L'index doit couvrir les faits du projet, pas quelques-uns.",
        )

    def test_tous_les_chemins_cites_existent(self):
        for cellules in self.lignes:
            for cellule in cellules:
                for chemin in chemins(cellule):
                    self.assertTrue(
                        (RACINE / chemin).exists(),
                        f"L'index cite '{chemin}' (ligne « {cellules[0]} »), "
                        f"qui n'existe pas sur le disque.",
                    )

    def test_aucun_fait_n_a_deux_sources_d_autorite(self):
        vues = {}
        for cellules in self.lignes:
            for source in chemins(cellules[1]):
                self.assertNotIn(
                    source,
                    vues,
                    f"'{source}' est declare source d'autorite pour « {cellules[0]} » "
                    f"et pour « {vues.get(source)} ». Un fait = une source.",
                )
                vues[source] = cellules[0]

    def test_chaque_source_generee_nomme_un_generateur_reel(self):
        for cellules in self.lignes:
            generateur = cellules[2]
            if generateur.strip() in ("—", "-", ""):
                continue
            cites = chemins(generateur)
            self.assertTrue(
                cites,
                f"« {cellules[0]} » : colonne « Généré par » remplie ('{generateur}') "
                f"mais aucun chemin de script cite entre accents graves.",
            )
            for chemin in cites:
                self.assertTrue(
                    (RACINE / chemin).exists(),
                    f"« {cellules[0]} » : generateur '{chemin}' introuvable.",
                )

    def test_les_controles_de_l_index_ne_sont_pas_vides(self):
        """Un controle qui n'inspecte rien passe au vert sans rien garantir.

        Mesure du 21/09 : 38 chemins verifies pour 23 lignes de tableau. Si
        l'index est vide de sa substance, les controles ci-dessus deviendraient
        verts par vacuite ; celui-ci passe rouge a la place.
        """
        total = sum(len(chemins(cellule)) for ligne in self.lignes for cellule in ligne)
        self.assertGreaterEqual(
            total,
            20,
            f"L'index ne cite que {total} chemins : les controles qui le lisent "
            f"ne verifient presque rien et passeraient au vert par vacuite.",
        )

    def test_chaque_lien_entre_documents_resout(self):
        """Garde tourne vers l'avenir.

        Mesure du 21/09 : 65 fichiers .md inspectes, 2 liens markdown trouves,
        0 interne. Le depot cite ses fichiers entre accents graves, pas en liens
        markdown : ce controle ne prouve donc rien aujourd'hui, il empeche une
        regression le jour ou des liens apparaitront. Elargir aux chemins entre
        accents graves de tout le depot a ete mesure et ecarte : 241 faux
        positifs sur 502 (URL du site, fichiers a creer), soit un rouge
        permanent qu'on apprendrait a ignorer.
        """
        for fichier in markdown_du_projet():
            texte = fichier.read_text(encoding="utf-8", errors="replace")
            for cible in LIEN_MARKDOWN.findall(texte):
                if cible.startswith(("http://", "https://", "#", "mailto:")):
                    continue
                cible = cible.split("#")[0]
                if not cible:
                    continue
                resolu = (fichier.parent / cible).resolve()
                self.assertTrue(
                    resolu.exists(),
                    f"{fichier.relative_to(RACINE).as_posix()} pointe vers "
                    f"'{cible}', qui ne mene nulle part.",
                )


if __name__ == "__main__":
    unittest.main()
