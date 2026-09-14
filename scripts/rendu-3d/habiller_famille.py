"""
Habille tous les visuels d'une ou plusieurs familles (rendus bruts dans %LOCALAPPDATA%/SiteAciersGrosjean/rendu3d/final/),
photo studio comprise, puis lance les controles automatiques (controler_rendus.py).

  python scripts/rendu-3d/habiller_famille.py <famille> [<famille> ...]

Code de sortie : celui des controles (1 s'il reste un ecart, ou si un rendu manque).
"""
import json
import os
import subprocess
import sys
from pathlib import Path

ICI = Path(__file__).resolve().parent
FINAL = Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / "SiteAciersGrosjean" / "rendu3d" / "final"


def lancer(*args):
    r = subprocess.run([sys.executable, *args], capture_output=True, text=True, encoding="utf-8", errors="replace")
    derniere = (r.stdout.strip().splitlines() or [""])[-1]
    if r.returncode:
        derniere = (r.stderr.strip().splitlines() or [derniere])[-1]
    return r.returncode, derniere


def main():
    familles = sys.argv[1:]
    if not familles:
        raise SystemExit(__doc__)
    produits = json.loads((ICI / "donnees" / "produits.json").read_text(encoding="utf-8"))
    manquants = 0
    for famille in familles:
        slugs = sorted(s for s, p in produits.items() if p["famille"] == famille)
        print(f"== {famille} : {len(slugs)} fiches")
        for slug in slugs:
            if not (FINAL / f"{slug}.png").exists():
                print(f"   MANQUANT {slug}")
                manquants += 1
                continue
            code, ligne = lancer(ICI / "habiller.py", slug)
            print(f"   {'ERREUR' if code else 'ok'} {slug} -> {ligne}")
        studio = f"studio-{famille}"
        if (FINAL / f"{studio}.png").exists():
            code, ligne = lancer(ICI / "habiller.py", "--studio", studio)
            print(f"   {'ERREUR' if code else 'ok'} {studio} -> {ligne}")
        else:
            print(f"   MANQUANT {studio}")
            manquants += 1
    r = subprocess.run([sys.executable, str(ICI / "controler_rendus.py"), *familles])
    sys.exit(1 if manquants else r.returncode)


if __name__ == "__main__":
    main()
