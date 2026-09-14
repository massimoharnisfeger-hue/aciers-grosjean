@echo off
title Site Aciers Grosjean - Sauvegarde
echo Enregistrement des modifications et envoi sur GitHub...
echo (la premiere fois, une fenetre de connexion GitHub peut s'ouvrir)
echo.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0synchro.ps1" -Mode sauvegarder
echo.
pause
