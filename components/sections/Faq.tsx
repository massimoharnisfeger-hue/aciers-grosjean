"use client";

import { useState } from "react";
import { AnimatePresence, motion } from "framer-motion";
import Reveal from "@/components/fx/Reveal";
import { faq } from "@/lib/content";

export default function Faq() {
  const [open, setOpen] = useState<number | null>(0);

  return (
    <section id="faq" className="bg-nuage py-24 md:py-32">
      <div className="container-g grid gap-12 lg:grid-cols-[0.8fr_1.2fr]">
        <Reveal>
          <span className="font-body text-xs uppercase tracking-[0.2em] text-soft">
            Questions fréquentes
          </span>
          <h2 className="h-display mt-3 text-4xl md:text-5xl">
            On répond <span className="mark-jaune">sans jargon</span>
          </h2>
          <p className="mt-4 font-body text-soft">
            Une autre question ? Notre équipe vous répond directement — et vous
            oriente vers le bon produit.
          </p>
        </Reveal>

        <Reveal delay={0.1}>
          <div className="divide-y divide-brume rounded-2xl border border-brume bg-white">
            {faq.map((item, i) => {
              const isOpen = open === i;
              return (
                <div key={i}>
                  <button
                    onClick={() => setOpen(isOpen ? null : i)}
                    className="flex w-full items-center justify-between gap-4 px-6 py-5 text-left"
                    aria-expanded={isOpen}
                  >
                    <span className="h-title font-semibold text-encre">{item.q}</span>
                    <span
                      className={`flex h-7 w-7 shrink-0 items-center justify-center rounded-full transition-all duration-300 ${
                        isOpen ? "rotate-45 bg-jaune" : "bg-nuage"
                      }`}
                    >
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                        <path d="M12 5v14M5 12h14" stroke="#333642" strokeWidth="2" strokeLinecap="round" />
                      </svg>
                    </span>
                  </button>
                  <AnimatePresence initial={false}>
                    {isOpen && (
                      <motion.div
                        initial={{ height: 0, opacity: 0 }}
                        animate={{ height: "auto", opacity: 1 }}
                        exit={{ height: 0, opacity: 0 }}
                        transition={{ duration: 0.3, ease: [0.22, 1, 0.36, 1] }}
                        className="overflow-hidden"
                      >
                        <p className="px-6 pb-5 font-body text-soft">{item.r}</p>
                      </motion.div>
                    )}
                  </AnimatePresence>
                </div>
              );
            })}
          </div>
        </Reveal>
      </div>
    </section>
  );
}
