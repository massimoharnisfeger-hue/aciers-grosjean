/**
 * Logo officiel Aciers Grosjean.
 *
 * Extrait en vectoriel de la charte graphique (e-identite, avril 2024, page 2,
 * déclinaison à plat) par scripts/extraire-logo.py — 23 tracés, pas une
 * recomposition typographique. La charte l'interdit formellement (§4) et c'est
 * bien le fichier d'origine qui est servi ici.
 *
 *   public/logo.svg        encre #333642, pour fond blanc
 *   public/logo-blanc.svg  blanc, pour le pied de page sombre
 *   app/icon.svg           monogramme, pour l'onglet du navigateur
 *
 * Proportions natives : 214 × 77,7 pt, soit un rapport de 2,754.
 * La hauteur pilote l'affichage ; la largeur en découle, et les attributs
 * width/height évitent tout saut de mise en page au chargement.
 */

const RATIO = 214 / 77.7;

export default function Logo({
  variante = "encre",
  hauteur = 34,
  className = "",
}: {
  variante?: "encre" | "blanc";
  /** Hauteur d'affichage en pixels. */
  hauteur?: number;
  className?: string;
}) {
  return (
    // eslint-disable-next-line @next/next/no-img-element
    <img
      src={variante === "blanc" ? "/logo-blanc.svg" : "/logo.svg"}
      alt="Aciers Grosjean"
      width={Math.round(hauteur * RATIO)}
      height={hauteur}
      className={`w-auto ${className}`}
      style={{ height: hauteur }}
    />
  );
}
