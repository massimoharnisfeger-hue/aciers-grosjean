@echo off
chcp 65001 >nul
title Aciers Grosjean - Site local
cd /d "%~dp0"
echo ============================================
echo    ACIERS GROSJEAN - Lancement du site
echo ============================================
echo.
where node >nul 2>nul
if errorlevel 1 (
  echo [!] Node.js n est pas installe. Ouverture du telechargement (LTS).
  echo     Installe-le, puis relance ce fichier.
  start https://nodejs.org/fr
  pause
  exit /b
)
echo [OK] Node.js : & node -v & echo.
if not exist node_modules (
  echo [..] Premiere installation, patiente 1 a 2 minutes...
  call npm install
  if errorlevel 1 ( echo [!] Installation echouee. & pause & exit /b )
)
echo [..] Demarrage du site...
start "Serveur Grosjean (ne pas fermer)" cmd /k npm run dev
timeout /t 12 /nobreak >nul
start "" http://localhost:3000
echo  Le site : http://localhost:3000  ^|  Pour arreter : ferme la fenetre noire.
pause
