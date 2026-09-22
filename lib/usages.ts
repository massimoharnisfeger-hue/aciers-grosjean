/**
 * Ce a quoi sert chaque famille de produits — un texte par categorie.
 *
 * GENERE puis VERIFIE, ET EN ATTENTE DE RELECTURE DU PROPRIETAIRE.
 *
 * Pourquoi ce fichier existe : le site officiel ne decrit les usages que pour
 * 141 fiches sur 495. Ecrire un usage par produit aurait ete de l'invention ;
 * un usage par FAMILLE est verifiable par n'importe quel professionnel du
 * metier. Decision du proprietaire le 22/09, qui relit avant publication.
 *
 * Regles tenues a l'ecriture, et re-verifiees par une seconde passe qui a
 * corrige 31 des 54 textes : aucune norme, aucune certification,
 * aucun chiffre (charge, portee, epaisseur, duree), aucune promesse
 * commerciale, aucune affirmation sur l'entreprise. Rien que l'usage general
 * de la famille.
 *
 * Le texte du site officiel prime toujours : quand une fiche porte une
 * section « Applications » relevee sur aciersgrosjean.be, c'est elle qui
 * s'affiche, et ce fichier ne sert alors a rien (voir lib/onglets.ts).
 */
export type UsageCategorie = { texte: string; exemples: string[] };

export const USAGES: Record<string, UsageCategorie> = {
  "/acier/armatures-beton/rond-a-beton-lamine-a-chaud": {
    texte: "Le rond à béton est la barre d'armature que l'on noie dans le béton pour lui apporter la résistance à la traction qui lui manque. Ses crénelures en surface assurent l'accrochage entre l'acier et le béton. Sur chantier, les barres sont coupées, cintrées et ligaturées en cages ou en nappes avant le coulage.",
    exemples: ["semelles de fondation", "dalles et planchers", "poteaux et poutres béton", "murs de soutènement", "chaînages"],
  },
  "/acier/armatures-beton/rond-a-beton-lamine-a-froid": {
    texte: "Le rond à béton laminé à froid remplit la même fonction d'armature, sur des sections plus fines que les barres laminées à chaud. Crénelé lui aussi, il se coupe et se cintre facilement, ce qui le destine aux ouvrages de faible épaisseur et aux armatures secondaires qui complètent les barres principales.",
    exemples: ["chapes armées", "cadres et étriers", "petits massifs béton", "seuils et linteaux", "ligatures d'armature"],
  },
  "/acier/armatures-beton/treillis-soudes": {
    texte: "Le treillis soudé est une nappe de fils d'acier soudés en quadrillage, qui répartit l'armature sur toute la surface d'un ouvrage plutôt que barre par barre. Il se pose en panneaux entiers, avec recouvrement entre panneaux voisins, ce qui simplifie l'armature des grandes surfaces, dalles comme voiles.",
    exemples: ["dalles de terrasse", "planchers béton", "chapes et radiers", "dallage de hangar", "murs banchés"],
  },
  "/acier/armatures-beton/treillis-soudes-depassants": {
    texte: "Le treillis à dépassants est un treillis dont les fils dépassent du panneau sur un ou plusieurs bords. Ces dépassants servent de zone de recouvrement avec le panneau voisin et assurent la continuité de l'armature d'un panneau à l'autre.",
    exemples: ["continuité entre panneaux", "grandes dalles", "reprises de bétonnage", "dallage de hangar", "liaison de nappes"],
  },
  "/acier/poutrelles/hea": {
    texte: "La poutrelle HEA est un profilé en H à ailes larges, utilisé comme élément porteur d'une ossature métallique. La largeur de ses semelles lui donne une inertie plus équilibrée entre ses deux axes que celle d'un profilé en I, ainsi qu'une large surface d'appui pour les platines et les boulonnages. Elle s'emploie donc aussi bien en poteau qu'en poutre.",
    exemples: ["poteaux de charpente", "poutres de plancher", "ossature de hangar", "portiques métalliques", "renfort de structure"],
  },
  "/acier/poutrelles/heb": {
    texte: "La poutrelle HEB appartient à la même famille de profilés en H à ailes larges, avec une âme et des semelles plus épaisses que la HEA de même désignation. On la retient quand les charges à reprendre sont plus importantes ou quand l'encombrement en hauteur doit rester limité.",
    exemples: ["poteaux porteurs", "poutres principales", "ossature de bâtiment", "supports de machine", "renfort structurel"],
  },
  "/acier/poutrelles/ipe": {
    texte: "La poutrelle IPE est un profilé en I dont la hauteur domine la largeur, forme qui concentre la matière là où la flexion la sollicite. Posée horizontalement sur appuis, elle sert couramment à franchir une ouverture ou à porter un plancher.",
    exemples: ["linteau d'ouverture", "solives de plancher", "poutre de reprise", "charpente de hangar", "support de mezzanine"],
  },
  "/acier/poutrelles/upn": {
    texte: "La poutrelle UPN est un profilé en U, ouvert sur une face. Cette section se pose contre un mur ou en rive d'un ouvrage, reçoit une pièce dans sa gorge, ou s'assemble dos à dos pour former un caisson.",
    exemples: ["encadrement de trémie", "chevêtre de plancher", "rives et seuils", "assemblage dos à dos", "renfort de châssis"],
  },
  "/acier/profiles/carre-plein": {
    texte: "Le carré plein est une barre massive à section carrée, sans creux. Ses faces planes facilitent le positionnement, le traçage, la soudure et le perçage, et la matière pleine lui donne de la rigidité sur une section réduite.",
    exemples: ["barreaudage de grille", "garde-corps", "pieds de mobilier", "entretoises soudées", "pièces usinées"],
  },
  "/acier/profiles/corniere-egale": {
    texte: "La cornière sert à former un angle rigide : renfort d'assemblage, encadrement, support ou protection d'arête. À ailes égales, les deux faces jouent le même rôle, ce qui la rend polyvalente dans les cadres et les ossatures légères.",
    exemples: ["renfort d'angle", "encadrement de trappe", "support d'étagère", "protection d'arête", "cadre de portail"],
  },
  "/acier/profiles/corniere-inegale": {
    texte: "La cornière inégale remplit le même rôle d'angle rigide, avec une aile plus longue que l'autre. On la retient quand les deux faces n'ont pas la même fonction : l'une sert d'appui ou de fixation, l'autre de retombée ou de rive.",
    exemples: ["console d'appui", "support de marche", "rive de dalle", "fixation murale", "habillage de rive"],
  },
  "/acier/profiles/fer-t": {
    texte: "Le fer T présente une âme perpendiculaire à une table, ce qui en fait une pièce de jonction et de raidissement. L'âme sépare ou guide deux éléments, la table sert d'appui ou de fixation.",
    exemples: ["montant de cloison", "jonction de panneaux", "piquet de clôture", "raidisseur de tôle", "cadre de vitrage"],
  },
  "/acier/profiles/large-plat": {
    texte: "Le large plat est une barre laminée de section rectangulaire, plus large que le plat courant. Sa largeur en fait une base de pièce à découper, à percer ou à souder, quand il faut une surface d'appui plutôt qu'une simple barre.",
    exemples: ["platine d'appui", "semelle de poteau", "plaque de répartition", "pièces découpées", "renfort soudé"],
  },
  "/acier/profiles/plat": {
    texte: "Le plat est la barre rectangulaire courante de la construction métallique et de la ferronnerie. Il se coupe, se perce, se cintre et se soude facilement, et sert autant de pièce d'assemblage que d'élément visible d'un ouvrage.",
    exemples: ["lisse de garde-corps", "goussets et éclisses", "cadre de portail", "entretoises", "sabots de fixation"],
  },
  "/acier/profiles/rond-plein": {
    texte: "Le rond plein lisse est une barre cylindrique massive, sans crénelure. Sa section régulière convient aux pièces qui tournent, qui traversent ou qui travaillent en traction, ainsi qu'au barreaudage décoratif.",
    exemples: ["axe de pivot", "tirants et entretoises", "barreaudage décoratif", "broches et goujons", "pièces tournées"],
  },
  "/acier/toles/tole-corten": {
    texte: "La tôle corten est un acier dit auto-patinable : exposée à l'air, sa surface développe une couche d'oxydation brune qui lui donne son aspect caractéristique. Elle est employée brute, sans peinture, pour ce rendu en extérieur. À la livraison, cette teinte n'est pas encore formée.",
    exemples: ["bardage décoratif", "jardinières", "brise-vue de jardin", "habillage de façade", "bordures paysagères"],
  },
  "/acier/toles/tole-galvanisee": {
    texte: "La tôle galvanisée est une tôle d'acier revêtue d'une couche de zinc qui la protège de la corrosion. Elle s'emploie telle quelle, sans peinture, pour les pièces exposées à l'humidité ou aux intempéries. Découpe et perçage mettent l'acier à nu sur les tranches.",
    exemples: ["habillages extérieurs", "gaines et goulottes", "carters et capotages", "supports de couverture", "pièces exposées à l'humidité"],
  },
  "/acier/toles/tole-laminee-a-chaud": {
    texte: "La tôle laminée à chaud est la tôle d'acier brute, à surface calaminée, destinée aux travaux de construction et de mécano-soudure. Elle se découpe, se perce, se plie et se soude, et reçoit ensuite une peinture ou un traitement de surface selon l'usage.",
    exemples: ["platines et goussets", "pièces mécano-soudées", "cuves et bennes", "renforts de structure", "semelles de poteau"],
  },
  "/acier/toles/tole-laminee-a-froid": {
    texte: "La tôle laminée à froid se distingue par une surface lisse et régulière et par de faibles épaisseurs. Elle convient à la tôlerie fine, au pliage et aux pièces qui doivent recevoir une finition soignée. Nue, elle n'a aucune protection contre la corrosion et reçoit en général une peinture ou un revêtement.",
    exemples: ["capotages et habillages", "pièces pliées", "mobilier métallique", "tôlerie fine", "supports peints"],
  },
  "/acier/toles/tole-larmee": {
    texte: "La tôle larmée porte des reliefs en saillie qui rompent la surface et limitent le glissement. Elle est employée pour les surfaces sur lesquelles on marche ou on roule, à l'intérieur comme à l'extérieur.",
    exemples: ["marches d'escalier", "plancher de mezzanine", "rampes et seuils", "plateaux de remorque", "trappes de visite"],
  },
  "/acier/toles/tole-perforee": {
    texte: "La tôle perforée est ajourée de trous répartis sur toute sa surface, en trous ronds, en trous carrés ou en perforation aléatoire. Elle ferme physiquement un espace tout en laissant passer l'air, la lumière et la vue, et sert aussi bien de protection que d'élément décoratif.",
    exemples: ["grilles de ventilation", "habillage de façade", "brise-vue", "protection de machine", "faux-plafond"],
  },
  "/acier/toles/tole-quarto": {
    texte: "La tôle quarto est une tôle forte, employée quand l'ouvrage demande une épaisseur que les tôles minces n'offrent pas. Elle se découpe, se soude et se grenaille, et sert de base aux pièces massives de chaudronnerie et de construction lourde.",
    exemples: ["platines d'ancrage", "pièces de chaudronnerie", "semelles épaisses", "plaques d'usure", "découpes lourdes"],
  },
  "/acier/tubes/tube-carre": {
    texte: "Le tube carré est un profilé creux dont la matière est répartie loin du centre, ce qui lui donne de la rigidité en flexion et en torsion sans le poids d'une section pleine. Ses faces planes simplifient l'aboutage, la soudure et la fixation d'accessoires.",
    exemples: ["ossature de portail", "poteaux de structure", "garde-corps", "mobilier métallique", "bâtis et supports"],
  },
  "/acier/tubes/tube-rectangulaire": {
    texte: "Le tube rectangulaire est un profilé creux dont les deux dimensions diffèrent : sa rigidité n'est donc pas la même dans les deux sens, et on l'oriente grande dimension dans le sens de la flexion. On l'emploie pour les éléments horizontaux d'une ossature légère et les traverses.",
    exemples: ["traverse de portail", "lisses de clôture", "ossature légère", "cadres de châssis", "bâtis soudés"],
  },
  "/acier/tubes/tube-rond": {
    texte: "Le tube rond est un profilé creux à section circulaire, sans arête, qui se comporte de la même façon dans toutes les directions. Il sert d'élément de structure, de pièce que l'on saisit à la main, ou de fourreau pour protéger un câble ou une gaine.",
    exemples: ["main courante", "poteaux de barrière", "structures tubulaires", "fourreaux et manchons", "mobilier et agrès"],
  },
  "/aluminium/profiles/corniere-egale": {
    texte: "La cornière égale en aluminium forme un angle à deux ailes de même largeur, utilisé pour rigidifier un assemblage ou reprendre une arête. Sa légèreté et sa tenue naturelle à la corrosion la destinent aux ouvrages manipulés, démontables ou exposés à l'humidité. Elle se coupe et se perce avec de l'outillage courant, ce qui permet de l'ajuster sur place.",
    exemples: ["renfort d'angle de caisson", "encadrement de panneau", "protection d'arête", "support de tablette", "finition de chant"],
  },
  "/aluminium/profiles/plat": {
    texte: "Le plat en aluminium est une barre à section rectangulaire, employée comme pièce d'assemblage, de liaison ou d'habillage. On l'utilise là où une section pleine légère suffit à tenir, entretoiser ou recouvrir. Il se perce et se recoupe avec de l'outillage courant pour fabriquer des pièces sur mesure.",
    exemples: ["platine de fixation", "entretoise entre montants", "barre de maintien", "habillage de chant", "gabarit d'atelier"],
  },
  "/aluminium/profiles/profil-t": {
    texte: "Le profil en T en aluminium associe une âme et une semelle, ce qui lui donne un appui d'un côté et une nervure de l'autre. Il sert à réunir deux éléments coplanaires en marquant la jonction, ou à raidir une surface. Sa faible masse le destine aux travaux d'agencement et de finition.",
    exemples: ["jonction entre deux panneaux", "raidisseur de surface", "séparation de revêtements", "profil de finition", "guidage léger"],
  },
  "/aluminium/profiles/profil-u": {
    texte: "Le profil en U en aluminium présente une gorge ouverte qui vient prendre la tranche d'un panneau ou d'une pièce plate. Il sert autant à encadrer et protéger un chant qu'à constituer un rail ou une glissière. Léger et non sujet à la rouille, il s'utilise en intérieur comme en extérieur.",
    exemples: ["encadrement de panneau", "protection de chant", "rail de guidage", "glissière de coulissant", "cache-câbles"],
  },
  "/aluminium/toles/tole-plane": {
    texte: "La tôle plane en aluminium est une feuille lisse destinée à l'habillage, au capotage et à la découpe de pièces. Elle se cisaille, se perce et se plie pour former des faces, des couvercles ou des éléments façonnés. Sa légèreté et sa tenue à la corrosion la rendent courante en agencement, en carrosserie et en enveloppe de machine.",
    exemples: ["habillage de façade", "capotage de machine", "découpe de pièces", "plaque de propreté", "fond de bac"],
  },
  "/aluminium/toles/tole-striee": {
    texte: "La tôle striée en aluminium porte un relief en saillie destiné à limiter le glissement des pieds et des charges. Elle est utilisée pour les surfaces sur lesquelles on marche, on roule ou on dépose du matériel. Son faible poids facilite la pose de trappes et de planchers démontables.",
    exemples: ["marche d'escalier", "plancher de plateforme", "seuil de passage", "fond de remorque", "trappe de visite"],
  },
  "/aluminium/tubes/tube-carre": {
    texte: "Le tube carré en aluminium offre une section fermée à quatre faces planes, commode pour assembler à angle droit et fixer à plat. Il sert d'ossature à des structures légères que l'on souhaite manipuler ou démonter. Ses faces parallèles simplifient le traçage, le perçage et le vissage.",
    exemples: ["ossature de cadre", "piètement de table", "montant de garde-corps", "structure de stand", "châssis léger"],
  },
  "/aluminium/tubes/tube-rectangulaire": {
    texte: "Le tube rectangulaire en aluminium présente deux faces plus larges que les autres, ce qui l'oriente vers les éléments posés à plat ou sollicités dans un seul sens. On l'emploie en traverse, en montant d'encadrement ou en ossature de panneau. Comme le tube carré, il se coupe et se perce avec de l'outillage courant pour composer des cadres.",
    exemples: ["traverse de cadre", "montant d'encadrement", "cadre de panneau", "support de bardage", "barre de renfort"],
  },
  "/aluminium/tubes/tube-rond": {
    texte: "Le tube rond en aluminium est un profil creux sans arête vive, utilisé là où la pièce est saisie à la main ou doit rester discrète. Il sert de main courante, de barreau, de montant ou d'élément de tringlerie. Sa faible masse facilite la manutention et la pose.",
    exemples: ["main courante", "barreaudage de garde-corps", "montant de support", "tringle d'atelier", "structure de mobilier"],
  },
  "/inox/profiles/corniere-egale": {
    texte: "La cornière inox forme un angle rigide à deux ailes de même largeur. On l'emploie pour raidir un assemblage, encadrer une ouverture ou protéger une arête, dans les situations où la pièce reste exposée à l'humidité, aux nettoyages répétés ou à l'extérieur. Elle se perce, se recoupe et se soude comme un profilé courant.",
    exemples: ["renfort d'angle de cadre", "encadrement de trappe", "protection d'arête", "support de tablette", "bordure de plan de travail"],
  },
  "/inox/profiles/plat": {
    texte: "Le plat inox est une barre pleine de section rectangulaire, utilisée comme renfort, support, entretoise ou pièce de liaison. Sa section plate se perce et se boulonne, et se soude à plat contre une autre pièce. On y recourt quand l'élément reste apparent ou travaille en milieu humide.",
    exemples: ["lisse de garde-corps", "platine de fixation", "renfort de portail", "plinthe de protection", "bride de serrage"],
  },
  "/inox/profiles/rond-plein": {
    texte: "Le rond plein inox est une barre cylindrique lisse, employée comme barreau, axe, tige ou entretoise. Il se cintre, s'usine et se soude, et reste généralement apparent, sans finition peinte. On le retrouve aussi bien sur des pièces mécaniques que sur des ouvrages exposés à l'humidité.",
    exemples: ["barreau de garde-corps", "barreau de grille", "axe d'articulation", "tige de guidage", "entretoise"],
  },
  "/inox/toles/tole-plane-304-brossee": {
    texte: "La tôle inox plane à finition brossée sert d'habillage ou de surface de travail là où la matière reste visible et subit des nettoyages fréquents. Elle se découpe, se plie et se perce pour former des panneaux, des capotages ou des pièces de tôlerie. Le brossage donne un satiné orienté dans un sens sur la face concernée, à respecter au moment de la pose.",
    exemples: ["crédence de cuisine", "habillage mural", "protection de porte", "plan de travail", "panneau de signalétique"],
  },
  "/inox/tubes/tube-carre": {
    texte: "Le tube carré inox est un profilé creux à faces planes, utilisé pour monter des cadres et des structures légères. Ses faces facilitent les coupes d'angle, les soudures et la fixation d'accessoires. On le choisit quand l'ossature reste apparente ou se trouve en milieu humide.",
    exemples: ["cadre de portail", "piètement de table", "structure de garde-corps", "ossature de meuble", "support d'équipement"],
  },
  "/inox/tubes/tube-rectangulaire": {
    texte: "Le tube rectangulaire inox est un profilé creux dont les deux côtés de la section sont de largeurs différentes. On l'emploie en traverse, en montant ou en cadre, quand cette section allongée s'accorde mieux à la géométrie de l'ouvrage qu'un tube carré. Ses faces planes simplifient l'assemblage par soudure ou par vis.",
    exemples: ["traverse de cadre", "montant de châssis", "encadrement de panneau", "support d'habillage", "ossature légère"],
  },
  "/inox/tubes/tube-rond": {
    texte: "Le tube rond inox est un profilé creux cylindrique, employé comme élément d'ossature légère ou comme pièce apparente saisie à la main. Sa forme sans arête convient aux mains courantes, aux barreaudages et aux piètements. Il s'assemble par soudure ou par raccords.",
    exemples: ["main courante", "poteau de garde-corps", "barreaudage de balcon", "piètement de mobilier", "portant de vêtements"],
  },
  "/jardin-cloture/amenagement/bordures": {
    texte: "La bordure délimite une surface au sol et retient les matériaux de part et d'autre : elle sépare une pelouse d'un massif, contient un gravier ou un paillage et matérialise le tracé d'une allée. Posée le long du tracé, elle donne une arête nette là où deux revêtements se rejoignent.",
    exemples: ["séparation pelouse et massif", "contour d'allée gravillonnée", "retenue de paillage", "délimitation de potager", "bordure de terrasse"],
  },
  "/jardin-cloture/clotures/fixations": {
    texte: "Les fixations assurent la liaison entre le panneau de clôture et son poteau : elles maintiennent le panneau en place et transmettent au poteau les efforts appliqués à la clôture. La famille comprend aussi les accessoires de pose, notamment les outils servant au montage ou au serrage des brides.",
    exemples: ["fixation d'un panneau sur poteau", "montage d'une clôture rigide", "serrage des brides au montage", "démontage puis repose d'un panneau", "remplacement d'une bride"],
  },
  "/jardin-cloture/clotures/panneaux-rigides": {
    texte: "Le panneau rigide forme le remplissage de la clôture : un treillis de fils soudés, raidi par des plis horizontaux, qui ferme une limite en laissant passer la vue. Il se monte entre poteaux et se décline en plusieurs hauteurs et teintes selon la fermeture et l'intégration visuelle recherchées.",
    exemples: ["clôture de jardin privatif", "limite entre deux parcelles", "enclos pour animaux", "fermeture d'une aire de jeux", "clôture de parking d'entreprise"],
  },
  "/jardin-cloture/clotures/poteaux": {
    texte: "Le poteau constitue l'ossature verticale de la clôture : implanté à intervalles réguliers le long du tracé, il reçoit les panneaux, tient leur aplomb et transmet au sol les efforts appliqués à la ligne. Sa longueur se choisit en rapport avec la hauteur du panneau, et son profil détermine le système de fixation employé.",
    exemples: ["support de panneau rigide", "angle de tracé", "pose sur terrain en pente", "départ ou fin de ligne", "remplacement d'un poteau endommagé"],
  },
  "/quincaillerie/caillebotis-marches": {
    texte: "Le caillebotis et la marche métallique forment une surface de circulation ajourée : on marche dessus, l'eau s'évacue au lieu de stagner. La famille couvre les panneaux de plancher et les marches destinées aux escaliers, passerelles et plateformes, en mailles assemblées ou en tôle perforée. On les emploie là où un plancher plein retiendrait l'eau ou la salissure.",
    exemples: ["Plancher de local technique", "Marche d'escalier extérieur", "Passerelle de circulation", "Couverture de fosse", "Platelage de mezzanine"],
  },
  "/quincaillerie/outillage": {
    texte: "L'outillage regroupe les outils qui servent à couper, meuler et ébavurer le métal, en atelier comme sur chantier. Ils interviennent à la découpe elle-même et sur les reprises qui la suivent : ajuster une longueur, casser une arête, nettoyer une surface avant assemblage ou mise en peinture.",
    exemples: ["Coupe de profilé", "Ébavurage d'une découpe", "Préparation avant peinture", "Reprise de cordon de soudure"],
  },
  "/quincaillerie/protection-chimie/colles-etancheite": {
    texte: "Cette famille rassemble les colles, mastics et résines de scellement utilisés au moment de l'assemblage et de la finition. Selon la formulation, le produit colle deux éléments sans perçage, ferme un joint contre l'eau et l'air, ou scelle une tige dans un support maçonné. Ils interviennent en complément d'une fixation mécanique, ou à sa place quand le support ne permet pas de percer.",
    exemples: ["Collage de panneau", "Joint périphérique de châssis", "Scellement de tige filetée", "Étanchéité d'un raccord", "Collage sans perçage"],
  },
  "/quincaillerie/protection-chimie/galvanisation-a-froid": {
    texte: "Les produits de galvanisation à froid déposent un film riche en zinc sur l'acier ; le zinc se corrode avant l'acier et le protège. Ils s'appliquent au pinceau, au rouleau ou en aérosol, ce qui permet de traiter une pièce déjà posée ou une zone que la galvanisation en bain n'atteint plus. La famille comprend aussi les solvants et les finitions qui accompagnent leur mise en œuvre.",
    exemples: ["Retouche après soudure", "Protection d'une coupe", "Reprise d'une rayure", "Traitement d'un assemblage posé"],
  },
  "/quincaillerie/protection-chimie/peintures-primaires": {
    texte: "Les primaires anticorrosion forment la première couche appliquée sur un métal nu : ils accrochent au support et servent de base à la finition. La famille se décline en plusieurs teintes et s'emploie aussi bien comme protection d'un ouvrage avant pose que comme sous-couche d'un système de peinture.",
    exemples: ["Sous-couche avant finition", "Protection d'un ouvrage neuf", "Retouche après découpe", "Mise en peinture d'une ferronnerie"],
  },
  "/quincaillerie/visserie": {
    texte: "La visserie assure les fixations vissées entre tôle, bois et acier. La vis autoforante perce et fixe en une seule opération, sans avant-trou ; la vis à bois se pose dans une ossature ou un support tendre. Le choix se fait selon la nature de l'élément à traverser et celle du support qui reçoit la vis.",
    exemples: ["Fixation de tôle profilée", "Pose de bardage", "Fixation sur ossature bois", "Assemblage tôle sur acier"],
  },
  "/toiture-bardage/bardage/imitation-bois": {
    texte: "Le bardage imitation bois est un profil d'acier dont la face vue reproduit l'aspect de lames de bois posées en tasseaux. Il sert à habiller une paroi, en extérieur comme en intérieur, quand on cherche ce rendu avec un support métallique plutôt qu'avec du bois. C'est un parement décoratif : il couvre et finit un support, il ne le porte pas.",
    exemples: ["habillage de façade", "pignon de maison", "mur intérieur décoratif", "parement de soubassement", "habillage d'abri de jardin"],
  },
  "/toiture-bardage/panneaux-isoles/eurocopre-monolamiera-eco": {
    texte: "Le panneau isolé associe en un seul élément un parement en acier et une âme isolante. Il sert à fermer l'enveloppe d'un bâtiment, en couverture ou en façade, tout en assurant la fonction d'isolation dans la même mise en œuvre. On l'emploie là où l'on veut éviter de superposer une peau et une couche isolante posées séparément.",
    exemples: ["toiture de hangar", "bardage d'atelier", "bâtiment agricole", "couverture de local technique", "façade de bâtiment industriel"],
  },
  "/toiture-bardage/toles-profilees/profil-30-200-1000": {
    texte: "La tôle profilée est une tôle d'acier nervurée utilisée comme peau de couverture ou de bardage. Le profil en nervures lui donne sa rigidité et permet une pose sur ossature, pannes en toiture ou lattage en façade. On la retrouve aussi bien sur des bâtiments que sur des constructions annexes.",
    exemples: ["toiture de carport", "couverture d'abri de jardin", "bardage de hangar", "toiture de garage", "façade de bâtiment agricole"],
  },
};

/** L'usage de la categorie d'un produit, s'il en existe un. */
export const usageDe = (categorie: string): UsageCategorie | undefined => USAGES[categorie];
