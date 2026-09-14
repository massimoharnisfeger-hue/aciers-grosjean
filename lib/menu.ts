import { univers, noeuds, produitsSous } from "@/lib/catalogue";

/**
 * Données du méga-menu, calculées côté serveur.
 *
 * Nav est un composant client : s'il importait lib/catalogue.ts, les 495 fiches
 * produits (≈ 270 Ko de JavaScript) partiraient dans le navigateur sur chaque
 * page du site. Le layout lui passe seulement ce résumé.
 */
export type MenuUnivers = {
  slug: string;
  nom: string;
  total: number;
  familles: { nom: string; chemin: string }[];
};

export function menuCatalogue(): MenuUnivers[] {
  return univers.map((u) => ({
    slug: u.slug,
    nom: u.nom,
    total: produitsSous(`/${u.slug}`).length,
    familles: u.enfants
      .map((c) => noeuds[c])
      .filter(Boolean)
      .map((f) => ({ nom: f.nom, chemin: f.chemin })),
  }));
}
