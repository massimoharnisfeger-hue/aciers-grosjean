import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import CtaBand from "@/components/sections/CtaBand";
import Reveal from "@/components/fx/Reveal";
import { productArt, ArtPoutrelle } from "@/components/art/ProductArt";
import { matieres, matiereBySlug, familleBySlug, refsParMatiere } from "@/lib/catalogue";
import { guides } from "@/lib/edito";

type Params = { slug: string };

export function generateStaticParams() {
  return matieres.map((m) => ({ slug: m.slug }));
}

export async function generateMetadata({ params }: { params: Promise<Params> }): Promise<Metadata> {
  const { slug } = await params;
  const m = matiereBySlug(slug);
  if (!m) return { title: "Matériau introuvable | Aciers Grosjean" };
  return {
    title: `${m.titreSeo} | Aciers Grosjean`,
    description: m.descSeo,
    alternates: { canonical: `/materiaux/${m.slug}` },
  };
}

export default async function MatierePage({ params }: { params: Promise<Params> }) {
  const { slug } = await params;
  const m = matiereBySlug(slug);
  if (!m) notFound();

  const famillesLiees = m.familles
    .map((f) => familleBySlug(f))
    .filter((f): f is NonNullable<ReturnType<typeof familleBySlug>> => Boolean(f));

  const refsMatiere = refsParMatiere(m.slug).slice(0, 6);
  const guidesLies = guides.filter((g) => g.liens.some((l) => l.href.includes(m.slug))).slice(0, 3);
  const autresMatieres = matieres.filter((x) => x.slug !== m.slug);

  return (
    <main>
      <header className="relative overflow-hidden border-b border-brume bg-nuage pt-32 md:pt-40">
        <div className="grid-industrie pointer-events-none absolute inset-0 opacity-60" />
        <div className="pointer-events-none absolute -right-16 top-16 h-64 w-64 rounded-full bg-jaune/10 blur-[110px]" />
        <div className="container-g relative pb-14 md:pb-20">
          <nav className="mb-5 font-body text-xs text-soft">
            <Link href="/" className="hover:text-encre">Accueil</Link>
            <span className="mx-2 text-brume">/</span>
            <Link href="/produits" className="hover:text-encre">Matériaux</Link>
            <span className="mx-2 text-brume">/</span>
            <span className="text-encre">{m.nom}</span>
          </nav>
          <h1 className="h-display max-w-3xl text-4xl md:text-6xl">{m.accroche}</h1>
          <p className="mt-5 max-w-2xl font-body text-lg text-soft">{m.intro}</p>
          <div className="mt-8 flex flex-wrap gap-3">
            <Link href="/devis" className="btn-cta">Demander un prix</Link>
            {famillesLiees[0] && (
              <Link href={`/produits/${famillesLiees[0].slug}`} className="btn-ghost">
                Voir les produits
              </Link>
            )}
          </div>
        </div>
      </header>

      {/* propriétés & à retenir */}
      <section className="bg-white py-14 md:py-20">
        <div className="container-g grid gap-12 lg:grid-cols-2 lg:gap-16">
          <Reveal>
            <h2 className="h-display text-2xl md:text-3xl">Les propriétés qui comptent</h2>
            <dl className="mt-6 divide-y divide-brume border-y border-brume">
              {m.proprietes.map((p) => (
                <div key={p.label} className="flex flex-wrap items-baseline justify-between gap-4 py-3.5">
                  <dt className="font-body text-sm text-soft">{p.label}</dt>
                  <dd className="text-right font-mono text-sm text-encre">{p.valeur}</dd>
                </div>
              ))}
            </dl>

            <h2 className="h-title mt-10 text-sm font-semibold uppercase tracking-[0.14em] text-soft">
              Usages typiques
            </h2>
            <ul className="mt-3 flex flex-wrap gap-2">
              {m.usages.map((u) => (
                <li key={u} className="rounded-full border border-brume bg-nuage px-3.5 py-1.5 font-body text-sm text-encre">
                  {u}
                </li>
              ))}
            </ul>
          </Reveal>

          <Reveal delay={0.08}>
            <h2 className="h-display text-2xl md:text-3xl">À retenir avant de commander</h2>
            <div className="mt-6 space-y-4">
              {m.aRetenir.map((a, i) => (
                <div key={a.titre} className="rounded-2xl border border-brume bg-nuage p-6">
                  <div className="flex items-baseline gap-3">
                    <span className="font-mono text-xs text-soft">{String(i + 1).padStart(2, "0")}</span>
                    <h3 className="h-title font-semibold text-encre">{a.titre}</h3>
                  </div>
                  <p className="mt-2 font-body leading-relaxed text-soft">{a.texte}</p>
                </div>
              ))}
            </div>
          </Reveal>
        </div>
      </section>

      {/* familles disponibles */}
      <section className="border-t border-brume bg-nuage py-16 md:py-20">
        <div className="container-g">
          <h2 className="h-display text-2xl md:text-3xl">
            En {m.nom.toLowerCase()}, nous tenons&nbsp;:
          </h2>
          <div className="mt-8 grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
            {famillesLiees.map((f, i) => {
              const Art = productArt[f.art] ?? ArtPoutrelle;
              return (
                <Reveal key={f.slug} delay={(i % 3) * 0.07}>
                  <Link
                    href={`/produits/${f.slug}`}
                    className="group flex h-full flex-col overflow-hidden rounded-2xl border border-brume bg-white transition-all duration-300 hover:-translate-y-1 hover:shadow-[0_28px_64px_-36px_rgba(51,54,66,.55)]"
                  >
                    <div className="shine relative aspect-[16/9] overflow-hidden bg-nuage">
                      <div className="grid-industrie absolute inset-0 opacity-70" />
                      <Art className="absolute inset-0 h-full w-full transition-transform duration-700 group-hover:scale-105" />
                    </div>
                    <div className="flex flex-1 flex-col p-6">
                      <h3 className="h-title text-lg font-semibold text-encre">{f.nom}</h3>
                      <p className="mt-1.5 flex-1 font-body text-sm text-soft">{f.accroche}</p>
                      <span className="mt-4 font-mono text-xs text-soft">{f.refs.length} références</span>
                    </div>
                  </Link>
                </Reveal>
              );
            })}
          </div>

          {refsMatiere.length > 0 && (
            <>
              <h3 className="h-title mt-14 text-sm font-semibold uppercase tracking-[0.14em] text-soft">
                Références les plus demandées en {m.nom.toLowerCase()}
              </h3>
              <ul className="mt-5 grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
                {refsMatiere.map(({ famille, ref }) => (
                  <li key={ref.ref}>
                    <Link
                      href={`/produits/${famille.slug}/${ref.ref}`}
                      className="flex items-center justify-between gap-4 rounded-xl border border-brume bg-white px-4 py-3.5 transition-colors hover:border-encre/30"
                    >
                      <span className="min-w-0">
                        <span className="h-title block truncate font-semibold text-encre">{ref.nom}</span>
                        <span className="mt-0.5 block font-mono text-xs text-soft">{ref.dims}</span>
                      </span>
                      <span className="h-title shrink-0 font-bold tabular-nums text-encre">{ref.prixTexte}</span>
                    </Link>
                  </li>
                ))}
              </ul>
            </>
          )}
        </div>
      </section>

      {/* guides liés */}
      {guidesLies.length > 0 && (
        <section className="bg-white py-16">
          <div className="container-g">
            <h2 className="h-display text-2xl md:text-3xl">Pour aller plus loin</h2>
            <div className="mt-8 grid gap-5 md:grid-cols-3">
              {guidesLies.map((g, i) => (
                <Reveal key={g.slug} delay={i * 0.07}>
                  <Link
                    href={`/guides/${g.slug}`}
                    className="group flex h-full flex-col rounded-2xl border border-brume bg-white p-6 transition-all duration-300 hover:-translate-y-1 hover:shadow-[0_26px_60px_-34px_rgba(51,54,66,.5)]"
                  >
                    <span className="font-mono text-xs text-soft">{g.lecture} min</span>
                    <h3 className="h-title mt-2 font-semibold leading-snug text-encre">{g.titre}</h3>
                    <p className="mt-2 flex-1 font-body text-sm text-soft">{g.chapo}</p>
                  </Link>
                </Reveal>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* comparaison */}
      <section className="border-t border-brume bg-white py-14">
        <div className="container-g">
          <h2 className="h-title text-sm font-semibold uppercase tracking-[0.14em] text-soft">
            Comparer avec les autres matières
          </h2>
          <div className="mt-5 flex flex-wrap gap-3">
            {autresMatieres.map((a) => (
              <Link
                key={a.slug}
                href={`/materiaux/${a.slug}`}
                className="rounded-full border border-brume px-4 py-2 font-body text-sm text-encre transition-colors hover:border-encre hover:bg-nuage"
              >
                {a.nom}
              </Link>
            ))}
            <Link
              href="/guides/galvanise-inox-ou-acier-peint"
              className="rounded-full border border-encre bg-encre px-4 py-2 font-body text-sm text-white transition-opacity hover:opacity-90"
            >
              Le comparatif complet
            </Link>
          </div>
        </div>
      </section>

      <CtaBand />
    </main>
  );
}
