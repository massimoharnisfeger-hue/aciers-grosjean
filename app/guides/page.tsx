import type { Metadata } from "next";
import Link from "next/link";
import PageHeader from "@/components/ui/PageHeader";
import CtaBand from "@/components/sections/CtaBand";
import Reveal from "@/components/fx/Reveal";
import { guides } from "@/lib/edito";

export const metadata: Metadata = {
  title: "Guides acier — choisir, calculer, construire | Aciers Grosjean",
  description:
    "Les réponses aux questions qu'on nous pose au comptoir : galvanisé ou inox, quelle poutrelle, quelle épaisseur de tôle, comment souder. Écrit par des négociants, pas par des vendeurs.",
  alternates: { canonical: "/guides" },
};

export default function GuidesPage() {
  const categories = Array.from(new Set(guides.map((g) => g.categorie)));

  return (
    <main>
      <PageHeader
        surtitre="Guides"
        titre={
          <>
            Les réponses qu'on donne <span className="mark-jaune">au comptoir</span>
          </>
        }
        intro="Quarante ans de questions de clients, réunies ici. Pas de blabla : ce qu'il faut savoir pour choisir juste, et ce qu'on vous dirait au téléphone."
      />

      <section className="bg-white py-16 md:py-24">
        <div className="container-g">
          {categories.map((cat) => (
            <div key={cat} className="mb-16 last:mb-0">
              <h2 className="h-title mb-6 text-sm font-semibold uppercase tracking-[0.14em] text-soft">
                {cat}
              </h2>
              <div className="grid gap-5 md:grid-cols-2">
                {guides
                  .filter((g) => g.categorie === cat)
                  .map((g, i) => (
                    <Reveal key={g.slug} delay={(i % 2) * 0.08}>
                      <Link
                        href={`/guides/${g.slug}`}
                        className="group flex h-full flex-col rounded-2xl border border-brume bg-white p-7 transition-all duration-300 hover:-translate-y-1 hover:border-encre/20 hover:shadow-[0_28px_64px_-36px_rgba(51,54,66,.55)]"
                      >
                        <span className="font-mono text-xs text-soft">
                          {g.lecture} min de lecture
                        </span>
                        <h3 className="h-title mt-3 text-xl font-semibold leading-snug text-encre">
                          {g.titre}
                        </h3>
                        <p className="mt-3 flex-1 font-body leading-relaxed text-soft">{g.chapo}</p>
                        <span className="mt-6 inline-flex items-center gap-2 font-body text-sm font-medium text-encre">
                          Lire le guide
                          <svg
                            width="15" height="15" viewBox="0 0 24 24" fill="none"
                            className="transition-transform group-hover:translate-x-1"
                          >
                            <path d="M5 12h14M13 6l6 6-6 6" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round" />
                          </svg>
                        </span>
                      </Link>
                    </Reveal>
                  ))}
              </div>
            </div>
          ))}
        </div>
      </section>

      <CtaBand />
    </main>
  );
}
