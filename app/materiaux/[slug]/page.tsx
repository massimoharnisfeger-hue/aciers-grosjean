import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import PageHeader from "@/components/ui/PageHeader";
import CtaBand from "@/components/sections/CtaBand";
import Reveal from "@/components/fx/Reveal";
import { productArt, ArtPoutrelle } from "@/components/art/ProductArt";
import { matieres, matiereBySlug, familleBySlug } from "@/lib/catalogue";

type Params = { slug: string };

export function generateStaticParams() {
  return matieres.map((m) => ({ slug: m.slug }));
}

export async function generateMetadata({ params }: { params: Promise<Params> }): Promise<Metadata> {
  const { slug } = await params;
  const m = matiereBySlug(slug);
  if (!m) return { title: "Matière introuvable | Aciers Grosjean" };
  // Titre pensé pour le clic : la matière + ce qui déclenche la décision.
  return {
    title: `${m.nom} — découpe sur mesure, retrait le jour même | Aciers Grosjean`,
    description: `${m.accroche}. ${m.intro.slice(0, 110)}… Prix négociant, devis en 24h, 4 dépôts en Wallonie et en France.`,
  };
}

export default async function MatierePage({ params }: { params: Promise<Params> }) {
  const { slug } = await params;
  const m = matiereBySlug(slug);
  if (!m) notFound();

  const dispo = m.familles.map(familleBySlug).filter(Boolean);

  return (
    <main>
      <PageHeader surtitre={m.nom} titre={<>{m.accroche}</>} intro={m.intro} />

      {/* propriétés */}
      <section className="bg-white py-16 md:py-24">
        <div className="container-g grid gap-12 lg:grid-cols-2 lg:gap-16">
          <Reveal>
            <h2 className="h-display text-2xl md:text-3xl">Ce qu'il faut savoir</h2>
            <dl className="mt-6 divide-y divide-brume border-y border-brume">
              {m.proprietes.map((p) => (
                <div key={p.label} className="flex items-baseline justify-between gap-6 py-4">
                  <dt className="font-body text-sm text-soft">{p.label}</dt>
                  <dd className="text-right font-mono text-sm text-encre">{p.valeur}</dd>
                </div>
              ))}
            </dl>

            <h3 className="h-title mt-10 text-sm font-semibold uppercase tracking-[0.14em] text-soft">
              Usages courants
            </h3>
            <ul className="mt-3 flex flex-wrap gap-2">
              {m.usages.map((u) => (
                <li key={u} className="rounded-full border border-brume bg-nuage px-3.5 py-1.5 font-body text-sm text-encre">
                  {u}
                </li>
              ))}
            </ul>

            <div className="mt-10 flex flex-col gap-3 sm:flex-row">
              <Link href="/devis" className="btn-cta justify-center">Demander un devis</Link>
              <Link href="/produits" className="btn-ghost justify-center">Voir le catalogue</Link>
            </div>
          </Reveal>

          <Reveal delay={0.08}>
            <div className="group relative aspect-square overflow-hidden rounded-2xl border border-brume bg-nuage lg:sticky lg:top-28">
              <div className="grid-industrie absolute inset-0 opacity-70" />
              <div className="shine absolute inset-0">
                {(() => {
                  const f = dispo[0];
                  const Art = f ? productArt[f.art] ?? ArtPoutrelle : ArtPoutrelle;
                  return <Art className="h-full w-full transition-transform duration-700 group-hover:scale-105" />;
                })()}
              </div>
              <span className="absolute bottom-5 left-5 font-mono text-[11px] uppercase tracking-[0.16em] text-soft">
                {m.nom} · profilés disponibles
              </span>
            </div>
          </Reveal>
        </div>
      </section>

      {/* familles disponibles dans cette matière */}
      <section className="border-t border-brume bg-nuage py-16 md:py-24">
        <div className="container-g">
          <Reveal className="mb-9 max-w-2xl">
            <h2 className="h-display text-2xl md:text-3xl">
              Disponible en <span className="mark-jaune">{m.nom.toLowerCase()}</span>
            </h2>
            <p className="mt-3 font-body text-soft">
              Les familles que nous tenons en stock dans cette matière.
            </p>
          </Reveal>
          <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
            {dispo.map((f, i) =>
              f ? (
                <Reveal key={f.slug} delay={(i % 3) * 0.07}>
                  <Link
                    href={`/produits/${f.slug}`}
                    className="group flex h-full items-center justify-between gap-4 rounded-2xl border border-brume bg-white p-6 transition-all duration-300 hover:-translate-y-1 hover:shadow-[0_24px_56px_-34px_rgba(51,54,66,.5)]"
                  >
                    <div>
                      <h3 className="h-title font-semibold text-encre">{f.nom}</h3>
                      <p className="mt-1 font-body text-sm text-soft">{f.accroche}</p>
                    </div>
                    <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-jaune text-encre transition-transform duration-300 group-hover:rotate-45">
                      <svg width="15" height="15" viewBox="0 0 24 24" fill="none">
                        <path d="M7 17L17 7M9 7h8v8" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round" />
                      </svg>
                    </span>
                  </Link>
                </Reveal>
              ) : null
            )}
          </div>
        </div>
      </section>

      <CtaBand />
    </main>
  );
}
