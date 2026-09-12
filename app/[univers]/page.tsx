import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import CtaBand from "@/components/sections/CtaBand";
import Reveal from "@/components/fx/Reveal";
import Tilt from "@/components/fx/Tilt";
import FilAriane from "@/components/ui/FilAriane";
import { productArt, ArtPoutrelle } from "@/components/art/ProductArt";
import {
  univers as tousUnivers,
  universBySlug,
  noeuds,
  produitsSous,
  prixMini,
  formatPrix,
} from "@/lib/catalogue";
import { artPour } from "@/lib/visuels";
import { titre, description } from "@/lib/seo";

type Params = { univers: string };

export const dynamicParams = false;

export function generateStaticParams() {
  return tousUnivers.map((u) => ({ univers: u.slug }));
}

export async function generateMetadata({ params }: { params: Promise<Params> }): Promise<Metadata> {
  const { univers } = await params;
  const u = universBySlug(univers);
  if (!u) return { title: "Univers introuvable | Aciers Grosjean" };
  return {
    title: titre(u.titreSeo),
    description: description(u.descSeo),
    alternates: { canonical: `/${u.slug}` },
  };
}

export default async function UniversPage({ params }: { params: Promise<Params> }) {
  const { univers } = await params;
  const u = universBySlug(univers);
  if (!u) notFound();

  const Art = productArt[u.art] ?? ArtPoutrelle;
  const total = produitsSous(`/${u.slug}`).length;
  const mini = prixMini(`/${u.slug}`);
  const familles = u.enfants.map((c) => noeuds[c]).filter(Boolean);

  return (
    <main>
      <header className="relative overflow-hidden border-b border-brume bg-nuage pt-32 md:pt-40">
        <div className="grid-industrie pointer-events-none absolute inset-0 opacity-60" />
        <div className="pointer-events-none absolute -right-16 top-16 h-64 w-64 rounded-full bg-jaune/10 blur-[110px]" />
        <div className="container-g relative pb-14 md:pb-20">
          <div className="mb-5">
            <FilAriane items={[{ label: "Catalogue", href: "/produits" }, { label: u.nom }]} />
          </div>
          <h1 className="h-display max-w-3xl text-4xl md:text-6xl">{u.accroche}</h1>
          <p className="mt-5 max-w-2xl font-body text-lg text-soft">{u.intro}</p>

          <dl className="mt-9 grid max-w-xl grid-cols-2 gap-6 sm:grid-cols-4">
            {[
              [total.toString(), "produits"],
              [familles.length.toString(), "familles"],
              [mini !== null ? formatPrix(mini) : "—", "prix d'entrée"],
              ["Jour même", "retrait"],
            ].map(([v, l]) => (
              <div key={l}>
                <dt className="sr-only">{l}</dt>
                <dd>
                  <span className="h-title block text-2xl font-bold tabular-nums text-encre">{v}</span>
                  <span className="mt-0.5 block font-body text-xs uppercase tracking-[0.12em] text-soft">{l}</span>
                </dd>
              </div>
            ))}
          </dl>

          <div className="mt-8 flex flex-wrap gap-3">
            <Link href="/devis" className="btn-cta">Demander un devis</Link>
            <Link href="/services/decoupe" className="btn-ghost">La découpe sur mesure</Link>
          </div>
        </div>
      </header>

      <section className="bg-white py-16 md:py-24">
        <div className="container-g">
          <h2 className="h-display mb-10 text-2xl md:text-3xl">Les familles</h2>

          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {familles.map((f, i) => {
              const FArt = productArt[artPour(f.chemin, u.art)] ?? Art;
              const n = produitsSous(f.chemin).length;
              const min = prixMini(f.chemin);
              const sous = f.enfants.map((c) => noeuds[c]).filter(Boolean);
              return (
                <Reveal key={f.chemin} delay={(i % 3) * 0.07}>
                  <Tilt className="group h-full" intensity={6}>
                    <Link
                      href={f.chemin}
                      className="lift flex h-full flex-col overflow-hidden rounded-2xl border border-brume bg-white"
                    >
                      <div className="shine relative aspect-[4/3] overflow-hidden bg-nuage">
                        <div className="grid-industrie absolute inset-0 opacity-70" />
                        <FArt className="absolute inset-0 h-full w-full transition-transform duration-700 group-hover:scale-[1.07]" />
                        <span className="tag-stock absolute left-4 top-4 z-10">En stock</span>
                      </div>
                      <div className="flex flex-1 flex-col p-6" style={{ transform: "translateZ(40px)" }}>
                        <h3 className="h-title text-xl font-semibold text-encre">{f.nom}</h3>
                        {f.accroche && (
                          <p className="mt-1.5 font-body text-sm text-soft">{f.accroche}</p>
                        )}
                        {sous.length > 0 && (
                          <ul className="mt-4 flex flex-wrap gap-1.5">
                            {sous.slice(0, 5).map((s) => (
                              <li key={s.chemin} className="rounded-full bg-nuage px-2.5 py-1 font-body text-[11px] text-soft">
                                {s.nom}
                              </li>
                            ))}
                            {sous.length > 5 && (
                              <li className="px-1 py-1 font-body text-[11px] text-soft">+{sous.length - 5}</li>
                            )}
                          </ul>
                        )}
                        <div className="mt-auto flex items-end justify-between border-t border-brume pt-4 [margin-top:1.25rem]">
                          <div>
                            <span className="block font-mono text-xs text-soft">{n} produits</span>
                            {min !== null && (
                              <span className="h-title mt-0.5 block text-sm font-semibold tabular-nums text-encre">
                                dès {formatPrix(min)}
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

      <section className="border-t border-brume bg-nuage py-14">
        <div className="container-g">
          <h2 className="h-title text-sm font-semibold uppercase tracking-[0.14em] text-soft">
            Les autres univers
          </h2>
          <div className="mt-5 flex flex-wrap gap-3">
            {tousUnivers
              .filter((x) => x.slug !== u.slug)
              .map((x) => (
                <Link
                  key={x.slug}
                  href={`/${x.slug}`}
                  className="rounded-full border border-brume bg-white px-4 py-2 font-body text-sm text-encre transition-colors hover:border-encre"
                >
                  {x.nom}
                </Link>
              ))}
          </div>
        </div>
      </section>

      <CtaBand />
    </main>
  );
}
