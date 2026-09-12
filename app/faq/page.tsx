import type { Metadata } from "next";
import Link from "next/link";
import PageHeader from "@/components/ui/PageHeader";
import CtaBand from "@/components/sections/CtaBand";
import Faq from "@/components/sections/Faq";
import { faq } from "@/lib/content";
import { articles } from "@/lib/edito";

export const metadata: Metadata = {
  title: "Questions fréquentes — acheter de l'acier quand on n'est pas du métier",
  description:
    "Faut-il être professionnel ? Livrez-vous ? En combien de temps un devis ? Galvanisé ou inox ? Les réponses aux questions qu'on nous pose tous les jours au comptoir.",
  alternates: { canonical: "/faq" },
};

export default function FaqPage() {
  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    mainEntity: faq.map((f) => ({
      "@type": "Question",
      name: f.q,
      acceptedAnswer: { "@type": "Answer", text: f.r },
    })),
  };

  return (
    <main>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }} />

      <PageHeader
        surtitre="FAQ"
        titre={
          <>
            Les questions <span className="mark-jaune">qu'on nous pose</span>
          </>
        }
        intro="Aucune question n'est trop simple. Celles-ci reviennent tellement souvent qu'elles méritaient une page."
      />

      <Faq />

      <section className="bg-white py-16 md:py-20">
        <div className="container-g">
          <h2 className="h-display text-2xl md:text-3xl">Des réponses plus longues</h2>
          <p className="mt-3 max-w-xl font-body text-soft">
            Certaines questions demandent plus de trois lignes. On leur a consacré un guide
            complet.
          </p>
          <div className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            {articles.slice(0, 4).map((g) => (
              <Link
                key={g.slug}
                href={`/conseils/${g.slug}`}
                className="group flex h-full flex-col rounded-2xl border border-brume bg-white p-6 transition-all duration-300 hover:-translate-y-1 hover:shadow-[0_26px_60px_-34px_rgba(51,54,66,.5)]"
              >
                <span className="font-mono text-xs text-soft">{g.lecture} min</span>
                <h3 className="h-title mt-2 flex-1 font-semibold leading-snug text-encre">{g.titre}</h3>
                <span className="mt-4 h-px w-6 bg-jaune transition-all duration-300 group-hover:w-10" />
              </Link>
            ))}
          </div>
          <div className="mt-8">
            <Link href="/conseils" className="btn-ghost">Tous les conseils</Link>
          </div>
        </div>
      </section>

      <CtaBand />
    </main>
  );
}
