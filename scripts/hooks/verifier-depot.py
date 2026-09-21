"""Verifie les fichiers d'un commit avant qu'il parte.

Lit des chemins sur l'entree standard (un par ligne), relatifs au repertoire
courant, et refuse :

  - les fichiers d'environnement (.env, .env.production...), sauf .env.example ;
  - les fichiers de plus de 5 Mo ;
  - les fichiers contenant un motif de secret connu.

Sortie 0 si tout va bien, 1 sinon, avec la liste des problemes.

Appele par scripts/hooks/pre-commit. Volontairement separe du hook : un script
autonome s'exerce sans creer de commit, ce qui rend le garde-fou testable
(tests/test_depot.py). Un garde-fou non testable finit par ne plus garder.
"""

import re
import sys
from pathlib import Path

TAILLE_MAX = 5 * 1024 * 1024  # 5 Mo

# .env, .env.local, .env.production... mais pas .env.example.
FICHIER_ENV = re.compile(r"(^|/)\.env($|\.(?!example)[A-Za-z0-9_.-]+$)")

MOTIFS_SECRETS = (
    ("jeton GitHub", re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}")),
    ("cle AWS", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("cle Stripe", re.compile(r"sk_live_[0-9A-Za-z]{10,}")),
    ("cle OpenAI", re.compile(r"sk-(proj-)?[A-Za-z0-9]{20,}")),
    ("jeton Slack", re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}")),
    ("jeton Notion", re.compile(r"ntn_[A-Za-z0-9]{20,}")),
    ("jeton Airtable", re.compile(r"\bpat[A-Za-z0-9]{14}\.[A-Za-z0-9]{40,}")),
    ("cle Google", re.compile(r"AIza[0-9A-Za-z_-]{30,}")),
    ("cle privee", re.compile(r"BEGIN (RSA|OPENSSH|EC|PGP) PRIVATE KEY")),
)

# Fichiers dont le contenu documente les motifs eux-memes : les scanner
# reviendrait a s'interdire d'ecrire le garde-fou.
EXEMPTS_DE_SCAN = (
    "scripts/hooks/verifier-depot.py",
    "tests/test_depot.py",
    ".github/workflows/quality.yml",
    "package-lock.json",
)


def problemes(chemin: str, secrets_seulement: bool = False) -> list[str]:
    fichier = Path(chemin)
    normalise = chemin.replace("\\", "/")
    trouves = []

    if FICHIER_ENV.search(normalise):
        trouves.append(
            f"{chemin} : fichier d'environnement. Le depot est PUBLIC. "
            f"Utiliser .env.example sans valeurs."
        )

    if not fichier.is_file():
        return trouves

    taille = fichier.stat().st_size
    if not secrets_seulement and taille > TAILLE_MAX:
        trouves.append(
            f"{chemin} : {taille / 1024 / 1024:.1f} Mo, au-dela de la limite "
            f"de {TAILLE_MAX // 1024 // 1024} Mo. Compresser, ou deposer dans "
            f"_DEPOT/ qui n'est pas versionne."
        )

    if normalise in EXEMPTS_DE_SCAN:
        return trouves

    try:
        contenu = fichier.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return trouves

    for nom, motif in MOTIFS_SECRETS:
        if motif.search(contenu):
            trouves.append(
                f"{chemin} : ressemble a un secret ({nom}). Ne jamais le "
                f"commiter sur un depot public ; le revoquer s'il a existe."
            )

    return trouves


def main() -> int:
    # Mode secrets : utilise par la CI, qui scanne TOUT le depot. La taille y
    # est hors sujet — des PDF volumineux y sont deja versionnes, et faire
    # echouer la CI dessus la rendrait rouge en permanence, donc ignoree.
    secrets_seulement = "--secrets-seulement" in sys.argv

    chemins = [ligne.strip() for ligne in sys.stdin if ligne.strip()]
    if not chemins:
        return 0

    tous = []
    for chemin in chemins:
        tous.extend(problemes(chemin, secrets_seulement))

    if tous:
        print("COMMIT REFUSE — verification du depot :")
        for probleme in tous:
            print(f"  - {probleme}")
        print("")
        print(f"{len(chemins)} fichier(s) inspecte(s), {len(tous)} probleme(s).")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
