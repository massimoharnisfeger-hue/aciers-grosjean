import LogoSvg from "@/components/ui/LogoSvg";

/**
 * Logo officiel Aciers Grosjean.
 *
 * Extrait en vectoriel de la charte graphique (e-identite, avril 2024,
 * déclinaison à plat de la page 2) — 23 tracés, pas une recomposition
 * typographique, que la charte interdit formellement (§4).
 *
 * Rendu en SVG inline (voir LogoSvg) pour pouvoir animer le monogramme
 * séparément du lettrage. Les fichiers public/logo.svg et
 * public/logo-blanc.svg restent disponibles pour les usages externes
 * (signature e-mail, documents, réseaux sociaux).
 */
export default function Logo({
  variante = "encre",
  hauteur = 44,
  anime = true,
  className = "",
}: {
  variante?: "encre" | "blanc";
  /** Hauteur d'affichage en pixels. */
  hauteur?: number;
  anime?: boolean;
  className?: string;
}) {
  return (
    <LogoSvg
      hauteur={hauteur}
      couleur={variante === "blanc" ? "#FFFFFF" : "#333642"}
      anime={anime}
      className={className}
    />
  );
}
