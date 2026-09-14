/**
 * Formatage partagé par le serveur et les composants client.
 *
 * Fichier séparé de lib/catalogue.ts : un composant client qui importe une
 * fonction du catalogue embarque aussi les 495 fiches produits dans le JavaScript.
 */
export function formatPrix(v: number | null) {
  if (v === null) return "Sur devis";
  return v.toLocaleString("fr-BE", { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + " €";
}
