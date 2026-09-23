# Prompts de mise en situation — un par catégorie

Écrits le 22/09/2026 d'après le brief du propriétaire, puis audités par une seconde passe
qui en a corrigé **30 sur 54** (décor dupliqué, scène invraisemblable, image de référence
inexistante, exigence de fidélité trop faible).

**Rien n'a été généré.** Aucun crédit dépensé, aucune image produite. Ce document est la
matière à relire avant de lancer quoi que ce soit.

## Ce que dit le brief, en une phrase

Une photographie réaliste du produit **réel** intégré dans un projet concret, pour que le
client se projette — pas une scène publicitaire, pas d'influenceur, pas d'avatar. La photo
produit existante fait foi : forme, section, matière, couleur et finition ne se redessinent pas.

## 5 catégories bloquées faute de photo produit

Ces catégories n'ont **aucun visuel** dans le dépôt. Sans photo de référence, l'image de mise
en situation n'a rien à respecter : elle inventerait le produit. Ce sont les consommables déjà
identifiés comme dépourvus de rendu 3D — un rendu coté n'a pas de sens pour un tube de mastic,
mais une photo studio, si.

| Catégorie | Produit de référence à photographier |
|---|---|
| `/quincaillerie/outillage` | `meuleuse-d-angle-flex-l-1001-1010w-125-mm` |
| `/quincaillerie/protection-chimie/colles-etancheite` | `dl-chemicals-parabond-600-290ml-gris` |
| `/quincaillerie/protection-chimie/galvanisation-a-froid` | `zinga-film-galvanisant-1kg` |
| `/quincaillerie/protection-chimie/peintures-primaires` | `primer-anticorrosion-1l-blanc-ral-9010` |
| `/quincaillerie/visserie` | `vis-a-bois-6-3x-100-tete-hexagonale-de-10mm` |

**Ordre des opérations** : photo studio fond blanc → dépôt sous
`public/images/produits/<univers>/<catégorie>/studio-<famille>.webp` → référencement dans
`lib/visuels-produits.json` → alors seulement la mise en situation.

## 49 prompts prêts

### Rond à béton laminé à chaud

`/acier/armatures-beton/rond-a-beton-lamine-a-chaud`

**Scène.** Semelle de fondation ferraillée sur un chantier de maison en Wallonie : cage de barres ligaturées dans un coffrage bois, juste avant le coulage.

**Référence.** `/images/produits/acier/armatures-beton/rond-a-beton-lamine-a-chaud/studio-rond-a-beton-lamine-a-chaud.webp`

```text
Photorealistic documentary photograph of a house foundation being reinforced on a residential building site in Wallonia, Belgium: hot-rolled ribbed reinforcing bars tied into a cage inside a timber formwork trench, resting on small concrete spacers, tie wire twisted at the crossings, excavated clay soil, a wheelbarrow and a concrete mixer truck out of focus behind, red-brick neighbouring houses and a grey overcast sky.

PRODUCT FIDELITY — ABSOLUTE PRIORITY: the attached reference photograph is the only source of truth for the bar itself. Reproduce exactly the same round cross-section, the same rib and transverse pattern, the same rolled-steel surface texture, the same colour and the same finish. The reference shows several diameters of the same family side by side: it defines shape, section, surface and material, not how many bars appear in the scene. Do not redraw, smooth, simplify, restyle or replace the product; never turn the ribbed bar into a plain smooth rod; do not add paint, galvanising, coating or surface markings that are not in the reference.

PHOTOGRAPHY: ultra-realistic, full-frame camera, 35 mm lens, eye level, soft overcast Northern-European daylight, physically correct shadows and dull metallic reflections, natural depth of field with a sharp foreground and a softly blurred background, real site imperfections — dried mud splashes, dust, a thin orange surface rust film, footprints in the soil.

PEOPLE: none needed. Only if scale demands it, one site worker may appear small and secondary, seen from behind or cropped at the edge, never centred, never facing the camera, never hiding the bars.

FRAMING: the reinforcing cage fills a large, clearly readable part of the foreground; the site around it is legible but secondary. No text, signage, labels, stickers, logos, stamped markings or numbers anywhere in the image.
```

```text
NEGATIF — CGI render, 3D render, video-game look, plastic or waxy surface, over-clean perfect objects, smooth unribbed bar, altered rib pattern, changed cross-section, painted or galvanised finish, invented markings, any text, numbers, logos, watermarks, signage, influencer, presenter, model facing camera, selfie, social-media styling, person centred in frame, HDR glow, heavy vignette, oversaturated colours, warped perspective, floating or duplicated bars, melted geometry, artefacts, extra fingers
```

### Rond à béton laminé à froid

`/acier/armatures-beton/rond-a-beton-lamine-a-froid`  — *corrigé par l'audit*

**Scène.** Aire de ferraillage d'un petit chantier belge : étriers et cadres en fines barres crénelées ligaturés en cages élancées sur tréteaux, au pied d'un coffrage de poteau.

**Référence.** `/images/produits/acier/armatures-beton/rond-a-beton-lamine-a-froid/studio-rond-a-beton-lamine-a-froid.webp`

**Correction apportée.** Décor dupliqué : la scène (linteau au-dessus d'une baie, maison en brique en rénovation, étais) est la même que celle de la poutrelle IPE — même sujet, même bâtiment, même lumière. Référence valide. Scène réécrite vers l'usage propre au laminé à froid dans lib/usages.ts (« cadres et étriers », armatures secondaires de faible section) : atelier de ferraillage sur chantier, sans linteau ni étais, et sans grosses barres en premier plan qui feraient concurrence au produit de référence.

```text
Photorealistic documentary photograph of the reinforcement bay of a small building site in Belgium: thin cold-rolled ribbed reinforcing bars bent into rectangular stirrups and tied with twisted wire into slender cages, laid across wooden trestles beside a plywood column formwork, a manual bar bender and a coil of tie wire on the ground, bundles of cut bars stacked on timber bearers, a heap of sand, a concrete block wall and a grey overcast sky behind.

PRODUCT FIDELITY — ABSOLUTE PRIORITY: the attached reference photograph is the only source of truth for the bar itself. Reproduce exactly the same round cross-section, the same fine rib pattern, the same cold-rolled surface texture, the same colour and the same finish as in the reference. Every bar in focus must be this product and this slender diameter. Do not redraw, thicken, smooth, simplify or replace it; never turn the ribbed bar into a plain smooth rod; do not add paint, coating, galvanising or markings absent from the reference. Bends and hooks are allowed only where the stirrups require them, with the section kept identical along the bar and honest saw-cut ends.

PHOTOGRAPHY: ultra-realistic, full-frame camera, 50 mm lens, three-quarter viewpoint at trestle height so the ribs and the tied corners read clearly, soft overcast Northern-European daylight, physically correct shadows and weak metallic reflections, natural depth of field with the stacked bars falling out of focus behind, real imperfections — a faint rust film on the steel, cement dust, mud on the trestles, wire offcuts on the ground.

PEOPLE: none required; if scale demands it, one worker small, secondary, cropped or seen from behind, never centred, never facing the camera, never masking the steel.

FRAMING: the tied stirrups and cages fill a large, clearly readable part of the frame; the site stays secondary. No text, signage, labels, logos, stamped markings or numbers in the image.
```

```text
NEGATIF — CGI render, 3D render, plastic or rubbery surface, over-smooth perfect steel, smooth unribbed rod, oversized bar diameter, thick structural bars in focus, changed section, painted or galvanised look, invented markings, any text, numbers, logos, watermark, influencer, presenter, face to camera, selfie, lifestyle styling, person centred, HDR glow, oversaturation, distorted perspective, floating bars, melted or fused geometry, artefacts
```

### Treillis soudés

`/acier/armatures-beton/treillis-soudes`

**Scène.** Dalle de terrasse en préparation derrière une maison belge : nappes de treillis soudé posées sur cales, coffrage périphérique, avant le coulage.

**Référence.** `/images/produits/acier/armatures-beton/treillis-soudes/studio-treillis-soude.webp`

```text
Photorealistic documentary photograph of a garden terrace slab being prepared behind a Belgian brick house: flat welded steel mesh panels laid over a compacted hardcore bed and a polythene sheet, raised on small plastic and concrete spacers, panels overlapping at the edges, timber edge formwork around the slab, a shovel and a coil of tie wire resting nearby, hedges and a grey overcast sky in the background.

PRODUCT FIDELITY — ABSOLUTE PRIORITY: the attached reference photograph is the only source of truth for the mesh. Reproduce exactly the same square grid geometry, the same wire section, the same welded cross-junctions, the same flat panel edges, the same steel colour, surface texture and finish. Keep the mesh proportions consistent with the reference; do not redraw, re-space, stylise or replace it, do not turn welded mesh into woven or crimped wire netting, do not add coating, paint or galvanising that is not in the reference. The reference shows several sizes of the same family side by side: it defines the product, not the number of panels in the scene.

PHOTOGRAPHY: ultra-realistic, full-frame camera, 35 mm lens, high three-quarter viewpoint showing the grid receding in perspective, soft overcast Northern-European daylight, physically correct shadows cast by the grid onto the sub-base, natural depth of field, real imperfections — dust, mud, a light rust bloom at the welds, slightly bent wire ends.

PEOPLE: none required; if scale demands it, one worker small, secondary, cropped or from behind, never centred, never facing the camera, never covering the mesh.

FRAMING: the mesh fills a large, clearly readable part of the image, its grid unmistakable; the garden context stays secondary. No text, signage, labels, logos, stamped markings or numbers in the image.
```

```text
NEGATIF — CGI render, 3D render, plastic look, woven wire netting, chicken wire, chain-link, irregular or wavy grid, wrong mesh spacing, missing welds, painted or bright galvanised finish, over-clean perfect panels, any text, numbers, logos, watermark, influencer, presenter, face to camera, selfie, social-media styling, person centred, HDR glow, oversaturation, warped perspective, floating panels, moiré artefacts, melted geometry
```

### Treillis à dépassants

`/acier/armatures-beton/treillis-soudes-depassants`

**Scène.** Grand dallage de hangar agricole : deux panneaux de treillis à dépassants se recouvrant bord à bord pour assurer la continuité de l'armature.

**Référence.** `/images/produits/acier/armatures-beton/treillis-soudes-depassants/studio-treillis-soude-depassants.webp`

```text
Photorealistic documentary photograph of a large floor slab being armed inside an agricultural shed under construction in Belgium: two welded steel mesh panels with protruding wire ends laid side by side on spacers over a levelled sub-base, the protruding ends of one panel overlapping the body of the next and tied with wire, a construction joint and a screed rail crossing the slab, steel portal frame and translucent roof lights above, daylight entering from the open gable end.

PRODUCT FIDELITY — ABSOLUTE PRIORITY: the attached reference photograph is the only source of truth for the mesh. Reproduce exactly the same square grid, the same wire section, the same welded junctions and, above all, the same protruding wire ends on the panel edges, with the same look and the same proportion as in the reference. Do not redraw, re-space, trim or stylise the product, do not remove the protruding ends, do not turn welded mesh into woven netting, do not add paint, coating or galvanising absent from the reference. The reference shows several sizes of the same family side by side: it defines the product, not the number of panels in the scene.

PHOTOGRAPHY: ultra-realistic, full-frame camera, 35 mm lens, low three-quarter viewpoint along the overlap so the protruding ends read clearly, soft diffuse daylight, physically correct shadows of the grid on the sub-base, natural depth of field, real imperfections — dust, tyre tracks, a light rust bloom, slightly bent wire ends.

PEOPLE: none required; if scale demands it, one worker small, secondary, cropped or from behind, never centred, never facing the camera, never hiding the mesh.

FRAMING: the overlapping panels and their protruding ends fill a large, clearly readable part of the frame; the shed stays secondary. No text, signage, labels, logos, stamped markings or numbers in the image.
```

```text
NEGATIF — CGI render, 3D render, plastic look, protruding ends removed or shortened, panels with clean cut edges only, woven wire netting, chain-link, irregular grid, wrong spacing, missing welds, painted or shiny galvanised finish, over-clean perfect panels, any text, numbers, logos, watermark, influencer, presenter, face to camera, selfie, person centred, HDR glow, oversaturation, warped perspective, floating panels, moiré artefacts, melted geometry
```

### Poutrelle HEA

`/acier/poutrelles/hea`

**Scène.** Poteau d'ossature métallique boulonné sur sa platine d'ancrage, sur le chantier d'une extension d'atelier.

**Référence.** `/images/produits/acier/poutrelles/hea/studio-poutrelle-hea.webp`

```text
Photorealistic documentary photograph of a steel-framed workshop extension under construction in Belgium: a wide-flange H-section steel column standing vertically, bolted through a welded base plate onto a concrete foundation pad, a beam already bolted to its flange at mid-height, other columns lined up behind, scaffolding, a compacted gravel site floor, brick buildings and a grey overcast sky.

PRODUCT FIDELITY — ABSOLUTE PRIORITY: the attached reference photograph is the only source of truth for the profile. Reproduce exactly the same H cross-section with its wide flanges, the same flange-to-web proportion, the same web thickness, the same root fillets, the same rolled-steel surface, the same colour and the same finish. The reference shows several sizes of the same family side by side: it defines the section and the material, not the number of pieces in the scene. Do not redraw, taper, thin, restyle or substitute the profile, never replace it with a narrow I-section or a channel, do not add paint, galvanising, fireproofing or rolled markings that are not in the reference; cut ends must be honest saw-cut ends.

PHOTOGRAPHY: ultra-realistic, full-frame camera, 35 mm lens, slightly low angle emphasising the column's height, soft overcast Northern-European daylight, physically correct shadows and dull reflections along the flanges, natural depth of field, real imperfections — mill scale, light surface rust, chalk marks smeared, dust, drill swarf near the base plate.

PEOPLE: none required; if scale demands it, one erector small, secondary, cropped or from behind, never centred, never facing the camera, never hiding the profile.

FRAMING: the column fills a large, clearly readable part of the frame, its H section unmistakable; the site stays secondary. No text, signage, labels, logos, stamped markings or numbers in the image.
```

```text
NEGATIF — CGI render, 3D render, architectural visualisation, plastic or chrome surface, over-clean perfect steel, narrow I-beam instead of wide-flange H, channel or box section, wrong flange width, tapered or bent profile, painted red or white finish, galvanised look, invented rolling marks, any text, numbers, logos, watermark, influencer, presenter, face to camera, selfie, person centred, HDR glow, lens flare, oversaturation, warped perspective, floating steel, melted geometry, artefacts
```

### Poutrelle HEB

`/acier/poutrelles/heb`  — *corrigé par l'audit*

**Scène.** Poutre principale en H épais installée en support d'une plateforme de machine, dans un atelier de production en service.

**Référence.** `/images/produits/acier/poutrelles/heb/studio-poutrelle-heb.webp`

**Correction apportée.** Décor dupliqué avec la HEA : même chantier de charpente métallique, même ciel gris, même assemblage boulonné vu de dessous — deux catégories voisines auraient produit deux photos jumelles. La référence est valide. Scène réécrite sur l'usage propre à la HEB dans lib/usages.ts (« supports de machine », « poutres principales », charges plus fortes) : intérieur d'usine en service, lumière et matériaux différents. L'élingue de grue encore accrochée a aussi été retirée, c'est le détail qui produit le plus d'artefacts de gréage impossible.

```text
Photorealistic documentary photograph of a heavy steel beam installed inside a working production plant in Belgium: a thick wide-flange H-section beam spanning horizontally between two existing columns, bolted through end plates with large bolts and washers, carrying the steel platform of a heavy production machine above it, packing plates at the seatings, a worn concrete floor, cable trays and pipework running along a painted brick wall, machines and stacked pallets out of focus, mixed light from high windows and industrial lamps.

PRODUCT FIDELITY — ABSOLUTE PRIORITY: the attached reference photograph is the only source of truth for the profile. Reproduce exactly the same H cross-section with its wide flanges and its noticeably thick web and flanges, the same proportions, the same root fillets, the same rolled-steel surface, colour and finish. The reference shows several sizes of the same family side by side: it defines the section and the material, not the number of pieces in the scene. Do not redraw, slim down, taper, restyle or substitute the profile, never replace it with a narrow I-section or a channel, do not add paint, galvanising or rolled markings that are not in the reference; ends must be honest saw-cut or plated ends.

PHOTOGRAPHY: ultra-realistic, full-frame camera, 35 mm lens, low angle from the floor looking up along the underside and one flange so the thickness of the section reads, physically correct shadows and dull reflections on the flanges, natural depth of field, real imperfections — mill scale, light rust, grease on the bolts, dust on the top flange, scuffed concrete.

PEOPLE: none required; if scale demands it, one fitter small, secondary, cropped or from behind, never centred, never facing the camera, never hiding the beam.

FRAMING: the beam and its bolted end connection fill a large, clearly readable part of the frame; the plant stays secondary. No text, signage, labels, logos, stamped markings or numbers in the image.
```

```text
NEGATIF — CGI render, 3D render, architectural visualisation, plastic or chrome look, over-clean perfect steel, thin-walled profile, narrow I-beam, channel or box section, wrong flange thickness, tapered or bent beam, painted or galvanised finish, invented rolling marks, any text, numbers, logos, watermark, machine branding, influencer, presenter, face to camera, selfie, person centred, HDR glow, lens flare, oversaturation, warped perspective, floating steel, melted geometry, artefacts
```

### Poutrelle IPE

`/acier/poutrelles/ipe`

**Scène.** Linteau posé au-dessus d'une ouverture percée dans un mur porteur en brique, chantier de rénovation avec étais.

**Référence.** `/images/produits/acier/poutrelles/ipe/studio-poutrelle-ipe.webp`

```text
Photorealistic documentary photograph of a structural opening being formed in a load-bearing brick wall of a Belgian house under renovation: a narrow, tall I-section steel beam installed horizontally as a lintel over the new opening, its ends bearing on brick piers with mortar packing, adjustable steel props still supporting the wall above, brick dust and rubble on the floor, a dust-sheeted room on one side and daylight from the garden on the other.

PRODUCT FIDELITY — ABSOLUTE PRIORITY: the attached reference photograph is the only source of truth for the profile. Reproduce exactly the same I cross-section, taller than it is wide, with the same narrow flanges, the same slender web, the same root fillets, the same rolled-steel surface, colour and finish. The reference shows several sizes of the same family side by side: it defines the section and the material, not the number of pieces in the scene. Do not redraw, widen, restyle or substitute the profile, never replace it with a wide-flange H-section or a channel, do not add paint, galvanising, fire protection or rolled markings that are not in the reference; ends must be honest saw-cut ends.

PHOTOGRAPHY: ultra-realistic, full-frame camera, 35 mm lens, slightly low angle looking along the beam so the I section reads, mixed soft daylight from the opening and dim interior light, physically correct shadows and dull reflections, natural depth of field, real imperfections — mill scale, light rust, brick dust settled on the top flange, chalk marks, scuffed plaster.

PEOPLE: none required; if scale demands it, one worker small, secondary, cropped or from behind, never centred, never facing the camera, never hiding the beam.

FRAMING: the beam spans a large, clearly readable part of the frame; the renovation stays secondary. No text, signage, labels, logos, stamped markings or numbers in the image.
```

```text
NEGATIF — CGI render, 3D render, architectural visualisation, plastic or chrome look, over-clean perfect steel, wide-flange H-beam, channel or box section, square proportions, wrong flange width, bowed or tapered beam, painted or galvanised finish, invented rolling marks, any text, numbers, logos, watermark, influencer, presenter, face to camera, selfie, person centred, HDR glow, oversaturation, warped perspective, floating beam, impossible bearing, melted geometry, artefacts
```

### Poutrelle UPN

`/acier/poutrelles/upn`

**Scène.** Chevêtre de trémie d'escalier dans un plancher de loft en rénovation : profilés en U posés en encadrement, gorge tournée vers l'intérieur de la trémie.

**Référence.** `/images/produits/acier/poutrelles/upn/studio-poutrelle-upn.webp`

```text
Photorealistic documentary photograph of a stairwell opening being trimmed in the floor of a brick loft under renovation in Belgium: U-shaped channel steel sections bolted together to frame the rectangular opening, their open grooves facing into the void so the timber joist ends sit inside them, joists and floorboards stopping at the frame, a stepladder and a cordless drill on the boards, dusty light from a roof window, exposed brick walls and old roof trusses.

PRODUCT FIDELITY — ABSOLUTE PRIORITY: the attached reference photograph is the only source of truth for the profile. Reproduce exactly the same U cross-section, open on one face, with the same web height, the same flange length, the same slightly tapered inner flange faces and root fillets, the same rolled-steel surface, colour and finish. The reference shows several sizes of the same family side by side: it defines the section and the material, not the number of pieces in the scene. Do not redraw, close, box, restyle or substitute the profile, never replace it with an I or H beam or a rectangular tube, do not add paint, galvanising or rolled markings that are not in the reference; ends must be honest saw-cut ends.

PHOTOGRAPHY: ultra-realistic, full-frame camera, 35 mm lens, high three-quarter viewpoint looking down into the opening so the open groove is visible, soft daylight from above, physically correct shadows inside the channel, natural depth of field, real imperfections — mill scale, light rust, sawdust and plaster dust, chalk lines, scratched timber.

PEOPLE: none required; if scale demands it, one worker small, secondary, cropped or from behind, never centred, never facing the camera, never hiding the steel.

FRAMING: the channel frame fills a large, clearly readable part of the image, its open U section unmistakable; the loft stays secondary. No text, signage, labels, logos, stamped markings or numbers in the image.
```

```text
NEGATIF — CGI render, 3D render, architectural visualisation, plastic or chrome look, over-clean perfect steel, closed box section, I-beam or H-beam instead of channel, groove facing the wrong way, symmetrical flanges of equal thickness, wrong web height, painted or galvanised finish, invented rolling marks, any text, numbers, logos, watermark, influencer, presenter, face to camera, selfie, person centred, HDR glow, oversaturation, warped perspective, floating steel, melted geometry, artefacts
```

### Carré plein

`/acier/profiles/carre-plein`

**Scène.** Grille de fenêtre en barres carrées pleines, ferronnerie soudée fraîchement posée sur la façade en brique d'une maison de village.

**Référence.** `/images/produits/acier/profiles/carre-plein/studio-carre-plein.webp`

```text
Photorealistic documentary photograph of a hand-made steel window grille freshly fitted to the brick facade of a village house in Wallonia: vertical solid square steel bars set at regular spacing, welded through a flat frame, anchored into the brick reveals, bare steel with fresh grinder marks at the welds, an old wooden window behind the bars, weathered pointing, a climbing plant at the edge of the frame, soft grey daylight.

PRODUCT FIDELITY — ABSOLUTE PRIORITY: the attached reference photograph is the only source of truth for the bar. Reproduce exactly the same solid square cross-section with its slightly rounded rolled corners, the same face flatness, the same rolled-steel surface texture, the same colour and the same finish. The reference shows several sizes of the same family side by side: it defines the section and the material, not the number of bars in the scene. Do not redraw, twist, taper, round, hollow out, restyle or substitute the bar; never turn it into a round bar, a tube or a decorative forged element; do not add paint, galvanising, scrollwork or markings that are not in the reference; cut ends must be honest saw-cut ends.

PHOTOGRAPHY: ultra-realistic, full-frame camera, 50 mm lens, one single slightly angled three-quarter viewpoint on the facade so the square section is read on the bar ends while the grille stays nearly frontal, soft overcast daylight raking across the brickwork, physically correct shadows of the bars on the wall and dull reflections along the flats, natural depth of field, real imperfections — mill scale, light rust film, weld discolouration, brick dust.

PEOPLE: none. No figure is needed at this scale.

FRAMING: the grille and its square bars fill a large, clearly readable part of the frame; the house stays secondary. No text, signage, labels, logos, stamped markings or numbers in the image.
```

```text
NEGATIF — CGI render, 3D render, plastic or chrome look, over-clean perfect steel, round bar, hollow tube, twisted or forged decorative bar, wrong corner radius, tapered bar, painted black or galvanised finish, ornate scrollwork, invented markings, any text, numbers, logos, watermark, influencer, presenter, face to camera, selfie, person centred, HDR glow, oversaturation, warped perspective, floating bars, bars of uneven section, melted geometry, artefacts
```

### Cornière égale

`/acier/profiles/corniere-egale`

**Scène.** Cadre de portail en cornières à ailes égales, assemblé et pointé sur la table d'un atelier de serrurerie.

**Référence.** `/images/produits/acier/profiles/corniere-egale/studio-corniere-egale.webp`

```text
Photorealistic documentary photograph of a gate frame being assembled in a small Belgian metalworking shop: equal-leg steel angle sections cut with mitred corners and laid flat on a scarred steel welding table, clamped square with F-clamps and an angle square, the corners tacked with fresh weld beads, welding cables and a chipping hammer at the edge of the table, daylight from a workshop window mixing with an overhead lamp, other angle lengths racked in the background.

PRODUCT FIDELITY — ABSOLUTE PRIORITY: the attached reference photograph is the only source of truth for the profile. Reproduce exactly the same L cross-section with two legs of equal width, the same leg thickness, the same rounded inner root and outer heel, the same rolled-steel surface texture, colour and finish. The reference shows several sizes of the same family side by side: it defines the section and the material, not the number of pieces in the scene. Do not redraw, thin, thicken, restyle or substitute the profile; never make the legs unequal; never replace it with a folded sheet-metal angle, a channel or a tube; do not add paint, galvanising or markings that are not in the reference; ends must be honest saw-cut or mitred ends.

PHOTOGRAPHY: ultra-realistic, full-frame camera, 35 mm lens, high three-quarter viewpoint over the table so the L section reads on the cut ends, soft daylight plus warm workshop light, physically correct shadows and dull reflections, natural depth of field, real imperfections — mill scale, grinding dust, blue weld heat tint, oil stains, scratches on the table.

PEOPLE: none required; if scale demands it, a pair of gloved hands or a cropped shoulder at the frame edge, never a face, never centred, never covering the steel.

FRAMING: the angle frame fills a large, clearly readable part of the image, its equal legs unmistakable; the workshop stays secondary. No text, signage, labels, logos, stamped markings or numbers in the image.
```

```text
NEGATIF — CGI render, 3D render, plastic or chrome look, over-clean perfect steel, unequal legs, folded thin sheet angle, channel or tube instead of angle, sharp unrounded heel, wrong thickness, painted or galvanised finish, invented markings, any text, numbers, logos, watermark, influencer, presenter, face to camera, selfie, person centred, HDR glow, oversaturation, warped perspective, floating parts, impossible clamps, melted geometry, artefacts, extra fingers
```

### Cornière inégale

`/acier/profiles/corniere-inegale`  — *corrigé par l'audit*

**Scène.** Cornières à ailes inégales en rive d'un quai de chargement : aile longue ancrée à plat sur la dalle béton, aile courte rabattue sur la face verticale pour protéger l'arête.

**Référence.** `/images/produits/acier/profiles/corniere-inegale/studio-corniere-inegale.webp`

**Correction apportée.** Décor dupliqué avec la tôle larmée : escalier métallique extérieur, tarmac mouillé, façade d'entrepôt, lumière grise après la pluie — deux fois la même photo. Référence valide. Scène réécrite sur les usages propres à l'aile inégale dans lib/usages.ts (« rive de dalle », « habillage de rive », une aile qui fixe, l'autre qui retombe) : rive de quai de chargement, où les deux ailes ont chacune leur rôle visible et où le rapport d'ailes se lit au premier plan.

```text
Photorealistic documentary photograph of the edge of a concrete loading dock in an industrial yard in Belgium: unequal-leg steel angles fixed along the whole dock edge, the long leg anchored flat on top of the concrete slab with expansion bolts, the short leg turned down over the vertical face so it caps and protects the edge, rubber dock buffers bolted below, a trailer backed up at the next bay far out of focus, wet tarmac with puddles and tyre marks, a brick and profiled-sheet facade, soft grey daylight.

PRODUCT FIDELITY — ABSOLUTE PRIORITY: the attached reference photograph is the only source of truth for the profile. Reproduce exactly the same L cross-section with one leg clearly longer than the other, the same ratio between the legs, the same thickness, the same rounded root and heel, the same rolled-steel surface texture, colour and finish. The reference shows several sizes of the same family side by side: it defines the section and the material, not the number of pieces in the scene. Do not redraw, equalise the legs, thin, restyle or substitute the profile; never replace it with an equal-leg angle, a folded sheet trim, a channel or a tube; do not add paint, galvanising or markings that are not in the reference; ends must be honest saw-cut ends.

PHOTOGRAPHY: ultra-realistic, full-frame camera, 35 mm lens, low three-quarter viewpoint from yard level running along the dock edge so both legs and one cut end are read at once, soft overcast Northern-European daylight, physically correct shadows under the overhanging leg and dull wet reflections, natural depth of field with the dock line receding, real imperfections — mill scale, light rust film, chipped concrete at the edge, drill dust, grease on the bolt heads, rain water.

PEOPLE: none. No figure is needed at this scale.

FRAMING: the angles and their unequal legs fill a large, clearly readable part of the foreground; the dock and yard stay secondary. No text, signage, labels, logos, stamped markings or numbers in the image.
```

```text
NEGATIF — CGI render, 3D render, plastic or chrome look, over-clean perfect steel, equal legs, folded thin sheet trim, channel or tube instead of angle, sharp unrounded heel, wrong leg ratio, painted yellow or galvanised finish, hazard stripes, invented markings, any text, numbers, logos, truck livery, watermark, influencer, presenter, face to camera, selfie, person centred, HDR glow, oversaturation, warped perspective, floating angles, anchors in mid-air, melted geometry, artefacts
```

### Fer T

`/acier/profiles/fer-t`

**Scène.** Piquets en fer T plantés le long d'une clôture de prairie, en bordure d'un pâturage wallon.

**Référence.** `/images/produits/acier/profiles/fer-t/studio-fer-t.webp`

```text
Photorealistic documentary photograph of a field fence line along a Belgian pasture: T-section steel posts driven into the grassy verge at regular spacing, the flat table of the T facing the field and the perpendicular web standing out, wire strained and clipped against the posts, tall wet grass at the base, a hedge, grazing cows far out of focus, a low horizon and a grey sky with broken clouds.

PRODUCT FIDELITY — ABSOLUTE PRIORITY: the attached reference photograph is the only source of truth for the profile. Reproduce exactly the same T cross-section, with the same table width, the same web height and thickness, the same rounded root, the same rolled-steel surface texture, colour and finish. The reference shows several sizes of the same family side by side: it defines the section and the material, not the number of posts in the scene. Do not redraw, restyle, perforate or substitute the profile; never replace it with a stamped or punched fencing stake, an angle, a channel or a tube; do not add paint, galvanising, holes or markings that are not in the reference; the top ends must be honest saw-cut ends.

PHOTOGRAPHY: ultra-realistic, full-frame camera, 50 mm lens, low viewpoint close to the nearest post so its T section is clearly read, soft overcast Northern-European daylight, physically correct shadows in the grass and dull reflections on the steel, natural depth of field with the fence line receding, real imperfections — mill scale, light surface rust, mud splashes, moss at the base, slightly leaning posts.

PEOPLE: none. No figure is needed at this scale.

FRAMING: the nearest T posts fill a large, clearly readable part of the foreground; the pasture stays secondary. No text, signage, labels, logos, stamped markings or numbers in the image.
```

```text
NEGATIF — CGI render, 3D render, plastic or chrome look, over-clean perfect steel, punched or perforated fence stake, angle or channel or tube instead of T, wrong table-to-web ratio, sharp unrounded root, painted green or galvanised finish, invented holes or markings, any text, numbers, logos, watermark, influencer, presenter, face to camera, selfie, person centred, HDR glow, oversaturation, warped perspective, floating posts, melted geometry, artefacts
```

### Large plat

`/acier/profiles/large-plat`

**Scène.** Platine d'appui en large plat, tracée et percée sur l'établi d'un atelier de construction métallique avant soudure en pied de poteau.

**Référence.** `/images/produits/acier/profiles/large-plat/studio-large-plat.webp`

```text
Photorealistic documentary photograph of a base plate being prepared in a Belgian structural steel workshop: a wide flat steel bar cut to a rectangular plate lying on a heavy workbench, scribed layout lines and centre punch marks on its face, freshly drilled holes with curled swarf around them, a drill bit and a steel rule beside it, further lengths of wide flat bar stacked on a rack behind, a column stub waiting to be welded on, an overhead crane hook high in the background, daylight from a high window mixed with workshop lamps.

PRODUCT FIDELITY — ABSOLUTE PRIORITY: the attached reference photograph is the only source of truth for the product. Reproduce exactly the same rectangular cross-section, clearly wider than it is thick, with the same slightly rounded rolled edges, the same flat faces, the same rolled-steel surface texture, colour and finish. The reference shows several sizes of the same family side by side: it defines the section and the material, not the number of pieces in the scene. Do not redraw, thin, taper, bevel, emboss, restyle or substitute the product; never turn it into thin sheet metal, a chequer plate or a tube; do not add paint, galvanising or markings that are not in the reference; the drilled holes and cut edges must look honestly machined, with saw-cut ends.

PHOTOGRAPHY: ultra-realistic, full-frame camera, 50 mm lens, close three-quarter viewpoint over the bench so the plate thickness is read on its edge, soft daylight plus warm workshop light, physically correct shadows and dull streaky reflections on the flat face, natural depth of field, real imperfections — mill scale, oil film, fine swarf, scratches and dents on the bench.

PEOPLE: none required; if scale demands it, a pair of gloved hands or a cropped shoulder at the frame edge, never a face, never centred, never covering the steel.

FRAMING: the wide flat bar fills a large, clearly readable part of the frame; the workshop stays secondary. No text, signage, labels, logos, stamped markings, scribed characters or numbers in the image.
```

```text
NEGATIF — CGI render, 3D render, plastic or chrome look, mirror-polished steel, over-clean perfect plate, thin sheet metal, chequer or tread plate, tube or angle, wrong width-to-thickness ratio, bevelled or chamfered edges, painted or galvanised finish, invented stamped markings, dimension lines, any text, numbers, logos, watermark, influencer, presenter, face to camera, selfie, person centred, HDR glow, oversaturation, warped perspective, floating tools, melted geometry, artefacts, extra fingers
```

### Plat

`/acier/profiles/plat`

**Scène.** Garde-corps de mezzanine en cours de montage dans un hall : lisses et traverses en plats acier bruts boulonnées et pointées sur les montants.

**Référence.** `/images/produits/acier/profiles/plat/studio-plat.webp`

```text
Photorealistic documentary photograph of a mezzanine guard rail being installed inside a Belgian workshop hall: flat steel bars used as the top rail and the horizontal intermediate rails, bolted and tack-welded flat against upright posts along the edge of a steel mezzanine, one bar still clamped in position waiting to be welded, the hall floor and stacked material visible below through the opening, daylight from roof lights and a bare industrial lamp.

PRODUCT FIDELITY — ABSOLUTE PRIORITY: the attached reference photograph is the only source of truth for the product. Reproduce exactly the same rectangular cross-section, the same width-to-thickness proportion, the same slightly rounded rolled edges, the same flat faces, the same rolled-steel surface texture, colour and finish. The reference shows several sizes of the same family side by side: it defines the section and the material, not the number of pieces in the scene. Do not redraw, twist, taper, emboss, restyle or substitute the product; never replace it with a tube, an angle, a round bar or thin folded sheet; do not add paint, galvanising or markings that are not in the reference; cut ends must be honest saw-cut ends.

PHOTOGRAPHY: ultra-realistic, full-frame camera, 35 mm lens, three-quarter viewpoint running along the rail so both the flat face and the narrow edge are read, mixed daylight and industrial lamp light, physically correct shadows and dull elongated reflections on the flats, natural depth of field, real imperfections — mill scale, blue weld heat tint, grinder marks, dust, fingerprints, oil.

PEOPLE: none required; if scale demands it, one fitter small, secondary, cropped or from behind, never centred, never facing the camera, never hiding the steel.

FRAMING: the flat bars fill a large, clearly readable part of the frame, their rectangular section unmistakable; the hall stays secondary. No text, signage, labels, logos, stamped markings or numbers in the image.
```

```text
NEGATIF — CGI render, 3D render, plastic or chrome look, mirror-polished steel, over-clean perfect bars, round bar, tube, angle, folded thin sheet, wrong width-to-thickness ratio, twisted or wavy bar, painted or galvanised finish, invented markings, any text, numbers, logos, watermark, influencer, presenter, face to camera, selfie, person centred, HDR glow, lens flare, oversaturation, warped perspective, floating rails, melted geometry, artefacts
```

### Rond plein

`/acier/profiles/rond-plein`  — *corrigé par l'audit*

**Scène.** Tirants en ronds lisses montés en croix de contreventement dans la travée d'extrémité d'une grange agricole en service.

**Référence.** `/images/produits/acier/profiles/rond-plein/studio-rond-plein.webp`

**Correction apportée.** Décor dupliqué : intérieur de hangar en construction avec pannes, pignon ouvert et champs belges au fond — c'est déjà le décor du treillis à dépassants. Référence valide. L'usage retenu (« tirants et entretoises ») est le bon, donc seul le lieu change : une grange agricole en service, lumière chaude rasante, matière ancienne. Le produit gagne au passage un fond sombre qui détache le filé spéculaire du rond lisse, seul indice qui le distingue du rond à béton.

```text
Photorealistic documentary photograph of the end bay of a working farm barn in Belgium: two smooth solid round steel rods crossing diagonally as bracing between the frame uprights, each rod threaded at its ends into a tensioning fitting and anchored to a gusset plate, the rods straight and taut, straw bales stacked below them, an old tractor and feed sacks at the side, timber and steel structure darkened by years of use, low afternoon light entering through the open side of the barn.

PRODUCT FIDELITY — ABSOLUTE PRIORITY: the attached reference photograph is the only source of truth for the bar. Reproduce exactly the same smooth circular cross-section, perfectly plain with no ribs or crenellations, the same constant diameter along its length, the same rolled-steel surface texture, colour and finish. The reference shows several sizes of the same family side by side: it defines the section and the material, not the number of rods in the scene. Do not redraw, taper, bend, hollow out, restyle or substitute the bar; never turn it into a ribbed reinforcing bar, a tube, a cable or a chain; do not add paint, galvanising or markings that are not in the reference; ends must look honestly machined.

PHOTOGRAPHY: ultra-realistic, full-frame camera, 35 mm lens, low three-quarter angle looking up into the braced bay, warm raking late-afternoon daylight against the dark interior, physically correct shadows and one narrow continuous specular highlight running along each round rod, natural depth of field, real imperfections — mill scale, light rust film, grease near the threads, straw dust and dust motes in the light beam, cobwebs on the structure.

PEOPLE: none. No figure is needed at this scale.

FRAMING: the crossing rods fill a large, clearly readable part of the frame, their round section unmistakable; the barn stays secondary. No text, signage, labels, logos, stamped markings or numbers in the image.
```

```text
NEGATIF — CGI render, 3D render, plastic or chrome look, over-clean perfect steel, ribbed or crenellated reinforcing bar, hollow tube, wire rope, cable, chain, tapered or sagging rod, square section, painted or galvanised finish, invented markings, any text, numbers, logos, tractor branding, watermark, influencer, presenter, face to camera, selfie, person centred, HDR glow, lens flare, godray overload, oversaturation, warped perspective, floating rods, impossible anchorage, melted geometry, artefacts
```

### Tôle corten

`/acier/toles/tole-corten`  — *corrigé par l'audit*

**Scène.** Jardinières et bordures paysagères en tôle auto-patinable dans un jardin belge, posées la saison précédente, plantations installées.

**Référence.** `/images/produits/acier/toles/tole-corten/studio-tole-corten.webp`

**Correction apportée.** Deux fautes. Fidélité d'abord : j'ai ouvert la référence, elle montre une tôle DÉJÀ patinée, brun chaud finement marbré — or le prompt interdisait « d'ajouter la moindre patine », ce qui pousse le modèle vers un acier brut bleu-gris, exactement le contraire de l'image qui fait foi. La consigne est retournée : reproduire ce brun-là, sans le pousser vers l'orange ni le ramener au métal nu. Ensuite décor : « brise-vue » doublonnait avec le claustra en tôle perforée ; la scène est recentrée sur jardinières et bordures paysagères, et posée une saison plus tôt pour que la patine de la référence soit cohérente avec le chantier montré. Le mot de marque déposée n'apparaît pas dans le prompt (« weathering steel »), c'était déjà correct.

```text
Photorealistic documentary photograph of a landscaped garden in Belgium: flat weathering-steel plates used as the sides of a raised planter bed and as a low edging strip separating a gravel path from a mown lawn, the plates standing vertically with clean straight edges and slim gaps at the corners, ornamental grasses and perennials well established and spilling over the top edge, a young multi-stem tree, a stone terrace and a brick house with large glazing out of focus, soft overcast Northern-European daylight after rain.

PRODUCT FIDELITY — ABSOLUTE PRIORITY: the attached reference photograph is the only source of truth for the plate. It shows an evenly mottled warm brown patinated surface: reproduce that exact colour, that exact fine mottling and that matt finish, nothing more and nothing less. Do not return the plate to bare blue-grey mill-scale steel, do not deepen it into bright orange corrosion, do not add rust streaks, blotches, pitting, flaking or run-off stains on the gravel, the lawn or the paving. Reproduce the same flat sheet geometry and the same apparent thickness read at the edges. Do not redraw, corrugate, perforate, emboss, restyle or substitute the plate; simple straight folded corners are allowed for the planter and nothing else; do not add paint, coating, laser-cut patterns or markings that are not in the reference; cut edges must look honestly sheared.

PHOTOGRAPHY: ultra-realistic, full-frame camera, 35 mm lens, slightly low three-quarter viewpoint so one plate edge shows its thickness against the planting, soft diffuse daylight, physically correct soft shadows and matt reflections, natural depth of field, real imperfections — water droplets on the surface, soil marks at the base, a fallen leaf caught against the edging, uneven gravel.

PEOPLE: none. No figure is needed at this scale.

FRAMING: the steel plates fill a large, clearly readable part of the frame; the garden stays secondary. No text, signage, labels, logos, stamped markings or numbers in the image.
```

```text
NEGATIF — CGI render, 3D render, architectural visualisation, plastic or lacquered surface, over-clean perfect panel, bare mill-scale steel, unpatinated blue-grey plate, bright orange corrosion, deepened or accelerated patina, rust streaks, rust run-off stains on gravel or paving, flaking scale, corrugated or profiled sheet, laser-cut decorative pattern, perforations, painted finish, embossed texture, invented markings, any text, numbers, logos, watermark, influencer, presenter, face to camera, selfie, person centred, HDR glow, oversaturation, warped perspective, floating panels, melted geometry, artefacts
```

### Tôle galvanisée

`/acier/toles/tole-galvanisee`  — *corrigé par l'audit*

**Scène.** Habillage d'un local technique extérieur : panneaux pliés en tôle galvanisée vissés sur une ossature, à l'arrière d'un atelier.

**Référence.** `/images/produits/acier/toles/tole-galvanisee/studio-tole-galvanisee.webp`

**Correction apportée.** Fidélité contredite par la référence, que j'ai ouverte : le zinc y est gris argent, finement et régulièrement moucheté, mat — il n'y a pas de grandes fleurs de cristallisation. Or le prompt exigeait « its characteristic spangle pattern » et le négatif interdisait « missing spangle texture » : les deux poussaient le modèle à inventer des cristaux absents de l'image qui fait foi. Consignes réécrites sur la texture réellement visible. Le reste (décor de local technique, unique dans la gamme, tranche nue visible à la coupe conforme à lib/usages.ts, réalisme, interdits) était bon.

```text
Photorealistic documentary photograph of an outdoor plant enclosure being clad behind a Belgian workshop building: folded galvanised steel sheet panels screwed onto a light steel framework to box in pipework and a ventilation unit, one panel still leaning against the wall waiting to be fitted, its sheared edge showing the bare steel core, drill swarf and screws on the concrete apron, weeds at the base of a brick wall, a grey sky.

PRODUCT FIDELITY — ABSOLUTE PRIORITY: the attached reference photograph is the only source of truth for the sheet. Reproduce exactly the same flat sheet geometry, the same apparent thickness at the edges, and above all the same zinc surface as in the reference: a silvery grey, finely and evenly mottled, matt to semi-matt coating, with no large crystalline spangle flowers, no mirror brightness, no blue, golden or iridescent tint. Do not redraw, corrugate, profile, perforate, emboss, restyle or substitute the sheet; simple straight folds are allowed for the cladding, everything else must stay identical; do not add paint, powder coating, plastic film or markings that are not in the reference; cut edges must look honestly sheared, with the bare steel core visible on the cut.

PHOTOGRAPHY: ultra-realistic, full-frame camera, 35 mm lens, three-quarter viewpoint so both a flat face and a folded edge are read, soft overcast Northern-European daylight, physically correct shadows and the soft, slightly mottled semi-matt reflection typical of this zinc surface, natural depth of field, real imperfections — fingerprints, dust, a faint white oxidation bloom, scratches from handling, slight panel waviness.

PEOPLE: none required; if scale demands it, one fitter small, secondary, cropped or from behind, never centred, never facing the camera, never hiding the panels.

FRAMING: the galvanised panels fill a large, clearly readable part of the frame; the yard stays secondary. No text, signage, labels, logos, stamped markings or numbers in the image.
```

```text
NEGATIF — CGI render, 3D render, plastic or chrome look, mirror-polished metal, chrome-bright zinc, large crystalline spangle flowers, invented crystal pattern, over-clean perfect panel, corrugated or profiled sheet, perforations, embossed pattern, painted or powder-coated colour, rusted surface, blue, golden or iridescent tint, invented markings, any text, numbers, logos, watermark, influencer, presenter, face to camera, selfie, person centred, HDR glow, blown highlights, oversaturation, warped perspective, floating panels, melted geometry, artefacts
```

### Tôle laminée à chaud

`/acier/toles/tole-laminee-a-chaud`  — *corrigé par l'audit*

**Scène.** Benne mécano-soudée en cours de fabrication dans un atelier : panneaux en tôle brute calaminée assemblés et pointés sur un gabarit.

**Référence.** `/images/produits/acier/toles/tole-laminee-a-chaud/studio-tole-laminee-a-chaud.webp`

**Correction apportée.** Deux corrections. Couleur : la référence ouverte montre un gris sombre neutre légèrement marbré ; le prompt demandait « dark blue-grey mill scale », teinte qui risque de sortir franchement bleutée et qui contredit la règle de fidélité colorimétrique. Formulation : « sparks absent » dans la partie positive nomme les étincelles là où le modèle les lit comme un élément de scène ; déplacé en négatif. Le reste (benne mécano-soudée, conforme à l'usage « cuves et bennes », atelier différencié des trois autres par le gabarit et le pont roulant) est conservé.

```text
Photorealistic documentary photograph of a steel skip body being fabricated in a Belgian metal fabrication workshop: flat hot-rolled steel sheets cut to shape, stood on a jig and tacked together to form the sides and floor of the container, weld beads running along the seams, a corner reinforcement clamped in place, a welding torch and cables resting on the shop floor with the arc off, daylight from a high window mixing with overhead lamps, material racks and an overhead crane hook in the background.

PRODUCT FIDELITY — ABSOLUTE PRIORITY: the attached reference photograph is the only source of truth for the sheet. Reproduce exactly the same flat sheet geometry, the same apparent thickness at the edges, and the same surface as in the reference: a dark, neutral grey mill-scale finish, slightly uneven and matt, with no blue, brown or metallic-blue cast and no shine. Do not redraw, corrugate, profile, perforate, emboss, polish, restyle or substitute the sheet; do not add paint, primer, galvanising or markings that are not in the reference; cut edges must look honestly flame-cut or sheared.

PHOTOGRAPHY: ultra-realistic, full-frame camera, 35 mm lens, three-quarter viewpoint so a sheet edge reveals its thickness, mixed daylight and warm workshop light, physically correct soft shadows and low matt reflections on the scale, natural depth of field, real imperfections — mill scale flaking, grinder marks, blue heat tint confined to the weld seams, chalk marks smeared, oil stains and dust.

PEOPLE: none required; if scale demands it, one welder small, secondary, cropped or from behind, never centred, never facing the camera, never hiding the steel.

FRAMING: the raw steel sheets fill a large, clearly readable part of the frame; the workshop stays secondary. No text, signage, labels, logos, stamped markings or numbers in the image.
```

```text
NEGATIF — CGI render, 3D render, plastic or chrome look, mirror-polished or shiny steel, over-clean perfect sheet, blue or brown tinted steel, galvanised spangle, painted or primed surface, corrugated or profiled sheet, perforations, chequer pattern, wrong thickness, invented markings, any text, numbers, logos, watermark, influencer, presenter, face to camera, selfie, person centred, welding sparks, arc light, welding glare, HDR glow, oversaturation, warped perspective, floating panels, melted geometry, artefacts
```

### Tôle laminée à froid

`/acier/toles/tole-laminee-a-froid`  — *corrigé par l'audit*

**Scène.** Atelier de tôlerie fine : capots pliés en tôle laminée à froid posés sur tréteaux, l'un déjà monté sur le bâti d'une machine.

**Référence.** `/images/produits/acier/toles/tole-laminee-a-froid/studio-tole-laminee-a-froid.webp`

**Correction apportée.** Contradiction interne sur la fidélité : la scène ajoutait « a protective film peeled back at one corner » alors que le même prompt interdit d'ajouter un film ou un revêtement — et un film plastique bleuté est justement l'artefact qui fait basculer la tôle vers le rendu plastique proscrit. Retiré. Teinte ajustée aussi : la référence ouverte est un gris moyen satiné uniforme, pas un « light-grey ». Le reste (atelier de tôlerie fine, usage « capotages et habillages », pliages nets, mains gantées hors centre) est conservé.

```text
Photorealistic documentary photograph of sheet-metal covers being made in a small Belgian sheet-metal shop: thin cold-rolled steel panels with crisp press-brake folds resting on trestles next to a press brake, one finished cover already fitted onto a machine frame with countersunk screws, a deburring tool and a steel rule on the bench, daylight from a window plus neutral workshop lighting.

PRODUCT FIDELITY — ABSOLUTE PRIORITY: the attached reference photograph is the only source of truth for the sheet. Reproduce exactly the same flat sheet geometry, the same thin apparent thickness at the edges, and the same surface as in the reference: a smooth, even, untextured mid-grey steel with a soft satin sheen, bare and uncoated. Do not redraw, corrugate, profile, perforate, emboss, texture, polish to a mirror, restyle or substitute the sheet; clean straight folds are allowed for the covers, nothing else; do not add paint, powder coating, galvanising, protective plastic film or markings that are not in the reference; cut edges must look honestly sheared and deburred.

PHOTOGRAPHY: ultra-realistic, full-frame camera, 50 mm lens, three-quarter viewpoint so a folded edge reveals the thin section, soft even daylight, physically correct shadows and the soft satin sheen typical of cold-rolled steel, natural depth of field, real imperfections — fingerprints, faint handling scratches, a slight oil film, fine dust, a small dent at one corner.

PEOPLE: none required; if scale demands it, a pair of gloved hands or a cropped shoulder at the frame edge, never a face, never centred, never covering the steel.

FRAMING: the cold-rolled panels fill a large, clearly readable part of the frame; the workshop stays secondary. No text, signage, labels, logos, stamped markings or numbers in the image.
```

```text
NEGATIF — CGI render, 3D render, plastic or chrome look, mirror-polished metal, protective plastic film, blue or coloured film, over-clean flawless panel, thick plate, mill scale, rust, galvanised spangle, brushed stainless grain, corrugated or profiled sheet, perforations, painted or powder-coated colour, invented markings, any text, numbers, logos, watermark, influencer, presenter, face to camera, selfie, person centred, HDR glow, blown highlights, oversaturation, warped perspective, floating panels, melted geometry, artefacts, extra fingers
```

### Tôle larmée

`/acier/toles/tole-larmee`  — *corrigé par l'audit*

**Scène.** Escalier extérieur d'entrepôt : marches et palier en tôle larmée, sol mouillé après la pluie.

**Référence.** `/images/produits/acier/toles/tole-larmee/studio-tole-larmee.webp`

**Correction apportée.** Faute de fidélité majeure : le prompt décrivait « the raised teardrop pattern », or la référence ouverte porte des bossages RONDS, petites pastilles en relief réparties en quadrillage régulier — pas le motif en larmes/amandes. Le prompt aurait fait produire une tôle qui n'est pas celle que vend l'entreprise. Motif redécrit et motifs concurrents (larme, diamant, cinq barres) passés en négatif. Décor conservé (escalier extérieur d'entrepôt, usage « marches d'escalier ») : il ne doublonne plus depuis que la cornière inégale a quitté l'escalier.

```text
Photorealistic documentary photograph of an external steel staircase on the side of a warehouse in Belgium: the treads and the upper landing formed from raised-pattern steel floor plate, bolted onto the stringers, the relief catching the light, a simple steel handrail at the side, wet tarmac and puddles at the foot of the stairs, a brick and profiled-sheet facade behind, grey daylight just after rain.

PRODUCT FIDELITY — ABSOLUTE PRIORITY: the attached reference photograph is the only source of truth for the plate. Its pattern is made of small ROUND raised studs laid out in a regular grid across the whole sheet: reproduce that exact stud shape, that exact grid spacing and alignment, that same low relief and that same density, on the same flat base plate, with the same apparent thickness at the edges, the same steel surface, colour and finish. Do not redraw, rescale, reorient, randomise or simplify the pattern; never replace it with an elongated teardrop or almond bar pattern, a diamond or lozenge pattern, a five-bar pattern, diamond mesh, open grating or perforations. Do not bend, corrugate or restyle the plate beyond a simple folded nosing; do not add paint, galvanising or markings that are not in the reference; cut edges must look honestly sheared.

PHOTOGRAPHY: ultra-realistic, full-frame camera, 35 mm lens, low three-quarter viewpoint from the foot of the stairs so several treads and the relief read clearly, soft overcast Northern-European daylight, physically correct shadows in the relief and wet specular highlights on top of the studs, natural depth of field, real imperfections — worn shiny patches where feet pass, a rust film at the edges, grit and water droplets between the studs.

PEOPLE: none. No figure is needed at this scale.

FRAMING: the patterned treads fill a large, clearly readable part of the foreground; the warehouse stays secondary. No text, signage, labels, logos, stamped markings or numbers in the image.
```

```text
NEGATIF — CGI render, 3D render, plastic or rubber look, over-clean perfect plate, smooth flat plate without pattern, teardrop pattern, almond or lens-shaped raised bars, diamond or lozenge pattern, five-bar pattern, diamond mesh, open grating, perforated sheet, rescaled or misaligned relief, irregular stud spacing, painted or galvanised finish, invented markings, any text, numbers, logos, watermark, influencer, presenter, face to camera, selfie, person centred, HDR glow, oversaturation, tiling or repeating artefacts, moiré, warped perspective, floating steps, melted geometry
```

### Tôle perforée

`/acier/toles/tole-perforee`

**Scène.** Claustra en tôle perforée fermant une terrasse d'immeuble contemporain, la lumière traversant les perforations.

**Référence.** `/images/produits/acier/toles/tole-perforee/studio-tole-perforee.webp`

```text
Photorealistic documentary photograph of a perforated steel screen on a contemporary residential building in Belgium: flat perforated steel panels fixed in a slim frame as a privacy screen at the edge of a terrace, late-afternoon light passing through the holes and projecting a pattern of small dots onto the concrete floor and the wall behind, planters and a glazed sliding door partially visible through the screen, brick and concrete architecture, a pale northern sky.

PRODUCT FIDELITY — ABSOLUTE PRIORITY: the attached reference photograph is the only source of truth for the panel. Its perforation is made of small ROUND holes in a regular staggered grid covering the whole sheet: reproduce that exact hole shape, the same hole size relative to the sheet, the same pitch, the same staggering, the same open area and the same solid margin at the panel edges, on the same flat sheet with the same apparent thickness, the same bare dark steel surface, colour and finish. Do not redraw, rescale, rotate, randomise, densify or simplify the perforation; do not replace it with square or slotted holes, expanded metal, woven mesh, welded grid or laser-cut decorative motifs; do not corrugate, emboss or restyle the sheet; do not add paint, powder coating or galvanising that is not in the reference, and do not let the warm light read as a lacquered colour; cut edges must look honestly sheared.

PHOTOGRAPHY: ultra-realistic, full-frame camera, 35 mm lens, three-quarter viewpoint so the screen is seen both face-on and edge-on, warm low daylight with physically correct shadows, real light transmission through every hole, natural depth of field, real imperfections — dust and a few raindrops on the surface, slight panel waviness, fingerprints near the frame.

PEOPLE: none. No figure is needed at this scale.

FRAMING: the perforated panel fills a large, clearly readable part of the frame; the terrace stays secondary. No text, signage, labels, logos, stamped markings or numbers in the image.
```

```text
NEGATIF — CGI render, 3D render, architectural visualisation, plastic look, over-clean perfect panel, expanded metal, woven mesh, welded grid, laser-cut decorative pattern, square or slotted holes, holes of the wrong size, random or irregular hole spacing, blocked or filled holes, moiré and aliasing artefacts, corrugated sheet, painted or powder-coated colour, invented markings, any text, numbers, logos, watermark, influencer, presenter, face to camera, selfie, person centred, HDR glow, oversaturation, warped perspective, floating panels, melted geometry
```

### Tôle quarto

`/acier/toles/tole-quarto`

**Scène.** Platine d'ancrage en tôle forte boulonnée sur un massif béton, en pied de structure sur un site industriel.

**Référence.** `/images/produits/acier/toles/tole-quarto/studio-tole-quarto.webp`

```text
Photorealistic documentary photograph of a heavy anchor plate at the foot of a steel structure on an industrial site in Belgium: a thick heavy steel plate sitting on a concrete foundation block, bolted down by large anchor bolts with nuts and washers, levelling shims under one edge, a steel column welded onto the plate above, fresh grout at the perimeter, gravel and tyre tracks around the base, other foundation blocks receding into the yard, grey overcast light.

PRODUCT FIDELITY — ABSOLUTE PRIORITY: the attached reference photograph is the only source of truth for the plate. Reproduce exactly the same flat plate geometry with its clearly substantial thickness read on the edge, the same edge character, the same heavy-plate surface texture, colour and finish as in the reference. Do not redraw, thin down, bevel, chamfer, emboss, corrugate, perforate, restyle or substitute the plate; never turn it into thin sheet or chequer plate; do not add paint, galvanising or markings that are not in the reference; drilled holes and cut edges must look honestly machined or flame-cut, with a visible cut face.

PHOTOGRAPHY: ultra-realistic, full-frame camera, 35 mm lens, low viewpoint close to ground level so the plate thickness is unmistakable against the concrete, soft overcast Northern-European daylight, physically correct shadows under the plate and dull matt reflections on the top face, natural depth of field, real imperfections — mill scale, light rust film, grout smears, grease on the bolts, dust and grit.

PEOPLE: none. No figure is needed at this scale.

FRAMING: the thick plate and its bolted connection fill a large, clearly readable part of the foreground; the site stays secondary. No text, signage, labels, logos, stamped markings or numbers in the image.
```

```text
NEGATIF — CGI render, 3D render, plastic or chrome look, mirror-polished steel, over-clean perfect plate, thin sheet metal, chequer or tread plate, bevelled or chamfered edges, wrong thickness, painted or galvanised finish, invented stamped markings, any text, numbers, logos, watermark, influencer, presenter, face to camera, selfie, person centred, HDR glow, oversaturation, warped perspective, floating plate, bolts in mid-air, melted geometry, artefacts
```

### Tube carré

`/acier/tubes/tube-carre`

**Scène.** Ossature de carport en tubes carrés, fraîchement montée dans l'allée d'une maison belge.

**Référence.** `/images/produits/acier/tubes/tube-carre/studio-tube-carre.webp`

```text
Photorealistic documentary photograph of a carport frame just erected beside a Belgian family house: square hollow steel tubes forming four uprights and the rectangular roof frame, welded at the corners and bolted to concrete pads in the paved driveway, cross members spanning the top waiting for the roof covering, a cordless drill and offcuts on the paving, a hedge, a brick facade and a grey sky with broken clouds behind.

PRODUCT FIDELITY — ABSOLUTE PRIORITY: the attached reference photograph is the only source of truth for the tube. Reproduce exactly the same square hollow cross-section, the same corner radius, the same wall thickness visible at the cut ends, the same flat faces, the same steel surface texture, colour and finish. The reference shows several sizes of the same family side by side: it defines the section and the material, not the number of pieces in the scene. Do not redraw, taper, round, fill, restyle or substitute the tube; never turn it into a solid bar, a round tube or a rectangular tube; do not add paint, powder coating, galvanising or markings that are not in the reference; cut ends must be honest saw-cut ends showing the wall thickness.

PHOTOGRAPHY: ultra-realistic, full-frame camera, 35 mm lens, slightly low three-quarter viewpoint so an open tube end shows the wall thickness, soft overcast Northern-European daylight, physically correct shadows on the paving and dull reflections along the flat faces, natural depth of field, real imperfections — mill scale, light rust film, blue weld heat tint at the joints, grinder marks, dust and leaves on the paving.

PEOPLE: none required; if scale demands it, one fitter small, secondary, cropped or from behind, never centred, never facing the camera, never hiding the frame.

FRAMING: the square tubes fill a large, clearly readable part of the frame; the house and driveway stay secondary. No text, signage, labels, logos, stamped markings or numbers in the image.
```

```text
NEGATIF — CGI render, 3D render, architectural visualisation, plastic or chrome look, over-clean perfect steel, solid bar, round tube, rectangular tube instead of square, wrong corner radius, wrong wall thickness, closed or capped ends hiding the section, painted or powder-coated colour, galvanised finish, invented markings, any text, numbers, logos, number plates, watermark, influencer, presenter, face to camera, selfie, person centred, HDR glow, oversaturation, warped perspective, floating frame, melted geometry, artefacts
```

### Tube rectangulaire

`/acier/tubes/tube-rectangulaire`  — *corrigé par l'audit*

**Scène.** Ossature secondaire de bardage : traverses en tubes rectangulaires fixées horizontalement sur une façade, grande dimension dans le sens de la flexion, avant la pose du parement.

**Référence.** `/images/produits/acier/tubes/tube-rectangulaire/studio-tube-rectangulaire.webp`

**Correction apportée.** Scène en contradiction avec l'usage validé : le prompt plaçait les traverses « their wider face against the brackets », donc grande dimension à plat, alors que lib/usages.ts dit qu'on oriente ce tube grande dimension dans le sens de la flexion — et, accessoirement, cette pose écrase la lecture de la section rectangulaire, seul signe qui le distingue du tube carré. Orientation corrigée, et un bout de tube ouvert ramené face caméra pour que le rapport des côtés et l'épaisseur de paroi soient prouvés dans l'image. La ligne PEOPLE, incomplète, reçoit l'interdiction du face caméra comme les autres. Référence valide.

```text
Photorealistic documentary photograph of a cladding support framework on the facade of a light industrial building in Belgium: rectangular hollow steel tubes fixed horizontally as rails across the wall, each rail set on edge with its long side vertical so the deeper dimension takes the bending, bolted to short brackets anchored to the blockwork, the rails at regular spacing running away in perspective, the nearest rail cut short so its open end faces the camera and shows the rectangular section and the wall thickness, the first cladding panels already fixed at the far end of the wall, a mobile scaffold tower, a grey overcast sky.

PRODUCT FIDELITY — ABSOLUTE PRIORITY: the attached reference photograph is the only source of truth for the tube. Reproduce exactly the same rectangular hollow cross-section with one side clearly longer than the other, the same side ratio, the same corner radius, the same wall thickness visible at the cut ends, the same steel surface texture, colour and finish. The reference shows several sizes of the same family side by side: it defines the section and the material, not the number of pieces in the scene. Do not redraw, square it up, taper, fill, restyle or substitute the tube; never turn it into a square tube, a solid bar, a channel or a round tube; do not add paint, powder coating, galvanising or markings that are not in the reference; cut ends must be honest saw-cut ends showing the wall thickness.

PHOTOGRAPHY: ultra-realistic, full-frame camera, 35 mm lens, sharp oblique viewpoint along the wall so the rails recede and the nearest open end reads clearly, soft overcast Northern-European daylight, physically correct shadows cast by each rail onto the wall and dull reflections along the faces, natural depth of field, real imperfections — mill scale, light rust film, drill dust, grease on the bolts, mortar splashes on the blockwork.

PEOPLE: none required; if scale demands it, one fitter small, secondary, cropped or from behind, never centred, never facing the camera, never hiding the rails.

FRAMING: the rectangular tubes fill a large, clearly readable part of the frame; the facade stays secondary. No text, signage, labels, logos, stamped markings or numbers in the image.
```

```text
NEGATIF — CGI render, 3D render, architectural visualisation, plastic or chrome look, over-clean perfect steel, square tube instead of rectangular, round tube, solid bar, open channel, rail laid flat on its wide face, wrong side ratio, wrong corner radius, wrong wall thickness, capped ends hiding the section, painted or powder-coated colour, galvanised finish, invented markings, any text, numbers, logos, watermark, influencer, presenter, face to camera, selfie, person centred, HDR glow, oversaturation, warped perspective, floating rails, melted geometry, artefacts
```

### Tube rond

`/acier/tubes/tube-rond`

**Scène.** Main courante et poteaux en tubes ronds le long d'une rampe d'accès en béton, à l'entrée d'un bâtiment.

**Référence.** `/images/produits/acier/tubes/tube-rond/studio-tube-rond.webp`

```text
Photorealistic documentary photograph of a handrail along a concrete access ramp at the entrance of a public building in Belgium: round hollow steel tubes forming the continuous top rail and the vertical posts, the rail bent smoothly at the change of slope, posts anchored through small base plates into the concrete, a brushed concrete ramp surface, brick and glass entrance behind, wet ground and soft grey daylight.

PRODUCT FIDELITY — ABSOLUTE PRIORITY: the attached reference photograph is the only source of truth for the tube. Reproduce exactly the same round hollow cross-section, the same constant diameter, the same wall thickness visible at any open end, the same smooth cylindrical surface texture, colour and finish. The reference shows several sizes of the same family side by side: it defines the section and the material, not the number of pieces in the scene. Do not redraw, taper, flatten, fill, restyle or substitute the tube; never turn it into a solid round bar, a square tube or a polished stainless rail; do not add paint, powder coating, galvanising or markings that are not in the reference; bends must keep a constant section, cut ends must be honest saw-cut ends.

PHOTOGRAPHY: ultra-realistic, full-frame camera, 35 mm lens, low three-quarter viewpoint following the rail up the ramp, soft overcast Northern-European daylight, physically correct shadows on the concrete and a narrow continuous specular highlight running along the cylindrical rail, natural depth of field, real imperfections — mill scale, light rust film, weld seams at the joints, hand-worn patches on the rail, water droplets.

PEOPLE: none. No figure is needed at this scale.

FRAMING: the round tube rail fills a large, clearly readable part of the frame; the building stays secondary. No text, signage, labels, logos, stamped markings or numbers in the image.
```

```text
NEGATIF — CGI render, 3D render, architectural visualisation, plastic or chrome look, mirror-polished stainless rail, over-clean perfect steel, solid round bar, square or oval tube, tapered or flattened tube, kinked bend, wrong wall thickness, painted or powder-coated colour, galvanised finish, invented markings, any text, numbers, logos, watermark, influencer, presenter, face to camera, selfie, person centred, HDR glow, lens flare, oversaturation, warped perspective, floating rail, melted geometry, artefacts
```

### Cornière égale

`/aluminium/profiles/corniere-egale`  — *corrigé par l'audit*

**Scène.** Atelier de menuiserie wallon : les cornieres sont vissees en protection d'arete sur les angles verticaux d'une caisse de transport en contreplaque, en cours de montage sur l'etabli.

**Référence.** `/images/produits/aluminium/profiles/corniere-egale/studio-aluminium-corniere-egale.webp`

**Correction apportée.** Chemin de reference VALIDE (present dans lib/visuels-produits.json cle categories, fichier present sur disque). Scene validee par usages.ts (« renfort d'angle de caisson », « protection d'arete »). Trois defauts : (1) le prompt appelle la reference « photograph » alors que c'est un rendu 3D propre sur fond blanc — rien n'interdit au modele d'en copier la surface parfaite et l'eclairage studio, ce qui produit exactement le CGI que la regle 3 bannit ; (2) verification faite sur l'image : la reference montre TROIS tailles cote a cote — le prompt n'en dit rien de clair, le modele peut aligner trois pieces catalogue dans la scene ; (3) l'inventaire d'outils sur l'etabli reprend la meme formule de mise en scene que 6 autres prompts (piece en rab + outils poses), ce qui homogeneise toute la gamme.

```text
REFERENCE — The attached image is a clean technical studio render of the product on a white background. It is authoritative for the OBJECT ONLY: an equal-leg aluminium angle, two legs of identical width, constant thin wall, crisp outer arris and a small radius on the inner corner, clean square-cut ends, no holes, no coating, plain mill finish in matte satin silver-grey. Reproduce that exactly — same L cross-section, same equal-leg proportion, same wall thickness, same metal, same colour, same finish, same light satin grain. Do not redesign, stylise, thicken, taper, round off or substitute it; do not add ribs, flanges, lips, perforations, paint or anodising it does not have.

WHAT IS NOT SPECIFIED — The reference shows three lengths of the same profile in three sizes, side by side, only to document the section. The number of pieces and their length are not part of the specification: the scene decides them. Never reproduce that catalogue line-up inside the scene.

NOT A STYLE REFERENCE — Copy the object, never the rendering. Do not carry over the white background, the studio lighting, or the flawless computer-generated surface. The output must read as a real photograph taken in a real workshop.

SCENE — A cabinetmaker's workshop in Wallonia, late morning. A birch-plywood transport case sits half-assembled on a scarred wooden bench: lengths of the aluminium angle are screwed down the case's vertical corners as edge protection, countersunk screws sunk flush along one leg. One cut length rests on the bench where the work stopped. Fine sawdust hanging in the light, shavings on the floor, plywood off-cuts stacked against a whitewashed brick wall, daylight through a tall dusty window.

FRAMING — Three-quarter view from standing height, close to the case. One fitted angle runs diagonally through the frame, large and fully sharp, its L-section clearly readable at the cut end. The workshop is legible but secondary and slightly soft.

LIGHT & CAMERA — Natural window light only, no flash. Soft directional daylight, physically coherent contact shadows under the case and under the loose length, real specular roll-off on brushed aluminium, honest perspective from eye level, full-frame camera with a 50 mm lens, moderate aperture, natural shallow depth of field with the product entirely in focus.

MATERIAL TRUTH — Visible workshop reality: faint brush lines in the metal, a light scuff along one leg, a trace of saw burr on a cut end, sawdust settled on the top face. Nothing shiny-new, nothing mirror-polished.

NO TEXT — Nothing written anywhere in the frame: no signage, lettering, numbers, labels, stickers, printed graphics or brand marks, and no markings on the product or on the tools. Every surface that could carry print stays blank.

PEOPLE — Preferably none. At most a joiner's gloved forearm entering at the very edge of the frame, out of focus: never centred, never between the camera and the product, never overlapping or masking the profile. No face, no pose, no eye contact with the camera.
```

```text
NEGATIF — CGI render, 3D render look, ray-traced showroom lighting, studio white background, white cyclorama, catalogue line-up of three sizes side by side, product repeated in a row, plastic or rubbery surface, waxy material, over-smooth flawless object, chrome mirror finish, gold or coloured anodising, powder-coated paint, rust, unequal legs, changed cross-section, extra holes or slots, added ribs or lips, warped or wavy straight edges, bent or melted geometry, floating object, missing contact shadow, influencer, presenter, model posing, face to camera, selfie, TikTok style, person masking the product, distorted hands, extra fingers, text, lettering, numbers, dimension annotations, labels, stickers, watermark, logo, brand mark, signage, HDR halo, oversaturated colour, heavy vignette, lens flare, bokeh balls, tilt-shift, motion blur, fisheye distortion, low resolution, jpeg artefacts
```

### Plat

`/aluminium/profiles/plat`  — *corrigé par l'audit*

**Scène.** Toit d'appentis translucide a l'arriere d'une maison wallonne : les plats en aluminium sont visses le long de chaque chevron et serrent les plaques de couverture, vue prise de dessous.

**Référence.** `/images/produits/aluminium/profiles/plat/studio-aluminium-plat.webp`

**Correction apportée.** Chemin de reference VALIDE. Defaut principal de plausibilite (regle 4) : le plat aluminium sert de « platine et entretoise boulonnee entre poteaux bois et chevrons » — une liaison structurelle de charpente se fait en acier galvanise, jamais en plat aluminium ; un professionnel repere la faute immediatement. Role corrige en « barre de maintien » (serrage de plaques de couverture translucides sur chevrons), usage reel du plat alu et valide par usages.ts. Manquent aussi la clause « la reference est un rendu, pas un modele d'eclairage », la clause trois tailles (verifiee : la reference montre trois plats cote a cote) et la clause anti-texte dans le prompt. Vue prise de dessous sous une couverture translucide : decor et lumiere uniques dans la gamme, la formule « piece en rab sur treteaux » est supprimee.

```text
REFERENCE — The attached image is a clean technical studio render of the product on a white background. It is authoritative for the OBJECT ONLY: a solid aluminium flat bar, rectangular section, clearly wider than it is thick, flat parallel faces, straight square edges with a very slight break, square-cut ends, plain mill finish in matte satin silver-grey. Reproduce it exactly — same rectangular section, same width-to-thickness proportion, same solid (not hollow) body, same metal, same colour, same finish. Do not redesign, taper, curve, hollow out, thicken or substitute it; do not turn it into a tube, an angle, a channel or a sheet. Since the bars are screwed down in this scene, the only added feature may be plain countersunk round holes at the fixing points — nothing else.

WHAT IS NOT SPECIFIED — The reference shows three bars in three sizes, side by side, only to document the section. The number of bars and their length are not part of the specification: the scene decides them. Never reproduce that catalogue line-up inside the scene.

NOT A STYLE REFERENCE — Copy the object, never the rendering. Do not carry over the white background, the studio lighting, or the flawless computer-generated surface. The output must read as a real photograph taken on a real job.

SCENE — A lean-to veranda roof at the back of a red-brick Walloon house, bright overcast day, seen from underneath while standing on the terrace below. Translucent roofing sheets lie across squared timber rafters, and a flat aluminium bar is screwed along each rafter on top of the sheets, clamping them down, with a dark sealing gasket just visible under the bar. The nearest bar runs down the frame towards the eave, where its square-cut end and thin edge are exposed. Diffuse grey Belgian light pours through the translucent sheets, a bare hedge and a tiled roofline visible past the open end.

FRAMING — Low view from directly under the roof, looking up and along the rafter line. The nearest clamping bar crosses the frame large and fully sharp, its wide face lit from above through the sheeting and its narrow edge readable in profile. The veranda structure and the house stay secondary.

LIGHT & CAMERA — Natural overcast daylight only, no flash. Strong soft backlight coming through the translucent roof, the bar reading darker against it with a real reflected sheen along its edge, physically coherent shadow of the bar cast on the sheeting, honest upward perspective, full-frame camera with a 35 mm lens, natural depth of field, the bar entirely sharp and the far end of the roof gently soft.

MATERIAL TRUTH — Honest site condition: fine rolling grain in the metal, a few handling scratches, a bright ring of fresh metal around a drilled hole, a smear of brick dust near a screw, rainwater dried into faint streaks on the sheeting.

NO TEXT — Nothing written anywhere in the frame: no signage, lettering, numbers, labels, stickers, printed film, brand marks or markings on the product, the sheeting or the timber. Every surface that could carry print stays blank.

PEOPLE — None.
```

```text
NEGATIF — CGI render, 3D render look, ray-traced showroom lighting, studio white background, white cyclorama, catalogue line-up of three sizes side by side, product repeated in a row, plastic or rubbery surface, waxy material, over-perfect flawless bar, chrome mirror finish, coloured anodising, painted bar, rust, hollow tube instead of solid bar, angle or channel instead of flat bar, changed section, tapered or curved bar, added flanges or ribs, perforated strip, slotted rail, warped edges, floating object, missing shadow, influencer, presenter, model posing, face to camera, selfie, TikTok style, person masking the product, distorted hands, extra fingers, text, lettering, numbers, dimension annotations, labels, printed protective film, stickers, watermark, logo, brand mark, signage, HDR halo, blown-out highlights, oversaturated colour, heavy vignette, lens flare, bokeh balls, tilt-shift, motion blur, fisheye distortion, low resolution, jpeg artefacts
```

### Profil T

`/aluminium/profiles/profil-t`  — *corrigé par l'audit*

**Scène.** Agencement interieur d'un commerce en renovation, local encore vide : le profil T couvre le joint vertical entre deux grands panneaux muraux, pose en cours, aucune enseigne ni signaletique posee.

**Référence.** `/images/produits/aluminium/profiles/profil-t/studio-aluminium-profil-t.webp`

**Correction apportée.** Chemin de reference VALIDE. Scene validee par usages.ts (« jonction entre deux panneaux », « profil de finition », « travaux d'agencement »). Quatre corrections : (1) clause rendu-pas-photo absente ; (2) clause trois tailles absente (la reference montre trois profils T cote a cote) ; (3) risque texte eleve et mal couvert — un commerce en agencement est l'environnement le plus charge en enseignes et signaletique de toute la gamme : la scene precise maintenant un local vide avant toute pose d'enseigne, toutes surfaces nues ; (4) clause personne incomplete (il manquait « ni visage, ni pose, ni regard camera »). Les panneaux passent du contreplaque au MDF peint : le contreplaque revenait dans trois scenes sur neuf. L'inventaire d'outils est supprime.

```text
REFERENCE — The attached image is a clean technical studio render of the product on a white background. It is authoritative for the OBJECT ONLY: an aluminium T profile, a flat flange on top and a single web perpendicular at its centre, both of similar width, constant thin wall, small fillets at the junction, sharp square-cut ends, plain mill finish in matte satin silver-grey. Reproduce it exactly — same T cross-section, same flange-to-web proportion, same wall thickness, same metal, same colour, same finish. Do not redesign it into an angle, a U, an H or a flat bar, do not widen the web, do not add returns, lips, ribs, screw channels, perforations or coatings, and do not simplify the profile.

WHAT IS NOT SPECIFIED — The reference shows three lengths of the same profile in three sizes, side by side, only to document the section. The number of pieces and their length are not part of the specification: the scene decides them. Never reproduce that catalogue line-up inside the scene.

NOT A STYLE REFERENCE — Copy the object, never the rendering. Do not carry over the white background, the studio lighting, or the flawless computer-generated surface. The output must read as a real photograph taken inside a real building site.

SCENE — The interior of a small shop under renovation in Brussels, early afternoon, the space still completely empty and unfitted. Two large primed MDF wall panels meet on a vertical joint, and the T profile is fitted over that joint, flange flat against the panel faces, web hidden in the gap — a finishing bead that marks the junction. A second length leans against the bare wall a little further along, its cut end towards the camera. Bare screed floor, protective dust sheets bunched at the skirting, daylight raking in through a big empty shopfront window. No fittings, no shelving, no displays, no signage of any kind has been installed yet.

FRAMING — Frontal three-quarter view from standing height, close to the joint. The fitted T runs the full height of the frame, large and razor-sharp; its T-section is clearly readable at the cut end of the leaning length in the foreground. The empty shell reads behind it, secondary.

LIGHT & CAMERA — Daylight only, no flash. Directional window light grazing along the profile to reveal its edge, coherent soft shadow in the panel joint, physically correct highlight running down the flange, true perspective, full-frame camera with a 50 mm lens, natural shallow depth of field, product entirely sharp.

MATERIAL TRUTH — Real building-site texture: faint mill grain, plaster dust settled on the flange, a fingerprint near the top, a small handling scuff, a slightly burred saw cut.

NO TEXT — Nothing written anywhere in the frame: no shop sign, no lettering on the window, no numbers, labels, stickers, printed graphics or brand marks, and no markings on the product or the panels. Every surface that could carry print stays blank.

PEOPLE — Preferably none. At most one fitter far back in the empty room, small, out of focus, turned away: never centred, never between the camera and the product, never overlapping or masking the profile. No face, no pose, no eye contact with the camera.
```

```text
NEGATIF — CGI render, 3D render look, ray-traced showroom lighting, studio white background, white cyclorama, catalogue line-up of three sizes side by side, product repeated in a row, plastic or rubbery surface, waxy material, over-perfect flawless profile, chrome mirror finish, coloured anodising, painted profile, rust, angle profile instead of T, U or H section, inverted or doubled web, added lips or returns, screw channel, perforations, warped or wavy edges, floating object, missing shadow, furnished shop, shelving, displays, merchandise, influencer, presenter, model posing, face to camera, selfie, TikTok style, person masking the product, distorted hands, extra fingers, text, lettering, numbers, dimension annotations, labels, stickers, watermark, logo, brand mark, signage, shop sign, window graphics, price tags, HDR halo, oversaturated colour, heavy vignette, lens flare, bokeh balls, tilt-shift, motion blur, fisheye distortion, low resolution, jpeg artefacts
```

### Profil U

`/aluminium/profiles/profil-u`  — *corrigé par l'audit*

**Scène.** Terrasse d'une maison wallonne : le profil U est enfile en protection de chant sur le chant superieur expose d'un panneau brise-vue en bois plein, pose en cours.

**Référence.** `/images/produits/aluminium/toles/tole-plane/studio-tole-aluminium.webp`

**Correction apportée.** Chemin de reference VALIDE. Usage valide par usages.ts (« protection de chant », « encadrement de panneau »). Defaut de coherence de scene : le prompt decrit un claustra a lames ET « un grand panneau a dos de contreplaque » — un claustra ajoure n'a pas de panneau plein a coiffer, les deux descriptions se contredisent et le modele devra trancher au hasard. Corrige en panneau de bois plein a chant expose, ce qui donne au U quelque chose de reel a enfiler. Manquent aussi la clause rendu-pas-photo et la clause trois tailles (reference a trois U cote a cote). Mise en scene changee de pelouse a terrasse bois et formule « piece en rab + maillet + scie » supprimee ; le contreplaque disparait aussi (il revenait dans trois scenes).

```text
REFERENCE — The attached image is a clean technical studio render of the product on a white background. It is authoritative for the OBJECT ONLY: an aluminium U channel, a flat base with two parallel side walls of equal height rising square from it, an open groove along the whole length, constant thin wall, slightly softened outer arrises, square-cut ends, plain mill finish in matte satin silver-grey. Reproduce it exactly — same U cross-section, same groove width, same wall height and thickness, same metal, same colour, same finish. Do not redesign it into an angle, a closed tube, a C with returned lips or a deeper track; do not add inward lips, ribs, screw ports, drainage slots, perforations or coatings; do not simplify or thicken the walls.

WHAT IS NOT SPECIFIED — The reference shows three lengths of the same channel in three sizes, side by side, only to document the section. The number of pieces and their length are not part of the specification: the scene decides them. Never reproduce that catalogue line-up inside the scene.

NOT A STYLE REFERENCE — Copy the object, never the rendering. Do not carry over the white background, the studio lighting, or the flawless computer-generated surface. The output must read as a real photograph taken in a real garden.

SCENE — A timber terrace behind a Walloon house, bright overcast late afternoon. A solid timber privacy panel has just been stood upright between two posts at the end of the terrace, and the aluminium U channel is pushed over its exposed top edge as capping, protecting the end grain from the rain — pushed fully home along most of the run, standing slightly proud at the far end where the work stopped. Grey timber decking underfoot, a clipped box hedge and a terracotta pot beyond, a brick gable and a flat grey sky behind.

FRAMING — Slightly low three-quarter view along the top edge of the panel, so the open groove and both side walls are clearly visible at the near end. The channel crosses the frame large and fully sharp; terrace and garden stay secondary and gently soft.

LIGHT & CAMERA — Natural diffuse daylight only, no flash. Soft sky light with a real shadow line inside the groove and a contact shadow where the channel meets the timber, believable sheen along the outer walls, honest perspective, full-frame camera with a 50 mm lens, natural depth of field, product fully sharp.

MATERIAL TRUTH — Garden-job realism: fine mill grain, fine scratches from sliding the channel onto the panel, a few rain droplets beaded on the base, a leaf caught against the timber, a lightly burred cut end.

NO TEXT — Nothing written anywhere in the frame: no signage, lettering, numbers, labels, stickers, printed graphics or brand marks, and no markings on the product or the timber. Every surface that could carry print stays blank.

PEOPLE — Preferably none. At most a gloved hand entering low at the very edge of the frame, out of focus: never centred, never between the camera and the product, never overlapping or masking the channel. No face, no pose, no eye contact with the camera.
```

```text
NEGATIF — CGI render, 3D render look, ray-traced showroom lighting, studio white background, white cyclorama, catalogue line-up of three sizes side by side, product repeated in a row, plastic or rubbery surface, waxy material, over-perfect flawless profile, chrome mirror finish, coloured anodising, painted or wood-effect profile, rust, closed tube instead of open U, C profile with returned lips, unequal side walls, added ribs, screw ports, drainage slots or perforations, warped or wavy edges, floating object, missing shadow, slatted openwork screen with nothing to cap, influencer, presenter, model posing, face to camera, selfie, TikTok style, person masking the product, distorted hands, extra fingers, text, lettering, numbers, dimension annotations, labels, stickers, watermark, logo, brand mark, signage, HDR halo, oversaturated colour, heavy vignette, lens flare, bokeh balls, tilt-shift, motion blur, fisheye distortion, low resolution, jpeg artefacts
```

### Tôle plane

`/aluminium/toles/tole-plane`  — *corrigé par l'audit*

**Scène.** Extension contemporaine d'une maison belge : une tole plane en aluminium est presentee sur l'ossature de bardage de la facade avant fixation, en fin de journee.

**Référence.** `/images/produits/aluminium/toles/tole-plane/studio-tole-aluminium.webp`

**Correction apportée.** ATTENTION — la reference d'origine etait bonne, ne pas la confondre avec la ligne precedente : le chemin correct est celui de la tole plane, verifie present dans lib/visuels-produits.json et sur disque. Scene validee par usages.ts (« habillage de facade », premier exemple de la famille). Trois corrections : clause rendu-pas-photo absente (ici le risque est maximal, une tole lisse est ce qui vire le plus facilement au CGI) ; clause personne incomplete (ni visage, ni pose, ni regard camera manquait) ; et la seconde tole sur treteaux avec straightedge, grignoteuse et sachet de fixations reprend la formule de mise en scene commune a sept prompts — supprimee au profit d'un seul panneau presente sur l'ossature. La reference ne montre qu'une seule tole : pas de clause trois tailles ici.

```text
REFERENCE — The attached image is a clean technical studio render of the product on a white background. It is authoritative for the OBJECT ONLY: a plain flat aluminium sheet, rectangular, roughly twice as long as it is wide, smooth unpatterned faces, uniform thin gauge, straight clean-cut edges with square corners, plain mill finish in matte satin silver-grey with a soft even sheen. Reproduce it exactly — same flat rectangular format, same proportion, same thinness, same smooth surface, same metal, same colour, same finish. Do not emboss, stripe, perforate, corrugate, profile, rib or anodise it; do not turn it into a tread plate, a trapezoidal panel or a composite panel; do not make it thick or curl its edges beyond the natural slight flex of a thin sheet held upright.

NOT A STYLE REFERENCE — Copy the object, never the rendering. Do not carry over the white background, the studio lighting, or the flawless computer-generated surface: a real sheet on site is never that perfect. The output must read as a real photograph, not a render.

SCENE — The rear extension of a contemporary Belgian house, clear late afternoon in autumn. A flat aluminium sheet is offered up against the timber batten framework of the façade, resting on two setting blocks and leaning slightly into the wall, ready to be fixed; the run of sheets already fixed to its left shows what the finished cladding will look like. Bare timber battens and dark breather membrane behind, black window frames to one side, a gravel strip and mown lawn in front, low golden light skimming the wall.

FRAMING — Three-quarter view from standing height, close enough that the upright sheet fills most of the frame, fully sharp, its thin edge and square corner clearly readable against the batten frame. The house and garden read behind it, secondary.

LIGHT & CAMERA — Natural daylight only, no flash. Raking low sun plus soft sky fill; the sheet reflects sky and surroundings as a diffuse, physically correct gradient rather than a mirror image; real shadow cast on the battens behind, honest perspective, full-frame camera with a 35 mm lens, natural depth of field, sheet entirely in focus.

MATERIAL TRUTH — Site reality: faint rolling grain, a fingerprint near the edge, a light scratch, a pale streak of dust, and the very slight waviness a thin sheet really has when stood on edge.

NO TEXT — Nothing written anywhere in the frame: no signage, lettering, numbers, labels, stickers, printed protective film, brand marks or markings on the sheet, the membrane or the timber. Every surface that could carry print stays blank.

PEOPLE — Preferably none. At most a fitter's forearm steadying the far edge at the very border of the frame, out of focus: never centred, never between the camera and the product, never overlapping or masking the sheet. No face, no pose, no eye contact with the camera.
```

```text
NEGATIF — CGI render, 3D render look, ray-traced showroom lighting, studio white background, white cyclorama, plastic or rubbery surface, waxy material, over-perfect flawless panel, chrome mirror finish, mirror reflection of a room, coloured anodising, painted or printed sheet, rust, tread plate pattern, embossed or striped surface, corrugated or trapezoidal profile, perforated sheet, composite sandwich panel, thick slab, curled or crumpled sheet, floating object, missing shadow, influencer, presenter, model posing, face to camera, selfie, TikTok style, person masking the product, distorted hands, extra fingers, text, lettering, numbers, dimension annotations, labels, printed protective film, stickers, watermark, logo, brand mark, signage, HDR halo, blown-out specular, oversaturated colour, heavy vignette, lens flare, bokeh balls, tilt-shift, motion blur, fisheye distortion, low resolution, jpeg artefacts
```

### Tôle striée

`/aluminium/toles/tole-striee`  — *corrigé par l'audit*

**Scène.** Cour d'atelier apres la pluie : la tole striee forme le plancher d'une remorque plateau ouverte, hayon rabattu, prete a charger, cadree de sorte qu'aucune plaque n'apparaisse.

**Référence.** `/images/produits/aluminium/toles/tole-striee/studio-tole-aluminium-striee.webp`

**Correction apportée.** Chemin de reference VALIDE. Point important verifie sur l'image elle-meme : le motif en damier de barrettes groupees par CINQ decrit dans le prompt est exact, la description ne trahit pas la reference — aucune correction a faire de ce cote. Scene validee par usages.ts (« fond de remorque »). Restent deux manques : la clause rendu-pas-photo, et la clause personne incomplete (ni visage, ni pose, ni regard camera). Le risque texte est reel et mal couvert : une remorque porte une plaque d'immatriculation — la scene impose maintenant un cadrage ou aucune plaque n'apparait. La reference ne montre qu'une seule tole : pas de clause trois tailles.

```text
REFERENCE — The attached image is a clean technical studio render of the product on a white background. It is authoritative for the OBJECT ONLY: an aluminium chequer plate whose raised pattern is made of short parallel bars grouped in fives, each group set at right angles to the next in a regular chessboard-like layout, raised low and rounded on a smooth flat backing sheet, plain mill finish in matte satin silver-grey, straight cut edges, uniform thin gauge. Reproduce that exact pattern — same bar grouping, same alternating orientation, same pitch and relief height relative to the plate, same metal, same colour, same finish. Do not replace it with a diamond pattern, round studs, a two-bar or single-bar tread, a mesh or a perforated plate; do not change the bar count per group, do not enlarge or shrink the pattern scale, do not smooth it flat.

NOT A STYLE REFERENCE — Copy the object, never the rendering. Do not carry over the white background, the studio lighting, or the flawless computer-generated surface. The output must read as a real photograph of a plate that has been walked on.

SCENE — A workshop yard in Wallonia just after rain, early morning. An open flat-bed trailer stands hitched on wet concrete, its tailgate folded down, the whole deck made of this chequer plate; the raised pattern holds standing water in thin films between the bars, and a ratchet strap and a pair of work gloves lie where they were dropped on the deck. A brick workshop wall with a roller shutter behind, a puddle reflecting a grey sky, damp weeds at the foot of the wall. Frame the trailer from the open deck end so that no number plate is anywhere in view.

FRAMING — Low three-quarter view from the tailgate corner, camera just above deck height, so the pattern runs away in perspective and is large and fully sharp in the near half of the frame. The trailer and yard read clearly but stay secondary.

LIGHT & CAMERA — Natural overcast daylight only, no flash. Soft sky light picking out each raised bar with its own tiny shadow, real wet-surface specular highlights, believable perspective compression, full-frame camera with a 35 mm lens, natural depth of field with the near deck sharp and the far end gently soft.

MATERIAL TRUTH — Genuine working wear: scuffs and boot marks polishing the tops of the bars, grit trapped between them, water droplets, faint scratches near the tailgate hinge, a dull unbuffed sheen.

NO TEXT — Nothing written anywhere in the frame: no number plate, no signage, lettering, numbers, labels, stickers, printed graphics or brand marks, and no markings on the deck, the straps or the shutter. Every surface that could carry print stays blank.

PEOPLE — Preferably none. At most a worker's boot and lower leg stepping onto the deck at the very edge of the frame, out of focus: never centred, never between the camera and the product, never hiding the pattern. No face, no pose, no eye contact with the camera.
```

```text
NEGATIF — CGI render, 3D render look, ray-traced showroom lighting, studio white background, white cyclorama, plastic or rubbery surface, waxy material, over-perfect flawless plate, chrome mirror finish, coloured anodising, painted deck, rust, diamond pattern, round stud pattern, single-bar or two-bar tread, mesh, expanded metal, perforated plate, wrong bar count per group, uniform bar direction, exaggerated or oversized relief, flattened smooth surface, tiling seams, repeated copy-paste texture, warped edges, floating object, missing shadow, influencer, presenter, model posing, face to camera, selfie, TikTok style, person masking the product, distorted hands, extra fingers, text, lettering, numbers, dimension annotations, number plate, registration plate, labels, stickers, watermark, logo, brand mark, signage, HDR halo, oversaturated colour, heavy vignette, lens flare, bokeh balls, tilt-shift, motion blur, fisheye distortion, low resolution, jpeg artefacts
```

### Tube carré

`/aluminium/tubes/tube-carre`  — *corrigé par l'audit*

**Scène.** Hall d'exposition avant l'habillage : l'ossature d'un stand demontable en tubes carres d'aluminium est boulonnee au sol, panneaux encore nus, aucun graphisme pose.

**Référence.** `/images/produits/aluminium/tubes/tube-carre/studio-aluminium-tube-carre.webp`

**Correction apportée.** Chemin de reference VALIDE. La scene est legitime — « structure de stand » figure litteralement dans les exemples valides de usages.ts, donc on la garde plutot que d'inventer un autre decor. Mais elle porte le plus gros risque de la gamme au regard de l'interdit « aucun texte visible » : un hall d'exposition est l'environnement le plus sature d'enseignes, de bandeaux et de logos qui soit, et le prompt d'origine se contentait de « banner text » dans le negatif. Corrige en imposant le moment precis ou il n'y a rien a lire : ossature nue avant habillage, panneaux vierges, hall vide avant montage des graphismes ; la flight case (toujours pochee au nom du prestataire) est retiree. Manquent par ailleurs la clause rendu-pas-photo, la clause trois tailles (la reference montre trois tubes cote a cote) et la clause personne complete.

```text
REFERENCE — The attached image is a clean technical studio render of the product on a white background. It is authoritative for the OBJECT ONLY: a square hollow aluminium tube, four flat faces of equal width, slightly softened outer corners, constant thin wall clearly visible as a fine open square at the cut end, square-cut ends, plain mill finish in matte satin silver-grey. Reproduce it exactly — same square section, same wall thickness, same corner radius, same metal, same colour, same finish. Do not redesign it into a rectangular, round or slotted tube, do not make it solid, do not add T-slots, grooves, ribs, factory perforations or coatings, do not thicken or taper it. Only the plain round holes needed at the bolted joints may appear where the scene requires them.

WHAT IS NOT SPECIFIED — The reference shows three lengths of the same tube in three sizes, side by side, only to document the section. The number of pieces and their length are not part of the specification: the scene decides them. Never reproduce that catalogue line-up inside the scene.

NOT A STYLE REFERENCE — Copy the object, never the rendering. Do not carry over the white background, the studio lighting, or the flawless computer-generated surface. The output must read as a real photograph taken during a real build-up.

SCENE — A demountable exhibition stand being assembled inside a daylit hall in Belgium, morning, well before the fit-out. A base frame of square aluminium tubes is bolted together on the polished concrete floor, two uprights already standing, a corner connector half tightened; three more tubes lie in a loose stack beside an Allen key. The infill panels leaning against the frame are completely bare and unprinted — no graphics have been mounted yet, anywhere in the hall. High north-facing glazing and a pale steel roof structure above, other bare frames far behind, softly out of focus.

FRAMING — Low three-quarter view onto the corner joint, camera near floor height, so one tube runs diagonally across the foreground large and fully sharp with its open square end and wall thickness clearly readable. The hall reads behind it, secondary and soft.

LIGHT & CAMERA — Natural daylight from the roof glazing only, no flash. Soft directional light giving each of the four faces a different value, coherent contact shadows on the concrete, physically correct satin reflections, honest perspective, full-frame camera with a 35 mm lens, natural shallow depth of field, product entirely sharp.

MATERIAL TRUTH — Real handling: fine mill grain, light scratches along the faces, a fingerprint, a few flecks of dust, a faint burr inside a cut end. Nothing mirror-polished.

NO TEXT — Nothing written anywhere in the frame: no banners, no printed panels, no hall signage, no stand numbers, no lettering, labels, stickers, brand marks or markings on the tubes, the panels, the tools or the floor. Every surface that could carry print stays blank.

PEOPLE — Preferably none. At most one fitter kneeling in the background, small, out of focus, turned away: never centred, never between the camera and the product, never overlapping the foreground tube. No face, no pose, no eye contact with the camera.
```

```text
NEGATIF — CGI render, 3D render look, ray-traced showroom lighting, studio white background, white cyclorama, catalogue line-up of three sizes side by side, product repeated in a row, plastic or rubbery surface, waxy material, over-perfect flawless tube, chrome mirror finish, coloured anodising, painted tube, rust, solid bar instead of hollow tube, rectangular or round section, T-slot extrusion, grooved or ribbed profile, factory perforations, thick clumsy wall, invisible wall at cut end, warped or wavy edges, floating object, missing shadow, finished branded stand, printed graphics panels, banners, flight case, crowd, visitors, influencer, presenter, model posing, face to camera, selfie, TikTok style, person masking the product, distorted hands, extra fingers, text, lettering, numbers, dimension annotations, banner text, stand numbers, labels, stickers, watermark, logo, brand mark, signage, HDR halo, oversaturated colour, heavy vignette, lens flare, bokeh balls, tilt-shift, motion blur, fisheye distortion, low resolution, jpeg artefacts
```

### Tube rectangulaire

`/aluminium/tubes/tube-rectangulaire`  — *corrigé par l'audit*

**Scène.** Entree d'allee d'une maison wallonne : le cadre d'un portillon de jardin en tubes rectangulaires, montants et traverses assembles, remplissage en lames partiellement pose, une extremite de traverse encore ouverte.

**Référence.** `/images/produits/aluminium/tubes/tube-rectangulaire/studio-aluminium-tube-rectangulaire.webp`

**Correction apportée.** Chemin de reference VALIDE. Scene validee par usages.ts (« montant d'encadrement », « cadre de panneau ») et par le catalogue reel (jusqu'a 60x40x3 mm, section credible pour un cadre de portillon). Corrections : clause rendu-pas-photo absente ; clause trois tailles absente (la reference montre trois tubes cote a cote) ; et la traverse en rab posee sur deux treteaux avec perceuse et equerre est la septieme occurrence de la meme formule de mise en scene dans la gamme — supprimee. La lecture de la section ouverte, qu'assurait cette piece en rab, est reportee sur une extremite non encore obturee du cadre lui-meme, ce qui est plus juste sur un chantier.

```text
REFERENCE — The attached image is a clean technical studio render of the product on a white background. It is authoritative for the OBJECT ONLY: a rectangular hollow aluminium tube, two wide faces and two narrow ones, flat sides, slightly softened corners, constant thin wall visible as a fine open rectangle at the cut end, square-cut ends, plain mill finish in matte satin silver-grey. Reproduce it exactly — same rectangular section, same width-to-height ratio, same wall thickness, same corner radius, same metal, same colour, same finish. Do not redesign it into a square or round tube, do not make it solid, do not add grooves, T-slots, ribs, factory perforations or coatings, do not change its proportions. Only the plain holes required at the assembly points may appear.

WHAT IS NOT SPECIFIED — The reference shows three lengths of the same tube in three sizes, side by side, only to document the section. The number of pieces and their length are not part of the specification: the scene decides them. Never reproduce that catalogue line-up inside the scene.

NOT A STYLE REFERENCE — Copy the object, never the rendering. Do not carry over the white background, the studio lighting, or the flawless computer-generated surface. The output must read as a real photograph taken on a real installation.

SCENE — The entrance of a gravel drive at a Walloon brick house, soft light just after a shower. A garden gate frame made of rectangular aluminium tubes — two uprights, top and bottom rails, one intermediate rail — stands propped upright against the brick pier, its timber slat infill only partly fitted so the frame itself stays fully visible. The near end of the top rail has not been capped yet: its open rectangular section faces the camera. Clipped hedge, wet gravel, a tiled roofline and a grey-blue sky behind.

FRAMING — Three-quarter view from standing height, slightly to the hinge side so that both a wide face and a narrow edge of the tube are visible, with the open cut end of the top rail reading clearly in the near part of the frame. The gate frame is large and fully sharp; house and hedge stay secondary.

LIGHT & CAMERA — Natural daylight only, no flash. Soft post-rain light with a clear value difference between the wide and narrow faces, real contact shadow on the gravel and on the brick pier, physically plausible satin reflections, honest perspective, full-frame camera with a 50 mm lens, natural depth of field, product entirely sharp.

MATERIAL TRUTH — Believable installation state: fine mill grain, a few scratches, water beads sitting on the upper rail, brick dust in a corner, a slightly burred cut end.

NO TEXT — Nothing written anywhere in the frame: no house number, no nameplate, no signage, lettering, numbers, labels, stickers, printed graphics or brand marks, and no markings on the tubes or the timber. Every surface that could carry print stays blank.

PEOPLE — Preferably none. At most an installer's gloved hand steadying the frame at the very edge of the picture, out of focus: never centred, never between the camera and the product, never overlapping or masking the tubes. No face, no pose, no eye contact with the camera.
```

```text
NEGATIF — CGI render, 3D render look, ray-traced showroom lighting, studio white background, white cyclorama, catalogue line-up of three sizes side by side, product repeated in a row, plastic or rubbery surface, waxy material, over-perfect flawless tube, chrome mirror finish, coloured anodising, painted or wood-effect tube, rust, solid bar instead of hollow tube, square or round section, changed proportions, T-slot extrusion, grooved or ribbed profile, factory perforations, thick clumsy wall, invisible wall at cut end, warped or wavy edges, floating object, missing shadow, influencer, presenter, model posing, face to camera, selfie, TikTok style, person masking the product, distorted hands, extra fingers, text, lettering, numbers, dimension annotations, house number, nameplate, letterbox lettering, labels, stickers, watermark, logo, brand mark, signage, HDR halo, oversaturated colour, heavy vignette, lens flare, bokeh balls, tilt-shift, motion blur, fisheye distortion, low resolution, jpeg artefacts
```

### Tube rond

`/aluminium/tubes/tube-rond`  — *corrigé par l'audit*

**Scène.** Entree d'une maison contemporaine au petit matin : le tube rond sert de main courante sur supports muraux le long des quelques marches en beton, rosee sur la barre, personne dans le cadre.

**Référence.** `/images/produits/aluminium/tubes/tube-rond/studio-aluminium-tube-rond.webp`

**Correction apportée.** Chemin de reference VALIDE. Scene verifiee et confirmee : « main courante » est le premier exemple valide de usages.ts pour cette famille, et le catalogue monte jusqu'au tube rond de 40x2 mm, diametre reellement prehensible — la main courante n'est donc pas un usage invente, elle tient. Deux corrections : la clause rendu-pas-photo manque (sur un cylindre lisse c'est la porte ouverte au chrome CGI), et la main posee sur la barre est le seul endroit de la gamme ou une personne touche le produit au point de le masquer partiellement, en plus de tirer l'image vers le registre lifestyle interdit — supprimee, la scene se tient mieux vide au petit matin. Manque aussi la clause trois tailles (la reference montre trois tubes cote a cote).

```text
REFERENCE — The attached image is a clean technical studio render of the product on a white background. It is authoritative for the OBJECT ONLY: a round hollow aluminium tube, perfectly circular section, smooth cylindrical wall with no seam ridge, thin constant wall visible as a fine ring at the open cut end, square-cut ends, plain mill finish in matte satin silver-grey with a soft lengthwise sheen. Reproduce it exactly — same circular section, same diameter-to-wall proportion, same metal, same colour, same finish. Do not redesign it into a square, oval or fluted tube, do not make it solid, do not add knurling, grooves, ribs, welds, perforations, rubber sleeves or coatings, do not bend it into a curve it does not need.

WHAT IS NOT SPECIFIED — The reference shows three lengths of the same tube in three sizes, side by side, only to document the section. The number of pieces and their length are not part of the specification: the scene decides them. Never reproduce that catalogue line-up inside the scene.

NOT A STYLE REFERENCE — Copy the object, never the rendering. Do not carry over the white background, the studio lighting, or the flawless computer-generated surface — and above all do not let the cylinder turn into polished chrome. The output must read as a real photograph of a rail that is used every day.

SCENE — The entrance of a contemporary house in Belgium at first light, nobody about. A straight run of the round aluminium tube serves as a handrail on plain brackets along a short flight of in-situ concrete steps rising to a flush front door; the rail runs parallel to the slope of the steps, its far end closed off by a simple square-cut return. Smooth concrete, a strip of pale gravel and low ornamental grasses at the foot of the steps, rendered wall, first sun grazing across everything, dew on the rail.

FRAMING — Three-quarter view from the bottom of the steps, camera at chest height, the handrail running diagonally from foreground to background, large and fully sharp in the near half, its cylindrical form and open end clearly readable. The house reads behind it, secondary and gently soft.

LIGHT & CAMERA — Natural early daylight only, no flash. Low sun creating a continuous, physically correct specular band running along the top of the cylinder — a soft satin band, never a mirror line — soft shadow of the rail falling on the wall and steps, honest perspective, full-frame camera with a 50 mm lens, natural depth of field, product entirely sharp.

MATERIAL TRUTH — Real in-use detail: fine mill grain, dew droplets beaded along the upper curve, a faintly hand-polished stretch where people grip, a light scratch near a bracket, a trace of dust on the shadow side.

NO TEXT — Nothing written anywhere in the frame: no house number, no nameplate, no signage, lettering, numbers, labels, stickers or brand marks, and no markings on the rail, the brackets or the door. Every surface that could carry print stays blank.

PEOPLE — None.
```

```text
NEGATIF — CGI render, 3D render look, ray-traced showroom lighting, studio white background, white cyclorama, catalogue line-up of three sizes side by side, product repeated in a row, plastic or rubbery surface, waxy material, over-perfect flawless tube, chrome mirror finish, polished stainless look, coloured anodising, painted tube, rust, solid bar instead of hollow tube, square or oval section, fluted or knurled surface, visible weld seam, added grooves or ribs, rubber sleeve, thick clumsy wall, invisible wall at cut end, oval distortion, warped or wavy rail, floating object, missing shadow, hand on the rail, influencer, presenter, model posing, face to camera, selfie, TikTok style, person masking the product, distorted hands, extra fingers, text, lettering, numbers, dimension annotations, house number, nameplate, labels, stickers, watermark, logo, brand mark, signage, HDR halo, oversaturated colour, heavy vignette, lens flare, bokeh balls, tilt-shift, motion blur, fisheye distortion, low resolution, jpeg artefacts
```

### Cornière égale

`/inox/profiles/corniere-egale`

**Scène.** Local de lavage d'une petite brasserie artisanale belge : une cornière protège l'arête d'un angle de mur carrelé, une autre borde le caniveau du sol béton.

**Référence.** `/images/produits/inox/profiles/corniere-egale/studio-inox-corniere-egale.webp`

```text
Ultra-realistic documentary photograph of stainless steel equal angle profiles installed in a real, finished project. PRODUCT FIDELITY - THE ATTACHED REFERENCE IMAGE IS THE ABSOLUTE AUTHORITY FOR THE PRODUCT ITSELF: reproduce exactly the same equal-angle section shown there - two legs of identical width meeting at a true right angle, the same constant wall thickness, the same leg-width to thickness proportion, the same slightly radiused outer corner and inner fillet, the same clean square-cut ends. Match the reference material and finish exactly: satin stainless steel, cool neutral grey, softly and diffusely reflective, exactly as bright as the reference - never mirror chrome, never dull matte, never painted, never galvanised, never coated. IMPORTANT: the reference is a plain studio shot of the bare product on a white background and shows several identical angles of different sizes lined up side by side. Take from it ONLY the section, geometry, proportions, material, colour and finish. Do not copy its white background, its studio staging, its camera angle, its floating position or the number of pieces it shows; show the profile built into the scene described below. Do not redraw, restyle, simplify, thicken, thin, taper or substitute the profile; add no perforation, hole, slot, rib, groove, embossing, marking or surface pattern that the reference does not show. SCENE: the washdown area of a small artisan brewery in Belgium, recently completed and in service. One angle is fitted vertically as edge protection on the corner of a white-tiled wall, its two legs wrapping the corner; a second angle runs horizontally along the lip of the drainage channel set into the polished concrete floor, fixed flush. Background, secondary and slightly out of focus: stainless brewing tanks, a coiled rubber hose, tiled wall with visible grout lines, a damp floor with shallow puddles and faint water marks. LIGHT AND CAMERA: soft cool daylight from a high industrial window mixed with neutral ceiling light; 35mm lens at eye level, natural shallow depth of field, the angle profile sharp and filling a clear part of the foreground, the room readable behind it. REALISM: physically correct reflections picking up the tiles and the window, coherent contact shadows where the profile meets wall and floor, fine brushed texture on the metal, water droplets, honest imperfections in grout, concrete and sealant. PEOPLE: no people anywhere in the frame. NO GRAPHICS: no visible text, no lettering, no numbers, no dimensions, no logos, no brand marks, no signage, no labels, no stamped or etched markings anywhere in the image.
```

```text
NEGATIF — CGI, 3D render, video game asset, clay render, product catalogue shot, white studio background, cut-out product on white, three profiles lined up side by side, duplicate identical profiles, unused product lying on the floor, plastic or waxy surfaces, mirror chrome, over-polished, dull matte grey, fake HDR glow, oversaturated colours, flat studio lighting, floating object, impossible or missing shadows, warped or duplicated geometry, wrong section, unequal legs, rounded tube shape, invented holes, perforations, slots, rivets, decorative pattern, rust, corrosion, weathering steel, painted metal, text, letters, numbers, dimensions, watermark, logo, brand mark, sticker, label, certification stamp, etched marking, signage, influencer, model posing, person facing camera, selfie, portrait, hands near the lens, smiling face, TikTok style, vlog framing, fisheye, heavy vignette, motion blur, noise artifacts, tropical vegetation, desert, American suburb
```

### Plat

`/inox/profiles/plat`  — *corrigé par l'audit*

**Scène.** Échelle d'accès fixée au mur de quai d'un canal en Wallonie : les deux limons soudés de l'échelle sont en plat inox, les barreaux ronds sont secondaires.

**Référence.** `/images/produits/inox/profiles/plat/studio-inox-plat.webp`

**Correction apportée.** Trois écarts. (1) Règle 4 : décor réutilisé — le garde-corps à lisses horizontales au-dessus de l'eau double le garde-corps de terrasse du tube rond ; deux fois le même objet dans la même gamme. (2) Règle 2 : une personne est autorisée (« a single pedestrian may appear ») alors que l'échelle n'en a aucun besoin, un parapet suffit à donner l'échelle. (3) Règle 4 encore : lib/usages.ts décrit le plat comme renfort, support, entretoise et pièce de liaison, pas comme remplissage de garde-corps. Scène remplacée par une échelle de quai au bord d'un canal wallon, où les deux limons sont en plat inox soudé : usage juste, milieu humide qui justifie l'inox, décor unique dans la gamme, produit très lisible au premier plan. Fixations soudées et non boulonnées pour ne pas introduire de perçages que la référence ne montre pas. Référence vérifiée : présente et conforme.

```text
Ultra-realistic documentary photograph of stainless steel flat bars installed in a real, finished project. PRODUCT FIDELITY - THE ATTACHED REFERENCE IMAGE IS THE ABSOLUTE AUTHORITY FOR THE PRODUCT ITSELF: reproduce exactly the same solid rectangular flat section shown there - the same width to thickness ratio (a wide flat face and a narrow edge), the same flat parallel faces, the same slightly broken sharp edges, the same square cut ends, a solid bar throughout, never hollow, never a tube, never a thin sheet. Match the reference material and finish exactly: satin stainless steel, cool neutral grey, softly and diffusely reflective, exactly as bright as the reference - never mirror chrome, never dull matte, never painted, never galvanised, never coated. IMPORTANT: the reference is a plain studio shot of the bare product on a white background and shows several identical flat bars of different sizes lined up side by side. Take from it ONLY the section, geometry, proportions, material, colour and finish. Do not copy its white background, its studio staging, its camera angle or the number of pieces it shows; show the flat bar built into the scene described below. Do not redraw, restyle, simplify, thicken, thin, twist or substitute the section; add no perforation, hole, slot, rib, embossing, marking or surface pattern that the reference does not show. SCENE: an access ladder fixed to the stone quay wall of a canal in Wallonia, Belgium, recently installed. The two flat bars form the vertical side rails of the ladder, standing on edge with their wide faces turned inward, the rungs welded between them, the whole ladder held off the wall by welded brackets and running down towards the dark water. Background, secondary: mossy stone and concrete quay wall, a heavy mooring bollard, still dark green canal water, a brick quayside and bare-branched trees on the far bank, grey northern sky. LIGHT AND CAMERA: soft diffuse overcast daylight with weak reflected light bouncing off the water; 50mm lens, low three-quarter view from the quay edge looking along the ladder, the flat side rails sharp, large and clearly readable in the foreground, the canal falling gently out of focus. REALISM: physically correct soft reflections gliding along the flat faces and a brighter line on the narrow edge, coherent shadows on the stone, fine brushed grain on the metal, faint water splashes and dust, weld beads slightly discoloured, real moss, algae line and chipped mortar on the quay. PEOPLE: no people anywhere in the frame. NO GRAPHICS: no visible text, no lettering, no numbers, no dimensions, no logos, no brand marks, no signage, no labels, no stamped or etched markings anywhere in the image.
```

```text
NEGATIF — CGI, 3D render, video game asset, clay render, product catalogue shot, white studio background, cut-out product on white, three flat bars lined up side by side, duplicate identical bars, unused product leaning against a wall, plastic or waxy surfaces, mirror chrome, over-polished, dull matte grey, fake HDR glow, oversaturated colours, flat studio lighting, floating object, impossible shadows, warped or duplicated geometry, hollow tube instead of solid flat bar, round or square tube, sheet metal panel, wrong thickness, twisted or wavy bars, invented holes, perforations, bolt holes, rivets, decorative pattern, rust, corrosion, painted metal, text, letters, numbers, dimensions, watermark, logo, brand mark, sticker, label, certification stamp, etched marking, signage, influencer, model posing, person facing camera, selfie, portrait, close-up hands, smiling face, TikTok style, vlog framing, fisheye, heavy vignette, motion blur, noise artifacts, tropical vegetation, desert, American suburb
```

### Rond plein

`/inox/profiles/rond-plein`

**Scène.** Grille de fenêtre au rez-de-chaussée d'une maison en briques wallonne : les ronds pleins forment les barreaux verticaux soudés dans l'embrasure.

**Référence.** `/images/produits/inox/profiles/rond-plein/studio-inox-rond-plein.webp`

```text
Ultra-realistic documentary photograph of solid stainless steel round bars installed in a real, finished project. PRODUCT FIDELITY - THE ATTACHED REFERENCE IMAGE IS THE ABSOLUTE AUTHORITY FOR THE PRODUCT ITSELF: reproduce exactly the same smooth solid cylindrical bar shown there - perfectly circular section, constant diameter along the whole length, smooth unribbed surface with no thread and no knurling, the same clean square cut ends showing a full solid section, never hollow. Match the reference material and finish exactly: satin stainless steel, cool neutral grey, softly reflective, exactly as bright as the reference - never mirror chrome, never dull matte, never painted, never galvanised, never ribbed rebar. IMPORTANT: the reference is a plain studio shot of the bare product on a white background and shows several identical round bars of different diameters lined up side by side. Take from it ONLY the section, geometry, proportions, material, colour and finish. Do not copy its white background, its studio staging, its camera angle or the number of pieces it shows; show the bars built into the scene described below. Do not redraw, restyle, taper, bend, flatten, simplify or substitute the bar; add no perforation, hole, groove, thread, marking or surface pattern that the reference does not show. SCENE: the ground-floor window of a red brick house in Wallonia, Belgium. The round bars form a plain vertical window grille set into the masonry reveal, evenly spaced and welded into a slim perimeter frame of the same stainless steel, the welds ground smooth, the frame anchored into the brickwork. Background, secondary: brick coursing with visible mortar joints, a bluestone sill, a white timber window behind the bars with a curtain half drawn, ivy climbing at the edge of the reveal, a grey sky reflected in the glass. LIGHT AND CAMERA: soft overcast daylight raking slightly across the facade so each bar carries a vertical highlight; 50mm lens, slightly oblique frontal view at standing height, the bars sharp and large in the frame, the facade readable around them. REALISM: physically correct specular highlights curving around each cylinder, coherent shadows cast on the brick, fine brushed texture, dust and a few dried rain traces, weathered brick, chipped mortar and a little moss at the sill. PEOPLE: no people anywhere in the frame. NO GRAPHICS: no visible text, no lettering, no numbers, no dimensions, no house number, no logos, no brand marks, no signage, no labels, no stamped or etched markings anywhere in the image.
```

```text
NEGATIF — CGI, 3D render, video game asset, clay render, product catalogue shot, white studio background, cut-out product on white, three bars lined up side by side, duplicate identical bars, unused product lying on the ground, plastic or waxy surfaces, mirror chrome, over-polished, dull matte grey, fake HDR glow, oversaturated colours, flat studio lighting, floating object, impossible shadows, warped or duplicated geometry, hollow tube, ribbed rebar, threaded rod, knurled bar, tapered or bent bars, square section, invented holes, perforations, rivets, decorative scrollwork, rust, corrosion, painted or black metal, text, letters, numbers, dimensions, watermark, logo, brand mark, sticker, label, certification stamp, etched marking, signage, house number, influencer, model posing, person facing camera, selfie, portrait, close-up hands, TikTok style, vlog framing, fisheye, heavy vignette, motion blur, noise artifacts, tropical vegetation, desert, American suburb
```

### Tôle plane 304 brossée

`/inox/toles/tole-plane-304-brossee`

**Scène.** Cuisine rénovée d'une maison de ville belge : la tôle inox brossée fait crédence derrière la plaque de cuisson, grain satiné horizontal continu.

**Référence.** `/images/produits/inox/toles/tole-plane-304-brossee/studio-tole-inox-brossee.webp`

```text
Ultra-realistic documentary photograph of a flat brushed stainless steel sheet installed in a real, finished project. PRODUCT FIDELITY - THE ATTACHED REFERENCE IMAGE IS THE ABSOLUTE AUTHORITY FOR THE PRODUCT ITSELF: reproduce exactly the same flat sheet shown there - perfectly planar surface with no waviness, the same constant thin gauge visible at the edges, straight clean-cut edges, and above all the same unidirectional brushed satin finish, a fine consistent linear grain running in one single direction across the whole panel, identical in scale and regularity to the reference. Match the reference material and colour exactly: cool neutral grey stainless, satin and diffusely reflective, exactly as bright as the reference - never mirror chrome, never dull matte, never painted, never textured, never patterned. IMPORTANT: the reference is a plain studio shot of the bare sheet on a white background. Take from it ONLY the flatness, edges, thickness, material, colour and brushed grain. Do not copy its white background, its studio staging, its floating angle or its isolation; show the sheet installed in the scene described below. Do not redraw, simplify or substitute the material: no checker plate, no diamond plate, no perforation, no corrugation, no embossing, no visible screws, rivets or fixing holes the reference does not show. SCENE: the renovated kitchen of a Belgian townhouse. The sheet is fitted as a one-piece splashback behind an induction hob, spanning from the worktop up to the wall units, edges tight against the wall with no visible fixings, its brushed grain running horizontally and continuously across the whole panel. Background, secondary: a solid oak worktop, matte dark cabinet fronts, a pot and a wooden board pushed to one side, a window on the left with a garden blurred behind it. LIGHT AND CAMERA: soft daylight from the side window plus a warm under-cabinet light; 35mm lens, slightly angled frontal view so the panel catches a soft gradient instead of a hard glare, the panel sharp and dominant in the frame, the kitchen readable around it. REALISM: physically correct anisotropic reflections stretched along the brush direction, coherent shadows under the wall units, faint fingerprints, a few micro-scratches and dust near the edges, real wood grain and honest wear on the worktop. PEOPLE: no people anywhere in the frame. NO GRAPHICS: no visible text, no lettering, no numbers, no dimensions, no logos, no brand marks, no signage, no labels, no stamped or etched markings anywhere in the image.
```

```text
NEGATIF — CGI, 3D render, video game asset, clay render, product catalogue shot, white studio background, cut-out panel on white, floating panel, duplicate panels, plastic or waxy surfaces, mirror chrome, polished mirror panel, over-polished, dull matte grey, fake HDR glow, blown highlights, oversaturated colours, flat studio lighting, impossible shadows, warped geometry, wavy or dented sheet, checker plate, diamond plate, perforated sheet, corrugated sheet, hammered or patterned metal, visible screws, rivets, fixing holes, random multidirectional scratches, swirl marks, grain running in several directions, rust, corrosion, painted metal, text, letters, numbers, dimensions, watermark, logo, brand mark, sticker, label, certification stamp, etched marking, signage, influencer, model posing, person facing camera, selfie, portrait, hands cooking close to lens, smiling face, TikTok style, vlog framing, fisheye, heavy vignette, motion blur, noise artifacts, tropical vegetation, desert, American suburb
```

### Tube carré

`/inox/tubes/tube-carre`

**Scène.** Portail d'entrée contemporain d'une maison belge : cadre et montants en tube carré inox, remplissage en lattes de bois sombre, piliers en briques.

**Référence.** `/images/produits/inox/tubes/tube-carre/studio-inox-tube-carre.webp`

```text
Ultra-realistic documentary photograph of stainless steel square tubes installed in a real, finished project. PRODUCT FIDELITY - THE ATTACHED REFERENCE IMAGE IS THE ABSOLUTE AUTHORITY FOR THE PRODUCT ITSELF: reproduce exactly the same square hollow section shown there - four flat faces of strictly equal width, the same slightly radiused outer corners, the same constant wall thickness visible at the open end, the same hollow interior, the same clean square cut. Match the reference material and finish exactly: satin stainless steel, cool neutral grey, softly reflective, exactly as bright as the reference - never mirror chrome, never dull matte, never painted, never galvanised, never anodised. IMPORTANT: the reference is a plain studio shot of the bare product on a white background and shows several identical square tubes of different sizes lined up side by side. Take from it ONLY the section, geometry, proportions, material, colour and finish. Do not copy its white background, its studio staging, its camera angle or the number of pieces it shows; show the tube built into the scene described below. Do not redraw, restyle, round, taper, simplify or substitute the section; add no perforation, hole, bolt head, embossing, marking or surface pattern that the reference does not show. SCENE: the driveway entrance of a contemporary house in Belgium, the work recently completed. The square tubes form the outer frame and the vertical stiles of a single-leaf swing gate, assembled with tight ground welds, the infill made of vertical dark timber slats set back from the frame, the hinge side fixed to a brick pillar. Background, secondary: brick gate pillars, a gravel driveway, a clipped hedge and birch trees, a rendered facade with large glazing, overcast northern sky. LIGHT AND CAMERA: soft diffuse late-afternoon daylight with a gentle directional accent skimming the top rail; 35mm lens, three-quarter view from the street side at standing height, the tube frame sharp and clearly readable in the foreground, the house softly out of focus behind. REALISM: physically correct reflections breaking cleanly at each edge of the square faces, coherent shadows on the gravel, fine brushed texture, faint dust and dried rain traces, real scattered gravel and irregular living hedge. PEOPLE: no people anywhere in the frame. NO GRAPHICS: no visible text, no lettering, no numbers, no house number, no dimensions, no logos, no brand marks, no signage, no labels, no stamped or etched markings anywhere in the image.
```

```text
NEGATIF — CGI, 3D render, video game asset, clay render, product catalogue shot, white studio background, cut-out product on white, three tubes lined up side by side, duplicate identical tubes, unused product leaning on the gate, plastic or waxy surfaces, mirror chrome, over-polished, dull matte grey, fake HDR glow, oversaturated colours, flat studio lighting, floating object, impossible shadows, warped or duplicated geometry, round tube, rectangular tube, solid bar, unequal faces, wrong wall thickness, invented holes, perforations, rivets, decorative scrollwork, rust, corrosion, painted or powder-coated metal, text, letters, numbers, dimensions, watermark, logo, brand mark, sticker, label, certification stamp, etched marking, signage, house number, intercom text, influencer, model posing, person facing camera, selfie, portrait, close-up hands, TikTok style, vlog framing, fisheye, heavy vignette, motion blur, noise artifacts, tropical vegetation, desert, American suburb
```

### Tube rectangulaire

`/inox/tubes/tube-rectangulaire`  — *corrigé par l'audit*

**Scène.** Abri à vélos d'une petite entreprise en Belgique : les tubes rectangulaires forment les deux poutres horizontales et les montants du cadre porteur, toiture translucide, dalle béton.

**Référence.** `/images/produits/inox/tubes/tube-rectangulaire/studio-inox-tube-rectangulaire.webp`

**Correction apportée.** Règle 4, décor réutilisé : auvent adossé à une maison belge avec briques, haie, jardin et ciel couvert — c'est le même décor que le portail du tube carré (même maison, mêmes briques, même haie, même ciel), au point qu'un spectateur croirait deux photos du même chantier. La scène est aussi très proche du garde-corps de terrasse du tube rond. Le reste du prompt (fidélité de la section rectangulaire, réalisme, pas de personne, pas de texte) était bon et a été conservé. Nouvelle scène : abri à vélos d'une petite entreprise ou d'une école, où le tube rectangulaire travaille en poutre horizontale et en montant — usage exact de lib/usages.ts (traverse, montant, cadre, section allongée qui s'accorde à la géométrie), décor public et minéral qui n'existe nulle part ailleurs dans la gamme. Référence vérifiée présente ; elle montre un tube unique, la clause anti-mise-en-scène a été adaptée.

```text
Ultra-realistic documentary photograph of stainless steel rectangular tubes installed in a real, finished project. PRODUCT FIDELITY - THE ATTACHED REFERENCE IMAGE IS THE ABSOLUTE AUTHORITY FOR THE PRODUCT ITSELF: reproduce exactly the same rectangular hollow section shown there - two wide faces and two narrow faces with the same width to height ratio, the same slightly radiused corners, the same constant wall thickness visible at the open end, the same hollow interior, the same clean square cut. Match the reference material and finish exactly: satin stainless steel, cool neutral grey, softly reflective, exactly as bright as the reference - never mirror chrome, never dull matte, never painted, never galvanised, never anodised. IMPORTANT: the reference is a plain studio shot of a single bare tube on a white background. Take from it ONLY the section, geometry, proportions, material, colour and finish. Do not copy its white background, its studio staging, its floating angle or its isolation; show the tube built into the scene described below. Do not redraw, restyle, square up the section, taper, simplify or substitute it; add no perforation, hole, bolt head, embossing, marking or surface pattern that the reference does not show. SCENE: a covered bicycle shelter in the yard of a small company in Belgium, recently built and already in use. The rectangular tubes form the two long horizontal beams and the vertical posts of the frame, wide faces turned outward, welded at the corners and standing on the concrete slab, carrying a light translucent roof. Background, secondary: a few bicycles parked under the shelter, concrete paving with visible joints, a low clipped hedge, a plain brick building with grey window frames, wet asphalt and a grey northern sky. LIGHT AND CAMERA: flat soft overcast daylight with a faint sun break brightening one beam, diffuse light passing through the translucent roof; 35mm lens, low three-quarter view looking up along the front beam so the rectangular section is clearly readable, the yard falling gently out of focus. REALISM: physically correct highlights breaking sharply at each corner of the section, coherent shadows on the concrete, fine brushed texture, dust, rain streaks and a few water drops, weathered concrete, moss in the paving joints, honestly used bicycles. PEOPLE: no people anywhere in the frame. NO GRAPHICS: no visible text, no lettering, no numbers, no dimensions, no logos, no brand marks on the bicycles or the building, no signage, no labels, no stamped or etched markings anywhere in the image.
```

```text
NEGATIF — CGI, 3D render, video game asset, clay render, product catalogue shot, white studio background, cut-out product on white, floating tube, duplicate identical tubes, unused product lying on the ground, plastic or waxy surfaces, mirror chrome, over-polished, dull matte grey, fake HDR glow, oversaturated colours, flat studio lighting, impossible shadows, warped or duplicated geometry, square tube with equal sides, round tube, solid bar, wrong proportions, wrong wall thickness, invented holes, perforations, rivets, decorative pattern, rust, corrosion, painted or powder-coated metal, text, letters, numbers, dimensions, watermark, logo, brand mark, bicycle branding, sticker, label, certification stamp, etched marking, signage, influencer, model posing, person facing camera, selfie, portrait, close-up hands, smiling face, TikTok style, vlog framing, fisheye, heavy vignette, motion blur, noise artifacts, tropical vegetation, desert, American suburb
```

### Tube rond

`/inox/tubes/tube-rond`  — *corrigé par l'audit*

**Scène.** Terrasse d'étage d'une maison de ville belge : le tube rond forme la main courante et les poteaux du garde-corps, au-dessus des toits d'ardoise.

**Référence.** `/images/produits/inox/tubes/tube-rond/studio-inox-tube-rond.webp`

**Correction apportée.** Règle 2 : le prompt autorise une personne (« One person may appear small at the far end ») alors que l'échelle n'en a pas besoin — une main courante et une terrasse donnent déjà l'échelle, et la règle ne tolère la personne que si l'échelle l'exige. La contradiction est double puisque le négatif bannit par ailleurs toute figure humaine. Personne retirée. Le reste est solide : fidélité de la section creuse circulaire, usage exact selon lib/usages.ts (main courante saisie à la main, barreaudage), décor de toitures distinct du reste de la gamme. Référence vérifiée présente. Ajouts : neutralisation de la mise en scène studio (trois tubes alignés sur fond blanc), calage de brillance, assemblage soudé sans perçages inventés.

```text
Ultra-realistic documentary photograph of stainless steel round tubes installed in a real, finished project. PRODUCT FIDELITY - THE ATTACHED REFERENCE IMAGE IS THE ABSOLUTE AUTHORITY FOR THE PRODUCT ITSELF: reproduce exactly the same circular hollow section shown there - perfectly round, constant outside diameter along the whole length, the same constant wall thickness visible at the cut end, the same hollow interior, the same smooth unribbed surface, the same clean square cut. Match the reference material and finish exactly: satin stainless steel, cool neutral grey, softly reflective, exactly as bright as the reference - never mirror chrome, never dull matte, never painted, never galvanised. IMPORTANT: the reference is a plain studio shot of the bare product on a white background and shows several identical round tubes of different diameters lined up side by side. Take from it ONLY the section, geometry, proportions, material, colour and finish. Do not copy its white background, its studio staging, its camera angle or the number of pieces it shows; show the tube built into the scene described below. Do not redraw, restyle, taper, flatten, oval, simplify or substitute the section; add no perforation, hole, groove, marking or surface pattern that the reference does not show. SCENE: the first-floor terrace of a Belgian townhouse, freshly completed. The round tubes form the continuous handrail and the vertical posts of the terrace guardrail, joined by neat ground welds, with a slim tensioned infill below and a tiled terrace floor. Background, secondary: neighbouring brick gables with slate and zinc roofs, chimney stacks, tree crowns below the parapet, a soft grey northern sky. LIGHT AND CAMERA: soft overcast daylight with a warm low sun grazing the top of the handrail; 35mm lens, view running along the handrail from hand height so the tube leads the eye into the frame, the product sharp and large in the foreground, the rooftops softly out of focus. REALISM: physically correct specular band sweeping around the cylindrical surface, coherent shadows on the terrace floor, fine brushed texture, faint fingerprints on the grip area, dust and dried rain traces, real moss in the tile joints and weathered slate behind. PEOPLE: no people anywhere in the frame. NO GRAPHICS: no visible text, no lettering, no numbers, no dimensions, no logos, no brand marks, no signage, no labels, no stamped or etched markings anywhere in the image.
```

```text
NEGATIF — CGI, 3D render, video game asset, clay render, product catalogue shot, white studio background, cut-out product on white, three tubes lined up side by side, duplicate identical tubes, unused product lying on the terrace, plastic or waxy surfaces, mirror chrome, over-polished, dull matte grey, fake HDR glow, oversaturated colours, flat studio lighting, floating railing, impossible shadows, warped or duplicated geometry, solid bar instead of tube, square or rectangular tube, oval or flattened section, varying diameter, ribbed or threaded surface, invented holes, perforations, rivets, decorative scrollwork, rust, corrosion, painted or black metal, text, letters, numbers, dimensions, watermark, logo, brand mark, sticker, label, certification stamp, etched marking, signage, people, person, silhouette, influencer, model posing, person facing camera, selfie, portrait, hands gripping the rail, smiling face, TikTok style, vlog framing, fisheye, heavy vignette, motion blur, noise artifacts, tropical vegetation, desert, American suburb
```

### Bordures

`/jardin-cloture/amenagement/bordures`

**Scène.** Jardin contemporain wallon terminé : la bordure Corten sépare une allée de gravier d'une pelouse et d'un massif de graminées, maison en brique rouge floue à l'arrière.

**Référence.** `/images/produits/jardin-cloture/amenagement/bordures/studio-bordure.webp`

```text
Use the attached reference image as the single, authoritative source of truth for the product. Ultra-realistic documentary photograph of that exact steel garden edging, installed in a finished private garden in Belgium.

PRODUCT FIDELITY (highest priority): reproduce the profile exactly as shown in the reference — one long, thin, perfectly straight flat strip of sheet steel standing vertically on its edge, with a single narrow lip folded at a right angle along its top edge only, forming a narrow flat top rim; constant height over its entire length, the same thin sheet thickness, the same proportion between that narrow top lip and the tall blade below it, the same clean square-cut ends. Same material and finish as the reference: weathered Corten steel with its cloudy, uneven, orange-brown to deep rust oxidation, slightly darker in patches, with the thin bare bright metal line visible along the cut edge. Do not redraw, simplify, thicken, curve, emboss, perforate, decorate or replace the product, and do not duplicate it or add a second profile. No ribs, no holes, no ornaments, no different colour, no wood, no plastic, no concrete or brick substitute.

SCENE: the edging runs diagonally across the frame, bedded into the ground along its lower edge only, so that most of its height and the whole of its top lip stay clearly visible. On one side, a raked grey gravel path; on the other, a clipped lawn and a planted bed of ornamental grasses, low perennials and dark bark mulch. A few gravel stones and crumbs of damp soil rest against the steel; a thin line of darker earth marks where the strip enters the ground; one or two blades of grass lean over the top lip. Background, soft and clearly secondary: a red-brick Belgian house facade with white joinery, a trimmed beech hedge, a few wet paving slabs.

LIGHT AND CAMERA: soft overcast northern daylight, late morning after rain; diffuse, physically coherent shadows; damp surfaces with subtle non-mirror reflections. 35 mm lens, low three-quarter viewpoint at roughly knee height, looking along the line of the edging so its length and straightness read clearly. The product fills the foreground, stays sharp, and is large enough to be identified immediately; natural shallow depth of field softening the background only.

REALISM: authentic photographic texture — fine grain, micro-scratches, dust, irregular gravel, uneven grass, natural muted colour. Absolutely no CGI or 3D-render look, no plastic-smooth surfaces, no unnaturally perfect objects. No people. No visible text, no lettering, no logo, no brand mark, no signage, no dimension callout anywhere in the image.
```

```text
NEGATIF — CGI, 3D render, CAD render, product mockup, video game graphics, plastic look, glossy plastic surface, waxy material, oversaturated colours, HDR halos, illustration, painting, cartoon, sketch, collage, watermark, signature, any visible text, letters, numbers, logo, brand mark, label, signage, dimension lines, measurement callouts, redesigned product, altered profile, thicker sheet, curved or wavy strip, lip on both edges, lip too wide, added ribs, added perforations, added holes, decorative pattern, duplicated strip, second profile, wood edging, plastic edging, concrete kerb, brick border, galvanised silver finish instead of Corten, uniform flat rust colour, fake painted rust, product buried and barely visible, people, influencer, model posing, face to camera, selfie, portrait, hands holding the product, TikTok style, studio lighting, white studio background, flat lighting, lens flare, bokeh balls, fisheye distortion, tilt-shift, motion blur, floating objects, impossible shadows, inconsistent perspective, blurry product, product too small, AI artifacts, deformed geometry, noise artifacts
```

### Fixations

`/jardin-cloture/clotures/fixations`  — *corrigé par l'audit*

**Scène.** Gros plan sur la liaison panneau-poteau d'une clôture de jardin terminée. Réserve : aucune photo de fixation n'existe dans lib/visuels-produits.json, la référence est donc le poteau CLOPLUS 40 — sa géométrie fait foi, la bride reste une reconstitution. Faire rendre un visuel studio de la bride avant toute utilisation définitive.

**Référence.** `/images/produits/jardin-cloture/clotures/poteaux/studio-poteau-cloplus-40.webp`

**Correction apportée.** Vérification faite : /jardin-cloture/clotures/fixations n'apparaît NULLE PART dans lib/visuels-produits.json — ni dans la clé categories (seules bordures, panneaux-rigides et poteaux y figurent pour cet univers), ni dans la clé produits (aucune entrée bride ni fixation). Le chemin utilisé existe bien comme fichier, mais c'est la photo studio des POTEAUX : le produit réel de la catégorie, la bride, n'a donc aucune référence et serait entièrement inventé par le modèle. C'est une entorse à la règle 1, non réparable par la rédaction seule : la vraie correction est de produire un rendu studio de la bride (FIXATION BRIDE 30 NV NOIR, présente dans lib/catalogue.ts) avant de générer cette mise en situation. Deuxième défaut, identique aux poteaux : le poteau est décrit en « steel » alors que le CLOPLUS 40 est en aluminium thermolaqué (lib/catalogue.ts) — corrigé. Le prompt ci-dessous est la meilleure version utilisable en attendant : le poteau de la référence sert d'ancrage géométrique, la bride est décrite au strict minimum mécanique (platine plate, un boulon dans un trou oblong existant) et sa teinte noire est sourcée du catalogue, pas inventée ; toute invention de forme est interdite. Le reste du prompt était bon : cadrage macro justifié par la taille de la pièce, aucune personne ni main, réalisme complet, aucun texte ni cote.

```text
Use the attached reference image as the authoritative source of truth for the POST visible in this photograph. Ultra-realistic close-up documentary photograph of the fastening point where a rigid welded-mesh fence panel is clamped onto that exact post, on a finished garden fence in Belgium.

PRODUCT FIDELITY (highest priority): the post must match the reference exactly — an H-shaped extruded profile whose two flanges are closed rectangular tubes, joined by a recessed central web forming an open channel, with the regular row of small oval holes pierced along the centre of that channel; same proportions, same crisp folded edges, same matte dark powder-coated aluminium finish, no bare metal showing. Do not redraw, simplify, round off or replace the post section. The fastening itself is the subject and must stay strictly minimal and mechanical: one small flat rectangular clamping plate in the same matte black coated finish, seated flat in the channel of the post, pressing two vertical wires of the mesh panel against the post, held by a single bolt passing through one of the existing oval holes, with a plain flat washer and the bolt head standing slightly proud. Nothing else: no invented shapes, no hooks, no cable ties, no welded plates, no screws driven into the mesh, no second bracket, no added parts, no ornament.

SCENE: the panel and the post meet at the centre-right of the frame; the dark mesh runs out of focus to the left, the post rises vertically and is cut by the top of the frame. Far behind and completely soft, a mown lawn, a mixed planted border and the corner of a grey paved terrace. Small honest details: a fingerprint on the coating, a drop of water on the bolt head, a faint dusty film, a thin cobweb between two wires.

LIGHT AND CAMERA: soft overcast northern daylight; gentle, physically coherent shadows; matte coating with a faint diffuse highlight, never mirror-like. 85 mm lens at close range, placed slightly below the bracket and looking up a few degrees, three-quarter angle so the clamping plate, the bolt, the clamped wires and the channel of the post are all readable in one view. The fastening is sharp and fills a large part of the frame; the background is a smooth natural blur.

REALISM: authentic macro photographic texture — micro-scratches, dust, uneven light on the coating, fine grain, a slightly imperfect bolt alignment. Absolutely no CGI or 3D-render look, no plastic surfaces, no unnaturally perfect objects. No people, no hands, no tools held in frame. No visible text, no lettering, no logo, no brand mark, no part number, no dimension callout anywhere in the image.
```

```text
NEGATIF — CGI, 3D render, CAD render, exploded view, technical diagram, product mockup, video game graphics, plastic look, glossy plastic clamp, chrome mirror finish, oversaturated colours, HDR halos, illustration, painting, cartoon, watermark, signature, any visible text, letters, numbers, logo, brand mark, part number, label, dimension lines, callout arrows, redesigned post, round tube post, square tube post, wooden post, post without recessed channel, post without oval holes, steel or galvanised look instead of dark coated aluminium, bare metal, invented bracket shapes, ornate bracket, hooks, cable ties, zip ties, wire twists, welded plate, self-tapping screws into the mesh, oversized bolt, multiple redundant fixings, second bracket, rust, peeling paint, people, hands, gloves, worker, influencer, face to camera, selfie, TikTok style, studio lighting, white studio background, flat lighting, ring light, lens flare, fisheye distortion, extreme macro distortion, motion blur, duplicated objects, floating objects, impossible shadows, inconsistent perspective, blurry product, AI artifacts, deformed geometry
```

### Panneaux rigides

`/jardin-cloture/clotures/panneaux-rigides`  — *corrigé par l'audit*

**Scène.** Limite terminée d'un parking d'entreprise dans un zoning wallon : plusieurs panneaux rigides sombres alignés entre l'aire asphaltée et une bande enherbée, jeune haie de charmes et hall industriel bardé à l'arrière.

**Référence.** `/images/produits/jardin-cloture/clotures/panneaux-rigides/studio-panneau-cloture-plis-205.webp`

**Correction apportée.** Référence vérifiée et valide (clé categories de lib/visuels-produits.json, fichier présent). Trois défauts. 1) Décor recyclé : le prompt d'origine place le panneau dans un fond de jardin privatif avec pelouse, haie de hêtre et pignons en brique belge — soit exactement le décor des bordures (maison en brique, haie de hêtre taillée, pelouse). Règle 4 non respectée. Corrigé en déplaçant la scène vers une limite de parking d'entreprise, contexte explicitement listé dans lib/usages.ts (« clôture de parking d'entreprise », « limite entre deux parcelles »), et qui ne réapparaît dans aucune autre catégorie de l'univers. 2) Erreur technique de fidélité : « every welded intersection stays a simple butt weld » — un treillis soudé se fait par points de soudure aux croisements, pas en bout à bout ; formulation corrigée. 3) Fidélité incomplète : sur la photo studio, les fils horizontaux se resserrent nettement en haut et en bas du panneau et de part et d'autre des plis — détail absent du prompt, donc laissé à l'invention du modèle ; ajouté. Ajout aussi de l'interdiction des plaques d'immatriculation et enseignes, puisque la nouvelle scène comporte des véhicules potentiels.

```text
Use the attached reference image as the single, authoritative source of truth for the product. Ultra-realistic documentary photograph of that exact rigid welded-mesh fence panel, installed as a finished boundary around the car park of a small company in a Belgian business park.

PRODUCT FIDELITY (highest priority): reproduce the panel exactly as shown in the reference — a flat rectangular welded wire mesh with closely spaced vertical wires and more widely spaced horizontal wires, forming tall narrow rectangular openings; keep the same wire gauge ratio, the same mesh spacing and proportions, and the same horizontal stiffening folds running right across the panel at the same relative heights. Reproduce as well the two details visible in the reference: the horizontal wires come much closer together in a denser band along the top and the bottom edges of the panel, and short wire ends protrude beyond the outermost horizontal wire at the top and at the bottom. Each crossing is a simple spot weld with the wires resting flat one on the other, no beads, no collars, no clips. Same finish and colour as the reference: matte dark powder-coated metal, uniform on every wire, with the faint sheen of a coated surface. Do not redraw, simplify, replace or restyle the mesh: no square mesh, no chain-link, no chicken wire, no decorative pattern, no slats, no privacy strips woven into the mesh, no different colour, no added surrounding frame.

SCENE: a finished fence line closing a newly completed company car park, three or four identical panels running away from the camera along the boundary, each fixed to slim dark posts of the same colour. On the near side an empty asphalt surface with a low concrete kerb and plain white bay lines; on the far side a strip of rough grass and a freshly planted young hornbeam hedge still tied to its stakes. A little gravel and dried mud at the foot of the posts, a few leaves caught against the lowest wires. Background, clearly secondary and softer: a low prefabricated hall with grey profiled steel cladding, a light mast, a grey-blue northern sky with broken cloud.

LIGHT AND CAMERA: natural late-afternoon light, low sun from the side, warm but not orange; the mesh casts a fine, physically coherent shadow pattern on the asphalt. 50 mm lens, eye level, three-quarter angle so both the flat face of the nearest panel and the receding fence line are readable. The nearest panel dominates the frame, stays sharp, and its mesh geometry, its folds and its protruding wire ends are clearly identifiable; natural depth of field softening the background.

REALISM: authentic photographic texture — fine grain, dust and a few water marks on the coating, a little pollen and one cobweb between wires, grass that is not perfectly cut, asphalt with real aggregate. Absolutely no CGI or 3D-render look, no plastic surfaces, no unnaturally perfect objects. No people. No visible text, no lettering, no logo, no brand mark, no signage, no dimension callout anywhere in the image.
```

```text
NEGATIF — CGI, 3D render, CAD render, architectural visualisation, video game graphics, plastic look, glossy plastic wires, waxy material, oversaturated colours, HDR halos, illustration, painting, cartoon, watermark, signature, any visible text, letters, numbers, logo, brand mark, label, signage, company sign, number plate, car badge, road marking letters, dimension lines, redesigned mesh, wrong mesh spacing, square mesh, chain-link fence, chicken wire, welded mesh without stiffening folds, extra or missing folds, uniform horizontal spacing from top to bottom, missing denser band at top and bottom, missing protruding wire ends, beaded or lumpy welds, clips at every crossing, added frame around the panel, woven privacy strips, wooden slats, composite panel, white or galvanised silver finish instead of the reference colour, rusty wires, bent or wavy panel, leaning panel, private garden setting, brick house facade, beech hedge, people, influencer, model posing, face to camera, selfie, portrait, hands on the fence, TikTok style, studio lighting, white studio background, flat lighting, lens flare, fisheye distortion, tilt-shift, motion blur, duplicated objects, floating objects, impossible shadows, inconsistent perspective, moiré artifacts, blurry product, product too small, AI artifacts, deformed geometry
```

### Poteaux

`/jardin-cloture/clotures/poteaux`  — *corrigé par l'audit*

**Scène.** Chantier de clôture en cours sur un terrain en pente à la campagne wallonne : poteaux déjà scellés et alignés au cordeau, un panneau posé au sol en attente.

**Référence.** `/images/produits/jardin-cloture/clotures/poteaux/studio-poteau-cloplus-40.webp`

**Correction apportée.** Référence vérifiée et valide (clé categories, fichier présent) et la description de la section H à ailes tubulaires, âme en creux et trous oblongs correspond fidèlement au rendu studio. Défaut bloquant : le prompt impose deux fois une matière fausse — « H-shaped steel profile », « matte dark powder-coated steel ». lib/catalogue.ts donne pour le CLOPLUS 40 : Matière = Aluminium, Revêtement = Thermolaqué polyester, Section 40 × 76 mm. Imposer l'acier au modèle, c'est lui demander une matière que l'entreprise ne vend pas dans cette référence, et ouvrir la porte au rendu galvanisé ou rouillé. Corrigé en aluminium extrudé thermolaqué, avec interdiction explicite du rendu galvanisé, brut ou rouillé. Reste conforme par ailleurs : scène de chantier propre à cette catégorie (terrain en pente, scellements frais, cordeau), aucune personne dans le cadre, réalisme complet, aucune cote ni texte.

```text
Use the attached reference image as the single, authoritative source of truth for the product. Ultra-realistic documentary photograph of that exact fence post, on a fence line being installed on a gently sloping plot in rural Wallonia, Belgium.

PRODUCT FIDELITY (highest priority): reproduce the post section exactly as shown in the reference — an H-shaped extruded profile whose two flanges are closed rectangular tubes, joined by a recessed central web that forms an open channel on each face, with a regular row of small oval holes pierced along the centre of that channel, evenly spaced over the whole length. Keep the same proportions between flange width, web depth and overall section, the same crisp folded edges, the same open hollow tube ends at the top. Same material and finish as the reference: powder-coated extruded aluminium, matte, dark, with a faint even sheen and no bare metal showing. Do not redraw, simplify, round off, replace or restyle the post: no plain round tube, no plain square tube, no I-beam, no wooden post, no concrete post, no added cap, no extra holes, no missing holes, no different colour, no galvanised, raw or rusty metal.

SCENE: work in progress. Three or four identical posts already set upright and aligned along the boundary, their bases sunk into fresh concrete footings still visible as grey collars in the dug earth; the nearest post stands in the foreground, full height, its section clearly readable. A taut mason's string line runs along the tops, a spirit level leans against one post, a spade and a wheelbarrow with leftover concrete sit on the grass for scale, a rigid mesh panel of the same colour lies flat on the ground waiting to be lifted. The slope of the ground is visible: the posts stay vertical while the ground falls away. Background, clearly secondary: a hedgerow, a meadow with a few cattle far off, a farm building in brick and slate, a grey-blue northern sky with moving cloud.

LIGHT AND CAMERA: natural diffuse daylight on a partly cloudy autumn morning; soft, physically coherent shadows; damp earth. 35 mm lens, standing eye level, slight three-quarter angle so the H section of the nearest post and the alignment of the line are both readable. The nearest post dominates the frame and stays sharp from base to top; natural depth of field softening the landscape.

REALISM: authentic photographic texture — wet soil, concrete splashes, mud on the spade, fine scratches on the coating, trampled grass, fine grain. Absolutely no CGI or 3D-render look, no plastic surfaces, no unnaturally perfect objects. No people in the frame. No visible text, no lettering, no logo, no brand mark, no signage, no dimension callout anywhere in the image.
```

```text
NEGATIF — CGI, 3D render, CAD render, architectural visualisation, video game graphics, plastic look, glossy plastic surface, oversaturated colours, HDR halos, illustration, painting, cartoon, watermark, signature, any visible text, letters, numbers, logo, brand mark, label, signage, dimension lines, measurement callouts, redesigned post, round tube post, square tube post, I-beam, C-channel, wooden post, concrete post, post without the central recessed channel, post without oval holes, wrong hole shape, round holes, irregular hole spacing, added decorative cap, added finial, welded brackets not in the reference, bare aluminium, mill finish, galvanised silver finish, rusty post, peeling coating, wrong colour, bent or leaning posts, people, worker in frame, influencer, model posing, face to camera, selfie, portrait, gloved hands holding the post, TikTok style, studio lighting, white studio background, flat lighting, lens flare, fisheye distortion, tilt-shift, motion blur, duplicated objects, floating objects, impossible shadows, inconsistent perspective, blurry product, product too small, AI artifacts, deformed geometry
```

### Caillebotis & marches

`/quincaillerie/caillebotis-marches`  — *corrigé par l'audit*

**Scène.** Passerelle de circulation sur la toiture plate d'un batiment technique en brique, entre les gaines de ventilation, un jour couvert.

**Référence.** `/images/produits/quincaillerie/caillebotis-marches/studio-plancher-o2.webp`

**Correction apportée.** Fond du prompt conforme (fidelite exigee, scene tiree de l'usage reel « passerelle de circulation / plancher de local technique », aucune personne, aucun texte, aucune cote inventee) et chemin de reference verifie : /images/produits/quincaillerie/caillebotis-marches/studio-plancher-o2.webp existe bien dans la cle categories de lib/visuels-produits.json et sur le disque. Deux defauts de realisme : (1) le prompt demande « soft consistent shadows falling through the perforations » sous un ciel couvert et une lumiere diffuse — sous un ciel couvert il n'y a pas d'ombre portee marquee, la consigne se contredit et pousse le modele vers un eclairage incoherent ; (2) le mot « galvanised » risque de faire ajouter le motif cristallin (spangle) absent de la reference, qui montre une surface gris clair mate et uniforme. Corrige : lumiere d'ombre douce coherente avec le couvert, et interdiction explicite de toute texture absente de la reference. Verifie aussi : l'image de reference est bien une tole perforee (bandes de trous ronds separees par des nervures non perforees), pas un caillebotis a mailles — la description du produit dans le prompt est fidele.

```text
Ultra-realistic architectural photograph of a real, finished rooftop service walkway on a low brick technical building in Belgium.

PRODUCT FIDELITY — ABSOLUTE PRIORITY: the attached reference image is the source of truth. Reproduce the panel exactly as shown: a flat, thin, square steel floor panel with a uniform light grey matte metallic finish; its top face covered with dense rows of small round perforations grouped into parallel bands; each band separated by a narrow unperforated raised rib running the full length of the panel; a plain flat continuous edge frame on all four sides; low overall thickness. Keep the same geometry, the same proportions, the same section, the same flat profile, the same material, the same light grey colour, the same matte non-glossy finish, and the exact same perforation pattern — hole shape, hole size, hole spacing and the exact relief of the hole edges as shown on the reference. Add no surface texture that is not visible on the reference: no spangle, no crystalline pattern, no brushed grain, no gloss. Do not redesign, do not simplify, do not stylise, do not substitute a mesh grating or an expanded metal sheet, do not add or remove holes, do not change the rib layout, do not bend or taper the panel.

SCENE: three or four of these identical panels laid end to end as a straight service walkway over a flat bituminous roof, resting on a simple galvanised steel support frame, running between grey ventilation ducts and a small metal plant enclosure. Low brick parapet, overcast northern-European sky, thin winter light, a little moss in the roof seams, dried water marks and light dust on the panel surface, one panel edge slightly scuffed from use. No person in frame.

CAMERA AND LIGHT: 35mm lens, camera at about hip height, standing at the start of the walkway so the nearest panel fills the lower half of the frame and stays large, sharp and clearly identifiable; the roof context recedes behind it. Flat diffuse overcast daylight with no hard cast shadows: only soft contact shading under the panel edges and the support frame, and faint pale dots of daylight passing through the perforations onto the darker roof membrane below. Physically correct dull metallic reflections, natural depth of field with the foreground panel fully in focus.

Strict documentary realism: real materials, real weathering, small imperfections. No text, no markings, no branding anywhere in the image.
```

```text
NEGATIF — CGI, 3D render, videogame render, plastic or rubbery surfaces, glossy toy metal, studio white background, seamless backdrop, product redesigned, simplified, stylised or replaced, mesh grating instead of perforated panel, expanded metal, wrong hole shape, wrong hole size, missing perforations, added perforations, altered rib pattern, changed proportions, changed thickness, changed colour, shiny chrome finish, spangle or crystalline galvanised pattern absent from the reference, hard sunlight shadows under an overcast sky, double shadows, floating panel, impossible shadows, influencer, presenter, model facing camera, selfie, portrait, hands presenting the product, TikTok style, vlog framing, watermark, logo, brand name, printed text, labels, numbers, dimension lines, arrows, callouts, infographic, collage, duplicated identical object, warped geometry, melted edges, bent panel, AI artifacts, oversharpening, heavy HDR, oversaturated colours, lens flare, fisheye, motion blur, blurry product, cartoon, illustration, painting, low resolution
```

### Imitation bois

`/toiture-bardage/bardage/imitation-bois`  — *corrigé par l'audit*

**Scène.** Pignon d'une extension de maison récemment terminée en Wallonie, habillé du haut en bas de ce bardage à tasseaux imitation chêne clair, au-dessus d'un soubassement en brique, en fin d'après-midi.

**Référence.** `/images/produits/toiture-bardage/bardage/imitation-bois/studio-tasseau-imitation-bois.webp`

**Correction apportée.** Fond solide : la scène (pignon de maison) colle exactement à l'usage validé (« habillage de façade », « pignon de maison »), la description produit correspond à l'image studio vérifiée (tasseaux à sommet plat, entraxe régulier, fond anthracite visible au creux, chêne clair satiné), le décor n'est réutilisé nulle part ailleurs, aucune personne imposée. Trois défauts réels : (1) « roughly two storeys tall » est un chiffre d'échelle inventé, interdit par le brief ; (2) l'interdiction du rendu CGI / plastique / objet trop parfait n'existe que dans le négatif, alors que la règle 3 exige de l'énoncer explicitement — beaucoup de modèles image ignorent le champ négatif ; (3) rien n'interdit qu'un objet de contexte porte une marque visible. Chemin de référence vérifié et exact.

```text
Ultra-realistic architectural photograph of a finished residential project. The product shown in the attached reference image must be reproduced exactly as it is: the same steel cladding panel with lengthwise raised battens of square section and flat tops, the same number of battens per panel and the same even spacing between them, the same deep narrow shadow gaps, the same flat dark anthracite backing strip visible at the bottom of each gap, the same folded sheet-metal edges, the same light oak wood-grain printed finish with its exact warm pale tone, its satin low-gloss sheen and its grain running along the battens. The reference image is the authority on shape, geometry, proportion, section, material, colour and finish. Do not redraw, restyle, simplify or replace the product. Do not turn it into real solid timber. Do not add, remove or re-space battens. Do not round, widen or narrow the battens. Do not change the colour, the sheen or the direction of the grain.

Scene: the street-facing gable of a newly completed house extension in Wallonia, Belgium. The whole upper part of the gable is clad with these panels installed vertically, battens running continuously from the top of the masonry to the roof edge, forming a long ribbed wood-look surface with crisp vertical shadow lines. The lower part of the wall is red-brown Belgian brick with a light mortar joint. A tall window with slim dark grey aluminium frames sits at the junction, reflecting the sky. A pre-weathered zinc gutter and a slim dark downpipe run along the eaves. In front, a strip of gravel, a clipped hornbeam hedge, a young birch and a concrete terrace slab. A neighbouring brick party wall is visible at the edge of the frame. Late afternoon in early autumn, soft hazy sunlight coming from the side at a low angle, grazing the battens so each one casts a thin defined shadow onto the dark background strip; a mostly overcast northern sky with pale breaks of blue.

Photography: shot on a full-frame camera with a 35 mm lens, eye level, slightly off-axis three-quarter view so both the face of the cladding and the depth of the battens read clearly, verticals kept straight. Natural daylight only, physically correct soft shadows, realistic specular reflections on the metal and on the window glass, natural shallow depth of field with the cladding fully sharp and the hedge and background gently softened.

Realism is mandatory and must be stated in the image itself: this has to look like a real photograph taken on site, never a CGI render, never an architectural visualisation, never a game engine image. No plastic, waxy or rubbery surfaces. No flawless, untouched, over-clean objects. Fine real-world texture everywhere: subtle print grain in the wood-look finish, faint dust and a few water marks near the bottom of the panels, tiny irregularities in the brick, a few fallen leaves on the gravel, a slightly uneven gravel line. Realistic colour balance, no boosted saturation, no rendering artefacts.

Every object in the frame must be plain and unbranded: no readable text, no logo, no signage, no label, no sticker, no house number anywhere in the image.

The cladding occupies a large, clearly identifiable part of the frame and stays the subject; the house and garden are secondary context only. No people are needed; if one appears for scale, keep them small, at the edge of the frame, turned away, never in the centre and never overlapping the cladding.
```

```text
NEGATIF — CGI, 3D render, architectural visualisation look, video game look, plastic or rubbery surfaces, waxy materials, over-smooth flawless finish, perfect untouched objects, AI artifacts, warped or duplicated ribs, uneven or invented batten spacing, extra or missing battens, rounded or bulging battens, real solid wood planks, natural timber knots, different wood tone, orange or reddish wood, high-gloss varnish, changed colour, changed profile, simplified product, floating product, white studio background, cut-out look, influencer, content creator, presenter, avatar, model posing, face to camera, selfie, portrait, hands holding the product, person in the centre, person blocking the cladding, TikTok or reels style, collage, split screen, text, lettering, captions, watermarks, logos, brand names, signage, labels, stickers, house numbers, dimension lines, measurement callouts, arrows, icons, oversaturation, HDR halos, heavy vignetting, lens flare, bloom, motion blur, blurry product, oversharpening, fisheye distortion, tilted horizon, converging verticals, harsh midday flash, tropical or Mediterranean vegetation, palm trees, American suburban houses
```

### Panneau ECO Eurocopre

`/toiture-bardage/panneaux-isoles/eurocopre-monolamiera-eco`  — *corrigé par l'audit*

**Scène.** Hangar agricole neuf dans la campagne wallonne dont la toiture et le haut de façade viennent d'être fermés avec ces panneaux sandwich anthracite, les derniers panneaux encore en cours de pose.

**Référence.** `/images/produits/toiture-bardage/panneaux-isoles/eurocopre-monolamiera-eco/studio-panneau-isole-eco.webp`

**Correction apportée.** Défaut de fidélité réel et bloquant : le prompt demande « tall trapezoidal ribs », alors que l'image studio vérifiée montre des nervures BASSES, à peine saillantes sur de larges plages plates. Le modèle image va exagérer la hauteur de nervure et produire un panneau qui n'est plus le produit. Deuxième problème : le télescopique (« telehandler ») porte toujours une marque et un marquage constructeur visibles — la règle « aucune marque, aucun logo, aucun texte » n'est pas tenue côté positif. Troisième : l'interdiction du CGI n'est que dans le négatif. Le reste est bon : scène (hangar agricole) conforme à l'usage validé, âme isolante crème visible en rive décrite correctement, décor distinct des deux autres, deux poseurs de dos et au loin (échelle légitime, ni au centre ni masquant le produit). Chemin de référence vérifié et exact.

```text
Ultra-realistic documentary photograph of a real building project nearing completion. The product shown in the attached reference image must be reproduced exactly as it is: the same insulated sandwich panel with a profiled steel outer skin carrying low trapezoidal ribs that stand only slightly proud of wide flat pans, at exactly the rib height, rib width, rib count and rib spacing shown in the reference and no more; the same fine secondary stiffening grooves running along the flat pans between the ribs; the same thin pale cream-beige insulating core visible as a continuous layer under the steel skin at every cut edge; the same crisp folded side laps; the same matte to satin dark anthracite grey colour with its slightly cool tone. The reference image is the authority on shape, geometry, proportion, section, material, colour and finish. Do not redraw, restyle, simplify or replace the product. Do not exaggerate the ribs: they are shallow, not tall, not deep, not steep. Do not turn it into a thin single-skin sheet and do not hide the insulating core at the edges. Do not add, remove or re-space ribs, do not change the rib shape, and do not change the colour or the sheen.

Scene: a newly built farm shed in the open Walloon countryside, Belgium, on the day the envelope is being closed. The long roof slope and the upper part of the side facade are already fully covered with these panels laid lengthwise, ribs running straight up the slope in perfect alignment, side laps repeating across the whole surface; the dark grey planes catch the sky in long soft reflections. Two or three panels are still being positioned at the far end of the roof, one of them slung on soft slings from a plain unbranded telehandler with no markings and no decals, leaving a short open section where the galvanised steel portal frame and purlins are visible. Below, a fresh concrete slab, a bare concrete-block base wall, a stack of remaining panels on timber bearers held by a plain strap, and an open bay showing the shadowed interior. Around the shed, grazed pasture, a muddy access track with tyre prints, a line of bare poplars and a hedgerow in the distance. Overcast northern European weather with broken cloud, diffuse silver daylight, a few brighter patches on the fields, damp ground after rain.

Photography: shot on a full-frame camera with a 50 mm lens from a slightly elevated position across the yard, three-quarter view so the roof plane, the facade plane and the panel edge with its visible core are all readable in one frame, verticals kept straight. Natural light only, physically coherent shadows, realistic specular sheen on the coated steel, natural depth of field with the panels sharp and the distant treeline softened.

Realism is mandatory and must be stated in the image itself: this has to look like a real photograph taken on a working site, never a CGI render, never an architectural visualisation, never a game engine image. No plastic, waxy or rubbery surfaces. No flawless, untouched, over-clean objects. Real-world imperfections: mud splashes at the base, dust and fingerprints on the lower panels, a faint chalk mark, slight flexing in the panel being lifted, straw on the concrete, a puddle in the track. Realistic colour balance, no boosted saturation, no rendering artefacts.

Every object in the frame must be plain and unbranded: no readable text, no logo, no machine livery, no company signage, no label and no sticker anywhere in the image, including on the machine, the straps and the stacked panels.

The panels occupy a large, clearly identifiable part of the frame and stay the subject; the shed, machine and landscape are secondary context only. At most two fitters may appear for scale, small, seen from behind or in profile, at the far end of the roof, never in the centre and never overlapping the panel being shown.
```

```text
NEGATIF — CGI, 3D render, architectural visualisation look, video game look, plastic or rubbery surfaces, waxy materials, over-smooth flawless finish, perfect untouched objects, AI artifacts, warped or duplicated ribs, tall exaggerated ribs, deep or steep ribs, uneven or invented rib spacing, extra or missing ribs, rounded ribs, corrugated wavy sheet, thin single-skin sheet, missing insulation core at the edges, exposed fibrous wool core, changed core colour, white or silver panels, glossy mirror finish, changed colour, changed profile, simplified product, floating product, white studio background, cut-out look, influencer, content creator, presenter, avatar, model posing, face to camera, selfie, portrait, worker in the centre, person blocking the panels, hands holding the product, TikTok or reels style, text, lettering, captions, watermarks, logos, brand names, machine livery, company signage, labels, stickers, decals, dimension lines, measurement callouts, arrows, icons, oversaturation, HDR halos, heavy vignetting, lens flare, bloom, motion blur, blurry product, oversharpening, fisheye distortion, tilted horizon, converging verticals, harsh midday flash, dramatic sunset sky, American barn, tropical vegetation, palm trees
```

### Profil 30.200.1000

`/toiture-bardage/toles-profilees/profil-30-200-1000`  — *corrigé par l'audit*

**Scène.** Carport en ossature bois à toiture monopente fraîchement terminé dans un jardin de banlieue belge, couverture en tôle profilée anthracite vue de trois quarts au-dessus, sous une pluie fine d'automne.

**Référence.** `/images/produits/toiture-bardage/toles-profilees/profil-30-200-1000/studio-tole-profilee-30-200-1000.webp`

**Correction apportée.** La description produit est juste : l'image studio vérifiée montre bien une tôle simple peau, nervures trapézoïdales basses à sommet plat, rainure de raidissage dans chaque plage, rive fine sans âme — et la scène carport correspond à l'usage validé (« toiture de carport »). Trois incohérences à corriger. (1) « from ridge to eaves » : un carport est à toiture monopente, il n'a pas de faîtage — la scène demandée est contradictoire. (2) « the sheets are fixed onto visible planed timber purlins » : depuis une fenêtre d'étage on voit le dessus des tôles, pas les pannes qui sont dessous — la structure n'est lisible qu'en rive. (3) « A dark grey family car is parked underneath » : une voiture affiche toujours logo de marque et plaque d'immatriculation, donc du texte et une marque visibles, ce que le brief interdit. S'y ajoute l'interdiction du CGI reléguée au seul champ négatif. Chemin de référence vérifié et exact.

```text
Ultra-realistic photograph of a small finished building project. The product shown in the attached reference image must be reproduced exactly as it is: the same single-skin profiled steel sheet with low trapezoidal ribs running lengthwise, the same number of ribs across the sheet width and the same regular spacing between them, the same shallow rib height and narrow flat-topped rib shape standing proud of wide flat pans, the same single fine stiffening line running along each flat pan, the same thin cut edges with no core and no visible thickness beyond the sheet itself, the same matte to satin dark anthracite grey coating with its slightly cool tone. The reference image is the authority on shape, geometry, proportion, section, material, colour and finish. Do not redraw, restyle, simplify or replace the product. Do not turn it into a thick insulated sandwich panel, a corrugated wavy sheet or a tile-shaped roofing sheet. Do not add, remove or re-space ribs, do not change the rib shape or the rib height, and do not change the colour or the sheen.

Scene: a freshly completed timber-frame carport with a single-slope mono-pitch roof, beside a detached brick house in a Belgian suburb. The roof is covered with these profiled sheets laid side by side with overlapping side laps, ribs running straight down the slope from the high edge to the low edge, the repeating lines drawing long parallels across the whole roof; a dark eaves trim and a slim gutter close the low edge, and along the open sides the planed timber purlins, beam and posts of the frame are visible under the sheet edge. Underneath, the shaded empty parking bay on a paved surface, with a garden hose reel and a stacked pile of firewood against the far post. Around it, a lawn with fallen leaves, a low brick garden wall, a clipped hedge, and the rear facade of the house in dark red brick with white-framed windows. Late autumn, light drizzle just stopping, thick even overcast, cool diffuse daylight, water beading and running along the rib valleys, a few wet leaves stuck on the sheets, damp reflections on the paving.

Photography: shot on a full-frame camera with a 35 mm lens from a slightly elevated position, as if from a first-floor window of the house, so the roof plane fills a large part of the frame and the rib profile and side laps are clearly readable, with the structure and garden receding below; verticals kept straight. Natural light only, physically coherent soft shadows, realistic wet specular reflections on the coated steel, natural depth of field with the roof sheets fully sharp and the garden background gently softened.

Realism is mandatory and must be stated in the image itself: this has to look like a real photograph taken from a window, never a CGI render, never an architectural visualisation, never a game engine image. No plastic, waxy or rubbery surfaces. No flawless, untouched, over-clean objects. Real-world imperfections: water droplets and drying streaks, a faint scuff near a fixing, slight dust on the flat pans, small knots and colour variation in the timber, a hairline gap in the trim, moss in a paving joint. Realistic colour balance, no boosted saturation, no rendering artefacts.

Every object in the frame must be plain and unbranded: no readable text, no logo, no signage, no label, no sticker, no vehicle, no number plate and no house number anywhere in the image.

The profiled sheets occupy the dominant, clearly identifiable part of the frame and stay the subject; the carport and garden are secondary context only. No people are needed; if one appears for scale, keep them small, at the edge of the frame, turned away, never in the centre and never overlapping the roof surface.
```

```text
NEGATIF — CGI, 3D render, architectural visualisation look, video game look, plastic or rubbery surfaces, waxy materials, over-smooth flawless finish, perfect untouched objects, AI artifacts, warped or duplicated ribs, uneven or invented rib spacing, extra or missing ribs, tall or deep ribs, rounded or wavy corrugation, sinusoidal sheet, tile-profile roofing, thick insulated sandwich panel, visible foam core, galvanised silver or white sheets, rusty sheets, glossy mirror finish, changed colour, changed profile, simplified product, floating product, white studio background, cut-out look, ridge line, two-sided gable roof on the carport, car, van, vehicle badge, number plate, influencer, content creator, presenter, avatar, model posing, face to camera, selfie, portrait, person on the roof, person in the centre, hands holding the product, TikTok or reels style, text, lettering, captions, watermarks, logos, brand names, signage, labels, stickers, house numbers, dimension lines, measurement callouts, arrows, icons, oversaturation, HDR halos, heavy vignetting, lens flare, bloom, motion blur, blurry product, oversharpening, fisheye distortion, tilted horizon, converging verticals, harsh midday sun, dramatic sunset sky, American suburban house, tropical vegetation, palm trees
```
