import Link from "next/link";
import Reveal from "@/components/fx/Reveal";
import { site, lienTel } from "@/lib/content";

export default function CtaBand() {
  return (
    <section className="bg-white py-8">
      <div className="container-g">
        <div className="relative overflow-hidden rounded-3xl bg-encre px-6 py-16 md:px-16 md:py-20">
          <div className="grid-industrie-dark pointer-events-none absolute inset-0" />
          <div className="pointer-events-none absolute -right-10 -top-10 h-56 w-56 rounded-full bg-jaune/20 blur-[100px]" />
          <div className="relative mx-auto max-w-2xl text-center">
            <Reveal y={20}>
              <h2 className="h-display text-4xl text-white md:text-5xl">
                Un projet ? Votre devis en <span className="on-encre-jaune">24 heures.</span>
              </h2>
            </Reveal>
            <p className="mt-4 font-body text-lg text-soft-light">
              Décrivez votre besoin (dimensions, quantités, usage). On revient vers vous sous 24h, sans engagement.
            </p>
            <div className="mt-8 flex flex-col items-center justify-center gap-3 sm:flex-row">
              <Link href="/devis" className="btn-cta justify-center">
                Demander un devis
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
                  <path d="M5 12h14M13 6l6 6-6 6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                </svg>
              </Link>
              <a href={lienTel(site.tel)} className="inline-flex items-center gap-2 rounded-md border border-white/25 px-6 py-3 font-title font-semibold text-white transition-colors hover:bg-white/10">
                {site.tel}
              </a>
            </div>
            <p className="mt-6 font-body text-sm text-soft-light">Sans engagement · Particuliers & pros · Réponse rapide</p>
          </div>
        </div>
      </div>
    </section>
  );
}
