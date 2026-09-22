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
 */
export default function VisuelFamille({
  chemin,
  Art,
  className = "",
}: {
  chemin: string;
  /** Illustration de repli, choisie par `artPour`. */
  Art: (p: { className?: string }) => JSX.Element;
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
        sizes="(min-width: 1024px) 33vw, (min-width: 640px) 50vw, 100vw"
        unoptimized
        className={`absolute inset-0 h-full w-full object-cover transition-transform duration-700 group-hover:scale-[1.07] ${className}`}
      />
    );
  }
  return (
    <Art className={`absolute inset-0 h-full w-full transition-transform duration-700 group-hover:scale-[1.07] ${className}`} />
  );
}
