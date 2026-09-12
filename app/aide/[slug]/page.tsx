import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import CtaBand from "@/components/sections/CtaBand";
import Faq from "@/components/sections/Faq";
import Reveal from "@/components/fx/Reveal";
import FilAriane from "@/components/ui/FilAriane";
import { pagesAide, aideBySlug, type Bloc } from "@/lib/edito";
import { titre, description } from "@/lib/seo";

type Params = { slug: string };

export const dynamicParams = false;

export function generateStaticParams() {
  return pagesAide.map((p) => ({ slug: p.slug }));
}

export async function generateMetadata({ params }: { params: Promise<Params> }): Promise<Metadata> {
  const { slug } = await params;
  const p = aideBySlug(slug);
  if (!p) return { title: "Page introuvable | Aciers Grosjean" };
  return {
    title: titre(p.titreSeo),
    description: description(p.descSeo),
    alternates: { canonical: `/aide/${p.slug}` },
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
                <td key={j} className={`px-5 py-3.5 ${j === 0 ? "h-title font-semibold text-encre" : "font-mono text-sm tabular-nums text-soft"}`}>
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

export default async function AidePage({ params }: { params: Promise<Params> }) {
  const { slug } = await params;
  const p = aideBySlug(slug);
  if (!p) notFound();

  const autres = pagesAide.filter((x) => x.slug !== p.slug);

  return (
    <main>
      <header className="relative overflow-hidden border-b border-brume bg-nuage pt-32 md:pt-40">
        <div className="grid-industrie pointer-events-none absolute inset-0 opacity-60" />
        <div className="container-g relative pb-12 md:pb-16">
          <div className="mb-5">
            <FilAriane items={[{ label: "Aide", href: "/aide/faq" }, { label: p.titre }]} />
          </div>
          <h1 className="h-display max-w-3xl text-3xl md:text-5xl">{p.titre}</h1>
          <p className="mt-4 max-w-2xl font-body text-lg text-soft">{p.chapo}</p>
        </div>
      </header>

      {p.slug === "faq" ? (
        <Faq />
      ) : (
        <section className="bg-white py-14 md:py-20">
          <div className="container-g max-w-[46rem]">
            {p.sections.map((s, i) => (
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
          </div>
        </section>
      )}

      <section className="border-t border-brume bg-nuage py-14">
        <div className="container-g">
          <h2 className="h-title text-sm font-semibold uppercase tracking-[0.14em] text-soft">
            Autres pages d'aide
          </h2>
          <div className="mt-5 flex flex-wrap gap-3">
            {autres.map((a) => (
              <Link
                key={a.slug}
                href={`/aide/${a.slug}`}
                className="rounded-full border border-brume bg-white px-4 py-2 font-body text-sm text-encre transition-colors hover:border-encre"
              >
                {a.titre}
              </Link>
            ))}
            <Link href="/contact" className="rounded-full border border-encre bg-encre px-4 py-2 font-body text-sm text-white transition-opacity hover:opacity-90">
              Nous contacter
            </Link>
          </div>
        </div>
      </section>

      <CtaBand />
    </main>
  );
}
