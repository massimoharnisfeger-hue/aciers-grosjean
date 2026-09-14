import type { CSSProperties } from "react";

/**
 * Apparition douce au défilement, sans JavaScript (classe .reveal, globals.css).
 * Le contenu est rendu visible par défaut : l'effet est un bonus, jamais une
 * condition pour voir la page. `delay` décale l'effet (en secondes, comme avant).
 */
export default function Reveal({
  children,
  className = "",
  delay = 0,
  y = 28,
}: {
  children: React.ReactNode;
  className?: string;
  delay?: number;
  y?: number;
}) {
  const style = {
    "--reveal-y": `${y}px`,
    "--reveal-decalage": `${Math.round(delay * 400)}px`,
  } as CSSProperties;

  return (
    <div className={`reveal ${className}`} style={style}>
      {children}
    </div>
  );
}
