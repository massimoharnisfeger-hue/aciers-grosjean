import type { Metadata } from "next";
import Link from "next/link";
import PageHeader from "@/components/ui/PageHeader";
import CtaBand from "@/components/sections/CtaBand";
import Reveal from "@/components/fx/Reveal";
import { univers, noeuds, produitsSous, formatPrix } from "@/lib/catalogue";

export const metadata: Metadata = {
  title: "Nouveautés — les derniers produits entrés au catalogue | Aciers Grosjean",
  description:
    "Les dernières références ajoutées au catalogue, univers par univers : acier, inox, aluminium, toiture, jardin et quincaillerie.",
  alternates: { canonical: "/nouveautes" },
};

export default function NouveautesPage() {
  return (
    <main>
      <PageHeader
        surtitre="Nouveautés"
        titre={<>Derniers arrivés <span className="mark-jaune">au catalogue</span></>}
        intro="Les références entrées récemment en stock, univers par univers. Tout est disponible au retrait comme le reste du catalogue."
      />

      <section className="bg-white py-14 md:py-20">
        <div className="container-g space-y-14">
          {univers.map((u) => {
            const derniers = produitsSous(`/${u.slug}`).slice(-4);
            if (!derniers.length) return null;
            return (
              <div key={u.slug}>
                <div className="mb-6 flex flex-wrap items-baseline justify-between gap-3">
                  <h2 className="h-display text-2xl md:text-3xl">{u.nom}</h2>
                  <Link href={`/${u.slug}`} className="font-body text-sm text-encre hover:text-jaune">
                    Voir tout l&apos;univers →
                  </Link>
                </div>
                <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
                  {derniers.map((p, i) => (
                    <Reveal key={p.slug} delay={(i % 4) * 0.06}>
                      <Link
                        href={`/p/${p.slug}`}
                        className="group flex h-full flex-col justify-between rounded-2xl border border-brume bg-white p-6 transition-all duration-300 hover:-translate-y-1 hover:shadow-[0_26px_60px_-34px_rgba(51,54,66,.5)]"
                      >
                        <div>
                          <span className="tag-stock">En stock</span>
                          <h3 className="h-title mt-3 font-semibold leading-snug text-encre">{p.nom}</h3>
                          <p className="mt-1 font-mono text-xs text-soft">{noeuds[p.categorie]?.nom}</p>
                        </div>
                        <span className="h-title mt-6 text-lg font-bold tabular-nums text-encre">
                          {formatPrix(p.prix)}
                        </span>
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
