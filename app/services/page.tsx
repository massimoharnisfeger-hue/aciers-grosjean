import type { Metadata } from "next";
import PageHeader from "@/components/ui/PageHeader";
import Etapes from "@/components/sections/Etapes";
import CtaBand from "@/components/sections/CtaBand";
import Reveal from "@/components/fx/Reveal";
import Parallax from "@/components/fx/Parallax";
import { services } from "@/lib/content";
import { ArtDecoupe, ArtAtelier, ArtStock } from "@/components/art/ProductArt";

export const metadata: Metadata = {
  title: "Services — Découpe, transformation, conseil | Aciers Grosjean",
  description:
    "Découpe sur mesure, transformation et façonnage, conseil technique, click & collect. On prépare votre acier pour que votre projet démarre plus vite.",
};

const icons = [
  "M4 12h10M14 12l-3-3M14 12l-3 3M17 5v14",
  "M12 3v4M12 17v4M5 12H3M21 12h-2M6 6l2 2M16 16l2 2M6 18l2-2M16 8l2-2",
  "M12 3a7 7 0 00-4 12.7V19h8v-3.3A7 7 0 0012 3zM9 22h6",
  "M6 6h15l-1.5 9h-12zM6 6L5 3H2M9 20a1 1 0 100 2 1 1 0 000-2zM17 20a1 1 0 100 2 1 1 0 000-2z",
];

export default function ServicesPage() {
  return (
    <main>
      <PageHeader
        surtitre="Services"
        titre={<>Bien plus qu'un <span className="mark-jaune">négociant</span></>}
        intro="On ne se contente pas de vendre l'acier : on le prépare pour que votre projet démarre plus vite et plus juste."
      />

      <section className="bg-white py-20 md:py-28">
        <div className="container-g grid gap-6 md:grid-cols-2">
          {services.map((s, i) => (
            <Reveal key={s.nom} delay={(i % 2) * 0.08}>
              <div className="flex h-full gap-5 rounded-2xl border border-brume bg-white p-7">
                <div className="flex h-14 w-14 shrink-0 items-center justify-center rounded-xl bg-encre">
                  <svg width="26" height="26" viewBox="0 0 24 24" fill="none" className="on-encre-jaune">
                    <path d={icons[i % icons.length]} stroke="currentColor" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round" />
                  </svg>
                </div>
                <div>
                  <h2 className="h-title text-xl font-semibold text-encre">{s.nom}</h2>
                  <p className="mt-2 font-body text-soft">{s.detail ?? s.desc}</p>
                </div>
              </div>
            </Reveal>
          ))}
        </div>
      </section>

      {/* Bande visuelle atelier */}
      <section className="bg-nuage py-20 md:py-28">
        <div className="container-g">
          <Reveal className="mb-10 max-w-2xl">
            <span className="font-body text-xs uppercase tracking-[0.2em] text-soft">L'atelier</span>
            <h2 className="h-display mt-3 text-3xl md:text-4xl">
              La matière préparée <span className="mark-jaune">avant votre chantier</span>
            </h2>
          </Reveal>
          <div className="grid gap-5 md:grid-cols-3">
            {[
              { A: ArtDecoupe, t: "Découpe aux cotes" },
              { A: ArtAtelier, t: "Structures & charpente" },
              { A: ArtStock, t: "Stock permanent" },
            ].map(({ A, t }, i) => (
              <Reveal key={t} delay={i * 0.08}>
                <div className="group overflow-hidden rounded-2xl border border-brume bg-white">
                  <div className="shine relative aspect-[4/3] overflow-hidden">
                    <Parallax amount={7} scale className="h-full w-full">
                      <A className="h-full w-full" />
                    </Parallax>
                  </div>
                  <p className="h-title p-5 font-semibold text-encre">{t}</p>
                </div>
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
