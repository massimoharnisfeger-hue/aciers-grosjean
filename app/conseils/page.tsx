import type { Metadata } from "next";
import Link from "next/link";
import PageHeader from "@/components/ui/PageHeader";
import CtaBand from "@/components/sections/CtaBand";
import Reveal from "@/components/fx/Reveal";
import { articles, categoriesArticles } from "@/lib/edito";

export const metadata: Metadata = {
  title: "Conseils acier — guides, matières et marché",
  description:
    "Guides d'achat, fiches matière et analyses de marché écrits par des négociants : corten, caillebotis, panneaux isolés, prix de l'acier en Belgique.",
  alternates: { canonical: "/conseils" },
};

export default function ConseilsPage() {
  const une = articles[0];

  return (
    <main>
      <PageHeader
        surtitre="Conseils"
        titre={
          <>
            Les réponses qu'on donne <span className="mark-jaune">au comptoir</span>
          </>
        }
        intro="Guides d'achat, fiches matière, analyses de marché. Écrits par des gens qui vendent l'acier tous les jours, pas par une agence."
      />

      <section className="bg-white py-14 md:py-20">
        <div className="container-g">
          {/* à la une */}
          <Reveal>
            <Link
              href={`/conseils/${une.slug}`}
              className="group relative flex flex-col justify-end overflow-hidden rounded-2xl bg-encre p-8 md:p-12"
            >
              <div className="grid-industrie-dark pointer-events-none absolute inset-0" />
              <div className="pointer-events-none absolute -right-10 -top-10 h-64 w-64 rounded-full bg-jaune/15 blur-[90px]" />
              <div className="relative max-w-2xl">
                <span className="font-body text-xs uppercase tracking-[0.2em] text-white/50">
                  {une.categorie} · {une.lecture} min · {une.date}
                </span>
                <h2 className="h-display mt-4 text-3xl leading-tight text-white md:text-4xl">{une.titre}</h2>
                <p className="mt-4 font-body text-soft-light">{une.chapo}</p>
                <span className="on-encre-jaune mt-7 inline-flex items-center gap-2 font-body text-sm font-medium">
                  Lire l'article
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" aria-hidden="true"
                    className="transition-transform group-hover:translate-x-1">
                    <path d="M5 12h14M13 6l6 6-6 6" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round" />
                  </svg>
                </span>
              </div>
            </Link>
          </Reveal>

          {/* par catégorie */}
          {categoriesArticles.map((cat) => {
            const liste = articles.filter((a) => a.categorie === cat && a.slug !== une.slug);
            if (!liste.length) return null;
            return (
              <div key={cat} className="mt-16">
                <h2 className="h-title mb-6 text-sm font-semibold uppercase tracking-[0.14em] text-soft">
                  {cat}
                  <span className="ml-2 font-mono text-xs">{liste.length}</span>
                </h2>
                <div className="grid gap-5 md:grid-cols-2 lg:grid-cols-3">
                  {liste.map((a, i) => (
                    <Reveal key={a.slug} delay={(i % 3) * 0.06}>
                      <Link
                        href={`/conseils/${a.slug}`}
                        className="group flex h-full flex-col rounded-2xl border border-brume bg-white p-6 transition-all duration-300 hover:-translate-y-1 hover:border-encre/20 hover:shadow-[0_28px_64px_-36px_rgba(51,54,66,.55)]"
                      >
                        <span className="font-mono text-xs text-soft">
                          {a.lecture} min · {a.date}
                        </span>
                        <h3 className="h-title mt-2.5 text-lg font-semibold leading-snug text-encre">
                          {a.titre}
                        </h3>
                        <p className="mt-2.5 flex-1 font-body text-sm leading-relaxed text-soft">{a.chapo}</p>
                        <span className="mt-5 h-px w-6 bg-jaune transition-all duration-300 group-hover:w-12" />
                      </Link>
                    </Reveal>
                  ))}
                </div>
              </div>
            );
          })}
        </div>
      </section>

      <CtaBand />
    </main>
  );
}
