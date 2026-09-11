"use client";

import { useMemo, useState } from "react";
import Link from "next/link";
import type { Ref } from "@/lib/catalogue";

/** Normalise pour la recherche : sans accent, sans séparateur, minuscule. */
const norm = (s: string) =>
  s
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/[^a-z0-9]/g, "");

export default function TableauRefs({
  famille,
  refs,
  series,
}: {
  famille: string;
  refs: Ref[];
  series: string[];
}) {
  const [q, setQ] = useState("");
  const [serie, setSerie] = useState<string>("Toutes");
  const [tri, setTri] = useState<"section" | "prix" | "poids">("section");

  const filtres = useMemo(() => {
    const nq = norm(q);
    let out = refs.filter((r) => {
      if (serie !== "Toutes" && r.serie !== serie) return false;
      if (!nq) return true;
      return norm(r.nom + r.dims + r.serie + r.usages.join("")).includes(nq);
    });
    if (tri === "prix") out = [...out].sort((a, b) => (a.prix ?? 1e9) - (b.prix ?? 1e9));
    if (tri === "poids") out = [...out].sort((a, b) => a.kg - b.kg);
    return out;
  }, [refs, q, serie, tri]);

  const onglets = ["Toutes", ...series];

  return (
    <div>
      {/* barre d'outils */}
      <div className="sticky top-[72px] z-30 -mx-5 mb-8 border-y border-brume bg-white/85 px-5 py-4 backdrop-blur-md md:-mx-8 md:px-8">
        <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
          {/* onglets série */}
          <div className="-mb-2 flex gap-2 overflow-x-auto pb-2">
            {onglets.map((s) => (
              <button
                key={s}
                type="button"
                onClick={() => setSerie(s)}
                aria-pressed={serie === s}
                className={`whitespace-nowrap rounded-full border px-4 py-1.5 font-body text-sm transition-all ${
                  serie === s
                    ? "border-encre bg-encre text-white"
                    : "border-brume text-encre hover:border-encre/40"
                }`}
              >
                {s}
                <span className={`ml-2 font-mono text-[11px] ${serie === s ? "text-white/55" : "text-soft"}`}>
                  {s === "Toutes" ? refs.length : refs.filter((r) => r.serie === s).length}
                </span>
              </button>
            ))}
          </div>

          <div className="flex gap-3">
            <label className="relative flex-1 lg:w-64">
              <span className="sr-only">Rechercher une section</span>
              <svg
                className="pointer-events-none absolute left-3.5 top-1/2 -translate-y-1/2 text-soft"
                width="16" height="16" viewBox="0 0 24 24" fill="none"
              >
                <circle cx="11" cy="11" r="7" stroke="currentColor" strokeWidth="2" />
                <path d="M20 20l-3.5-3.5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
              </svg>
              <input
                id={`recherche-${famille}`}
                value={q}
                onChange={(e) => setQ(e.target.value)}
                placeholder="40x40, IPE 200, portail…"
                className="w-full rounded-xl border border-brume bg-white py-2.5 pl-10 pr-3 font-body text-sm text-encre placeholder:text-soft focus:border-encre focus:outline-none"
              />
            </label>

            <label className="sr-only" htmlFor={`tri-${famille}`}>Trier par</label>
            <select
              id={`tri-${famille}`}
              value={tri}
              onChange={(e) => setTri(e.target.value as typeof tri)}
              className="rounded-xl border border-brume bg-white px-3 py-2.5 font-body text-sm text-encre focus:border-encre focus:outline-none"
            >
              <option value="section">Par section</option>
              <option value="prix">Prix croissant</option>
              <option value="poids">Poids croissant</option>
            </select>
          </div>
        </div>
      </div>

      <p className="mb-5 font-body text-sm text-soft" aria-live="polite">
        <strong className="font-mono tabular-nums text-encre">{filtres.length}</strong>{" "}
        référence{filtres.length > 1 ? "s" : ""}
        {serie !== "Toutes" && <> · {serie.toLowerCase()}</>}
        {q && <> · « {q} »</>}
      </p>

      {filtres.length === 0 ? (
        <div className="rounded-2xl border border-dashed border-brume bg-nuage p-12 text-center">
          <p className="h-title text-lg text-encre">Aucune section ne correspond</p>
          <p className="mx-auto mt-2 max-w-sm font-body text-sm text-soft">
            Le stock va bien au-delà de ce qui est listé ici. Décrivez votre besoin, on vous
            dit en 24 h si on l'a — et à quel prix.
          </p>
          <Link href="/devis" className="btn-cta mt-6">Demander une section</Link>
        </div>
      ) : (
        <>
          {/* ---- Tableau (écrans larges) ---- */}
          <div className="hidden overflow-x-auto rounded-2xl border border-brume md:block">
            <table className="w-full border-collapse text-left">
              <thead>
                <tr className="border-b border-brume bg-nuage">
                  <th scope="col" className="px-5 py-3 font-body text-xs font-semibold uppercase tracking-[0.12em] text-soft">Référence</th>
                  <th scope="col" className="px-5 py-3 font-body text-xs font-semibold uppercase tracking-[0.12em] text-soft">Dimensions</th>
                  <th scope="col" className="px-5 py-3 text-right font-body text-xs font-semibold uppercase tracking-[0.12em] text-soft">Poids</th>
                  <th scope="col" className="px-5 py-3 text-right font-body text-xs font-semibold uppercase tracking-[0.12em] text-soft">Prix</th>
                  <th scope="col" className="px-5 py-3 text-right font-body text-xs font-semibold uppercase tracking-[0.12em] text-soft">Stock</th>
                  <th scope="col" className="w-12 px-5 py-3"><span className="sr-only">Voir</span></th>
                </tr>
              </thead>
              <tbody>
                {filtres.map((r) => (
                  <tr key={r.ref} className="group border-b border-brume/70 last:border-0 transition-colors hover:bg-nuage/70">
                    <th scope="row" className="px-5 py-3.5 text-left font-normal">
                      <Link href={`/produits/${famille}/${r.ref}`} className="h-title font-semibold text-encre hover:underline">
                        {r.nom}
                      </Link>
                      <span className="mt-0.5 block font-body text-xs text-soft">{r.serie}</span>
                    </th>
                    <td className="px-5 py-3.5 font-mono text-sm tabular-nums text-soft">{r.dims}</td>
                    <td className="px-5 py-3.5 text-right font-mono text-sm tabular-nums text-soft">
                      {r.kg.toLocaleString("fr-BE", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                      <span className="ml-1 text-[11px]">{r.unitePoids}</span>
                    </td>
                    <td className="px-5 py-3.5 text-right">
                      <span className="h-title font-bold tabular-nums text-encre">{r.prixTexte}</span>
                      <span className="ml-1 font-body text-[11px] text-soft">{r.uniteCourte.slice(1)}</span>
                    </td>
                    <td className="px-5 py-3.5 text-right">
                      {r.stock ? (
                        <span className="inline-flex items-center gap-1.5 font-body text-xs text-encre">
                          <span className="h-2 w-2 rounded-full bg-jaune" />En stock
                        </span>
                      ) : (
                        <span className="font-body text-xs text-soft">Sur commande</span>
                      )}
                    </td>
                    <td className="px-5 py-3.5 text-right">
                      <Link
                        href={`/produits/${famille}/${r.ref}`}
                        className="inline-flex h-8 w-8 items-center justify-center rounded-full border border-brume text-encre transition-all group-hover:border-jaune group-hover:bg-jaune"
                        aria-label={`Voir la fiche ${r.nom}`}
                      >
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none">
                          <path d="M5 12h14M13 6l6 6-6 6" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round" />
                        </svg>
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* ---- Cartes (mobile) ---- */}
          <ul className="grid gap-3 md:hidden">
            {filtres.map((r) => (
              <li key={r.ref}>
                <Link
                  href={`/produits/${famille}/${r.ref}`}
                  className="flex items-center justify-between gap-4 rounded-xl border border-brume bg-white p-4"
                >
                  <span className="min-w-0">
                    <span className="h-title block truncate font-semibold text-encre">{r.nom}</span>
                    <span className="mt-0.5 block font-mono text-xs text-soft">
                      {r.dims} · {r.kg.toLocaleString("fr-BE", { minimumFractionDigits: 2, maximumFractionDigits: 2 })} {r.unitePoids}
                    </span>
                  </span>
                  <span className="shrink-0 text-right">
                    <span className="h-title block font-bold tabular-nums text-encre">{r.prixTexte}</span>
                    <span className="font-body text-[11px] text-soft">{r.uniteCourte.slice(1)}</span>
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
