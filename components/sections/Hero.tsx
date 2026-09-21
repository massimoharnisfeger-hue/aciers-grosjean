import type { CSSProperties } from "react";
import Link from "next/link";
import { trust } from "@/lib/content";
import { ArtStock, ArtPoutrelle, ArtTube, ArtDecoupe } from "@/components/art/ProductArt";

// Animations en CSS (globals.css : .apparait, .flotte) : le titre s'affiche dès
// le premier rendu, sans attendre le JavaScript.
const delai = (s: number) => ({ "--delai": `${s}s` }) as CSSProperties;
const flotte = (duree: number, amplitude: number, decalage = 0) =>
  ({ "--duree": `${duree}s`, "--amplitude": `${amplitude}px`, "--delai": `${decalage}s` }) as CSSProperties;

export default function Hero() {
  return (
    <section className="relative overflow-hidden bg-white pt-32 md:pt-40">
      <div className="grid-industrie pointer-events-none absolute inset-0 opacity-60" />
      <div className="pointer-events-none absolute -right-20 top-24 h-72 w-72 rounded-full bg-jaune/10 blur-[120px]" />

      <div className="container-g relative grid items-center gap-12 pb-16 md:grid-cols-2 md:pb-24">
        <div>
          <div
            className="apparait mb-6 inline-flex items-center gap-2 rounded-full border border-brume bg-white px-4 py-1.5"
            style={delai(0)}
          >
            <span className="h-2 w-2 rounded-full bg-jaune" />
            <span className="font-body text-xs uppercase tracking-[0.15em] text-soft">
              Négoce &amp; transformation d’acier · depuis 40 ans
            </span>
          </div>

          <h1
            className="apparait h-display text-[9vw] leading-[1.02] md:text-6xl lg:text-7xl"
            style={delai(0.05)}
          >
            L’acier de pro,
            <br />
            <span className="mark-jaune">accessible à tous.</span>
          </h1>

          <p className="apparait mt-6 max-w-md font-body text-lg text-soft" style={delai(0.15)}>
            Poutrelles, tôles, tubes, cornières, corten… Découpe sur mesure, devis en 24h et
            retrait le jour même dans l’un de nos 4 dépôts.
          </p>

          <div className="apparait mt-8 flex flex-col gap-3 sm:flex-row" style={delai(0.25)}>
            <Link href="/devis" className="btn-cta justify-center">
              Demander un devis
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                <path d="M5 12h14M13 6l6 6-6 6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
              </svg>
            </Link>
            <Link href="/produits" className="btn-ghost justify-center">Voir les produits</Link>
          </div>

          <p className="apparait mt-6 font-body text-sm text-soft" style={delai(0.4)}>
            ✓ Sans engagement&nbsp;&nbsp;·&nbsp;&nbsp;✓ Particuliers &amp; pros&nbsp;&nbsp;·&nbsp;&nbsp;✓ Certifié EN1090-Exc2
          </p>
        </div>

        {/* Composition visuelle */}
        <div className="apparait group relative mx-auto w-full max-w-lg" style={delai(0.2)}>
          {/* carte principale : le dépôt */}
          <div className="shine relative aspect-[4/3] overflow-hidden rounded-2xl border border-brume bg-nuage shadow-[0_40px_90px_-50px_rgba(51,54,66,.6)]">
            <ArtStock className="h-full w-full transition-transform duration-700 group-hover:scale-[1.04]" />
            <span className="tag-stock absolute left-5 top-5 z-10">495 produits</span>
          </div>

          {/* vignettes flottantes */}
          <div
            className="flotte absolute -left-6 -bottom-10 w-40 overflow-hidden rounded-xl border border-brume bg-white shadow-xl md:-left-10"
            style={flotte(5, -10)}
          >
            <ArtPoutrelle className="h-24 w-full" />
            <p className="px-3 pb-2 font-body text-[11px] text-soft">Poutrelles IPE</p>
          </div>

          <div
            className="flotte absolute -right-4 -top-8 w-36 overflow-hidden rounded-xl border border-brume bg-white shadow-xl md:-right-8"
            style={flotte(6, 10, 0.6)}
          >
            <ArtTube className="h-24 w-full" />
            <p className="px-3 pb-2 font-body text-[11px] text-soft">Tubes &amp; profilés</p>
          </div>

          <div
            className="flotte absolute -right-2 bottom-6 hidden w-32 overflow-hidden rounded-xl border border-encre/20 shadow-xl lg:block"
            style={flotte(7, -8, 1.2)}
          >
            <ArtDecoupe className="h-20 w-full" />
            <p className="bg-encre px-3 py-1.5 font-body text-[11px] text-white">Découpe sur mesure</p>
          </div>
        </div>
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
