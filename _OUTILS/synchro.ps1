# Synchronisation du dossier "Site Aciers Grosjean" avec GitHub.
#   -Mode auto        : (tache planifiee) recupere les nouveautes sans commit ni push automatique.
#                       Ne cree jamais de commit, ne touche pas a un travail en cours.
#   -Mode sauvegarder : (humain uniquement) enregistre tout (commit), recupere les nouveautes, puis envoie sur GitHub.
# Fichier volontairement sans accents : PowerShell 5.1 lit mal l'UTF-8 sans BOM.
param(
  [ValidateSet('auto', 'sauvegarder')][string]$Mode = 'auto',
  [string]$Message = ''
)

$racine = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $racine
$journal = Join-Path $PSScriptRoot 'synchro.log'

function Note([string]$texte) {
  $ligne = '{0}  [{1}] {2}' -f (Get-Date -Format 'yyyy-MM-dd HH:mm'), $Mode, $texte
  Add-Content -LiteralPath $journal -Value $ligne
  Write-Output $ligne
}

if (-not (Get-Command git -ErrorAction SilentlyContinue)) { Note 'ERREUR : git introuvable'; exit 1 }

# En automatique, aucune fenetre de connexion ne doit bloquer la tache.
if ($Mode -eq 'auto') { $env:GCM_INTERACTIVE = 'never'; $env:GIT_TERMINAL_PROMPT = '0' }

# Garder le log court.
if ((Test-Path -LiteralPath $journal) -and (Get-Item -LiteralPath $journal).Length -gt 200KB) {
  $fin = Get-Content -LiteralPath $journal -Tail 500
  Set-Content -LiteralPath $journal -Value $fin
}

if ($Mode -eq 'sauvegarder') {
  git add -A 2>$null
  git diff --cached --quiet
  if ($LASTEXITCODE -ne 0) {
    if (-not $Message) { $Message = 'Sauvegarde du ' + (Get-Date -Format 'dd/MM/yyyy HH:mm') }
    git commit --quiet -m $Message
    Note "Sauvegarde enregistree : $Message"
  }
}

git fetch origin --quiet 2>$null
if ($LASTEXITCODE -ne 0) { Note 'GitHub injoignable (hors ligne ?) : nouvel essai plus tard'; exit 0 }

$branche = (git rev-parse --abbrev-ref HEAD).Trim()
$enRetard = [int](git rev-list --count "HEAD..origin/$branche")
$enAvance = [int](git rev-list --count "origin/$branche..HEAD")
$modifsLocales = [bool](git status --porcelain)

if ($enRetard -gt 0) {
  if ($modifsLocales) {
    Note "$enRetard nouveaute(s) sur GitHub, mais des modifications locales ne sont pas enregistrees : recuperation reportee"
  }
  elseif ($enAvance -gt 0) {
    git rebase --quiet "origin/$branche" 2>$null
    if ($LASTEXITCODE -ne 0) {
      git rebase --abort 2>$null
      Note 'CONFLIT entre GitHub et ce PC : rien n a ete modifie. Demander a Claude de fusionner.'
      exit 1
    }
    Note "$enRetard nouveaute(s) recuperee(s) depuis GitHub"
  }
  else {
    git merge --ff-only --quiet "origin/$branche" 2>$null
    Note "$enRetard nouveaute(s) recuperee(s) depuis GitHub"
  }
}

$enAvance = [int](git rev-list --count "origin/$branche..HEAD")
if ($enAvance -gt 0) {
  if ($Mode -eq 'auto') {
    Note "AUTO-PUSH DESACTIVE : $enAvance commit(s) restent locaux. Validation humaine requise."
  }
  else {
    git push --quiet origin $branche 2>$null
    if ($LASTEXITCODE -eq 0) { Note "$enAvance sauvegarde(s) envoyee(s) sur GitHub : le site en ligne se met a jour" }
    else { Note 'ENVOI IMPOSSIBLE : connexion GitHub a faire une fois (double-clic sur SAUVEGARDER.cmd)' }
  }
}
elseif ($enRetard -eq 0) {
  if ($modifsLocales) { Note 'A jour avec GitHub. Des modifications locales attendent une sauvegarde.' }
  else { Note 'Deja a jour' }
}
