"use client";

import { useState } from "react";
import { AnimatePresence, motion } from "framer-motion";
import Reveal from "@/components/fx/Reveal";
import Parallax from "@/components/fx/Parallax";
import { realisations } from "@/lib/content";
import {
  ArtAtelier,
  ArtDecoupe,
  ArtStock,
  ArtPoutrelle,
  ArtCorten,
  ArtTube,
} from "@/components/art/ProductArt";

const scenes = [ArtAtelier, ArtDecoupe, ArtStock, ArtCorten, ArtPoutrelle, ArtTube];

export default function Realisations() {
  const [open, setOpen] = useState<number | null>(null);
  const Active = open !== null ? scenes[open % scenes.length] : null;

  return (
    <section className="bg-nuage py-24 md:py-32">
      <div className="container-g">
        <Reveal className="mb-12 max-w-2xl">
          <span className="font-body text-xs uppercase tracking-[0.2em] text-soft">Réalisations</span>
          <h2 className="h-display mt-3 text-4xl md:text-5xl">
            Ce que devient <span className="mark-jaune">notre acier</span>
          </h2>
          <p className="mt-4 font-body text-lg text-soft">
            Des projets de pros comme de particuliers. Cliquez pour agrandir.
          </p>
        </Reveal>

        <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
          {realisations.map((r, i) => {
            const Art = scenes[i % scenes.length];
            return (
              <Reveal key={r.titre} delay={(i % 3) * 0.08}>
                <button
                  onClick={() => setOpen(i)}
                  className="group block w-full overflow-hidden rounded-2xl border border-brume bg-white text-left"
                  aria-label={`Agrandir : ${r.titre}`}
                >
                  <div className="shine relative aspect-[4/3] overflow-hidden">
                    <Parallax amount={8} scale className="h-full w-full">
                      <Art className="h-full w-full transition-transform duration-700 group-hover:scale-105" />
                    </Parallax>
                    <span className="tag-stock absolute left-4 top-4 z-10">{r.tag}</span>
                    <span className="absolute bottom-4 right-4 z-10 flex h-10 w-10 translate-y-2 items-center justify-center rounded-full bg-white/90 opacity-0 backdrop-blur transition-all duration-300 group-hover:translate-y-0 group-hover:opacity-100">
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                        <path d="M21 21l-4.3-4.3M11 19a8 8 0 100-16 8 8 0 000 16zM11 8v6M8 11h6" stroke="#333642" strokeWidth="1.8" strokeLinecap="round" />
                      </svg>
                    </span>
                  </div>
                  <div className="p-5">
                    <h3 className="h-title font-semibold text-encre">{r.titre}</h3>
                  </div>
                </button>
              </Reveal>
            );
          })}
        </div>
      </div>

      {/* Lightbox */}
      <AnimatePresence>
        {Active && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={() => setOpen(null)}
            className="fixed inset-0 z-[9998] flex items-center justify-center bg-encre/85 p-6 backdrop-blur-md"
          >
            <motion.div
              initial={{ scale: 0.9, opacity: 0, y: 20 }}
              animate={{ scale: 1, opacity: 1, y: 0 }}
              exit={{ scale: 0.94, opacity: 0 }}
              transition={{ duration: 0.4, ease: [0.22, 1, 0.36, 1] }}
              className="w-full max-w-3xl overflow-hidden rounded-2xl bg-white"
            >
              <Active className="aspect-[4/3] w-full" />
              <div className="flex items-center justify-between p-5">
                <h3 className="h-title text-lg font-semibold text-encre">
                  {realisations[open!].titre}
                </h3>
                <span className="tag-stock">{realisations[open!].tag}</span>
              </div>
            </motion.div>
            <button
              onClick={() => setOpen(null)}
              aria-label="Fermer"
              className="absolute right-6 top-6 flex h-12 w-12 items-center justify-center rounded-full bg-white text-encre"
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                <path d="M6 6l12 12M18 6L6 18" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
              </svg>
            </button>
          </motion.div>
        )}
      </AnimatePresence>
    </section>
  );
}
