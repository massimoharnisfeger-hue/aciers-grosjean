/**
 * Catalogue Aciers Grosjean
 * ------------------------------------------------------------------
 * Calqué sur l'architecture réelle d'aciersgrosjean.be relevée à l'audit :
 *   · pages matière      (/inox, /aluminium)
 *   · familles produits  (poutrelles, cornières, poteaux de clôture, visserie…)
 *   · fiches au grain de la référence
 *     (/vis-autoforante-pour-acier-63x-100-tête-hexagonale-de-10mm)
 *
 * Les URLs sont assainies : famille → référence, sans accent, sans identifiant CMS.
 * Les références sont les sections normalisées réellement tenues en stock par un
 * négoce acier (EN 10025 / 10219 / 10056). Poids calculés (densité 7,85 acier,
 * 8,00 inox, 2,70 aluminium) — prix indicatifs calibrés sur les tarifs publics
 * connus, à confirmer au devis (l'acier cote à la semaine).
 */

export type Spec = { label: string; valeur: string };

export type Ref = {
  ref: string;
  nom: string;
  dims: string;
  serie: string;
  matiere: string;
  kg: number;
  unitePoids: string;
  prix: number | null;
  prixTexte: string;
  unite: string;
  uniteCourte: string;
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
  titreSeo: string;
  descSeo: string;
  art: string;
  series: string[];
  refs: Ref[];
};

export type Matiere = {
  slug: string;
  nom: string;
  accroche: string;
  intro: string;
  titreSeo: string;
  descSeo: string;
  proprietes: Spec[];
  usages: string[];
  familles: string[];
  aRetenir: { titre: string; texte: string }[];
};

/* ------------------------------------------------------------------ */
/*  Tarification                                                       */
/* ------------------------------------------------------------------ */

const TARIF: Record<string, { kg: number; min: number }> = {
  poutrelles: { kg: 1.05, min: 6.0 },
  cornieres: { kg: 1.18, min: 1.6 },
  "plats-barres": { kg: 1.3, min: 1.95 },
  tubes: { kg: 1.385, min: 2.2 },
  toles: { kg: 1.18, min: 12.0 },
  treillis: { kg: 1.15, min: 3.0 },
  corten: { kg: 2.6, min: 18.0 },
  "poteaux-cloture": { kg: 1.9, min: 8.0 },
  visserie: { kg: 1.0, min: 0 },
  inox: { kg: 5.2, min: 6.0 },
  aluminium: { kg: 6.5, min: 5.0 },
};

/** Arrondi commercial : pas de 5 centimes sous 20 €, de 10 au-dessus. */
function arrondi(v: number) {
  const pas = v < 20 ? 0.05 : 0.1;
  return Math.round(v / pas) * pas;
}

function tarifer(famille: string, kg: number) {
  const t = TARIF[famille];
  if (!t) return null;
  return arrondi(Math.max(t.min, kg * t.kg));
}

export function formatPrix(v: number | null) {
  if (v === null) return "Sur devis";
  return v.toLocaleString("fr-BE", { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + " €";
}

const nb = (v: number, d = 2) =>
  v.toLocaleString("fr-BE", { minimumFractionDigits: d, maximumFractionDigits: d });

/* ------------------------------------------------------------------ */
/*  Fabrique de référence                                              */
/* ------------------------------------------------------------------ */

type MkArgs = {
  famille: string;
  ref: string;
  nom: string;
  dims: string;
  serie: string;
  matiere?: string;
  kg: number;
  unitePoids?: string;
  unite?: string;
  uniteCourte?: string;
  resume: string;
  specs: Spec[];
  usages: string[];
  prix?: number | null;
  surDevis?: boolean;
  stock?: boolean;
};

function mk(a: MkArgs): Ref {
  const unitePoids = a.unitePoids ?? "kg/m";
  const prix = a.surDevis ? null : a.prix !== undefined ? a.prix : tarifer(a.famille, a.kg);
  return {
    ref: a.ref,
    nom: a.nom,
    dims: a.dims,
    serie: a.serie,
    matiere: a.matiere ?? "acier",
    kg: a.kg,
    unitePoids,
    prix,
    prixTexte: formatPrix(prix),
    unite: a.unite ?? "au mètre",
    uniteCourte: a.uniteCourte ?? "€/m",
    stock: a.stock ?? true,
    resume: a.resume,
    specs: [...a.specs, { label: "Poids", valeur: `${nb(a.kg)} ${unitePoids}` }],
    usages: a.usages,
  };
}

const LONG_STD = { label: "Longueur standard", valeur: "6 m — découpe aux cotes" };
const LONG_PROFIL = { label: "Longueur standard", valeur: "6 m ou 12 m — découpe aux cotes" };

/* ------------------------------------------------------------------ */
/*  1 · POUTRELLES & PROFILÉS                                          */
/* ------------------------------------------------------------------ */

type Profil = [nom: string, h: number, b: number, tw: number, tf: number, kg: number];

const IPE: Profil[] = [
  ["80", 80, 46, 3.8, 5.2, 6.0], ["100", 100, 55, 4.1, 5.7, 8.1],
  ["120", 120, 64, 4.4, 6.3, 10.4], ["140", 140, 73, 4.7, 6.9, 12.9],
  ["160", 160, 82, 5.0, 7.4, 15.8], ["180", 180, 91, 5.3, 8.0, 18.8],
  ["200", 200, 100, 5.6, 8.5, 22.4], ["220", 220, 110, 5.9, 9.2, 26.2],
  ["240", 240, 120, 6.2, 9.8, 30.7], ["270", 270, 135, 6.6, 10.2, 36.1],
  ["300", 300, 150, 7.1, 10.7, 42.2], ["330", 330, 160, 7.5, 11.5, 49.1],
  ["360", 360, 170, 8.0, 12.7, 57.1], ["400", 400, 180, 8.6, 13.5, 66.3],
  ["450", 450, 190, 9.4, 14.6, 77.6], ["500", 500, 200, 10.2, 16.0, 90.7],
  ["550", 550, 210, 11.1, 17.2, 106.0], ["600", 600, 220, 12.0, 19.0, 122.0],
];

const HEA: Profil[] = [
  ["100", 96, 100, 5.0, 8.0, 16.7], ["120", 114, 120, 5.0, 8.0, 19.9],
  ["140", 133, 140, 5.5, 8.5, 24.7], ["160", 152, 160, 6.0, 9.0, 30.4],
  ["180", 171, 180, 6.0, 9.5, 35.5], ["200", 190, 200, 6.5, 10.0, 42.3],
  ["220", 210, 220, 7.0, 11.0, 50.5], ["240", 230, 240, 7.5, 12.0, 60.3],
  ["260", 250, 260, 7.5, 12.5, 68.2], ["280", 270, 280, 8.0, 13.0, 76.4],
  ["300", 290, 300, 8.5, 14.0, 88.3],
];

const HEB: Profil[] = [
  ["100", 100, 100, 6.0, 10.0, 20.4], ["120", 120, 120, 6.5, 11.0, 26.7],
  ["140", 140, 140, 7.0, 12.0, 33.7], ["160", 160, 160, 8.0, 13.0, 42.6],
  ["180", 180, 180, 8.5, 14.0, 51.2], ["200", 200, 200, 9.0, 15.0, 61.3],
  ["220", 220, 220, 9.5, 16.0, 71.5], ["240", 240, 240, 10.0, 17.0, 83.2],
  ["260", 260, 260, 10.0, 17.5, 93.0], ["280", 280, 280, 10.5, 18.0, 103.0],
  ["300", 300, 300, 11.0, 19.0, 117.0],
];

const IPN: Profil[] = [
  ["80", 80, 42, 3.9, 5.9, 5.94], ["100", 100, 50, 4.5, 6.8, 8.34],
  ["120", 120, 58, 5.1, 7.7, 11.1], ["140", 140, 66, 5.7, 8.6, 14.3],
  ["160", 160, 74, 6.3, 9.5, 17.9], ["180", 180, 82, 6.9, 10.4, 21.9],
  ["200", 200, 90, 7.5, 11.3, 26.2], ["220", 220, 98, 8.1, 12.2, 31.1],
  ["240", 240, 106, 8.7, 13.1, 36.2],
];

const UPN: Profil[] = [
  ["50", 50, 25, 5.0, 7.0, 5.59], ["65", 65, 42, 5.5, 7.5, 7.09],
  ["80", 80, 45, 6.0, 8.0, 8.64], ["100", 100, 50, 6.0, 8.5, 10.6],
  ["120", 120, 55, 7.0, 9.0, 13.4], ["140", 140, 60, 7.0, 10.0, 16.0],
  ["160", 160, 65, 7.5, 10.5, 18.8], ["180", 180, 70, 8.0, 11.0, 22.0],
  ["200", 200, 75, 8.5, 11.5, 25.3], ["220", 220, 80, 9.0, 12.5, 29.4],
  ["240", 240, 85, 9.5, 13.0, 33.2], ["260", 260, 90, 10.0, 14.0, 37.9],
  ["300", 300, 100, 10.0, 16.0, 46.2],
];

const RESUME_PROFIL: Record<string, string> = {
  IPE: "Profil en I à ailes parallèles : le meilleur rendement en flexion sur longue portée. C'est le profil des linteaux et des planchers.",
  IPN: "Profil en I à ailes inclinées, le plus ancien du catalogue. Toujours demandé en rénovation pour reprendre un existant à l'identique.",
  HEA: "Profil H allégé : ailes larges pour la compression, âme fine pour le poids. Le compromis des poteaux et des ossatures courantes.",
  HEB: "Profil H lourd, section quasi carrée : le plus résistant à encombrement égal. Poteaux, reprises de charge, portiques.",
  UPN: "Profil en U à ailes inclinées : chevêtres, rives de plancher, glissières, encadrements. Se boulonne à plat sans usinage.",
};

const USAGES_PROFIL: Record<string, string[]> = {
  IPE: ["Linteau", "Plancher", "Poutre", "Mezzanine"],
  IPN: ["Rénovation", "Linteau", "Reprise d'existant"],
  HEA: ["Poteau", "Ossature", "Charpente"],
  HEB: ["Poteau", "Reprise de charge", "Portique"],
  UPN: ["Chevêtre", "Rive de plancher", "Encadrement", "Glissière"],
};

function profils(serie: string, table: Profil[]): Ref[] {
  return table.map(([n, h, b, tw, tf, kg]) =>
    mk({
      famille: "poutrelles",
      ref: `${serie.toLowerCase()}-${n}`,
      nom: `Poutrelle ${serie} ${n}`,
      dims: `${h} × ${b} mm`,
      serie,
      kg,
      resume: RESUME_PROFIL[serie],
      specs: [
        { label: "Hauteur (h)", valeur: `${nb(h, 0)} mm` },
        { label: "Largeur d'aile (b)", valeur: `${nb(b, 0)} mm` },
        { label: "Épaisseur d'âme (tw)", valeur: `${nb(tw, 1)} mm` },
        { label: "Épaisseur d'aile (tf)", valeur: `${nb(tf, 1)} mm` },
        { label: "Nuance", valeur: "S235JR — EN 10025-2" },
        { label: "Procédé", valeur: "Laminé à chaud" },
        LONG_PROFIL,
      ],
      usages: USAGES_PROFIL[serie],
    })
  );
}

/* ------------------------------------------------------------------ */
/*  2 · CORNIÈRES                                                      */
/* ------------------------------------------------------------------ */

const CORN_EGALES: [number, number][] = [
  [20, 3], [25, 3], [25, 4], [30, 3], [30, 4], [30, 5], [35, 4], [40, 4], [40, 5],
  [45, 5], [50, 5], [50, 6], [60, 6], [60, 8], [70, 7], [80, 8], [90, 9],
  [100, 10], [120, 12],
];

const CORN_INEGALES: [number, number, number][] = [
  [30, 20, 3], [40, 20, 4], [40, 25, 4], [50, 30, 5], [60, 40, 5], [60, 40, 6],
  [65, 50, 5], [70, 50, 6], [80, 40, 6], [80, 60, 7], [100, 50, 8], [100, 65, 8],
  [100, 75, 10],
];

/** Congé de raccordement et arrondis de bec : +1,3 % sur la section théorique
 *  d'une cornière (EN 10056). Sans ce facteur, la 40×40×4 tombe à 2,39 kg/m
 *  au lieu des 2,42 kg/m normalisés — et le prix public de 2,85 €/m est faux. */
const CONGE_CORNIERE = 1.013;

const cornieresEgales: Ref[] = CORN_EGALES.map(([a, e]) => {
  const kg = +(((2 * a - e) * e * 7.85 * CONGE_CORNIERE) / 1000).toFixed(2);
  return mk({
    famille: "cornieres",
    ref: `corniere-egale-${a}x${a}x${e}`,
    nom: `Cornière égale ${a} × ${a} × ${e}`,
    dims: `${a} × ${a} × ${e} mm`,
    serie: "Cornière égale",
    kg,
    resume:
      a === 40 && e === 4
        ? "La référence la plus demandée du catalogue. Laminée à chaud, ailes égales, prête à souder ou à boulonner."
        : "Cornière à ailes égales laminée à chaud : la pièce de renfort universelle — cadre, support, raidisseur, bordure.",
    specs: [
      { label: "Ailes", valeur: `${a} × ${a} mm` },
      { label: "Épaisseur", valeur: `${e} mm` },
      { label: "Nuance", valeur: "S235JR — EN 10056" },
      { label: "Procédé", valeur: "Laminé à chaud" },
      LONG_STD,
    ],
    usages: ["Cadre", "Renfort", "Support", "Bordure"],
  });
});

const cornieresInegales: Ref[] = CORN_INEGALES.map(([a, b, e]) => {
  const kg = +(((a + b - e) * e * 7.85 * CONGE_CORNIERE) / 1000).toFixed(2);
  return mk({
    famille: "cornieres",
    ref: `corniere-inegale-${a}x${b}x${e}`,
    nom: `Cornière inégale ${a} × ${b} × ${e}`,
    dims: `${a} × ${b} × ${e} mm`,
    serie: "Cornière inégale",
    kg,
    resume:
      "Ailes de largeurs différentes : la grande aile porte, la petite se fixe. Le profil des rives, des seuils et des supports asymétriques.",
    specs: [
      { label: "Grande aile", valeur: `${a} mm` },
      { label: "Petite aile", valeur: `${b} mm` },
      { label: "Épaisseur", valeur: `${e} mm` },
      { label: "Nuance", valeur: "S235JR — EN 10056" },
      LONG_STD,
    ],
    usages: ["Rive", "Seuil", "Support", "Encadrement"],
  });
});

/* ------------------------------------------------------------------ */
/*  3 · PLATS & BARRES                                                 */
/* ------------------------------------------------------------------ */

const PLATS: [number, number][] = [
  [20, 3], [20, 4], [20, 5], [25, 3], [25, 4], [25, 5], [30, 3], [30, 4], [30, 5],
  [30, 6], [35, 5], [40, 3], [40, 4], [40, 5], [40, 6], [40, 8], [45, 5], [50, 4],
  [50, 5], [50, 6], [50, 8], [50, 10], [60, 5], [60, 6], [60, 8], [60, 10],
  [70, 6], [70, 8], [80, 6], [80, 8], [80, 10], [90, 8], [100, 6], [100, 8],
  [100, 10], [100, 12], [120, 10], [150, 10],
];

const RONDS = [6, 8, 10, 12, 14, 16, 18, 20, 22, 25, 28, 30, 35, 40, 45, 50, 60, 70, 80];
const CARRES = [8, 10, 12, 14, 16, 20, 25, 30, 35, 40, 50];

const plats: Ref[] = PLATS.map(([l, e]) => {
  const kg = +((l * e * 7.85) / 1000).toFixed(2);
  return mk({
    famille: "plats-barres",
    ref: `plat-${l}x${e}`,
    nom: `Plat acier ${l} × ${e}`,
    dims: `${l} × ${e} mm`,
    serie: "Plat",
    kg,
    resume:
      "Le fer plat de ferronnerie : portails, grilles, pièces de liaison, platines. Se perce, se cintre et se soude sans préparation.",
    specs: [
      { label: "Largeur", valeur: `${l} mm` },
      { label: "Épaisseur", valeur: `${e} mm` },
      { label: "Nuance", valeur: "S235JR — EN 10058" },
      { label: "Procédé", valeur: "Laminé à chaud" },
      LONG_STD,
    ],
    usages: ["Ferronnerie", "Portail", "Grille", "Platine"],
  });
});

const ronds: Ref[] = RONDS.map((d) => {
  const kg = +(d * d * 0.00617).toFixed(2);
  return mk({
    famille: "plats-barres",
    ref: `rond-plein-${d}`,
    nom: `Rond plein Ø ${d}`,
    dims: `Ø ${d} mm`,
    serie: "Rond plein",
    kg,
    resume:
      "Barre ronde pleine laminée : barreaudage, axes, tiges, pièces tournées. La section pleine encaisse la torsion.",
    specs: [
      { label: "Diamètre", valeur: `${d} mm` },
      { label: "Nuance", valeur: "S235JR" },
      { label: "Procédé", valeur: "Laminé à chaud" },
      LONG_STD,
    ],
    usages: ["Barreaudage", "Axe", "Tige", "Usinage"],
  });
});

const carres: Ref[] = CARRES.map((a) => {
  const kg = +(a * a * 0.00785).toFixed(2);
  return mk({
    famille: "plats-barres",
    ref: `carre-plein-${a}`,
    nom: `Carré plein ${a} × ${a}`,
    dims: `${a} × ${a} mm`,
    serie: "Carré plein",
    kg,
    resume:
      "Barre carrée pleine : barreaudage décoratif, grilles de défense, pièces de ferronnerie traditionnelle.",
    specs: [
      { label: "Section", valeur: `${a} × ${a} mm` },
      { label: "Nuance", valeur: "S235JR" },
      { label: "Procédé", valeur: "Laminé à chaud" },
      LONG_STD,
    ],
    usages: ["Barreaudage", "Grille", "Ferronnerie"],
  });
});

/* ------------------------------------------------------------------ */
/*  4 · TUBES                                                          */
/* ------------------------------------------------------------------ */

const TUBES_CARRES: [number, number][] = [
  [20, 2], [25, 2], [30, 2], [30, 3], [35, 2], [40, 2], [40, 3], [40, 4],
  [50, 2], [50, 3], [50, 4], [50, 5], [60, 3], [60, 4], [60, 5], [70, 3],
  [70, 4], [80, 3], [80, 4], [80, 5], [90, 4], [100, 3], [100, 4], [100, 5],
  [120, 5], [140, 5], [150, 6],
];

const TUBES_RECT: [number, number, number][] = [
  [40, 20, 2], [50, 25, 2], [50, 30, 2], [60, 30, 2], [60, 40, 2], [60, 40, 3],
  [70, 50, 3], [80, 40, 3], [80, 40, 4], [80, 60, 3], [90, 50, 3], [100, 50, 3],
  [100, 50, 4], [100, 60, 4], [120, 60, 4], [120, 80, 4], [140, 80, 4], [150, 100, 5],
];

const TUBES_RONDS: [string, number, number][] = [
  ["21-3", 21.3, 2], ["26-9", 26.9, 2], ["33-7", 33.7, 2], ["33-7-26", 33.7, 2.6],
  ["42-4", 42.4, 2], ["42-4-26", 42.4, 2.6], ["48-3", 48.3, 2], ["48-3-3", 48.3, 3],
  ["60-3", 60.3, 2.9], ["60-3-36", 60.3, 3.6], ["76-1", 76.1, 3],
  ["88-9", 88.9, 3.2], ["101-6", 101.6, 3.6], ["114-3", 114.3, 3.6], ["139-7", 139.7, 4],
];

const tubesCarres: Ref[] = TUBES_CARRES.map(([a, e]) => {
  const kg = +(4 * (a - e) * e * 0.00785 * 0.97).toFixed(2);
  return mk({
    famille: "tubes",
    ref: `tube-carre-${a}x${a}x${e}`,
    nom: `Tube carré ${a} × ${a} × ${e}`,
    dims: `${a} × ${a} × ${e} mm`,
    serie: "Tube carré",
    kg,
    resume:
      "Le tube d'ossature par défaut : à poids égal, il est plus rigide que le plein, et ses quatre faces planes se soudent d'équerre sans préparation.",
    specs: [
      { label: "Section", valeur: `${a} × ${a} mm` },
      { label: "Épaisseur", valeur: `${e} mm` },
      { label: "Nuance", valeur: "S235JRH — EN 10219" },
      { label: "Formage", valeur: "Profilé à froid, soudé" },
      LONG_STD,
    ],
    usages: ["Portail", "Garde-corps", "Ossature", "Mobilier"],
  });
});

const tubesRect: Ref[] = TUBES_RECT.map(([a, b, e]) => {
  const kg = +(2 * (a + b - 2 * e) * e * 0.00785 * 0.97).toFixed(2);
  return mk({
    famille: "tubes",
    ref: `tube-rectangulaire-${a}x${b}x${e}`,
    nom: `Tube rectangulaire ${a} × ${b} × ${e}`,
    dims: `${a} × ${b} × ${e} mm`,
    serie: "Tube rectangulaire",
    kg,
    resume:
      "Section rectangulaire : la rigidité se concentre dans le sens de la hauteur. Le profil des traverses et des poutres de portail.",
    specs: [
      { label: "Section", valeur: `${a} × ${b} mm` },
      { label: "Épaisseur", valeur: `${e} mm` },
      { label: "Nuance", valeur: "S235JRH — EN 10219" },
      { label: "Formage", valeur: "Profilé à froid, soudé" },
      LONG_STD,
    ],
    usages: ["Traverse", "Poutre de portail", "Ossature", "Châssis"],
  });
});

const tubesRonds: Ref[] = TUBES_RONDS.map(([id, d, e]) => {
  const kg = +((d - e) * e * 0.02466).toFixed(2);
  return mk({
    famille: "tubes",
    ref: `tube-rond-${id}`,
    nom: `Tube rond Ø ${nb(d, 1)} × ${nb(e, 1)}`,
    dims: `Ø ${nb(d, 1)} × ${nb(e, 1)} mm`,
    serie: "Tube rond",
    kg,
    resume:
      d === 33.7
        ? "Diamètre de main courante normalisé — la prise en main de référence des garde-corps."
        : "Tube rond soudé : mains courantes, barrières, mobilier, structures cintrées.",
    specs: [
      { label: "Diamètre extérieur", valeur: `${nb(d, 1)} mm` },
      { label: "Épaisseur", valeur: `${nb(e, 1)} mm` },
      { label: "Diamètre intérieur", valeur: `${nb(d - 2 * e, 1)} mm` },
      { label: "Nuance", valeur: "S235JRH — EN 10219" },
      LONG_STD,
    ],
    usages: ["Main courante", "Barrière", "Mobilier", "Cintrage"],
  });
});

/* ------------------------------------------------------------------ */
/*  5 · TÔLES                                                          */
/* ------------------------------------------------------------------ */

const EP_LISSES = [1, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10, 12, 15, 20];
const EP_LARMEES: [number, number][] = [[2, 4], [3, 5], [4, 6], [5, 7], [6, 8]];
const EP_GALVA = [0.75, 1, 1.5, 2, 2.5, 3];

const tolesLisses: Ref[] = EP_LISSES.map((e) => {
  const kg = +(e * 7.85).toFixed(2);
  return mk({
    famille: "toles",
    ref: `tole-lisse-${String(e).replace(".", "-")}mm`,
    nom: `Tôle lisse ${nb(e, e % 1 ? 1 : 0)} mm`,
    dims: `épaisseur ${nb(e, e % 1 ? 1 : 0)} mm`,
    serie: "Tôle lisse",
    kg,
    unitePoids: "kg/m²",
    unite: "au m²",
    uniteCourte: "€/m²",
    resume:
      "Tôle laminée à surface plane : platines, goussets, habillages, pièces découpées au plan. Se débite aux cotes exactes.",
    specs: [
      { label: "Épaisseur", valeur: `${nb(e, e % 1 ? 1 : 0)} mm` },
      { label: "Nuance", valeur: e <= 3 ? "DC01 — laminé à froid" : "S235JR — laminé à chaud" },
      { label: "Formats", valeur: "2000 × 1000 · 2500 × 1250 · 3000 × 1500 mm" },
      { label: "Découpe", valeur: "Cisaillage ou oxycoupage aux cotes" },
    ],
    usages: ["Platine", "Gousset", "Habillage", "Pièce au plan"],
  });
});

const tolesLarmees: Ref[] = EP_LARMEES.map(([e, t]) => {
  const kg = +(e * 7.85 + 1.6).toFixed(2);
  return mk({
    famille: "toles",
    ref: `tole-larmee-${e}-${t}mm`,
    nom: `Tôle larmée ${e}/${t} mm`,
    dims: `${e}/${t} mm — motif damier`,
    serie: "Tôle larmée",
    kg,
    unitePoids: "kg/m²",
    unite: "au m²",
    uniteCourte: "€/m²",
    resume:
      "Motif en relief antidérapant laminé dans la masse : planchers techniques, marches, passerelles, seuils de véhicule.",
    specs: [
      { label: "Épaisseur de base", valeur: `${e} mm` },
      { label: "Épaisseur au relief", valeur: `${t} mm` },
      { label: "Motif", valeur: "Damier (larmes croisées)" },
      { label: "Nuance", valeur: "S235JR" },
      { label: "Formats", valeur: "2000 × 1000 · 2500 × 1250 mm" },
    ],
    usages: ["Plancher technique", "Marche", "Passerelle", "Seuil"],
  });
});

const tolesGalva: Ref[] = EP_GALVA.map((e) => {
  const kg = +(e * 7.85).toFixed(2);
  return mk({
    famille: "toles",
    ref: `tole-galvanisee-${String(e).replace(".", "-")}mm`,
    nom: `Tôle galvanisée ${nb(e, e % 1 ? 2 : 0)} mm`,
    dims: `épaisseur ${nb(e, e % 1 ? 2 : 0)} mm`,
    serie: "Tôle galvanisée",
    matiere: "galvanise",
    kg,
    unitePoids: "kg/m²",
    unite: "au m²",
    uniteCourte: "€/m²",
    prix: arrondi(Math.max(14, e * 7.85 * 1.55)),
    resume:
      "Tôle protégée par un revêtement de zinc appliqué en continu : elle part dehors sans peinture ni traitement complémentaire.",
    specs: [
      { label: "Épaisseur", valeur: `${nb(e, e % 1 ? 2 : 0)} mm` },
      { label: "Revêtement", valeur: "Z275 — 275 g/m² de zinc" },
      { label: "Nuance", valeur: "DX51D — EN 10346" },
      { label: "Formats", valeur: "2000 × 1000 · 2500 × 1250 mm" },
      { label: "Découpe", valeur: "Cisaillage aux cotes" },
    ],
    usages: ["Extérieur", "Bardage", "Habillage", "Gouttière"],
  });
});

const tolesSpeciales: Ref[] = [
  mk({
    famille: "toles", ref: "tole-nervuree-bac-acier", nom: "Tôle nervurée — bac acier",
    dims: "profil 27/200 · 35/207", serie: "Tôle nervurée", matiere: "galvanise",
    kg: 5.9, unitePoids: "kg/m²", unite: "au m²", uniteCourte: "€/m²", prix: 14.71,
    resume: "Bac acier de toiture et de bardage : grande portée entre pannes, pose rapide par recouvrement, galvanisé ou prélaqué à la teinte.",
    specs: [
      { label: "Profils", valeur: "27/200 · 35/207 · 39/333" },
      { label: "Finitions", valeur: "Galvanisé Z275 ou prélaqué RAL" },
      { label: "Longueurs", valeur: "Sur mesure, à la coupe" },
      { label: "Recouvrement", valeur: "1 nervure latérale" },
    ],
    usages: ["Toiture", "Bardage", "Abri", "Hangar"],
  }),
  mk({
    famille: "toles", ref: "tole-ondulee", nom: "Tôle ondulée",
    dims: "onde 76/18", serie: "Tôle nervurée", matiere: "galvanise",
    kg: 5.2, unitePoids: "kg/m²", unite: "au m²", uniteCourte: "€/m²", prix: 13.4,
    resume: "L'onde sinusoïdale classique : couverture d'abri, de préau et de bâtiment agricole. Plus souple à cintrer qu'un bac nervuré.",
    specs: [
      { label: "Profil", valeur: "Onde 76/18" },
      { label: "Finition", valeur: "Galvanisé Z275" },
      { label: "Longueurs", valeur: "Sur mesure, à la coupe" },
      { label: "Cintrage", valeur: "Possible dans le sens de l'onde" },
    ],
    usages: ["Abri", "Préau", "Agricole", "Couverture"],
  }),
  mk({
    famille: "toles", ref: "tole-perforee-r5t8", nom: "Tôle perforée R5 T8",
    dims: "trous Ø5 — entraxe 8 mm", serie: "Tôle perforée",
    kg: 9.4, unitePoids: "kg/m²", unite: "au m²", uniteCourte: "€/m²", prix: 46.0,
    resume: "Perforation ronde en quinconce, 35 % de vide : ventilation, brise-vue, habillage de façade, protection de machine.",
    specs: [
      { label: "Perforation", valeur: "Ronde Ø 5 mm" },
      { label: "Entraxe", valeur: "8 mm, quinconce 60°" },
      { label: "Taux de vide", valeur: "35 %" },
      { label: "Épaisseur", valeur: "1,5 mm" },
      { label: "Formats", valeur: "2000 × 1000 mm" },
    ],
    usages: ["Ventilation", "Brise-vue", "Façade", "Protection"],
  }),
  mk({
    famille: "toles", ref: "tole-perforee-r10t15", nom: "Tôle perforée R10 T15",
    dims: "trous Ø10 — entraxe 15 mm", serie: "Tôle perforée",
    kg: 9.0, unitePoids: "kg/m²", unite: "au m²", uniteCourte: "€/m²", prix: 44.0,
    resume: "Perforation large : le maximum de passage d'air et de lumière pour un habillage qui reste structurel.",
    specs: [
      { label: "Perforation", valeur: "Ronde Ø 10 mm" },
      { label: "Entraxe", valeur: "15 mm, quinconce 60°" },
      { label: "Taux de vide", valeur: "40 %" },
      { label: "Épaisseur", valeur: "1,5 mm" },
      { label: "Formats", valeur: "2000 × 1000 mm" },
    ],
    usages: ["Ventilation", "Claustra", "Garde-corps", "Décor"],
  }),
  mk({
    famille: "toles", ref: "tole-striee-larme-fine", nom: "Tôle striée à larme fine",
    dims: "3 mm — stries parallèles", serie: "Tôle larmée",
    kg: 24.5, unitePoids: "kg/m²", unite: "au m²", uniteCourte: "€/m²",
    resume: "Stries parallèles plutôt qu'un damier : l'adhérence se fait dans un seul sens, idéal pour les rampes et les plans inclinés.",
    specs: [
      { label: "Épaisseur de base", valeur: "3 mm" },
      { label: "Motif", valeur: "Stries parallèles" },
      { label: "Nuance", valeur: "S235JR" },
      { label: "Formats", valeur: "2000 × 1000 mm" },
    ],
    usages: ["Rampe", "Plan incliné", "Marche", "Remorque"],
  }),
  mk({
    famille: "toles", ref: "tole-prelaquee-ral", nom: "Tôle prélaquée RAL",
    dims: "0,63 mm — teinte au choix", serie: "Tôle galvanisée", matiere: "galvanise",
    kg: 5.0, unitePoids: "kg/m²", unite: "au m²", uniteCourte: "€/m²", prix: 19.8,
    resume: "Galvanisée puis laquée en continu à la teinte RAL : la finition posée telle quelle, sans peinture de chantier.",
    specs: [
      { label: "Épaisseur", valeur: "0,63 mm" },
      { label: "Laquage", valeur: "25 µm polyester, face extérieure" },
      { label: "Teintes", valeur: "RAL standard — nous consulter" },
      { label: "Support", valeur: "Acier galvanisé Z275" },
    ],
    usages: ["Bardage", "Habillage", "Couverture", "Finition"],
  }),
];

/* ------------------------------------------------------------------ */
/*  6 · TREILLIS & ARMATURES                                           */
/* ------------------------------------------------------------------ */

const treillisRefs: Ref[] = [
  ...[
    ["st-25c", "Treillis soudé ST 25 C", "Ø 6 — maille 150 × 150", 3.02, "Le treillis d'armature courant des dalles de garage, terrasses et chapes fibrées."],
    ["st-30", "Treillis soudé ST 30", "Ø 6 — maille 100 × 200", 3.83, "Maille resserrée dans un sens : les dalles portant principalement dans une direction."],
    ["st-50", "Treillis soudé ST 50", "Ø 8 — maille 150 × 150", 5.37, "Section renforcée pour les dalles circulées et les planchers portés."],
    ["panneau-6x2-4", "Panneau treillis 6 × 2,4 m", "format standard chantier", 3.02, "Le panneau entier livré au format de chantier, sans recoupe ni perte."],
  ].map(([ref, nom, dims, kg, resume]) =>
    mk({
      famille: "treillis", ref: ref as string, nom: nom as string, dims: dims as string,
      serie: "Treillis soudé", kg: kg as number, unitePoids: "kg/m²",
      unite: "au m²", uniteCourte: "€/m²",
      resume: resume as string,
      specs: [
        { label: "Fil", valeur: (dims as string).split(" — ")[0] },
        { label: "Maille", valeur: (dims as string).split(" — ")[1] ?? "150 × 150 mm" },
        { label: "Nuance", valeur: "B500A — acier pour béton armé" },
        { label: "Panneau standard", valeur: "6000 × 2400 mm" },
      ],
      usages: ["Dalle", "Chape", "Terrasse", "Béton armé"],
    })
  ),
  ...[6, 8, 10, 12, 14, 16, 20].map((d) => {
    const kg = +(d * d * 0.00617).toFixed(2);
    return mk({
      famille: "treillis", ref: `rond-beton-${d}`, nom: `Rond à béton Ø ${d}`,
      dims: `Ø ${d} mm — haute adhérence`, serie: "Rond à béton", kg,
      resume: "Barre crénelée à haute adhérence : l'armature des poutres, poteaux et chaînages coulés en place.",
      specs: [
        { label: "Diamètre", valeur: `${d} mm` },
        { label: "Nuance", valeur: "B500B — haute adhérence" },
        { label: "Surface", valeur: "Crénelée" },
        { label: "Longueur", valeur: "6 m ou 12 m — coupe et façonnage" },
      ],
      usages: ["Poutre", "Poteau", "Chaînage", "Fondation"],
    });
  }),
  mk({
    famille: "treillis", ref: "fil-recuit-1-2", nom: "Fil recuit Ø 1,2",
    dims: "bobine 5 kg", serie: "Accessoire", kg: 5, unitePoids: "kg/bobine",
    unite: "à la bobine", uniteCourte: "€/bobine", prix: 12.5,
    resume: "Le fil noir qui ligature les armatures entre elles. Recuit, donc souple : il se noue à la main ou à la pince.",
    specs: [
      { label: "Diamètre", valeur: "1,2 mm" },
      { label: "État", valeur: "Recuit (noir)" },
      { label: "Conditionnement", valeur: "Bobine de 5 kg" },
    ],
    usages: ["Ligature", "Armature", "Attache"],
  }),
];

/* ------------------------------------------------------------------ */
/*  7 · CORTEN                                                         */
/* ------------------------------------------------------------------ */

const cortenRefs: Ref[] = [
  ...[2, 3, 4, 5].map((e) => {
    const kg = +(e * 7.85).toFixed(2);
    return mk({
      famille: "corten", ref: `tole-corten-${e}mm`, nom: `Tôle corten ${e} mm`,
      dims: `épaisseur ${e} mm`, serie: "Tôle corten", matiere: "corten", kg,
      unitePoids: "kg/m²", unite: "au m²", uniteCourte: "€/m²",
      resume: "L'acier qui se protège en rouillant. La patine se stabilise en 6 à 18 mois selon l'exposition, puis fait barrière — aucun entretien ensuite.",
      specs: [
        { label: "Épaisseur", valeur: `${e} mm` },
        { label: "Nuance", valeur: "S355J0WP — EN 10025-5" },
        { label: "Patine", valeur: "Stabilisée en 6 à 18 mois" },
        { label: "Formats", valeur: "2000 × 1000 · 3000 × 1500 mm" },
        { label: "Entretien", valeur: "Aucun" },
      ],
      usages: ["Bardage", "Déco jardin", "Habillage", "Signalétique"],
    });
  }),
  mk({
    famille: "corten", ref: "bordure-jardin-corten", nom: "Bordure de jardin corten",
    dims: "h 150 mm × L 2000 mm", serie: "Aménagement", matiere: "corten",
    kg: 4.7, unitePoids: "kg/pce", unite: "à l'unité", uniteCourte: "€/pce", prix: 38.0,
    resume: "Sépare la pelouse du massif d'un trait net qui rouille avec le jardin. Livrée avec les piquets d'ancrage.",
    specs: [
      { label: "Hauteur", valeur: "150 mm" },
      { label: "Longueur", valeur: "2000 mm" },
      { label: "Épaisseur", valeur: "2 mm" },
      { label: "Fourni avec", valeur: "3 piquets d'ancrage" },
      { label: "Hauteurs disponibles", valeur: "100 · 150 · 200 · 300 mm" },
    ],
    usages: ["Massif", "Allée", "Potager", "Pelouse"],
  }),
  mk({
    famille: "corten", ref: "bac-a-fleurs-corten", nom: "Bac à fleurs corten",
    dims: "800 × 400 × 400 mm", serie: "Aménagement", matiere: "corten",
    kg: 28, unitePoids: "kg/pce", unite: "à l'unité", uniteCourte: "€/pce", prix: 290.0,
    resume: "Bac soudé d'un seul tenant, fond percé pour le drainage. Sur mesure aux dimensions de votre terrasse.",
    specs: [
      { label: "Dimensions", valeur: "800 × 400 × 400 mm" },
      { label: "Épaisseur", valeur: "2 mm" },
      { label: "Fond", valeur: "Percé, drainage" },
      { label: "Sur mesure", valeur: "Toutes dimensions — sur plan" },
    ],
    usages: ["Terrasse", "Jardin", "Balcon", "Aménagement"],
  }),
  mk({
    famille: "corten", ref: "brise-vue-corten", nom: "Panneau brise-vue corten",
    dims: "1800 × 900 mm — découpe laser", serie: "Aménagement", matiere: "corten",
    kg: 25, unitePoids: "kg/pce", unite: "à l'unité", uniteCourte: "€/pce", prix: 340.0,
    resume: "Panneau ajouré au laser selon le motif de votre choix : il masque sans cloisonner, et la lumière dessine le motif au sol.",
    specs: [
      { label: "Dimensions", valeur: "1800 × 900 mm" },
      { label: "Épaisseur", valeur: "2 mm" },
      { label: "Découpe", valeur: "Laser, motif au choix" },
      { label: "Fixation", valeur: "Poteaux ou platines" },
    ],
    usages: ["Terrasse", "Clôture", "Séparation", "Décor"],
  }),
  mk({
    famille: "corten", ref: "bardage-corten", nom: "Bardage corten à clins",
    dims: "lames 200 mm — longueur libre", serie: "Bardage", matiere: "corten",
    kg: 15.7, unitePoids: "kg/m²", unite: "au m²", uniteCourte: "€/m²",
    resume: "Lames pliées à recouvrement pour l'habillage de façade. La patine uniformise les teintes en une saison.",
    specs: [
      { label: "Largeur utile", valeur: "200 mm" },
      { label: "Épaisseur", valeur: "2 mm" },
      { label: "Longueur", valeur: "Sur mesure jusqu'à 3 m" },
      { label: "Pose", valeur: "Clins à recouvrement sur tasseaux" },
    ],
    usages: ["Façade", "Extension", "Abri", "Habillage"],
  }),
];

/* ------------------------------------------------------------------ */
/*  8 · POTEAUX & CLÔTURE                                              */
/* ------------------------------------------------------------------ */

const poteauxRefs: Ref[] = [
  ...([[48, 1500], [48, 1750], [48, 2000], [48, 2500]] as [number, number][]).map(
    ([d, l]) => {
      const kg = +(((d - 2) * 2 * 0.02466 * l) / 1000).toFixed(2);
      return mk({
        famille: "poteaux-cloture", ref: `poteau-rond-${d}x${l}`,
        nom: `Poteau rond Ø ${d} — ${l} mm`, dims: `Ø ${d} mm × ${l} mm`,
        serie: "Poteau rond", matiere: "galvanise", kg, unitePoids: "kg/pce",
        unite: "à l'unité", uniteCourte: "€/pce",
        prix: arrondi(Math.max(14, kg * 3.2)),
        resume: `Poteau galvanisé pour grillage souple ou panneau rigide. Hauteur libre ${((l - 300) / 1000)
          .toFixed(2)
          .replace(".", ",")} m après scellement de 30 cm.`,
        specs: [
          { label: "Diamètre", valeur: `${d} mm` },
          { label: "Longueur totale", valeur: `${l} mm` },
          { label: "Épaisseur", valeur: "2 mm" },
          { label: "Protection", valeur: "Galvanisé à chaud" },
          { label: "Pose", valeur: "Scellement béton ou platine" },
        ],
        usages: ["Clôture", "Grillage", "Panneau rigide"],
      });
    }
  ),
  ...([[40, 1500], [40, 2000], [60, 2000]] as [number, number][]).map(([a, l]) => {
    const kg = +((4 * (a - 2) * 2 * 0.00785 * l) / 1000).toFixed(2);
    return mk({
      famille: "poteaux-cloture", ref: `poteau-carre-${a}x${l}`,
      nom: `Poteau carré ${a} × ${a} — ${l} mm`, dims: `${a} × ${a} mm × ${l} mm`,
      serie: "Poteau carré", matiere: "galvanise", kg, unitePoids: "kg/pce",
      unite: "à l'unité", uniteCourte: "€/pce",
      prix: arrondi(Math.max(16, kg * 3.4)),
      resume: "Section carrée : les panneaux rigides se clipsent à plat sans collier, et l'alignement se règle à l'œil.",
      specs: [
        { label: "Section", valeur: `${a} × ${a} mm` },
        { label: "Longueur totale", valeur: `${l} mm` },
        { label: "Épaisseur", valeur: "2 mm" },
        { label: "Protection", valeur: "Galvanisé à chaud" },
        { label: "Pose", valeur: "Scellement ou platine boulonnée" },
      ],
      usages: ["Panneau rigide", "Clôture", "Portillon"],
    });
  }),
  mk({
    famille: "poteaux-cloture", ref: "platine-poteau-100x100",
    nom: "Platine de poteau 100 × 100", dims: "100 × 100 × 6 mm — 4 trous Ø 12",
    serie: "Accessoire", kg: 0.47, unitePoids: "kg/pce", unite: "à l'unité",
    uniteCourte: "€/pce", prix: 6.5,
    resume: "Se soude en pied de poteau pour boulonner sur une dalle existante — pas de scellement, pas de béton à couler.",
    specs: [
      { label: "Dimensions", valeur: "100 × 100 mm" },
      { label: "Épaisseur", valeur: "6 mm" },
      { label: "Perçage", valeur: "4 trous Ø 12 mm" },
      { label: "Finition", valeur: "Brut ou galvanisé" },
    ],
    usages: ["Fixation sur dalle", "Poteau", "Garde-corps"],
  }),
  mk({
    famille: "poteaux-cloture", ref: "capuchon-poteau-48",
    nom: "Capuchon de poteau Ø 48", dims: "Ø 48 mm — PVC noir", serie: "Accessoire",
    kg: 0.02, unitePoids: "kg/pce", unite: "à l'unité", uniteCourte: "€/pce", prix: 1.2,
    resume: "Bouche le haut du poteau : l'eau n'entre pas, le poteau ne rouille pas de l'intérieur.",
    specs: [
      { label: "Diamètre", valeur: "48 mm" },
      { label: "Matière", valeur: "PVC noir" },
      { label: "Pose", valeur: "Emboîtement à force" },
    ],
    usages: ["Finition", "Étanchéité", "Clôture"],
  }),
  mk({
    famille: "poteaux-cloture", ref: "jambe-de-force-48",
    nom: "Jambe de force Ø 48", dims: "Ø 48 × 1500 mm", serie: "Accessoire",
    matiere: "galvanise", kg: 3.4, unitePoids: "kg/pce", unite: "à l'unité",
    uniteCourte: "€/pce", prix: 16.5,
    resume: "Contrevente le poteau d'angle et le poteau de départ : sans elle, la tension du grillage finit par coucher la ligne.",
    specs: [
      { label: "Diamètre", valeur: "48 mm" },
      { label: "Longueur", valeur: "1500 mm" },
      { label: "Protection", valeur: "Galvanisé à chaud" },
      { label: "Fourni avec", valeur: "Collier de liaison" },
    ],
    usages: ["Angle", "Départ", "Contreventement"],
  }),
  mk({
    famille: "poteaux-cloture", ref: "collier-fixation-48",
    nom: "Collier de fixation Ø 48", dims: "Ø 48 mm — galvanisé", serie: "Accessoire",
    matiere: "galvanise", kg: 0.09, unitePoids: "kg/pce", unite: "à l'unité",
    uniteCourte: "€/pce", prix: 1.9,
    resume: "Serre le fil de tension ou le panneau contre le poteau. Vendu à l'unité, boulon inclus.",
    specs: [
      { label: "Diamètre", valeur: "48 mm" },
      { label: "Protection", valeur: "Galvanisé" },
      { label: "Fourni avec", valeur: "Boulon M8" },
    ],
    usages: ["Grillage", "Panneau", "Fil de tension"],
  }),
];

/* ------------------------------------------------------------------ */
/*  9 · VISSERIE & FIXATION                                            */
/* ------------------------------------------------------------------ */

const AUTOFORANTES: [number, number, string, number][] = [
  [4.8, 20, "Hexagonale 8", 9.9], [4.8, 35, "Hexagonale 8", 11.5],
  [5.5, 25, "Hexagonale 8", 11.9], [5.5, 50, "Hexagonale 8", 14.9],
  [6.3, 60, "Hexagonale 10", 19.9], [6.3, 80, "Hexagonale 10", 23.5],
  [6.3, 100, "Hexagonale 10", 27.9],
];

const BOULONS: [number, number, number][] = [
  [8, 40, 0.38], [8, 60, 0.45], [10, 50, 0.62], [10, 80, 0.78], [12, 60, 0.95],
  [12, 100, 1.25],
];

const visserieRefs: Ref[] = [
  ...AUTOFORANTES.map(([d, l, tete, prix]) =>
    mk({
      famille: "visserie",
      ref: `vis-autoforante-${String(d).replace(".", "-")}x${l}-hex-${tete.split(" ")[1]}`,
      nom: `Vis autoforante ${nb(d, 1)} × ${l} — tête ${tete.toLowerCase()}`,
      dims: `${nb(d, 1)} × ${l} mm`, serie: "Vis autoforante", matiere: "galvanise",
      // masse d'une boîte de 100 : volume du fût × 7,85, majoré de 15 % (tête + filet)
      kg: +(((d * d * l * 0.7854 * 7.85 * 1.15) / 1e6) * 100).toFixed(2),
      unitePoids: "kg/boîte",
      unite: "à la boîte de 100", uniteCourte: "€/boîte", prix,
      resume:
        "Perce et fixe en une seule opération, sans avant-trou. Pointe autoforante, rondelle d'étanchéité EPDM intégrée.",
      specs: [
        { label: "Diamètre", valeur: `${nb(d, 1)} mm` },
        { label: "Longueur", valeur: `${l} mm` },
        { label: "Tête", valeur: `${tete} mm` },
        { label: "Pointe", valeur: "Autoforante, sans avant-trou" },
        { label: "Étanchéité", valeur: "Rondelle EPDM intégrée" },
        { label: "Protection", valeur: "Zinguée blanc" },
        { label: "Conditionnement", valeur: "Boîte de 100" },
      ],
      usages: ["Bac acier", "Bardage", "Ossature métallique", "Couverture"],
    })
  ),
  ...BOULONS.map(([d, l, prix]) =>
    mk({
      famille: "visserie", ref: `boulon-hm-${d}x${l}`,
      nom: `Boulon HM ${d} × ${l}`, dims: `M${d} × ${l} mm`, serie: "Boulonnerie",
      matiere: "galvanise",
      // fût + tête hexagonale + écrou + rondelle ≈ 1,4 × le volume du fût
      kg: +((d * d * l * 0.7854 * 7.85 * 1.4) / 1e6).toFixed(3),
      unitePoids: "kg/pce",
      unite: "à l'unité", uniteCourte: "€/pce", prix,
      resume:
        "Boulon à tête hexagonale classe 8.8 : l'assemblage démontable de la construction métallique. Écrou et rondelle vendus avec.",
      specs: [
        { label: "Filetage", valeur: `M${d}` },
        { label: "Longueur", valeur: `${l} mm` },
        { label: "Classe", valeur: "8.8 — haute résistance" },
        { label: "Protection", valeur: "Zingué" },
        { label: "Fourni avec", valeur: "Écrou + rondelle plate" },
      ],
      usages: ["Assemblage", "Platine", "Charpente", "Démontable"],
    })
  ),
  mk({
    famille: "visserie", ref: "tire-fond-8x80", nom: "Tire-fond 8 × 80",
    dims: "Ø 8 × 80 mm", serie: "Boulonnerie", kg: 0.03, unitePoids: "kg/pce",
    unite: "à l'unité", uniteCourte: "€/pce", prix: 0.55,
    resume: "Vis à bois de forte section pour fixer le métal sur une charpente bois : pannes, tasseaux, ossature.",
    specs: [
      { label: "Diamètre", valeur: "8 mm" },
      { label: "Longueur", valeur: "80 mm" },
      { label: "Tête", valeur: "Hexagonale 13" },
      { label: "Protection", valeur: "Zinguée" },
    ],
    usages: ["Charpente bois", "Panne", "Ossature mixte"],
  }),
  mk({
    famille: "visserie", ref: "cheville-metallique-m10",
    nom: "Cheville métallique M10", dims: "M10 × 90 mm", serie: "Ancrage",
    kg: 0.06, unitePoids: "kg/pce", unite: "à l'unité", uniteCourte: "€/pce", prix: 1.85,
    resume: "Ancrage à expansion pour béton : c'est ce qui tient une platine de poteau ou un garde-corps sur une dalle.",
    specs: [
      { label: "Filetage", valeur: "M10" },
      { label: "Longueur", valeur: "90 mm" },
      { label: "Support", valeur: "Béton non fissuré" },
      { label: "Perçage", valeur: "Ø 10 mm, profondeur 80 mm" },
    ],
    usages: ["Platine", "Garde-corps", "Dalle béton", "Ancrage"],
  }),
  mk({
    famille: "visserie", ref: "rondelle-etancheite-16",
    nom: "Rondelle d'étanchéité Ø 16", dims: "Ø 16 mm — EPDM", serie: "Accessoire",
    kg: 0.003, unitePoids: "kg/pce", unite: "au sachet de 100", uniteCourte: "€/sachet",
    prix: 7.9,
    resume: "Rondelle métal + joint EPDM : elle ferme le trou de vis sur une couverture. Sans elle, chaque vis est une fuite.",
    specs: [
      { label: "Diamètre", valeur: "16 mm" },
      { label: "Joint", valeur: "EPDM vulcanisé" },
      { label: "Support", valeur: "Inox ou zingué" },
      { label: "Conditionnement", valeur: "Sachet de 100" },
    ],
    usages: ["Couverture", "Bac acier", "Étanchéité"],
  }),
  mk({
    famille: "visserie", ref: "electrode-rutile-2-5",
    nom: "Électrode rutile Ø 2,5", dims: "Ø 2,5 × 350 mm — étui 2,5 kg",
    serie: "Soudage", kg: 2.5, unitePoids: "kg/étui", unite: "à l'étui",
    uniteCourte: "€/étui", prix: 14.5,
    resume: "L'électrode enrobée passe-partout pour l'acier doux : amorçage facile, laitier qui se détache seul. Le consommable du soudeur occasionnel.",
    specs: [
      { label: "Diamètre", valeur: "2,5 mm" },
      { label: "Longueur", valeur: "350 mm" },
      { label: "Enrobage", valeur: "Rutile" },
      { label: "Intensité", valeur: "60 à 90 A" },
      { label: "Conditionnement", valeur: "Étui de 2,5 kg" },
    ],
    usages: ["Soudage", "Acier doux", "Réparation"],
  }),
];

/* ------------------------------------------------------------------ */
/*  10 · INOX                                                          */
/* ------------------------------------------------------------------ */

const inoxRefs: Ref[] = [
  ...([[33.7, 2], [42.4, 2], [48.3, 2]] as [number, number][]).map(([d, e]) => {
    const kg = +((d - e) * e * 0.02513).toFixed(2);
    return mk({
      famille: "inox", ref: `tube-rond-inox-${String(d).replace(".", "-")}x${e}`,
      nom: `Tube rond inox Ø ${nb(d, 1)} × ${e}`, dims: `Ø ${nb(d, 1)} × ${e} mm`,
      serie: "Tube inox", matiere: "inox", kg,
      resume: "Tube inox 304 brossé grain 240 : la main courante qui ne rouille pas et ne se repeint jamais.",
      specs: [
        { label: "Diamètre extérieur", valeur: `${nb(d, 1)} mm` },
        { label: "Épaisseur", valeur: `${e} mm` },
        { label: "Nuance", valeur: "304 (1.4301)" },
        { label: "Finition", valeur: "Brossé grain 240" },
        LONG_STD,
      ],
      usages: ["Main courante", "Garde-corps", "Mobilier", "Extérieur"],
    });
  }),
  mk({
    famille: "inox", ref: "tube-carre-inox-40x40x2", nom: "Tube carré inox 40 × 40 × 2",
    dims: "40 × 40 × 2 mm", serie: "Tube inox", matiere: "inox", kg: 2.36,
    resume: "Ossature inox pour les ouvrages exposés en permanence : abords de piscine, bord de mer, agroalimentaire.",
    specs: [
      { label: "Section", valeur: "40 × 40 mm" },
      { label: "Épaisseur", valeur: "2 mm" },
      { label: "Nuance", valeur: "304 (1.4301)" },
      { label: "Finition", valeur: "Brossé grain 240" },
      LONG_STD,
    ],
    usages: ["Ossature", "Piscine", "Agroalimentaire", "Extérieur"],
  }),
  ...([[30, 3], [40, 5], [50, 5]] as [number, number][]).map(([l, e]) => {
    const kg = +((l * e * 8.0) / 1000).toFixed(2);
    return mk({
      famille: "inox", ref: `plat-inox-${l}x${e}`, nom: `Plat inox ${l} × ${e}`,
      dims: `${l} × ${e} mm`, serie: "Plat inox", matiere: "inox", kg,
      resume: "Fer plat inox pour la ferronnerie exposée : fixations, brides, pièces de liaison qui restent brillantes.",
      specs: [
        { label: "Largeur", valeur: `${l} mm` },
        { label: "Épaisseur", valeur: `${e} mm` },
        { label: "Nuance", valeur: "304 (1.4301)" },
        { label: "Finition", valeur: "Brut ou brossé" },
        LONG_STD,
      ],
      usages: ["Ferronnerie", "Bride", "Liaison", "Extérieur"],
    });
  }),
  ...([[40, 4], [50, 5]] as [number, number][]).map(([a, e]) => {
    const kg = +(((2 * a - e) * e * 8.0) / 1000).toFixed(2);
    return mk({
      famille: "inox", ref: `corniere-inox-${a}x${a}x${e}`,
      nom: `Cornière inox ${a} × ${a} × ${e}`, dims: `${a} × ${a} × ${e} mm`,
      serie: "Cornière inox", matiere: "inox", kg,
      resume: "Angle inox pour les cadres et les protections d'arête en milieu humide ou alimentaire.",
      specs: [
        { label: "Ailes", valeur: `${a} × ${a} mm` },
        { label: "Épaisseur", valeur: `${e} mm` },
        { label: "Nuance", valeur: "304 (1.4301)" },
        LONG_STD,
      ],
      usages: ["Cadre", "Protection d'arête", "Agroalimentaire"],
    });
  }),
  ...[1.5, 2, 3].map((e) => {
    const kg = +(e * 8.0).toFixed(2);
    return mk({
      famille: "inox", ref: `tole-inox-${String(e).replace(".", "-")}mm`,
      nom: `Tôle inox ${nb(e, e % 1 ? 1 : 0)} mm`,
      dims: `épaisseur ${nb(e, e % 1 ? 1 : 0)} mm`, serie: "Tôle inox", matiere: "inox",
      kg, unitePoids: "kg/m²", unite: "au m²", uniteCourte: "€/m²",
      resume: "Tôle inox brossée : plan de travail, crédence, habillage de cuisine professionnelle, plaque de propreté.",
      specs: [
        { label: "Épaisseur", valeur: `${nb(e, e % 1 ? 1 : 0)} mm` },
        { label: "Nuance", valeur: "304 (1.4301)" },
        { label: "Finition", valeur: "Brossé grain 240, film de protection" },
        { label: "Formats", valeur: "2000 × 1000 · 2500 × 1250 mm" },
      ],
      usages: ["Crédence", "Plan de travail", "Habillage", "Cuisine pro"],
    });
  }),
  ...[12, 16, 20].map((d) => {
    const kg = +(d * d * 0.00629).toFixed(2);
    return mk({
      famille: "inox", ref: `rond-inox-${d}`, nom: `Rond plein inox Ø ${d}`,
      dims: `Ø ${d} mm`, serie: "Rond inox", matiere: "inox", kg,
      resume: "Barre ronde inox : barreaudage de garde-corps, axes, tiges filetables qui ne grippent pas.",
      specs: [
        { label: "Diamètre", valeur: `${d} mm` },
        { label: "Nuance", valeur: "304 (1.4301)" },
        { label: "Finition", valeur: "Brossé" },
        LONG_STD,
      ],
      usages: ["Barreaudage", "Axe", "Garde-corps"],
    });
  }),
  mk({
    famille: "inox", ref: "tole-inox-316l-2mm", nom: "Tôle inox 316L 2 mm",
    dims: "épaisseur 2 mm — qualité marine", serie: "Tôle inox", matiere: "inox",
    kg: 16.0, unitePoids: "kg/m²", unite: "au m²", uniteCourte: "€/m²",
    prix: arrondi(16.0 * 7.4),
    resume: "Le 316L contient du molybdène : c'est la nuance qui tient en bord de mer, en piscine et au contact des chlorures.",
    specs: [
      { label: "Épaisseur", valeur: "2 mm" },
      { label: "Nuance", valeur: "316L (1.4404)" },
      { label: "Particularité", valeur: "Allié molybdène — milieu chloré" },
      { label: "Formats", valeur: "2000 × 1000 mm" },
    ],
    usages: ["Bord de mer", "Piscine", "Chimie", "Agroalimentaire"],
  }),
];

/* ------------------------------------------------------------------ */
/*  11 · ALUMINIUM                                                     */
/* ------------------------------------------------------------------ */

const aluRefs: Ref[] = [
  ...([[20, 2], [30, 3], [40, 4], [50, 5]] as [number, number][]).map(([a, e]) => {
    const kg = +(((2 * a - e) * e * 2.7) / 1000).toFixed(2);
    return mk({
      famille: "aluminium", ref: `corniere-alu-${a}x${a}x${e}`,
      nom: `Cornière alu ${a} × ${a} × ${e}`, dims: `${a} × ${a} × ${e} mm`,
      serie: "Profilé alu", matiere: "aluminium", kg,
      resume: "Angle aluminium : protection d'arête, encadrement, finition. Se coupe à la scie à métaux et ne rouille jamais.",
      specs: [
        { label: "Ailes", valeur: `${a} × ${a} mm` },
        { label: "Épaisseur", valeur: `${e} mm` },
        { label: "Alliage", valeur: "6060 T66" },
        { label: "Finition", valeur: "Brut — anodisable" },
        { label: "Longueur standard", valeur: "6 m — découpe aux cotes" },
      ],
      usages: ["Protection d'arête", "Encadrement", "Finition"],
    });
  }),
  ...([[30, 3], [40, 5]] as [number, number][]).map(([l, e]) => {
    const kg = +((l * e * 2.7) / 1000).toFixed(2);
    return mk({
      famille: "aluminium", ref: `plat-alu-${l}x${e}`, nom: `Plat alu ${l} × ${e}`,
      dims: `${l} × ${e} mm`, serie: "Profilé alu", matiere: "aluminium", kg,
      resume: "Fer plat aluminium : signalétique, supports légers, pièces à percer et visser sans soudure.",
      specs: [
        { label: "Largeur", valeur: `${l} mm` },
        { label: "Épaisseur", valeur: `${e} mm` },
        { label: "Alliage", valeur: "6060 T66" },
        { label: "Longueur standard", valeur: "6 m — découpe aux cotes" },
      ],
      usages: ["Signalétique", "Support", "Habillage"],
    });
  }),
  ...([[30, 2], [40, 2], [50, 3]] as [number, number][]).map(([a, e]) => {
    const kg = +(4 * (a - e) * e * 0.0027).toFixed(2);
    return mk({
      famille: "aluminium", ref: `tube-carre-alu-${a}x${a}x${e}`,
      nom: `Tube carré alu ${a} × ${a} × ${e}`, dims: `${a} × ${a} × ${e} mm`,
      serie: "Tube alu", matiere: "aluminium", kg,
      resume: "Ossature légère : trois fois plus léger que l'acier à section égale, pour les structures qu'on déplace ou qu'on porte.",
      specs: [
        { label: "Section", valeur: `${a} × ${a} mm` },
        { label: "Épaisseur", valeur: `${e} mm` },
        { label: "Alliage", valeur: "6060 T66" },
        { label: "Longueur standard", valeur: "6 m — découpe aux cotes" },
      ],
      usages: ["Structure légère", "Mobilier", "Stand", "Menuiserie"],
    });
  }),
  ...([[30, 2], [40, 2]] as [number, number][]).map(([d, e]) => {
    const kg = +((d - e) * e * 0.00848).toFixed(2);
    return mk({
      famille: "aluminium", ref: `tube-rond-alu-${d}x${e}`,
      nom: `Tube rond alu Ø ${d} × ${e}`, dims: `Ø ${d} × ${e} mm`,
      serie: "Tube alu", matiere: "aluminium", kg,
      resume: "Tube rond aluminium pour mains courantes légères, mâts, supports et mobilier d'extérieur.",
      specs: [
        { label: "Diamètre extérieur", valeur: `${d} mm` },
        { label: "Épaisseur", valeur: `${e} mm` },
        { label: "Alliage", valeur: "6060 T66" },
        { label: "Longueur standard", valeur: "6 m — découpe aux cotes" },
      ],
      usages: ["Main courante", "Mât", "Mobilier"],
    });
  }),
  ...[1, 2, 3].map((e) => {
    const kg = +(e * 2.7).toFixed(2);
    return mk({
      famille: "aluminium", ref: `tole-alu-${e}mm`, nom: `Tôle alu ${e} mm`,
      dims: `épaisseur ${e} mm`, serie: "Tôle alu", matiere: "aluminium", kg,
      unitePoids: "kg/m²", unite: "au m²", uniteCourte: "€/m²",
      resume: "Tôle aluminium lisse : habillage, capotage, signalétique. Se plie à froid et se découpe proprement.",
      specs: [
        { label: "Épaisseur", valeur: `${e} mm` },
        { label: "Alliage", valeur: "5754 ou 1050 selon usage" },
        { label: "Formats", valeur: "2000 × 1000 · 2500 × 1250 mm" },
        { label: "Finition", valeur: "Brut — anodisable ou laquable" },
      ],
      usages: ["Habillage", "Capotage", "Signalétique"],
    });
  }),
  mk({
    famille: "aluminium", ref: "tole-alu-larmee-3mm", nom: "Tôle alu larmée 3 mm",
    dims: "3/4,5 mm — motif duett", serie: "Tôle alu", matiere: "aluminium",
    kg: 9.2, unitePoids: "kg/m²", unite: "au m²", uniteCourte: "€/m²",
    resume: "Antidérapante et inoxydable : marchepieds de véhicule, planchers de remorque, seuils exposés.",
    specs: [
      { label: "Épaisseur de base", valeur: "3 mm" },
      { label: "Motif", valeur: "Duett (deux larmes)" },
      { label: "Alliage", valeur: "5754" },
      { label: "Formats", valeur: "2000 × 1000 mm" },
    ],
    usages: ["Marchepied", "Remorque", "Plancher", "Seuil"],
  }),
  mk({
    famille: "aluminium", ref: "profile-u-alu-40x40",
    nom: "Profilé U alu 40 × 40 × 3", dims: "40 × 40 × 3 mm", serie: "Profilé alu",
    matiere: "aluminium", kg: 0.89,
    resume: "Le U aluminium reçoit un panneau, un verre ou une plaque : rail de guidage, encadrement, finition de chant.",
    specs: [
      { label: "Section", valeur: "40 × 40 mm" },
      { label: "Épaisseur", valeur: "3 mm" },
      { label: "Alliage", valeur: "6060 T66" },
      { label: "Longueur standard", valeur: "6 m — découpe aux cotes" },
    ],
    usages: ["Rail", "Encadrement", "Chant", "Panneau"],
  }),
  mk({
    famille: "aluminium", ref: "rond-alu-20", nom: "Rond plein alu Ø 20",
    dims: "Ø 20 mm", serie: "Profilé alu", matiere: "aluminium", kg: 0.85,
    resume: "Barre ronde aluminium pour l'usinage, les entretoises et les pièces tournées légères.",
    specs: [
      { label: "Diamètre", valeur: "20 mm" },
      { label: "Alliage", valeur: "6082 T6 — usinage" },
      { label: "Longueur standard", valeur: "6 m — découpe aux cotes" },
    ],
    usages: ["Usinage", "Entretoise", "Axe léger"],
  }),
];

/* ------------------------------------------------------------------ */
/*  FAMILLES                                                           */
/* ------------------------------------------------------------------ */

export const familles: Famille[] = [
  {
    slug: "poutrelles",
    nom: "Poutrelles & profilés",
    accroche: "IPE, IPN, HEA, HEB, UPN — la structure porteuse",
    intro:
      "Profilés normalisés laminés à chaud, la matière des ossatures. L'IPE porte en flexion sur de longues portées ; les HEA et HEB, plus larges d'aile, reprennent la compression et font les poteaux ; l'UPN se boulonne à plat en rive. Coupés à la longueur, percés et livrés prêts à monter.",
    titreSeo: "Poutrelles IPE, HEA, HEB, UPN — prix au mètre, découpe sur mesure",
    descSeo:
      "62 sections de poutrelles acier en stock : IPE, IPN, HEA, HEB, UPN. Poids, cotes et prix au mètre affichés. Découpe aux cotes, retrait le jour même dans nos 4 dépôts.",
    art: "poutrelles",
    series: ["IPE", "IPN", "HEA", "HEB", "UPN"],
    refs: [
      ...profils("IPE", IPE), ...profils("HEA", HEA), ...profils("HEB", HEB),
      ...profils("IPN", IPN), ...profils("UPN", UPN),
    ],
  },
  {
    slug: "cornieres",
    nom: "Cornières",
    accroche: "L'angle qui raidit tout",
    intro:
      "La cornière laminée à chaud est la pièce de renfort universelle : cadre, support, raidisseur, bordure. Ailes égales pour les cadres symétriques, ailes inégales quand une face porte et l'autre se fixe. C'est la famille la plus demandée du catalogue.",
    titreSeo: "Cornière acier égale et inégale — dès 1,60 €/m, coupée sur mesure",
    descSeo:
      "32 sections de cornières acier laminées à chaud, de 20 × 20 × 3 à 120 × 120 × 12. Prix au mètre, poids, découpe aux cotes exactes. Stock permanent dans nos 4 dépôts.",
    art: "cornieres-plats",
    series: ["Cornière égale", "Cornière inégale"],
    refs: [...cornieresEgales, ...cornieresInegales],
  },
  {
    slug: "plats-barres",
    nom: "Plats & barres",
    accroche: "Le fer de ferronnerie",
    intro:
      "Plats laminés, ronds et carrés pleins : la matière première du ferronnier. Le plat se perce, se cintre et se soude sans préparation ; le rond encaisse la torsion ; le carré fait le barreaudage traditionnel. Toutes les sections se coupent à la demande.",
    titreSeo: "Plat acier, rond et carré plein — dès 1,95 €/m, toutes sections",
    descSeo:
      "68 sections de plats, ronds et carrés pleins en acier S235. Prix au mètre et poids affichés, découpe aux cotes. Portails, grilles, ferronnerie — retrait le jour même.",
    art: "plats",
    series: ["Plat", "Rond plein", "Carré plein"],
    refs: [...plats, ...ronds, ...carres],
  },
  {
    slug: "tubes",
    nom: "Tubes",
    accroche: "L'ossature creuse, légère et rigide",
    intro:
      "À poids égal, le tube est plus rigide que le plein — c'est pourquoi il fait les portails, les garde-corps et les structures de mobilier. Carré pour souder d'équerre sans préparation, rectangulaire pour porter dans un sens, rond pour les mains courantes et le cintrage.",
    titreSeo: "Tube acier carré, rectangulaire et rond — dès 2,20 €/m, sur mesure",
    descSeo:
      "60 sections de tubes acier profilés à froid EN 10219 : carré, rectangulaire, rond. Prix au mètre, poids, découpe aux cotes. Portail, garde-corps, ossature — 4 dépôts.",
    art: "tubes",
    series: ["Tube carré", "Tube rectangulaire", "Tube rond"],
    refs: [...tubesCarres, ...tubesRect, ...tubesRonds],
  },
  {
    slug: "toles",
    nom: "Tôles",
    accroche: "Couvrir, habiller, fermer",
    intro:
      "Lisse pour les platines et les pièces au plan, larmée pour les sols antidérapants, galvanisée pour ce qui part dehors, nervurée pour la toiture et le bardage, perforée pour ventiler ou tamiser. Toutes disponibles au format et débitées aux cotes.",
    titreSeo: "Tôle acier lisse, larmée, galvanisée et nervurée — prix au m²",
    descSeo:
      "34 références de tôles : lisse de 1 à 20 mm, larmée antidérapante, galvanisée Z275, bac acier dès 14,71 €/m², perforée. Découpe aux cotes dans nos 4 dépôts.",
    art: "toles",
    series: ["Tôle lisse", "Tôle larmée", "Tôle galvanisée", "Tôle nervurée", "Tôle perforée"],
    refs: [...tolesLisses, ...tolesLarmees, ...tolesGalva, ...tolesSpeciales],
  },
  {
    slug: "treillis",
    nom: "Treillis & armatures",
    accroche: "Ce qui arme le béton",
    intro:
      "Treillis soudés et aciers à béton pour les dalles, chapes, poutres et chaînages. Panneaux au format chantier, ronds crénelés coupés et façonnés à la demande, plus les accessoires de ligature.",
    titreSeo: "Treillis soudé et rond à béton — panneaux 6 × 2,4 m, coupe et façonnage",
    descSeo:
      "Treillis soudés ST 25 C, ST 30, ST 50 et ronds à béton B500B de Ø 6 à Ø 20. Panneaux au format chantier, coupe et façonnage sur plan. Retrait en dépôt.",
    art: "treillis",
    series: ["Treillis soudé", "Rond à béton", "Accessoire"],
    refs: treillisRefs,
  },
  {
    slug: "corten",
    nom: "Acier corten",
    accroche: "La rouille qui protège",
    intro:
      "Le corten développe une patine dense qui fait barrière et stoppe la corrosion au lieu de l'entretenir. Zéro peinture, zéro entretien, une teinte qui évolue avec les saisons — c'est devenu la matière des jardins contemporains et des façades qui assument leur matière.",
    titreSeo: "Acier corten — tôle, bordure de jardin, bac à fleurs, bardage sur mesure",
    descSeo:
      "Tôle corten de 2 à 5 mm, bordures de jardin, bacs à fleurs, brise-vue découpés au laser et bardage à clins. Patine stabilisée, aucun entretien. Fabrication sur mesure.",
    art: "corten",
    series: ["Tôle corten", "Aménagement", "Bardage"],
    refs: cortenRefs,
  },
  {
    slug: "poteaux-cloture",
    nom: "Poteaux de clôture",
    accroche: "Ce qui tient la clôture debout",
    intro:
      "Poteaux galvanisés prêts à sceller ou à platiner, dimensionnés pour les grillages souples et les panneaux rigides, avec tous les accessoires : jambes de force, colliers, capuchons, platines. Vendus à l'unité, sans lot minimum.",
    titreSeo: "Poteaux de clôture acier galvanisé — ronds, carrés et accessoires",
    descSeo:
      "Poteaux de clôture galvanisés Ø 48 et carrés 40/60, de 1,50 à 2,50 m, plus jambes de force, colliers, capuchons et platines. Vendus à l'unité, retrait en dépôt.",
    art: "poteaux-cloture",
    series: ["Poteau rond", "Poteau carré", "Accessoire"],
    refs: poteauxRefs,
  },
  {
    slug: "visserie",
    nom: "Visserie & fixation",
    accroche: "Ce qui assemble le reste",
    intro:
      "Vis autoforantes pour bac acier, boulonnerie 8.8, ancrages béton, consommables de soudage. Ce sont les pièces qu'on oublie de commander et qui arrêtent un chantier — elles sont en stock permanent.",
    titreSeo: "Vis autoforante, boulon HM et fixation acier — stock permanent",
    descSeo:
      "Vis autoforantes 4,8 à 6,3 mm avec rondelle EPDM, boulonnerie 8.8, chevilles béton, tire-fond et électrodes. Boîtes de 100 ou à l'unité. Retrait le jour même.",
    art: "visserie",
    series: ["Vis autoforante", "Boulonnerie", "Ancrage", "Accessoire", "Soudage"],
    refs: visserieRefs,
  },
  {
    slug: "inox",
    nom: "Inox",
    accroche: "Ce qui reste dehors sans rouiller",
    intro:
      "Tubes, plats, cornières, tôles et ronds en 304 brossé, plus le 316L pour les milieux chlorés. L'inox coûte plus cher au mètre mais ne se repeint jamais : sur la durée de vie d'un garde-corps extérieur, il revient moins cher que l'acier peint.",
    titreSeo: "Inox 304 et 316L — tube, tôle, plat, cornière coupés sur mesure",
    descSeo:
      "Inox 304 brossé grain 240 et 316L qualité marine : tubes ronds et carrés, tôles, plats, cornières, ronds. Prix au mètre, découpe aux cotes. Garde-corps, cuisine pro, bord de mer.",
    art: "tubes",
    series: ["Tube inox", "Plat inox", "Cornière inox", "Tôle inox", "Rond inox"],
    refs: inoxRefs,
  },
  {
    slug: "aluminium",
    nom: "Aluminium",
    accroche: "Trois fois plus léger, jamais de rouille",
    intro:
      "Profilés, tubes et tôles en alliage 6060 et 5754. L'aluminium s'impose dès que le poids compte ou que la structure doit rester nue : il se coupe à la scie à métaux, se perce sans effort et ne demande aucune protection.",
    titreSeo: "Profilé aluminium, tube et tôle alu — coupe sur mesure, dès 5 €/m",
    descSeo:
      "Profilés aluminium 6060 : cornières, plats, U, tubes carrés et ronds, tôles lisses et larmées 5754. Découpe aux cotes, anodisable et laquable. 4 dépôts en Wallonie et France.",
    art: "cornieres-plats",
    series: ["Profilé alu", "Tube alu", "Tôle alu"],
    refs: aluRefs,
  },
];

/* ------------------------------------------------------------------ */
/*  MATIÈRES                                                           */
/* ------------------------------------------------------------------ */

export const matieres: Matiere[] = [
  {
    slug: "acier",
    nom: "Acier",
    accroche: "La matière de structure, brute ou protégée",
    intro:
      "L'acier de construction couvre l'essentiel des besoins : structure, ossature, ferronnerie. Brut à l'intérieur ou sous peinture, galvanisé dès que l'ouvrage est exposé. C'est la matière la plus disponible, la plus facile à souder et la mieux placée en prix.",
    titreSeo: "Acier S235 — poutrelles, tubes, tôles et cornières coupés sur mesure",
    descSeo:
      "Acier de construction S235JR en stock : poutrelles, cornières, plats, tubes, tôles. Prix au mètre affichés, découpe aux cotes, retrait le jour même dans nos 4 dépôts.",
    proprietes: [
      { label: "Nuances courantes", valeur: "S235JR · S275JR · S355JR" },
      { label: "Densité", valeur: "7,85 kg/dm³" },
      { label: "États", valeur: "Brut laminé à chaud, profilé à froid" },
      { label: "Soudabilité", valeur: "Excellente — tous procédés" },
      { label: "Tenue extérieure", valeur: "Peinture ou galvanisation requise" },
    ],
    usages: ["Charpente", "Mezzanine", "Portail", "Garde-corps", "Ferronnerie", "Ossature"],
    familles: ["poutrelles", "cornieres", "plats-barres", "tubes", "toles", "treillis"],
    aRetenir: [
      { titre: "S235, et ça suffit", texte: "Pour 95 % des ouvrages courants, le S235JR est la bonne nuance. Les S275 et S355 ne se justifient que si le calcul de structure l'impose." },
      { titre: "Il rouille — c'est prévu", texte: "L'acier brut s'oxyde en surface dès qu'il est dehors. Peinture antirouille, galvanisation ou changement de matière : le choix se fait avant la commande, pas après." },
      { titre: "Il se soude partout", texte: "C'est son vrai avantage sur l'inox et l'alu : un poste à souder d'entrée de gamme et une électrode rutile suffisent." },
    ],
  },
  {
    slug: "galvanise",
    nom: "Acier galvanisé",
    accroche: "L'acier qui part dehors sans peinture",
    intro:
      "La galvanisation dépose une couche de zinc qui se sacrifie à la place de l'acier. Résultat : 20 à 50 ans de tenue en extérieur, sans peinture, sans reprise. C'est le compromis évident entre l'acier brut et l'inox — et c'est ce qu'on recommande par défaut pour une clôture ou une charpente exposée.",
    titreSeo: "Acier galvanisé — tôle Z275, poteaux et bac acier, tenue 20 ans dehors",
    descSeo:
      "Acier galvanisé à chaud Z275 : tôles de 0,75 à 3 mm, bac acier, tôles prélaquées RAL, poteaux de clôture. Sans peinture, sans entretien. Découpe aux cotes en dépôt.",
    proprietes: [
      { label: "Revêtement", valeur: "Z275 — 275 g/m² de zinc" },
      { label: "Norme", valeur: "EN 10346 (continu) · EN ISO 1461 (bain)" },
      { label: "Durée de vie", valeur: "20 à 50 ans selon l'exposition" },
      { label: "Entretien", valeur: "Aucun" },
      { label: "Soudage", valeur: "Possible — reprise au spray zinc obligatoire" },
    ],
    usages: ["Clôture", "Bardage", "Toiture", "Charpente exposée", "Gouttière"],
    familles: ["toles", "poteaux-cloture", "visserie"],
    aRetenir: [
      { titre: "Le zinc se sacrifie", texte: "Une rayure ne condamne pas la pièce : le zinc voisin protège électrochimiquement l'acier mis à nu sur quelques millimètres." },
      { titre: "Souder détruit la galva", texte: "La chaleur brûle le zinc sur 3 à 5 cm. Toute soudure doit être reprise au spray de zinc, sinon la rouille démarre là." },
      { titre: "Coupez avant, pas après", texte: "En galvanisation au bain, on coupe et on perce avant de tremper. En tôle prégalvanisée, la tranche reste protégée par effet de bord." },
    ],
  },
  {
    slug: "inox",
    nom: "Inox",
    accroche: "Pour ce qui doit tenir dehors, sans entretien",
    intro:
      "L'inox ne rouille pas : le chrome forme en surface une couche d'oxyde qui se reconstitue seule à chaque rayure. Le 304 couvre la majorité des usages extérieurs ; le 316L, allié au molybdène, résiste en bord de mer, en piscine et au contact des produits chlorés.",
    titreSeo: "Inox 304 et 316L — tube, tôle et plat, découpe sur mesure en Wallonie",
    descSeo:
      "Inox 304 brossé et 316L qualité marine : tubes, tôles, plats, cornières, ronds. Garde-corps, cuisine professionnelle, bord de mer. Prix affichés, coupe aux cotes.",
    proprietes: [
      { label: "Nuances", valeur: "304 (1.4301) · 316L (1.4404)" },
      { label: "Densité", valeur: "8,00 kg/dm³" },
      { label: "Finitions", valeur: "Brut 2B, brossé grain 240, poli miroir" },
      { label: "Tenue à la corrosion", valeur: "Très élevée — sans traitement" },
      { label: "Usage littoral / chloré", valeur: "316L obligatoire" },
    ],
    usages: ["Garde-corps", "Agroalimentaire", "Bord de mer", "Piscine", "Cuisine pro", "Mobilier"],
    familles: ["inox"],
    aRetenir: [
      { titre: "304 ou 316L ?", texte: "304 partout, sauf si la pièce voit du sel ou du chlore en continu — bord de mer, abords de piscine, station d'épuration. Là, 316L, sans discussion." },
      { titre: "L'inox peut quand même rouiller", texte: "Pas lui : les particules d'acier déposées dessus. Ne jamais meuler de l'acier à côté d'une pièce inox, ni utiliser la même brosse métallique." },
      { titre: "Il revient moins cher qu'il n'en a l'air", texte: "Un garde-corps acier peint se repeint tous les 5 à 7 ans. Sur 30 ans, l'inox nu coûte moins que l'acier + la main d'œuvre de reprise." },
    ],
  },
  {
    slug: "aluminium",
    nom: "Aluminium",
    accroche: "Trois fois plus léger, jamais de rouille",
    intro:
      "Le profilé aluminium s'impose dès que le poids compte ou que la structure doit rester nue. Il s'usine et se perce très facilement, se plie à froid, et sa couche d'alumine le protège naturellement. Il se soude en revanche différemment de l'acier — on vous oriente sur l'assemblage.",
    titreSeo: "Profilé aluminium 6060 — tube, tôle, cornière coupés à la demande",
    descSeo:
      "Aluminium 6060 et 5754 : cornières, plats, U, tubes carrés et ronds, tôles lisses et larmées. Léger, inoxydable, anodisable. Découpe aux cotes dans nos 4 dépôts.",
    proprietes: [
      { label: "Alliages", valeur: "6060 T66 (profilés) · 6082 T6 (usinage) · 5754 (tôle)" },
      { label: "Densité", valeur: "2,70 — contre 7,85 pour l'acier" },
      { label: "Tenue à la corrosion", valeur: "Naturelle — couche d'alumine" },
      { label: "Finitions", valeur: "Brut, anodisé, thermolaqué RAL" },
      { label: "Soudage", valeur: "TIG ou MIG sous argon — pas à l'électrode" },
    ],
    usages: ["Habillage", "Menuiserie", "Structure légère", "Mobilier", "Signalétique", "Remorque"],
    familles: ["aluminium"],
    aRetenir: [
      { titre: "Léger ne veut pas dire faible", texte: "L'alu est trois fois moins dense mais aussi trois fois moins rigide. À section égale il fléchit plus : on compense en augmentant la section, pas en espérant." },
      { titre: "Pas d'électrode enrobée", texte: "L'aluminium se soude au TIG ou au MIG sous argon. Un poste à électrode classique ne fait rien de propre dessus." },
      { titre: "Attention au contact acier", texte: "Alu et acier en contact direct avec de l'humidité créent une pile : l'alu se corrode. On isole avec une rondelle nylon ou une fixation inox." },
    ],
  },
  {
    slug: "corten",
    nom: "Acier corten",
    accroche: "La rouille qui protège au lieu de détruire",
    intro:
      "Le corten est un acier allié au cuivre, au chrome et au phosphore. Sa rouille ne s'écaille pas : elle forme une patine dense et adhérente qui bloque l'oxydation en profondeur. On l'achète pour sa tenue, on le garde pour sa couleur.",
    titreSeo: "Acier corten — tôle, bordure, bac et bardage, patine sans entretien",
    descSeo:
      "Acier corten S355J0WP : tôle de 2 à 5 mm, bordures de jardin, bacs à fleurs, brise-vue laser, bardage à clins. Patine stabilisée en 6 à 18 mois, zéro entretien.",
    proprietes: [
      { label: "Nuance", valeur: "S355J0WP — EN 10025-5" },
      { label: "Alliage", valeur: "Cuivre, chrome, phosphore" },
      { label: "Patine", valeur: "Stabilisée en 6 à 18 mois" },
      { label: "Entretien", valeur: "Aucun" },
      { label: "Soudabilité", valeur: "Bonne — fil ou électrode adaptés" },
    ],
    usages: ["Bardage", "Déco jardin", "Bordure", "Bac à fleurs", "Signalétique", "Mobilier"],
    familles: ["corten"],
    aRetenir: [
      { titre: "Il coule pendant sa patine", texte: "Les premiers mois, l'eau de pluie emporte des oxydes qui tachent durablement le béton clair et la pierre. Prévoyez un gravier ou un écoulement." },
      { titre: "Il lui faut des cycles secs", texte: "La patine ne se forme qu'en alternant humide et sec. En contact permanent avec l'eau ou la terre, le corten se corrode comme un acier ordinaire." },
      { titre: "Comptez l'épaisseur perdue", texte: "La patine consomme quelques dixièmes de millimètre. Pour une pièce structurelle, on part d'une épaisseur supérieure au calcul." },
    ],
  },
];

/* ------------------------------------------------------------------ */
/*  HELPERS                                                            */
/* ------------------------------------------------------------------ */

export const familleBySlug = (slug: string) => familles.find((f) => f.slug === slug);
export const matiereBySlug = (slug: string) => matieres.find((m) => m.slug === slug);
export const refBySlug = (famille: string, ref: string) =>
  familleBySlug(famille)?.refs.find((r) => r.ref === ref);

export const allRefs = familles.flatMap((f) => f.refs.map((r) => ({ famille: f, ref: r })));

export const totalRefs = allRefs.length;

export const refsParMatiere = (matiere: string) =>
  allRefs.filter(({ ref }) => ref.matiere === matiere);

/** Prix d'entrée d'une famille, pour les cartes de catalogue. */
export function prixMini(f: Famille) {
  const prix = f.refs.map((r) => r.prix).filter((p): p is number => p !== null);
  if (!prix.length) return null;
  const min = Math.min(...prix);
  const r = f.refs.find((x) => x.prix === min)!;
  return { valeur: min, unite: r.uniteCourte, texte: `dès ${formatPrix(min)}/${r.uniteCourte.slice(2)}` };
}
