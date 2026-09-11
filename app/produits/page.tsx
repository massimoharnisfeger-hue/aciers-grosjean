import type { Metadata } from "next";
import Link from "next/link";
import PageHeader from "@/components/ui/PageHeader";
import CtaBand from "@/components/sections/CtaBand";
import Reveal from "@/components/fx/Reveal";
import Tilt from "@/components/fx/Tilt";
import { productArt, ArtPoutrelle } from "@/components/art/ProductArt";
import { familles, matieres, totalRefs, prixMini } from "@/lib/catalogue";

export const metadata: Metadata = {
  title: `Catalogue acier — ${totalRefs} références en stock, coupées sur mesure | Aciers Grosjean`,
  description: `${totalRefs} références en stock réparties en ${familles.length} familles : poutrelles IPE/HEA/HEB, cornières, plats, tubes, tôles, treillis, corten, inox, aluminium. Prix au mètre affichés, découpe aux cotes, retrait le jour même.`,
  alternates: { canonical: "/produits" },
};

export default function CataloguePage() {
  return (
    <main>
      <PageHeader
        surtitre="Catalogue"
        titre={
          <>
            {totalRefs} références, <span className="mark-jaune">toutes en stock</span>
          </>
        }
        intro={`${familles.length} familles, ${matieres.length} matières, et un prix au mètre affiché sur chaque fiche. Tout se coupe aux cotes exactes — vous ne payez que la longueur utile.`}
      />

      {/* chiffres du catalogue */}
      <section className="border-b border-brume bg-white py-10">
        <div className="container-g">
          <dl className="grid grid-cols-2 gap-6 md:grid-cols-4">
            {[
              [totalRefs.toString(), "références en stock"],
              [familles.length.toString(), "familles produits"],
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

      {/* familles */}
      <section className="bg-white py-16 md:py-24">
        <div className="container-g">
          <Reveal className="mb-10 max-w-2xl">
            <span className="font-body text-xs uppercase tracking-[0.2em] text-soft">Par famille</span>
            <h2 className="h-display mt-3 text-3xl md:text-4xl">
              Vous savez ce que vous cherchez
            </h2>
            <p className="mt-4 font-body text-soft">
              Chaque famille donne accès au tableau complet des sections, filtrable par série,
              par cote ou par usage.
            </p>
          </Reveal>

          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {familles.map((f, i) => {
              const Art = productArt[f.art] ?? ArtPoutrelle;
              const mini = prixMini(f);
              return (
                <Reveal key={f.slug} delay={(i % 3) * 0.07}>
                  <Tilt className="group h-full" intensity={6}>
                    <Link
                      href={`/produits/${f.slug}`}
                      className="lift flex h-full flex-col overflow-hidden rounded-2xl border border-brume bg-white"
                    >
                      <div className="shine relative aspect-[4/3] overflow-hidden bg-nuage">
                        <div className="grid-industrie absolute inset-0 opacity-70" />
                        <Art className="absolute inset-0 h-full w-full transition-transform duration-700 group-hover:scale-[1.07]" />
                        <span className="tag-stock absolute left-4 top-4 z-10">En stock</span>
                      </div>
                      <div className="flex flex-1 flex-col p-6" style={{ transform: "translateZ(40px)" }}>
                        <h3 className="h-title text-xl font-semibold text-encre">{f.nom}</h3>
                        <p className="mt-1.5 flex-1 font-body text-sm text-soft">{f.accroche}</p>
                        <div className="mt-5 flex items-end justify-between border-t border-brume pt-4">
                          <div>
                            <span className="block font-mono text-xs text-soft">
                              {f.refs.length} référence{f.refs.length > 1 ? "s" : ""}
                            </span>
                            {mini && (
                              <span className="h-title mt-0.5 block text-sm font-semibold tabular-nums text-encre">
                                {mini.texte}
                              </span>
                            )}
                          </div>
                          <span className="glow-jaune flex h-10 w-10 items-center justify-center rounded-full bg-jaune text-encre transition-transform duration-300 group-hover:rotate-45">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
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

      {/* matières */}
      <section className="border-t border-brume bg-nuage py-16 md:py-24">
        <div className="container-g">
          <Reveal className="mb-10 max-w-2xl">
            <span className="font-body text-xs uppercase tracking-[0.2em] text-soft">Par matière</span>
            <h2 className="h-display mt-3 text-3xl md:text-4xl">
              Vous hésitez encore sur <span className="mark-jaune">la matière</span>
            </h2>
            <p className="mt-4 font-body text-soft">
              C'est la décision qui coûte le plus cher quand on se trompe. Cinq pages pour
              trancher sans jargon — exposition, budget, entretien.
            </p>
          </Reveal>

          <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
            {matieres.map((m, i) => (
              <Reveal key={m.slug} delay={(i % 3) * 0.07}>
                <Link
                  href={`/materiaux/${m.slug}`}
                  className="group flex h-full flex-col rounded-2xl border border-brume bg-white p-7 transition-all duration-300 hover:-translate-y-1 hover:shadow-[0_26px_60px_-36px_rgba(51,54,66,.5)]"
                >
                  <h3 className="h-title text-2xl font-semibold text-encre">{m.nom}</h3>
                  <p className="mt-2 flex-1 font-body text-sm leading-relaxed text-soft">{m.accroche}</p>
                  <span className="mt-5 inline-flex items-center gap-2 font-body text-sm font-medium text-encre">
                    Comprendre la matière
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
