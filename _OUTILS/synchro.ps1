# Synchronisation du dossier "Site Aciers Grosjean" avec GitHub.
#   -Mode auto        : (tache planifiee) recupere les nouveautes sans commit ni push automatique.
#                       Ne cree jamais de commit, ne touche pas a un travail en cours.
#   -Mode sauvegarder : (humain uniquement) enregistre tout (commit), recupere les nouveautes,
#                       puis envoie le travail sur une BRANCHE et affiche le lien de la pull request.
#                       `main` est protegee cote GitHub : push direct refuse, pull request + check
#                       "quality" obligatoires (voir docs/architecture/SYNC_POLICY.md).
# Fichier volontairement sans accents : PowerShell 5.1 lit mal l'UTF-8 sans BOM.
param(
  [ValidateSet('auto', 'sauvegarder')][string]$Mode = 'auto',
  [string]$Message = '',
  # Nom distinct de $branche (branche courante) : PowerShell ignore la casse,
  # les deux seraient la MEME variable. Garde : tests/test_gate.py (S3).
  [string]$BrancheCible = ''
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
    # `main` est protegee : GitHub refuse le push direct ("Changes must be made
    # through a pull request"). Le travail part donc sur une branche, et c'est
    # la pull request qui, une fois le check "quality" vert, met le site a jour.
    $brancheTravail = $BrancheCible
    if (-not $brancheTravail) {
      if ($branche -ne 'main') { $brancheTravail = $branche }
      else { $brancheTravail = 'travail/' + (Get-Date -Format 'yyyy-MM-dd-HHmm') }
    }
    if ($brancheTravail -ne $branche) { git branch -f $brancheTravail HEAD 2>$null }

    # stderr capture, pas jete : un envoi refuse doit dire POURQUOI (protection de
    # branche, reseau, identifiants). Un message devine envoie chercher au mauvais
    # endroit - c'est la lecon L-021.
    $refspec = "{0}:{1}" -f $brancheTravail, $brancheTravail
    Note "Envoi de $refspec"
    $sortiePush = (git push --quiet -u origin $refspec 2>&1 | ForEach-Object { $_.ToString().Trim() }) -join ' / '
    if ($LASTEXITCODE -eq 0) {
      $depot = (git remote get-url origin).Trim() -replace '\.git$', ''
      $lien = "$depot/pull/new/$brancheTravail"
      Note "$enAvance sauvegarde(s) envoyee(s) sur la branche $brancheTravail"
      Note 'DERNIERE ETAPE : ouvrir la pull request, puis fusionner quand le controle "quality" est vert.'
      Note $lien
      Note 'Deploiement de cette branche (avant fusion) : https://vercel.com/massimoharnisfeger-hues-projects/aciers-grosjean'
      Note 'Le site de production ne change qu a la fusion dans main.'
      Start-Process $lien -ErrorAction SilentlyContinue
    }
    else {
      Note 'ENVOI IMPOSSIBLE. Message de GitHub ci-dessous ; rien n a ete perdu, le travail reste enregistre sur ce PC.'
      if ($sortiePush) { Note "  git : $sortiePush" }
      Note '  Si GitHub parle de "pull request" : la branche est protegee, passer par le lien de PR.'
    }
  }
}
elseif ($enRetard -eq 0) {
  if ($modifsLocales) { Note 'A jour avec GitHub. Des modifications locales attendent une sauvegarde.' }
  else { Note 'Deja a jour' }
}
