"use client";

import { motion } from "framer-motion";
import Link from "next/link";
import { trust } from "@/lib/content";
import { ArtStock, ArtPoutrelle, ArtTube, ArtDecoupe } from "@/components/art/ProductArt";

export default function Hero() {
  return (
    <section className="relative overflow-hidden bg-white pt-32 md:pt-40">
      <div className="grid-industrie pointer-events-none absolute inset-0 opacity-60" />
      <div className="pointer-events-none absolute -right-20 top-24 h-72 w-72 rounded-full bg-jaune/10 blur-[120px]" />

      <div className="container-g relative grid items-center gap-12 pb-16 md:grid-cols-2 md:pb-24">
        <div>
          <motion.div
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="mb-6 inline-flex items-center gap-2 rounded-full border border-brume bg-white px-4 py-1.5"
          >
            <span className="h-2 w-2 rounded-full bg-jaune" />
            <span className="font-body text-xs uppercase tracking-[0.15em] text-soft">
              Négoce &amp; transformation d'acier · depuis 40 ans
            </span>
          </motion.div>

          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7, delay: 0.05 }}
            className="h-display text-[9vw] leading-[1.02] md:text-6xl lg:text-7xl"
          >
            L'acier de pro,
            <br />
            <span className="mark-jaune">accessible à tous.</span>
          </motion.h1>

          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7, delay: 0.15 }}
            className="mt-6 max-w-md font-body text-lg text-soft"
          >
            Poutrelles, tôles, tubes, cornières, corten… Découpe sur mesure, devis en 24h et
            retrait le jour même dans l'un de nos 4 dépôts.
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7, delay: 0.25 }}
            className="mt-8 flex flex-col gap-3 sm:flex-row"
          >
            <Link href="/devis" className="btn-cta justify-center">
              Demander un devis
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
                <path d="M5 12h14M13 6l6 6-6 6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
              </svg>
            </Link>
            <Link href="/produits" className="btn-ghost justify-center">Voir les produits</Link>
          </motion.div>

          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.7, delay: 0.4 }}
            className="mt-6 font-body text-sm text-soft"
          >
            ✓ Sans engagement&nbsp;&nbsp;·&nbsp;&nbsp;✓ Particuliers &amp; pros&nbsp;&nbsp;·&nbsp;&nbsp;✓ Certifié EN1090-Exc2
          </motion.p>
        </div>

        {/* Composition visuelle */}
        <motion.div
          initial={{ opacity: 0, scale: 0.94 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.8, delay: 0.2, ease: [0.22, 1, 0.36, 1] }}
          className="group relative mx-auto w-full max-w-lg"
        >
          {/* carte principale : le dépôt */}
          <div className="shine relative aspect-[4/3] overflow-hidden rounded-2xl border border-brume bg-nuage shadow-[0_40px_90px_-50px_rgba(51,54,66,.6)]">
            <ArtStock className="h-full w-full transition-transform duration-700 group-hover:scale-[1.04]" />
            <span className="tag-stock absolute left-5 top-5 z-10">495 produits</span>
          </div>

          {/* vignettes flottantes */}
          <motion.div
            animate={{ y: [0, -10, 0] }}
            transition={{ duration: 5, repeat: Infinity, ease: "easeInOut" }}
            className="absolute -left-6 -bottom-10 w-40 overflow-hidden rounded-xl border border-brume bg-white shadow-xl md:-left-10"
          >
            <ArtPoutrelle className="h-24 w-full" />
            <p className="px-3 pb-2 font-body text-[11px] text-soft">Poutrelles IPE</p>
          </motion.div>

          <motion.div
            animate={{ y: [0, 10, 0] }}
            transition={{ duration: 6, repeat: Infinity, ease: "easeInOut", delay: 0.6 }}
            className="absolute -right-4 -top-8 w-36 overflow-hidden rounded-xl border border-brume bg-white shadow-xl md:-right-8"
          >
            <ArtTube className="h-24 w-full" />
            <p className="px-3 pb-2 font-body text-[11px] text-soft">Tubes &amp; profilés</p>
          </motion.div>

          <motion.div
            animate={{ y: [0, -8, 0] }}
            transition={{ duration: 7, repeat: Infinity, ease: "easeInOut", delay: 1.2 }}
            className="absolute -right-2 bottom-6 hidden w-32 overflow-hidden rounded-xl border border-encre/20 shadow-xl lg:block"
          >
            <ArtDecoupe className="h-20 w-full" />
            <p className="bg-encre px-3 py-1.5 font-body text-[11px] text-white">Découpe sur mesure</p>
          </motion.div>
        </motion.div>
      </div>

      {/* barre de confiance */}
      <div className="border-y border-brume bg-white">
        <div className="container-g flex flex-wrap items-center justify-center gap-x-8 gap-y-2 py-4 md:justify-between">
          {trust.map((t) => (
            <div key={t.label} className="flex items-baseline gap-2">
              <span className="h-title text-lg font-bold text-encre">{t.valeur}</span>
              <span className="font-body text-sm text-soft">{t.label}</span>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
