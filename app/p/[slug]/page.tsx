import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import CtaBand from "@/components/sections/CtaBand";
import Reveal from "@/components/fx/Reveal";
import FilAriane from "@/components/ui/FilAriane";
import Calculateur from "@/components/catalogue/Calculateur";
import { productArt, ArtPoutrelle } from "@/components/art/ProductArt";
import {
  produits as tous,
  produitBySlug,
  noeuds,
  ancetres,
  universBySlug,
  formatPrix,
} from "@/lib/catalogue";
import { artPour } from "@/lib/visuels";
import { titre, description } from "@/lib/seo";

type Params = { slug: string };

export const dynamicParams = false;

export function generateStaticParams() {
  return Object.keys(tous).map((slug) => ({ slug }));
}

export async function generateMetadata({ params }: { params: Promise<Params> }): Promise<Metadata> {
  const { slug } = await params;
  const p = produitBySlug(slug);
  if (!p) return { title: "Produit introuvable | Aciers Grosjean" };

  const prixTxt = p.prix !== null ? ` — ${formatPrix(p.prix)}` : "";
  const poids = p.kg !== null ? ` ${p.kg.toString().replace(".", ",")} ${p.unitePoids}.` : "";

  return {
    title: titre(`${p.nom}${prixTxt}`),
    description: description(
      `${p.nom} en stock.${poids}` +
        (p.prix !== null ? ` ${formatPrix(p.prix)} ${p.unite} HTVA.` : " Prix sur devis sous 24 h.") +
        " Découpe aux cotes, retrait le jour même dans nos 4 dépôts."
    ),
    alternates: { canonical: `/p/${p.slug}` },
  };
}

export default async function FicheProduit({ params }: { params: Promise<Params> }) {
  const { slug } = await params;
  const p = produitBySlug(slug);
  if (!p) notFound();

  const cat = noeuds[p.categorie];
  const u = universBySlug(p.univers)!;
  const Art = productArt[artPour(p.categorie, u.art)] ?? ArtPoutrelle;

  const chaine = ancetres(p.categorie);
  const miettes = [
    { label: "Catalogue", href: "/produits" },
    ...chaine.map((a) => ({ label: a.nom, href: a.chemin })),
    { label: p.nom },
  ];

  const voisins = (cat?.produits ?? [])
    .filter((s) => s !== p.slug)
    .map((s) => tous[s])
    .filter(Boolean)
    .slice(0, 4);

  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "Product",
    name: p.nom,
    category: cat?.nom ?? u.nom,
    material: u.nom,
    brand: { "@type": "Brand", name: "Aciers Grosjean" },
    ...(p.kg !== null && {
      weight: { "@type": "QuantitativeValue", value: p.kg, unitText: p.unitePoids },
    }),
    ...(p.prix !== null && {
      offers: {
        "@type": "Offer",
        price: p.prix.toFixed(2),
        priceCurrency: "EUR",
        availability: "https://schema.org/InStock",
        availableDeliveryMethod: "https://schema.org/InStorePickup",
        priceSpecification: {
          "@type": "UnitPriceSpecification",
          price: p.prix.toFixed(2),
          priceCurrency: "EUR",
          unitText: p.unite,
        },
      },
    }),
  };

  return (
    <main>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }} />

      <div className="border-b border-brume bg-nuage pt-28 md:pt-32">
        <div className="container-g py-4">
          <FilAriane items={miettes} />
        </div>
      </div>

      <section className="bg-white py-12 md:py-16">
        <div className="container-g grid gap-12 lg:grid-cols-2 lg:gap-16">
          {/* visuel */}
          <Reveal>
            <div className="lg:sticky lg:top-28">
              <div className="group relative aspect-square overflow-hidden rounded-2xl border border-brume bg-nuage">
                <div className="grid-industrie absolute inset-0 opacity-70" />
                <div className="shine absolute inset-0">
                  <Art className="h-full w-full transition-transform duration-700 group-hover:scale-105" />
                </div>
                <span className="tag-stock absolute left-5 top-5">En stock</span>
                <span className="absolute bottom-5 left-5 right-5 truncate font-mono text-[11px] uppercase tracking-[0.16em] text-soft">
                  Schéma technique · {cat?.nom}
                </span>
              </div>

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

              <p className="mt-4 font-body text-[11px] leading-relaxed text-soft">
                Illustration technique, non contractuelle. Les informations techniques sont
                données à titre indicatif.
              </p>
            </div>
          </Reveal>

          {/* détails */}
          <Reveal delay={0.08}>
            <div className="flex flex-col">
              <div className="flex flex-wrap items-center gap-2">
                <Link
                  href={`/${u.slug}`}
                  className="font-body text-xs uppercase tracking-[0.2em] text-soft transition-colors hover:text-encre"
                >
                  {u.nom}
                </Link>
                {cat && (
                  <>
                    <span className="text-brume" aria-hidden="true">·</span>
                    <Link
                      href={cat.chemin}
                      className="font-body text-xs uppercase tracking-[0.2em] text-soft transition-colors hover:text-encre"
                    >
                      {cat.nom}
                    </Link>
                  </>
                )}
              </div>

              <h1 className="h-display mt-3 text-3xl leading-[1.1] md:text-4xl">{p.nom}</h1>

              <div className="mt-7 flex flex-wrap items-end gap-x-4 gap-y-1 border-y border-brume py-6">
                <span className="h-title text-4xl font-bold tabular-nums text-encre md:text-5xl">
                  {formatPrix(p.prix)}
                </span>
                <span className="pb-1 font-body text-sm text-soft">{p.unite}</span>
                {p.prix !== null && (
                  <span className="pb-1 font-body text-xs text-soft">· HTVA · dégressif dès 100 kg</span>
                )}
              </div>

              <div className="mt-7">
                <Calculateur p={p} />
              </div>

              {p.specs.length > 0 && (
                <div className="mt-10">
                  <h2 className="h-title text-sm font-semibold uppercase tracking-[0.14em] text-soft">
                    Spécifications
                  </h2>
                  <dl className="mt-4 divide-y divide-brume border-y border-brume">
                    {p.specs.map((s) => (
                      <div key={s.label} className="flex items-baseline justify-between gap-6 py-3">
                        <dt className="font-body text-sm text-soft">{s.label}</dt>
                        <dd className="text-right font-mono text-sm tabular-nums text-encre">{s.valeur}</dd>
                      </div>
                    ))}
                  </dl>
                </div>
              )}

              <div className="mt-8 grid gap-3 sm:grid-cols-2">
                <Link href="/devis" className="btn-cta justify-center">Demander un devis</Link>
                <Link href="/depots" className="btn-ghost justify-center">Choisir mon dépôt</Link>
              </div>

              {cat && (
                <Link
                  href={cat.chemin}
                  className="group mt-8 flex items-center justify-between gap-4 rounded-2xl border border-brume bg-nuage p-5 transition-colors hover:border-encre/30"
                >
                  <span>
                    <span className="font-body text-xs uppercase tracking-[0.14em] text-soft">Catégorie</span>
                    <span className="h-title mt-0.5 block font-semibold text-encre">{cat.nom}</span>
                    <span className="mt-1 block font-body text-sm text-soft">
                      {cat.produits.length} produit{cat.produits.length > 1 ? "s" : ""} de la même famille
                    </span>
                  </span>
                  <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-jaune text-encre transition-transform duration-300 group-hover:rotate-45">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                      <path d="M7 17L17 7M9 7h8v8" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round" />
                    </svg>
                  </span>
                </Link>
              )}
            </div>
          </Reveal>
        </div>
      </section>

      {voisins.length > 0 && (
        <section className="border-t border-brume bg-nuage py-16 md:py-20">
          <div className="container-g">
            <h2 className="h-display text-2xl md:text-3xl">Dans la même catégorie</h2>
            <div className="mt-8 grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
              {voisins.map((v, i) => (
                <Reveal key={v.slug} delay={i * 0.06}>
                  <Link
                    href={`/p/${v.slug}`}
                    className="group flex h-full flex-col justify-between rounded-2xl border border-brume bg-white p-6 transition-all duration-300 hover:-translate-y-1 hover:shadow-[0_26px_60px_-34px_rgba(51,54,66,.5)]"
                  >
                    <h3 className="h-title font-semibold leading-snug text-encre">{v.nom}</h3>
                    <div className="mt-6 flex items-end justify-between">
                      <span className="h-title text-lg font-bold tabular-nums text-encre">{formatPrix(v.prix)}</span>
                      <span className="flex h-9 w-9 items-center justify-center rounded-full bg-jaune text-encre transition-transform duration-300 group-hover:rotate-45">
                        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                          <path d="M7 17L17 7M9 7h8v8" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round" />
                        </svg>
                      </span>
                    </div>
                  </Link>
                </Reveal>
              ))}
            </div>
            {cat && (
              <div className="mt-10">
                <Link href={cat.chemin} className="btn-ghost">
                  Voir les {cat.produits.length} produits {cat.nom.toLowerCase()}
                </Link>
              </div>
            )}
          </div>
        </section>
      )}

      <CtaBand />
    </main>
  );
}
