/**
 * Contenu éditorial — calqué sur le site réel.
 *
 * Les 16 articles, leurs slugs, leurs titres et leurs plans de H2 viennent du
 * crawl (blueprint § 21.3). Les textes sont réécrits : le crawl donne la
 * structure, pas le corps des articles.
 *
 * Les 8 services et les 4 dépôts suivent les routes de la section 46.
 */

export type Bloc =
  | { type: "p"; texte: string }
  | { type: "liste"; items: string[] }
  | { type: "encadre"; titre: string; texte: string }
  | { type: "tableau"; entetes: string[]; lignes: string[][] };

export type Section = { titre: string; blocs: Bloc[] };

export type Article = {
  slug: string;
  titre: string;
  titreSeo: string;
  descSeo: string;
  chapo: string;
  categorie: string;
  date: string;
  lecture: number;
  sections: Section[];
  liens: { label: string; href: string }[];
};

/* ================================================================== */
/*  ARTICLES — /conseils/{slug}                                        */
/* ================================================================== */

export const articles: Article[] = [
  {
    slug: "acier-corten-qu-est-ce-que-c-est",
    titre: "L'acier corten, qu'est-ce que c'est ?",
    titreSeo: "Qu'est-ce que l'acier corten ? Le guide complet",
    descSeo:
      "Pourquoi le corten rouille sans se détériorer, ses quatre propriétés, où l'utiliser — et les trois choses qu'il ne faut jamais faire avec.",
    chapo:
      "Un acier qui rouille exprès, et dont la rouille le protège. Voici comment ça marche, et ce que ça implique quand on le pose chez soi.",
    categorie: "Corten",
    date: "23 avril 2026",
    lecture: 5,
    sections: [
      {
        titre: "Pourquoi l'acier corten rouille sans se détériorer",
        blocs: [
          {
            type: "p",
            texte:
              "L'acier ordinaire rouille en couches qui s'écaillent : chaque écaille emporte de la matière et découvre du métal neuf, qui rouille à son tour. Le processus ne s'arrête jamais — c'est pour ça qu'une grille non protégée finit par percer.",
          },
          {
            type: "p",
            texte:
              "Le corten est allié au cuivre, au chrome, au nickel et au phosphore. Ces éléments changent la nature de la rouille : au lieu d'une croûte poreuse, il se forme une couche dense, fine et adhérente, qui colle au métal et bloque l'oxygène et l'humidité. La corrosion s'arrête d'elle-même après quelques dixièmes de millimètre. On appelle ça une patine protectrice.",
          },
        ],
      },
      {
        titre: "Les propriétés du corten en quatre points",
        blocs: [
          {
            type: "liste",
            items: [
              "Aucun entretien. Pas de peinture, pas de traitement, pas de reprise. Une fois la patine formée, on n'y touche plus.",
              "Une teinte vivante. Orange vif les premiers mois, brun profond ensuite, avec des variations selon l'exposition à la pluie et au soleil. Deux pièces posées côte à côte ne vieillissent jamais exactement pareil.",
              "Une résistance mécanique supérieure. Le S355J0WP est plus résistant que le S235 courant : à épaisseur égale, la pièce porte davantage.",
              "Une durée de vie longue. En usage extérieur normal, comptez plusieurs décennies sans intervention.",
            ],
          },
        ],
      },
      {
        titre: "Où utiliser le corten",
        blocs: [
          {
            type: "p",
            texte:
              "Partout où la pièce est exposée à l'air libre et peut sécher entre deux pluies : bardage de façade, bordures de massif, bacs à plantes, brise-vue, jardinières, signalétique, mobilier de jardin, habillage d'escalier extérieur.",
          },
          {
            type: "p",
            texte:
              "En revanche, il n'a rien à faire en intérieur — la patine ne se formera pas — ni dans un endroit qui reste humide en permanence.",
          },
        ],
      },
      {
        titre: "Ce qu'il ne faut jamais faire",
        blocs: [
          {
            type: "liste",
            items: [
              "Le poser au contact permanent de la terre ou de l'eau stagnante. Sans cycles secs, la patine ne se forme pas et le corten se corrode comme un acier ordinaire — jusqu'à percer.",
              "L'installer au-dessus d'un béton clair, d'une pierre bleue ou d'une terrasse claire sans protection. Pendant les premiers mois, l'eau de pluie emporte des oxydes qui tachent définitivement.",
              "Le peindre ou le vernir. On annule exactement ce pour quoi on l'a payé.",
            ],
          },
          {
            type: "encadre",
            titre: "Combien de temps pour la patine ?",
            texte:
              "De six à dix-huit mois selon l'exposition. Une façade plein sud battue par la pluie patine vite ; une pièce abritée sous un débord de toit met beaucoup plus longtemps et reste plus claire. C'est normal, et c'est même ce qui fait le charme de la matière.",
          },
        ],
      },
    ],
    liens: [
      { label: "Tôle corten", href: "/acier/toles/tole-corten" },
      { label: "Bordures corten", href: "/jardin-cloture/amenagement/bordures" },
      { label: "10 idées jardin en corten", href: "/conseils/idees-jardin-acier-corten-inspirations" },
    ],
  },

  {
    slug: "bordure-jardin-acier-corten-guide-complet",
    titre: "Bordure jardin corten : guide complet",
    titreSeo: "Bordure de jardin en acier corten : le guide complet",
    descSeo:
      "Hauteur, épaisseur, pose, prix au mètre et l'erreur n°1 à éviter. Tout ce qu'il faut savoir avant de commander une bordure corten.",
    chapo:
      "La bordure corten sépare la pelouse du massif d'un trait net qui vieillit avec le jardin. Reste à choisir la bonne hauteur et la bonne épaisseur — c'est là que ça se joue.",
    categorie: "Corten",
    date: "9 avril 2026",
    lecture: 6,
    sections: [
      {
        titre: "Corten, bois, béton ou plastique : le vrai comparatif",
        blocs: [
          {
            type: "tableau",
            entetes: ["", "Corten", "Bois", "Béton", "Plastique"],
            lignes: [
              ["Durée de vie", "30 ans et plus", "5 à 10 ans", "Très longue", "3 à 8 ans"],
              ["Entretien", "Aucun", "Traitement régulier", "Aucun", "Aucun"],
              ["Courbes", "Se cintre à la main", "Difficile", "Impossible", "Facile"],
              ["Finesse du trait", "2 mm", "20 mm et plus", "60 mm et plus", "3 mm"],
              ["Prix au mètre", "Élevé", "Bas", "Moyen", "Très bas"],
            ],
          },
          {
            type: "p",
            texte:
              "Le corten gagne sur deux points que rien d'autre n'offre ensemble : un trait de 2 mm d'épaisseur qui disparaît visuellement, et une durée de vie qui dépasse celle de la plantation qu'il borde.",
          },
        ],
      },
      {
        titre: "Quelle hauteur choisir",
        blocs: [
          {
            type: "liste",
            items: [
              "100 mm — séparation pelouse / gravier, là où il n'y a pas de dénivelé à retenir.",
              "150 mm — la hauteur passe-partout : massif, potager, allée. C'est celle que nous tenons en stock.",
              "200 mm — retenue de terre légère, massif surélevé de quelques centimètres.",
              "300 mm et plus — vraie retenue de terre. À partir de là, il faut des piquets plus longs et un ancrage sérieux.",
            ],
          },
          {
            type: "p",
            texte:
              "Attention : la hauteur annoncée est la hauteur totale. Il faut enterrer un tiers de la bordure pour qu'elle tienne. Une bordure de 150 mm laisse donc 100 mm visibles.",
          },
        ],
      },
      {
        titre: "Quelle épaisseur",
        blocs: [
          {
            type: "p",
            texte:
              "2 mm pour tout usage de jardin courant. C'est assez rigide pour rester droit et assez souple pour se cintrer à la main sur un rayon large. En dessous, la bordure ondule ; au-dessus, elle devient difficile à courber et le prix grimpe vite.",
          },
          {
            type: "p",
            texte:
              "Pensez aussi que la patine consomme quelques dixièmes de millimètre. Sur une pièce de 2 mm c'est sans conséquence, mais c'est une raison de plus de ne pas descendre à 1 mm.",
          },
        ],
      },
      {
        titre: "La pose, et l'erreur n°1",
        blocs: [
          {
            type: "p",
            texte:
              "L'erreur qu'on voit le plus souvent : poser la bordure directement contre une terrasse en pierre claire ou un béton désactivé. Pendant la formation de la patine, les coulures d'oxyde tachent la surface de façon définitive. Aucun nettoyant ne les enlève complètement.",
          },
          {
            type: "p",
            texte:
              "La parade est simple : ménagez une bande de gravier de dix centimètres entre la bordure et toute surface claire, ou posez la bordure du côté terre. Cela ne coûte rien et évite un regret durable.",
          },
          {
            type: "encadre",
            titre: "Prix au mètre",
            texte:
              "Comptez environ 15 € du mètre courant en hauteur 150 mm, piquets compris. C'est plus cher que le plastique la première année, et moins cher que le bois dès la huitième.",
          },
        ],
      },
    ],
    liens: [
      { label: "Bordures corten et galva", href: "/jardin-cloture/amenagement/bordures" },
      { label: "Poser une bordure, pas à pas", href: "/conseils/comment-poser-bordure-jardin-acier-corten" },
      { label: "Tôle corten", href: "/acier/toles/tole-corten" },
    ],
  },

  {
    slug: "comment-poser-bordure-jardin-acier-corten",
    titre: "Poser une bordure corten, mode d'emploi",
    titreSeo: "Poser une bordure jardin corten : guide pas-à-pas",
    descSeo:
      "Le matériel, les cinq étapes de pose et trois astuces de pro pour une bordure corten droite, stable et durable.",
    chapo:
      "Une bordure corten se pose en une demi-journée, sans béton et sans outillage particulier. À condition de suivre l'ordre.",
    categorie: "Corten",
    date: "24 avril 2026",
    lecture: 5,
    sections: [
      {
        titre: "Ce qu'il vous faut",
        blocs: [
          {
            type: "liste",
            items: [
              "La bordure, et ses piquets d'ancrage (comptez trois piquets par élément de 2,5 m).",
              "Une bêche ou un louchet pour ouvrir la saignée.",
              "Un maillet en caoutchouc — pas un marteau, qui marque la tôle.",
              "Un cordeau et des piquets de traçage.",
              "Une chute de bois pour taper sans déformer le chant.",
              "Des gants : le corten neuf a des arêtes vives.",
            ],
          },
        ],
      },
      {
        titre: "Les cinq étapes",
        blocs: [
          {
            type: "liste",
            items: [
              "1. Tracez. Cordeau tendu pour les lignes droites, tuyau d'arrosage posé au sol pour les courbes — vous voyez le dessin avant de creuser.",
              "2. Ouvrez une saignée au tiers de la hauteur de la bordure, soit 5 cm pour une bordure de 150 mm. Une largeur de bêche suffit.",
              "3. Posez et emboîtez. Les éléments se recouvrent de quelques centimètres ; faites toujours recouvrir dans le sens de la vue principale, la jonction se voit beaucoup moins.",
              "4. Enfoncez les piquets côté terre, jamais côté visible, en tapant à travers la chute de bois.",
              "5. Remblayez des deux côtés et tassez au pied. La terre tassée fait plus pour la stabilité que les piquets.",
            ],
          },
        ],
      },
      {
        titre: "Trois astuces de pro",
        blocs: [
          {
            type: "liste",
            items: [
              "Pour une courbe régulière, cintrez la bordure à plat sur l'herbe avant de la descendre dans la saignée. À la main, progressivement, sur toute la longueur — pas en forçant en un point.",
              "Laissez 2 mm de jeu aux jonctions. Le métal se dilate au soleil, et une bordure posée serrée en août gondole dès la première canicule.",
              "Ne nettoyez pas les traces d'orange des premières semaines. Elles partent seules quand la patine se stabilise, et frotter ne fait que marquer la surface.",
            ],
          },
        ],
      },
    ],
    liens: [
      { label: "Bordures corten et galva", href: "/jardin-cloture/amenagement/bordures" },
      { label: "Le guide complet des bordures", href: "/conseils/bordure-jardin-acier-corten-guide-complet" },
      { label: "Nos dépôts", href: "/depots" },
    ],
  },

  {
    slug: "bac-plantes-acier-corten-exterieur",
    titre: "Bac à plantes en acier corten",
    titreSeo: "Bac à plantes acier corten extérieur : choisir, poser, entretenir",
    descSeo:
      "Corten, plastique, bois ou inox : le comparatif honnête. Taille, drainage, tenue au climat belge et prix réels.",
    chapo:
      "Un bac corten dure plus longtemps que la plupart des plantes qu'on y met. Encore faut-il régler la question du drainage — c'est là que tout se joue.",
    categorie: "Corten",
    date: "23 avril 2026",
    lecture: 6,
    sections: [
      {
        titre: "Corten, plastique, bois ou inox",
        blocs: [
          {
            type: "tableau",
            entetes: ["", "Corten", "Plastique", "Bois", "Inox"],
            lignes: [
              ["Durée de vie", "30 ans +", "5 à 10 ans", "8 à 15 ans", "30 ans +"],
              ["Entretien", "Aucun", "Aucun", "Traitement annuel", "Nettoyage"],
              ["Inertie thermique", "Bonne", "Faible", "Bonne", "Faible"],
              ["Sur mesure", "Oui", "Non", "Oui", "Oui"],
              ["Prix", "Élevé", "Bas", "Moyen", "Très élevé"],
            ],
          },
        ],
      },
      {
        titre: "Le climat belge",
        blocs: [
          {
            type: "p",
            texte:
              "Nos hivers sont humides mais rarement très froids, et nos étés alternent pluie et soleil. C'est exactement le régime de cycles humide/sec dont le corten a besoin pour patiner correctement. Un bac corten vieillit donc très bien chez nous — mieux qu'en climat méditerranéen sec, où la patine met des années à se former.",
          },
          {
            type: "p",
            texte:
              "Point d'attention : le métal conduit le gel. Un bac corten en pleine exposition protège moins les racines qu'un bac en bois. Pour les plantes sensibles, doublez l'intérieur d'une plaque de polystyrène de 2 cm.",
          },
        ],
      },
      {
        titre: "La taille, et l'erreur de drainage",
        blocs: [
          {
            type: "p",
            texte:
              "Pour un arbuste, comptez 40 cm de profondeur minimum ; pour une graminée ou une vivace, 30 cm suffisent. Plus le bac est grand, plus le substrat reste stable en température et en humidité — les petits bacs sèchent en une journée d'été.",
          },
          {
            type: "encadre",
            titre: "L'erreur qui tue le bac",
            texte:
              "Un bac corten sans percement de fond garde l'eau. Les racines pourrissent, et surtout le fond baigne en permanence : la patine ne se forme pas à cet endroit, et c'est précisément là que le bac finit par percer. Exigez un fond percé, ou percez-le vous-même à 8 mm tous les 20 cm, puis posez le bac sur des cales de 2 cm.",
          },
        ],
      },
      {
        titre: "Prix réels",
        blocs: [
          {
            type: "p",
            texte:
              "Un bac de 80 × 40 × 40 cm en 2 mm soudé d'un seul tenant coûte autour de 290 €. C'est trois à quatre fois le prix d'un bac plastique de même contenance, et c'est le dernier que vous achèterez pour cet emplacement.",
          },
          {
            type: "p",
            texte:
              "Le sur-mesure ne coûte pas beaucoup plus cher que le standard : la découpe et le pliage sont les mêmes opérations, seules les cotes changent. Si vous avez une longueur de terrasse à occuper exactement, demandez plutôt que d'adapter.",
          },
        ],
      },
    ],
    liens: [
      { label: "Tôle corten", href: "/acier/toles/tole-corten" },
      { label: "Pliage et façonnage", href: "/services/pliage-faconnage" },
      { label: "Demander un bac sur mesure", href: "/devis" },
    ],
  },

  {
    slug: "brasero-acier-corten-jardin-quel-modele",
    titre: "Brasero corten : lequel choisir ?",
    titreSeo: "Brasero acier corten pour jardin : quel modèle choisir ?",
    descSeo:
      "Les trois formats de brasero corten, les critères qui comptent vraiment et cinq règles d'or pour un usage sûr.",
    chapo:
      "Le corten et le feu vont bien ensemble : la chaleur accélère la patine et le métal ne craint pas les cycles de température. Reste à choisir le format.",
    categorie: "Corten",
    date: "24 avril 2026",
    lecture: 5,
    sections: [
      {
        titre: "Pourquoi un brasero en acier corten",
        blocs: [
          {
            type: "p",
            texte:
              "Un brasero passe sa vie dehors et encaisse des écarts de température extrêmes. La fonte fissure au choc thermique, l'acier peint perd sa peinture dès la première flambée, l'inox se marque en bleu. Le corten, lui, ne fait que patiner plus vite.",
          },
        ],
      },
      {
        titre: "Les trois formats",
        blocs: [
          {
            type: "liste",
            items: [
              "La vasque basse, de 60 à 80 cm de diamètre : la plus conviviale, on s'assoit autour. C'est le format le plus vendu.",
              "Le cube ou le cylindre sur pied : plus haut, plus graphique, il chauffe davantage à hauteur de buste et protège mieux la pelouse.",
              "Le brasero-plancha, avec une couronne plate autour du foyer : il cuisine autant qu'il chauffe. Prévoyez une épaisseur de 4 mm minimum sur la partie cuisson, sinon elle se voile.",
            ],
          },
        ],
      },
      {
        titre: "Quel brasero corten choisir",
        blocs: [
          {
            type: "p",
            texte:
              "L'épaisseur est le seul critère technique qui compte vraiment. En dessous de 3 mm, le fond se déforme après quelques saisons de feu direct. À 4 mm, il tient indéfiniment. Le reste — diamètre, forme, pied — relève du goût et de la place disponible.",
          },
        ],
      },
      {
        titre: "Cinq règles d'or",
        blocs: [
          {
            type: "liste",
            items: [
              "Posez-le sur une surface non combustible et non claire : gravier ou dalle sombre. Jamais directement sur une terrasse en bois ni sur une pierre claire.",
              "Laissez trois mètres de dégagement avec toute façade, haie ou mobilier.",
              "Ne l'éteignez jamais à l'eau : le choc thermique sur un métal à 600 °C n'est bon ni pour le brasero, ni pour vous. Laissez mourir le feu.",
              "Videz les cendres une fois froides. Humides, elles sont corrosives et retiennent l'eau au fond.",
              "Renseignez-vous sur le règlement communal : le feu ouvert est réglementé et parfois interdit en période sèche.",
            ],
          },
        ],
      },
    ],
    liens: [
      { label: "Tôle corten", href: "/acier/toles/tole-corten" },
      { label: "Découpe et pliage sur mesure", href: "/services/pliage-faconnage" },
      { label: "Nos dépôts", href: "/depots" },
    ],
  },

  {
    slug: "idees-jardin-acier-corten-inspirations",
    titre: "10 idées jardin avec l'acier corten",
    titreSeo: "Idées jardin acier corten : 8 inspirations",
    descSeo:
      "Bordures, jardinières, brise-vue, escaliers, fontaines : dix façons d'utiliser le corten au jardin, avec la matière à commander pour chacune.",
    chapo:
      "Le corten est devenu la matière du jardin contemporain. Voici dix usages concrets, du plus simple au plus ambitieux — et ce qu'il faut commander pour chacun.",
    categorie: "Corten",
    date: "23 avril 2026",
    lecture: 5,
    sections: [
      {
        titre: "Pourquoi le corten est devenu la tendance",
        blocs: [
          {
            type: "p",
            texte:
              "Parce qu'il fait exactement ce qu'un jardin demande à un matériau : il change avec les saisons, il ne demande rien, et sa teinte chaude va avec le vert de la végétation comme avec le gris du béton. C'est aussi l'un des rares matériaux qui devient plus beau en vieillissant.",
          },
        ],
      },
      {
        titre: "Les dix idées",
        blocs: [
          {
            type: "liste",
            items: [
              "Bordure de massif — le classique, et le plus rentable. Un trait de 2 mm qui structure tout le jardin. Tôle 2 mm pliée en L, ou bordure prête à poser.",
              "Jardinière sur mesure, aux dimensions exactes de la terrasse. Tôle 2 mm, soudée et percée au fond.",
              "Brise-vue ajouré au laser. Panneau de 1800 × 900 en 2 mm, motif au choix : il masque sans cloisonner et dessine des ombres au sol.",
              "Contremarche d'escalier extérieur. Tôle 3 mm pliée en U, posée sur une structure existante.",
              "Habillage de talus. Plusieurs tôles de 3 mm boulonnées entre elles sur profilés : ça retient la terre et ça remplace un mur.",
              "Numéro de maison découpé. Une chute de 3 mm suffit, et le rendu vaut n'importe quelle plaque du commerce.",
              "Lame d'eau ou fontaine murale. Tôle 3 mm pliée ; l'eau accélère la patine et crée des coulures qu'on recherche ici.",
              "Support de barbecue ou plancha, en 4 mm pour la zone de feu.",
              "Pare-vue de local technique — pompe à chaleur, poubelles, citerne. Tôle perforée ou pleine sur cadre en tube carré.",
              "Chemin de gravier délimité par des bordures basses de 100 mm : le gravier ne migre plus dans la pelouse.",
            ],
          },
        ],
      },
      {
        titre: "Où commander",
        blocs: [
          {
            type: "p",
            texte:
              "Tout part de la tôle corten, disponible en 2, 3, 4 et 5 mm aux formats 2000 × 1000 et 2500 × 1250. On la débite aux cotes et on la plie selon votre plan. Pour les pièces découpées au laser, envoyez un simple croquis coté : on s'occupe du reste.",
          },
        ],
      },
    ],
    liens: [
      { label: "Tôle corten", href: "/acier/toles/tole-corten" },
      { label: "Bordures corten", href: "/jardin-cloture/amenagement/bordures" },
      { label: "Pliage et façonnage", href: "/services/pliage-faconnage" },
    ],
  },

  {
    slug: "caillebotis-acier-guide-achat",
    titre: "Caillebotis acier : guide d'achat",
    titreSeo: "Caillebotis acier : guide d'achat",
    descSeo:
      "Galvanisé, inox ou aluminium ? Maille, portée, charge admissible : les critères de choix d'un caillebotis, et les trois erreurs classiques.",
    chapo:
      "Un caillebotis se choisit sur trois chiffres : la maille, la hauteur de porteur et la portée. Le reste est du détail.",
    categorie: "Guides d'achat",
    date: "24 avril 2026",
    lecture: 6,
    sections: [
      {
        titre: "Qu'est-ce qu'un caillebotis acier",
        blocs: [
          {
            type: "p",
            texte:
              "C'est un plancher ajouré formé de plats verticaux, les porteurs, croisés par des barres torsadées ou lisses. Les porteurs travaillent sur chant : c'est ce qui donne une résistance très élevée pour un poids faible, tout en laissant passer l'eau et la lumière.",
          },
          {
            type: "p",
            texte:
              "On le désigne par deux couples de chiffres, par exemple 30/30 - 30/2 : les 30/30 sont les entraxes de la maille en millimètres, les 30/2 la hauteur et l'épaisseur du porteur.",
          },
        ],
      },
      {
        titre: "Galvanisé, inox ou aluminium",
        blocs: [
          {
            type: "tableau",
            entetes: ["", "Galvanisé", "Inox", "Aluminium"],
            lignes: [
              ["Usage", "Extérieur courant", "Alimentaire, chimie, littoral", "Léger, démontable"],
              ["Tenue", "20 à 50 ans", "Illimitée", "Illimitée"],
              ["Charge", "Élevée", "Élevée", "Modérée"],
              ["Prix", "Référence", "×4 à ×6", "×2 à ×3"],
            ],
          },
          {
            type: "p",
            texte:
              "Pour neuf chantiers sur dix, le galvanisé est le bon choix. L'inox se justifie quand il y a du sel, du chlore ou une contrainte d'hygiène ; l'aluminium quand il faut soulever le panneau à la main régulièrement.",
          },
        ],
      },
      {
        titre: "Les critères de choix",
        blocs: [
          {
            type: "liste",
            items: [
              "La maille. 30/30 est la maille passe-partout. Descendez à 30/10 si des talons fins doivent passer dessus, montez à 70/70 pour un usage purement technique où seul le passage de l'eau compte.",
              "La hauteur du porteur. Elle détermine la portée admissible : 25 mm pour une portée de 70 cm, 30 mm pour 1 m, 40 mm au-delà. Dans le doute, prenez au-dessus.",
              "La charge. Un caillebotis de circulation piétonne courante vise 500 kg/m². Un passage de transpalette demande un calcul.",
              "L'encadrement. Un caillebotis posé sans cornière de rive s'ouvre en éventail sur les bords. La cornière fait partie du produit, pas de l'option.",
            ],
          },
        ],
      },
      {
        titre: "Les trois erreurs à éviter",
        blocs: [
          {
            type: "liste",
            items: [
              "Recouper un caillebotis à la meuleuse sans refermer la coupe. Les porteurs libérés s'écartent et le panneau perd sa rigidité. Toute recoupe demande une cornière de reprise soudée.",
              "Oublier les pattes de fixation. Un caillebotis non fixé se soulève au passage d'une roue, et c'est un accident.",
              "Choisir la maille sur le seul critère esthétique. Une maille large sous un escalier extérieur laisse passer les clés, les téléphones et les talons.",
            ],
          },
        ],
      },
    ],
    liens: [
      { label: "Caillebotis et marches", href: "/quincaillerie/caillebotis-marches" },
      { label: "Cornières acier", href: "/acier/profiles/corniere-egale" },
      { label: "Demander un devis", href: "/devis" },
    ],
  },

  {
    slug: "vente-acier-particulier-belgique",
    titre: "Acheter de l'acier en Belgique",
    titreSeo: "Acheter de l'acier en Belgique : tarifs, découpe et retrait",
    descSeo:
      "Peut-on acheter de l'acier quand on est particulier ? Quel acier pour quel projet, comment commander, et à quels délais s'attendre.",
    chapo:
      "Oui, un particulier peut acheter de l'acier chez un négociant, aux mêmes prix qu'un professionnel. Voici comment ça se passe concrètement.",
    categorie: "Guides d'achat",
    date: "24 avril 2026",
    lecture: 7,
    sections: [
      {
        titre: "Acheter de l'acier quand on est particulier",
        blocs: [
          {
            type: "p",
            texte:
              "Il n'y a aucune obligation d'avoir un numéro de TVA ni un compte professionnel. Les particuliers représentent une part importante de notre clientèle, et les prix affichés sont les mêmes pour tout le monde : le tarif dépend de la quantité, pas du statut.",
          },
          {
            type: "p",
            texte:
              "La seule différence tient au niveau de conseil attendu. Un métallier sait ce qu'il vient chercher ; un particulier décrit son projet et on traduit. C'est prévu, et c'est gratuit.",
          },
        ],
      },
      {
        titre: "Quel acier pour quel projet",
        blocs: [
          {
            type: "liste",
            items: [
              "Portail, garde-corps, ossature : tube carré ou rectangulaire, en galvanisé si c'est dehors.",
              "Linteau, plancher, mezzanine : poutrelle IPE, HEA ou HEB — avec une note de calcul, toujours.",
              "Renfort, cadre, support : cornière égale. La 40 × 40 × 4 est la section la plus vendue du catalogue.",
              "Portail plein, grille, ferronnerie : plat et carré plein.",
              "Platine, gousset, pièce découpée : tôle lisse de 3 à 8 mm.",
              "Plancher technique, marche, passerelle : tôle larmée ou caillebotis.",
              "Toiture d'abri, bardage : bac acier profilé, galvanisé ou prélaqué.",
              "Dalle, chape, terrasse : treillis soudé et ronds à béton.",
              "Jardin, bordure, bac : acier corten.",
            ],
          },
        ],
      },
      {
        titre: "Découpe, délais et choix",
        blocs: [
          {
            type: "p",
            texte:
              "La découpe aux cotes est le service qui change tout pour un particulier : au lieu d'acheter une barre de 6 mètres dont vous n'utiliserez que 2,40, vous payez la longueur utile. Comptez 2,50 € par coupe, et une tolérance de ± 2 mm.",
          },
          {
            type: "p",
            texte:
              "Pour ce qui est en stock, le retrait est possible le jour même. Pour une section spécifique ou un façonnage, comptez deux à cinq jours ouvrables. On vous annonce le délai au devis, pas après.",
          },
        ],
      },
      {
        titre: "Comment commander : trois options",
        blocs: [
          {
            type: "liste",
            items: [
              "Par téléphone, du lundi au vendredi de 7 h à 17 h. Le plus rapide quand vous avez une question technique en même temps.",
              "Par e-mail, avec une liste « section, longueur, quantité ». On confirme le prix et l'heure de retrait dans la journée.",
              "Directement au comptoir, sans rendez-vous, dans l'un des quatre dépôts. Vous voyez la matière avant d'acheter.",
            ],
          },
          {
            type: "encadre",
            titre: "Et la livraison ?",
            texte:
              "Notre modèle est le retrait en dépôt. C'est ce qui nous permet de tenir des prix au mètre serrés — pas de flotte de camions à financer. Pour les gros volumes et les chantiers, un transport peut être organisé : demandez au devis.",
          },
        ],
      },
    ],
    liens: [
      { label: "Tout le catalogue", href: "/produits" },
      { label: "La découpe sur mesure", href: "/services/decoupe" },
      { label: "Nos 4 dépôts", href: "/depots" },
    ],
  },

  {
    slug: "analyse-marche-acier-belgique-2026",
    titre: "Marché de l'acier 2026 en Belgique",
    titreSeo: "Prix acier Belgique 2026 : analyse marché et perspectives",
    descSeo:
      "MACF, marché belge, perspectives de printemps et impact concret sur vos chantiers et vos devis. L'analyse d'un négociant.",
    chapo:
      "Le prix de l'acier ne se décide pas en Belgique. Voici ce qui le fait bouger en 2026, et ce que ça change pour un devis signé aujourd'hui.",
    categorie: "Marché",
    date: "25 mars 2026",
    lecture: 6,
    sections: [
      {
        titre: "01 — Le MACF change la donne",
        blocs: [
          {
            type: "p",
            texte:
              "Le mécanisme d'ajustement carbone aux frontières applique aux importations d'acier un coût correspondant à leur empreinte carbone. Concrètement, l'acier produit hors Union européenne dans des conditions moins contraintes perd une partie de son avantage de prix.",
          },
          {
            type: "p",
            texte:
              "Pour un négociant belge, l'effet est double : les écarts entre origines se resserrent, et la traçabilité devient un sujet commercial et plus seulement réglementaire.",
          },
        ],
      },
      {
        titre: "02 — Le marché belge",
        blocs: [
          {
            type: "p",
            texte:
              "La construction reste en recul, ce qui pèse sur les volumes. Mais la demande de rénovation et d'aménagement extérieur tient bien, portée par les particuliers et les petits artisans. Les carnets sont donc plus courts et plus fragmentés qu'il y a trois ans.",
          },
        ],
      },
      {
        titre: "03 — Perspectives",
        blocs: [
          {
            type: "p",
            texte:
              "La volatilité reste la caractéristique dominante. Ce n'est pas la tendance de fond qui pose problème — elle est modérément haussière — mais l'amplitude des variations d'une semaine à l'autre, qui rend impossible tout engagement de prix à long terme.",
          },
        ],
      },
      {
        titre: "04 — Impact sur vos chantiers et vos devis",
        blocs: [
          {
            type: "liste",
            items: [
              "Un devis acier a une validité de quinze jours, et ce n'est pas une clause de style : au-delà, le prix d'achat a réellement bougé.",
              "Sur un chantier long, commandez la matière en une fois plutôt qu'au fil de l'eau. Vous figez le prix et vous évitez les écarts d'aspect entre lots.",
              "Anticipez le printemps. Le pic de demande de mars à juin tend les délais autant que les prix.",
            ],
          },
        ],
      },
      {
        titre: "05 — Comment nous vous accompagnons",
        blocs: [
          {
            type: "p",
            texte:
              "En tenant un stock profond, ce qui amortit les à-coups du marché ; en annonçant clairement la durée de validité de chaque devis ; et en vous disant franchement quand il vaut mieux attendre une semaine ou commander tout de suite.",
          },
        ],
      },
    ],
    liens: [
      { label: "Demander un devis", href: "/devis" },
      { label: "Prix alu et inox en 2026", href: "/conseils/info-alu-inox-mars2026" },
      { label: "Tout le catalogue", href: "/produits" },
    ],
  },

  {
    slug: "info-alu-inox-mars2026",
    titre: "Prix aluminium et inox en 2026 : volatilité, causes et comment protéger vos projets",
    titreSeo: "Prix aluminium et inox 2026 : volatilité et conseils",
    descSeo:
      "Pourquoi les prix de l'alu et de l'inox fluctuent autant, ce que ça change pour vos devis, et comment sécuriser un budget.",
    chapo:
      "L'aluminium et l'inox ne suivent pas la même logique de prix que l'acier au carbone. Comprendre pourquoi permet d'acheter au bon moment.",
    categorie: "Marché",
    date: "10 mars 2026",
    lecture: 5,
    sections: [
      {
        titre: "01 — Pourquoi les prix fluctuent",
        blocs: [
          {
            type: "p",
            texte:
              "L'aluminium est coté en continu sur les marchés de métaux : son prix bouge chaque jour, et il est très sensible au coût de l'électricité, puisque sa production est avant tout un procédé électrolytique.",
          },
          {
            type: "p",
            texte:
              "L'inox, lui, dépend du nickel et du chrome. Le nickel est un marché étroit, donc volatil : une tension d'approvisionnement suffit à déplacer le prix de plusieurs pour cent en quelques jours. C'est la raison du fameux « extrait d'alliage » que les producteurs répercutent mensuellement.",
          },
        ],
      },
      {
        titre: "02 — Ce que ça change pour vos devis",
        blocs: [
          {
            type: "p",
            texte:
              "Sur un projet en inox, l'écart entre un devis de janvier et une commande de mai peut dépasser 10 %. Ce n'est pas une marge cachée, c'est l'extrait d'alliage. Mieux vaut donc commander la matière dès la signature plutôt qu'au démarrage du chantier.",
          },
        ],
      },
      {
        titre: "03 — Comment nous nous adaptons",
        blocs: [
          {
            type: "p",
            texte:
              "En tenant les sections courantes en stock, ce qui nous permet de vous vendre au prix de notre approvisionnement et non au prix du jour. Et en indiquant clairement, sur chaque devis inox et aluminium, la date de validité.",
          },
        ],
      },
      {
        titre: "04 — Nos conseils",
        blocs: [
          {
            type: "liste",
            items: [
              "Groupez vos besoins inox sur une seule commande plutôt que de les étaler.",
              "Vérifiez si le 304 suffit avant de partir sur du 316L : l'écart de prix est réel, et le 316L n'est nécessaire qu'en milieu chloré.",
              "En aluminium, regardez l'alliage autant que le prix : un 6060 et un 6082 ne s'usinent pas pareil et ne coûtent pas pareil.",
              "Demandez un tarif du jour plutôt que de vous fier à un devis de plus d'un mois.",
            ],
          },
        ],
      },
      {
        titre: "05 — Obtenir un tarif du jour",
        blocs: [
          {
            type: "p",
            texte:
              "Un appel ou un e-mail suffit. Pour les projets significatifs, nous pouvons bloquer un prix sur une durée convenue, à condition que la commande soit ferme.",
          },
        ],
      },
    ],
    liens: [
      { label: "Inox 304", href: "/inox" },
      { label: "Aluminium", href: "/aluminium" },
      { label: "Demander un tarif du jour", href: "/devis" },
    ],
  },

  {
    slug: "panneau-isole-lattonedil-eurocopre-monolamiera-30mm",
    titre: "Panneau isolé Eurocopre Monolamiera 30 mm : le guide complet pour votre toiture",
    titreSeo: "Panneau isolé Eurocopre Monolamiera 30 mm | Aciers Grosjean",
    descSeo:
      "Composition, performances thermiques, longueurs en stock de 260 à 710 cm, applications et pose du panneau sandwich Eurocopre 30 mm.",
    chapo:
      "Isolation et couverture en une seule pose. Le panneau sandwich 30 mm est la solution la plus rapide pour couvrir un atelier, un carport ou une extension.",
    categorie: "Toiture",
    date: "4 février 2026",
    lecture: 5,
    sections: [
      {
        titre: "01 — Qu'est-ce qu'un panneau isolé",
        blocs: [
          {
            type: "p",
            texte:
              "C'est un sandwich : une tôle profilée en face extérieure, une âme isolante en mousse polyuréthane, et un parement en face intérieure. Le tout est collé en usine et forme un élément porteur à lui seul.",
          },
          {
            type: "p",
            texte:
              "L'avantage tient en une phrase : vous posez la couverture, l'isolation et le plafond en une seule opération, sans pare-vapeur rapporté ni ossature secondaire.",
          },
        ],
      },
      {
        titre: "02 — Performances",
        blocs: [
          {
            type: "tableau",
            entetes: ["Caractéristique", "Valeur"],
            lignes: [
              ["Épaisseur d'isolant", "30 mm de polyuréthane"],
              ["Largeur utile", "1 000 mm"],
              ["Teinte standard", "RAL 7016 gris anthracite"],
              ["Portée courante", "Jusqu'à 2,5 m entre pannes"],
              ["Poids", "Environ 9 kg/m²"],
            ],
          },
          {
            type: "p",
            texte:
              "Le 30 mm est le bon compromis pour un local non chauffé : il coupe la condensation et les écarts de température sans le surcoût d'une isolation de bâtiment habité. Pour un atelier chauffé, montez à 40 ou 60 mm.",
          },
        ],
      },
      {
        titre: "03 — Stock permanent : de 260 à 710 cm",
        blocs: [
          {
            type: "p",
            texte:
              "Nous tenons les longueurs courantes en stock, par pas de 50 cm de 260 à 710 cm. C'est ce qui permet un retrait le jour même, là où une commande usine demande plusieurs semaines. Les longueurs hors gamme restent possibles sur commande.",
          },
        ],
      },
      {
        titre: "04 — Applications",
        blocs: [
          {
            type: "liste",
            items: [
              "Toiture d'atelier, de garage ou de hangar agricole.",
              "Carport et abri de voiture.",
              "Extension et annexe non chauffée.",
              "Remplacement d'une couverture en fibrociment.",
            ],
          },
        ],
      },
      {
        titre: "05 — Commander",
        blocs: [
          {
            type: "p",
            texte:
              "Donnez-nous la surface à couvrir et l'entraxe de vos pannes : on calcule le nombre de panneaux, les recouvrements et la visserie qui va avec. Prévoyez des vis autoforantes adaptées à l'épaisseur totale, rondelle EPDM comprise.",
          },
        ],
      },
    ],
    liens: [
      { label: "Panneaux isolés", href: "/toiture-bardage/panneaux-isoles" },
      { label: "Vis autoforantes", href: "/quincaillerie/visserie" },
      { label: "Demander un devis", href: "/devis" },
    ],
  },

  {
    slug: "une-entreprise-tournee-vers-lavenir",
    titre: "Aciers Grosjean : 40 ans au service des professionnels de l'acier en Wallonie",
    titreSeo: "Aciers Grosjean : négoce acier en Wallonie depuis 1986 | 4 dépôts",
    descSeo:
      "Quarante ans de négoce, quatre dépôts, deux usines et un département trading. L'histoire et l'organisation du Groupe Aciers Grosjean.",
    chapo:
      "D'un dépôt unique à quatre implantations, en Belgique et en France. Ce qui a changé, et ce qui n'a pas bougé.",
    categorie: "Entreprise",
    date: "2 février 2026",
    lecture: 4,
    sections: [
      {
        titre: "01 — Quarante ans de négoce",
        blocs: [
          {
            type: "p",
            texte:
              "L'entreprise est née au milieu des années 1980, dans une région où l'acier faisait vivre des milliers de familles. Elle est restée familiale, et c'est encore la même conviction qui la guide : l'acier de qualité professionnelle doit être accessible à tous, du grand chantier au projet de week-end.",
          },
        ],
      },
      {
        titre: "02 — Quatre dépôts, deux usines, un département trading",
        blocs: [
          {
            type: "p",
            texte:
              "Charleroi (Mont-sur-Marchienne) est le dépôt historique et le plus profond en stock : c'est de là que partent les transferts vers les autres sites. La Louvière et Tournai couvrent le Centre et l'ouest wallon. Marville, dans la Meuse, dessert le Grand Est et le sud de la Belgique.",
          },
        ],
      },
      {
        titre: "03 — Le e-commerce, notre cinquième magasin",
        blocs: [
          {
            type: "p",
            texte:
              "Le catalogue en ligne n'est pas une vitrine : c'est un point de vente à part entière, avec les prix, les poids et les disponibilités. Il sert autant le professionnel qui commande à 6 h du matin que le particulier qui compare un dimanche soir.",
          },
        ],
      },
      {
        titre: "04 — Engagement environnemental",
        blocs: [
          {
            type: "p",
            texte:
              "L'acier est recyclable indéfiniment sans perte de propriétés — c'est l'un des rares matériaux dans ce cas. Notre premier rapport ESG formalise ce qui était jusque-là une pratique, et fixe une feuille de route jusqu'en 2030.",
          },
        ],
      },
      {
        titre: "05 — Nous contacter",
        blocs: [
          {
            type: "p",
            texte:
              "Par téléphone du lundi au vendredi, par e-mail avec réponse sous 24 h, ou directement au comptoir, sans rendez-vous.",
          },
        ],
      },
    ],
    liens: [
      { label: "L'entreprise", href: "/entreprise" },
      { label: "Nos 4 dépôts", href: "/depots" },
      { label: "Notre rapport ESG", href: "/conseils/rapport-esg-aciers-grosjean-2023" },
    ],
  },

  {
    slug: "rapport-esg-aciers-grosjean-2023",
    titre: "Notre premier Rapport ESG 2023",
    titreSeo: "Rapport ESG 2023 : notre engagement durabilité et responsabilité",
    descSeo:
      "112 points de contrôle, les chiffres clés 2023, les piliers environnement et social, et la feuille de route ESG jusqu'en 2030.",
    chapo:
      "Premier exercice de transparence formalisé : ce qu'on mesure, ce qu'on a trouvé, et ce qu'on s'engage à améliorer.",
    categorie: "Entreprise",
    date: "25 avril 2026",
    lecture: 4,
    sections: [
      {
        titre: "Qu'est-ce que l'ESG",
        blocs: [
          {
            type: "p",
            texte:
              "Trois lettres pour trois domaines : Environnement, Social, Gouvernance. C'est un cadre d'évaluation qui oblige à mesurer ce qu'une entreprise fait réellement, au-delà de ce qu'elle affiche.",
          },
        ],
      },
      {
        titre: "112 points de contrôle",
        blocs: [
          {
            type: "p",
            texte:
              "L'évaluation porte sur 112 points, de la consommation énergétique des dépôts à la politique de formation, en passant par la traçabilité des approvisionnements et la gouvernance familiale. Chaque point est documenté ou ne compte pas.",
          },
        ],
      },
      {
        titre: "Pilier environnement",
        blocs: [
          {
            type: "p",
            texte:
              "L'acier est recyclable à l'infini, ce qui place notre métier dans une position favorable de départ. L'enjeu est ailleurs : consommation des sites, optimisation des transferts entre dépôts, réduction des chutes grâce à la découpe à la demande — chaque coupe optimisée est de la matière qui ne part pas en ferraille.",
          },
        ],
      },
      {
        titre: "Pilier social : 993 heures de formation",
        blocs: [
          {
            type: "p",
            texte:
              "993 heures de formation dispensées sur l'exercice, dont une part significative en sécurité et en conduite d'engins de manutention. Dans un métier où l'on manipule des charges lourdes tous les jours, c'est la ligne budgétaire la moins discutable.",
          },
        ],
      },
      {
        titre: "Feuille de route 2022-2030",
        blocs: [
          {
            type: "p",
            texte:
              "Des objectifs datés plutôt que des intentions : réduction de l'intensité énergétique des sites, amélioration continue du taux de valorisation des chutes, et extension de la certification à l'ensemble des activités de transformation.",
          },
        ],
      },
    ],
    liens: [
      { label: "Engagement ESG", href: "/entreprise/engagement-esg" },
      { label: "L'entreprise", href: "/entreprise" },
      { label: "Nos certifications", href: "/entreprise/certifications" },
    ],
  },

  {
    slug: "certification-en1090exc2",
    titre: "Le Groupe Aciers Grosjean est certifié selon la Norme EN1090-Exc-2",
    titreSeo: "Certification EN 1090-Exc2 | Aciers Grosjean",
    descSeo:
      "Ce que signifie la certification EN 1090-Exc2, pourquoi elle est exigée sur certains chantiers, et ce qu'elle change pour vos commandes.",
    chapo:
      "Une norme européenne qui encadre la fabrication des structures en acier. Peu d'acteurs de notre taille la détiennent.",
    categorie: "Entreprise",
    date: "2 février 2026",
    lecture: 2,
    sections: [
      {
        titre: "Ce que couvre la norme",
        blocs: [
          {
            type: "p",
            texte:
              "L'EN 1090 encadre l'exécution des structures en acier et en aluminium destinées à la construction. Elle impose un système de contrôle de production en usine, la qualification des soudeurs et des modes opératoires de soudage, et la traçabilité des matériaux.",
          },
          {
            type: "p",
            texte:
              "La mention Exc2 désigne la classe d'exécution : c'est celle qui couvre la grande majorité des ouvrages courants de bâtiment, au-dessus de l'Exc1 réservée aux structures les moins sollicitées.",
          },
        ],
      },
      {
        titre: "Ce que ça change pour vous",
        blocs: [
          {
            type: "liste",
            items: [
              "Sur un chantier soumis à contrôle, un ouvrage porteur doit provenir d'un atelier certifié. Sans certification, la pièce est refusée à la réception.",
              "Les certificats matière sont disponibles sur demande pour les produits concernés.",
              "Les soudures réalisées dans notre atelier suivent des modes opératoires qualifiés, pas l'habitude du soudeur.",
            ],
          },
        ],
      },
    ],
    liens: [
      { label: "Nos certifications", href: "/entreprise/certifications" },
      { label: "Transformation sur plan", href: "/services/soudure" },
      { label: "L'entreprise", href: "/entreprise" },
    ],
  },

  {
    slug: "accessibilite-bricofer",
    titre: "Travaux à La Louvière : comment accéder facilement à votre magasin",
    titreSeo: "Travaux à La Louvière : accès au dépôt Aciers Grosjean",
    descSeo:
      "Itinéraire pas à pas pendant les travaux, accès depuis Mons, Charleroi et Bruxelles, horaires et ce que vous trouverez au dépôt.",
    chapo:
      "Des travaux perturbent les accès habituels au dépôt de La Louvière. Voici l'itinéraire qui fonctionne.",
    categorie: "Dépôts",
    date: "23 février 2026",
    lecture: 3,
    sections: [
      {
        titre: "L'itinéraire pas à pas",
        blocs: [
          {
            type: "p",
            texte:
              "Contournez le centre par le ring plutôt que de le traverser : le gain de temps est réel aux heures de pointe, même si le trajet paraît plus long sur la carte. Suivez la signalisation du zoning jusqu'à l'entrée poids lourds — c'est la même que pour les véhicules légers.",
          },
        ],
      },
      {
        titre: "Accès depuis Mons, Charleroi et Bruxelles",
        blocs: [
          {
            type: "liste",
            items: [
              "Depuis Mons : autoroute jusqu'à la sortie du zoning, puis la desserte locale. Environ 25 minutes.",
              "Depuis Charleroi : si le trajet vous rapproche autant de Mont-sur-Marchienne, ce dépôt est plus profond en stock — appelez avant de choisir.",
              "Depuis Bruxelles : comptez 50 minutes hors heures de pointe, et évitez la tranche 16 h – 18 h.",
            ],
          },
        ],
      },
      {
        titre: "Horaires",
        blocs: [
          {
            type: "p",
            texte:
              "Du lundi au vendredi, de 7 h à 17 h, sans interruption. Le dépôt de La Louvière est fermé le samedi — c'est Charleroi qui assure la permanence du samedi matin.",
          },
        ],
      },
      {
        titre: "Ce que vous trouverez au dépôt",
        blocs: [
          {
            type: "p",
            texte:
              "Le stock courant complet — tubes, cornières, plats, tôles — la scie à ruban et la cisaille sur place, et un chariot élévateur pour le chargement. Ce qui n'est pas sur place arrive par transfert interne depuis Charleroi sous 48 h.",
          },
        ],
      },
    ],
    liens: [
      { label: "Dépôt de La Louvière", href: "/depots/la-louviere" },
      { label: "Tous nos dépôts", href: "/depots" },
      { label: "Nous contacter", href: "/contact" },
    ],
  },

  {
    slug: "livraison-par-drone-stratos-grosjean-2000",
    titre: "Logistique 4.0 : premier essai (presque) concluant pour notre livraison par drone « Stratos-Grosjean 2000 »",
    titreSeo: "Livraison par drone : le premier essai du Stratos-Grosjean 2000",
    descSeo:
      "Récit du premier vol d'essai de notre drone de livraison de poutrelles. Publié un 1er avril.",
    chapo:
      "6 h 05, un IPE 240 accroché sous un drone de douze hélices. Ce qui devait arriver arriva.",
    categorie: "Entreprise",
    date: "1er avril 2026",
    lecture: 2,
    sections: [
      {
        titre: "6 h 05 : le décollage vers le futur",
        blocs: [
          {
            type: "p",
            texte:
              "L'engin s'est arraché du sol avec une autorité qui a impressionné toute l'équipe logistique. Six mètres de poutrelle IPE 240, soit 184 kg, suspendus à un harnais textile. Les douze rotors ont tenu sept secondes.",
          },
        ],
      },
      {
        titre: "6 h 18 : le test de résistance gravitationnelle (Nivelles)",
        blocs: [
          {
            type: "p",
            texte:
              "Le protocole ne prévoyait pas de test de chute libre. Il en a eu un. La poutrelle, elle, n'a rien. C'est bien la preuve de la qualité de notre acier — et c'est à peu près le seul enseignement exploitable de la matinée.",
          },
        ],
      },
      {
        titre: "L'innovation ne s'arrête jamais",
        blocs: [
          {
            type: "p",
            texte:
              "Le programme Stratos-Grosjean est suspendu jusqu'à nouvel ordre. En attendant, le retrait en dépôt reste disponible du lundi au vendredi de 7 h à 17 h, avec chariot élévateur et sans risque de chute depuis 40 mètres.",
          },
          {
            type: "encadre",
            titre: "Pour être tout à fait clair",
            texte:
              "Cet article a été publié un 1er avril. Nous ne livrons pas par drone. Nous n'avons jamais livré par drone. Le retrait se fait au comptoir, et c'est très bien comme ça.",
          },
        ],
      },
    ],
    liens: [
      { label: "Nos 4 dépôts", href: "/depots" },
      { label: "Transport et livraison", href: "/services/transport-livraison" },
      { label: "Poutrelles IPE", href: "/acier/poutrelles/ipe" },
    ],
  },
];

export const articleBySlug = (slug: string) => articles.find((a) => a.slug === slug);
export const categoriesArticles = Array.from(new Set(articles.map((a) => a.categorie)));

/* ================================================================== */
/*  SERVICES — /services/{slug}                                        */
/* ================================================================== */

export type ServiceDetail = {
  slug: string;
  nom: string;
  accroche: string;
  titreSeo: string;
  descSeo: string;
  intro: string;
  points: { titre: string; texte: string }[];
  specs: { label: string; valeur: string }[];
  delai: string;
  prix: string;
};

export const servicesDetail: ServiceDetail[] = [
  {
    slug: "decoupe",
    nom: "Découpe sur mesure",
    accroche: "Vos pièces aux cotes exactes, prêtes à assembler",
    titreSeo: "Découpe acier sur mesure — aux cotes exactes, dès 2,50 € la coupe",
    descSeo:
      "Sciage, cisaillage et oxycoupage aux cotes exactes. Vous ne payez que la longueur utile, et vous repartez avec des pièces prêtes à souder.",
    intro:
      "C'est le service le plus demandé, et celui qui change le plus le prix final d'un projet. Acheter une barre de 6 m pour n'en utiliser que 2,40 revient à payer 60 % de chute. La découpe au dépôt supprime cette perte.",
    points: [
      { titre: "Vous ne payez que la longueur utile",
        texte: "Le débit se fait sur la barre commerciale et la chute repart au stock, pas dans votre facture. Sur un chantier de ferronnerie, c'est souvent 20 à 30 % du budget matière." },
      { titre: "Une tolérance de ± 2 mm",
        texte: "Sciage à froid pour les profilés, cisaillage pour les tôles jusqu'à 8 mm, oxycoupage au-delà. La cote annoncée est la cote livrée." },
      { titre: "Donnez-nous une liste, pas un plan",
        texte: "Un tableau « section, longueur, quantité » suffit. Envoyez-le par mail, on confirme le prix et l'heure de retrait dans la journée." },
    ],
    specs: [
      { label: "Tolérance", valeur: "± 2 mm" },
      { label: "Profilés", valeur: "Sciage à froid jusqu'à 300 mm" },
      { label: "Tôles", valeur: "Cisaillage jusqu'à 8 mm · 3 m de long" },
      { label: "Fortes épaisseurs", valeur: "Oxycoupage jusqu'à 100 mm" },
      { label: "Ébavurage", valeur: "Sur demande" },
    ],
    delai: "Le jour même",
    prix: "Dès 2,50 € la coupe",
  },
  {
    slug: "pliage-faconnage",
    nom: "Pliage & façonnage",
    accroche: "La tôle arrive déjà en forme",
    titreSeo: "Pliage de tôle et façonnage acier — presse plieuse jusqu'à 3 m",
    descSeo:
      "Pliage sur presse jusqu'à 3 m de long et 8 mm d'épaisseur, cintrage de tubes et de plats. Vos pièces arrivent formées, prêtes à poser.",
    intro:
      "Plier une tôle demande une presse, des outils et de l'expérience du retour élastique. Plutôt que d'improviser à l'étau, envoyez la cote et l'angle : la pièce sort juste du premier coup.",
    points: [
      { titre: "Jusqu'à 3 m de long",
        texte: "Presse plieuse 3 mètres. Au-delà, la pièce se plie en plusieurs tronçons à assembler — on vous dit tout de suite ce que ça implique." },
      { titre: "Le rayon compte",
        texte: "En dessous d'un rayon intérieur égal à l'épaisseur, la fibre extérieure fissure. On adapte l'outil à votre épaisseur plutôt que de forcer." },
      { titre: "Cintrage de tubes et de plats",
        texte: "Pour les mains courantes, les arceaux et les pièces courbes. Le rayon minimum dépend de la section — appelez avant de dessiner." },
    ],
    specs: [
      { label: "Longueur max", valeur: "3 000 mm" },
      { label: "Épaisseur max", valeur: "8 mm en acier doux" },
      { label: "Angle", valeur: "De 15° à 135°" },
      { label: "Rayon intérieur", valeur: "≥ 1 × épaisseur" },
      { label: "Cintrage", valeur: "Tube et plat, rayon selon section" },
    ],
    delai: "2 à 5 jours ouvrables",
    prix: "Sur devis, selon le nombre de plis",
  },
  {
    slug: "coupe-plie-armatures",
    nom: "Coupé-plié armatures",
    accroche: "Vos armatures façonnées selon le plan de ferraillage",
    titreSeo: "Coupé-plié et armatures assemblées sur mesure",
    descSeo:
      "Ronds à béton coupés, pliés et assemblés d'après votre plan de ferraillage : cadres, étriers, épingles, cages. Livrés repérés et prêts à poser.",
    intro:
      "Façonner des armatures sur chantier, c'est du temps perdu, des chutes et des cotes approximatives. En atelier, on travaille sur gabarit d'après le plan de ferraillage : les cadres sont tous identiques et les recouvrements tombent juste.",
    points: [
      { titre: "D'après votre plan de ferraillage",
        texte: "Nomenclature, repères, quantités : on travaille sur le document du bureau d'études. Si une cote manque, on appelle plutôt que d'interpréter." },
      { titre: "Cadres, étriers, épingles, cages",
        texte: "Du simple cadre de poteau à la cage assemblée de longrine. Les éléments arrivent repérés, étiquetés et bottelés par ouvrage." },
      { titre: "Moins de chutes, moins de manutention",
        texte: "Le débit est optimisé sur les barres commerciales. Vous ne payez pas les chutes, et vous ne les évacuez pas non plus." },
    ],
    specs: [
      { label: "Diamètres", valeur: "Ø 6 à Ø 20 mm" },
      { label: "Nuance", valeur: "B500B haute adhérence" },
      { label: "Formats acceptés", valeur: "Plan papier, PDF, DXF" },
      { label: "Repérage", valeur: "Étiquetage par ouvrage" },
      { label: "Assemblage", valeur: "Ligaturé ou soudé" },
    ],
    delai: "3 à 7 jours ouvrables selon volume",
    prix: "Sur devis sous 24 h",
  },
  {
    slug: "forage-poinconnage",
    nom: "Forage & poinçonnage",
    accroche: "Les trous sont déjà faits, et ils tombent juste",
    titreSeo: "Perçage et poinçonnage acier — platines et profilés percés au plan",
    descSeo:
      "Perçage sur plan de platines, profilés et tôles. Trous de Ø 6 à Ø 30, entraxes garantis au demi-millimètre, oblongs possibles.",
    intro:
      "Percer une platine à la perceuse à main, c'est une demi-heure par trou et un entraxe approximatif. Sur perceuse à colonne avec montage, c'est deux minutes et un entraxe au dixième — et c'est ce qui fait qu'une platine tombe en face des chevilles du premier coup.",
    points: [
      { titre: "L'entraxe est garanti",
        texte: "C'est ce qui compte vraiment : un trou mal placé condamne la pièce. On travaille au montage, pas au pointeau." },
      { titre: "Trous oblongs disponibles",
        texte: "Indispensables dès qu'il faut rattraper une tolérance de maçonnerie ou absorber une dilatation." },
      { titre: "Un croquis coté suffit",
        texte: "Pas besoin de DAO. Un croquis à main levée avec les cotes et les diamètres est parfaitement exploitable." },
    ],
    specs: [
      { label: "Diamètres", valeur: "Ø 6 à Ø 30 mm" },
      { label: "Épaisseur max", valeur: "20 mm" },
      { label: "Tolérance d'entraxe", valeur: "± 0,5 mm" },
      { label: "Oblongs", valeur: "Sur demande" },
      { label: "Chanfrein", valeur: "Sur demande" },
    ],
    delai: "2 à 4 jours ouvrables",
    prix: "Dès 1,20 € le trou",
  },
  {
    slug: "soudure",
    nom: "Soudure & assemblage",
    accroche: "Des ensembles mécanosoudés, certifiés EN 1090-Exc2",
    titreSeo: "Soudure et assemblage acier — atelier certifié EN 1090-Exc2",
    descSeo:
      "Ensembles soudés et pièces mécanosoudées réalisés sur plan dans notre atelier certifié EN 1090-Exc2. De la platine au portique.",
    intro:
      "Pour ce qui dépasse la coupe et le pli, l'atelier prend le relais. Vous fournissez le plan ou le croquis, nous livrons la pièce finie, contrôlée et traçable.",
    points: [
      { titre: "Certifié EN 1090-Exc2",
        texte: "La norme européenne qui encadre la fabrication des structures en acier. Elle est exigée dès qu'une pièce entre dans un ouvrage soumis à contrôle — sans elle, la pièce est refusée à la réception." },
      { titre: "Soudeurs et modes opératoires qualifiés",
        texte: "MIG/MAG, MMA et TIG. Les procédures sont qualifiées et les soudeurs certifiés : ce n'est pas l'habitude qui décide des paramètres." },
      { titre: "Traçabilité matière",
        texte: "Certificats matière disponibles sur demande, et repérage des pièces par ouvrage." },
    ],
    specs: [
      { label: "Certification", valeur: "EN 1090-Exc2" },
      { label: "Procédés", valeur: "MIG/MAG · MMA · TIG" },
      { label: "Formats", valeur: "Croquis coté, PDF, DXF" },
      { label: "Contrôle", valeur: "Visuel systématique" },
      { label: "Traçabilité", valeur: "Certificat matière sur demande" },
    ],
    delai: "Sur planning, annoncé au devis",
    prix: "Sur devis sous 24 h",
  },
  {
    slug: "grenaillage-peinture-gpp",
    nom: "Grenaillage & peinture",
    accroche: "La pièce arrive protégée, prête à poser",
    titreSeo: "Grenaillage et peinture acier — préparation de surface et primaire",
    descSeo:
      "Grenaillage de décapage puis primaire anticorrosion ou thermolaquage RAL. La finition posée telle quelle, sans reprise de chantier.",
    intro:
      "Une peinture ne tient que ce que vaut sa préparation. Le grenaillage projette de l'abrasif à grande vitesse : la calamine et la rouille partent, et la surface prend une rugosité qui accroche le primaire.",
    points: [
      { titre: "Le grenaillage d'abord",
        texte: "Peindre sur une tôle calaminée, c'est peindre sur une croûte qui finira par se détacher avec la peinture dessus. Le grenaillage est la seule préparation qui garantisse l'accroche." },
      { titre: "Primaire ou finition complète",
        texte: "Primaire anticorrosion seul, si vous peignez ensuite vous-même. Ou finition thermolaquée à la teinte RAL de votre choix, prête à poser." },
      { titre: "Dimensions maîtrisées",
        texte: "Vérifiez les cotes maximales avant de concevoir : une pièce qui n'entre pas en cabine se peint à la brosse, et ça se voit." },
    ],
    specs: [
      { label: "Préparation", valeur: "Grenaillage Sa 2½" },
      { label: "Primaire", valeur: "Anticorrosion époxy" },
      { label: "Finition", valeur: "Thermolaquage RAL au choix" },
      { label: "Sous-traitance", valeur: "Suivie par nos soins" },
    ],
    delai: "5 à 10 jours ouvrables",
    prix: "Sur devis, selon surface",
  },
  {
    slug: "galvanisation",
    nom: "Galvanisation à chaud",
    accroche: "Vingt à cinquante ans dehors, sans entretien",
    titreSeo: "Galvanisation à chaud — protection zinc EN ISO 1461",
    descSeo:
      "Trempage au bain de zinc selon EN ISO 1461. La protection la plus durable pour un ouvrage extérieur, sans peinture ni reprise.",
    intro:
      "La galvanisation à chaud trempe la pièce entière dans un bain de zinc en fusion. Le zinc ne se dépose pas seulement en surface : il forme un alliage avec l'acier. C'est ce qui la distingue de tous les autres traitements, et ce qui explique sa durée de vie.",
    points: [
      { titre: "Percez et coupez avant",
        texte: "Toute coupe ou perçage réalisé après galvanisation met l'acier à nu. La règle est simple : toute la transformation d'abord, la galvanisation ensuite." },
      { titre: "Prévoyez les trous d'évent",
        texte: "Un caisson fermé explose dans le bain. Les profilés creux doivent être percés pour laisser entrer et sortir le zinc. On vous indique où au moment du devis." },
      { titre: "Le zinc se sacrifie",
        texte: "Une rayure ne condamne pas la pièce : le zinc voisin protège électrochimiquement l'acier mis à nu sur quelques millimètres." },
    ],
    specs: [
      { label: "Norme", valeur: "EN ISO 1461" },
      { label: "Épaisseur de zinc", valeur: "Selon épaisseur de la pièce" },
      { label: "Durée de vie", valeur: "20 à 50 ans selon exposition" },
      { label: "Entretien", valeur: "Aucun" },
      { label: "Sous-traitance", valeur: "Suivie par nos soins" },
    ],
    delai: "7 à 14 jours ouvrables",
    prix: "Sur devis, au poids",
  },
  {
    slug: "transport-livraison",
    nom: "Transport & retrait",
    accroche: "Vous commandez, vous retirez — souvent le jour même",
    titreSeo: "Retrait en dépôt et transport chantier — click & collect acier",
    descSeo:
      "Retrait en dépôt préparé à l'avance, souvent le jour même, dans nos 4 dépôts. Transport chantier possible sur devis pour les gros volumes.",
    intro:
      "Notre modèle est le retrait en dépôt, et c'est assumé : pas de flotte de camions à financer, donc des prix au mètre qui restent tenus. Vous commandez à l'avance, la commande est préparée, vous ne faites que charger.",
    points: [
      { titre: "Préparé avant votre arrivée",
        texte: "Coupé, compté, mis de côté. Vous ne cherchez pas dans le rack et vous n'attendez pas derrière quelqu'un." },
      { titre: "Quatre dépôts, transferts internes",
        texte: "Charleroi, La Louvière, Tournai et Marville. Ce qui n'est pas sur place arrive par transfert interne, généralement sous 48 h." },
      { titre: "Transport chantier sur devis",
        texte: "Pour les gros volumes et les longueurs de 12 m, un transport peut être organisé. Précisez les contraintes d'accès au moment du devis." },
    ],
    specs: [
      { label: "Commande", valeur: "Par e-mail ou par téléphone" },
      { label: "Préparation", valeur: "Souvent le jour même" },
      { label: "Dépôts", valeur: "Charleroi · La Louvière · Tournai · Marville" },
      { label: "Chargement", valeur: "Chariot élévateur aux heures d'ouverture" },
      { label: "Transport", valeur: "Sur devis, selon volume et accès" },
    ],
    delai: "Le jour même si en stock",
    prix: "Retrait sans frais",
  },
];

export const serviceBySlug = (slug: string) => servicesDetail.find((s) => s.slug === slug);

/* ================================================================== */
/*  DÉPÔTS — /depots/{slug}                                            */
/* ================================================================== */

export type DepotDetail = {
  slug: string;
  ville: string;
  nomComplet: string;
  pays: string;
  region: string;
  adresse: string;
  tel: string;
  horaires: { jours: string; heures: string }[];
  intro: string;
  equipements: string[];
  dessert: string[];
};

// Coordonnées et horaires relevés sur les pages « Points de vente » de aciersgrosjean.be (14/09/2026).
const HORAIRES_DEPOTS_BE = [
  { jours: "Lundi – Jeudi (sept. – juin)", heures: "8 h – 12 h · 12 h 45 – 17 h" },
  { jours: "Vendredi (sept. – juin)", heures: "8 h – 12 h · 12 h 45 – 16 h 30" },
  { jours: "Lundi – Jeudi (juil. – août)", heures: "7 h – 12 h · 12 h 45 – 16 h" },
  { jours: "Vendredi (juil. – août)", heures: "7 h – 12 h · 12 h 45 – 15 h 30" },
  { jours: "Samedi – Dimanche", heures: "Fermé" },
];

export const depotsDetail: DepotDetail[] = [
  {
    slug: "charleroi-mont-sur-marchienne",
    ville: "Charleroi",
    nomComplet: "Mont-sur-Marchienne (Charleroi)",
    pays: "Belgique",
    region: "Hainaut",
    adresse: "Rue de Zone 23, 6032 Mont-sur-Marchienne (accès via la sortie 5 du R3)",
    tel: "+32 (0)71 47 10 40",
    horaires: HORAIRES_DEPOTS_BE,
    intro:
      "Le dépôt historique et le plus profond en stock. C'est ici que sont tenues les grandes longueurs et les sections lourdes, et c'est de là que partent les transferts vers les autres sites.",
    equipements: [
      "Scie à ruban jusqu'à 300 mm",
      "Cisaille 3 m",
      "Presse plieuse 3 m",
      "Oxycoupage",
      "Perçage sur montage",
      "Chariot élévateur 5 t",
      "Parking poids lourd",
    ],
    dessert: ["Charleroi", "Châtelet", "Fleurus", "Gerpinnes", "Courcelles", "Fontaine-l'Évêque", "Thuin"],
  },
  {
    slug: "la-louviere",
    ville: "La Louvière",
    nomComplet: "La Louvière",
    pays: "Belgique",
    region: "Hainaut",
    adresse: "Bricofer SA — Rue des Boulonneries 15, 7100 La Louvière",
    tel: "+32 (0)64 26 59 55",
    horaires: HORAIRES_DEPOTS_BE,
    intro:
      "Le dépôt du Centre, orienté chantier et ferronnerie : tubes, cornières, plats et tôles courantes en stock permanent, avec la découpe sur place.",
    equipements: ["Scie à ruban", "Cisaille 2 m", "Perçage", "Chariot élévateur 3,5 t"],
    dessert: ["La Louvière", "Binche", "Soignies", "Manage", "Morlanwelz", "Le Rœulx", "Écaussinnes"],
  },
  {
    slug: "tournai",
    ville: "Tournai",
    nomComplet: "Tournai",
    pays: "Belgique",
    region: "Hainaut occidental",
    adresse: "Ferutil SA — Rue Lefèbvre-Caters 46, 7500 Tournai",
    tel: "+32 (0)69 22 12 12",
    horaires: HORAIRES_DEPOTS_BE,
    intro:
      "Le dépôt de l'ouest wallon, à vingt minutes de la frontière française. Stock courant complet et transferts quotidiens depuis Charleroi pour les références spécifiques.",
    equipements: ["Scie à ruban", "Cisaille 2 m", "Chariot élévateur 3,5 t"],
    dessert: ["Tournai", "Ath", "Mouscron", "Leuze-en-Hainaut", "Péruwelz", "Lille (FR)"],
  },
  {
    slug: "marville-france",
    ville: "Marville",
    nomComplet: "Marville (France)",
    pays: "France",
    region: "Meuse (55)",
    adresse: "Aciers Grosjean France — ZI Ancienne Base Canadienne, 55600 Marville",
    tel: "+33 (0)3 29 88 10 62",
    horaires: [
      { jours: "Lundi – Vendredi", heures: "8 h – 12 h · 12 h 30 – 16 h 30" },
      { jours: "Samedi – Dimanche", heures: "Fermé" },
    ],
    intro:
      "Notre implantation française, au nord de la Meuse. Elle dessert le Grand Est et le sud de la Belgique, avec le même catalogue et les mêmes services de découpe.",
    equipements: ["Scie à ruban", "Cisaille 2 m", "Chariot élévateur 3,5 t", "Parking poids lourd"],
    dessert: ["Marville", "Longuyon", "Montmédy", "Verdun", "Longwy", "Virton (BE)"],
  },
];

export const depotBySlug = (slug: string) => depotsDetail.find((d) => d.slug === slug);

/* ================================================================== */
/*  AIDE — /aide/{slug}                                                */
/* ================================================================== */

export type PageAide = {
  slug: string;
  titre: string;
  titreSeo: string;
  descSeo: string;
  chapo: string;
  sections: Section[];
};

export const pagesAide: PageAide[] = [
  {
    slug: "livraison-retrait",
    titre: "Livraison et retrait",
    titreSeo: "Livraison et retrait en dépôt — comment ça marche",
    descSeo:
      "Retrait en dépôt préparé à l'avance, horaires, aide au chargement, transferts entre dépôts et transport chantier.",
    chapo: "Comment récupérer votre commande, et ce qu'il faut prévoir.",
    sections: [
      {
        titre: "Le retrait en dépôt",
        blocs: [
          { type: "p", texte: "Vous commandez par téléphone ou par e-mail, nous préparons, vous êtes prévenu dès que c'est prêt. Pour ce qui est en stock, c'est souvent le jour même." },
          { type: "liste", items: [
            "Présentez-vous avec un véhicule adapté à la longueur et à la masse commandées.",
            "Le chargement se fait au chariot élévateur aux heures d'ouverture.",
            "Prévenez-nous si une pièce dépasse 100 kg ou 6 mètres.",
            "L'arrimage est à votre charge — prévoyez sangles et protections d'angle.",
          ] },
        ],
      },
      {
        titre: "Entre dépôts",
        blocs: [
          { type: "p", texte: "Ce qui n'est pas sur place arrive par transfert interne, généralement sous 48 h. Vous choisissez le dépôt de retrait qui vous arrange, pas celui où la matière se trouve." },
        ],
      },
      {
        titre: "Transport chantier",
        blocs: [
          { type: "p", texte: "Pour les gros volumes et les longueurs de 12 m, un transport peut être organisé sur devis. Précisez les contraintes d'accès : hauteur sous porche, place de déchargement, présence d'un engin sur site." },
        ],
      },
    ],
  },
  {
    slug: "decoupe-et-tolerances",
    titre: "Découpe et tolérances",
    titreSeo: "Tolérances de découpe et de fabrication — ce qui est normal",
    descSeo:
      "Tolérances dimensionnelles et pondérales des produits sidérurgiques, tolérance de coupe à ± 2 mm, ébavurage et aspect de surface.",
    chapo: "Ce qui relève de la tolérance normale, et ce qui est un défaut.",
    sections: [
      {
        titre: "Tolérances de coupe",
        blocs: [
          { type: "tableau", entetes: ["Opération", "Tolérance"], lignes: [
            ["Sciage de profilé", "± 2 mm"],
            ["Cisaillage de tôle", "± 2 mm"],
            ["Oxycoupage", "± 3 mm"],
            ["Perçage — entraxe", "± 0,5 mm"],
            ["Pliage — angle", "± 1°"],
          ] },
        ],
      },
      {
        titre: "Tolérances de la matière",
        blocs: [
          { type: "p", texte: "Les produits sidérurgiques sont soumis aux tolérances dimensionnelles et pondérales des normes européennes. Une tôle annoncée en 3 mm peut mesurer 2,8 mm : c'est dans la norme, ce n'est pas un défaut de conformité." },
          { type: "p", texte: "De même, le poids réel d'une barre peut s'écarter de quelques pour cent du poids théorique calculé. C'est pour cette raison que les prix affichés sur ce site sont indicatifs et que le devis fait foi." },
        ],
      },
      {
        titre: "Aspect de surface",
        blocs: [
          { type: "p", texte: "Les produits laminés à chaud présentent naturellement une calamine bleu-gris et une légère oxydation de surface. Ce n'est pas un défaut : c'est l'état de livraison normal. Si l'aspect compte, demandez du décapé, du laminé à froid, ou prévoyez un grenaillage." },
        ],
      },
    ],
  },
  {
    slug: "paiement",
    titre: "Paiement",
    titreSeo: "Moyens de paiement et compte professionnel",
    descSeo:
      "Paiement au retrait pour les particuliers, ouverture d'un compte professionnel, conditions et réserve de propriété.",
    chapo: "Comment et quand on paie, selon que vous êtes particulier ou professionnel.",
    sections: [
      {
        titre: "Particuliers",
        blocs: [
          { type: "p", texte: "Le paiement s'effectue au comptant lors du retrait, par carte ou en espèces dans les limites légales. Aucun acompte n'est demandé pour les produits en stock ; une commande spéciale ou une fabrication sur mesure peut en revanche faire l'objet d'un acompte, annoncé au devis." },
        ],
      },
      {
        titre: "Professionnels",
        blocs: [
          { type: "p", texte: "L'ouverture d'un compte professionnel donne accès à des conditions de paiement différées et à des tarifs négociés selon les volumes. La demande se fait en ligne et la réponse intervient sous quelques jours ouvrables." },
          { type: "liste", items: [
            "Numéro de TVA valide exigé.",
            "Conditions de paiement définies à l'ouverture du compte.",
            "Retards de paiement : intérêts et indemnité forfaitaire selon la loi sur le retard de paiement.",
          ] },
        ],
      },
      {
        titre: "Réserve de propriété",
        blocs: [
          { type: "p", texte: "Les marchandises restent notre propriété jusqu'au paiement intégral du prix. Le transfert des risques s'opère en revanche dès le retrait." },
        ],
      },
    ],
  },
  {
    slug: "faq",
    titre: "Questions fréquentes",
    titreSeo: "Questions fréquentes — acheter de l'acier sans être du métier",
    descSeo:
      "Faut-il être professionnel ? Livrez-vous ? Combien de temps pour un devis ? Galvanisé ou inox ? Les réponses aux questions du comptoir.",
    chapo: "Les questions qu'on nous pose tous les jours.",
    sections: [],
  },
];

export const aideBySlug = (slug: string) => pagesAide.find((p) => p.slug === slug);
