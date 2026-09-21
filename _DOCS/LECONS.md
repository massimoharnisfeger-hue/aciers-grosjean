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
