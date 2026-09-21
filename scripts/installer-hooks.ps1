# Installe les hooks Git du depot.
#
# Les hooks vivent dans .git/hooks/, qui n'est pas versionne : chaque poste doit
# les installer une fois. La source versionnee est scripts/hooks/.
#
#   powershell -File scripts/installer-hooks.ps1
#
# Relancer apres un clone, ou apres toute modification de scripts/hooks/.

$ErrorActionPreference = 'Stop'

$racine = Split-Path -Parent $PSScriptRoot
$source = Join-Path $PSScriptRoot 'hooks'
$cible = Join-Path $racine '.git\hooks'

if (-not (Test-Path $cible)) {
    Write-Host "Pas de dossier .git\hooks : ce dossier n'est pas un depot Git." -ForegroundColor Red
    exit 1
}

$poses = 0
foreach ($hook in Get-ChildItem -Path $source -File) {
    $destination = Join-Path $cible $hook.Name
    Copy-Item -Path $hook.FullName -Destination $destination -Force
    Write-Host "hook pose : $($hook.Name)"
    $poses++
}

Write-Host ""
Write-Host "$poses hook(s) installe(s) dans .git\hooks." -ForegroundColor Green
Write-Host "Desormais, un commit avec un controle rouge est refuse." -ForegroundColor Green
Write-Host "Verifier a tout moment : python tests/lancer.py"
