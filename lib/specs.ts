import type { Spec } from "@/lib/catalogue";

/**
 * Ordre de lecture des spécifications : ce qui définit la pièce d'abord.
 *
 * Une seule liste pour les chiffres clés de la fiche produit
 * (components/catalogue/FicheModules.tsx) et pour les cartes du catalogue
 * visuel (lib/catalogue-visuel.ts). Deux copies auraient fini par diverger,
 * et la même cornière se serait lue dans deux ordres selon la page.
 */
export const PRIORITE_SPECS = [
  "Largeur", "Épaisseur", "Hauteur", "Diamètre extérieur", "Diamètre", "Section", "Ailes",
  "Format", "Longueur", "Longueur utile", "Largeur utile", "Maille", "Poids", "Masse surfacique",
  "Nuance", "Alliage", "Matière", "Revêtement", "Finition", "Couleur",
];

export const rangSpec = (label: string) => {
  const i = PRIORITE_SPECS.indexOf(label);
  return i === -1 ? PRIORITE_SPECS.length : i;
};

/** Les spécifications triées par importance ; le tableau reçu n'est pas modifié. */
export const specsParImportance = (specs: Spec[]) =>
  [...specs].sort((a, b) => rangSpec(a.label) - rangSpec(b.label));
