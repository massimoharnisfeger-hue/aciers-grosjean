@echo off
title Site Aciers Grosjean - Site local (ne pas fermer)
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0site-local.ps1" -Mode dev
pause
