# Publie un travail deja pousse : pull request, attente du controle "quality", fusion.
# Appele par _OUTILS/synchro.ps1 apres un push reussi ; utilisable seul :
#   powershell -File scripts\publier.ps1 -Branche travail/2026-09-22-0130
#
# Pourquoi ce script existe : pousser une branche ne change rien a ce que le
# proprietaire voit. La production Vercel (https://aciers-grosjean.vercel.app)
# ne bouge qu'a une fusion dans `main`. Demande du 22/09/2026 : voir chaque
# modification sur Vercel. Regle et garde-fous : ADR-0009, tests/test_gate.py (S5).
#
# Ne fusionne JAMAIS sur un controle rouge ou en attente d'un resultat.
# Fichier volontairement sans accents : PowerShell 5.1 lit mal l'UTF-8 sans BOM.
param(
  [Parameter(Mandatory = $true)][string]$Branche,
  [string]$Base = 'main',
  [int]$AttenteMaxMinutes = 12
)

$ErrorActionPreference = 'Stop'
$depot = 'massimoharnisfeger-hue/aciers-grosjean'
$production = 'https://aciers-grosjean.vercel.app'

function Note([string]$texte) {
  $ligne = '{0}  [publier] {1}' -f (Get-Date -Format 'yyyy-MM-dd HH:mm'), $texte
  Add-Content -LiteralPath (Join-Path $PSScriptRoot '..\_OUTILS\synchro.log') -Value $ligne
  Write-Output $ligne
}

# Le jeton est celui que Git utilise deja pour pousser : aucun secret nouveau,
# rien d'ecrit sur le disque, rien d'affiche.
function Jeton {
  # L'entree passe par un FICHIER redirige, pas par un tuyau. Mesure du 22/09 :
  # @('protocol=https','host=github.com','') | git credential fill fait repondre
  # 'refusing to work with credential missing protocol field' : git ne recoit rien
  # et lit EOF. La meme entree redirigee depuis un fichier renvoie les quatre
  # lignes attendues. La forme tableau reglait la mise en forme de l'entree ; elle
  # ne reglait pas son acheminement. Controle S7.
  #
  # Le fichier ne contient aucun secret (protocole et hote seulement) ; le jeton
  # revient par la sortie standard et ne touche jamais le disque.
  #
  # Pas de 2>$null ici : sous PowerShell 5.1, rediriger stderr d'une commande
  # native emballe chaque ligne dans une ErrorRecord, et $ErrorActionPreference
  # a 'Stop' transforme ca en erreur terminante. Le script mourrait sans message.
  $prudent = $ErrorActionPreference
  $ErrorActionPreference = 'Continue'
  $demande = Join-Path ([System.IO.Path]::GetTempPath()) ('cred-' + [guid]::NewGuid().ToString('N') + '.txt')
  try {
    # LF et ligne vide finale : git credential fill lit ligne par ligne.
    [System.IO.File]::WriteAllText($demande, "protocol=https`nhost=github.com`n", [System.Text.Encoding]::ASCII)
    $reponse = cmd /c "git credential fill < ""$demande"""
  } catch {
    $reponse = @()
  } finally {
    $ErrorActionPreference = $prudent
    Remove-Item $demande -Force -ErrorAction SilentlyContinue
  }
  foreach ($l in $reponse) { if ($l -like 'password=*') { return $l.Substring(9) } }
  return $null
}

function AppelGitHub($methode, $chemin, $corps) {
  $entetes = @{ Authorization = "Bearer $jeton"; Accept = 'application/vnd.github+json'; 'User-Agent' = 'aciers-grosjean-publier' }
  $parametres = @{ Method = $methode; Uri = "https://api.github.com$chemin"; Headers = $entetes }
  if ($corps) { $parametres.Body = ($corps | ConvertTo-Json -Depth 5 -Compress); $parametres.ContentType = 'application/json' }
  return Invoke-RestMethod @parametres
}

$jeton = Jeton
if (-not $jeton) { Note 'PUBLICATION IMPOSSIBLE : aucun identifiant GitHub enregistre. Lancer SAUVEGARDER.cmd une fois pour se connecter.'; exit 1 }

# ---- 1. la pull request (reutilisee si elle existe deja)
try {
  $ouvertes = AppelGitHub GET "/repos/$depot/pulls?state=open&head=massimoharnisfeger-hue:$Branche"
} catch { Note "PUBLICATION IMPOSSIBLE : GitHub injoignable ($($_.Exception.Message))"; exit 1 }

if ($ouvertes.Count -gt 0) {
  $pr = $ouvertes[0]
  Note "Pull request existante : $($pr.html_url)"
} else {
  $titre = (git log -1 --format=%s).Trim()
  $corps = "Publication automatique depuis SAUVEGARDER.cmd. Le detail des changements est dans les messages de commit, ``_JOURNAL/`` et ``docs/decisions/``.`n`nFusionnee seulement si le controle ``quality`` est vert (ADR-0009).`n`nGenerated with Claude Code"
  try {
    $pr = AppelGitHub POST "/repos/$depot/pulls" @{ title = $titre; head = $Branche; base = $Base; body = $corps }
    Note "Pull request creee : $($pr.html_url)"
  } catch { Note "PULL REQUEST IMPOSSIBLE : $($_.Exception.Message)"; exit 1 }
}

# ---- 2. le controle "quality" doit finir, et finir vert
$sha = (git rev-parse HEAD).Trim()
$limite = (Get-Date).AddMinutes($AttenteMaxMinutes)
$conclusion = $null
Note "Attente du controle 'quality' sur $($sha.Substring(0,7))..."
while ((Get-Date) -lt $limite) {
  Start-Sleep -Seconds 20
  try { $checks = AppelGitHub GET "/repos/$depot/commits/$sha/check-runs" }
  catch { continue }   # coupure reseau passagere : on retente au tour suivant
  $q = $checks.check_runs | Where-Object { $_.name -eq 'quality' } | Select-Object -First 1
  if ($q -and $q.status -eq 'completed') { $conclusion = $q.conclusion; break }
}

if ($conclusion -ne 'success') {
  if ($null -eq $conclusion) { Note "CONTROLE TOUJOURS EN COURS apres $AttenteMaxMinutes min : rien n a ete fusionne." }
  else { Note "CONTROLE 'quality' : $conclusion. RIEN N A ETE FUSIONNE - corriger, puis relancer." }
  Note "Suivi : $($pr.html_url)/checks"
  exit 1
}
Note 'Controle quality : vert.'

# ---- 3. fusion, puis la seule adresse a regarder
try {
  $fusion = AppelGitHub PUT "/repos/$depot/pulls/$($pr.number)/merge" @{ merge_method = 'merge' }
} catch { Note "FUSION REFUSEE par GitHub : $($_.Exception.Message)"; Note "A faire a la main : $($pr.html_url)"; exit 1 }

if (-not $fusion.merged) { Note "FUSION REFUSEE : $($fusion.message)"; exit 1 }
Note "Fusionne dans $Base."
Note "EN LIGNE DANS 2 A 3 MINUTES : $production"
Note 'Suivi du deploiement : https://vercel.com/massimoharnisfeger-hues-projects/aciers-grosjean'
exit 0
