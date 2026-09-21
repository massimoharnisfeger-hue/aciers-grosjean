"""Controles de l'emplacement du depot.

Jusqu'au 21/09/2026 le depot vivait dans `OneDrive\\Bureau\\Site Aciers Grosjean`.
OneDrive y remplacait 1 767 fichiers de `.git` par des placeholders « en ligne
seulement » (ReparsePoint), verrouillait les fichiers pendant la synchro, et
faisait de `npm install` une operation interdite. C'est le mode de corruption
classique d'un depot Git, et la decision H1 (`_DOCS/CHANTIERS-RENFORCEMENT.md`)
etait ouverte depuis le 14/09.

Le 21/09, le depot est parti dans `C:\\Users\\massi\\Projects\\aciers-grosjean`
(ADR-0005). `_DEPOT/` (photos, documents) reste dans OneDrive, monte ici par une
jonction : sauvegarde par OneDrive, ignore par Git, exactement comme avant.

E1 - Le depot n'est pas sous un chemin OneDrive. Un retour en arriere
     (copie, restauration, nouveau clone au mauvais endroit) redevient rouge.
E2 - `_DEPOT` existe et est lisible : la jonction tient. Si OneDrive deplace
     ou renomme la cible, les scripts d'inventaire et de rendus 3D echoueraient
     silencieusement.

Un controle sur les placeholders OneDrive dans `.git` (attribut ReparsePoint)
a ete ecrit puis retire le 21/09 : il n'a jamais ete vu rouge, les lectures de
la seance ayant hydrate les fichiers avant lui. Un controle jamais vu rouge ne
prouve rien (_DOCS/LECONS.md).

E2 lit le systeme de fichiers local : sans objet en CI (pas de `_DEPOT`), il
s'y declare ignore.
"""

import os
import unittest
from pathlib import Path

RACINE = Path(__file__).resolve().parents[1]
DEPOT = RACINE / "_DEPOT"

EN_CI = os.environ.get("CI", "").lower() in ("1", "true", "yes")



class EmplacementDuDepot(unittest.TestCase):
    """Le depot vit hors de tout dossier synchronise par un cloud."""

    def test_e1_le_depot_n_est_pas_sous_onedrive(self):
        self.assertNotIn(
            "onedrive",
            str(RACINE).lower(),
            f"Le depot est sous OneDrive : {RACINE}. Decision H1 / ADR-0005 : il vit "
            f"dans C:\\Users\\massi\\Projects\\aciers-grosjean. Ne pas travailler ici.",
        )

    def test_e2_le_depot_de_photos_est_monte(self):
        if EN_CI:
            self.skipTest("_DEPOT n'existe pas en CI (ignore par Git, depot public).")
        self.assertTrue(
            DEPOT.is_dir() and (DEPOT / "LISEZ-MOI.txt").exists(),
            f"_DEPOT n'est pas lisible depuis {RACINE} : la jonction vers OneDrive "
            f"est cassee ou la cible a bouge. Recreer : New-Item -ItemType Junction "
            f"-Path _DEPOT -Target <OneDrive>\\Site Aciers Grosjean\\_DEPOT",
        )


if __name__ == "__main__":
    unittest.main()
