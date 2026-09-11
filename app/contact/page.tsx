import type { Metadata } from "next";
import Link from "next/link";
import PageHeader from "@/components/ui/PageHeader";
import CtaBand from "@/components/sections/CtaBand";
import Reveal from "@/components/fx/Reveal";
import { site } from "@/lib/content";
import { depotsDetail } from "@/lib/edito";

export const metadata: Metadata = {
  title: "Contact — téléphone, e-mail et 4 dépôts | Aciers Grosjean",
  description:
    "Joignez-nous par téléphone du lundi au vendredi de 7 h à 17 h, par e-mail avec réponse sous 24 h, ou passez directement dans l'un de nos 4 dépôts sans rendez-vous.",
  alternates: { canonical: "/contact" },
};

export default function ContactPage() {
  return (
    <main>
      <PageHeader
        surtitre="Contact"
        titre={
          <>
            Quelqu'un <span className="mark-jaune">répond vraiment</span>
          </>
        }
        intro="Pas de formulaire qui disparaît dans le vide. Un téléphone, une adresse e-mail, quatre comptoirs — et des gens qui connaissent la matière."
      />

      <section className="bg-white py-16 md:py-20">
        <div className="container-g grid gap-6 md:grid-cols-3">
          {[
            {
              t: "Par téléphone",
              s: site.tel,
              h: `tel:${site.tel.replace(/[^+\d]/g, "")}`,
              d: "Du lundi au vendredi, 7 h – 17 h. C'est le plus rapide pour une question technique.",
              icon: "M4 5c0-1 1-2 2-2h2l2 5-2 1a12 12 0 006 6l1-2 5 2v2c0 1-1 2-2 2A17 17 0 014 5z",
            },
            {
              t: "Par e-mail",
              s: site.email,
              h: `mailto:${site.email}`,
              d: "Réponse sous 24 h ouvrées. Idéal pour envoyer une liste de débit ou un plan.",
              icon: "M3 7l9 6 9-6M3 7v10h18V7M3 7h18",
            },
            {
              t: "Au comptoir",
              s: "4 dépôts",
              h: "/depots",
              d: "Sans rendez-vous. On vous montre la matière, et souvent vous repartez avec.",
              icon: "M12 21s-7-6.3-7-11a7 7 0 1114 0c0 4.7-7 11-7 11z",
            },
          ].map((c, i) => (
            <Reveal key={c.t} delay={i * 0.07}>
              <Link
                href={c.h}
                className="group flex h-full flex-col rounded-2xl border border-brume bg-white p-7 transition-all duration-300 hover:-translate-y-1 hover:border-encre/20 hover:shadow-[0_28px_64px_-36px_rgba(51,54,66,.55)]"
              >
                <span className="flex h-12 w-12 items-center justify-center rounded-xl bg-encre">
                  <svg width="22" height="22" viewBox="0 0 24 24" fill="none" className="on-encre-jaune">
                    <path d={c.icon} stroke="currentColor" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round" />
                  </svg>
                </span>
                <h2 className="h-title mt-5 text-lg font-semibold text-encre">{c.t}</h2>
                <p className="mt-1 font-mono text-sm text-encre">{c.s}</p>
                <p className="mt-3 flex-1 font-body text-sm leading-relaxed text-soft">{c.d}</p>
              </Link>
            </Reveal>
          ))}
        </div>
      </section>

      <section className="border-t border-brume bg-nuage py-16 md:py-20">
        <div className="container-g">
          <h2 className="h-display text-2xl md:text-3xl">Les quatre comptoirs</h2>
          <div className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            {depotsDetail.map((d, i) => (
              <Reveal key={d.slug} delay={i * 0.06}>
                <Link
                  href={`/depots/${d.slug}`}
                  className="group flex h-full flex-col rounded-2xl border border-brume bg-white p-6 transition-all duration-300 hover:-translate-y-1 hover:shadow-[0_26px_60px_-34px_rgba(51,54,66,.5)]"
                >
                  <h3 className="h-title text-lg font-semibold text-encre">{d.ville}</h3>
                  <p className="mt-0.5 font-body text-xs text-soft">{d.region}</p>
                  <p className="mt-4 font-mono text-sm text-encre">{d.tel}</p>
                  <p className="mt-1 font-body text-xs text-soft">
                    {d.horaires[0].jours} · {d.horaires[0].heures}
                  </p>
                </Link>
              </Reveal>
            ))}
          </div>

          <div className="mt-12 rounded-2xl border border-brume bg-white p-8">
            <h2 className="h-title text-lg font-semibold text-encre">
              Vous avez une liste de débit&nbsp;?
            </h2>
            <p className="mt-2 max-w-2xl font-body text-soft">
              Un tableau « section, longueur, quantité » suffit — pas besoin de plan. Envoyez-le
              et vous recevez un prix chiffré et une heure de retrait dans la journée.
            </p>
            <div className="mt-6 flex flex-wrap gap-3">
              <Link href="/devis" className="btn-cta">Envoyer ma demande</Link>
              <Link href="/services/decoupe" className="btn-ghost">Comment marche la découpe</Link>
            </div>
          </div>
        </div>
      </section>

      <CtaBand />
    </main>
  );
}
