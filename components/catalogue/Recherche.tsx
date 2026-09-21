"use client";

import { useMemo, useState } from "react";
import Link from "next/link";
import { tousProduits, noeuds, formatPrix } from "@/lib/catalogue";

const norm = (s: string) =>
  s
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/[^a-z0-9]+/g, " ")
    .trim();

/** Index construit une seule fois : produits + catégories. */
const INDEX = [
  ...tousProduits.map((p) => ({
    type: "produit" as const,
    titre: p.nom,
    href: `/p/${p.slug}`,
    contexte: noeuds[p.categorie]?.nom ?? p.univers,
    prix: p.prix,
    unite: p.uniteCourte,
    cle: norm(p.nom + " " + p.specs.map((s) => s.valeur).join(" ")),
  })),
  ...Object.values(noeuds).map((n) => ({
    type: "categorie" as const,
    titre: n.nom,
    href: n.chemin,
    contexte: n.chemin.split("/")[1],
    prix: null as number | null,
    unite: "",
    cle: norm(n.nom + " " + n.accroche),
  })),
];

export default function Recherche() {
  const [q, setQ] = useState("");

  const resultats = useMemo(() => {
    const mots = norm(q).split(" ").filter(Boolean);
    if (!mots.length) return [];
    return INDEX.filter((e) => mots.every((m) => e.cle.includes(m)))
      .sort((a, b) => (a.type === b.type ? 0 : a.type === "categorie" ? -1 : 1))
      .slice(0, 60);
  }, [q]);

  const suggestions = ["cornière 40x40", "IPE 200", "tôle 3mm", "tube carré", "corten", "treillis"];

  return (
    <div>
      <label className="relative block">
        <span className="sr-only">Rechercher dans le catalogue</span>
        <svg
          className="pointer-events-none absolute left-5 top-1/2 -translate-y-1/2 text-soft"
          width="20" height="20" viewBox="0 0 24 24" fill="none" aria-hidden="true"
        >
          <circle cx="11" cy="11" r="7" stroke="currentColor" strokeWidth="2" />
          <path d="M20 20l-3.5-3.5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
        </svg>
        <input
          id="recherche-globale"
          type="search"
          value={q}
          onChange={(e) => setQ(e.target.value)}
          placeholder="Cornière 40x40, IPE 200, tôle galvanisée…"
          className="w-full rounded-2xl border border-brume bg-white py-5 pl-14 pr-5 font-body text-lg text-encre placeholder:text-soft focus:border-encre focus:outline-none"
        />
      </label>

      {!q && (
        <div className="mt-5 flex flex-wrap items-center gap-2">
          <span className="font-body text-sm text-soft">Essayez&nbsp;:</span>
          {suggestions.map((s) => (
            <button
              key={s}
              type="button"
              onClick={() => setQ(s)}
              className="rounded-full border border-brume px-3.5 py-1.5 font-body text-sm text-encre transition-colors hover:border-encre hover:bg-nuage"
            >
              {s}
            </button>
          ))}
        </div>
      )}

      {q && (
        <>
          <p className="mt-6 font-body text-sm text-soft" aria-live="polite">
            <strong className="font-mono tabular-nums text-encre">{resultats.length}</strong>{" "}
            résultat{resultats.length > 1 ? "s" : ""} pour « {q} »
          </p>

          {resultats.length === 0 ? (
            <div className="mt-6 rounded-2xl border border-dashed border-brume bg-nuage p-12 text-center">
              <p className="h-title text-lg text-encre">Rien trouvé sous ce nom</p>
              <p className="mx-auto mt-2 max-w-sm font-body text-sm text-soft">
                Le stock va au-delà de ce qui est publié. Décrivez ce que vous cherchez&nbsp;:
                on vous dit en 24&nbsp;h si on l’a, et à quel prix.
              </p>
              <Link href="/devis" className="btn-cta mt-6">Décrire mon besoin</Link>
            </div>
          ) : (
            <ul className="mt-6 divide-y divide-brume overflow-hidden rounded-2xl border border-brume">
              {resultats.map((r) => (
                <li key={r.href}>
                  <Link
                    href={r.href}
                    className="group flex items-center justify-between gap-4 bg-white px-5 py-4 transition-colors hover:bg-nuage"
                  >
                    <span className="min-w-0">
                      <span className="h-title block truncate font-semibold text-encre">{r.titre}</span>
                      <span className="mt-0.5 block font-body text-xs text-soft">
                        {r.type === "categorie" ? "Catégorie" : r.contexte}
                      </span>
                    </span>
                    <span className="shrink-0 text-right">
                      {r.prix !== null ? (
                        <>
                          <span className="h-title block font-bold tabular-nums text-encre">
                            {formatPrix(r.prix)}
                          </span>
                          <span className="font-body text-[11px] text-soft">{r.unite.slice(1)}</span>
                        </>
                      ) : (
                        <span className="font-body text-sm text-soft">Parcourir</span>
                      )}
                    </span>
                  </Link>
                </li>
              ))}
            </ul>
          )}
        </>
      )}
    </div>
  );
}
