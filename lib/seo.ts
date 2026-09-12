/**
 * Garde-fous SEO.
 *
 * Google tronque le title autour de 580 px (≈ 60 caractères) et la meta
 * description vers 160. Au-delà, la fin est remplacée par « … » : le mot qui
 * déclenche le clic disparaît. L'audit du site actuel relevait des
 * descriptions allant jusqu'à 1 768 caractères — autant dire perdues.
 *
 * Ces deux fonctions coupent proprement, à la frontière d'un mot, et
 * n'ajoutent la marque que si elle tient dans le budget.
 */

export const MARQUE = "Aciers Grosjean";

const TITRE_MAX = 60;
const DESC_MAX = 158;

/** Coupe à la frontière de mot, sans laisser de ponctuation orpheline. */
function couper(s: string, max: number) {
  const t = s.trim().replace(/\s+/g, " ");
  if (t.length <= max) return t;
  const dur = t.slice(0, max - 1);
  const esp = dur.lastIndexOf(" ");
  return (esp > max * 0.6 ? dur.slice(0, esp) : dur).replace(/[\s,;:–—-]+$/, "") + "…";
}

/**
 * Title complet. La marque n'est ajoutée que si elle tient — le blueprint
 * demande explicitement d'éviter la double marque sur les fiches produits.
 */
export function titre(contenu: string, avecMarque = true) {
  const base = contenu.trim().replace(/\s+/g, " ");
  const suffixe = ` | ${MARQUE}`;
  if (avecMarque && base.length + suffixe.length <= TITRE_MAX) return base + suffixe;
  return couper(base, TITRE_MAX);
}

/** Meta description bornée à 158 caractères. */
export function description(contenu: string) {
  return couper(contenu, DESC_MAX);
}
