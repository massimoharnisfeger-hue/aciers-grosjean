import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import CtaBand from "@/components/sections/CtaBand";
import Reveal from "@/components/fx/Reveal";
import { ArtStock } from "@/components/art/ProductArt";
import { depotsDetail, depotBySlug, servicesDetail } from "@/lib/edito";
import { univers } from "@/lib/catalogue";
import { titre, description } from "@/lib/seo";
import { lienTel } from "@/lib/content";

type Params = { slug: string };

export function generateStaticParams() {
  return depotsDetail.map((d) => ({ slug: d.slug }));
}

export async function generateMetadata({ params }: { params: Promise<Params> }): Promise<Metadata> {
  const { slug } = await params;
  const d = depotBySlug(slug);
  if (!d) return { title: "Dépôt introuvable | Aciers Grosjean" };
  return {
    title: titre(`Acier à ${d.ville} — dépôt, découpe et retrait le jour même`),
    description: description(
      `Notre dépôt de ${d.ville} (${d.region}) : ${d.equipements.slice(0, 3).join(", ").toLowerCase()}. ` +
        "Horaires, coordonnées et communes desservies."
    ),
    alternates: { canonical: `/depots/${d.slug}` },
  };
}

export default async function DepotPage({ params }: { params: Promise<Params> }) {
  const { slug } = await params;
  const d = depotBySlug(slug);
  if (!d) notFound();

  const autres = depotsDetail.filter((x) => x.slug !== d.slug);

  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "HardwareStore",
    name: `Aciers Grosjean — ${d.ville}`,
    description: d.intro,
    telephone: d.tel,
    address: {
      "@type": "PostalAddress",
      streetAddress: d.adresse,
      addressLocality: d.ville,
      addressRegion: d.region,
      addressCountry: d.pays === "France" ? "FR" : "BE",
    },
    areaServed: d.dessert,
  };

  return (
    <main>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }} />

      <header className="relative overflow-hidden border-b border-brume bg-nuage pt-32 md:pt-40">
        <div className="grid-industrie pointer-events-none absolute inset-0 opacity-60" />
        <div className="container-g relative pb-14 md:pb-20">
          <nav className="mb-5 font-body text-xs text-soft">
            <Link href="/" className="hover:text-encre">Accueil</Link>
            <span className="mx-2 text-brume">/</span>
            <Link href="/depots" className="hover:text-encre">Dépôts</Link>
            <span className="mx-2 text-brume">/</span>
            <span className="text-encre">{d.ville}</span>
          </nav>
          <h1 className="h-display max-w-3xl text-4xl md:text-6xl">
            Votre acier à <span className="mark-jaune">{d.ville}</span>
          </h1>
          <p className="mt-5 max-w-2xl font-body text-lg text-soft">{d.intro}</p>
        </div>
      </header>

      <section className="bg-white py-14 md:py-20">
        <div className="container-g grid gap-12 lg:grid-cols-[1fr_20rem] lg:gap-16">
          <div>
            <div className="group relative mb-12 aspect-[16/9] overflow-hidden rounded-2xl border border-brume bg-nuage">
              <div className="grid-industrie absolute inset-0 opacity-70" />
              <div className="shine absolute inset-0">
                <ArtStock className="h-full w-full transition-transform duration-700 group-hover:scale-105" />
              </div>
              <span className="tag-stock absolute left-5 top-5">Retrait le jour même</span>
            </div>

            <Reveal>
              <h2 className="h-display text-2xl md:text-3xl">Sur place</h2>
              <ul className="mt-6 grid gap-3 sm:grid-cols-2">
                {d.equipements.map((e) => (
                  <li
                    key={e}
                    className="flex items-center gap-3 rounded-xl border border-brume bg-white px-4 py-3.5 font-body text-encre"
                  >
                    <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-jaune">
                      <svg width="13" height="13" viewBox="0 0 24 24" fill="none">
                        <path d="M5 13l4 4L19 7" stroke="#333642" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" />
                      </svg>
                    </span>
                    {e}
                  </li>
                ))}
              </ul>
            </Reveal>

            <Reveal delay={0.06}>
              <h2 className="h-display mt-14 text-2xl md:text-3xl">Communes desservies</h2>
              <p className="mt-3 max-w-xl font-body text-soft">
                Les clients de ce dépôt viennent principalement de ces communes. Si la vôtre n’y
                est pas, appelez : un autre dépôt est peut-être plus proche.
              </p>
              <ul className="mt-5 flex flex-wrap gap-2">
                {d.dessert.map((c) => (
                  <li
                    key={c}
                    className="rounded-full border border-brume bg-nuage px-3.5 py-1.5 font-body text-sm text-encre"
                  >
                    {c}
                  </li>
                ))}
              </ul>
            </Reveal>

            <Reveal delay={0.06}>
              <h2 className="h-display mt-14 text-2xl md:text-3xl">Ce qu’on y trouve</h2>
              <div className="mt-6 flex flex-wrap gap-3">
                {univers.map((x) => (
                  <Link
                    key={x.slug}
                    href={`/${x.slug}`}
                    className="rounded-full border border-brume px-4 py-2 font-body text-sm text-encre transition-colors hover:border-encre hover:bg-nuage"
                  >
                    {x.nom}
                  </Link>
                ))}
              </div>
            </Reveal>
          </div>

          {/* carte d'identité du dépôt */}
          <aside className="lg:sticky lg:top-28 lg:self-start">
            <div className="rounded-2xl border border-brume bg-nuage p-6">
              <h2 className="h-title text-sm font-semibold uppercase tracking-[0.14em] text-soft">
                Informations pratiques
              </h2>

              <dl className="mt-4 divide-y divide-brume border-y border-brume">
                <div className="py-3">
                  <dt className="font-body text-xs uppercase tracking-[0.1em] text-soft">Adresse</dt>
                  <dd className="mt-0.5 font-body text-sm text-encre">{d.adresse}</dd>
                </div>
                <div className="py-3">
                  <dt className="font-body text-xs uppercase tracking-[0.1em] text-soft">Téléphone</dt>
                  <dd className="mt-0.5">
                    <a href={lienTel(d.tel)} className="font-mono text-sm text-encre hover:text-jaune">
                      {d.tel}
                    </a>
                  </dd>
                </div>
                <div className="py-3">
                  <dt className="font-body text-xs uppercase tracking-[0.1em] text-soft">Horaires</dt>
                  <dd className="mt-1 space-y-1">
                    {d.horaires.map((h) => (
                      <span key={h.jours} className="flex justify-between gap-3 font-body text-sm">
                        <span className="text-soft">{h.jours}</span>
                        <span className="font-mono text-encre">{h.heures}</span>
                      </span>
                    ))}
                  </dd>
                </div>
              </dl>

              <Link href="/devis" className="btn-cta mt-6 w-full justify-center">
                Préparer ma commande
              </Link>
              <p className="mt-3 text-center font-body text-xs text-soft">
                Commandez à l’avance, on prépare — vous ne faites que charger.
              </p>
            </div>

            <div className="mt-5 rounded-2xl border border-brume p-6">
              <h2 className="h-title text-sm font-semibold uppercase tracking-[0.14em] text-soft">
                Services disponibles ici
              </h2>
              <ul className="mt-4 space-y-2">
                {servicesDetail.slice(0, 4).map((s) => (
                  <li key={s.slug}>
                    <Link
                      href={`/services/${s.slug}`}
                      className="font-body text-sm text-encre hover:text-jaune"
                    >
                      {s.nom}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          </aside>
        </div>
      </section>

      <section className="border-t border-brume bg-nuage py-16">
        <div className="container-g">
          <h2 className="h-display text-2xl md:text-3xl">Les autres dépôts</h2>
          <div className="mt-8 grid gap-5 sm:grid-cols-3">
            {autres.map((a, i) => (
              <Reveal key={a.slug} delay={i * 0.07}>
                <Link
                  href={`/depots/${a.slug}`}
                  className="group flex h-full flex-col justify-between rounded-2xl border border-brume bg-white p-6 transition-all duration-300 hover:-translate-y-1 hover:shadow-[0_26px_60px_-34px_rgba(51,54,66,.5)]"
                >
                  <div>
                    <h3 className="h-title text-lg font-semibold text-encre">{a.ville}</h3>
                    <p className="mt-1 font-body text-xs text-soft">{a.region} · {a.pays}</p>
                  </div>
                  <span className="mt-5 font-mono text-xs text-soft">{a.horaires[0].heures}</span>
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
