"use client";

import { useMemo, useState } from "react";
import Link from "next/link";
import type { Produit } from "@/lib/catalogue";
import { formatPrix } from "@/lib/format";

const norm = (s: string) =>
  s
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/[^a-z0-9]/g, "");

const nb = (v: number, d = 2) =>
  v.toLocaleString("fr-BE", { minimumFractionDigits: d, maximumFractionDigits: d });

export default function TableauProduits({
  produits,
  groupes = [],
  id,
}: {
  produits: Produit[];
  /** Sous-catégories pour filtrer, quand la page en couvre plusieurs. */
  groupes?: { chemin: string; nom: string }[];
  id: string;
}) {
  const [q, setQ] = useState("");
  const [groupe, setGroupe] = useState("Tous");
  const [tri, setTri] = useState<"defaut" | "prix" | "poids">("defaut");

  const liste = useMemo(() => {
    const nq = norm(q);
    let out = produits.filter((p) => {
      if (groupe !== "Tous" && p.categorie !== groupe) return false;
      if (!nq) return true;
      return norm(p.nom + p.specs.map((s) => s.valeur).join("")).includes(nq);
    });
    if (tri === "prix") out = [...out].sort((a, b) => (a.prix ?? 1e9) - (b.prix ?? 1e9));
    if (tri === "poids") out = [...out].sort((a, b) => (a.kg ?? 1e9) - (b.kg ?? 1e9));
    return out;
  }, [produits, q, groupe, tri]);

  return (
    <div>
      <div className="sticky top-[68px] z-30 -mx-5 mb-8 border-y border-brume bg-white/90 px-5 py-4 backdrop-blur-md md:-mx-8 md:px-8">
        <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
          {groupes.length > 1 && (
            <div className="-mb-2 flex gap-2 overflow-x-auto pb-2">
              {[{ chemin: "Tous", nom: "Tous" }, ...groupes].map((g) => {
                const n =
                  g.chemin === "Tous"
                    ? produits.length
                    : produits.filter((p) => p.categorie === g.chemin).length;
                const actif = groupe === g.chemin;
                return (
                  <button
                    key={g.chemin}
                    type="button"
                    onClick={() => setGroupe(g.chemin)}
                    aria-pressed={actif}
                    className={`whitespace-nowrap rounded-full border px-4 py-1.5 font-body text-sm transition-all ${
                      actif ? "border-encre bg-encre text-white" : "border-brume text-encre hover:border-encre/40"
                    }`}
                  >
                    {g.nom}
                    <span className={`ml-2 font-mono text-[11px] ${actif ? "text-white/55" : "text-soft"}`}>{n}</span>
                  </button>
                );
              })}
            </div>
          )}

          <div className="flex flex-1 gap-3 lg:max-w-md lg:justify-end">
            <label className="relative flex-1 lg:max-w-xs">
              <span className="sr-only">Rechercher une section</span>
              <svg
                className="pointer-events-none absolute left-3.5 top-1/2 -translate-y-1/2 text-soft"
                width="16" height="16" viewBox="0 0 24 24" fill="none" aria-hidden="true"
              >
                <circle cx="11" cy="11" r="7" stroke="currentColor" strokeWidth="2" />
                <path d="M20 20l-3.5-3.5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
              </svg>
              <input
                id={`recherche-${id}`}
                value={q}
                onChange={(e) => setQ(e.target.value)}
                placeholder="40x40, IPE 200, 3mm…"
                className="w-full rounded-xl border border-brume bg-white py-2.5 pl-10 pr-3 font-body text-sm text-encre placeholder:text-soft focus:border-encre focus:outline-none"
              />
            </label>

            <label className="sr-only" htmlFor={`tri-${id}`}>Trier</label>
            <select
              id={`tri-${id}`}
              value={tri}
              onChange={(e) => setTri(e.target.value as typeof tri)}
              className="rounded-xl border border-brume bg-white px-3 py-2.5 font-body text-sm text-encre focus:border-encre focus:outline-none"
            >
              <option value="defaut">Par section</option>
              <option value="prix">Prix croissant</option>
              <option value="poids">Poids croissant</option>
            </select>
          </div>
        </div>
      </div>

      <p className="mb-5 font-body text-sm text-soft" aria-live="polite">
        <strong className="font-mono tabular-nums text-encre">{liste.length}</strong> produit
        {liste.length > 1 ? "s" : ""}
        {q && <> · « {q} »</>}
      </p>

      {liste.length === 0 ? (
        <div className="rounded-2xl border border-dashed border-brume bg-nuage p-12 text-center">
          <p className="h-title text-lg text-encre">Aucun produit ne correspond</p>
          <p className="mx-auto mt-2 max-w-sm font-body text-sm text-soft">
            Le stock va au-delà de ce qui est listé ici. Décrivez votre besoin&nbsp;: on vous
            répond en 24&nbsp;h, avec le prix.
          </p>
          <Link href="/devis" className="btn-cta mt-6">Demander une section</Link>
        </div>
      ) : (
        <>
          <div className="hidden overflow-x-auto rounded-2xl border border-brume md:block">
            <table className="w-full border-collapse text-left">
              <caption className="sr-only">Produits disponibles avec poids et prix hors TVA</caption>
              <thead>
                <tr className="border-b border-brume bg-nuage">
                  <th scope="col" className="px-5 py-3 font-body text-xs font-semibold uppercase tracking-[0.12em] text-soft">Produit</th>
                  <th scope="col" className="px-5 py-3 text-right font-body text-xs font-semibold uppercase tracking-[0.12em] text-soft">Poids</th>
                  <th scope="col" className="px-5 py-3 text-right font-body text-xs font-semibold uppercase tracking-[0.12em] text-soft">Prix</th>
                  <th scope="col" className="px-5 py-3 text-right font-body text-xs font-semibold uppercase tracking-[0.12em] text-soft">Stock</th>
                  <th scope="col" className="w-12 px-5 py-3"><span className="sr-only">Voir</span></th>
                </tr>
              </thead>
              <tbody>
                {liste.map((p) => (
                  <tr key={p.slug} className="group border-b border-brume/70 transition-colors last:border-0 hover:bg-nuage/70">
                    <th scope="row" className="px-5 py-3.5 text-left font-normal">
                      <Link href={`/p/${p.slug}`} className="h-title font-semibold text-encre hover:underline">
                        {p.nom}
                      </Link>
                    </th>
                    <td className="px-5 py-3.5 text-right font-mono text-sm tabular-nums text-soft">
                      {p.kg !== null ? (
                        <>
                          {nb(p.kg)}
                          <span className="ml-1 text-[11px]">{p.unitePoids}</span>
                        </>
                      ) : "—"}
                    </td>
                    <td className="px-5 py-3.5 text-right">
                      <span className="h-title font-bold tabular-nums text-encre">{formatPrix(p.prix)}</span>
                      {p.prix !== null && (
                        <span className="ml-1 font-body text-[11px] text-soft">{p.uniteCourte.slice(1)}</span>
                      )}
                    </td>
                    <td className="px-5 py-3.5 text-right">
                      <span className="inline-flex items-center gap-1.5 font-body text-xs text-encre">
                        <span className="h-2 w-2 rounded-full bg-jaune" />En stock
                      </span>
                    </td>
                    <td className="px-5 py-3.5 text-right">
                      <Link
                        href={`/p/${p.slug}`}
                        className="inline-flex h-8 w-8 items-center justify-center rounded-full border border-brume text-encre transition-all group-hover:border-jaune group-hover:bg-jaune"
                        aria-label={`Voir ${p.nom}`}
                      >
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                          <path d="M5 12h14M13 6l6 6-6 6" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round" />
                        </svg>
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <ul className="grid gap-3 md:hidden">
            {liste.map((p) => (
              <li key={p.slug}>
                <Link href={`/p/${p.slug}`} className="flex items-center justify-between gap-4 rounded-xl border border-brume bg-white p-4">
                  <span className="min-w-0">
                    <span className="h-title block font-semibold leading-snug text-encre">{p.nom}</span>
                    {p.kg !== null && (
                      <span className="mt-0.5 block font-mono text-xs text-soft">
                        {nb(p.kg)} {p.unitePoids}
                      </span>
                    )}
                  </span>
                  <span className="shrink-0 text-right">
                    <span className="h-title block font-bold tabular-nums text-encre">{formatPrix(p.prix)}</span>
                    {p.prix !== null && <span className="font-body text-[11px] text-soft">{p.uniteCourte.slice(1)}</span>}
                  </span>
                </Link>
              </li>
            ))}
          </ul>
        </>
      )}
    </div>
  );
}
