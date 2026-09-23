import type { Metadata } from "next";
import Link from "next/link";
import PageHeader from "@/components/ui/PageHeader";
import CtaBand from "@/components/sections/CtaBand";
import Reveal from "@/components/fx/Reveal";
import Tilt from "@/components/fx/Tilt";
import { productArt, ArtPoutrelle } from "@/components/art/ProductArt";
import {
  univers,
  noeuds,
  produitsSous,
  prixMini,
  formatPrix,
  totalProduits,
} from "@/lib/catalogue";
import { titre, description } from "@/lib/seo";
import { catalogueActif } from "@/lib/catalogue-visuel";

export const metadata: Metadata = {
  title: titre(`Catalogue acier — ${totalProduits} produits en stock`),
  description: description(
    `${totalProduits} produits en 6 univers : acier, inox, aluminium, toiture & bardage, ` +
      "jardin & clôture, quincaillerie. Poids et prix affichés, découpe aux cotes."
  ),
  alternates: { canonical: "/produits" },
};

export default function CataloguePage() {
  const nbCategories = Object.keys(noeuds).length;

  return (
    <main>
      <PageHeader
        surtitre="Catalogue"
        titre={
          <>
            {totalProduits} produits, <span className="mark-jaune">tous en stock</span>
          </>
        }
        intro={`Six univers, ${nbCategories} catégories, un poids et un prix affichés sur chaque fiche. Tout se coupe aux cotes exactes — vous ne payez que la longueur utile.`}
      />

      <section className="border-b border-brume bg-white py-10">
        <div className="container-g">
          <dl className="grid grid-cols-2 gap-6 md:grid-cols-4">
            {[
              [totalProduits.toString(), "produits en stock"],
              [univers.length.toString(), "univers"],
              ["4", "dépôts de retrait"],
              ["24 h", "pour votre devis"],
            ].map(([v, l]) => (
              <div key={l}>
                <dt className="sr-only">{l}</dt>
                <dd>
                  <span className="h-title block text-3xl font-bold tabular-nums text-encre md:text-4xl">{v}</span>
                  <span className="mt-1 block font-body text-sm text-soft">{l}</span>
                </dd>
              </div>
            ))}
          </dl>
        </div>
      </section>

      {catalogueActif && (
        <section className="border-b border-brume bg-white py-6">
          <div className="container-g flex flex-wrap items-center justify-between gap-4">
            <p className="max-w-xl font-body text-sm text-soft">
              Le catalogue en images : chaque famille avec sa photo studio, chaque variante avec son rendu 3D
              aux cotes, chapitre par chapitre.
            </p>
            <Link href="/catalogue" prefetch={false} className="btn-ghost">Feuilleter le catalogue</Link>
          </div>
        </section>
      )}

      <section className="bg-white py-16 md:py-24">
        <div className="container-g">
          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {univers.map((u, i) => {
              const Art = productArt[u.art] ?? ArtPoutrelle;
              const n = produitsSous(`/${u.slug}`).length;
              const mini = prixMini(`/${u.slug}`);
              const familles = u.enfants.map((c) => noeuds[c]).filter(Boolean);
              return (
                <Reveal key={u.slug} delay={(i % 3) * 0.07}>
                  <Tilt className="group h-full" intensity={6}>
                    <Link
                      href={`/${u.slug}`}
                      className="lift flex h-full flex-col overflow-hidden rounded-2xl border border-brume bg-white"
                    >
                      <div className="shine relative aspect-[4/3] overflow-hidden bg-nuage">
                        <div className="grid-industrie absolute inset-0 opacity-70" />
                        <Art className="absolute inset-0 h-full w-full transition-transform duration-700 group-hover:scale-[1.07]" />
                        <span className="tag-stock absolute left-4 top-4 z-10">En stock</span>
                      </div>
                      <div className="flex flex-1 flex-col p-6" style={{ transform: "translateZ(40px)" }}>
                        <h2 className="h-title text-xl font-semibold text-encre">{u.nom}</h2>
                        <p className="mt-1.5 font-body text-sm text-soft">{u.accroche}</p>
                        <ul className="mt-4 flex flex-wrap gap-1.5">
                          {familles.map((f) => (
                            <li key={f.chemin} className="rounded-full bg-nuage px-2.5 py-1 font-body text-[11px] text-soft">
                              {f.nom}
                            </li>
                          ))}
                        </ul>
                        <div className="mt-5 flex items-end justify-between border-t border-brume pt-4">
                          <div>
                            <span className="block font-mono text-xs text-soft">{n} produits</span>
                            {mini !== null && (
                              <span className="h-title mt-0.5 block text-sm font-semibold tabular-nums text-encre">
                                dès {formatPrix(mini)}
                              </span>
                            )}
                          </div>
                          <span className="glow-jaune flex h-10 w-10 items-center justify-center rounded-full bg-jaune text-encre transition-transform duration-300 group-hover:rotate-45">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                              <path d="M7 17L17 7M9 7h8v8" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round" />
                            </svg>
                          </span>
                        </div>
                      </div>
                    </Link>
                  </Tilt>
                </Reveal>
              );
            })}
          </div>
        </div>
      </section>

      <CtaBand />
    </main>
  );
}
