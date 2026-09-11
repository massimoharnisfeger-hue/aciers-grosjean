"use client";

import Link from "next/link";
import Reveal from "@/components/fx/Reveal";
import Tilt from "@/components/fx/Tilt";
import { familles, totalRefs } from "@/lib/catalogue";
import { productArt, ArtPoutrelle } from "@/components/art/ProductArt";

export default function Produits() {
  return (
    <section id="produits" className="relative bg-white py-24 md:py-32">
      <div className="container-g">
        <Reveal className="mb-14 max-w-2xl">
          <span className="font-body text-xs uppercase tracking-[0.2em] text-soft">Le catalogue</span>
          <h2 className="h-display mt-3 text-4xl md:text-5xl">
            Des produits <span className="mark-jaune">en stock</span>, prêts à partir
          </h2>
          <p className="mt-4 font-body text-lg text-soft">
            {familles.length} familles, {totalRefs} références, un prix au mètre affiché sur
            chaque fiche. Tout se coupe aux cotes exactes, avec retrait le jour même.
          </p>
        </Reveal>

        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {familles.slice(0, 6).map((f, i) => {
            const Art = productArt[f.art] ?? ArtPoutrelle;
            return (
              <Reveal key={f.slug} delay={(i % 3) * 0.08}>
                <Tilt className="group h-full" intensity={7}>
                  <Link
                    href={`/produits/${f.slug}`}
                    className="lift flex h-full flex-col overflow-hidden rounded-2xl border border-brume bg-white"
                  >
                    <div className="shine relative aspect-[4/3] overflow-hidden bg-nuage">
                      <div className="absolute inset-0 grid-industrie opacity-70" />
                      <Art className="absolute inset-0 h-full w-full transition-transform duration-700 group-hover:scale-[1.07]" />
                      <span className="tag-stock absolute left-4 top-4 z-10">En stock</span>
                    </div>

                    <div className="flex flex-1 flex-col p-6" style={{ transform: "translateZ(40px)" }}>
                      <h3 className="h-title text-xl font-semibold text-encre">{f.nom}</h3>
                      <p className="mt-2 flex-1 font-body text-sm text-soft">{f.accroche}</p>
                      <div className="mt-5 flex items-center justify-between border-t border-brume pt-4">
                        <span className="font-mono text-xs text-soft">
                          {f.refs.length} référence{f.refs.length > 1 ? "s" : ""}
                        </span>
                        <span className="glow-jaune flex h-10 w-10 items-center justify-center rounded-full bg-jaune text-encre transition-transform duration-300 group-hover:rotate-45">
                          <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                            <path d="M7 17L17 7M9 7h8v8" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round" />
                          </svg>
                        </span>
                      </div>
                    </div>
                  </Link>
                </Tilt>
              </Reveal>
            );
          })}
        </div>

        <div className="mt-12 flex justify-center">
          <Link href="/produits" className="btn-ghost">
            Voir tout le catalogue
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
              <path d="M5 12h14M13 6l6 6-6 6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
          </Link>
        </div>
      </div>
    </section>
  );
}
