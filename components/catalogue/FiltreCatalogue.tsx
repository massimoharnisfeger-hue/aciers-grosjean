"use client";

import { useEffect, useId, useState } from "react";
import Link from "next/link";
import { normaliserRecherche, correspondALaRecherche } from "@/lib/recherche-texte";

/**
 * Le filtre d'un chapitre du catalogue.
 *
 * Il n'embarque aucune donnée : les planches sont déjà dans la page, rendues
 * par le serveur, chacune avec son texte de recherche en `data-recherche`. Le
 * filtre lit ces attributs et masque ce qui ne répond pas ; une famille ou une
 * section dont toutes les planches sont masquées disparaît avec elles. Sans
 * JavaScript, tout reste visible.
 *
 * `style.display` plutôt que l'attribut `hidden` : les planches portent des
 * classes d'affichage Tailwind (`flex`), qui l'emporteraient sur `[hidden]`.
 */
export default function FiltreCatalogue({
  total,
  portee,
  exemples,
}: {
  total: number;
  /** `id` de l'élément qui contient les planches à filtrer. */
  portee: string;
  /** Familles réelles du chapitre, proposées comme point de départ. */
  exemples: string[];
}) {
  const [q, setQ] = useState("");
  const [visibles, setVisibles] = useState(total);
  const id = useId();

  useEffect(() => {
    const zone = document.getElementById(portee);
    if (!zone) return;
    const requete = normaliserRecherche(q);
    let n = 0;
    zone.querySelectorAll<HTMLElement>("[data-variante]").forEach((el) => {
      const ok = correspondALaRecherche(el.dataset.recherche ?? "", requete);
      el.style.display = ok ? "" : "none";
      if (ok) n += 1;
    });
    zone.querySelectorAll<HTMLElement>("[data-famille]").forEach((f) => {
      const vivante = Array.from(f.querySelectorAll<HTMLElement>("[data-variante]")).some((v) => v.style.display !== "none");
      f.style.display = vivante ? "" : "none";
    });
    zone.querySelectorAll<HTMLElement>("[data-section]").forEach((s) => {
      const vivante = Array.from(s.querySelectorAll<HTMLElement>("[data-famille]")).some((f) => f.style.display !== "none");
      s.style.display = vivante ? "" : "none";
    });
    setVisibles(n);
  }, [q, portee]);

  return (
    <div className="print:hidden">
      <label htmlFor={id} className="block font-title text-sm font-semibold text-encre">
        Filtrer ce chapitre
      </label>
      <p className="mt-0.5 font-body text-xs text-soft">Un nom, une cote (« 40x40 », « 3 mm »), une famille.</p>
      <div className="relative mt-2 max-w-xl">
        <svg
          className="pointer-events-none absolute left-4 top-1/2 -translate-y-1/2 text-soft"
          width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true"
        >
          <circle cx="11" cy="11" r="7" stroke="currentColor" strokeWidth="2" />
          <path d="M20 20l-3.5-3.5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
        </svg>
        <input
          id={id}
          type="search"
          value={q}
          onChange={(e) => setQ(e.target.value)}
          autoComplete="off"
          className="w-full rounded-xl border border-brume bg-white py-3 pl-11 pr-4 font-body text-base text-encre placeholder:text-soft focus:border-encre focus:outline-none focus:ring-2 focus:ring-jaune"
        />
      </div>
      <p className="mt-2 font-body text-sm text-soft" aria-live="polite">
        {q ? (
          <>
            <strong className="font-mono tabular-nums text-encre">{visibles}</strong> produit{visibles > 1 ? "s" : ""} sur {total} pour « {q} »
          </>
        ) : (
          <>{total} produits dans ce chapitre</>
        )}
      </p>

      {q && visibles === 0 && (
        <div className="mt-4 max-w-xl rounded-2xl border border-dashed border-acier bg-nuage p-6">
          <p className="h-title font-title text-base font-semibold text-encre">Rien dans ce chapitre sous « {q} »</p>
          <p className="mt-2 font-body text-sm leading-relaxed text-soft">
            Essayez une cote plus courte, ou une famille :
          </p>
          <ul className="mt-3 flex flex-wrap gap-2">
            {exemples.map((e) => (
              <li key={e}>
                <button
                  type="button"
                  onClick={() => setQ(e)}
                  className="rounded-full border border-brume bg-white px-3 py-1.5 font-body text-sm text-encre transition-colors hover:border-encre"
                >
                  {e}
                </button>
              </li>
            ))}
          </ul>
          <p className="mt-4 font-body text-sm leading-relaxed text-soft">
            Le produit peut être dans un autre chapitre :{" "}
            <Link href="/recherche" className="lien-tactile font-medium text-encre underline decoration-brume underline-offset-4 hover:decoration-jaune">
              chercher dans tout le site
            </Link>
            , ou{" "}
            <Link href="/devis" className="lien-tactile font-medium text-encre underline decoration-brume underline-offset-4 hover:decoration-jaune">
              décrire votre besoin
            </Link>
            : réponse en 24 h.
          </p>
        </div>
      )}
    </div>
  );
}
