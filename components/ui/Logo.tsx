/**
 * Logo Aciers Grosjean.
 *
 * ⚠️ PROVISOIRE — le lettrage officiel est propriétaire et la charte interdit
 * formellement de le recomposer avec une police (§4 : « ne jamais le recomposer
 * avec une police. Utiliser le fichier logo fourni »).
 *
 * Ce qui s'affiche ici est donc un MARQUEUR DE PLACE, pas le logo de la marque.
 *
 * POUR METTRE LE VRAI LOGO — une seule manipulation, rien d'autre à toucher :
 *   1. déposer le fichier officiel dans  public/logo.svg        (version sombre, pour fond blanc)
 *   2. déposer la version blanche dans   public/logo-blanc.svg  (pour le pied de page sombre)
 *   3. c'est tout : la barre de navigation, le pied de page et tous les gabarits
 *      basculent automatiquement sur ces fichiers.
 *
 * La zone d'exclusion de la charte (un espace au moins égal à la hauteur du « G »)
 * est réservée ci-dessous par le padding du conteneur.
 */

const AVEC_FICHIER_OFFICIEL = false; // ← passer à true une fois les fichiers déposés

export default function Logo({
  variante = "encre",
  className = "",
}: {
  variante?: "encre" | "blanc";
  className?: string;
}) {
  const blanc = variante === "blanc";

  if (AVEC_FICHIER_OFFICIEL) {
    return (
      // eslint-disable-next-line @next/next/no-img-element
      <img
        src={blanc ? "/logo-blanc.svg" : "/logo.svg"}
        alt="Aciers Grosjean"
        className={`h-7 w-auto ${className}`}
      />
    );
  }

  return (
    <span
      className={`flex items-baseline gap-1.5 leading-none ${className}`}
      aria-label="Aciers Grosjean"
      data-logo="provisoire"
    >
      <span className={`h-title text-xl font-bold tracking-tight ${blanc ? "text-white" : "text-encre"}`}>
        GROSJEAN
      </span>
      <span className={`h-sub text-xs ${blanc ? "text-soft-light" : "text-soft"}`}>aciers</span>
    </span>
  );
}
