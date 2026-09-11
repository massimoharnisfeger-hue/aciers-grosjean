import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import CtaBand from "@/components/sections/CtaBand";
import Reveal from "@/components/fx/Reveal";
import Calculateur from "@/components/catalogue/Calculateur";
import { productArt, ArtPoutrelle } from "@/components/art/ProductArt";
import { familles, familleBySlug, refBySlug, matiereBySlug } from "@/lib/catalogue";

type Params = { famille: string; ref: string };

export function generateStaticParams() {
  return familles.flatMap((f) => f.refs.map((r) => ({ famille: f.slug, ref: r.ref })));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<Params>;
}): Promise<Metadata> {
  const { famille, ref } = await params;
  const f = familleBySlug(famille);
  const r = refBySlug(famille, ref);
  if (!f || !r) return { title: "Référence introuvable | Aciers Grosjean" };

  const prix = r.prix !== null ? `${r.prixTexte}${r.uniteCourte.slice(1)} — ` : "";
  return {
    title: `${r.nom} (${r.dims}) — ${prix}en stock, coupé sur mesure | Aciers Grosjean`,
    description: `${r.resume} ${
      r.prix !== null ? `${r.prixTexte} ${r.unite}, HTVA.` : "Prix sur devis sous 24 h."
    } Poids ${r.kg} ${r.unitePoids}. Découpe aux cotes, retrait le jour même dans nos 4 dépôts.`,
    alternates: { canonical: `/produits/${f.slug}/${r.ref}` },
  };
}

export default async function FicheProduit({ params }: { params: Promise<Params> }) {
  const { famille, ref } = await params;
  const f = familleBySlug(famille);
  const r = refBySlug(famille, ref);
  if (!f || !r) notFound();

  const Art = productArt[f.art] ?? ArtPoutrelle;
  const matiere = matiereBySlug(r.matiere);

  // Voisines : même série d'abord, puis le reste de la famille.
  const memeSerie = f.refs.filter((x) => x.ref !== r.ref && x.serie === r.serie);
  const autres = f.refs.filter((x) => x.ref !== r.ref && x.serie !== r.serie);
  const voisines = [...memeSerie, ...autres].slice(0, 4);

  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "Product",
    name: r.nom,
    description: r.resume,
    category: f.nom,
    material: matiere?.nom ?? "Acier",
    brand: { "@type": "Brand", name: "Aciers Grosjean" },
    weight: { "@type": "QuantitativeValue", value: r.kg, unitText: r.unitePoids },
    ...(r.prix !== null && {
      offers: {
        "@type": "Offer",
        price: r.prix.toFixed(2),
        priceCurrency: "EUR",
        availability: r.stock
          ? "https://schema.org/InStock"
          : "https://schema.org/PreOrder",
        availableDeliveryMethod: "https://schema.org/InStorePickup",
      },
    }),
  };

  return (
    <main>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />

      {/* fil d'ariane */}
      <div className="border-b border-brume bg-nuage pt-28 md:pt-32">
        <div className="container-g overflow-x-auto py-4">
          <nav className="whitespace-nowrap font-body text-xs text-soft" aria-label="Fil d'ariane">
            <Link href="/" className="hover:text-encre">Accueil</Link>
            <span className="mx-2 text-brume">/</span>
            <Link href="/produits" className="hover:text-encre">Catalogue</Link>
            <span className="mx-2 text-brume">/</span>
            <Link href={`/produits/${f.slug}`} className="hover:text-encre">{f.nom}</Link>
            <span className="mx-2 text-brume">/</span>
            <span className="text-encre">{r.nom}</span>
          </nav>
        </div>
      </div>

      <section className="bg-white py-12 md:py-16">
        <div className="container-g grid gap-12 lg:grid-cols-2 lg:gap-16">
          {/* ---- visuel technique ---- */}
          <Reveal>
            <div className="lg:sticky lg:top-28">
              <div className="group relative aspect-square overflow-hidden rounded-2xl border border-brume bg-nuage">
                <div className="grid-industrie absolute inset-0 opacity-70" />
                <div className="shine absolute inset-0">
                  <Art className="h-full w-full transition-transform duration-700 group-hover:scale-105" />
                </div>
                {r.stock && <span className="tag-stock absolute left-5 top-5">En stock</span>}
                <span className="absolute bottom-5 left-5 font-mono text-[11px] uppercase tracking-[0.16em] text-soft">
                  Schéma technique · {r.dims}
                </span>
              </div>

              {/* rappels de service sous le visuel */}
              <ul className="mt-5 grid grid-cols-3 gap-3">
                {[
                  ["Découpe", "aux cotes exactes"],
                  ["Retrait", "le jour même"],
                  ["Devis", "sous 24 h"],
                ].map(([t, s]) => (
                  <li key={t} className="rounded-xl border border-brume bg-white px-3 py-3 text-center">
                    <span className="h-title block text-sm font-semibold text-encre">{t}</span>
                    <span className="mt-0.5 block font-body text-[11px] leading-tight text-soft">{s}</span>
                  </li>
                ))}
              </ul>
            </div>
          </Reveal>

          {/* ---- détails ---- */}
          <Reveal delay={0.08}>
            <div className="flex flex-col">
              <div className="flex flex-wrap items-center gap-2">
                <Link
                  href={`/produits/${f.slug}`}
                  className="font-body text-xs uppercase tracking-[0.2em] text-soft transition-colors hover:text-encre"
                >
                  {f.nom}
                </Link>
                <span className="text-brume">·</span>
                <span className="font-body text-xs uppercase tracking-[0.2em] text-soft">{r.serie}</span>
              </div>

              <h1 className="h-display mt-3 text-3xl leading-[1.08] md:text-5xl">{r.nom}</h1>
              <p className="mt-1 font-mono text-sm text-soft">{r.dims}</p>

              <p className="mt-6 max-w-xl font-body text-lg leading-relaxed text-soft">{r.resume}</p>

              {/* prix */}
              <div className="mt-8 flex flex-wrap items-end gap-x-4 gap-y-1 border-y border-brume py-6">
                <span className="h-title text-4xl font-bold tabular-nums text-encre md:text-5xl">
                  {r.prixTexte}
                </span>
                <span className="pb-1 font-body text-sm text-soft">{r.unite}</span>
                {r.prix !== null && (
                  <span className="pb-1 font-body text-xs text-soft">
                    · HTVA · dégressif dès 100 kg
                  </span>
                )}
              </div>

              {/* calculateur */}
              <div className="mt-7">
                <Calculateur r={r} famille={f.slug} />
              </div>

              {/* caractéristiques */}
              <div className="mt-10">
                <h2 className="h-title text-sm font-semibold uppercase tracking-[0.14em] text-soft">
                  Caractéristiques techniques
                </h2>
                <dl className="mt-4 divide-y divide-brume border-y border-brume">
                  {r.specs.map((s) => (
                    <div key={s.label} className="flex items-baseline justify-between gap-6 py-3">
                      <dt className="font-body text-sm text-soft">{s.label}</dt>
                      <dd className="text-right font-mono text-sm tabular-nums text-encre">{s.valeur}</dd>
                    </div>
                  ))}
                </dl>
              </div>

              {/* usages */}
              <div className="mt-8">
                <h2 className="h-title text-sm font-semibold uppercase tracking-[0.14em] text-soft">
                  Usages courants
                </h2>
                <ul className="mt-3 flex flex-wrap gap-2">
                  {r.usages.map((u) => (
                    <li
                      key={u}
                      className="rounded-full border border-brume bg-nuage px-3.5 py-1.5 font-body text-sm text-encre"
                    >
                      {u}
                    </li>
                  ))}
                </ul>
              </div>

              {/* matière */}
              {matiere && (
                <Link
                  href={`/materiaux/${matiere.slug}`}
                  className="group mt-8 flex items-center justify-between gap-4 rounded-2xl border border-brume bg-nuage p-5 transition-colors hover:border-encre/30"
                >
                  <span>
                    <span className="font-body text-xs uppercase tracking-[0.14em] text-soft">Matière</span>
                    <span className="h-title mt-0.5 block font-semibold text-encre">{matiere.nom}</span>
                    <span className="mt-1 block font-body text-sm text-soft">{matiere.accroche}</span>
                  </span>
                  <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-jaune text-encre transition-transform duration-300 group-hover:rotate-45">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                      <path d="M7 17L17 7M9 7h8v8" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round" />
                    </svg>
                  </span>
                </Link>
              )}
            </div>
          </Reveal>
        </div>
      </section>

      {/* références voisines */}
      {voisines.length > 0 && (
        <section className="border-t border-brume bg-nuage py-16 md:py-20">
          <div className="container-g">
            <h2 className="h-display text-2xl md:text-3xl">
              {memeSerie.length > 0 ? `Autres ${r.serie.toLowerCase()}s` : "Dans la même famille"}
            </h2>
            <div className="mt-8 grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
              {voisines.map((v, i) => (
                <Reveal key={v.ref} delay={i * 0.06}>
                  <Link
                    href={`/produits/${f.slug}/${v.ref}`}
                    className="group flex h-full flex-col justify-between rounded-2xl border border-brume bg-white p-6 transition-all duration-300 hover:-translate-y-1 hover:shadow-[0_26px_60px_-34px_rgba(51,54,66,.5)]"
                  >
                    <div>
                      <h3 className="h-title font-semibold text-encre">{v.nom}</h3>
                      <p className="mt-1 font-mono text-xs text-soft">{v.dims}</p>
                    </div>
                    <div className="mt-6 flex items-end justify-between">
                      <span className="h-title text-lg font-bold tabular-nums text-encre">{v.prixTexte}</span>
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

            <div className="mt-10">
              <Link href={`/produits/${f.slug}`} className="btn-ghost">
                Voir les {f.refs.length} références {f.nom.toLowerCase()}
              </Link>
            </div>
          </div>
        </section>
      )}

      <CtaBand />
    </main>
  );
}
