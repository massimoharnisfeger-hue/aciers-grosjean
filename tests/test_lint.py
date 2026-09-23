"""Controles de l'outillage de qualite JavaScript/TypeScript.

`next build` ne lint rien : sans ESLint declare et lance, aucune regle de
qualite JS/TS n'est appliquee sur 40 pages et 32 composants.

Ces controles verifient la DECLARATION (dependance, script, configuration,
synchronisation du lock, etape CI). Ils ne lancent pas ESLint : un controle
qui ne peut pas s'executer partout (sessions web sans node_modules) ne doit
pas pretendre le faire.
L'execution reelle appartient a `_OUTILS/site-local.ps1` et a la CI.

C1 - Aucun composant `"use client"` n'importe `lib/catalogue.ts` ni
     `lib/edito.ts`. La regle est ecrite dans CLAUDE.md depuis le depart :
     « tout le catalogue partirait dans le JavaScript du navigateur ». Rien ne
     la verifiait. Mesure du 22/09 sur une fiche produit : la page pesait
     2 241 Ko dont 52 Ko d'images, et le plus gros fichier — 485 Ko — etait le
     chunk de `/recherche`, telecharge sur CHAQUE page parce que l'en-tete y
     renvoie et que Next precharge les liens visibles. `Recherche.tsx` etait
     `"use client"` et importait `tousProduits` : les 495 produits avec leurs
     prix, leurs specs et leurs poids partaient chez le visiteur.

     La parade prevue par la regle : calculer dans la page serveur, passer en
     props. Ce controle lit la premiere ligne du fichier pour la directive, et
     ses imports : il ne lance rien, il se contente de rendre la regle
     opposable.

     Il ne compte QUE les imports de valeurs. `import type { Produit }` est
     efface a la compilation et n'embarque rien : trois composants le font, et
     les signaler aurait appris a ignorer ce controle.
"""

import json
import re
import unittest
from pathlib import Path

RACINE = Path(__file__).resolve().parents[1]
APP = RACINE / "app"
COMPOSANTS = RACINE / "components"
# Modules dont l'import cote client embarquerait tout le catalogue.
LOURDS = ("@/lib/catalogue", "@/lib/edito")
PAQUET = RACINE / "package.json"
LOCK = RACINE / "package-lock.json"
CI = RACINE / ".github" / "workflows" / "quality.yml"

CONFIGURATIONS = ("eslint.config.mjs", "eslint.config.js", ".eslintrc.json")


def paquet() -> dict:
    return json.loads(PAQUET.read_text(encoding="utf-8"))


class DonneesCoteClient(unittest.TestCase):
    """C1 : le catalogue reste sur le serveur."""

    def test_c1_aucun_composant_client_n_importe_le_catalogue(self):
        fautifs = []
        for fichier in list(APP.rglob("*.tsx")) + list(COMPOSANTS.rglob("*.tsx")):
            texte = fichier.read_text(encoding="utf-8")
            premiere = next((l.strip() for l in texte.splitlines() if l.strip()), "")
            if "use client" not in premiere:
                continue
            for declaration in re.findall(r"import[^;]*?from " + chr(34) + "[^" + chr(34) + "]+" + chr(34), texte, re.S):
                module = declaration.rsplit(chr(34), 2)[1]
                if module not in LOURDS:
                    continue
                if declaration.lstrip().startswith("import type"):
                    continue
                noms = re.search(r"\{([^}]*)\}", declaration)
                if noms and all(
                    n.strip().startswith("type ") for n in noms.group(1).split(",") if n.strip()
                ):
                    continue
                fautifs.append(f"{fichier.name} importe des valeurs de {module}")
        self.assertEqual(
            fautifs, [],
            "un composant client embarque le catalogue dans le navigateur "
            "(CLAUDE.md, ligne 19) : calculer dans la page serveur et passer "
            "en props. " + str(fautifs),
        )


class LintTests(unittest.TestCase):
    def test_eslint_est_declare_en_dependance_de_developpement(self):
        dev = paquet().get("devDependencies", {})
        for attendu in ("eslint", "eslint-config-next"):
            self.assertIn(
                attendu,
                dev,
                f"{attendu} absent des devDependencies : rien ne lint le code.",
            )

    def test_un_script_lint_existe(self):
        scripts = paquet().get("scripts", {})
        self.assertIn(
            "lint",
            scripts,
            "package.json doit exposer un script `lint` : une dependance "
            "installee que personne n'appelle ne verifie rien.",
        )

    def test_une_configuration_eslint_existe(self):
        presentes = [nom for nom in CONFIGURATIONS if (RACINE / nom).is_file()]
        self.assertTrue(
            presentes,
            f"Aucune configuration ESLint parmi {CONFIGURATIONS}. "
            f"ESLint sans configuration n'applique aucune regle.",
        )

    def test_le_lock_est_synchronise_avec_le_paquet(self):
        """Un lock desynchronise fait echouer `npm ci` en CI.

        C'est le piege de ce chantier : ajouter une dependance a package.json
        sans regenerer package-lock.json casse la CI au premier push, alors que
        tout parait correct en local.
        """
        dev = paquet().get("devDependencies", {})
        lock = LOCK.read_text(encoding="utf-8")
        for dependance in dev:
            self.assertIn(
                f'"node_modules/{dependance}"',
                lock,
                f"{dependance} est dans package.json mais absent de "
                f"package-lock.json : `npm ci` echouera en CI.",
            )

    def test_la_ci_lance_le_lint(self):
        texte = CI.read_text(encoding="utf-8")
        self.assertIn(
            "run lint",
            texte,
            "La CI doit lancer le lint : declare mais jamais execute, il ne "
            "garde rien.",
        )


if __name__ == "__main__":
    unittest.main()
