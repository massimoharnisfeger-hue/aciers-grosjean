"""Registre des controles du depot.

Decouvre et execute tous les controles de `tests/`, puis affiche :

    N controles - M echecs - T secondes

INVARIANT : N ne diminue jamais.
-------------------------------
Le nombre de controles atteint est memorise dans `tests/socle.json`. Si un
lancement en compte moins, ce script echoue. Un controle rouge se corrige, il
ne se supprime pas et il ne se desactive pas.

Pour abaisser volontairement le socle (fusion de deux controles en un seul,
suppression d'un controle devenu faux), il faut editer `tests/socle.json` a la
main et ecrire pourquoi dans `_DOCS/LECONS.md`. C'est un acte conscient, pas un
effet de bord.

Usage :
    python tests/lancer.py
    python tests/lancer.py -v                 (detail de chaque controle)
    python tests/lancer.py --dossier <chemin> (autre dossier de controles)

`--dossier` sert aux controles qui verifient ce lanceur lui-meme : sans lui,
son contrat de sortie ne serait garanti par rien. Le socle suivi est alors
celui du dossier vise, pas celui du depot.

Code de sortie : 0 si tout passe, 1 sinon.
"""

import json
import sys
import time
import unittest
from datetime import date
from pathlib import Path

RACINE = Path(__file__).resolve().parents[1]
DOSSIER_TESTS = RACINE / "tests"

# Une suite lente est une suite qu'on saute. Reglable par `budget_secondes`
# dans socle.json, mais le relever doit etre un acte reflechi, pas un reflexe.
BUDGET_PAR_DEFAUT = 60


def dossier_vise(argv: list[str]) -> Path:
    """Dossier de controles a executer : `tests/` par defaut, sinon --dossier."""
    if "--dossier" in argv:
        indice = argv.index("--dossier")
        if indice + 1 < len(argv):
            return Path(argv[indice + 1]).resolve()
    return DOSSIER_TESTS


def _sortie_utf8() -> None:
    """La console Windows est en cp1252 par defaut : evite un plantage sur les accents."""
    for flux in (sys.stdout, sys.stderr):
        try:
            flux.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass


def compter(suite: unittest.TestSuite) -> int:
    """Nombre de controles unitaires dans une suite, sous-suites comprises."""
    total = 0
    for element in suite:
        if isinstance(element, unittest.TestSuite):
            total += compter(element)
        else:
            total += 1
    return total


def lire_socle(socle: Path) -> dict:
    if not socle.exists():
        return {}
    try:
        return json.loads(socle.read_text(encoding="utf-8"))
    except json.JSONDecodeError as erreur:
        print(f"socle.json illisible : {erreur}", file=sys.stderr)
        return {}


def ecrire_socle(socle: Path, controles: int, existant: dict) -> None:
    """Releve le maximum sans perdre les autres reglages (budget, notes)."""
    donnees = dict(existant)
    donnees["controles_max"] = controles
    donnees["date"] = date.today().isoformat()
    socle.write_text(
        json.dumps(donnees, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    _sortie_utf8()
    if str(RACINE) not in sys.path:
        sys.path.insert(0, str(RACINE))

    dossier = dossier_vise(sys.argv)
    socle_fichier = dossier / "socle.json"

    chargeur = unittest.TestLoader()
    suite = chargeur.discover(str(dossier), pattern="test_*.py")
    controles = compter(suite)

    detail = "-v" in sys.argv or "--verbose" in sys.argv
    debut = time.perf_counter()
    resultat = unittest.TextTestRunner(
        verbosity=2 if detail else 1, stream=sys.stderr
    ).run(suite)
    duree = time.perf_counter() - debut

    echecs = len(resultat.failures) + len(resultat.errors)

    socle = lire_socle(socle_fichier)
    maximum = socle.get("controles_max", 0)
    regression_socle = controles < maximum

    print()
    print(f"{controles} controles - {echecs} echecs - {duree:.1f} s")

    if regression_socle:
        print(
            f"SOCLE ROMPU : {maximum} controles atteints le "
            f"{socle.get('date', '?')}, {controles} aujourd'hui. "
            f"{maximum - controles} controle(s) ont disparu.",
            file=sys.stderr,
        )
        return 1

    if controles > maximum:
        ecrire_socle(socle_fichier, controles, socle)
        if maximum:
            print(f"socle releve : {maximum} -> {controles} controles")
        else:
            print(f"socle initialise a {controles} controles")

    budget = socle.get("budget_secondes", BUDGET_PAR_DEFAUT)
    if duree > budget:
        print(
            f"BUDGET DEPASSE : {duree:.1f} s pour un budget de {budget} s. "
            f"Une suite lente finit par etre sautee : isoler le controle lent "
            f"ou l'accelerer, ne pas relever le budget par reflexe.",
            file=sys.stderr,
        )
        return 1

    return 1 if echecs else 0


if __name__ == "__main__":
    raise SystemExit(main())
