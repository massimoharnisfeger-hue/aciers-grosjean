#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Synchronise /home/user/grosjean (source de travail) vers le dépôt git.

ATTENTION — piège corrigé ici : avec os.walk(topdown=False), modifier `dirs`
n'a AUCUN effet, les exclusions sont ignorées et la passe de suppression entre
dans .git. On filtre donc explicitement sur le chemin relatif, jamais sur la
liste `dirs`.
"""

import os, shutil, filecmp, sys
from pathlib import Path

SRC = Path("/home/user/grosjean")
DST = Path(sys.argv[1] if len(sys.argv) > 1 else "/home/user/aciers-grosjean")

EXCLUS_DIRS = {".git", "node_modules", ".next", "shots"}
EXCLUS_FICHIERS = {"capture.js", "dev.log", "srv.log"}


def exclu(rel: Path) -> bool:
    """Vrai si le chemin relatif traverse un dossier exclu."""
    return any(p in EXCLUS_DIRS for p in rel.parts)


def copier():
    n = 0
    for root, dirs, files in os.walk(SRC):
        rel = Path(root).relative_to(SRC)
        if exclu(rel):
            dirs[:] = []
            continue
        dirs[:] = [d for d in dirs if d not in EXCLUS_DIRS]
        (DST / rel).mkdir(parents=True, exist_ok=True)
        for f in files:
            if f in EXCLUS_FICHIERS:
                continue
            s, t = Path(root) / f, DST / rel / f
            if not t.exists() or not filecmp.cmp(s, t, shallow=False):
                shutil.copy2(s, t)
                n += 1
    return n


def supprimer():
    n = 0
    for root, _dirs, files in os.walk(DST, topdown=False):
        rel = Path(root).relative_to(DST)
        if exclu(rel):          # ← le filtre qui manquait
            continue
        for f in files:
            if f in EXCLUS_FICHIERS:
                continue
            if not (SRC / rel / f).exists():
                (Path(root) / f).unlink()
                n += 1
        p = Path(root)
        if rel != Path(".") and not any(p.iterdir()) and not (SRC / rel).exists():
            p.rmdir()
    return n


if __name__ == "__main__":
    c, d = copier(), supprimer()
    print(f"copiés : {c}  supprimés : {d}")
