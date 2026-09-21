"""Controles du journal des decisions.

Une decision tranchee et ecrite ne se repose pas. Encore faut-il qu'elle soit
retrouvable : un ADR cite quelque part et introuvable sur le disque est pire
qu'une decision jamais ecrite, parce qu'on croit pouvoir s'y referer.

Le gabarit n'est pas invente ici : il vient de `docs/decisions/README.md`, qui
preexiste. Ces controles ne font que le rendre obligatoire.
"""

import re
import unittest
from pathlib import Path

RACINE = Path(__file__).resolve().parents[1]
DOSSIER = RACINE / "docs" / "decisions"

CHAMPS = (
    "ID",
    "DATE",
    "STATUS",
    "DECISION",
    "REASON",
    "IMPACT",
    "SUPERSEDES",
    "VALIDATED_BY",
)
STATUTS = {"ACTIVE", "SUPERSEDED", "DEPRECATED", "REJECTED"}

FORMAT_NOM = re.compile(r"^(\d{4})-[a-z0-9-]+\.md$")
FORMAT_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
REFERENCE = re.compile(r"ADR-(\d{4})")

# Arbres tiers : leur contenu n'est pas ecrit par le projet.
EXCLUS = (".git", "node_modules", "__pycache__", ".claude/skills", ".agents/skills")


def fichiers_adr() -> list[Path]:
    if not DOSSIER.exists():
        return []
    return sorted(p for p in DOSSIER.glob("*.md") if FORMAT_NOM.match(p.name))


def champs(fichier: Path) -> dict:
    texte = fichier.read_text(encoding="utf-8")
    trouves = {}
    for champ in CHAMPS:
        capture = re.search(rf"^{champ}:[ \t]*(.*)$", texte, re.MULTILINE)
        trouves[champ] = capture.group(1).strip() if capture else None
    return trouves


def markdown_du_projet() -> list[Path]:
    fichiers = []
    for chemin in RACINE.rglob("*.md"):
        relatif = chemin.relative_to(RACINE).as_posix()
        if any(relatif.startswith(exclu) for exclu in EXCLUS):
            continue
        fichiers.append(chemin)
    return fichiers


class DecisionsTests(unittest.TestCase):
    def test_le_journal_des_decisions_n_est_pas_vide(self):
        self.assertTrue(
            fichiers_adr(),
            "docs/decisions/ ne contient aucune decision. Les arbitrages "
            "empiles ailleurs (project-state/CURRENT_STATE.md) ne sont pas "
            "retrouvables et se reposent a chaque session.",
        )

    def test_chaque_decision_suit_le_gabarit_du_readme(self):
        for fichier in fichiers_adr():
            trouves = champs(fichier)
            for champ in CHAMPS:
                self.assertIsNotNone(
                    trouves[champ],
                    f"{fichier.name} : champ '{champ}:' manquant. Le gabarit est "
                    f"celui de docs/decisions/README.md, il ne s'en invente pas "
                    f"un second.",
                )
            self.assertRegex(
                trouves["DATE"],
                FORMAT_DATE,
                f"{fichier.name} : DATE attendue au format AAAA-MM-JJ.",
            )

    def test_les_identifiants_sont_uniques_et_correspondent_au_nom_de_fichier(self):
        vus = {}
        for fichier in fichiers_adr():
            numero = FORMAT_NOM.match(fichier.name).group(1)
            self.assertNotIn(
                numero,
                vus,
                f"Numero {numero} porte par {fichier.name} et {vus.get(numero)}. "
                f"Un numero ne se reutilise jamais.",
            )
            vus[numero] = fichier.name
            identifiant = champs(fichier)["ID"] or ""
            self.assertIn(
                numero,
                identifiant,
                f"{fichier.name} : le champ ID ('{identifiant}') ne contient pas "
                f"le numero du fichier ({numero}).",
            )

    def test_les_statuts_sont_valides(self):
        for fichier in fichiers_adr():
            brut = champs(fichier)["STATUS"] or ""
            statut = brut.split()[0] if brut.split() else ""
            self.assertIn(
                statut,
                STATUTS,
                f"{fichier.name} : STATUS '{statut}' hors de {sorted(STATUTS)}.",
            )

    def test_chaque_reference_a_une_decision_existe(self):
        numeros = {FORMAT_NOM.match(f.name).group(1) for f in fichiers_adr()}
        for fichier in markdown_du_projet():
            texte = fichier.read_text(encoding="utf-8", errors="replace")
            for numero in set(REFERENCE.findall(texte)):
                self.assertIn(
                    numero,
                    numeros,
                    f"{fichier.relative_to(RACINE).as_posix()} cite ADR-{numero}, "
                    f"qui n'existe pas dans docs/decisions/. Une decision citee "
                    f"et introuvable est pire qu'une decision jamais ecrite.",
                )


if __name__ == "__main__":
    unittest.main()
