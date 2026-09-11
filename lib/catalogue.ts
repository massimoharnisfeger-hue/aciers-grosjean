/**
 * Catalogue — calqué sur l'architecture réelle d'aciersgrosjean.be
 * (pages matières /inox, /aluminium + familles poutrelles, cornières,
 * poteaux de clôture, visserie… + fiches produits au niveau de la référence).
 * Les URLs sont assainies : hiérarchie famille → référence, sans accent.
 */

export type Spec = { label: string; valeur: string };

export type Ref = {
  ref: string;
  nom: string;
  dims: string;
  prix: string;
  unite: string;
  stock: boolean;
  resume: string;
  specs: Spec[];
  usages: string[];
};

export type Famille = {
  slug: string;
  nom: string;
  accroche: string;
  intro: string;
  art: string;
  refs: Ref[];
};

export type Matiere = {
  slug: string;
  nom: string;
  accroche: string;
  intro: string;
  proprietes: Spec[];
  usages: string[];
  familles: string[];
};

/* ----------------------------- MATIÈRES ----------------------------- */

export const matieres: Matiere[] = [
  {
    slug: "acier",
    nom: "Acier",
    accroche: "La matière de structure, brute ou protégée",
    intro:
      "L'acier de construction couvre l'essentiel des besoins : structure, ossature, ferronnerie. Brut pour l'intérieur ou les pièces peintes, galvanisé dès que l'ouvrage est exposé. C'est la matière la plus disponible et la mieux placée en prix.",
    proprietes: [
      { label: "Nuances courantes", valeur: "S235JR · S275 · S355" },
      { label: "États", valeur: "Brut laminé à chaud, galvanisé à chaud" },
      { label: "Soudabilité", valeur: "Excellente" },
      { label: "Tenue extérieure", valeur: "Galvanisation requise" },
    ],
    usages: ["Charpente", "Mezzanine", "Portail", "Garde-corps", "Ferronnerie"],
    familles: ["poutrelles", "cornieres", "tubes", "toles"],
  },
  {
    slug: "inox",
    nom: "Inox",
    accroche: "Pour ce qui doit tenir dehors, sans entretien",
    intro:
      "L'inox ne rouille pas : c'est la matière des ouvrages exposés et des environnements exigeants. Le 304 couvre la majorité des usages extérieurs ; le 316, allié au molybdène, résiste en bord de mer et en milieu chloré.",
    proprietes: [
      { label: "Nuances", valeur: "304 (1.4301) · 316L (1.4404)" },
      { label: "Finitions", valeur: "Brut, brossé grain 240, poli" },
      { label: "Tenue à la corrosion", valeur: "Très élevée — sans traitement" },
      { label: "Usage littoral", valeur: "316L recommandé" },
    ],
    usages: ["Garde-corps", "Agroalimentaire", "Bord de mer", "Mobilier extérieur", "Piscine"],
    familles: ["tubes", "toles", "cornieres"],
  },
  {
    slug: "aluminium",
    nom: "Aluminium",
    accroche: "Trois fois plus léger, jamais de rouille",
    intro:
      "Le profilé aluminium s'impose dès que le poids compte ou que la structure doit rester nue sans rouiller. Il s'usine et se perce facilement, mais se soude différemment de l'acier — on vous oriente sur l'assemblage.",
    proprietes: [
      { label: "Alliages", valeur: "6060 · 6082" },
      { label: "Densité", valeur: "2,7 — contre 7,85 pour l'acier" },
      { label: "Tenue à la corrosion", valeur: "Naturelle (couche d'alumine)" },
      { label: "Finitions", valeur: "Brut, anodisé, thermolaqué" },
    ],
    usages: ["Habillage", "Menuiserie", "Structure légère", "Mobilier", "Signalétique"],
    familles: ["tubes", "toles", "cornieres"],
  },
];

/* ----------------------------- FAMILLES ----------------------------- */

export const familles: Famille[] = [
  {
    slug: "poutrelles",
    nom: "Poutrelles & profilés",
    accroche: "IPE, HEA, HEB — la structure porteuse",
    intro:
      "Profilés normalisés laminés à chaud. L'IPE porte en flexion sur de longues portées ; les HEA et HEB, plus larges d'aile, reprennent la compression et conviennent aux poteaux.",
    art: "poutrelles",
    refs: [
      {
        ref: "ipe-120",
        nom: "Poutrelle IPE 120",
        dims: "120 × 64 mm",
        prix: "Sur devis",
        unite: "au mètre",
        stock: true,
        resume: "Le profil de flexion le plus courant en habitation : linteaux, planchers, petites portées.",
        specs: [
          { label: "Hauteur", valeur: "120 mm" },
          { label: "Largeur d'aile", valeur: "64 mm" },
          { label: "Épaisseur d'âme", valeur: "4,4 mm" },
          { label: "Poids", valeur: "10,4 kg/m" },
          { label: "Nuance", valeur: "S235JR" },
          { label: "Longueur standard", valeur: "6 m ou 12 m" },
        ],
        usages: ["Linteau", "Plancher", "Petite portée"],
      },
      {
        ref: "heb-120",
        nom: "Poutrelle HEB 120",
        dims: "120 × 120 mm",
        prix: "Sur devis",
        unite: "au mètre",
        stock: true,
        resume: "Section carrée à ailes larges : le profil des poteaux et des reprises de charge importantes.",
        specs: [
          { label: "Hauteur", valeur: "120 mm" },
          { label: "Largeur d'aile", valeur: "120 mm" },
          { label: "Épaisseur d'âme", valeur: "6,5 mm" },
          { label: "Poids", valeur: "26,7 kg/m" },
          { label: "Nuance", valeur: "S235JR" },
          { label: "Longueur standard", valeur: "6 m ou 12 m" },
        ],
        usages: ["Poteau", "Reprise de charge", "Mezzanine"],
      },
      {
        ref: "hea-100",
        nom: "Poutrelle HEA 100",
        dims: "96 × 100 mm",
        prix: "Sur devis",
        unite: "au mètre",
        stock: true,
        resume: "Le compromis poids/résistance : plus léger qu'un HEB à encombrement voisin.",
        specs: [
          { label: "Hauteur", valeur: "96 mm" },
          { label: "Largeur d'aile", valeur: "100 mm" },
          { label: "Épaisseur d'âme", valeur: "5 mm" },
          { label: "Poids", valeur: "16,7 kg/m" },
          { label: "Nuance", valeur: "S235JR" },
          { label: "Longueur standard", valeur: "6 m ou 12 m" },
        ],
        usages: ["Ossature", "Poteau léger", "Charpente"],
      },
    ],
  },
  {
    slug: "cornieres",
    nom: "Cornières & plats",
    accroche: "L'angle qui raidit tout",
    intro:
      "La cornière égale laminée à chaud est la pièce de renfort universelle : cadre, support, raidisseur, bordure. Le plat complète la gamme pour la ferronnerie et les assemblages.",
    art: "cornieres-plats",
    refs: [
      {
        ref: "corniere-egale-40x40x4",
        nom: "Cornière égale 40 × 40 × 4",
        dims: "40 × 40 × 4 mm",
        prix: "2,85 €",
        unite: "au mètre",
        stock: true,
        resume:
          "La référence la plus demandée du catalogue. Laminée à chaud, ailes égales, prête à souder ou à boulonner.",
        specs: [
          { label: "Ailes", valeur: "40 × 40 mm" },
          { label: "Épaisseur", valeur: "4 mm" },
          { label: "Poids", valeur: "2,42 kg/m" },
          { label: "Nuance", valeur: "S235JR" },
          { label: "Procédé", valeur: "Laminé à chaud" },
          { label: "Longueur standard", valeur: "6 m — coupe sur mesure" },
        ],
        usages: ["Cadre", "Renfort", "Support", "Bordure"],
      },
      {
        ref: "corniere-egale-50x50x5",
        nom: "Cornière égale 50 × 50 × 5",
        dims: "50 × 50 × 5 mm",
        prix: "Sur devis",
        unite: "au mètre",
        stock: true,
        resume: "Section renforcée pour les cadres porteurs et les supports de charge.",
        specs: [
          { label: "Ailes", valeur: "50 × 50 mm" },
          { label: "Épaisseur", valeur: "5 mm" },
          { label: "Poids", valeur: "3,77 kg/m" },
          { label: "Nuance", valeur: "S235JR" },
          { label: "Procédé", valeur: "Laminé à chaud" },
          { label: "Longueur standard", valeur: "6 m — coupe sur mesure" },
        ],
        usages: ["Cadre porteur", "Support", "Châssis"],
      },
      {
        ref: "plat-30x3",
        nom: "Plat acier 30 × 3",
        dims: "30 × 3 mm",
        prix: "1,95 €",
        unite: "au mètre",
        stock: true,
        resume: "Le fer plat de ferronnerie : portails, grilles, pièces de liaison.",
        specs: [
          { label: "Largeur", valeur: "30 mm" },
          { label: "Épaisseur", valeur: "3 mm" },
          { label: "Poids", valeur: "0,71 kg/m" },
          { label: "Nuance", valeur: "S235JR" },
          { label: "Longueur standard", valeur: "6 m — coupe sur mesure" },
        ],
        usages: ["Ferronnerie", "Portail", "Grille", "Liaison"],
      },
    ],
  },
  {
    slug: "tubes",
    nom: "Tubes ronds & carrés",
    accroche: "L'ossature creuse, légère et rigide",
    intro:
      "À section égale, le tube offre une rigidité supérieure au plein pour un poids moindre. Carré pour les assemblages d'équerre, rond pour les mains courantes et le mobilier.",
    art: "tubes",
    refs: [
      {
        ref: "tube-carre-40x40x2",
        nom: "Tube carré 40 × 40 × 2",
        dims: "40 × 40 × 2 mm",
        prix: "3,20 €",
        unite: "au mètre",
        stock: true,
        resume: "Le tube d'ossature par défaut : portails, garde-corps, structures de mobilier.",
        specs: [
          { label: "Section", valeur: "40 × 40 mm" },
          { label: "Épaisseur", valeur: "2 mm" },
          { label: "Poids", valeur: "2,31 kg/m" },
          { label: "Nuance", valeur: "S235JRH" },
          { label: "Longueur standard", valeur: "6 m — coupe sur mesure" },
        ],
        usages: ["Portail", "Garde-corps", "Ossature", "Mobilier"],
      },
      {
        ref: "tube-rond-33-7x2",
        nom: "Tube rond Ø 33,7 × 2",
        dims: "Ø 33,7 × 2 mm",
        prix: "Sur devis",
        unite: "au mètre",
        stock: true,
        resume: "Diamètre de main courante normalisé — la prise en main de référence.",
        specs: [
          { label: "Diamètre extérieur", valeur: "33,7 mm" },
          { label: "Épaisseur", valeur: "2 mm" },
          { label: "Poids", valeur: "1,56 kg/m" },
          { label: "Nuance", valeur: "S235JRH" },
          { label: "Longueur standard", valeur: "6 m — coupe sur mesure" },
        ],
        usages: ["Main courante", "Barrière", "Mobilier"],
      },
    ],
  },
  {
    slug: "toles",
    nom: "Tôles",
    accroche: "Couvrir, habiller, fermer",
    intro:
      "Lisse pour les pièces usinées et les platines, larmée pour les sols antidérapants, nervurée pour le bardage et la toiture. Toutes disponibles au format et à la découpe.",
    art: "toles",
    refs: [
      {
        ref: "tole-lisse-2mm",
        nom: "Tôle lisse 2 mm",
        dims: "épaisseur 2 mm",
        prix: "18,50 €",
        unite: "au m²",
        stock: true,
        resume: "Tôle laminée à froid, surface plane : platines, habillages, pièces découpées.",
        specs: [
          { label: "Épaisseur", valeur: "2 mm" },
          { label: "Poids", valeur: "15,7 kg/m²" },
          { label: "Nuance", valeur: "DC01 / S235JR" },
          { label: "Formats", valeur: "2000 × 1000 · 2500 × 1250 mm" },
          { label: "Découpe", valeur: "Aux cotes, sur demande" },
        ],
        usages: ["Platine", "Habillage", "Pièce découpée"],
      },
      {
        ref: "tole-nervuree",
        nom: "Tôle profilée nervurée",
        dims: "profil bac acier",
        prix: "dès 14,71 €",
        unite: "au m²",
        stock: true,
        resume: "Bac acier de bardage et de toiture : grande portée, pose rapide, galvanisé ou prélaqué.",
        specs: [
          { label: "Type", valeur: "Bac acier nervuré" },
          { label: "Finitions", valeur: "Galvanisé ou prélaqué" },
          { label: "Longueurs", valeur: "Sur mesure, à la coupe" },
          { label: "Pose", valeur: "Recouvrement latéral" },
        ],
        usages: ["Toiture", "Bardage", "Abri", "Hangar"],
      },
    ],
  },
  {
    slug: "poteaux-cloture",
    nom: "Poteaux de clôture",
    accroche: "Ce qui tient la clôture debout",
    intro:
      "Poteaux galvanisés prêts à sceller ou à platiner, dimensionnés pour les grillages et panneaux rigides. Vendus à l'unité, avec les accessoires de fixation.",
    art: "tubes",
    refs: [
      {
        ref: "poteau-rond-48x1500",
        nom: "Poteau rond Ø 48 — 1500 mm",
        dims: "Ø 48 mm × 1500 mm",
        prix: "Sur devis",
        unite: "à l'unité",
        stock: true,
        resume: "Poteau galvanisé pour clôture souple ou panneau rigide, hauteur libre 1,20 m après scellement.",
        specs: [
          { label: "Diamètre", valeur: "48 mm" },
          { label: "Longueur", valeur: "1500 mm" },
          { label: "Protection", valeur: "Galvanisé à chaud" },
          { label: "Pose", valeur: "Scellement béton ou platine" },
          { label: "Accessoires", valeur: "Capuchon, colliers, platine" },
        ],
        usages: ["Clôture", "Grillage", "Panneau rigide"],
      },
    ],
  },
  {
    slug: "visserie",
    nom: "Visserie & fixation",
    accroche: "Ce qui assemble le reste",
    intro:
      "Vis autoforantes, boulonnerie et accessoires de fixation pour l'acier et le bac acier. Vendus au sachet ou à la boîte, en stock permanent.",
    art: "visserie",
    refs: [
      {
        ref: "vis-autoforante-6-3x100-hex-10",
        nom: "Vis autoforante 6,3 × 100 — tête hexagonale 10",
        dims: "6,3 × 100 mm",
        prix: "Sur devis",
        unite: "à la boîte",
        stock: true,
        resume:
          "Perce et fixe en une seule opération, sans avant-trou. Tête hexagonale de 10 mm, pour bac acier sur ossature métallique.",
        specs: [
          { label: "Diamètre", valeur: "6,3 mm" },
          { label: "Longueur", valeur: "100 mm" },
          { label: "Tête", valeur: "Hexagonale 10 mm" },
          { label: "Pointe", valeur: "Autoforante" },
          { label: "Protection", valeur: "Zinguée" },
          { label: "Conditionnement", valeur: "Boîte de 100" },
        ],
        usages: ["Bac acier", "Bardage", "Ossature métallique"],
      },
    ],
  },
];

/* ----------------------------- HELPERS ----------------------------- */

export const familleBySlug = (slug: string) => familles.find((f) => f.slug === slug);
export const matiereBySlug = (slug: string) => matieres.find((m) => m.slug === slug);
export const refBySlug = (famille: string, ref: string) =>
  familleBySlug(famille)?.refs.find((r) => r.ref === ref);

export const allRefs = familles.flatMap((f) =>
  f.refs.map((r) => ({ famille: f, ref: r }))
);
