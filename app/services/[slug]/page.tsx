import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import CtaBand from "@/components/sections/CtaBand";
import Reveal from "@/components/fx/Reveal";
import { ArtDecoupe, ArtAtelier, ArtStock } from "@/components/art/ProductArt";
import { servicesDetail, serviceBySlug } from "@/lib/edito";
import { titre, description } from "@/lib/seo";

type Params = { slug: string };

const visuels: Record<string, (p: { className?: string }) => JSX.Element> = {
  decoupe: ArtDecoupe,
  pliage: ArtAtelier,
  percage: ArtAtelier,
  "conseil-technique": ArtStock,
  "click-and-collect": ArtStock,
  transformation: ArtAtelier,
};

export function generateStaticParams() {
  return servicesDetail.map((s) => ({ slug: s.slug }));
}

export async function generateMetadata({ params }: { params: Promise<Params> }): Promise<Metadata> {
  const { slug } = await params;
  const s = serviceBySlug(slug);
  if (!s) return { title: "Service introuvable | Aciers Grosjean" };
  return {
    title: titre(s.titreSeo),
    description: description(s.descSeo),
    alternates: { canonical: `/services/${s.slug}` },
  };
}

export default async function ServicePage({ params }: { params: Promise<Params> }) {
  const { slug } = await params;
  const s = serviceBySlug(slug);
  if (!s) notFound();

  const Art = visuels[s.slug] ?? ArtAtelier;
  const autres = servicesDetail.filter((x) => x.slug !== s.slug);

  return (
    <main>
      <header className="relative overflow-hidden border-b border-brume bg-nuage pt-32 md:pt-40">
        <div className="grid-industrie pointer-events-none absolute inset-0 opacity-60" />
        <div className="container-g relative pb-14 md:pb-20">
          <nav className="mb-5 font-body text-xs text-soft">
            <Link href="/" className="lien-tactile hover:text-encre">Accueil</Link>
            <span className="mx-2 text-brume">/</span>
            <Link href="/services" className="lien-tactile hover:text-encre">Services</Link>
            <span className="mx-2 text-brume">/</span>
            <span className="text-encre">{s.nom}</span>
          </nav>
          <h1 className="h-display max-w-3xl text-4xl md:text-6xl">{s.accroche}</h1>
          <p className="mt-5 max-w-2xl font-body text-lg text-soft">{s.intro}</p>
        </div>
      </header>

      <section className="bg-white py-14 md:py-20">
        <div className="container-g grid gap-12 lg:grid-cols-[1fr_20rem] lg:gap-16">
          <div>
            <div className="group relative mb-12 aspect-[16/9] overflow-hidden rounded-2xl border border-brume bg-nuage">
              <div className="grid-industrie absolute inset-0 opacity-70" />
              <div className="shine absolute inset-0">
                <Art className="h-full w-full transition-transform duration-700 group-hover:scale-105" />
              </div>
            </div>

            <div className="space-y-10">
              {s.points.map((p, i) => (
                <Reveal key={p.titre} delay={i * 0.06}>
                  <div className="flex gap-6">
                    <span className="h-title shrink-0 font-mono text-sm text-soft">
                      {String(i + 1).padStart(2, "0")}
                    </span>
                    <div>
                      <h2 className="h-title text-xl font-semibold text-encre">{p.titre}</h2>
                      <p className="mt-2 max-w-xl font-body text-lg leading-relaxed text-soft">
                        {p.texte}
                      </p>
                    </div>
                  </div>
                </Reveal>
              ))}
            </div>
          </div>

          {/* fiche technique du service */}
          <aside className="lg:sticky lg:top-28 lg:self-start">
            <div className="rounded-2xl border border-brume bg-nuage p-6">
              <h2 className="h-title text-sm font-semibold uppercase tracking-[0.14em] text-soft">
                Caractéristiques
              </h2>
              <dl className="mt-4 divide-y divide-brume border-y border-brume">
                {s.specs.map((c) => (
                  <div key={c.label} className="py-3">
                    <dt className="font-body text-xs uppercase tracking-[0.1em] text-soft">{c.label}</dt>
                    <dd className="mt-0.5 font-body text-sm text-encre">{c.valeur}</dd>
                  </div>
                ))}
              </dl>

              <div className="mt-5 grid grid-cols-2 gap-3">
                <div className="rounded-xl bg-white p-3">
                  <span className="block font-body text-[11px] uppercase tracking-[0.1em] text-soft">Délai</span>
                  <span className="h-title mt-0.5 block text-sm font-semibold text-encre">{s.delai}</span>
                </div>
                <div className="rounded-xl bg-white p-3">
                  <span className="block font-body text-[11px] uppercase tracking-[0.1em] text-soft">Tarif</span>
                  <span className="h-title mt-0.5 block text-sm font-semibold text-encre">{s.prix}</span>
                </div>
              </div>

              <Link href="/devis" className="btn-cta mt-6 w-full justify-center">
                Demander ce service
              </Link>
            </div>
          </aside>
        </div>
      </section>

      <section className="border-t border-brume bg-nuage py-16">
        <div className="container-g">
          <h2 className="h-display text-2xl md:text-3xl">Les autres services</h2>
          <div className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-5">
            {autres.map((a, i) => (
              <Reveal key={a.slug} delay={i * 0.05}>
                <Link
                  href={`/services/${a.slug}`}
                  className="group flex h-full flex-col justify-between rounded-2xl border border-brume bg-white p-5 transition-all duration-300 hover:-translate-y-1 hover:shadow-[0_24px_56px_-34px_rgba(51,54,66,.5)]"
                >
                  <h3 className="h-title font-semibold leading-snug text-encre">{a.nom}</h3>
                  <span className="mt-4 font-body text-xs text-soft">{a.prix}</span>
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
