import Image from "next/image";
import type { JSX } from "react";
import { studioUniqueDe } from "@/lib/visuels";

/**
 * Le visuel d'une carte de famille ou de sous-catégorie.
 *
 * Montre la vraie photo studio quand une seule existe sous ce chemin ; sinon
 * l'illustration SVG de la famille. Choisir entre deux photos est une décision
 * visuelle humaine, pas une déduction : c'est pourquoi la règle s'arrête au
 * candidat unique (`lib/visuels.ts`, contrôle D11).
 *
 * Un seul composant pour les deux gabarits de catalogue : recopier ce JSX
 * perdrait la règle dans l'un des deux — c'est la leçon L-029.
 *
 * `sizes` est obligatoire et n'a pas de valeur par défaut : les deux gabarits
 * affichent le même composant à des tailles sans rapport — une carte de 4/3
 * pleine colonne, et une vignette de 80 px. Les photos studio font toutes
 * 1600 × 1200. Une valeur par défaut serait juste pour l'un et fausse pour
 * l'autre, sans que rien ne le signale : le 22/09/2026, la vignette de 80 px
 * téléchargeait la photo entière (jusqu'à 187 Ko pour 80 px de côté).
 * Contrôle P10.
 */
export default function VisuelFamille({
  chemin,
  Art,
  sizes,
  className = "",
}: {
  chemin: string;
  /** Illustration de repli, choisie par `artPour`. */
  Art: (p: { className?: string }) => JSX.Element;
  /** Largeur d'affichage réelle, vue du gabarit appelant. */
  sizes: string;
  className?: string;
}) {
  const studio = studioUniqueDe(chemin);
  if (studio) {
    return (
      <Image
        src={studio.src}
        alt={studio.alt}
        width={studio.largeur}
        height={studio.hauteur}
        sizes={sizes}
        className={`absolute inset-0 h-full w-full object-cover transition-transform duration-700 group-hover:scale-[1.07] ${className}`}
      />
    );
  }
  return (
    <Art className={`absolute inset-0 h-full w-full transition-transform duration-700 group-hover:scale-[1.07] ${className}`} />
  );
}
