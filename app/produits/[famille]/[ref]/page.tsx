import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import CtaBand from "@/components/sections/CtaBand";
import Reveal from "@/components/fx/Reveal";
import { productArt, ArtPoutrelle } from "@/components/art/ProductArt";
import { familles, familleBySlug, refBySlug } from "@/lib/catalogue";

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
  return {
    title: `${r.nom} — ${r.dims} | Aciers Grosjean`,
    description: `${r.resume} ${r.prix !== "Sur devis" ? `À partir de ${r.prix} ${r.unite}.` : ""} En stock, découpe sur mesure, retrait le jour même dans nos 4 dépôts.`,
  };
}

export default async function FicheProduit({ params }: { params: Promise<Params> }) {
  const { famille, ref } = await params;
  const f = familleBySlug(famille);
  const r = refBySlug(famille, ref);
  if (!f || !r) notFound();

  const Art = productArt[f.art] ?? ArtPoutrelle;
  const voisines = f.refs.filter((x) => x.ref !== r.ref).slice(0, 3);

  return (
    <main>
      {/* fil d'ariane */}
      <div className="border-b border-brume bg-nuage pt-28 md:pt-32">
        <div className="container-g py-4">
          <nav className="font-body text-xs text-soft" aria-label="Fil d'ariane">
            <Link href="/" className="hover:text-encre">Accueil</Link>
            <span className="mx-2 text-brume">/</span>
            <Link href="/produits" className="hover:text-encre">Produits</Link>
            <span className="mx-2 text-brume">/</span>
            <Link href={`/produits/${f.slug}`} className="hover:text-encre">{f.nom}</Link>
            <span className="mx-2 text-brume">/</span>
            <span className="text-encre">{r.nom}</span>
          </nav>
        </div>
      </div>

      {/* fiche */}
      <section className="bg-white py-12 md:py-20">
        <div className="container-g grid gap-12 lg:grid-cols-2 lg:gap-16">
          {/* visuel */}
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
            </div>
          </Reveal>

          {/* détails */}
          <Reveal delay={0.08}>
            <div className="flex flex-col">
              <Link
                href={`/produits/${f.slug}`}
                className="font-body text-xs uppercase tracking-[0.2em] text-soft transition-colors hover:text-encre"
              >
                {f.nom}
              </Link>

              <h1 className="h-display mt-3 text-3xl leading-[1.08] md:text-5xl">{r.nom}</h1>
              <p className="mt-1 font-mono text-sm text-soft">{r.dims}</p>

              <p className="mt-6 max-w-xl font-body text-lg leading-relaxed text-soft">{r.resume}</p>

              {/* prix */}
              <div className="mt-8 flex flex-wrap items-end gap-x-4 gap-y-1 border-y border-brume py-6">
                <span className="h-title text-4xl font-bold tabular-nums text-encre md:text-5xl">
                  {r.prix}
                </span>
                <span className="pb-1 font-body text-sm text-soft">{r.unite}</span>
                {r.prix !== "Sur devis" && (
                  <span className="pb-1 font-body text-xs text-soft">· HTVA, dégressif selon quantité</span>
                )}
              </div>

              {/* actions */}
              <div className="mt-7 flex flex-col gap-3 sm:flex-row">
                <Link href="/devis" className="btn-cta justify-center">
                  Demander le prix exact
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
                    <path d="M5 12h14M13 6l6 6-6 6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                  </svg>
                </Link>
                <Link href="/depots" className="btn-ghost justify-center">Voir les dépôts</Link>
              </div>

              <p className="mt-4 font-body text-sm text-soft">
                ✓ Découpe aux cotes&nbsp;&nbsp;·&nbsp;&nbsp;✓ Retrait le jour même&nbsp;&nbsp;·&nbsp;&nbsp;✓ Devis sous 24h
              </p>

              {/* caractéristiques */}
              <div className="mt-10">
                <h2 className="h-title text-sm font-semibold uppercase tracking-[0.14em] text-soft">
                  Caractéristiques
                </h2>
                <dl className="mt-4 divide-y divide-brume border-y border-brume">
                  {r.specs.map((s) => (
                    <div key={s.label} className="flex items-baseline justify-between gap-6 py-3">
                      <dt className="font-body text-sm text-soft">{s.label}</dt>
                      <dd className="font-mono text-sm tabular-nums text-encre">{s.valeur}</dd>
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
                    <li key={u} className="rounded-full border border-brume bg-nuage px-3.5 py-1.5 font-body text-sm text-encre">
                      {u}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </Reveal>
        </div>
      </section>

      {/* références voisines */}
      {voisines.length > 0 && (
        <section className="border-t border-brume bg-nuage py-16 md:py-20">
          <div className="container-g">
            <h2 className="h-display text-2xl md:text-3xl">Dans la même famille</h2>
            <div className="mt-8 grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
              {voisines.map((v, i) => (
                <Reveal key={v.ref} delay={i * 0.07}>
                  <Link
                    href={`/produits/${f.slug}/${v.ref}`}
                    className="group flex h-full flex-col justify-between rounded-2xl border border-brume bg-white p-6 transition-all duration-300 hover:-translate-y-1 hover:shadow-[0_26px_60px_-34px_rgba(51,54,66,.5)]"
                  >
                    <div>
                      <h3 className="h-title font-semibold text-encre">{v.nom}</h3>
                      <p className="mt-1 font-mono text-xs text-soft">{v.dims}</p>
                    </div>
                    <div className="mt-6 flex items-end justify-between">
                      <span className="h-title text-lg font-bold text-encre">{v.prix}</span>
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
      )}

      <CtaBand />
    </main>
  );
}
