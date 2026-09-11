/**
 * Contenu éditorial — la partie du site que l'audit désignait comme manquante.
 * leboutte.be est positionné sur 347 mots-clés que Grosjean ne couvre pas :
 * ces guides sont la réponse, écrits sur les questions que les clients posent
 * vraiment au comptoir avant d'acheter.
 */

export type Bloc =
  | { type: "p"; texte: string }
  | { type: "liste"; items: string[] }
  | { type: "encadre"; titre: string; texte: string }
  | { type: "tableau"; entetes: string[]; lignes: string[][] };

export type Section = { titre: string; blocs: Bloc[] };

export type Guide = {
  slug: string;
  titre: string;
  titreSeo: string;
  descSeo: string;
  chapo: string;
  categorie: string;
  lecture: number;
  maj: string;
  sections: Section[];
  liens: { label: string; href: string }[];
};

/* ------------------------------------------------------------------ */
/*  GUIDES                                                             */
/* ------------------------------------------------------------------ */

export const guides: Guide[] = [
  {
    slug: "galvanise-inox-ou-acier-peint",
    titre: "Galvanisé, inox ou acier peint : lequel pour votre projet ?",
    titreSeo: "Galvanisé, inox ou acier peint — comment choisir (et combien ça coûte)",
    descSeo:
      "Le comparatif honnête des trois protections de l'acier : coût au mètre, durée de vie, entretien, et le cas où chacun est le bon choix. Par un négociant, pas par un fabricant.",
    chapo:
      "C'est la question qu'on nous pose le plus au comptoir, et celle qui coûte le plus cher quand on se trompe. Voici comment trancher en trois minutes.",
    categorie: "Choisir sa matière",
    lecture: 4,
    maj: "Septembre 2026",
    sections: [
      {
        titre: "La vraie question n'est pas le prix d'achat",
        blocs: [
          {
            type: "p",
            texte:
              "Un garde-corps en acier peint coûte environ deux fois moins cher qu'en inox à l'achat. Mais il se repeint tous les cinq à sept ans — ponçage, primaire, deux couches, une journée de travail à chaque fois. Sur trente ans, l'inox nu revient moins cher. Le bon arbitrage ne se fait donc pas sur la facture du jour, mais sur la durée pendant laquelle l'ouvrage doit tenir sans que vous y touchiez.",
          },
          {
            type: "p",
            texte:
              "Posez-vous trois questions dans cet ordre : est-ce que la pièce est exposée à la pluie ? Est-ce qu'elle voit du sel, du chlore ou des embruns ? Est-ce que vous accepterez d'y revenir dans cinq ans ? Les réponses déterminent la matière plus sûrement que n'importe quel tableau.",
          },
        ],
      },
      {
        titre: "Le comparatif en un coup d'œil",
        blocs: [
          {
            type: "tableau",
            entetes: ["", "Acier peint", "Galvanisé", "Inox 304"],
            lignes: [
              ["Coût matière", "Le plus bas", "+20 à 30 %", "×4 à ×5"],
              ["Tenue en extérieur", "5 à 7 ans", "20 à 50 ans", "Illimitée"],
              ["Entretien", "Repeindre", "Aucun", "Aucun"],
              ["Aspect", "Toutes teintes", "Gris zinc", "Brossé"],
              ["Soudage", "Facile", "Reprise au zinc", "Inox uniquement"],
              ["Bord de mer", "Non", "Limité", "316L obligatoire"],
            ],
          },
        ],
      },
      {
        titre: "Quand choisir quoi",
        blocs: [
          {
            type: "liste",
            items: [
              "Intérieur, atelier, garage, mezzanine : acier brut ou peint. Inutile de payer une protection contre une pluie qui ne viendra pas.",
              "Clôture, portail, charpente d'abri, bardage : galvanisé. C'est le choix par défaut de l'extérieur, et de loin le meilleur rapport tenue/prix.",
              "Garde-corps de terrasse, main courante, mobilier de jardin visible : inox 304 brossé. On le touche, on le voit, il ne doit jamais couler de rouille sur la façade.",
              "Abords de piscine, bord de mer, station d'épuration : inox 316L, sans discussion. Le 304 y pique en quelques saisons.",
              "Jardin contemporain, bardage assumé, bordures : acier corten, qui est un cas à part — il rouille exprès, et cette rouille le protège.",
            ],
          },
          {
            type: "encadre",
            titre: "L'erreur la plus fréquente",
            texte:
              "Souder du galvanisé et repartir sans rien faire. La chaleur brûle le zinc sur trois à cinq centimètres de part et d'autre du cordon : la rouille démarre exactement là, et elle démarre vite. Une bombe de spray zinc coûte une douzaine d'euros et règle le problème définitivement.",
          },
        ],
      },
    ],
    liens: [
      { label: "Acier galvanisé", href: "/materiaux/galvanise" },
      { label: "Inox 304 et 316L", href: "/materiaux/inox" },
      { label: "Acier corten", href: "/materiaux/corten" },
    ],
  },

  {
    slug: "ipe-hea-heb-quelle-poutrelle-choisir",
    titre: "IPE, HEA, HEB, UPN : quelle poutrelle pour quoi ?",
    titreSeo: "IPE, HEA, HEB ou UPN — quelle poutrelle choisir et pourquoi",
    descSeo:
      "Les quatre profils de poutrelle expliqués simplement : ce que chacun sait faire, comment lire les cotes, et les erreurs qui reviennent le plus souvent en rénovation.",
    chapo:
      "Quatre lettres, quatre formes, quatre usages. Une fois qu'on a compris la logique, on ne se trompe plus.",
    categorie: "Comprendre les produits",
    lecture: 5,
    maj: "Septembre 2026",
    sections: [
      {
        titre: "Tout part de la forme de la section",
        blocs: [
          {
            type: "p",
            texte:
              "Une poutrelle résiste à la flexion grâce à la matière qui se trouve loin de son axe : ce sont les ailes, en haut et en bas, qui travaillent. L'âme, la partie verticale, sert surtout à les tenir écartées. C'est pourquoi un profil haut et étroit porte beaucoup mieux à plat qu'un profil bas et large.",
          },
          {
            type: "p",
            texte:
              "À partir de là, tout s'explique : l'IPE est haut et étroit, donc c'est le profil de la poutre horizontale. Le HEB est presque carré, donc il résiste aussi bien dans les deux sens — c'est le profil du poteau, qui peut flamber dans n'importe quelle direction.",
          },
        ],
      },
      {
        titre: "Les quatre profils",
        blocs: [
          {
            type: "tableau",
            entetes: ["Profil", "Forme", "Usage principal", "Repère"],
            lignes: [
              ["IPE", "I haut et étroit, ailes parallèles", "Poutre, linteau, plancher", "Le plus courant"],
              ["IPN", "I à ailes inclinées", "Rénovation, reprise d'existant", "L'ancien"],
              ["HEA", "H allégé, ailes larges", "Poteau, ossature", "Le compromis"],
              ["HEB", "H lourd, section carrée", "Poteau, forte charge", "Le costaud"],
              ["UPN", "U à ailes inclinées", "Chevêtre, rive, encadrement", "Se boulonne à plat"],
            ],
          },
          {
            type: "p",
            texte:
              "Le nombre qui suit la lettre est la hauteur du profil en millimètres — sauf pour les HEA, où la hauteur réelle est légèrement inférieure au chiffre annoncé : un HEA 200 mesure 190 mm de haut. C'est une source d'erreur classique quand on prépare des réservations dans un mur.",
          },
        ],
      },
      {
        titre: "Trois erreurs qui reviennent",
        blocs: [
          {
            type: "liste",
            items: [
              "Commander un IPE pour faire un poteau. Il porte très bien dans un sens et flambe dans l'autre. Pour un poteau, c'est HEA ou HEB.",
              "Oublier la longueur d'appui. Un linteau ne se pose pas bord à bord sur la maçonnerie : il faut 15 à 20 cm de portée de chaque côté, et souvent une platine pour répartir la charge.",
              "Confondre IPN et IPE en rénovation. Les ailes inclinées de l'IPN ne reçoivent pas une platine plate sans cale. Si vous reprenez un existant, mesurez l'inclinaison avant de commander.",
            ],
          },
          {
            type: "encadre",
            titre: "Ce guide ne remplace pas un calcul",
            texte:
              "Dès qu'une poutrelle reprend une charge de structure — un plancher, un mur porteur, une toiture — le dimensionnement relève d'un ingénieur ou d'un architecte. Nous fournissons la matière aux cotes et le poids exact ; le calcul, c'est leur métier, et c'est votre assurance décennale qui en dépend.",
          },
        ],
      },
    ],
    liens: [
      { label: "Toutes les poutrelles", href: "/produits/poutrelles" },
      { label: "Poutrelle IPE 200", href: "/produits/poutrelles/ipe-200" },
      { label: "Poutrelle HEB 140", href: "/produits/poutrelles/heb-140" },
    ],
  },

  {
    slug: "quelle-epaisseur-de-tole",
    titre: "Quelle épaisseur de tôle choisir ?",
    titreSeo: "Épaisseur de tôle acier — le tableau des usages, de 1 à 20 mm",
    descSeo:
      "De la tôle de 1 mm à celle de 20 mm : à quoi sert chaque épaisseur, ce qu'elle pèse au m², ce qu'elle coûte, et jusqu'où elle se plie ou se découpe.",
    chapo:
      "Trop fine, elle ondule et vibre. Trop épaisse, elle coûte cher et ne se plie plus. Voici comment viser juste du premier coup.",
    categorie: "Comprendre les produits",
    lecture: 4,
    maj: "Septembre 2026",
    sections: [
      {
        titre: "Le repère : une tôle pèse 7,85 kg/m² par millimètre",
        blocs: [
          {
            type: "p",
            texte:
              "C'est le seul chiffre à retenir. Une tôle de 2 mm pèse 15,7 kg/m², une tôle de 5 mm en pèse 39,25. Cela vous donne immédiatement le poids à manipuler, le coût approximatif — l'acier se vend au poids — et la faisabilité de la pose à deux personnes.",
          },
          {
            type: "p",
            texte:
              "Concrètement : un panneau de 2 × 1 m en 3 mm pèse 47 kg. C'est la limite du portage à deux sans matériel. Au-delà, prévoyez un transpalette ou faites-le débiter en deux morceaux — la découpe coûte moins cher qu'un dos bloqué.",
          },
        ],
      },
      {
        titre: "Le tableau des usages",
        blocs: [
          {
            type: "tableau",
            entetes: ["Épaisseur", "Poids", "Usages typiques"],
            lignes: [
              ["0,75 à 1 mm", "6 à 8 kg/m²", "Habillage, capotage, gouttière, signalétique"],
              ["1,5 à 2 mm", "12 à 16 kg/m²", "Coffret, carter, habillage rigide, crédence"],
              ["3 mm", "23,5 kg/m²", "Platine légère, seuil, plancher de remorque"],
              ["4 à 5 mm", "31 à 39 kg/m²", "Platine de poteau, gousset, marche"],
              ["6 à 8 mm", "47 à 63 kg/m²", "Platine de charpente, pièce structurelle"],
              ["10 à 20 mm", "78 à 157 kg/m²", "Semelle, contrepoids, usinage lourd"],
            ],
          },
        ],
      },
      {
        titre: "Ce qui change avec l'épaisseur",
        blocs: [
          {
            type: "liste",
            items: [
              "Jusqu'à 2 mm, la tôle se cisaille proprement et se plie sans difficulté sur une plieuse standard.",
              "De 3 à 6 mm, le pliage demande une presse et un rayon intérieur d'au moins une épaisseur, sinon la fibre extérieure fissure.",
              "Au-delà de 8 mm, on passe à l'oxycoupage plutôt qu'au cisaillage, et le bord demande un ébavurage.",
              "En dessous de 1,5 mm sur une grande surface, la tôle ondule sous son propre poids : il faut un cadre, une nervure ou un contrecollage.",
            ],
          },
          {
            type: "encadre",
            titre: "Notre conseil de comptoir",
            texte:
              "Dans le doute entre deux épaisseurs voisines, prenez la plus épaisse si la pièce est visible ou porte quelque chose, la plus fine si elle est cachée et ne fait qu'habiller. L'écart de prix est presque toujours inférieur à ce que coûte un remplacement.",
          },
        ],
      },
    ],
    liens: [
      { label: "Toutes les tôles", href: "/produits/toles" },
      { label: "Tôle lisse 3 mm", href: "/produits/toles/tole-lisse-3mm" },
      { label: "La découpe sur mesure", href: "/services/decoupe" },
    ],
  },

  {
    slug: "fabriquer-un-portail-en-acier",
    titre: "Fabriquer un portail en acier : la liste de matière complète",
    titreSeo: "Fabriquer un portail acier — liste de matière, cotes et budget réel",
    descSeo:
      "Tout ce qu'il faut commander pour un portail battant de 3 m : sections de tubes, quantités, budget matière, et les cinq points où les amateurs se trompent.",
    chapo:
      "Un portail battant de 3 mètres, c'est environ 28 mètres de tube et 180 € de matière. Voici la liste exacte, section par section.",
    categorie: "Projets",
    lecture: 6,
    maj: "Septembre 2026",
    sections: [
      {
        titre: "Le principe : un cadre rigide, un remplissage léger",
        blocs: [
          {
            type: "p",
            texte:
              "Un portail travaille en porte-à-faux : tout le poids pend sur deux gonds. La règle est donc de concentrer la matière dans le cadre périphérique et de rester léger au milieu. Un cadre en tube 50 × 50 × 2 et un remplissage en tube 30 × 30 × 2 tient beaucoup mieux qu'un ensemble homogène en 40 × 40, à poids égal.",
          },
          {
            type: "p",
            texte:
              "La diagonale est l'autre point non négociable. Sans elle, le cadre est un parallélogramme articulé : il s'affaisse côté serrure en quelques mois. Une diagonale allant du gond haut vers la serrure basse règle définitivement la question.",
          },
        ],
      },
      {
        titre: "La liste de matière — portail battant 2 vantaux, 3 × 1,60 m",
        blocs: [
          {
            type: "tableau",
            entetes: ["Poste", "Section", "Quantité", "Matière"],
            lignes: [
              ["Cadre des vantaux", "Tube carré 50 × 50 × 2", "9,2 m", "Galvanisé"],
              ["Traverses intermédiaires", "Tube carré 40 × 40 × 2", "6 m", "Galvanisé"],
              ["Barreaudage", "Tube carré 30 × 30 × 2", "13 m", "Galvanisé"],
              ["Diagonales", "Plat 40 × 5", "4 m", "Acier"],
              ["Platines de gond", "Tôle lisse 6 mm", "0,2 m²", "Acier"],
              ["Poteaux", "Tube carré 100 × 100 × 4", "2 × 2 m", "Galvanisé"],
            ],
          },
          {
            type: "p",
            texte:
              "Comptez environ 180 à 220 € de matière hors quincaillerie et hors poteaux, selon la nuance et la protection choisies. Ajoutez les gonds réglables, la serrure, et une bombe de spray zinc pour reprendre les soudures si vous partez sur du galvanisé.",
          },
        ],
      },
      {
        titre: "Les cinq erreurs à ne pas faire",
        blocs: [
          {
            type: "liste",
            items: [
              "Souder le cadre à plat sur un sol qui ne l'est pas. Le vantail sortira vrillé et ne fermera jamais. Calez et vérifiez les diagonales au mètre avant le premier point de soudure.",
              "Oublier le jeu. Prévoyez 10 à 15 mm entre les vantaux et 15 mm au sol, sinon la dilatation d'été bloque la fermeture.",
              "Sous-dimensionner les poteaux. Un vantail de 1,5 m exerce un levier considérable : en dessous du tube 100 × 100 × 4 correctement scellé, ça bouge.",
              "Fermer le bas des tubes. L'eau entre par le haut, stagne, et le tube rouille de l'intérieur. Percez un trou de drainage de 6 mm en point bas de chaque montant.",
              "Peindre sans dégraisser. Les tubes neufs sont huilés en sortie de laminage. Sans dégraissage à l'acétone, la peinture cloque dans l'année.",
            ],
          },
        ],
      },
    ],
    liens: [
      { label: "Tubes carrés", href: "/produits/tubes" },
      { label: "Tube carré 50 × 50 × 2", href: "/produits/tubes/tube-carre-50x50x2" },
      { label: "Demander la découpe", href: "/services/decoupe" },
    ],
  },

  {
    slug: "poser-une-cloture-rigide",
    titre: "Poser une clôture à panneaux rigides, poteau par poteau",
    titreSeo: "Poser une clôture rigide — entraxe, scellement, jambes de force",
    descSeo:
      "La méthode complète : calculer le nombre de poteaux, choisir la longueur, sceller correctement, et pourquoi la jambe de force n'est jamais optionnelle en bout de ligne.",
    chapo:
      "Une clôture rigide bien posée tient trente ans. Mal posée, elle penche dès le premier hiver — et c'est presque toujours le même détail qui manque.",
    categorie: "Projets",
    lecture: 5,
    maj: "Septembre 2026",
    sections: [
      {
        titre: "Combien de poteaux, et de quelle longueur",
        blocs: [
          {
            type: "p",
            texte:
              "Les panneaux rigides standard mesurent 2,50 m de large. Le nombre de poteaux est donc le nombre de panneaux plus un. Pour 20 mètres de clôture : 8 panneaux, 9 poteaux. Ajoutez un poteau à chaque angle et de part et d'autre d'un portillon.",
          },
          {
            type: "p",
            texte:
              "Pour la longueur du poteau, la règle est simple : hauteur de clôture souhaitée plus 30 cm de scellement, arrondie à la longueur commerciale au-dessus. Une clôture de 1,50 m demande donc un poteau de 1,75 m, pas de 1,50.",
          },
        ],
      },
      {
        titre: "Le scellement",
        blocs: [
          {
            type: "liste",
            items: [
              "Trou de 30 cm de profondeur sur 25 cm de diamètre, à la tarière ou à la bêche à trou.",
              "Un lit de gravier de 5 cm au fond : le poteau ne baigne pas dans l'eau, et le béton ne remonte pas par capillarité.",
              "Béton dosé à 350 kg/m³, soit un sac de 35 kg pour environ deux trous.",
              "Vérifiez l'aplomb dans les deux sens au niveau à bulle, et calez avec des chutes de bois le temps de la prise.",
              "48 heures avant de poser les panneaux. Tirer sur un poteau qui n'a pas fini de prendre le descelle sans qu'on le voie.",
            ],
          },
        ],
      },
      {
        titre: "Le détail qui fait tout : la jambe de force",
        blocs: [
          {
            type: "p",
            texte:
              "Une ligne de clôture est sous tension. Chaque poteau intermédiaire est retenu de part et d'autre par ses voisins, mais le premier et le dernier de la ligne, ainsi que chaque poteau d'angle, ne le sont que d'un seul côté. Sans contreventement, ils s'inclinent vers l'intérieur, et toute la ligne suit.",
          },
          {
            type: "encadre",
            titre: "La règle des trois positions",
            texte:
              "Une jambe de force au poteau de départ, une au poteau d'arrivée, et une de chaque côté de chaque angle. C'est la pièce à 16 € qu'on est tenté d'économiser, et c'est celle dont l'absence se voit à l'œil nu deux ans plus tard.",
          },
        ],
      },
    ],
    liens: [
      { label: "Poteaux de clôture", href: "/produits/poteaux-cloture" },
      { label: "Jambe de force Ø 48", href: "/produits/poteaux-cloture/jambe-de-force-48" },
      { label: "Nos dépôts", href: "/depots" },
    ],
  },

  {
    slug: "acier-corten-ce-qu-il-faut-savoir",
    titre: "Acier corten : ce que les vendeurs ne disent pas toujours",
    titreSeo: "Acier corten — patine, coulures, durée de vie : le guide honnête",
    descSeo:
      "Le corten est magnifique et durable, mais il coule, il tache et il ne convient pas partout. Les trois limites à connaître avant de commander, et comment les gérer.",
    chapo:
      "Le corten mérite sa réputation. Mais trois choses surprennent systématiquement les clients, et il vaut mieux les savoir avant la livraison qu'après.",
    categorie: "Choisir sa matière",
    lecture: 4,
    maj: "Septembre 2026",
    sections: [
      {
        titre: "Comment ça marche",
        blocs: [
          {
            type: "p",
            texte:
              "Le corten est un acier allié au cuivre, au chrome et au phosphore. Sa rouille, contrairement à celle de l'acier ordinaire, forme une couche dense et adhérente qui colle à la surface au lieu de s'écailler. Cette patine bloque l'oxygène et l'humidité : la corrosion s'arrête d'elle-même après quelques dixièmes de millimètre.",
          },
          {
            type: "p",
            texte:
              "Elle met six à dix-huit mois à se stabiliser, selon l'exposition. Pendant cette période, la teinte évolue d'un orange vif à un brun profond, et la pièce n'a pas encore son aspect définitif.",
          },
        ],
      },
      {
        titre: "Les trois surprises",
        blocs: [
          {
            type: "liste",
            items: [
              "Il coule. Pendant la formation de la patine, la pluie emporte des oxydes qui tachent durablement le béton clair, la pierre bleue et les dalles de terrasse. Prévoyez un lit de gravier, une rigole ou un débord sous toute pièce corten posée au-dessus d'un sol clair.",
              "Il lui faut sécher. La patine ne se forme qu'en alternance humide/sec. Une pièce en contact permanent avec la terre, l'eau stagnante ou un paillis humide se corrode comme un acier ordinaire — et là, elle perce.",
              "Il perd de l'épaisseur. Comptez deux à trois dixièmes de millimètre consommés par la patine. Sans conséquence sur une tôle de 3 mm décorative, mais à intégrer au calcul pour une pièce qui porte.",
            ],
          },
          {
            type: "encadre",
            titre: "Peut-on accélérer la patine ?",
            texte:
              "Oui, en alternant pulvérisations d'eau vinaigrée et séchages complets pendant une à deux semaines. Le résultat est plus rapide mais souvent plus irrégulier qu'une patine naturelle. Si l'aspect compte, laissez faire les saisons.",
          },
        ],
      },
    ],
    liens: [
      { label: "Acier corten", href: "/materiaux/corten" },
      { label: "Produits corten", href: "/produits/corten" },
      { label: "Bordure de jardin corten", href: "/produits/corten/bordure-jardin-corten" },
    ],
  },

  {
    slug: "calculer-le-poids-de-l-acier",
    titre: "Calculer le poids de l'acier sans tableau",
    titreSeo: "Calculer le poids de l'acier — les 4 formules à connaître par cœur",
    descSeo:
      "Tôle, plat, rond, tube : quatre formules simples pour connaître le poids au mètre de n'importe quelle section, et savoir si ça passe dans la voiture.",
    chapo:
      "L'acier se vend au poids, se transporte au poids et se porte au poids. Ces quatre formules tiennent sur un coin de table et évitent les mauvaises surprises au dépôt.",
    categorie: "Repères techniques",
    lecture: 3,
    maj: "Septembre 2026",
    sections: [
      {
        titre: "Le point de départ",
        blocs: [
          {
            type: "p",
            texte:
              "L'acier pèse 7,85 kg par décimètre cube. Toutes les formules qui suivent en découlent. Pour l'inox, remplacez par 8,00 ; pour l'aluminium, par 2,70 — c'est-à-dire environ trois fois moins.",
          },
        ],
      },
      {
        titre: "Les quatre formules",
        blocs: [
          {
            type: "tableau",
            entetes: ["Produit", "Formule", "Exemple"],
            lignes: [
              ["Tôle (kg/m²)", "épaisseur mm × 7,85", "3 mm → 23,6 kg/m²"],
              ["Plat (kg/m)", "largeur × épaisseur × 0,00785", "40 × 5 → 1,57 kg/m"],
              ["Rond plein (kg/m)", "Ø² × 0,00617", "Ø 20 → 2,47 kg/m"],
              ["Tube (kg/m)", "(périmètre − 4×ép) × ép × 0,00785", "40×40×2 → 2,31 kg/m"],
            ],
          },
          {
            type: "p",
            texte:
              "Pour les poutrelles, il n'y a pas de formule simple : la section est trop complexe. Le poids au mètre figure sur chaque fiche produit du catalogue, et c'est la valeur normalisée officielle.",
          },
        ],
      },
      {
        titre: "À quoi ça sert concrètement",
        blocs: [
          {
            type: "liste",
            items: [
              "Savoir si ça rentre dans le véhicule. Une remorque de 500 kg de charge utile, c'est 21 mètres de tube 50 × 50 × 3, ou 12 m² de tôle de 5 mm. Pas plus.",
              "Estimer le prix avant d'appeler. L'acier de base tourne autour de 1 à 1,50 € le kilo au détail selon le produit : le poids donne l'ordre de grandeur immédiatement.",
              "Dimensionner la manutention. Au-delà de 50 kg par pièce, il faut être deux ; au-delà de 100, il faut du matériel.",
              "Vérifier une facture. Le poids annoncé et le poids calculé doivent coïncider à quelques pour cent près.",
            ],
          },
          {
            type: "encadre",
            titre: "Plus simple encore",
            texte:
              "Chaque fiche produit du catalogue affiche le poids au mètre et un calculateur : entrez votre longueur, il vous donne le poids total et l'estimation de prix. C'est la même formule, mais faite pour vous.",
          },
        ],
      },
    ],
    liens: [
      { label: "Tout le catalogue", href: "/produits" },
      { label: "Plats & barres", href: "/produits/plats-barres" },
      { label: "Tubes", href: "/produits/tubes" },
    ],
  },

  {
    slug: "souder-quand-on-debute",
    titre: "Souder l'acier quand on débute : le matériel et les réglages",
    titreSeo: "Souder l'acier pour débuter — poste, électrodes et réglages de base",
    descSeo:
      "Quel poste acheter, quelle électrode pour quelle épaisseur, à quelle intensité régler, et les cinq défauts de cordon qu'on reconnaît d'un coup d'œil.",
    chapo:
      "On peut apprendre à faire un cordon correct en un après-midi. Ce qui bloque les débutants, ce n'est pas le geste : c'est le réglage.",
    categorie: "Repères techniques",
    lecture: 5,
    maj: "Septembre 2026",
    sections: [
      {
        titre: "Le matériel minimum",
        blocs: [
          {
            type: "liste",
            items: [
              "Un poste à électrode enrobée (MMA) de 160 A suffit pour tout ce qu'un particulier soude : tube, plat, cornière jusqu'à 8 mm.",
              "Un masque à cristaux liquides automatique. Le masque à main coûte trois fois moins cher et fait rater trois fois plus d'amorçages.",
              "Des gants de soudeur, une veste en coton épais, et surtout des chaussures fermées : une goutte de laitier dans une basket ne s'oublie pas.",
              "Une brosse métallique et un marteau à piquer pour retirer le laitier entre les passes.",
            ],
          },
        ],
      },
      {
        titre: "Quelle électrode, à quelle intensité",
        blocs: [
          {
            type: "tableau",
            entetes: ["Épaisseur", "Électrode", "Intensité"],
            lignes: [
              ["1,5 à 3 mm", "Ø 2,0 mm", "50 à 70 A"],
              ["3 à 5 mm", "Ø 2,5 mm", "60 à 90 A"],
              ["5 à 8 mm", "Ø 3,2 mm", "90 à 130 A"],
              ["Plus de 8 mm", "Ø 4,0 mm", "130 à 170 A"],
            ],
          },
          {
            type: "p",
            texte:
              "L'électrode rutile est celle du débutant : elle amorce facilement, le laitier se détache seul, et le cordon est visuellement lisible. Gardez les basiques pour plus tard, elles demandent un étuvage et une main plus sûre.",
          },
        ],
      },
      {
        titre: "Lire son cordon",
        blocs: [
          {
            type: "liste",
            items: [
              "Cordon haut et étroit, qui ne mouille pas les bords : intensité trop faible. Montez de 10 A.",
              "Métal qui s'effondre, perforation : intensité trop forte, ou vitesse trop lente.",
              "Projections partout : arc trop long. Rapprochez l'électrode, la longueur d'arc doit valoir son diamètre.",
              "Cordon irrégulier en vagues : vitesse d'avance irrégulière. Appuyez le poignet et avancez lentement, de façon continue.",
              "Caniveaux sur les bords : vous balayez trop large pour l'intensité. Réduisez l'amplitude.",
            ],
          },
          {
            type: "encadre",
            titre: "Le galvanisé et l'inox, pas maintenant",
            texte:
              "Souder du galvanisé dégage des fumées de zinc réellement toxiques : ventilation obligatoire, et de préférence, meulez le zinc avant. L'inox ne se soude pas à l'électrode ordinaire — il lui faut une électrode inox, ou mieux, du TIG. Commencez sur de l'acier brut.",
          },
        ],
      },
    ],
    liens: [
      { label: "Électrodes et consommables", href: "/produits/visserie" },
      { label: "Plats & barres", href: "/produits/plats-barres" },
      { label: "Acier S235", href: "/materiaux/acier" },
    ],
  },
];

export const guideBySlug = (slug: string) => guides.find((g) => g.slug === slug);

/* ------------------------------------------------------------------ */
/*  SERVICES                                                           */
/* ------------------------------------------------------------------ */

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
      "Sciage, cisaillage et oxycoupage aux cotes exactes. Vous ne payez que la longueur utile, et vous repartez avec des pièces prêtes à souder. Retrait le jour même.",
    intro:
      "C'est le service le plus demandé, et celui qui change le plus le prix final d'un projet. Acheter une barre de 6 m pour n'en utiliser que 2,40 revient à payer 60 % de chute. La découpe au dépôt supprime cette perte et vous fait gagner une demi-journée de travail.",
    points: [
      {
        titre: "Vous ne payez que la longueur utile",
        texte:
          "Le débit se fait sur la barre commerciale et la chute repart au stock, pas dans votre facture. Sur un chantier de ferronnerie, c'est souvent 20 à 30 % du budget matière.",
      },
      {
        titre: "Une tolérance de ± 2 mm",
        texte:
          "Sciage à froid pour les profilés, cisaillage pour les tôles jusqu'à 8 mm, oxycoupage au-delà. Dans tous les cas, la cote annoncée est la cote livrée.",
      },
      {
        titre: "Donnez-nous une liste, pas un plan",
        texte:
          "Un tableau « section, longueur, quantité » suffit. Envoyez-le par mail, on vous confirme le prix et l'heure de retrait dans la journée.",
      },
    ],
    specs: [
      { label: "Tolérance", valeur: "± 2 mm" },
      { label: "Profilés", valeur: "Sciage à froid jusqu'à 300 mm" },
      { label: "Tôles", valeur: "Cisaillage jusqu'à 8 mm · 3 m de long" },
      { label: "Fortes épaisseurs", valeur: "Oxycoupage jusqu'à 100 mm" },
      { label: "Ébavurage", valeur: "Sur demande" },
    ],
    delai: "Le jour même pour les demandes simples",
    prix: "À partir de 2,50 € la coupe",
  },
  {
    slug: "pliage",
    nom: "Pliage & façonnage",
    accroche: "La tôle arrive déjà en forme",
    titreSeo: "Pliage de tôle et façonnage acier — presse plieuse jusqu'à 3 m",
    descSeo:
      "Pliage sur presse jusqu'à 3 m de long et 8 mm d'épaisseur, cintrage de tubes et de plats. Vos pièces arrivent formées, prêtes à poser.",
    intro:
      "Plier une tôle demande une presse, des outils et de l'expérience du retour élastique. Plutôt que d'improviser à l'étau, envoyez-nous la cote et l'angle : la pièce sort juste du premier coup.",
    points: [
      {
        titre: "Jusqu'à 3 m de long",
        texte:
          "Presse plieuse 3 mètres. Au-delà, la pièce se plie en plusieurs tronçons à assembler, on vous dit tout de suite ce que ça implique.",
      },
      {
        titre: "Le rayon compte",
        texte:
          "En dessous d'un rayon intérieur égal à l'épaisseur, la fibre extérieure fissure. On adapte l'outil à votre épaisseur plutôt que de forcer.",
      },
      {
        titre: "Cintrage de tubes et de plats",
        texte:
          "Pour les mains courantes, les arceaux et les pièces courbes. Le rayon minimum dépend de la section — appelez-nous avant de dessiner.",
      },
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
    slug: "percage",
    nom: "Perçage & poinçonnage",
    accroche: "Les trous sont déjà faits, et ils tombent juste",
    titreSeo: "Perçage et poinçonnage acier — platines et profilés percés au plan",
    descSeo:
      "Perçage sur plan de platines, profilés et tôles. Trous de Ø 6 à Ø 30, entraxes garantis, oblongs possibles. Vos pièces arrivent prêtes à boulonner.",
    intro:
      "Percer une platine à la perceuse à main, c'est une demi-heure par trou et un entraxe approximatif. Sur perceuse à colonne avec un montage, c'est deux minutes et un entraxe au dixième — et c'est ce qui fait qu'une platine tombe en face des chevilles du premier coup.",
    points: [
      {
        titre: "L'entraxe est garanti",
        texte:
          "C'est ce qui compte vraiment : un trou mal placé condamne la pièce. On travaille au montage, pas au pointeau.",
      },
      {
        titre: "Trous oblongs disponibles",
        texte:
          "Indispensables dès qu'il faut rattraper une tolérance de maçonnerie ou absorber une dilatation.",
      },
      {
        titre: "Un croquis coté suffit",
        texte:
          "Pas besoin de DAO. Un croquis à main levée avec les cotes et les diamètres est parfaitement exploitable.",
      },
    ],
    specs: [
      { label: "Diamètres", valeur: "Ø 6 à Ø 30 mm" },
      { label: "Épaisseur max", valeur: "20 mm" },
      { label: "Tolérance d'entraxe", valeur: "± 0,5 mm" },
      { label: "Oblongs", valeur: "Sur demande" },
      { label: "Chanfrein", valeur: "Sur demande" },
    ],
    delai: "2 à 4 jours ouvrables",
    prix: "À partir de 1,20 € le trou",
  },
  {
    slug: "conseil-technique",
    nom: "Conseil technique",
    accroche: "40 ans d'expérience au bout du fil",
    titreSeo: "Conseil technique acier — nuance, épaisseur, protection : on vous oriente",
    descSeo:
      "Un doute sur la nuance, l'épaisseur ou la protection ? Décrivez votre projet, on vous oriente vers le bon produit — gratuitement, et sans vous vendre plus que nécessaire.",
    intro:
      "La moitié des appels qu'on reçoit commencent par « je ne sais pas trop quoi demander ». C'est normal, et c'est exactement pour ça qu'on répond au téléphone. Décrivez ce que vous voulez construire, on traduit en références.",
    points: [
      {
        titre: "On vous dit aussi quand c'est trop",
        texte:
          "Si une section plus petite suffit, on vous le dit. Un client qui revient vaut mieux qu'une vente surdimensionnée.",
      },
      {
        titre: "On vous dit quand ça ne relève pas de nous",
        texte:
          "Dès qu'il y a une charge de structure, il faut un calcul d'ingénieur. On vous le dira clairement plutôt que de vous vendre une poutrelle au jugé.",
      },
      {
        titre: "Particuliers bienvenus",
        texte:
          "Aucun compte professionnel n'est nécessaire, et aucune question n'est trop simple. On explique sans jargon.",
      },
    ],
    specs: [
      { label: "Par téléphone", valeur: "Du lundi au vendredi, 7 h – 17 h" },
      { label: "Par e-mail", valeur: "Réponse sous 24 h ouvrées" },
      { label: "Au comptoir", valeur: "Dans les 4 dépôts, sans rendez-vous" },
      { label: "Tarif", valeur: "Gratuit" },
    ],
    delai: "Immédiat par téléphone",
    prix: "Gratuit",
  },
  {
    slug: "click-and-collect",
    nom: "Click & collect",
    accroche: "Vous commandez, vous retirez — souvent le jour même",
    titreSeo: "Click & collect acier — commande et retrait en dépôt le jour même",
    descSeo:
      "Commandez par mail ou par téléphone, retirez dans le dépôt de votre choix, souvent le jour même. Pas de frais de livraison, pas d'attente au comptoir.",
    intro:
      "Notre modèle est le retrait en dépôt, et c'est assumé : pas de camion à financer, donc des prix au mètre qui restent tenus. Vous commandez à l'avance, la commande est préparée, vous ne faites que charger.",
    points: [
      {
        titre: "Préparé avant votre arrivée",
        texte:
          "Coupé, compté, mis de côté. Vous ne cherchez pas dans le rack et vous n'attendez pas derrière quelqu'un.",
      },
      {
        titre: "Quatre dépôts",
        texte:
          "Charleroi, La Louvière, Tournai et Marville. Vous choisissez celui qui vous arrange, on transfère si la référence est ailleurs.",
      },
      {
        titre: "Aide au chargement",
        texte:
          "Chariot élévateur disponible aux heures d'ouverture. Prévenez-nous si la pièce dépasse 100 kg ou 6 mètres.",
      },
    ],
    specs: [
      { label: "Commande", valeur: "Par e-mail ou par téléphone" },
      { label: "Préparation", valeur: "Souvent le jour même" },
      { label: "Dépôts", valeur: "Charleroi · La Louvière · Tournai · Marville" },
      { label: "Frais", valeur: "Aucun" },
      { label: "Paiement", valeur: "Au retrait" },
    ],
    delai: "Le jour même si en stock",
    prix: "Sans frais",
  },
  {
    slug: "transformation",
    nom: "Transformation sur plan",
    accroche: "Vous envoyez le plan, vous recevez la pièce",
    titreSeo: "Transformation acier sur plan — pièces prêtes à poser, certifié EN1090",
    descSeo:
      "Ensembles soudés, assemblages et pièces complexes réalisés sur plan dans notre atelier certifié EN1090-Exc2. De la platine au portique.",
    intro:
      "Pour ce qui dépasse la coupe et le pli, l'atelier prend le relais. Assemblages soudés, ensembles mécanosoudés, pièces de reprise : vous fournissez le plan ou le croquis, nous livrons la pièce finie, contrôlée et traçable.",
    points: [
      {
        titre: "Certifié EN1090-Exc2",
        texte:
          "C'est la norme européenne qui encadre la fabrication des structures en acier. Peu d'acteurs de notre taille la détiennent — elle est exigée dès qu'une pièce entre dans un ouvrage soumis à contrôle.",
      },
      {
        titre: "Du croquis au plan DAO",
        texte:
          "On travaille aussi bien sur un dessin coté à la main que sur un DXF. Si le plan manque d'une cote, on appelle plutôt que d'interpréter.",
      },
      {
        titre: "Protection incluse si besoin",
        texte:
          "Galvanisation à chaud ou thermolaquage RAL en sous-traitance suivie. La pièce arrive protégée, prête à poser.",
      },
    ],
    specs: [
      { label: "Certification", valeur: "EN1090-Exc2" },
      { label: "Procédés", valeur: "MIG/MAG, MMA, TIG" },
      { label: "Formats", valeur: "Croquis coté, PDF, DXF" },
      { label: "Protection", valeur: "Galvanisation ou thermolaquage" },
      { label: "Traçabilité", valeur: "Certificat matière sur demande" },
    ],
    delai: "Sur planning, annoncé au devis",
    prix: "Sur devis sous 24 h",
  },
];

export const serviceBySlug = (slug: string) => servicesDetail.find((s) => s.slug === slug);

/* ------------------------------------------------------------------ */
/*  DÉPÔTS                                                             */
/* ------------------------------------------------------------------ */

export type DepotDetail = {
  slug: string;
  ville: string;
  pays: string;
  region: string;
  adresse: string;
  tel: string;
  horaires: { jours: string; heures: string }[];
  intro: string;
  equipements: string[];
  dessert: string[];
};

export const depotsDetail: DepotDetail[] = [
  {
    slug: "charleroi",
    ville: "Charleroi",
    pays: "Belgique",
    region: "Hainaut",
    adresse: "Zoning industriel, Charleroi",
    tel: "+32 (0)71 00 00 00",
    horaires: [
      { jours: "Lundi – Vendredi", heures: "7 h – 17 h" },
      { jours: "Samedi", heures: "8 h – 12 h" },
      { jours: "Dimanche", heures: "Fermé" },
    ],
    intro:
      "Le dépôt historique et le plus profond en stock. C'est ici que sont tenues les grandes longueurs et les sections lourdes, et c'est de là que partent les transferts vers les autres sites.",
    equipements: [
      "Scie à ruban jusqu'à 300 mm",
      "Cisaille 3 m",
      "Presse plieuse 3 m",
      "Oxycoupage",
      "Chariot élévateur 5 t",
      "Parking poids lourd",
    ],
    dessert: ["Charleroi", "Châtelet", "Fleurus", "Gerpinnes", "Courcelles", "Fontaine-l'Évêque"],
  },
  {
    slug: "la-louviere",
    ville: "La Louvière",
    pays: "Belgique",
    region: "Hainaut",
    adresse: "Zoning, La Louvière",
    tel: "+32 (0)64 00 00 00",
    horaires: [
      { jours: "Lundi – Vendredi", heures: "7 h – 17 h" },
      { jours: "Samedi", heures: "Fermé" },
      { jours: "Dimanche", heures: "Fermé" },
    ],
    intro:
      "Le dépôt du Centre, orienté chantier et ferronnerie : tubes, cornières, plats et tôles courantes en stock permanent, avec la découpe sur place.",
    equipements: ["Scie à ruban", "Cisaille 2 m", "Perçage", "Chariot élévateur 3,5 t"],
    dessert: ["La Louvière", "Binche", "Soignies", "Manage", "Morlanwelz", "Le Rœulx"],
  },
  {
    slug: "tournai",
    ville: "Tournai",
    pays: "Belgique",
    region: "Hainaut occidental",
    adresse: "Zoning, Tournai",
    tel: "+32 (0)69 00 00 00",
    horaires: [
      { jours: "Lundi – Vendredi", heures: "7 h – 17 h" },
      { jours: "Samedi", heures: "Fermé" },
      { jours: "Dimanche", heures: "Fermé" },
    ],
    intro:
      "Le dépôt de l'ouest wallon, à vingt minutes de la frontière française. Stock courant complet et transferts quotidiens depuis Charleroi pour les références spécifiques.",
    equipements: ["Scie à ruban", "Cisaille 2 m", "Chariot élévateur 3,5 t"],
    dessert: ["Tournai", "Ath", "Mouscron", "Leuze-en-Hainaut", "Péruwelz", "Lille (FR)"],
  },
  {
    slug: "marville",
    ville: "Marville",
    pays: "France",
    region: "Meuse (55)",
    adresse: "Zone d'activité, Marville",
    tel: "+33 (0)3 00 00 00 00",
    horaires: [
      { jours: "Lundi – Vendredi", heures: "8 h – 17 h" },
      { jours: "Samedi", heures: "Fermé" },
      { jours: "Dimanche", heures: "Fermé" },
    ],
    intro:
      "Notre implantation française, au nord de la Meuse. Elle dessert le Grand Est et le sud de la Belgique, avec le même catalogue et les mêmes services de découpe.",
    equipements: ["Scie à ruban", "Cisaille 2 m", "Chariot élévateur 3,5 t", "Parking poids lourd"],
    dessert: ["Marville", "Longuyon", "Montmédy", "Verdun", "Longwy", "Virton (BE)"],
  },
];

export const depotBySlug = (slug: string) => depotsDetail.find((d) => d.slug === slug);
