/**
 * Associe un chemin de catalogue à l'illustration technique qui lui va.
 * Les illustrations sont dessinées à la main en SVG (components/art),
 * donc libres de droit et nettes à toutes les tailles.
 */

const REGLES: [RegExp, string][] = [
  [/poutrelles/, "poutrelles"],
  [/tubes?/, "tubes"],
  [/toles?|tole-/, "toles"],
  [/corniere/, "cornieres-plats"],
  [/corten/, "corten"],
  [/treillis|armatures-beton|rond-a-beton/, "treillis"],
  [/plat|rond-plein|carre-plein|fer-t|profil-/, "plats"],
  [/visserie|fixations/, "visserie"],
  [/poteaux|clotures|panneaux-rigides|bordures/, "poteaux-cloture"],
  [/caillebotis|outillage|protection-chimie/, "visserie"],
  [/toiture|bardage|panneaux-isoles|panneau-tuile/, "toles"],
];

export function artPour(chemin: string, defaut = "poutrelles") {
  const c = chemin.toLowerCase();
  // on teste du segment le plus précis au plus général
  const segments = c.replace(/^\//, "").split("/").reverse();
  for (const seg of segments) {
    for (const [re, art] of REGLES) if (re.test(seg)) return art;
  }
  return defaut;
}
