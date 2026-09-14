# Brief — visuels 3D des fiches produits

Objectif : chaque fiche produit affiche trois visuels cohérents, exacts et dans la charte du site.

| Visuel | Portée | Produit par |
|---|---|---|
| Photo studio, fond blanc | 1 par catégorie, commune à ses fiches | Blender (rendu 3D) — ou IA, à décider |
| Caractéristiques : pièce cotée + fiche technique | 1 par fiche, aux cotes exactes | Blender + habillage automatique |
| Mise en situation | 1 par catégorie | IA (ChatGPT, Gemini) |

Test réalisé le 14/09/2026 : `_DEPOT/images/test-blender/poutrelle-ipe-200-en-acier-caracteristiques.png`
(rendu 4 min 15 s sur le PC, cotes et fiche lues dans `lib/catalogue.ts`).

---

## 1. Méthode

1. **Valider le style** sur l'IPE 200 et sur une photo studio de la catégorie IPE.
2. **Corriger le catalogue d'abord.** Les visuels lisent le catalogue : une erreur du site devient une erreur sur l'image. 50 lignes sont déjà signalées dans le classeur.
3. **Produire par vagues**, dans l'ordre où les données sont prêtes :

   | Vague | Produits | Contenu | État des données |
   |---|---|---|---|
   | 1 | 253 | Poutrelles, cornières, fers T, plats, ronds, carrés, tubes, tôles laminées à chaud, armatures | Complètes. Il ne manque que la finition réelle. |
   | 2 | 145 | Tôles laminées à froid, galvanisées, corten, larmées, perforées ; tout l'alu et l'inox | Cotes présentes. Finition et motif à confirmer. |
   | 3 | 73 | Clôtures, bordures, caillebotis et marches, tôles profilées, panneaux isolés, tasseaux | Fiches fournisseurs en main, sauf exceptions (§ 3.4). |
   | 4 | 24 | Colles, galvanisation à froid, primaires, visserie, outillage | Pas de 3D : photos des fournisseurs. |

4. **Pour chaque famille** : un rendu test → validation → rendu en série la nuit → contrôle image par image → intégration sur les fiches → mise en ligne.
5. **En parallèle** : les photos de mise en situation par IA, une par catégorie.

Temps de calcul estimé : ~40 photos studio + 398 visuels de caractéristiques ≈ 30 h au rythme du test, soit plusieurs nuits PC branché. Optimisation à tester.

---

## 2. Déjà en main — rien à demander

- **Cotes** des 398 produits acier, alu et inox : `lib/catalogue.ts`.
- **Rayons de congé et d'angle** (r, r1, r2) : tableaux fournisseurs VM 2013 dans `_DEPOT/documents/pdf-site-actuel/`
  (IPE, HEA, HEB, UPN, cornières égales et inégales, fers T, plats, larges plats, ronds, carrés, tubes carrés et ronds, tôles laminées à chaud).
- **Fiches techniques** : clôtures Clogriff 64 et Cloplus 40, caillebotis et marches PcP, tôle 30.200.1000, panneau Eurocopre Monolamiera, tasseaux imitation bois, Zinga, DL Chemicals, Vibol, vis TH, meuleuse Flex.
- **Motifs** : perforations (R5 T8, R10 T15, C10 U15), épaisseurs des tôles larmées et striées, modèles, hauteurs et RAL des clôtures, mailles des caillebotis — tous lus dans les noms des produits.
- **Charte** : polices Poppins, Questrial, IBM Plex Mono ; couleurs encre, jaune, acier, brume.

---

## 3. À fournir

### 3.1 Décisions (5 minutes)

- [ ] Rendu de l'IPE 200 : validé ? (teinte de l'acier, placement des cotes, fiche à droite)
- [ ] Photo studio : Blender avec **une barre**, Blender avec **2 ou 3 tailles côte à côte** (ex. IPE 100, 200, 300), ou IA ?
- [ ] Logo Aciers Grosjean sur les visuels : oui / non
- [ ] Mention « Rendu 3D aux cotes nominales — illustration non contractuelle » : garder ?

### 3.2 Le classeur, produit par produit

Fichier : `_DEPOT/rendus-3d/collecte-donnees-produits.xlsx` (regénérable avec `python scripts/generer-collecte-rendus.py`).
Les 495 produits sont pré-remplis. Pour chacun, **quatre cases jaunes** :

| Case | Pourquoi |
|---|---|
| Finition réelle en stock (menu) | C'est ce qui change le plus le rendu : noir, décapé, galvanisé, brut, brossé, corten neuf ou patiné… |
| Cotes exactes ? oui / non + correction | Les chiffres s'affichent sur l'image. |
| Détails visibles | Cordon de soudure dans les tubes, film de protection sur l'alu et l'inox, sens du brossage, face laquée… |
| Réponse à la remarque | 50 lignes signalent une erreur ou un manque (voir § 3.4). |

Une réponse par catégorie suffit souvent (« tous les tubes carrés acier sont noirs ») : l'écrire sur la première ligne de la catégorie.
Priorité : feuille **Vague 1**.

### 3.3 Photos de référence des finitions

Quatorze sujets, listés dans la feuille « Photos matières » du classeur. Elles servent à caler les matières et **ne sont pas publiées**.

- Téléphone, lumière du jour, **sans flash**.
- Trois prises par sujet : vue d'ensemble, gros plan à 20 cm, extrémité ou tranche.
- Pour les motifs (larmée, perforée, striée) : une pièce de monnaie posée à côté, pour l'échelle.
- Dépôt : `_DEPOT/images/references-matieres/`, nommées comme indiqué dans la feuille.

### 3.4 Documents et corrections

- [ ] **Profils U en aluminium** (4) : le site affiche une épaisseur de 20 à 40 mm, le nom indique 2 mm.
- [ ] **Tôles alu et inox** (34) : le site propose l'oxycoupage, impossible sur ces métaux. Remplacer par cisaillage, plasma ou laser selon l'atelier.
- [ ] **Poteau Clogriff 64 – 2M50 – « VERT RAL 7016 »** : 7016 est un gris anthracite.
- [ ] **Panneaux MEDIUM 3D** (9) : fiche technique du fournisseur.
- [ ] **Fixations de clôture** (5) : photo ou plan coté.
- [ ] **Bordures corten et galvanisée** (2) : forme exacte de « 150/25 » et système de piquets.
- [ ] **Tôle perforée « aléatoire »** : photo ou plan du motif.
- [ ] **Marches caillebotis hors PcP** (5) : maille et nez de marche.
- [ ] **Alu et inox** : tableaux de cotes du fournisseur s'ils existent (rayons des tubes et profils). À défaut, valeurs usuelles.

### 3.5 Produits de marque (vague 4)

Pour les 24 produits : photos HD des fournisseurs (Zinga, DL Chemicals, Flex, primaire anticorrosion, visserie) et l'accord de les utiliser sur le site.

---

## 4. Message prêt à envoyer à l'entreprise

> Bonjour,
>
> Pour les nouvelles fiches produits du site, nous préparons des visuels 3D réalisés aux cotes exactes de chaque référence. Les cotes et les fiches techniques sont déjà rassemblées ; il nous manque surtout des confirmations sur l'état réel du stock.
>
> 1. Un classeur Excel pré-rempli (495 produits) : pour chaque référence, choisir la finition réelle en stock dans le menu, confirmer les cotes et répondre aux remarques en orange. Une réponse par catégorie suffit souvent.
> 2. Quelques photos au téléphone dans le dépôt (liste dans l'onglet « Photos matières ») : lumière du jour, sans flash, vue d'ensemble, gros plan et extrémité. Elles servent de référence et ne seront pas publiées.
> 3. Si vous les avez : la fiche technique des panneaux MEDIUM 3D, une photo des fixations de clôture et des bordures, et les photos HD des produits de marque (Zinga, DL Chemicals, Flex…) avec l'accord de les utiliser.
>
> Nous avons aussi relevé trois erreurs sur le site en préparation (profils U alu, découpe des tôles alu et inox, un poteau de clôture) : elles sont signalées dans le classeur.
>
> Merci d'avance !

---

## 5. Prompt de lancement pour une séance Claude

> Lis `CLAUDE.md`, puis `_DOCS/BRIEF-RENDUS-3D.md` et le dernier fichier de `_JOURNAL/`.
> Nous produisons les visuels 3D des fiches produits. Les scripts du test sont dans `scripts/rendu-3d/`
> (Blender 4.5 LTS portable dans `%LOCALAPPDATA%\Blender`, travail dans `%LOCALAPPDATA%\SiteAciersGrosjean\rendu3d`).
> Lis le classeur `_DEPOT/rendus-3d/collecte-donnees-produits.xlsx` : applique d'abord les corrections au générateur du catalogue,
> puis, pour la vague [N] : ajoute les sections manquantes au script de rendu (cotes du catalogue, rayons des tableaux VM 2013),
> cale les matières sur `_DEPOT/images/references-matieres/`, fais un rendu test par famille et montre-le-moi avant la série.
> Contrôle chaque image avant de l'intégrer. WebP < 200 Ko, `alt` descriptif, fin de séance selon `CLAUDE.md`.
