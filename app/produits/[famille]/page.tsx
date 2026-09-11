import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import PageHeader from "@/components/ui/PageHeader";
import CtaBand from "@/components/sections/CtaBand";
import Reveal from "@/components/fx/Reveal";
import TableauRefs from "@/components/catalogue/TableauRefs";
import { productArt, ArtPoutrelle } from "@/components/art/ProductArt";
import { familles, familleBySlug, matieres, prixMini } from "@/lib/catalogue";

type Params = { famille: string };

export function generateStaticParams() {
  return familles.map((f) => ({ famille: f.slug }));
}

export async function generateMetadata({ params }: { params: Promise<Params> }): Promise<Metadata> {
  const { famille } = await params;
  const f = familleBySlug(famille);
  if (!f) return { title: "Famille introuvable | Aciers Grosjean" };
  return {
    title: `${f.titreSeo} | Aciers Grosjean`,
    description: f.descSeo,
    alternates: { canonical: `/produits/${f.slug}` },
  };
}

export default async function FamillePage({ params }: { params: Promise<Params> }) {
  const { famille } = await params;
  const f = familleBySlug(famille);
  if (!f) notFound();

  const Art = productArt[f.art] ?? ArtPoutrelle;
  const mini = prixMini(f);
  const matieresLiees = matieres.filter((m) => m.familles.includes(f.slug));
  const autres = familles.filter((x) => x.slug !== f.slug).slice(0, 4);

  return (
    <main>
      <PageHeader surtitre={f.nom} titre={<>{f.accroche}</>} intro={f.intro} />

      <section className="bg-white py-14 md:py-20">
        <div className="container-g">
          {/* bandeau chiffres + visuel */}
          <div className="mb-14 grid items-center gap-10 md:grid-cols-[1fr_.85fr]">
            <Reveal>
              <dl className="grid grid-cols-2 gap-x-8 gap-y-6 sm:grid-cols-4 md:grid-cols-2 lg:grid-cols-4">
                <div>
                  <dt className="font-body text-xs uppercase tracking-[0.14em] text-soft">Références</dt>
                  <dd className="h-title mt-1 text-3xl font-bold tabular-nums text-encre">{f.refs.length}</dd>
                </div>
                <div>
                  <dt className="font-body text-xs uppercase tracking-[0.14em] text-soft">Séries</dt>
                  <dd className="h-title mt-1 text-3xl font-bold tabular-nums text-encre">{f.series.length}</dd>
                </div>
                {mini && (
                  <div>
                    <dt className="font-body text-xs uppercase tracking-[0.14em] text-soft">À partir de</dt>
                    <dd className="h-title mt-1 text-3xl font-bold tabular-nums text-encre">
                      {mini.valeur.toLocaleString("fr-BE", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                      <span className="ml-1 text-base font-normal text-soft">{mini.unite}</span>
                    </dd>
                  </div>
                )}
                <div>
                  <dt className="font-body text-xs uppercase tracking-[0.14em] text-soft">Retrait</dt>
                  <dd className="h-title mt-1 text-3xl font-bold text-encre">Jour même</dd>
                </div>
              </dl>

              <p className="mt-7 max-w-lg font-body text-soft">
                Toutes les sections sont débitées aux cotes exactes — vous ne payez que ce
                dont vous avez besoin. Les prix sont indicatifs, hors TVA, et dégressifs dès
                100&nbsp;kg.
              </p>
              <div className="mt-6 flex flex-wrap gap-3">
                <Link href="/devis" className="btn-cta">Demander un devis</Link>
                <Link href="/services/decoupe" className="btn-ghost">La découpe sur mesure</Link>
              </div>
            </Reveal>

            <Reveal delay={0.08}>
              <div className="group relative aspect-[4/3] overflow-hidden rounded-2xl border border-brume bg-nuage">
                <div className="grid-industrie absolute inset-0 opacity-70" />
                <div className="shine absolute inset-0">
                  <Art className="h-full w-full transition-transform duration-700 group-hover:scale-105" />
                </div>
                <span className="tag-stock absolute left-5 top-5">Stock permanent</span>
              </div>
            </Reveal>
          </div>

          <h2 className="h-display mb-2 text-2xl md:text-3xl">
            Les {f.refs.length} références en stock
          </h2>
          <p className="mb-6 max-w-xl font-body text-soft">
            Filtrez par série, cherchez une cote ou un usage. Chaque ligne mène à la fiche
            technique complète, avec le poids au mètre et le calcul de votre quantité.
          </p>

          <TableauRefs famille={f.slug} refs={f.refs} series={f.series} />
        </div>
      </section>

      {/* matières liées */}
      {matieresLiees.length > 0 && (
        <section className="border-t border-brume bg-nuage py-16">
          <div className="container-g">
            <h2 className="h-display text-2xl md:text-3xl">Dans quelle matière&nbsp;?</h2>
            <p className="mt-3 max-w-xl font-body text-soft">
              C'est la question qui coûte le plus cher quand on se trompe. Voici ce qui
              distingue les matières disponibles dans cette famille.
            </p>
            <div className="mt-8 grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
              {matieresLiees.map((m, i) => (
                <Reveal key={m.slug} delay={i * 0.07}>
                  <Link
                    href={`/materiaux/${m.slug}`}
                    className="group flex h-full flex-col rounded-2xl border border-brume bg-white p-6 transition-all duration-300 hover:-translate-y-1 hover:shadow-[0_26px_60px_-34px_rgba(51,54,66,.5)]"
                  >
                    <h3 className="h-title text-lg font-semibold text-encre">{m.nom}</h3>
                    <p className="mt-2 flex-1 font-body text-sm leading-relaxed text-soft">{m.accroche}</p>
                    <span className="mt-5 inline-flex items-center gap-2 font-body text-sm font-medium text-encre">
                      Comprendre la matière
                      <svg width="15" height="15" viewBox="0 0 24 24" fill="none" className="transition-transform group-hover:translate-x-1">
                        <path d="M5 12h14M13 6l6 6-6 6" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round" />
                      </svg>
                    </span>
                  </Link>
                </Reveal>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* familles voisines — maillage interne */}
      <section className="border-t border-brume bg-white py-14">
        <div className="container-g">
          <h2 className="h-title text-sm font-semibold uppercase tracking-[0.14em] text-soft">
            Autres familles du catalogue
          </h2>
          <div className="mt-5 flex flex-wrap gap-3">
            {autres.map((a) => (
              <Link
                key={a.slug}
                href={`/produits/${a.slug}`}
                className="rounded-full border border-brume px-4 py-2 font-body text-sm text-encre transition-colors hover:border-encre hover:bg-nuage"
              >
                {a.nom}
                <span className="ml-2 font-mono text-xs text-soft">{a.refs.length}</span>
              </Link>
            ))}
            <Link
              href="/produits"
              className="rounded-full border border-encre bg-encre px-4 py-2 font-body text-sm text-white transition-opacity hover:opacity-90"
            >
              Tout le catalogue
            </Link>
          </div>
        </div>
      </section>

      <CtaBand />
    </main>
  );
}
