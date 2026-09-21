import Link from "next/link";
import type { Produit } from "@/lib/catalogue";
import type { Paire, Section } from "@/lib/description";

/**
 * Modules de la fiche produit. Un seul gabarit pour 495 fiches : chaque module
 * ne s'affiche que si la donnée existe, et n'affiche que la donnée — rien n'est
 * complété. Les textes restent du HTML sémantique (titres, listes, <dl>) : ce
 * que le visiteur lit, Google le lit.
 */

/** Ordre de lecture des spécifications en tête de fiche : ce qui définit la pièce d'abord. */
const PRIORITE = [
  "Largeur", "Épaisseur", "Hauteur", "Diamètre extérieur", "Diamètre", "Section", "Ailes",
  "Format", "Longueur", "Longueur utile", "Largeur utile", "Maille", "Poids", "Masse surfacique",
  "Nuance", "Alliage", "Matière", "Revêtement", "Finition", "Couleur",
];

const rang = (label: string) => {
  const i = PRIORITE.indexOf(label);
  return i === -1 ? PRIORITE.length : i;
};

export function ChiffresCles({ p, matiere }: { p: Produit; matiere: string }) {
  const specs = [...p.specs].sort((a, b) => rang(a.label) - rang(b.label)).slice(0, 5);
  const cartes: Paire[] = [{ label: "Matière", valeur: matiere }, ...specs];
  if (p.kg !== null && !specs.some((s) => s.label === "Poids")) {
    cartes.push({ label: "Poids", valeur: `${p.kg.toLocaleString("fr-BE")} ${p.unitePoids || "kg"}` });
  }
  if (cartes.length < 2) return null;
  return (
    <dl data-module="chiffres-cles" className="mt-6 grid grid-cols-2 gap-2 sm:grid-cols-3">
      {cartes.map((c) => (
        <div key={c.label} className="rounded-xl border border-brume bg-nuage px-3 py-2.5">
          <dt className="font-body text-[11px] uppercase tracking-[0.14em] text-soft">{c.label}</dt>
          <dd className="mt-0.5 break-words font-mono text-sm font-semibold tabular-nums text-encre">{c.valeur}</dd>
        </div>
      ))}
    </dl>
  );
}

function Coche() {
  return (
    <span className="mt-0.5 flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-jaune" aria-hidden="true">
      <svg width="11" height="11" viewBox="0 0 24 24" fill="none">
        <path d="M5 13l4 4L19 7" stroke="#333642" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    </span>
  );
}

export function GrillePaires({ paires }: { paires: Paire[] }) {
  return (
    <dl className="grid gap-x-6 gap-y-2 sm:grid-cols-2">
      {paires.map((pa) => (
        <div key={pa.label + pa.valeur} className="flex flex-col gap-0.5 border-b border-brume/70 py-2 sm:flex-row sm:items-baseline sm:justify-between sm:gap-4">
          <dt className="font-body text-sm text-soft">{pa.label}</dt>
          <dd className="font-body text-sm font-medium text-encre sm:text-right">{pa.valeur}</dd>
        </div>
      ))}
    </dl>
  );
}

/** Un item court, sans verbe conjugué ni ponctuation : une puce visuelle suffit. */
const court = (s: string) => s.length <= 42 && !/[.;!?]/.test(s);

export function ModuleSection({ section, titreParDefaut, niveau = 2 }: { section: Section; titreParDefaut: string; niveau?: 2 | 3 }) {
  const titre = section.titre || titreParDefaut;
  const Titre = niveau === 2 ? "h2" : "h3";
  const tousCourts = section.items.length > 0 && section.items.every(court);
  return (
    <section data-module={section.type} className="rounded-2xl border border-brume bg-white p-5 md:p-6">
      <Titre className="h-title text-sm font-semibold uppercase tracking-[0.14em] text-soft">{titre}</Titre>
      {section.paragraphes.length > 0 && (
        <div className="mt-3 space-y-3 font-body text-sm leading-relaxed text-encre">
          {section.paragraphes.map((t) => <p key={t}>{t}</p>)}
        </div>
      )}
      {section.paires.length > 0 && (
        section.type === "caracteristiques" || section.type === "autre" || section.type === "presentation" ? (
          <div className="mt-3"><GrillePaires paires={section.paires} /></div>
        ) : (
          <ul className="mt-3 space-y-2">
            {section.paires.map((pa) => (
              <li key={pa.label + pa.valeur} className="flex items-start gap-2.5 font-body text-sm leading-relaxed text-encre">
                {section.type === "applications" ? <span className="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-jaune" aria-hidden="true" /> : <Coche />}
                <span><strong className="font-semibold">{pa.label}</strong> : {pa.valeur}</span>
              </li>
            ))}
          </ul>
        )
      )}
      {section.items.length > 0 && (
        section.type === "applications" && tousCourts ? (
          <ul className="mt-3 flex flex-wrap gap-2">
            {section.items.map((it) => (
              <li key={it} className="rounded-full border border-brume bg-nuage px-3 py-1.5 font-body text-sm text-encre">{it}</li>
            ))}
          </ul>
        ) : (
          <ul className="mt-3 space-y-2">
            {section.items.map((it) => (
              <li key={it} className="flex items-start gap-2.5 font-body text-sm leading-relaxed text-encre">
                {section.type === "atouts" || section.type === "services" ? <Coche /> : <span className="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-jaune" aria-hidden="true" />}
                <span>{it}</span>
              </li>
            ))}
          </ul>
        )
      )}
      {section.type === "services" && (
        <Link href="/services" className="lien-tactile mt-4 font-body text-sm font-medium text-encre hover:text-jaune">
          Tous nos services →
        </Link>
      )}
    </section>
  );
}
