@echo off
title Site Aciers Grosjean - Sauvegarde
echo Enregistrement des modifications et envoi sur GitHub...
echo Le travail part sur une branche, la pull request est creee, et la fusion se fait
echo automatiquement si le controle qualite est vert.
echo Resultat en ligne 2 a 3 minutes plus tard : https://aciers-grosjean.vercel.app
echo Cette fenetre reste ouverte le temps du controle (2 a 5 minutes).
echo (la premiere fois, une fenetre de connexion GitHub peut s'ouvrir)
echo.
rem Pose les garde-fous avant toute sauvegarde : .git\hooks n'est pas versionne,
rem donc sans cette ligne le controle ne protegerait aucun poste.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0..\scripts\installer-hooks.ps1"
echo.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0synchro.ps1" -Mode sauvegarder
echo.
pause
