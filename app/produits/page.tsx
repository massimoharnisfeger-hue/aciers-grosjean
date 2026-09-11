import type { Metadata } from "next";
import PageHeader from "@/components/ui/PageHeader";
import CtaBand from "@/components/sections/CtaBand";
import Reveal from "@/components/fx/Reveal";
import { categories } from "@/lib/content";
import { productArt, ArtPoutrelle } from "@/components/art/ProductArt";

export const metadata: Metadata = {
  title: "Catalogue acier — Poutrelles, tubes, tôles, cornières | Aciers Grosjean",
  description:
    "Plus de 500 références en stock : poutrelles IPE/HEA/HEB, tubes, tôles, cornières, plats, acier corten, treillis. Découpe sur mesure. Prix négociant.",
};

export default function ProduitsPage() {
  return (
    <main>
      <PageHeader
        surtitre="Produits"
        titre={<>Le catalogue <span className="mark-jaune">acier</span></>}
        intro="Plus de 500 références en stock, toutes disponibles à la découpe sur mesure. Voici les grandes familles — demandez un devis pour un tarif précis."
      />

      <section className="bg-white py-20 md:py-28">
        <div className="container-g space-y-20">
          {categories.map((cat, ci) => {
            const Art = productArt[cat.slug] ?? ArtPoutrelle;
            return (
            <div key={cat.slug} id={cat.slug} className="scroll-mt-28">
              <div className="group mb-8 grid items-center gap-8 md:grid-cols-[1.1fr_0.9fr]">
                <Reveal className="flex flex-col gap-2 border-l-4 border-jaune pl-5">
                  <h2 className="h-display text-3xl md:text-4xl">{cat.titre}</h2>
                  <p className="max-w-2xl font-body text-soft">{cat.intro}</p>
                </Reveal>
                <Reveal delay={0.1} className={ci % 2 ? "md:order-first" : ""}>
                  <div className="shine relative aspect-[4/3] overflow-hidden rounded-2xl border border-brume bg-nuage">
                    <div className="absolute inset-0 grid-industrie opacity-70" />
                    <Art className="absolute inset-0 h-full w-full transition-transform duration-700 group-hover:scale-105" />
                  </div>
                </Reveal>
              </div>
              <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
                {cat.refs.map((r, i) => (
                  <Reveal key={r.nom} delay={(i % 4) * 0.06}>
                    <div className="flex h-full flex-col rounded-xl border border-brume bg-white p-5 transition-all duration-300 hover:-translate-y-1 hover:shadow-[0_20px_50px_-30px_rgba(51,54,66,0.4)]">
                      <span className="tag-stock w-fit">En stock</span>
                      <h3 className="h-title mt-3 font-semibold text-encre">{r.nom}</h3>
                      <p className="font-body text-sm text-soft">{r.dim}</p>
                      <p className="h-title mt-3 border-t border-brume pt-3 font-bold text-encre">{r.prix}</p>
                    </div>
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
