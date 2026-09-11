import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import PageHeader from "@/components/ui/PageHeader";
import CtaBand from "@/components/sections/CtaBand";
import Reveal from "@/components/fx/Reveal";
import { productArt, ArtPoutrelle } from "@/components/art/ProductArt";
import { familles, familleBySlug } from "@/lib/catalogue";

type Params = { famille: string };

export function generateStaticParams() {
  return familles.map((f) => ({ famille: f.slug }));
}

export async function generateMetadata({ params }: { params: Promise<Params> }): Promise<Metadata> {
  const { famille } = await params;
  const f = familleBySlug(famille);
  if (!f) return { title: "Famille introuvable | Aciers Grosjean" };
  return {
    title: `${f.nom} — ${f.accroche} | Aciers Grosjean`,
    description: `${f.intro} En stock, découpe sur mesure, retrait le jour même dans nos 4 dépôts.`,
  };
}

export default async function FamillePage({ params }: { params: Promise<Params> }) {
  const { famille } = await params;
  const f = familleBySlug(famille);
  if (!f) notFound();
  const Art = productArt[f.art] ?? ArtPoutrelle;

  return (
    <main>
      <PageHeader
        surtitre={f.nom}
        titre={<>{f.accroche}</>}
        intro={f.intro}
      />

      <section className="bg-white py-16 md:py-24">
        <div className="container-g">
          <div className="mb-12 grid items-center gap-10 md:grid-cols-[1fr_.9fr]">
            <Reveal>
              <h2 className="h-display text-2xl md:text-3xl">Les références en stock</h2>
              <p className="mt-3 max-w-md font-body text-soft">
                Toutes disponibles à la découpe aux cotes. Les prix affichés sont indicatifs, hors
                TVA, et dégressifs selon la quantité — demandez votre tarif exact.
              </p>
            </Reveal>
            <Reveal delay={0.08}>
              <div className="group relative aspect-[4/3] overflow-hidden rounded-2xl border border-brume bg-nuage">
                <div className="grid-industrie absolute inset-0 opacity-70" />
                <div className="shine absolute inset-0">
                  <Art className="h-full w-full transition-transform duration-700 group-hover:scale-105" />
                </div>
              </div>
            </Reveal>
          </div>

          <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
            {f.refs.map((r, i) => (
              <Reveal key={r.ref} delay={(i % 3) * 0.07}>
                <Link
                  href={`/produits/${f.slug}/${r.ref}`}
                  className="group flex h-full flex-col rounded-2xl border border-brume bg-white p-6 transition-all duration-300 hover:-translate-y-1 hover:border-encre/20 hover:shadow-[0_28px_64px_-36px_rgba(51,54,66,.55)]"
                >
                  {r.stock && <span className="tag-stock w-fit">En stock</span>}
                  <h3 className="h-title mt-4 text-lg font-semibold text-encre">{r.nom}</h3>
                  <p className="mt-1 font-mono text-xs text-soft">{r.dims}</p>
                  <p className="mt-3 flex-1 font-body text-sm leading-relaxed text-soft">{r.resume}</p>
                  <div className="mt-5 flex items-end justify-between border-t border-brume pt-4">
                    <div>
                      <span className="h-title text-xl font-bold tabular-nums text-encre">{r.prix}</span>
                      <span className="ml-1.5 font-body text-xs text-soft">{r.unite}</span>
                    </div>
                    <span className="flex h-9 w-9 items-center justify-center rounded-full bg-jaune text-encre transition-transform duration-300 group-hover:rotate-45">
                      <svg width="15" height="15" viewBox="0 0 24 24" fill="none">
                        <path d="M7 17L17 7M9 7h8v8" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round" />
                      </svg>
                    </span>
                  </div>
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
