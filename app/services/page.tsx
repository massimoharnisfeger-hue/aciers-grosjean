import type { Metadata } from "next";
import Link from "next/link";
import PageHeader from "@/components/ui/PageHeader";
import Etapes from "@/components/sections/Etapes";
import CtaBand from "@/components/sections/CtaBand";
import Reveal from "@/components/fx/Reveal";
import Parallax from "@/components/fx/Parallax";
import Tilt from "@/components/fx/Tilt";
import { servicesDetail } from "@/lib/edito";
import { ArtDecoupe, ArtAtelier, ArtStock } from "@/components/art/ProductArt";

export const metadata: Metadata = {
  title: "Découpe, pliage et transformation acier sur mesure",
  description:
    "Découpe aux cotes dès 2,50 €, pliage jusqu'à 3 m, perçage sur plan, soudure certifiée EN 1090-Exc2, galvanisation et retrait en dépôt.",
  alternates: { canonical: "/services" },
};

export default function ServicesPage() {
  return (
    <main>
      <PageHeader
        surtitre="Services"
        titre={
          <>
            On ne vend pas que l’acier, <span className="mark-jaune">on le prépare</span>
          </>
        }
        intro="Entre la barre de 6 mètres et la pièce prête à souder, il y a six services. C'est là que se joue la différence entre un négociant et un rayon de grande surface."
      />

      <section className="bg-white py-16 md:py-24">
        <div className="container-g">
          <div className="grid gap-5 md:grid-cols-2 lg:grid-cols-3">
            {servicesDetail.map((s, i) => (
              <Reveal key={s.slug} delay={(i % 3) * 0.07}>
                <Tilt className="group h-full" intensity={6}>
                  <Link
                    href={`/services/${s.slug}`}
                    className="lift flex h-full flex-col rounded-2xl border border-brume bg-white p-7"
                  >
                    <span className="font-mono text-xs text-soft">
                      {String(i + 1).padStart(2, "0")}
                    </span>
                    <h2 className="h-title mt-3 text-xl font-semibold text-encre">{s.nom}</h2>
                    <p className="mt-1.5 font-body text-sm text-soft">{s.accroche}</p>
                    <p className="mt-4 flex-1 font-body leading-relaxed text-soft">
                      {s.intro.split(". ")[0]}.
                    </p>
                    <div className="mt-6 flex items-end justify-between border-t border-brume pt-4">
                      <div>
                        <span className="block font-body text-[11px] uppercase tracking-[0.1em] text-soft">
                          Tarif
                        </span>
                        <span className="h-title text-sm font-semibold text-encre">{s.prix}</span>
                      </div>
                      <span className="glow-jaune flex h-10 w-10 items-center justify-center rounded-full bg-jaune text-encre transition-transform duration-300 group-hover:rotate-45">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                          <path d="M7 17L17 7M9 7h8v8" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round" />
                        </svg>
                      </span>
                    </div>
                  </Link>
                </Tilt>
              </Reveal>
            ))}
          </div>
        </div>
      </section>

      {/* Bande visuelle atelier */}
      <section className="border-y border-brume bg-nuage py-20 md:py-24">
        <div className="container-g">
          <Reveal className="mb-10 max-w-2xl">
            <span className="font-body text-xs uppercase tracking-[0.2em] text-soft">L’atelier</span>
            <h2 className="h-display mt-3 text-3xl md:text-4xl">
              La matière préparée <span className="mark-jaune">avant votre chantier</span>
            </h2>
          </Reveal>
          <div className="grid gap-5 md:grid-cols-3">
            {[
              { A: ArtDecoupe, t: "Découpe aux cotes", h: "/services/decoupe" },
              { A: ArtAtelier, t: "Transformation sur plan", h: "/services/transformation" },
              { A: ArtStock, t: "Stock permanent", h: "/produits" },
            ].map(({ A, t, h }, i) => (
              <Reveal key={t} delay={i * 0.08}>
                <Link href={h} className="group block overflow-hidden rounded-2xl border border-brume bg-white">
                  <div className="shine relative aspect-[4/3] overflow-hidden">
                    <Parallax amount={7} scale className="h-full w-full">
                      <A className="h-full w-full" />
                    </Parallax>
                  </div>
                  <p className="h-title p-5 font-semibold text-encre">{t}</p>
                </Link>
              </Reveal>
            ))}
          </div>
        </div>
      </section>

      <Etapes />
      <CtaBand />
    </main>
  );
}
