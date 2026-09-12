import type { Metadata } from "next";
import PageHeader from "@/components/ui/PageHeader";
import Counters from "@/components/fx/Counters";
import CtaBand from "@/components/sections/CtaBand";
import Reveal from "@/components/fx/Reveal";
import { histoire } from "@/lib/content";
import { ArtAtelier } from "@/components/art/ProductArt";

export const metadata: Metadata = {
  title: "À propos — 40 ans d'expertise acier | Aciers Grosjean",
  description:
    "Entreprise familiale wallonne, près de 40 ans d'expertise acier, 4 dépôts, certification EN1090-Exc2. L'acier de pro, accessible à tous.",
  alternates: { canonical: "/a-propos" },
};

export default function AProposPage() {
  return (
    <main>
      <PageHeader
        surtitre="À propos"
        titre={<>40 ans à rendre l'acier <span className="mark-jaune">accessible</span></>}
      />

      <section className="bg-white py-20 md:py-28">
        <div className="container-g grid items-center gap-12 lg:grid-cols-2">
          <Reveal>
            <p className="font-body text-lg leading-relaxed text-soft">{histoire.intro}</p>
            <div className="mt-8 inline-flex items-center gap-3 rounded-xl bg-encre p-5">
              <span className="tag-stock">EN1090-Exc2</span>
              <span className="font-body text-sm text-soft-light">Une exigence que peu affichent dans notre secteur.</span>
            </div>
          </Reveal>
          <Reveal delay={0.1}>
            <div className="group relative aspect-square overflow-hidden rounded-2xl border border-brume bg-nuage">
              <div className="shine absolute inset-0">
                <ArtAtelier className="h-full w-full transition-transform duration-700 group-hover:scale-105" />
              </div>
              <span className="absolute bottom-5 left-5 h-1 w-16 rounded-full bg-jaune" />
            </div>
          </Reveal>
        </div>
      </section>

      <section className="bg-nuage py-20 md:py-28">
        <div className="container-g">
          <Reveal className="mb-12 max-w-2xl">
            <span className="font-body text-xs uppercase tracking-[0.2em] text-soft">Nos valeurs</span>
            <h2 className="h-display mt-3 text-4xl md:text-5xl">Ce qui nous <span className="mark-jaune">tient</span></h2>
          </Reveal>
          <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
            {histoire.valeurs.map((v, i) => (
              <Reveal key={v.titre} delay={(i % 4) * 0.08}>
                <div className="h-full rounded-2xl border border-brume bg-white p-6">
                  <span className="flex h-10 w-10 items-center justify-center rounded-lg bg-jaune font-title font-bold text-encre">{i + 1}</span>
                  <h3 className="h-title mt-4 text-lg font-semibold text-encre">{v.titre}</h3>
                  <p className="mt-2 font-body text-sm text-soft">{v.texte}</p>
                </div>
              </Reveal>
            ))}
          </div>
        </div>
      </section>

      <Counters />
      <CtaBand />
    </main>
  );
}
