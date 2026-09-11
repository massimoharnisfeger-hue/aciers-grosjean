"use client";

import Reveal from "@/components/fx/Reveal";
import { depots } from "@/lib/content";

export default function Depots() {
  return (
    <section id="depots" className="bg-white py-24 md:py-32">
      <div className="container-g grid items-center gap-12 lg:grid-cols-2">
        <Reveal>
          <span className="font-body text-xs uppercase tracking-[0.2em] text-soft">
            Nos dépôts
          </span>
          <h2 className="h-display mt-3 text-4xl md:text-5xl">
            4 dépôts, <span className="mark-jaune">près de chez vous</span>
          </h2>
          <p className="mt-4 max-w-md font-body text-lg text-soft">
            Trois en Wallonie, un en France. Le retrait est souvent possible le
            jour même — vous récupérez vos pièces sans attendre.
          </p>

          <div className="mt-8 grid grid-cols-2 gap-3">
            {depots.map((d) => (
              <div key={d.ville} className="flex items-center gap-3 rounded-xl border border-brume bg-nuage px-4 py-3">
                <span className="flex h-9 w-9 items-center justify-center rounded-lg bg-jaune">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
                    <path d="M12 21s-7-6.3-7-11a7 7 0 1114 0c0 4.7-7 11-7 11z" stroke="#333642" strokeWidth="1.8" strokeLinejoin="round" />
                    <circle cx="12" cy="10" r="2.4" fill="#333642" />
                  </svg>
                </span>
                <div>
                  <div className="h-title font-semibold text-encre">{d.ville}</div>
                  <div className="font-body text-xs text-soft">{d.pays}</div>
                </div>
              </div>
            ))}
          </div>
        </Reveal>

        {/* Carte stylisée Wallonie + points */}
        <Reveal delay={0.1}>
          <div className="relative aspect-[4/3] overflow-hidden rounded-2xl border border-brume bg-encre">
            <div className="grid-industrie-dark absolute inset-0" />
            <svg viewBox="0 0 100 75" className="absolute inset-0 h-full w-full">
              <path
                d="M8,40 C18,28 30,30 40,26 C52,21 60,30 74,26 C86,23 92,34 90,44 C88,56 72,58 60,54 C48,50 40,58 28,54 C16,50 6,52 8,40 Z"
                fill="#AAB0B3" opacity="0.18" stroke="#AAB0B3" strokeWidth="0.5"
              />
              {[
                { x: 30, y: 44 },
                { x: 46, y: 50 },
                { x: 62, y: 40 },
                { x: 80, y: 52 },
              ].map((p, i) => (
                <g key={i}>
                  <circle cx={p.x} cy={p.y} r="2.6" fill="#FFD500" />
                  <circle cx={p.x} cy={p.y} r="6" fill="none" stroke="#FFD500" strokeWidth="0.6" opacity="0.5" />
                </g>
              ))}
            </svg>
            <div className="absolute bottom-4 left-4 rounded-lg bg-white/10 px-3 py-1.5 font-body text-xs text-white backdrop-blur">
              Wallonie · Hainaut & France
            </div>
          </div>
        </Reveal>
      </div>
    </section>
  );
}
