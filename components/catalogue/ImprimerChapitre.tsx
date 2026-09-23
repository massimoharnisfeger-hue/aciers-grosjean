"use client";

/**
 * « Imprimer ce chapitre » : la feuille de style d'impression (app/globals.css,
 * section catalogue) masque la navigation et le filtre, coupe les pages entre
 * les familles et garde chaque planche entière. Enregistrer en PDF depuis la
 * boîte d'impression donne un catalogue du chapitre, tel quel.
 */
export default function ImprimerChapitre() {
  return (
    <button type="button" onClick={() => window.print()} className="btn-ghost print:hidden">
      Imprimer ce chapitre
    </button>
  );
}
