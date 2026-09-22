import visuels from "@/lib/visuels-produits.json";

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

/** Photo studio d'une catégorie, telle que produite par integrer_visuels.py. */
export type Studio = { src: string; largeur: number; hauteur: number; alt: string };

const STUDIOS = (visuels as { categories: Record<string, Studio> }).categories;

/**
 * La photo studio d'une famille, s'il n'y en a qu'une sous ce chemin.
 *
 * Une famille regroupe plusieurs catégories ; chacune peut avoir sa photo.
 * « Bardage » n'en a qu'une (parement imitation bois) : elle représente la
 * famille sans ambiguïté. « Profilés acier » en a sept — laquelle montrer est
 * un choix visuel, pas une déduction, donc on garde l'illustration dessinée.
 *
 * Contrôle : tests/test_produit.py (D11).
 */
export function studioUniqueDe(chemin: string): Studio | null {
  const prefixe = chemin.endsWith("/") ? chemin : chemin + "/";
  const candidats = Object.entries(STUDIOS).filter(
    ([c]) => c === chemin || c.startsWith(prefixe)
  );
  return candidats.length === 1 ? candidats[0][1] : null;
}
