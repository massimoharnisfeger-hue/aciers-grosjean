@echo off
title Site Aciers Grosjean - Mise a jour
echo Recuperation des nouveautes depuis GitHub...
echo.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0synchro.ps1" -Mode auto
echo.
pause
