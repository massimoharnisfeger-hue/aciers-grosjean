import type { Produit } from "@/lib/catalogue";

/**
 * Les nombres d'un nom de produit, dans l'ordre où ils apparaissent.
 * « Plat 20x3mm en acier » → [20, 3]. La virgule décimale est acceptée :
 * « Tube rond 42,4x2,5mm » → [42.4, 2.5].
 */
export const cotesDuNom = (nom: string) =>
  (nom.match(/\d+(?:[.,]\d+)?/g) ?? []).map((n) => parseFloat(n.replace(",", ".")));

/**
 * Le tri « Par section », qui ne triait rien.
 *
 * Mesuré le 22/09 sur `/acier/profiles/plat` : l'ordre servi était celui du
 * fichier, c'est-à-dire alphabétique — 100x10, 100x5, 100x8, 10x3, 120x10,
 * 20x10. Un client qui cherche un plat de 20x3 devait le traquer. Dans un
 * négoce où l'on choisit par cote, c'est le tri le plus utilisé, et c'était
 * celui proposé par défaut.
 *
 * La famille passe avant la cote. Premier essai, vu à l'écran : trier sur les
 * seuls nombres rangeait bien chaque famille, mais les entremêlait toutes dans
 * la vue « Tous » — rond lisse 8, carré plein 8, rond lisse 10, plat 10x3,
 * carré plein 10. « Par section » veut dire les sections d'une même famille, et
 * une famille se lit d'un bloc. On compare donc d'abord la sous-catégorie.
 *
 * Ensuite les nombres du nom, un à un. À nombres égaux jusque-là, le nom qui en
 * porte le moins passe devant, puis l'ordre alphabétique départage : un tri
 * doit être total, sinon l'ordre change d'un affichage à l'autre.
 *
 * Partagé par le tableau des pages de catégorie (TableauProduits, contrôle P14)
 * et par les variantes du catalogue visuel : une famille se lit dans le même
 * ordre partout.
 */
export const parCotes = (a: Produit, b: Produit) => {
  if (a.categorie !== b.categorie) return a.categorie.localeCompare(b.categorie, "fr");
  const ca = cotesDuNom(a.nom);
  const cb = cotesDuNom(b.nom);
  for (let i = 0; i < Math.max(ca.length, cb.length); i += 1) {
    const x = ca[i];
    const y = cb[i];
    if (x === undefined) return -1;
    if (y === undefined) return 1;
    if (x !== y) return x - y;
  }
  return a.nom.localeCompare(b.nom, "fr");
};
