# Lance ou verifie le site sur ce PC SANS installer node_modules dans OneDrive.
# Le code est copie dans %LOCALAPPDATA%\SiteAciersGrosjean\build, puis installe et demarre la-bas.
#   -Mode dev      : ouvre le site sur http://localhost:3000
#   -Mode verifier : TypeScript + build de production (a lancer avant chaque envoi)
# Fichier volontairement sans accents : PowerShell 5.1 lit mal l'UTF-8 sans BOM.
param([ValidateSet('dev', 'verifier')][string]$Mode = 'dev')

$racine = Split-Path -Parent $PSScriptRoot
$build = Join-Path $env:LOCALAPPDATA 'SiteAciersGrosjean\build'

if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
  Write-Host 'Node.js n est pas installe. Installe la version LTS puis relance.'
  Start-Process 'https://nodejs.org/fr'
  exit 1
}

New-Item -ItemType Directory -Force -Path $build | Out-Null
robocopy $racine $build /MIR /XD .git node_modules .next _DEPOT _OUTILS __pycache__ /XF *.pyc /NFL /NDL /NJH /NJS /NP | Out-Null
if ($LASTEXITCODE -ge 8) { Write-Host 'Copie du code impossible.'; exit 1 }

Set-Location -LiteralPath $build
Write-Host 'Installation des dependances (1 a 2 minutes la premiere fois)...'
npm install --no-audit --no-fund
if ($LASTEXITCODE -ne 0) { Write-Host 'Installation echouee.'; exit 1 }

if ($Mode -eq 'verifier') {
  Write-Host '--- TypeScript ---'
  npx tsc --noEmit
  if ($LASTEXITCODE -ne 0) { Write-Host 'ECHEC : erreurs TypeScript.'; exit 1 }
  Write-Host '--- Build de production ---'
  npm run build
  if ($LASTEXITCODE -ne 0) { Write-Host 'ECHEC : le build ne passe pas.'; exit 1 }
  Write-Host 'OK : TypeScript et build de production passent.'
  exit 0
}

Start-Job -ScriptBlock { Start-Sleep -Seconds 12; Start-Process 'http://localhost:3000' } | Out-Null
Write-Host 'Le site demarre sur http://localhost:3000 (fermer cette fenetre pour l arreter).'
Write-Host 'Les modifications faites ensuite dans le dossier du Bureau demandent de relancer ce bouton.'
npx next dev -p 3000
