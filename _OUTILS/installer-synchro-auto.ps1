# Installe (ou reinstalle) la tache Windows qui synchronise le dossier avec GitHub toutes les 2 heures.
# A relancer seulement si le dossier est deplace. Aucun droit administrateur necessaire.
# Fichier volontairement sans accents : PowerShell 5.1 lit mal l'UTF-8 sans BOM.

$nom = 'Site Aciers Grosjean - synchro GitHub'
$script = Join-Path $PSScriptRoot 'synchro.ps1'

# conhost --headless : aucune fenetre ne s'ouvre pendant la synchro.
$action = New-ScheduledTaskAction -Execute 'conhost.exe' `
  -Argument "--headless powershell.exe -NoProfile -ExecutionPolicy Bypass -File `"$script`" -Mode auto"

$toutesLes2h = New-ScheduledTaskTrigger -Once -At (Get-Date).Date.AddHours(8) `
  -RepetitionInterval (New-TimeSpan -Hours 2) -RepetitionDuration (New-TimeSpan -Days 3650)

# StartWhenAvailable : si le PC etait eteint a l'heure prevue, la synchro part des qu'il est rallume.
$reglages = New-ScheduledTaskSettingsSet -StartWhenAvailable -AllowStartIfOnBatteries `
  -DontStopIfGoingOnBatteries -ExecutionTimeLimit (New-TimeSpan -Minutes 10) -MultipleInstances IgnoreNew

Register-ScheduledTask -TaskName $nom -Action $action -Trigger $toutesLes2h -Settings $reglages `
  -Description 'Recupere les nouveautes GitHub du site Aciers Grosjean et envoie les sauvegardes deja enregistrees. Journal : _OUTILS\synchro.log' `
  -Force | Out-Null

Write-Output "Tache installee : $nom"
