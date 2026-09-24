# Carnet de leçons

Ce que le dépôt a appris. Chaque erreur constatée entre ici **avec le contrôle qui l'empêche de
revenir** — c'est ce qui distingue un carnet d'un journal.

À lire au début de chaque itération, avant de toucher à quoi que ce soit.

## Règles d'écriture

1. Une leçon = un symptôme observé, sa cause réelle, l'ID du contrôle qui l'attrape, la date.
2. **Une leçon sans contrôle ne compte pas.** Le contrôle s'écrit avant la correction, se voit
   rouge, puis vert. `tests/test_socle.py` rejette toute leçon citant un contrôle inexistant.
3. Format imposé, vérifié automatiquement :

```
### L-000 — titre court
- **Symptôme** : ce qui a été observé, factuellement.
- **Cause** : la cause réelle, pas le premier soupçon.
- **Contrôle** : `tests/fichier.py::Classe::methode`
- **Date** : AAAA-MM-JJ
```

4. Numérotation continue, jamais réutilisée. Une leçon corrigée est réécrite, pas supprimée.
5. Un défaut vu **une** fois devient un contrôle. Pas deux.

Carnet spécialisé de la production 3D : `_DOCS/rendus-3d/lecons.md` (réglages Blender, cadrages,
matières). Il reste séparé : son périmètre est la fabrication des images, celui-ci est le dépôt.

---

## Leçons

### L-001 — un code de sortie lu après un tube n'est pas celui du script
- **Symptôme** : la première vérification de `tests/lancer.py` a affiché `CODE_SORTIE=0` alors que le script sortait bien en 1. La ligne Z1 a failli être fermée sur une preuve fausse.
- **Cause** : `python tests/lancer.py | tail -25` suivi de `echo $?` mesure le code de `tail`, dernier maillon du tube, jamais celui du script. Le tube masque l'échec au lieu de le remonter.
- **Contrôle** : `tests/test_socle.py::LanceurTests::test_le_lanceur_sort_en_erreur_si_un_controle_echoue`
- **Date** : 2026-09-21

### L-012 — une règle appliquée à un endroit et oubliée à l'autre
- **Symptôme** : `docs/architecture/EXTERNAL_CAPABILITIES.md` épingle les skills externes au commit près (`15de38fb…`, `34040c9c…`), mais `.github/workflows/quality.yml` utilisait `actions/checkout@v4` et `actions/setup-node@v4` — des tags **mutables**, pour deux actions qui s'exécutent avec accès en lecture à tout le dépôt.
- **Cause** : la règle « épingler au commit » existait comme *pratique documentée*, pas comme *contrôle*. Elle a donc été appliquée là où quelqu'un y a pensé, et oubliée ailleurs. Une règle sans contrôle n'est pas une règle, c'est une habitude — et les habitudes ne traversent pas les fichiers.
- **Précaution de résolution** : les SHA n'ont pas été devinés. `git ls-remote --tags https://github.com/actions/checkout refs/tags/v4` donne `11d5960a326750d5838078e36cf38b85af677262`, et setup-node `49933ea5288caeca8642d1e84afbd3f7d6820020`. Un SHA inventé aurait cassé la CI silencieusement jusqu'au prochain push.
- **Contrôle** : `tests/test_project_os.py::ProjectOsTests::test_ci_actions_are_pinned_by_commit`
- **Date** : 2026-09-21

### L-011 — une liste blanche figée est un contrôle qui s'auto-détruit
- **Symptôme** : `test_working_tree_changes_are_allowed_and_no_deletion` était rouge en permanence sur ce poste depuis le 17/09. Il exigeait que **tout** chemin modifié figure dans une liste blanche de 36 lignes. Mesure du 21/09 : 26 chemins modifiés, la quasi-totalité hors liste.
- **Cause** : la liste était l'instantané des fichiers qu'une séance avait touchés. Elle décrit un passé, pas une règle. Toute journée de travail normale la contredit — le contrôle était donc programmé pour devenir faux, dès le lendemain de son écriture.
- **Conséquence réelle** : rouge permanent = contrôle ignoré. Et un contrôle qu'on a appris à ignorer ne protège plus **même quand il a raison** : la garde contre les suppressions accidentelles, elle légitime, était noyée dans le même échec depuis quatre jours.
- **Remède** : garder la moitié qui exprime une règle (aucun fichier suivi ne disparaît), supprimer celle qui décrit un instantané. Réserve déclarée : ce garde est local, vacant en CI sur un checkout neuf.
- **Règle générale** : un contrôle doit exprimer une **invariance**, jamais un **état**. Si sa formulation contient une liste de ce qui existait le jour où il a été écrit, il est déjà périmé.
- **Contrôle** : `tests/test_extensions.py::ExtensionTests::test_no_tracked_file_is_deleted_in_the_working_tree`
- **Date** : 2026-09-21

### L-010 — confondre un déclencheur et une opération désarme la vérification
- **Symptôme** : la CI ne s'est exécutée sur aucun des 69 commits du dépôt. Elle ne se déclenchait que sur `pull_request`, alors que le dépôt n'a qu'une branche et n'a jamais eu la moindre PR. Typecheck, build, tests et scan de secrets tournaient dans le vide pendant que chaque push sur `main` déployait en production.
- **Cause** : `tests/test_project_os.py:118` et `scripts/validation/project_os_check.py:87` rangeaient la chaîne `"  push:"` dans la même liste d'interdits que `git push`, `vercel` et `npm publish`. Or `push:` est un **déclencheur** — il dit *quand* la CI se lance — tandis que les autres sont des **opérations** — ce que la CI *fait*. La règle voulue était « la CI ne publie jamais » ; telle qu'écrite, elle disait aussi « la CI ne vérifie jamais le chemin de production ».
- **Gravité particulière** : le défaut était **verrouillé par des tests verts**. Corriger la CI faisait échouer la suite, ce qui donnait l'impression que la CI était correcte. Un contrôle mal formulé ne se contente pas de manquer un défaut, il le protège.
- **Remède** : deux contrôles séparés — l'un exige le déclencheur sur `main`, l'autre garde l'interdiction réelle de publier et vérifie `contents: read`.
- **Contrôle** : `tests/test_project_os.py::ProjectOsTests::test_ci_runs_on_the_production_path`
- **Date** : 2026-09-21

### L-009 — deux listes qui doivent dire la même chose finissent toujours par diverger
- **Symptôme** : le hook `pre-commit` cherchait 9 motifs de secrets, la CI 4, écrits séparément — un `git grep` inline dans `quality.yml:52`. Un jeton Notion, Airtable, Google, Slack ou OpenAI passait la CI sans être vu.
- **Cause** : la même règle exprimée deux fois, dans deux langages, à deux endroits. Personne ne les compare jamais, et en pratique **c'est la plus permissive qui décide** : il suffit de franchir la porte la moins attentive.
- **Remède** : la CI appelle le même script que le hook (`verifier-depot.py --secrets-seulement`), avec un mode qui neutralise la vérification de taille — sans quoi elle serait rouge en permanence sur des PDF déjà versionnés, donc ignorée. Une seule liste de motifs, deux usages.
- **Portée** : c'est le même défaut que les trois hiérarchies de précédence concurrentes du dépôt (L-004) et que les deux carnets de leçons (ADR-0002). À surveiller à chaque fois qu'une règle est réécrite ailleurs « pour aller plus vite ».
- **Contrôle** : `tests/test_depot.py::VerificateurDeCommitTests::test_la_ci_et_le_hook_partagent_les_memes_motifs`
- **Date** : 2026-09-21

### L-008 — un garde-fou qu'on ne peut exercer sans effet de bord ne sera jamais testé
- **Symptôme** : le hook `pre-commit` écrit en Z6 ne pouvait être vérifié qu'en tentant un vrai commit. La boucle l'interdit, et à raison : si le garde-fou avait échoué, le commit serait passé. Le contrôle n'aurait donc jamais été écrit, et le garde-fou serait resté une intention.
- **Cause** : la logique vivait dans le hook, dont le seul point d'entrée est Git. Tout ce qui ne s'invoque qu'à travers un effet irréversible échappe aux contrôles.
- **Remède** : extraire la logique dans `scripts/hooks/verifier-depot.py`, script autonome qui lit des chemins sur l'entrée standard. Le hook n'est plus que six lignes de plomberie. Le garde-fou s'exerce alors sur des fichiers jetables, sans toucher à Git. **Règle générale : un garde-fou se conçoit avec son point d'entrée testable, pas après.**
- **Mesure** : exercé sur les 874 fichiers suivis — 2 problèmes réels (PDF de 19,9 et 9,6 Mo), zéro faux positif sur les 9 motifs de secrets.
- **Contrôle** : `tests/test_depot.py::VerificateurDeCommitTests::test_il_refuse_un_jeton`
- **Date** : 2026-09-21

### L-007 — un motif d'exclusion qui ressemble à une protection n'en est pas une
- **Symptôme** : `.gitignore:7` contenait `.env*.local`. À l'œil, la ligne « parle de `.env` » et rassure. Interrogé, Git répondait que `.env`, `.env.production`, `.env.development`, `.vercel/project.json`, `.claude/settings.local.json`, `*.pem` et `*.key` seraient **commités** — sur un dépôt public, avec un bouton qui fait `git add -A` puis push sans revue.
- **Cause** : le motif exige le suffixe `.local`. Il ne couvre donc que le cas le plus rare et laisse passer le cas standard. Personne ne l'a vu parce que la ligne a été lue, jamais testée : lire un fichier de configuration ne dit pas ce que l'outil en fait.
- **Remède** : le contrôle n'analyse pas le texte de `.gitignore`, il interroge `git check-ignore`. Une ligne peut être annulée plus bas par une négation ; seul le comportement réel compte.
- **Contrôle** : `tests/test_depot.py::GitignoreTests::test_les_fichiers_sensibles_sont_ignores`
- **Date** : 2026-09-21

### L-006 — un contrôle qui interdit une formulation attrape aussi ceux qui la citent
- **Symptôme** : le contrôle qui interdit à l'état d'affirmer la propreté de l'arbre de travail est devenu rouge sur la note qui explique précisément pourquoi cette affirmation a été retirée. Le texte de correction déclenchait le contrôle de la faute.
- **Cause** : un contrôle qui cherche une formulation ne distingue pas l'assertion de la citation. La tentation immédiate est d'exempter les notes — et c'est le piège : l'exception devient le trou par lequel la vraie affirmation repasse un jour, sous forme de « note ».
- **Remède retenu** : garder le contrôle strict et reformuler la prose. Quand un contrôle et un texte se contredisent, c'est presque toujours le texte qui doit céder ; un contrôle truffé de cas particuliers cesse d'être fiable.
- **Contrôle** : `tests/test_etat.py::EtatTests::test_l_etat_ne_se_prononce_pas_sur_le_working_tree`
- **Date** : 2026-09-21

### L-005 — un contrôle qui n'inspecte rien est un faux vert
- **Symptôme** : les cinq contrôles de l'index sont passés verts du premier coup. Mesure : `test_chaque_lien_entre_documents_resout` inspectait **0 lien interne** sur 65 fichiers `.md`. Il ne garantissait rien et l'annonçait comme une réussite.
- **Cause** : le dépôt cite ses fichiers entre accents graves, jamais en liens Markdown. Le contrôle avait été écrit sur une hypothèse de format au lieu d'une mesure. Un vert sans dénombrement de ce qui a été inspecté ne distingue pas « rien à redire » de « rien à voir ».
- **Remède écarté, et pourquoi** : élargir aux chemins entre accents graves de tout le dépôt a été mesuré — 241 introuvables sur 502, presque tous faux positifs (URL du site, fichiers que les chantiers demandent de créer). Ç'aurait été un rouge permanent, donc un contrôle qu'on apprend à ignorer, soit le défaut **B3** reproduit volontairement.
- **Contrôle** : `tests/test_index.py::IndexTests::test_les_controles_de_l_index_ne_sont_pas_vides`
- **Date** : 2026-09-21

### L-004 — un gabarit qui existe déjà vaut mieux qu'un gabarit neuf
- **Symptôme** : au début du chantier Z3, un format d'ADR allait être défini de zéro. `docs/decisions/README.md` en contenait déjà un, complet, à huit champs, écrit le 17/09.
- **Cause** : la ligne de chantier décrivait le besoin (« contexte, décision, conséquence, date, qui a tranché ») sans dire qu'un gabarit existait, et le réflexe est de produire plutôt que de chercher. C'est exactement ce qui a fabriqué les trois hiérarchies de précédence concurrentes que l'audit du jour reproche au dépôt : chacune a été écrite par quelqu'un qui n'a pas lu la précédente.
- **Contrôle** : `tests/test_decisions.py::DecisionsTests::test_chaque_decision_suit_le_gabarit_du_readme`
- **Date** : 2026-09-21

### L-003 — un parseur qui lit la notice comme des données
- **Symptôme** : le contrôle du carnet est devenu rouge à sa première exécution, sur une leçon `L-000` que personne n'avait écrite, avec une date `AAAA-MM-JJ` et un contrôle `tests/fichier.py` inexistants.
- **Cause** : le parseur ne retirait pas les blocs de code encadrés. L'exemple de format donné dans la notice du fichier était lu comme une vraie leçon. Le document se contredisait lui-même à travers sa propre documentation — piège classique de tout contrôle qui lit du Markdown écrit pour des humains.
- **Contrôle** : `tests/test_socle.py::CarnetDeLeconsTests::test_les_exemples_de_format_ne_sont_pas_lus_comme_des_lecons`
- **Date** : 2026-09-21

### L-002 — une vérification faite à la main ne survit pas au premier refactor
- **Symptôme** : l'invariant « le nombre de contrôles ne diminue jamais » a d'abord été prouvé en éditant `tests/socle.json` à la main, en lisant le message, puis en restaurant le fichier. La preuve était réelle ce jour-là et nulle le lendemain : rien ne l'aurait rejouée.
- **Cause** : confusion entre *démontrer* un comportement une fois et le *garder*. Seul un contrôle du dépôt garde quelque chose ; une manipulation manuelle ne laisse qu'une trace dans une conversation, et les conversations ne sont pas rejouées.
- **Contrôle** : `tests/test_socle.py::LanceurTests::test_le_lanceur_refuse_une_suite_amputee`
- **Date** : 2026-09-21

### L-013 — une taille de police héritée ne se voit pas dans la classe du champ
- **Symptôme** : sur iPhone, la page s'agrandissait dès qu'on touchait un champ du formulaire de devis et n'en revenait pas toujours. Ressenti comme « le site bug sur mobile », alors que la mise en page ne déborde nulle part : mesures du 21/09 sur 12 gabarits à 320, 375, 768 et 1280 px, `scrollWidth` égal à la largeur d'écran partout.
- **Cause** : Safari iOS agrandit la page quand un champ focalisé a une police sous 16 px. `champStyle` ne déclarait aucune taille ; les 14 px venaient du `text-sm` porté par le `<label>` parent. Lire la classe du champ ne pouvait donc pas révéler le défaut — seule la taille calculée au navigateur le montre. Corrigé par `text-base` explicite, qui ne dépend plus du parent.
- **Contrôle** : `tests/test_mobile.py::FormulaireDevisMobile::test_m1_champs_au_moins_16px`
- **Date** : 2026-09-21

### L-014 — un formulaire sans `name` ni `autoComplete` fait retaper chaque visiteur
- **Symptôme** : les 6 champs du formulaire de devis ne proposaient aucun remplissage automatique, et le champ téléphone ouvrait un clavier alphabétique. Comptage sur le source : 0 `name`, 0 `autoComplete`, 0 `inputMode` sur les 115 lignes du fichier.
- **Cause** : le formulaire pilote tout par `useState` et envoie par `mailto:`, donc rien dans le code applicatif n'avait besoin de ces attributs pour fonctionner. Ils sont invisibles au développeur et décisifs pour le visiteur mobile — une absence qui ne casse rien ne se remarque jamais sans contrôle.
- **Contrôle** : `tests/test_mobile.py::FormulaireDevisMobile::test_m3_identite_remplissable_automatiquement`
- **Date** : 2026-09-21

### L-015 — la demande de devis partait par la messagerie du visiteur, ou ne partait pas
- **Symptôme** : `DevisForm.tsx` construisait un `mailto:` ; aucune requête ne partait vers le site, aucune trace n'existait côté entreprise, et sur un téléphone sans client mail configuré la demande disparaissait. Aucun contrôle n'appelait une route : `GET /api/devis` répondait 404.
- **Cause** : H4 ouverte depuis le 14/09 sans décision. Du point de vue du code, le formulaire « fonctionnait » : une absence d'envoi ne casse rien de visible, elle ne se remarque qu'en comptant les devis qui n'arrivent pas.
- **Contrôle** : `tests/test_parcours.py::ParcoursVisiteur::test_p8d_devis_api_sans_smtp_se_declare_indisponible`
- **Date** : 2026-09-21

### L-016 — une règle écrite ne retient pas un agent, un contrôle oui
- **Symptôme** : `npm ci`, `npm run build` et deux `npm install` lancés par Claude dans le dossier OneDrive le 21/09, malgré « ne jamais lancer `npm install` dans ce dossier » dans `CLAUDE.md`. Des dizaines de milliers de fichiers en file de synchronisation ; une simple lecture du dossier a dépassé 120 s.
- **Cause** : la séance avait été ouverte depuis le dossier utilisateur, et le `CLAUDE.md` du projet n'était pas encore chargé quand les commandes sont parties. La règle vivait dans un texte lu parfois, pas dans le dépôt lu toujours. Corrigé par le déplacement du dépôt (ADR-0005) et par un contrôle qui refuse tout chemin OneDrive.
- **Contrôle** : `tests/test_emplacement.py::EmplacementDuDepot::test_e1_le_depot_n_est_pas_sous_onedrive`
- **Date** : 2026-09-21

### L-017 — un garde-fou à liste noire ne sait pas porter une décision
- **Symptôme** : `test_no_business_infrastructure_was_added` interdisait `app/api` en bloc. La route de devis décidée en H4 l'a mis rouge, et rien dans le contrôle ne permettait de distinguer une route décidée d'une route sauvage.
- **Cause** : la liste noire encodait « pas de backend » comme un fait, alors que c'était une décision révisable. Réécrit : une route sous `app/api` est admise si un ADR la porte (`ALLOWED_API`), tout le reste et toute base de données restent interdits. Le contrôle est resté rouge jusqu'à l'existence de l'ADR-0006, ce qui est l'ordre voulu.
- **Contrôle** : `tests/test_project_os.py::ProjectOsTests::test_no_business_infrastructure_was_added`
- **Date** : 2026-09-21

### L-018 — `scrollWidth` ne voit pas un chevauchement masqué par `overflow-hidden`
- **Symptôme** : balayage Chromium de 30 gabarits × 11 largeurs (320 → 1280 px) : zéro débordement horizontal. Pourtant, à 320 px, la comparaison de l'accueil superposait « épaisseurs », « d'expertise », « Certification » et « Vendeur généraliste » sur les colonnes voisines. Vu seulement sur capture d'élément.
- **Cause** : `grid-cols-3` et `p-5` sans préfixe s'appliquaient à 320 px (≈ 53 px utiles par cellule, moins encore avec l'icône), et l'enveloppe `overflow-hidden rounded-2xl` avalait le dépassement : la page ne défilait pas, le texte était illisible. Un contrôle de débordement global prouve l'absence de défilement, pas la lisibilité. Corrigé par un gabarit mobile explicite (`grid-cols-[0.95fr_1.25fr_1fr]`, `p-3`, icône au-dessus du texte) que `sm:` remplace par l'existant, plus `break-words hyphens-auto`.
- **Contrôle** : `tests/test_responsive.py::ComparaisonMobile::test_r1_colonnes_et_remplissage_prefixes`
- **Date** : 2026-09-21

### L-019 — une cible tactile trop petite n'est pas un défaut « mobile »
- **Symptôme** : 37 à 46 liens sous 24 px de haut par page (218 occurrences de liens du pied de page à 14 px, fil d'Ariane à 13 px, plan du site : 152 cibles), comptés identiques à 320, 768 et 1280 px.
- **Cause** : les liens texte n'ont que la hauteur de leur ligne. Aucune règle de mise en page n'était en cause, donc aucun point de rupture ne pouvait le corriger : c'est une propriété des composants partagés, `Footer.tsx`, `FilAriane.tsx`, `plan-du-site`. Corrigé par une classe unique `.lien-tactile` (`inline-flex`, `min-height: 24px`) qui ne change ni la police ni la couleur ; grossir les textes aurait modifié le design.
- **Contrôle** : `tests/test_responsive.py::CiblesTactiles::test_r2bis_liens_texte_portent_la_classe`
- **Date** : 2026-09-21

### L-020 — un lien écrit à la main pointe là où personne ne regarde
- **Symptôme** : la carte « Transformation sur plan » de `/services` menait à `/services/transformation`, qui n'existe pas (404). Vu par le journal réseau du balayage (préchargement Next en 404), pas par un humain : la carte s'affiche parfaitement.
- **Cause** : le slug avait été inventé dans la page alors que `lib/edito.ts:1090` associe déjà ce libellé à `/services/soudure`. Les 32 hrefs littéraux du code n'étaient confrontés à aucune liste de pages réelles. Corrigé en reprenant la cible de `lib/edito.ts` ; le contrôle confronte désormais chaque href littéral aux pages statiques, aux chemins du catalogue et aux slugs connus.
- **Contrôle** : `tests/test_responsive.py::LiensInternes::test_r3_chaque_href_litteral_existe`
- **Date** : 2026-09-21

### L-021 — un bouton qui echoue en annoncant la mauvaise cause envoie chercher au mauvais endroit
- **Symptôme** : `git push origin main` refuse par GitHub le 21/09 — « Changes must be made through a pull request », « Required status check "quality" is expected ». Le bouton SAUVEGARDER, lui, affichait dans ce cas « ENVOI IMPOSSIBLE : connexion GitHub a faire une fois (double-clic sur SAUVEGARDER.cmd) » : un message qui renvoie vers une authentification qui, elle, fonctionnait parfaitement, et vers le bouton qui venait d'echouer.
- **Cause** : le script traitait tout `$LASTEXITCODE` non nul comme un probleme d'authentification, seule cause connue a l'ecriture. Une protection de branche activee plus tard produit le meme code de sortie et un message faux. Un diagnostic code en dur vieillit mal ; il vaut mieux decrire ce qu'on ignore (« verifier la connexion internet, puis la connexion GitHub ») que nommer une cause qu'on n'a pas verifiee. Corrige en meme temps que le flux : le mode sauvegarder pousse une branche de travail, affiche et ouvre le lien de la pull request.
- **Contrôle** : `tests/test_gate.py::GateTests::test_le_bouton_de_sauvegarde_passe_par_une_branche`
- **Date** : 2026-09-21

### L-022 — PowerShell ignore la casse : un parametre et une variable locale de meme nom sont la meme variable
- **Symptôme** : `synchro.ps1 -Mode sauvegarder` annonçait « Le travail part sur une branche », puis poussait `main` — refusé par GitHub. Le script tournait sans erreur et faisait le contraire de ce qu'il affichait. Deux hypothèses ont été testées et écartées avant de trouver (redirection `2>$null` cassant `$LASTEXITCODE` : fausse, vérifiée ; expression parenthésée en argument natif : fausse, vérifiée).
- **Cause** : le paramètre `[string]$Branche` et la variable `$branche = (git rev-parse --abbrev-ref HEAD)` sont **une seule variable**, PowerShell ne distinguant pas la casse. La branche courante écrasait silencieusement le paramètre, donc `$brancheTravail` valait `main` et la branche de travail n'était jamais calculée. Ni l'analyseur de syntaxe ni l'exécution ne signalent cette collision : elle ne se voit qu'en lisant le même nom deux fois à deux casses. Trouvée en journalisant le refspec réellement envoyé — la mesure, pas la troisième hypothèse.
- **Contrôle** : `tests/test_gate.py::GateTests::test_aucun_parametre_powershell_n_est_ecrase_par_une_variable_locale`
- **Date** : 2026-09-21

### L-023 — un « mur de texte » à l'écran est d'abord un défaut de données, pas de CSS
- **Symptôme** : sur les 495 fiches produit, la description s'affichait en paragraphes commençant par « • », sans titre ni liste, sous un intertitre « Description » qui laissait 36 % de la largeur vide à 1280 px. Le gabarit savait pourtant rendre des titres et des listes.
- **Cause** : `lib/descriptions-site-actuel.json` contenait 4 776 blocs, tous de type `p`. Le générateur (`scripts/inventaire/integrer.py`) ne faisait une liste que si un MÊME paragraphe contenait deux « • », et un titre que si le `<p>` ne contenait qu'un `<strong>` ; le site source met chaque puce dans son propre `<p>` et ses intertitres en `<p>` nu. Aucune des deux heuristiques ne rencontrait jamais le balisage réel. Corrigé dans le générateur (puces par paragraphe fusionnées en listes, intertitres reconnus par lexique et forme, garde contre les lignes « Libellé Valeur » d'un tableau aplati), JSON régénéré hors ligne depuis le cache : 494 titres, 721 listes, zéro puce littérale. Retoucher le CSS aurait décoré le symptôme.
- **Contrôle** : `tests/test_produit.py::DonneesDeDescription::test_d1_aucun_paragraphe_a_puce`
- **Date** : 2026-09-22

### L-024 — un chiffre à 48 px dans une colonne de 140 px se casse, et la grille ne le dit pas
- **Symptôme** : capture d'accueil à 320 px du 22/09 : « 40 ans » sur deux lignes, « 4 » seul sur la sienne, dans une grille restée à deux colonnes ; aucun débordement mesuré, donc invisible au balayage.
- **Cause** : `Counters.tsx` portait `text-5xl md:text-6xl` — la taille desktop moins un cran s'appliquait dès 320 px, soit 48 px pour deux compteurs dans 280 px utiles. La taille mobile n'était pas écrite, elle était héritée. Corrigé par `text-4xl sm:text-5xl md:text-6xl` et `tabular-nums`.
- **Contrôle** : `tests/test_responsive.py::CompteursMobiles::test_r4_taille_mobile_explicite`
- **Date** : 2026-09-22

### L-025 — un enfant de grille ne rétrécit jamais sous son mot le plus long
- **Symptôme** : balayage d'une fiche par catégorie (54 × 320 px) : deux débordements. « Tôle striée de 2000x1000x2,5/4mm en aluminium » sortait de 14 px, une section « Domaines d'applications » de 78 px. Les 52 autres catégories passaient, ce qui donnait l'illusion d'un défaut de contenu.
- **Cause** : un enfant de `grid` vaut `min-width: auto`, donc sa largeur minimale est celle de son contenu le plus large — et un nom de produit est plein de cotes insécables (`2000x1000x2,5/4mm`). Ni la largeur du conteneur ni le `container-g` ne peuvent le contraindre. Corrigé par `min-w-0` (lève la contrainte) et `break-words` (coupe le mot) sur le bloc d'identité et sur les modules. La règle vaut pour toute grille du site, pas pour ces deux fiches.
- **Contrôle** : `tests/test_produit.py::GrillesQuiRetrecissent::test_d8_les_blocs_de_grille_peuvent_retrecir`
- **Date** : 2026-09-22

### L-026 — « poussé » ne prouve pas « en ligne »
- **Symptôme** : les captures du propriétaire du 22/09 montraient des défauts déjà corrigés la veille. Le site déployé était à `54d93a2` (17/09) : cinq jours de travail local jamais mis en ligne, parce que `main` est protégée et qu'aucune pull request n'avait été fusionnée.
- **Cause** : la fin de session exigeait un commit, pas une publication. La chaîne réelle (commit → branche → PR → check vert → **fusion humaine** → Vercel) n'était écrite nulle part, donc personne ne voyait qu'elle s'arrêtait à l'étape 3. Corrigé par une règle explicite dans `CLAUDE.md` et par un `synchro.ps1` qui donne le lien de la PR **et** celui du déploiement de branche, en disant que seule la fusion change la production.
- **Contrôle** : `tests/test_gate.py::GateTests::test_la_regle_de_publication_continue_est_ecrite`
- **Date** : 2026-09-22

### L-027 — une revue humaine qui n'a jamais lieu ne protège rien
- **Symptôme** : cinq jours de travail invisibles pour le propriétaire. La production Vercel était restée à `54d93a2` (17/09) alors que quatorze commits attendaient sur une branche ; ses captures du 22/09 montraient des défauts corrigés la veille, et il croyait voir mon travail.
- **Cause** : `main` protégée + aucune pull request jamais ouverte. La règle « aucun agent ne fusionne » supposait qu'un humain fusionnerait ; personne ne l'a fait, et rien ne signalait que la chaîne s'arrêtait à l'étape 3. Un garde-fou qui dépend d'un geste que personne ne fait n'est pas un garde-fou, c'est un blocage silencieux. Remplacé (ADR-0009) par un garde-fou qui s'exécute vraiment : la fusion est automatique, mais refusée si le check `quality` n'est pas vert. Risque tenable parce que cette production est la préproduction, protégée et non indexée.
- **Contrôle** : `tests/test_gate.py::GateTests::test_la_chaine_de_publication_va_jusqu_a_vercel`
- **Date** : 2026-09-22

### L-028 — sous `ErrorActionPreference = 'Stop'`, un avertissement sur stderr tue le script
- **Symptôme** : `publier.ps1` venait d'être commité sans avoir jamais tourné en entier. Relecture : il déclarait `$ErrorActionPreference = 'Stop'` en tête et lisait ses identifiants par `… | git credential fill 2>$null`. Mesuré le 22/09 avec une commande native inoffensive qui écrit sur stderr et sort en code 0 : sous cette combinaison le script **meurt**, sans elle il passe. Le bouton de publication serait mort sans message utile, au premier avertissement de Git.
- **Cause** : PowerShell 5.1 emballe chaque ligne de stderr d'un exécutable dans une `ErrorRecord` dès que la redirection est explicite ; sous `Stop`, cette ErrorRecord devient terminante, même si l'exécutable a réussi. Les deux moitiés sont raisonnables séparément — `Stop` pour ne pas continuer sur une erreur, `2>$null` pour ne pas polluer la sortie — et fatales ensemble. Corrigé en baissant la préférence autour de l'appel (`try`/`finally`), pas en supprimant la redirection au hasard.
- **Contrôle** : `tests/test_gate.py::GateTests::test_aucun_script_ne_rend_stderr_fatal`
- **Date** : 2026-09-22

### L-029 — un composant recopié perd ce qui ne se voit pas
- **Symptôme** : quatre gabarits — `PageHeader` (22 pages), `PageLegale`, la fiche d'un dépôt, celle d'un service — dessinaient leur fil d'Ariane à la main. Rendu identique à `FilAriane` au pixel près, donc invisible à l'œil et au balayage responsive ; mais aucun `BreadcrumbList` schema.org. Google ne voyait la hiérarchie que sur les cinq pages qui utilisaient vraiment le composant.
- **Cause** : le fil d'Ariane est cinq lignes de JSX faciles à recopier, et sa partie coûteuse — le JSON-LD — est invisible. Ce qu'on recopie d'un composant, c'est ce qu'on voit ; ce qu'on perd, c'est le reste. Corrigé en passant les quatre gabarits sur `FilAriane`, qui accepte désormais des miettes optionnelles. Contrôle générique : aucun `<Link href="/">Accueil</Link>` hors du composant, et jamais deux fils sur une même page.
- **Contrôle** : `tests/test_responsive.py::FilsDAriane::test_r5_aucun_fil_d_ariane_code_a_la_main`
- **Date** : 2026-09-22

### L-030 — une règle de correspondance trop stricte fabrique du travail qui n'existe pas
- **Symptôme** : le premier audit des visuels classait **213 produits sur 466** en `AMBIGUOUS`, au motif que le titre inscrit dans le rendu Blender diffère du nom du catalogue. Lu tel quel, le rapport annonçait la moitié du catalogue à revérifier à la main.
- **Cause** : la règle exigeait l'égalité stricte des deux libellés. Or le rendu raccourcit volontairement — « Rond à béton de 10mm de diamètre » pour « Rond à béton de 10mm de diamètre en acier laminé à chaud » — parce que la matière figure déjà dans le surtitre de l'image. 201 des 213 écarts étaient de simples préfixes. La bonne règle tient à une propriété du domaine : le titre d'un rendu n'**ajoute** jamais d'information, il en retire ; ses mots doivent donc se retrouver dans le nom du produit, dans l'ordre, et ses cotes doivent toutes exister. Résultat après correction : zéro ambigu réel. Vérifier un échantillon avant de publier un compteur aurait coûté deux minutes.
- **Contrôle** : `tests/test_produit.py::CorrespondanceRenduProduit::test_d10_un_raccourci_designe_bien_le_produit`
- **Date** : 2026-09-22

### L-031 — un générateur qui écrase sans condition laisse le hasard décider
- **Symptôme** : intégrer les 10 caillebotis a silencieusement remplacé la photo studio de toute la catégorie « Caillebotis & marches » — `studio-plancher-o2` est devenu `studio-caillebotis`. Aucun message, aucune trace : découvert en comparant le manifeste avant/après.
- **Cause** : `integrer_visuels.py` faisait `manifeste["categories"][categorie] = image` sans condition. Trois catégories ont plusieurs familles de photo studio (celle-ci en a quatre) et le manifeste n'en tient qu'une : la dernière famille intégrée gagnait, par ordre d'exécution. Choisir entre quatre studios valides est une décision visuelle humaine, pas une conséquence de l'ordre des arguments. Le générateur conserve désormais l'existant et signale le candidat ignoré ; remplacer exige `--remplacer-studio`.
- **Contrôle** : `tests/test_produit.py::StudioDeCategorie::test_d9_le_studio_existant_n_est_pas_ecrase`
- **Date** : 2026-09-22

### L-032 — une donnée produite mais jamais servie ne se voit dans aucun contrôle
- **Symptôme** : « Dans le bardage je ne vois rien » (propriétaire, 22/09). La page `/toiture-bardage` affichait ses trois familles — Bardage, Panneaux isolés, Tôles profilées — avec **exactement le même dessin SVG** : `lib/visuels.ts` renvoyait tout ce qui est sous `toiture-bardage` vers l'illustration « tôles ». Aucun contrôle n'échouait : la page répondait 200, ne débordait pas, n'avait pas d'erreur console. Les trois photos studio existaient depuis des jours, servies une couche plus bas.
- **Cause** : le repli SVG était conçu pour l'absence de photo, et personne n'avait vérifié qu'il ne masquait pas une photo présente. Un audit qui compte les images *servies* ne voit pas celles qui *devraient* l'être ailleurs. Corrigé par la règle du candidat unique (`studioUniqueDe`) : une famille sous laquelle il n'existe qu'une photo studio la montre ; zéro ou plusieurs, le dessin reste, parce que choisir entre deux photos est un arbitrage visuel. Effet mesuré au-delà du bardage : 7 familles et plusieurs sous-catégories (`/acier/toles` en gagne 7 distinctes).
- **Contrôle** : `tests/test_produit.py::VisuelDeFamille::test_d11_la_regle_du_candidat_unique`
- **Date** : 2026-09-22

### L-033 — un chemin d'entrée hors du dépôt n'est pas une source, c'est une pièce qui manquera
- **Symptôme** : `lib/catalogue.ts` — 495 produits, cœur du site — porte l'en-tête « généré par `scripts/generer-catalogue.py` », et `CLAUDE.md` interdit de le modifier à la main. Or le générateur attendait son CSV à `/root/.claude/uploads/60ae7e8a-…/`, un chemin de session web Linux. Résultat découvert le 22/09 : le catalogue est **gelé** — impossible d'ajouter un produit vu sur le site officiel, impossible de corriger un nom, et la règle du projet interdit de contourner.
- **Cause** : le générateur a été écrit dans une session web où le fichier téléversé vivait à ce chemin, et le chemin est resté en dur au rapatriement sur le PC. Rien ne l'a signalé pendant huit jours : un générateur qu'on ne relance pas ne dit jamais qu'il est cassé. Corrigé en déplaçant l'entrée par défaut dans le dépôt et en faisant expliquer au script ce qui manque, avec les colonnes attendues et les trois voies de récupération — au lieu d'une trace de lecture sur un chemin Linux.
- **Contrôle** : `tests/test_produit.py::CatalogueRegenerable::test_d12_l_entree_du_generateur_est_dans_le_depot`
- **Date** : 2026-09-22
- **Suite (22/09, même nuit)** : le fichier a été retrouvé dans `Downloads/` et déposé dans le dépôt — le blocage est levé. Deux enseignements de plus. D'abord, un fichier « perdu » mérite une recherche disque avant d'être déclaré perdu : trois minutes de `find` contre huit jours de catalogue gelé. Ensuite, régénérer a produit un diff alarmant (quatre prix passant à 5,00 €) qui s'est révélé sans effet : `catalogue.ts` fusionne `site-actuel.json` au chargement et écrase `prix`. Avant de crier à la corruption, il faut vérifier ce que la page **sert** — elle servait le bon prix.

### L-034 — un en-tête « GÉNÉRÉ » dont le générateur n'existe pas est pire qu'aucun en-tête
- **Symptôme** : 15 des 622 destinations de `lib/redirections.mjs` ne menaient nulle part. 22 anciennes URLs — dont `/checkout`, `/wishlist`, `/panneau-tuile`, `/poutrelle-hem` — répondaient 301 puis 404 : le visiteur et le lien entrant perdus deux fois, avec la lenteur d'un saut inutile en prime.
- **Cause** : deux causes qui se protégeaient l'une l'autre. Le relevé d'URLs (`URL_cible_recommandee`) proposait des pages **à créer** — l'action portée en face disait « page de contenu à réalimenter ou fusionner » — et ces cibles ont été recopiées telles quelles ; personne n'a jamais construit `/acier/poutrelles/hem` ni `/commande`. Et le fichier portait l'en-tête « GÉNÉRÉ, NE PAS ÉDITER À LA MAIN — Générateur : `scripts/generer-redirections.py` », alors que ce générateur était un commentaire de trois lignes. L'étiquette décourageait la modification à la main **et** mentait sur l'existence d'un contrôle automatique : le fichier n'était ni tenu à la main, ni généré. Le générateur existe maintenant, valide chaque cible contre les routes réellement servies, et répare — table explicite pour les pages renommées, repli sur l'ancêtre servi pour les catégories jamais construites. Une régénération qui ne trouve pas de réparation s'arrête au lieu d'écrire une 404.
- **Contrôle** : `tests/test_redirections.py::Redirections::test_rd1_chaque_destination_existe`
- **Date** : 2026-09-22

### L-035 — un composant partagé par deux tailles ne peut pas avoir de `sizes` par défaut
- **Symptôme** : la page `/acier/toles` téléchargeait **328 Ko** de photos pour afficher sept vignettes de 80 px de côté — dont 187 Ko pour la seule tôle perforée. Toutes les photos studio font 1600 × 1200 : 400 fois la surface affichée. Mesuré sur le site construit, avant/après : 328 Ko → 15 Ko sur écran retina, 5 Ko sur écran standard.
- **Cause** : `VisuelFamille` a été créé la veille (leçon L-029) pour que les deux gabarits de catalogue partagent la même règle de choix d'image. Mutualiser le choix était juste ; mutualiser **la taille d'affichage** ne l'était pas. Le composant portait un `sizes` de carte pleine colonne et un `unoptimized` qui annulait de toute façon tout redimensionnement, alors qu'un des deux appelants l'affiche dans un carré de 80 px. Le défaut est invisible à la lecture de chaque fichier pris séparément : il naît de l'écart entre les deux appelants. `sizes` est devenu une prop **obligatoire sans valeur par défaut** — un défaut aurait été juste pour l'un et faux pour l'autre, sans que rien ne le signale. Règle générale : ce qu'un composant partagé ne peut pas connaître, il ne le devine pas, il l'exige.
- **Contrôle** : `tests/test_parcours.py::ParcoursVisiteur::test_p10_vignettes_categorie_passent_par_optimiseur`
- **Date** : 2026-09-22

### L-036 — une route qui envoie du courrier sans plafond prête l'adresse de l'entreprise
- **Symptôme** : `/api/devis` acceptait autant de demandes qu'on lui en envoyait. Une boucle de vingt lignes depuis n'importe quel poste remplissait la boîte commerciale et faisait relayer des milliers de messages par le compte Microsoft 365 de l'entreprise — jusqu'à ce que Microsoft bride ou bloque le compte, ce qui aurait coupé aussi les envois légitimes.
- **Cause** : la route a été écrite en pensant au contenu (validation, longueurs, injection d'en-tête SMTP, champ piège) et pas au volume. Le champ piège arrête un robot qui remplit tout ; il n'arrête pas une boucle qui poste un corps correct. Deux plafonds désormais, parce qu'ils protègent deux choses distinctes : 5 envois par adresse et par 10 minutes pour la boîte aux lettres, comptés seulement quand la demande va réellement partir ; 30 requêtes pour le quota d'exécutions, comptées dès l'entrée. Limite assumée et écrite dans le code : le compteur vit dans la mémoire de l'instance, donc il arrête le flot naïf, pas une attaque répartie. Un plafond partagé demanderait un stockage externe — la marche suivante, pas celle-ci.
- **Contrôle** : `tests/test_parcours.py::ParcoursVisiteur::test_p12_devis_api_refuse_un_flot`
- **Date** : 2026-09-22

### L-037 — une page juridique décrit un comportement : elle se périme quand le code change
- **Symptôme** : la page Protection des données affirmait « Les formulaires de devis et de contact n'enregistrent rien : ils composent un message dans votre propre logiciel de messagerie [...] Tant que vous n'avez pas cliqué sur « envoyer », aucune donnée ne nous parvient. » C'était exact jusqu'à l'ajout de `app/api/devis/route.ts` la veille — par moi. Depuis, le formulaire de devis poste au serveur, qui relaie par SMTP. La page est restée telle quelle : une information fausse sur un traitement de données personnelles, affichée à qui la lit précisément pour savoir ce qui lui arrive.
- **Cause** : le texte juridique était traité comme du contenu éditorial — écrit une fois, relu par personne — alors qu'il **décrit le code**. Rien ne le reliait au code : ajouter une route ne faisait rien échouer. Deux contrôles le relient maintenant. Enseignement de méthode, appris en écrivant le second : formulé d'abord comme « la promesse doit être qualifiée », il serait resté **vert** sur le texte fautif, qui la qualifiait — mais avec une réserve devenue fausse. Un contrôle doit viser l'invariant, pas la tournure ; et la seule façon de le savoir est de le faire tourner sur le texte d'avant. C'est ce qui a été fait ici, et c'est ce qui a montré que la première version ne servait à rien.
- **Contrôle** : `tests/test_rgpd.py::ProtectionDesDonnees::test_rg1_le_relais_serveur_est_annonce`
- **Date** : 2026-09-22
- **Suite (22/09, contre-audit)** : le même défaut existait en sens inverse. La page Cookies annonçait « Certaines préférences d'affichage peuvent être conservées dans le stockage local de votre navigateur — un filtre sélectionné, un onglet ouvert », alors qu'aucun `localStorage`, `sessionStorage` ni `document.cookie` n'existe dans le code. Sur-déclarer est moins grave que sous-déclarer, mais une page qui promet « voici ce qu'il utilise réellement » doit dire vrai dans les deux sens. Contrôle `tests/test_rgpd.py::ProtectionDesDonnees::test_rg3_aucun_stockage_navigateur_annonce_a_tort`. Vérifié au passage et exact : les polices sont bien servies depuis le domaine du site (`next/font/google` les intègre au build).

### L-038 — un contrôle qui lit une liste fixe de fichiers ne voit jamais le nouveau
- **Symptôme** : au balayage du 22/09, le lien « protection des données » du formulaire de devis mesurait 126 × 13 px — un lien légal, dans le formulaire qui rapporte, sous le seuil tactile de 24 px. R2bis, écrit la veille précisément pour cela (« un lien texte doit porter `lien-tactile` »), était vert.
- **Cause** : R2bis parcourait `FICHIERS_LIENS_TEXTE`, une liste fermée de dix composants établie d'après les défauts du 21/09. `DevisForm.tsx` n'y était pas, `PageEspace.tsx` non plus — dont le lien e-mail avait le même défaut, trouvé en étendant la liste. Un contrôle ne vaut que pour le périmètre qu'on lui donne, et une liste fermée périme à la première page ajoutée. Les trois composants de formulaire et d'espace y sont désormais ; la vraie réponse serait un parcours de tous les `.tsx`, ce qui demande d'abord d'inventorier les exceptions légitimes (boutons, cartes) — à faire quand un troisième oubli se présentera. Mesuré après correction, à 320 px : 126 × 24 et 146 × 24.
- **Contrôle** : `tests/test_responsive.py::CiblesTactiles::test_r2bis_liens_texte_portent_la_classe`
- **Date** : 2026-09-22

### L-039 — un outil de mesure qui crie à tort finit ignoré
- **Symptôme** : chaque fiche produit remontait deux « cibles tactiles » de 1 × 1 px au balayage — donc 990 alertes fausses sur les 495 fiches, au milieu des vraies.
- **Cause** : ce sont les boutons radio `sr-only` de la galerie (présents pour le lecteur d'écran, rognés à 1 px pour l'œil). Leur cible visible est l'étiquette, mesurée à 85 × 65 px en mobile et 184 × 139 en desktop. Le filtre `visible()` du balayage testait `display`, `visibility` et `opacity`, pas `clip` : la signature de `sr-only` est `clip: rect(0px, 0px, 0px, 0px)`. Un outil de QA a les mêmes obligations qu'un contrôle : une alerte fausse coûte plus qu'aucune alerte, parce qu'elle apprend à ne plus lire.
- **Contrôle** : `tests/test_responsive.py::BalayageFiable::test_r6_le_balayage_exclut_les_elements_sr_only`
- **Date** : 2026-09-22

### L-040 — corriger la mise en forme d'une entrée ne dit rien de son acheminement
- **Symptôme** : le bouton « Sauvegarder » a poussé la branche, annoncé la pull request… et s'est arrêté sur `fatal: refusing to work with credential missing protocol field`. Aucune pull request créée, aucune fusion, rien sur Vercel. Le propriétaire a demandé « c'est publié ? » — la réponse était non, après un message qui ressemblait à un succès.
- **Cause** : `Jeton()` alimentait `git credential fill` par un tuyau PowerShell. Mesuré ce jour sur ce poste : git ne reçoit **rien** et lit EOF, donc zéro champ, donc l'erreur sur le champ `protocol`. La même entrée redirigée depuis un fichier (`cmd /c "git credential fill < f"`) renvoie les quatre lignes attendues, jeton compris. Le piège : ce message d'erreur avait **déjà** été rencontré la veille et corrigé en passant d'une chaîne unique à un tableau de lignes. Cette correction était juste — elle réglait la *mise en forme* de l'entrée — et elle masquait le vrai problème, l'*acheminement*. Un message d'erreur identique ne signifie pas une cause identique : la première correction avait rendu la seconde invisible en supprimant le seul symptôme qui les distinguait.
- **Contrôle** : `tests/test_gate.py::GateTests::test_aucun_script_n_alimente_une_commande_native_par_un_tuyau`
- **Date** : 2026-09-22

### L-041 — un compteur dit ce qu'on a compté, pas ce que son libellé annonce
- **Symptôme** : `PRODUCTS-AJOUT-MODELISATION.md` annonçait « Rendus Blender dans `final/` : 466 » et « Rendus dans `essais/` : 64 ». Le dossier `final/` contient **1 697** fichiers et `essais/` **648**. Aucun des deux chiffres n'était faux — ils comptaient les seuls WebP de fiche produit — mais leur libellé disait « dans le dossier », ce que le dossier contredit d'un facteur quatre.
- **Cause** : le compteur a été écrit par quelqu'un qui savait ce qu'il comptait, et lu ensuite par quelqu'un qui ne le savait plus. Un document de suivi est relu des semaines après, hors du contexte qui l'a produit : le libellé est la seule chose qui survit. Le tableau porte désormais une colonne « Compté comment » qui nomme la source de chaque ligne, et les lignes d'atelier — hors dépôt, donc incontrôlables — sont séparées de celles qui se vérifient dans le dépôt. Trouvaille au passage, obtenue seulement parce qu'il a fallu tout recompter : les 64 rendus d'`essais/` visent **tous** un produit déjà pourvu, donc l'interdiction d'y puiser ne coûte rien.
- **Contrôle** : `tests/test_produit.py::CompteursDuDocument::test_d13_les_compteurs_verifiables_disent_la_verite`
- **Date** : 2026-09-22

### L-042 — un `<fieldset>` ne rétrécit pas comme un `<div>`
- **Symptôme** : à 320 px, la fiche produit débordait de 39 px à l'horizontale — sur cinq largeurs mobiles, seize mesures rouges. Le coupable désigné par le balayage était la barre d'onglets ; la vraie cause était son parent.
- **Cause** : le navigateur applique `min-inline-size: min-content` à tout `<fieldset>`. Contrairement à un `div`, il **refuse** de descendre sous la largeur de son contenu : le fieldset faisait 319 px dans un conteneur de 280, et l'`overflow-x: auto` posé à l'intérieur n'y pouvait rien puisque le débordement se produisait un niveau au-dessus. `overflow-x: hidden` aurait masqué le symptôme en coupant le contenu ; `min-w-0` retire la contrainte. Le contrôle a trouvé un second fautif que je ne cherchais pas : le `<fieldset>` du formulaire de devis, en place depuis des jours.
- **Contrôle** : `tests/test_responsive.py::FieldsetsRetrecissables::test_r7_tout_fieldset_porte_min_w_0`
- **Date** : 2026-09-22

### L-043 — un contrôle qu'on n'a pas vu rouge n'est pas un contrôle
- **Symptôme** : R7 est passé **vert** du premier coup, alors que deux `<fieldset>` sans `min-w-0` existaient dans le dépôt. Un débogage à côté du test les trouvait tous les deux.
- **Cause** : le motif écrit était `<fieldset\b[^>]*>`, mais la chaîne a traversé un outil qui réduit les doubles contre-obliques : le `\b` est devenu un **caractère backspace** (0x08) au lieu d'une limite de mot. Le motif ne pouvait plus correspondre à rien, et un contrôle qui ne correspond à rien réussit toujours. `cat -A` l'a révélé en une seconde, là où relire le fichier à l'œil ne montrait rien. Deux règles en sortent : écrire les motifs sans contre-oblique quand c'est possible (`[ >]` au lieu de `\b`), et surtout **ne jamais croire un contrôle neuf qui passe** — la discipline « rouge avant vert » n'est pas une formalité, c'est le seul moment où l'on vérifie que le contrôle sait échouer.
- **Contrôle** : `tests/test_responsive.py::FieldsetsRetrecissables::test_r7_tout_fieldset_porte_min_w_0`
- **Date** : 2026-09-22

### L-044 — rendre un lien plus facile à atteindre le rend plus facile à toucher par erreur
- **Symptôme** : sur `/devis` à 390 px, on remplit le formulaire, on touche le lien « protection des données » placé sous le bouton d'envoi, on revient en arrière — **nom, e-mail et détails sont vides**. Mesuré au navigateur, pas déduit.
- **Cause** : le lien est à l'intérieur du `<form>`, le formulaire n'a que des états React locaux, et le site n'écrit rien dans le navigateur. Le défaut préexistait, mais je l'ai **aggravé le matin même** : en donnant à ce lien la classe `lien-tactile` pour qu'il atteigne 24 px de haut (leçon L-038), je l'ai rendu plus facile à atteindre — donc plus facile à toucher par mégarde, sur la page qui rapporte les demandes de devis. Une correction d'accessibilité déplace le risque au lieu de le supprimer si l'on ne regarde pas ce qu'il y a autour. La parade n'est pas de stocker la saisie : ce serait rendre fausse la page Cookies corrigée le matin même (L-037). C'est de ne jamais quitter la page — `target="_blank"`.
- **Contrôle** : `tests/test_mobile.py::LiensDansUnFormulaire::test_m5_les_liens_dans_un_formulaire_ouvrent_un_nouvel_onglet`
- **Date** : 2026-09-22

### L-045 — une règle qu'on ne peut pas satisfaire n'est pas une règle, c'est une impasse
- **Symptôme** : supprimer un fichier suivi devenait impossible. Le contrôle B3 refusait la suppression ; la seule façon d'effacer la ligne de `git status` est de commiter ; et le hook de pré-commit refuse de commiter tant qu'un contrôle est rouge. Boucle fermée, sans issue autre que restaurer un fichier dont on ne voulait plus.
- **Cause** : `git status --short` tient deux colonnes, l'index puis le working tree. `D ` est une suppression **indexée** — un `git rm`, donc une décision. ` D` est une disparition que personne n'a demandée. Le contrôle appliquait `.strip()` avant de tester, ce qui écrasait la distinction et traitait les deux comme la même faute. Son intention — « une suppression se décide, elle ne se constate pas » — était juste ; sa mise en œuvre interdisait précisément ce qu'elle voulait autoriser. Un contrôle doit toujours laisser ouverte la voie qui le satisfait, sinon il ne protège pas : il bloque.
- **Contrôle** : `tests/test_extensions.py::ExtensionTests::test_no_tracked_file_is_deleted_in_the_working_tree`
- **Date** : 2026-09-22

### L-046 — une règle écrite que rien ne vérifie est un vœu
- **Symptôme** : une fiche produit pesait **2 241 Ko sur bureau et 1 345 Ko sur mobile**, dont **52 Ko d'images seulement**. Le plus gros fichier, **485 Ko**, était le paquet JavaScript de `/recherche` — téléchargé sur **chaque** page, parce que l'en-tête renvoie vers la recherche et que Next précharge les liens visibles.
- **Cause** : `components/catalogue/Recherche.tsx` était `"use client"` et importait `tousProduits` de `lib/catalogue.ts`. Les 495 produits, avec leurs prix, leurs spécifications et leurs poids, partaient chez chaque visiteur pour une recherche qu'il n'ouvrirait peut-être jamais. `CLAUDE.md` l'interdit **depuis le début**, ligne 19, avec la raison exacte — « tout le catalogue partirait dans le JavaScript du navigateur » — et même la parade : calculer dans la page serveur, passer en props. La règle était juste, écrite, et enfreinte, parce que **rien ne la vérifiait**. Une règle sans contrôle ne tient que par la mémoire de celui qui l'a écrite. Le contrôle a d'ailleurs trouvé un second coupable que personne ne cherchait, `FormulairePro.tsx`, qui embarquait l'éditorial pour afficher quatre dépôts. Mesuré après correction : **1 356 Ko sur bureau (−39 %) et 435 Ko sur mobile (−68 %)**, recherche vérifiée fonctionnelle (42 résultats pour « corniere 40x40 »).
- **Contrôle** : `tests/test_lint.py::DonneesCoteClient::test_c1_aucun_composant_client_n_importe_le_catalogue`
- **Date** : 2026-09-22

### L-047 — la mise en page suit le contenu, pas l'inverse
- **Symptôme** : le propriétaire, devant une cornière aluminium — « je ne trouve pas ça esthétique ». Il avait raison, et la cause n'était pas une affaire de goût. La valeur « Élément de base dans les petites charpentes et ossatures légères, assurant une répartition uniforme des charges » s'affichait sur quatre lignes **alignées à droite** : le bord gauche en escalier, l'œil qui perd le début de chaque ligne, et un libellé court perché en haut d'un bloc de quatre lignes avec un grand vide dessous.
- **Cause** : `GrillePaires` a été écrit pour des paires de fiche technique — « Épaisseur | 4 mm » — où l'alignement à droite met les chiffres en colonne et rend le tableau lisible. Puis on lui a donné les paires descriptives du site officiel sans se demander ce qu'elles contenaient. Mesure faite après coup, et décisive : sur les **1 727 paires** du catalogue, la valeur médiane fait **65 caractères** et **81 % sont des phrases**. Le gabarit était donc faux pour la grande majorité de ce qu'il recevait. Un composant ne doit pas imposer une forme à ses données : il doit lire ce qu'on lui donne et choisir. Les valeurs courtes gardent le tableau technique ; les phrases deviennent des définitions, terme au-dessus, texte à gauche. Même raisonnement pour « Longueurs standard » : une énumération tient en 40 caractères mais se brise au milieu d'une demi-colonne.
- **Contrôle** : `tests/test_parcours.py::ParcoursVisiteur::test_p15_aucune_phrase_n_est_alignee_a_droite`
- **Date** : 2026-09-22

### L-048 — ce qu'on peut retirer de la source ne se cache pas à l'affichage
- **Symptôme** : trois reproches successifs du propriétaire sur la même image. D'abord « on ne voit pas assez les mesures » — les cotes du rendu 3D étaient illisibles. Puis, après correction, « c'est beaucoup trop zoomé et ça prend trop de place ». Enfin « elles ressortent pas assez bien ».
- **Cause** : chaque rendu de fiche porte, sur ses 38 % droits, un tableau de spécifications incrusté qui répète la fiche technique affichée juste à côté. J'ai voulu le masquer **à l'affichage**, par `object-cover` sur une boîte 5/6. Cette solution est mauvaise sur trois plans à la fois, et c'est ce qui aurait dû m'alerter : elle force un agrandissement de 1,6× (d'où le zoom), elle rend la boîte verticale alors que l'objet est horizontal (d'où la place prise), et elle oblige `sizes` à mentir sur la largeur réellement affichée — l'image était servie en 384 px pour 763 requis, donc floue. Rogner à l'affichage ce qu'on peut rogner à la source est toujours un mauvais échange : on hérite des contraintes des deux côtés. Le tableau a donc été retiré du **fichier**, une fois, par un script qui repart toujours de l'original de l'atelier. L'image est ensuite montrée **entière** (`object-contain`) dans une boîte de rapport stable, sur fond neutre — la présentation d'une photo produit, et celle que suggérait le composant de référence fourni par le propriétaire. Mesuré : 466 rendus recadrés, 16,9 Mo → 10,8 Mo, et net aux densités 1× et 2×.
- **Leçon annexe** : `naturalWidth` lu trop tôt ment. Trois de mes diagnostics de flou étaient des artefacts de mesure, lus avant que la variante haute densité soit chargée. Une mesure au navigateur doit attendre, et se recouper avec `currentSrc`.
- **Contrôle** : `tests/test_parcours.py::ParcoursVisiteur::test_p10_vignettes_categorie_passent_par_optimiseur`
- **Date** : 2026-09-22

### L-049 — ce qu'un outil génère en s'exécutant n'est pas un fichier du dépôt
- **Symptôme** : deux contrôles rouges (« skill file sets diverge ») au premier lancement du registre de la séance du 23/09, alors qu'aucun fichier de skill n'avait été touché. Le registre partait de 160 verts la veille.
- **Cause** : lancer `python .claude/skills/ui-ux-pro-max/scripts/search.py` — exactement ce que `.claude/rules/external-capabilities.md` prescrit pour Claude — crée `scripts/__pycache__/*.pyc` dans la copie Claude seulement. Le comparateur des deux copies (`.claude/skills/` et `.agents/skills/`) listait *tous* les fichiers présents sur le disque, y compris ceux que Python génère à l'exécution et que Git ignore. La règle « les deux copies portent les mêmes octets » était juste ; sa mesure comptait des fichiers qui ne sont pas des fichiers du skill. Un contrôle qui devient rouge quand on suit une autre règle du dépôt oppose deux règles au lieu d'en garder une : la mesure doit exclure ce que l'outil produit de lui-même (`__pycache__`, `.pyc`), comme `.gitignore` le fait déjà.
- **Contrôle** : `tests/test_extensions.py::ExtensionTests::test_x1_les_fichiers_generes_par_python_ne_sont_pas_des_fichiers_de_skill`
- **Date** : 2026-09-23

### L-051 — une étape à relancer à la main après chaque intégration est une étape oubliée
- **Symptôme** : la vérification indépendante des carrés pleins (23/09) a trouvé que `integrer_visuels.py` servait l'image habillée **entière** (1600 × 1200 : fiche incrustée à droite et fondu de la barre en débord) et l'envoyait telle quelle dans la copie du propriétaire. Le site n'était propre que parce que `recadrer_visuels.py` avait été lancé une fois, le 22/09, à la main.
- **Cause** : le recadrage avait été ajouté comme un script à part, « une fois », au lieu d'être une étape de l'intégration. Toute famille réintégrée ensuite aurait réintroduit la fiche incrustée sur le site, sans qu'aucun contrôle ne le voie. Second piège, vu en corrigeant : le hook a refusé la ligne `import recadrer_visuels` pendant que l'appel `recadrer_visuels.CADRE` passait, et un contrôle qui cherchait seulement le mot restait vert sur un script qui aurait planté. Un contrôle de source vérifie la **structure** (l'import réel, l'appel dans la bonne fonction), pas la présence d'un mot.
- **Contrôle** : `tests/test_catalogue.py::CatalogueSource::test_k12_l_integration_recadre_ce_qu_elle_sert`
- **Date** : 2026-09-23

### L-050 — un serveur oublié réécrit le build suivant
- **Symptôme** : le 23/09, juste après un build vert et neuf contrôles K verts, `/catalogue`, `/catalogue/acier` et `/catalogue/quincaillerie` répondaient 404 sur un serveur fraîchement démarré, alors que `/catalogue/aluminium` répondait 200. Sur le disque, `.next/server/app/catalogue.html` faisait 47 Ko (la page 404) et son `.meta` disait `"status":404`, horodaté quatre minutes après le build.
- **Cause** : un `next start` lancé la veille à 17:12 par la séance précédente tournait encore sur le port 3000. Mon propre `next start -p 3000` a échoué en silence (`EADDRINUSE`) et mes mesures sont parties vers l'ancien processus. Celui-ci ne connaissait pas la route `/catalogue` : il a d'abord servi les fichiers prérendus trouvés dans le cache disque du build neuf (d'où un premier 200), puis les a **revalidés** avec sa propre table de routes, rendu sa 404, et l'a **écrite dans `.next/`** par-dessus les pages du build. Un serveur de production lit et écrit `.next/` ; deux processus sur le même dossier, dont un périmé, c'est le périmé qui a le dernier mot. La parade : avant de construire ou de mesurer, aucun `next start` de ce dépôt ne doit tourner (`netstat -ano | findstr :3000`, `Get-CimInstance Win32_Process`), et une mesure se fait sur un port libre choisi pour la séance — ce que `tests/test_parcours.py` fait déjà avec `port_libre()`. Le contrôle K2 est celui qui a révélé le défaut : rouge sur le build empoisonné, vert après reconstruction.
- **Contrôle** : `tests/test_catalogue.py::CatalogueRendu::test_k2_chaque_chapitre_repond`
- **Date** : 2026-09-23

### L-052 — un chanfrein en millimètres fixes n'a pas la même taille sur toutes les pièces
- **Symptôme** : le 23/09, le propriétaire relit le catalogue : « parfois il y a des arrondis alors qu'il n'y a pas d'arrondis ». Tous les profilés extrudés recevaient le même chanfrein de 0,6 mm : 10 % du côté d'un carré de 6, 20 % de l'épaisseur d'un plat de 3, et tout le chant d'une tôle de 1 mm. Sur la fiche d'un carré plein, la bande claire d'arête mesurait 20 à 25 px ; 4 à 6 px après correction (vérification indépendante du 23/09).
- **Cause** : un réglage de rendu écrit en millimètres absolus devient une géométrie disproportionnée sur les petites sections. Il se proportionne à la pièce : 2 % de la paroi la plus fine, plafonné à 0,6 mm, aucun sur une tôle (`largeur_chanfrein`). La correction a d'abord été jugée à l'œil (essais, planches, vérificateur), ce qui prouve l'image du jour et rien sur le code de demain. Le contrôle, écrit ensuite, a été vu rouge sur la version d'avant l'audit (commit b7b0341) et sur trois régressions simulées (chanfrein fixe, appel à `regler_chanfrein` retiré, tôle chanfreinée), vert sur le code corrigé. Il lit le source, sans Blender : il tourne aussi en CI.
- **Contrôle** : `tests/test_rendus_3d.py::ModelesSource::test_v1_le_chanfrein_reste_une_arete_vive`
- **Date** : 2026-09-23

### L-053 — la vue d'un visuel validé ne change pas sans l'accord du propriétaire (remplace la leçon du 23/09)
- **Symptôme** : le 23/09, le propriétaire : « parfois c'est beaucoup trop épais ». La barre rendue a été allongée 4 fois (`DEBORD`) pour sortir du cadre, et le studio porté à 18 fois la section. Le 24/09, en voyant le résultat en local : « Je veux vraiment avoir l'entièreté de la pièce et pas juste une coupe à moitié faite […] que tu laisses exactement les mêmes vues comme il y avait, juste que tu travailles plus la finition. » Plus de 200 images rendues avec la mauvaise vue, à refaire.
- **Cause** : la remarque visait la finition (arêtes arrondies, épaisseurs) ; elle a été lue comme un défaut de cadrage, et la vue a changé sur des planches jugées par Claude et le vérificateur, sans essai montré au propriétaire avant la série. Vue rétablie (ADR-0011) : tronçon de 6,25 fois vu en entier, studio à 7 fois. Contrôle réécrit, vu rouge sur le code du 23/09 (studio à 18, barre en débord), vert après : aucune barre ne sort du cadre, studio à 7 fois.
- **Contrôle** : `tests/test_rendus_3d.py::ModelesSource::test_v2_la_piece_entiere_reste_dans_le_cadre`
- **Date** : 2026-09-24

### L-054 — un contrôle d'image mesure ce que le visiteur voit
- **Symptôme** : le 23/09, les 37 plats refaits par l'audit passent tous leurs contrôles, mais la famille est refusée : « photo studio −31 niveaux de luminance par rapport aux visuels caractéristiques » (seuil 30). La photo studio n'avait pas changé (60 avant l'audit, 59 après) ; les fiches servies non plus (86 et 87).
- **Cause** : pour les barres en débord, le contrôle comparait le corps de la barre mesuré jusqu'au bord du rendu brut, donc aussi la partie cachée sous la fiche incrustée, que le site ne sert jamais. Avec la barre 4 fois plus longue, cette partie cachée faisait monter le corps des fiches de 85 à 92. La correction précédente (carré plein, le même jour) avait choisi une autre mesure sans voir qu'elle comptait des pixels invisibles : elle passait sur une famille et échouait sur la suivante. Mesuré sur la partie servie, l'écart vaut −23 avant comme après l'audit pour les plats, −13 et −15 pour le carré plein : la mesure ne bouge plus avec la composition, et le seuil de 30 reste celui calibré le 15/09. Contrôle vu rouge avant la correction, vert après ; les plats et le carré plein repassent à zéro écart.
- **Contrôle** : `tests/test_rendus_3d.py::ModelesSource::test_v3_une_barre_en_debord_se_mesure_sur_la_partie_servie`
- **Date** : 2026-09-23

### L-055 — une remarque mineure qui revient trois fois est un défaut
- **Symptôme** : le `.json` des photos studio ne notait que le type et la section des pièces, pas leur longueur. La vérification indépendante l'a signalé le 16/09, puis deux fois le 23/09 (plats, larges plats) : chaque fois, elle a dû retrouver la longueur commune des barres en ajustant une caméra sur l'image.
- **Cause** : la remarque était classée « mineure » et sa correction repoussée « après la production », pour ne pas changer l'empreinte du code en cours de série. Or l'empreinte ne se mélange qu'à l'intérieur d'une famille : chaque famille a son propre processus Blender, et le mode « points seuls » recalcule les `.json` d'une famille déjà rendue sans toucher aux images. Le report ne protégeait rien. Le contrôle, vu rouge avant la correction, vérifie que le code écrit la longueur ; `controler_rendus.py` refuse désormais un studio dont le fichier ne la porte pas.
- **Contrôle** : `tests/test_rendus_3d.py::ModelesSource::test_v5_la_photo_studio_note_la_longueur_de_chaque_piece`
- **Date** : 2026-09-23

### L-056 — une explication se prouve en rejouant la règle sur l'ancien fichier
- **Symptôme** : le 23/09, après l'audit, l'étiquette t de 17 tubes rectangulaires acier est descendue sous le tube, entre les deux rappels de la cote b ; sur le 50x20x2, « t 2 mm » se lisait comme la valeur de b. J'ai expliqué le déplacement par le chanfrein retiré, qui aurait masqué à la règle `paroi_sous()` le recouvrement de la paroi opposée. La vérification indépendante a rejoué la règle sur les anciens rendus : 5 à 23 % de paroi sous l'étiquette, bien au-dessus du seuil de 2 %. L'explication était fausse.
- **Cause** : ces images avaient été habillées le 15/09 à 6 h 12, six heures avant l'arrivée de la règle, et jamais rhabillées ; le contrôle de `controler_rendus.py` se taisait sur les sidecars sans centre d'étiquette. L'audit, en rhabillant, a appliqué la règle pour la première fois, et sa place de repli (sous la pièce) n'avait été jugée que sur trois tubes alu. Corrigé : `place_t_tube()` (cavité à 6 px des parois, sinon flanc du tube), contrôles d'habillage « entre les rappels d'une autre cote » et « à moins de 6 px d'un trait », sidecar sans centre = écart. Contrôle vu rouge avant la correction, vert après ; 19 fiches de 9 familles rhabillées sans fausse alerte.
- **Contrôle** : `tests/test_rendus_3d.py::ModelesSource::test_v6_une_etiquette_ne_se_lit_pas_comme_la_valeur_d_une_autre_cote`
- **Date** : 2026-09-23

### L-057 — une règle d'image écrite sur l'acier suppose un acier sombre
- **Symptôme** : le 23/09, sur le tube rectangulaire aluminium 60x30x3, l'étiquette t posée « sur le flanc » est partie à 350 px de sa pince, au bout d'un trait qui traversait toute la face. Puis, une fois replacée, le contrôle « étiquette t sur une paroi claire » l'a refusée à 100 %.
- **Cause** : `place_t_tube()` cherchait la fin de la paroi opposée au premier pixel sombre, et le contrôle de `controler_rendus.py` tenait toute surface claire sous l'étiquette pour une paroi. Deux hypothèses vraies sur l'acier (calamine sombre), fausses sur l'aluminium et l'inox, dont le flanc est aussi clair que la face sciée. Correctif : la paroi s'arrête à son épaisseur, mesurée sur la paroi pincée, quand la plage claire est trop longue ; l'habillage écrit la place choisie (`place_t` : cavité, calée, flanc) et le contrôle vérifie, pour le flanc, que l'étiquette laisse la paroi libre de 6 px. Les tubes acier sont restés identiques à l'octet. Règle : une mesure de pixels se teste sur toutes les matières du catalogue, pas seulement sur celle qui l'a fait naître.
- **Contrôle** : `tests/test_rendus_3d.py::ModelesSource::test_v7_l_etiquette_t_d_un_tube_clair_reste_pres_de_sa_section`
- **Date** : 2026-09-23

### L-058 — une valeur usuelle reprise d'un autre matériau se confronte à la photo du stock
- **Symptôme** : le 23/09, deux vérifications indépendantes ont trouvé des arrondis absents du produit, exactement la plainte du propriétaire : congé intérieur de t/2 sur les cornières alu (photo du stock G053 : angle quasi vif), coins extérieurs de 0,75 t sur les tubes carrés et rectangulaires alu (photos G061, G063 : coins vifs ; 30 px d'arrondi sur le 15x15x2). Les contrôles automatiques n'avaient rien vu : les images étaient fidèles à leurs données.
- **Cause** : ces rayons, jamais affichés, avaient été fixés comme « valeurs usuelles », en partie reprises de l'acier formé à froid (EN 10219), sans être posés à côté des photos du stock que le site publie. Corrigé dans `donnees_produits.py` (cornières alu 0,1 t, tubes alu 0,1 t, profils T alu 0,25 t d'après la photo, profils U confirmés par la photo), 16 valeurs changées et rien d'autre. Le contrôle, vu rouge avant (20 rayons), vert après : sur l'aluminium, un rayon supposé de plus d'un quart d'épaisseur doit citer la photo qui le justifie.
- **Contrôle** : `tests/test_rendus_3d.py::ModelesSource::test_v8_un_rayon_suppose_d_un_profil_alu_cite_la_photo_du_stock`
- **Date** : 2026-09-23

### L-059 — un réglage de matière se juge sur chaque forme de section
- **Symptôme** : le 23/09 au soir, la coupe claire de l'inox (base 0,58), adoptée sur un essai de cornière, sortait sur les 10 plats inox à 179 contre 183 pour la face longue : 4 niveaux d'écart, section à peine lisible en vignette. Sur la cornière, 9 niveaux ; sur le plat alu, 7.
- **Cause** : l'essai qui a fait adopter le réglage ne contenait ni plat inox ni mesure du contraste ; la face longue d'un plat, vue de face, est plus claire que celle d'une cornière. Corrigé en deux temps : coupe alu 0,66 et inox 0,50, puis alu 0,50 aussi (24/09, 0 h 10 : sur l'âme du profil T alu, face à 178, la coupe à 0,66 sortait 2 niveaux plus claire qu'elle) ; plats, T, U et cornières alu et six familles inox refaites dans la foulée. Contrôle, vu rouge avant (fonction absente), vert après : `controler_rendus.py` mesure la coupe contre la face longue voisine sur la rangée de la pince et refuse moins de 8 niveaux (plats, cornières, profils T et U) ; il refuse bien les 10 plats inox et laisse passer les familles lisibles.
- **Contrôle** : `tests/test_rendus_3d.py::ModelesSource::test_v9_la_coupe_se_distingue_de_la_face_longue`
- **Date** : 2026-09-23

### L-060 — un contrôle d'image qui exclut une forme ne la protège pas
- **Symptôme** : le 24/09 à 0 h 10, la vérification indépendante des tubes inox trouve la même coupe illisible que sur les plats : paroi opposée à 176 contre 183 pour le flanc des tubes carrés, anneau des tubes ronds au ton du corps sur son arc droit. Le contrôle V9, écrit une heure plus tôt pour ce défaut, excluait les tubes, dont la coupe « se lit contre la cavité sombre ».
- **Cause** : l'exclusion reposait sur une hypothèse vraie pour la paroi pincée (côté cavité), fausse pour la paroi d'en face et pour l'anneau, qui bordent le flanc. Corrigé : tubes ronds mesurés comme les plats (paroi pincée, flanc à droite), tubes carrés et rectangulaires par la paroi opposée (`contraste_paroi_opposee`, même épaisseur que la paroi pincée). Le contrôle, vu rouge avant (fonction absente), refuse les 14 tubes inox rendus à 0,58 et laisse passer les tubes acier.
- **Contrôle** : `tests/test_rendus_3d.py::ModelesSource::test_v10_la_paroi_d_un_tube_se_distingue_de_son_flanc`
- **Date** : 2026-09-24

### L-061 — retirer un défaut peut en révéler un autre, qu'il cachait
- **Symptôme** : le 24/09, la vérification indépendante des ronds à béton refaits par l'audit trouve deux demi-disques noirs sur chaque face sciée (297 px de noir pur sur le 12 mm, 1 avant l'audit), deux « rivets » visibles à pleine taille.
- **Cause** : les nervures longitudinales, des courbes à bouchons, partaient dans le plan même de la coupe ; le chanfrein de 0,6 mm, retiré par l'audit, masquait ce recouvrement. Le contrôle « part de noir pur » ne s'alerte qu'au-delà de 2 % de la pièce : 0,02 à 0,11 % ici. Corrigé dans `nervures_barre()` : départ 0,02 mm derrière la coupe, bouchons convertis en maillage et passés en matière de coupe ; au passage, nervures transverses inclinées en hélice (mineur du 15/09 jamais repris). Essai : 6 px de noir pur. Contrôle, vu rouge avant (fonction absente), puis refusant les 7 fiches de ronds à béton et aucune autre section pleine : plus de 20 px de noir pur dans la partie servie d'une section pleine est un écart.
- **Contrôle** : `tests/test_rendus_3d.py::ModelesSource::test_v11_aucun_noir_pur_sur_une_section_pleine`
- **Date** : 2026-09-24

### L-062 — un réglage de coupe se juge bord par bord, contre la face vue au-delà de chaque bord
- **Symptôme** : le 24/09, la vérification indépendante des U alu refaits à la coupe 0,50 trouve l'aile basse confondue avec le fond du U vu au-dessus d'elle : coupe à 149–155 contre 156–157, 1 à 4 niveaux sur les 4 fiches (22 à 27 avec l'ancienne coupe 0,36). L'épaisseur de l'aile basse ne se lit plus ; les contrôles automatiques étaient à 0 écart.
- **Cause** : V9 mesure la coupe à la seule rangée de la pince, donc sur l'âme ; aucun contrôle ne regardait les autres bords de la section. Et une valeur unique par finition ne peut pas convenir à la fois aux dessus sombres (140–151) et au fond clair du U (156). Contrôle, vu rouge avant (fonction absente), puis refusant les 4 U alu (0 à 1 niveau) : `contraste_aile_basse` (`controler_rendus.py`) mesure la bande du bas de la pièce, de l'épaisseur de l'aile haute, contre le fond au-dessus, et refuse moins de 8 niveaux. Corrigé pour le U alu seulement : `base_coupe` 0,40 (`reglages_matiere`, `preparer_rendus.py`) ; plus sombre pour tout l'aluminium, le dessus des plats 80x5 et 100x5 tomberait sous 8.
- **Contrôle** : `tests/test_rendus_3d.py::ModelesSource::test_v12_l_aile_basse_du_u_se_distingue_du_fond`
- **Date** : 2026-09-24
