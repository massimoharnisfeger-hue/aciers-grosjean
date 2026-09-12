import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import CtaBand from "@/components/sections/CtaBand";
import Reveal from "@/components/fx/Reveal";
import FilAriane from "@/components/ui/FilAriane";
import { articles, articleBySlug, type Bloc } from "@/lib/edito";
import { titre, description } from "@/lib/seo";

type Params = { slug: string };

export const dynamicParams = false;

export function generateStaticParams() {
  return articles.map((a) => ({ slug: a.slug }));
}

export async function generateMetadata({ params }: { params: Promise<Params> }): Promise<Metadata> {
  const { slug } = await params;
  const a = articleBySlug(slug);
  if (!a) return { title: "Article introuvable | Aciers Grosjean" };
  return {
    title: titre(a.titreSeo),
    description: description(a.descSeo),
    alternates: { canonical: `/conseils/${a.slug}` },
  };
}

function RenduBloc({ b }: { b: Bloc }) {
  if (b.type === "p") return <p className="font-body text-lg leading-[1.75] text-soft">{b.texte}</p>;

  if (b.type === "liste")
    return (
      <ul className="space-y-3">
        {b.items.map((it) => (
          <li key={it} className="flex gap-3 font-body text-lg leading-[1.7] text-soft">
            <span className="mt-[0.62em] h-1.5 w-1.5 shrink-0 rounded-full bg-jaune" aria-hidden="true" />
            <span>{it}</span>
          </li>
        ))}
      </ul>
    );

  if (b.type === "encadre")
    return (
      <aside className="rounded-2xl border-l-4 border-jaune bg-nuage p-6">
        <p className="h-title font-semibold text-encre">{b.titre}</p>
        <p className="mt-2 font-body leading-relaxed text-soft">{b.texte}</p>
      </aside>
    );

  return (
    <div className="overflow-x-auto rounded-2xl border border-brume">
      <table className="w-full border-collapse text-left">
        <thead>
          <tr className="border-b border-brume bg-nuage">
            {b.entetes.map((h, i) => (
              <th key={i} scope="col" className="px-5 py-3 font-body text-xs font-semibold uppercase tracking-[0.12em] text-soft">
                {h}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {b.lignes.map((l, i) => (
            <tr key={i} className="border-b border-brume/70 last:border-0">
              {l.map((c, j) => (
                <td key={j} className={`px-5 py-3.5 ${j === 0 ? "h-title font-semibold text-encre" : "font-body text-sm text-soft"}`}>
                  {c}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default async function ArticlePage({ params }: { params: Promise<Params> }) {
  const { slug } = await params;
  const a = articleBySlug(slug);
  if (!a) notFound();

  const memeCategorie = articles.filter((x) => x.categorie === a.categorie && x.slug !== a.slug);
  const autres = (memeCategorie.length ? memeCategorie : articles.filter((x) => x.slug !== a.slug)).slice(0, 3);

  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "Article",
    headline: a.titre,
    description: a.descSeo,
    articleSection: a.categorie,
    author: { "@type": "Organization", name: "Aciers Grosjean" },
    publisher: { "@type": "Organization", name: "Aciers Grosjean" },
  };

  return (
    <main>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }} />

      <header className="relative overflow-hidden border-b border-brume bg-nuage pt-32 md:pt-40">
        <div className="grid-industrie pointer-events-none absolute inset-0 opacity-60" />
        <div className="pointer-events-none absolute -right-16 top-16 h-64 w-64 rounded-full bg-jaune/10 blur-[110px]" />
        <div className="container-g relative pb-14">
          <div className="mb-5">
            <FilAriane items={[{ label: "Conseils", href: "/conseils" }, { label: a.categorie }]} />
          </div>
          <h1 className="h-display max-w-3xl text-3xl md:text-5xl">{a.titre}</h1>
          <p className="mt-5 max-w-2xl font-body text-lg text-soft">{a.chapo}</p>
          <p className="mt-6 font-mono text-xs text-soft">
            {a.date} · {a.lecture} min de lecture
          </p>
        </div>
      </header>

      <article className="bg-white py-14 md:py-20">
        <div className="container-g grid gap-12 lg:grid-cols-[minmax(0,1fr)_16rem] lg:gap-16">
          <div className="max-w-[46rem]">
            {a.sections.map((s, i) => (
              <Reveal key={s.titre} delay={0.04}>
                <section className={i > 0 ? "mt-14" : ""}>
                  <h2 className="h-display text-2xl md:text-3xl">{s.titre}</h2>
                  <div className="mt-6 space-y-6">
                    {s.blocs.map((b, j) => (
                      <RenduBloc key={j} b={b} />
                    ))}
                  </div>
                </section>
              </Reveal>
            ))}

            <div className="mt-14 rounded-2xl border border-brume bg-nuage p-7">
              <h2 className="h-title text-lg font-semibold text-encre">
                Une question que cet article ne couvre pas&nbsp;?
              </h2>
              <p className="mt-2 max-w-lg font-body text-soft">
                Décrivez votre projet en deux lignes. On répond sous 24&nbsp;h, sans engagement,
                et on vous dit franchement si ce n'est pas pour nous.
              </p>
              <Link href="/devis" className="btn-cta mt-5">Poser ma question</Link>
            </div>
          </div>

          <aside className="lg:sticky lg:top-28 lg:self-start">
            <h2 className="h-title text-sm font-semibold uppercase tracking-[0.14em] text-soft">
              À voir aussi
            </h2>
            <ul className="mt-4 space-y-2">
              {a.liens.map((l) => (
                <li key={l.href}>
                  <Link
                    href={l.href}
                    className="group flex items-center justify-between gap-3 rounded-xl border border-brume bg-white px-4 py-3 font-body text-sm text-encre transition-colors hover:border-encre/30"
                  >
                    {l.label}
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" aria-hidden="true"
                      className="shrink-0 text-soft transition-transform group-hover:translate-x-0.5">
                      <path d="M5 12h14M13 6l6 6-6 6" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round" />
                    </svg>
                  </Link>
                </li>
              ))}
            </ul>
          </aside>
        </div>
      </article>

      {autres.length > 0 && (
        <section className="border-t border-brume bg-nuage py-16">
          <div className="container-g">
            <h2 className="h-display text-2xl md:text-3xl">À lire ensuite</h2>
            <div className="mt-8 grid gap-5 md:grid-cols-3">
              {autres.map((x, i) => (
                <Reveal key={x.slug} delay={i * 0.07}>
                  <Link
                    href={`/conseils/${x.slug}`}
                    className="group flex h-full flex-col rounded-2xl border border-brume bg-white p-6 transition-all duration-300 hover:-translate-y-1 hover:shadow-[0_26px_60px_-34px_rgba(51,54,66,.5)]"
                  >
                    <span className="font-mono text-xs text-soft">{x.categorie} · {x.lecture} min</span>
                    <h3 className="h-title mt-2 font-semibold leading-snug text-encre">{x.titre}</h3>
                  </Link>
                </Reveal>
              ))}
            </div>
            <div className="mt-10">
              <Link href="/conseils" className="btn-ghost">Tous les conseils</Link>
            </div>
          </div>
        </section>
      )}

      <CtaBand />
    </main>
  );
}
