"use client";

import Reveal from "@/components/fx/Reveal";
import { publics } from "@/lib/content";

export default function Publics() {
  return (
    <section className="relative overflow-hidden bg-nuage py-24 md:py-32">
      <div className="grid-industrie pointer-events-none absolute inset-0 opacity-50" />
      <div className="container-g relative">
        <Reveal className="mb-14 max-w-2xl">
          <span className="font-body text-xs uppercase tracking-[0.2em] text-soft">
            Pour qui ?
          </span>
          <h2 className="h-display mt-3 text-4xl md:text-5xl">
            Le même acier, <span className="mark-jaune">pour tous</span>
          </h2>
        </Reveal>

        <div className="grid gap-6 md:grid-cols-2">
          {publics.map((p, i) => (
            <Reveal key={p.titre} delay={i * 0.1}>
              <div className="flex h-full flex-col rounded-2xl border border-brume bg-white p-8">
                <h3 className="h-title text-2xl font-semibold text-encre">{p.titre}</h3>
                <p className="mt-3 flex-1 font-body text-soft">{p.texte}</p>
                <ul className="mt-6 space-y-2">
                  {p.points.map((pt) => (
                    <li key={pt} className="flex items-center gap-3 font-body text-encre">
                      <span className="flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-jaune">
                        <svg width="12" height="12" viewBox="0 0 24 24" fill="none">
                          <path d="M5 13l4 4L19 7" stroke="#333642" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" />
                        </svg>
                      </span>
                      {pt}
                    </li>
                  ))}
                </ul>
              </div>
            </Reveal>
          ))}
        </div>
      </div>
    </section>
  );
}
