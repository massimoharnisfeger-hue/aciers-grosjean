import type { Metadata } from "next";
import Link from "next/link";
import PageHeader from "@/components/ui/PageHeader";
import CtaBand from "@/components/sections/CtaBand";
import Reveal from "@/components/fx/Reveal";
import { productArt, ArtPoutrelle } from "@/components/art/ProductArt";
import { familles, matieres } from "@/lib/catalogue";

export const metadata: Metadata = {
  title: "Catalogue acier — Poutrelles, cornières, tubes, tôles | Aciers Grosjean",
  description:
    "Plus de 500 références en stock : poutrelles IPE/HEA/HEB, cornières, plats, tubes, tôles, poteaux de clôture, visserie. Découpe sur mesure, retrait le jour même.",
};

export default function CataloguePage() {
  return (
    <main>
      <PageHeader
        surtitre="Produits"
        titre={<>Le catalogue <span className="mark-jaune">acier</span></>}
        intro="Sept familles, plus de 500 références en stock. Toutes disponibles à la découpe aux cotes exactes."
      />

      {/* familles */}
      <section className="bg-white py-16 md:py-24">
        <div className="container-g">
          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {familles.map((f, i) => {
              const Art = productArt[f.art] ?? ArtPoutrelle;
              return (
                <Reveal key={f.slug} delay={(i % 3) * 0.07}>
                  <Link
                    href={`/produits/${f.slug}`}
                    className="group flex h-full flex-col overflow-hidden rounded-2xl border border-brume bg-white transition-all duration-300 hover:-translate-y-1 hover:border-encre/20 hover:shadow-[0_30px_70px_-38px_rgba(51,54,66,.55)]"
                  >
                    <div className="shine relative aspect-[4/3] overflow-hidden bg-nuage">
                      <div className="grid-industrie absolute inset-0 opacity-70" />
                      <Art className="absolute inset-0 h-full w-full transition-transform duration-700 group-hover:scale-[1.07]" />
                    </div>
                    <div className="flex flex-1 flex-col p-6">
                      <h2 className="h-title text-xl font-semibold text-encre">{f.nom}</h2>
                      <p className="mt-1 font-body text-sm text-soft">{f.accroche}</p>
                      <div className="mt-5 flex items-center justify-between border-t border-brume pt-4">
                        <span className="font-mono text-xs text-soft">
                          {f.refs.length} référence{f.refs.length > 1 ? "s" : ""}
                        </span>
                        <span className="flex h-9 w-9 items-center justify-center rounded-full bg-jaune text-encre transition-transform duration-300 group-hover:rotate-45">
                          <svg width="15" height="15" viewBox="0 0 24 24" fill="none">
                            <path d="M7 17L17 7M9 7h8v8" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round" />
                          </svg>
                        </span>
                      </div>
                    </div>
                  </Link>
                </Reveal>
              );
            })}
          </div>
        </div>
      </section>

      {/* matières */}
      <section className="border-t border-brume bg-nuage py-16 md:py-24">
        <div className="container-g">
          <Reveal className="mb-10 max-w-2xl">
            <span className="font-body text-xs uppercase tracking-[0.2em] text-soft">Par matière</span>
            <h2 className="h-display mt-3 text-3xl md:text-4xl">
              Acier, inox ou <span className="mark-jaune">aluminium</span> ?
            </h2>
            <p className="mt-4 font-body text-soft">
              Le bon choix dépend de l'exposition, du poids et du budget. Voici de quoi trancher
              sans jargon.
            </p>
          </Reveal>
          <div className="grid gap-5 md:grid-cols-3">
            {matieres.map((m, i) => (
              <Reveal key={m.slug} delay={i * 0.08}>
                <Link
                  href={`/materiaux/${m.slug}`}
                  className="group flex h-full flex-col rounded-2xl border border-brume bg-white p-7 transition-all duration-300 hover:-translate-y-1 hover:shadow-[0_26px_60px_-36px_rgba(51,54,66,.5)]"
                >
                  <h3 className="h-title text-2xl font-semibold text-encre">{m.nom}</h3>
                  <p className="mt-2 flex-1 font-body text-sm leading-relaxed text-soft">{m.accroche}</p>
                  <span className="mt-5 inline-flex items-center gap-2 font-body text-sm font-medium text-encre">
                    En savoir plus
                    <span className="h-px w-6 bg-jaune transition-all duration-300 group-hover:w-10" />
                  </span>
                </Link>
              </Reveal>
            ))}
          </div>
        </div>
      </section>

      <CtaBand />
    </main>
  );
}
