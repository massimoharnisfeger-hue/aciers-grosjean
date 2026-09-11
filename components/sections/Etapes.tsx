"use client";

import Reveal from "@/components/fx/Reveal";
import { etapes } from "@/lib/content";

export default function Etapes() {
  return (
    <section className="bg-nuage py-24 md:py-32">
      <div className="container-g">
        <Reveal className="mb-14 max-w-2xl">
          <span className="font-body text-xs uppercase tracking-[0.2em] text-soft">
            Comment ça marche
          </span>
          <h2 className="h-display mt-3 text-4xl md:text-5xl">
            De l'idée au retrait, en <span className="mark-jaune">4 étapes</span>
          </h2>
        </Reveal>

        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
          {etapes.map((e, i) => (
            <Reveal key={e.n} delay={i * 0.1}>
              <div className="relative rounded-2xl border border-brume bg-white p-7">
                <span className="h-title text-5xl font-bold text-brume">{e.n}</span>
                <h3 className="h-title mt-3 text-xl font-semibold text-encre">{e.titre}</h3>
                <p className="mt-2 font-body text-sm text-soft">{e.texte}</p>
                <span className="absolute right-6 top-7 h-1.5 w-8 rounded-full bg-jaune" />
              </div>
            </Reveal>
          ))}
        </div>
      </div>
    </section>
  );
}
