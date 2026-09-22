"""Controles des 652 redirections 301 des anciennes URLs.

Constat du 22/09/2026 : 15 destinations sur 622 ne menent nulle part. 22
anciennes URLs repondent donc 301 puis 404 — le visiteur et le lien entrant
sont perdus deux fois. La cause n'est pas une faute de frappe : le blueprint
(`_DOCS/catalogue-site-actuel/inventaire-urls.csv`, colonne
`URL_cible_recommandee`) proposait des pages a creer (« page de contenu a
realimenter ou fusionner ») et ces cibles ont ete reprises telles quelles,
sans jamais verifier qu'elles existaient. `/acier/poutrelles/hem`,
`/toiture-bardage/panneau-tuile`, `/commande`, `/compte/profil` n'ont jamais
ete construites.

Second constat : `lib/redirections.mjs` porte l'en-tete « GENERE, NE PAS
EDITER A LA MAIN — Generateur : scripts/generer-redirections.py », et ce
generateur etait un commentaire de trois lignes. Le fichier etait donc tenu a
la main sous une etiquette qui disait le contraire.

RD1 - Toute destination mene a une route reellement servie.
RD2 - Aucune chaine : une destination n'est jamais elle-meme une source.
RD3 - Aucune source declaree deux fois (la seconde regle serait morte).
RD4 - `lib/redirections.mjs` est bien ce que son generateur produit.

RD1 lit les routes par `scripts/routes.py`, qui les deduit de la source comme
`generateStaticParams` le fait a la compilation. Verifie le 22/09 contre
`.next/prerender-manifest.json` : meme ensemble, au `/_not-found` pres.
"""

import re
import subprocess
import sys
import unittest
from pathlib import Path

RACINE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RACINE / "scripts"))

from routes import routes_du_depot  # noqa: E402

REDIRECTIONS = RACINE / "lib" / "redirections.mjs"
GENERATEUR = RACINE / "scripts" / "generer-redirections.py"

PAIRE = re.compile(r'\{\s*source:\s*"([^"]+)"\s*,\s*destination:\s*"([^"]+)"')


def paires() -> list[tuple[str, str]]:
    return PAIRE.findall(REDIRECTIONS.read_text(encoding="utf-8"))


class Redirections(unittest.TestCase):
    def test_rd1_chaque_destination_existe(self):
        routes = routes_du_depot()
        mortes = sorted({d for _, d in paires() if d not in routes})
        self.assertEqual(
            mortes,
            [],
            f"{len(mortes)} destinations repondent 301 puis 404 : {mortes}",
        )

    def test_rd2_aucune_chaine_de_redirection(self):
        p = paires()
        sources = {s for s, _ in p}
        chaines = sorted({(s, d) for s, d in p if d in sources})
        self.assertEqual(chaines, [], f"redirections en deux sauts : {chaines}")

    def test_rd3_aucune_source_en_double(self):
        vues, doubles = set(), []
        for s, _ in paires():
            if s in vues:
                doubles.append(s)
            vues.add(s)
        self.assertEqual(doubles, [], f"sources declarees deux fois : {doubles}")

    def test_rd4_le_fichier_est_bien_celui_du_generateur(self):
        r = subprocess.run(
            [sys.executable, "-X", "utf8", str(GENERATEUR), "--verifier"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=str(RACINE),
        )
        self.assertEqual(
            r.returncode,
            0,
            "lib/redirections.mjs ne correspond pas a son generateur :\n"
            + (r.stdout or "") + (r.stderr or ""),
        )


if __name__ == "__main__":
    unittest.main()
