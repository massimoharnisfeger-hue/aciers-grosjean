import type { Metadata } from "next";
import Link from "next/link";
import PageHeader from "@/components/ui/PageHeader";
import CtaBand from "@/components/sections/CtaBand";
import Reveal from "@/components/fx/Reveal";
import { depotsDetail } from "@/lib/edito";

export const metadata: Metadata = {
  title: "4 dépôts acier — Charleroi, La Louvière, Tournai, Marville | Aciers Grosjean",
  description:
    "Nos 4 dépôts : Charleroi, La Louvière, Tournai (Belgique) et Marville (France). Horaires, équipements de découpe sur place, communes desservies. Retrait le jour même.",
  alternates: { canonical: "/depots" },
};

export default function DepotsPage() {
  return (
    <main>
      <PageHeader
        surtitre="Dépôts"
        titre={
          <>
            4 dépôts, <span className="mark-jaune">près de chez vous</span>
          </>
        }
        intro="Trois en Wallonie, un en Meuse. Le retrait est souvent possible le jour même, et ce qui n'est pas sur place arrive par transfert interne sous 48 h."
      />

      <section className="bg-white py-16 md:py-24">
        <div className="container-g grid gap-6 md:grid-cols-2">
          {depotsDetail.map((d, i) => (
            <Reveal key={d.slug} delay={(i % 2) * 0.08}>
              <Link
                href={`/depots/${d.slug}`}
                className="group flex h-full flex-col rounded-2xl border border-brume bg-white p-7 transition-all duration-300 hover:-translate-y-1 hover:border-encre/20 hover:shadow-[0_28px_64px_-36px_rgba(51,54,66,.55)]"
              >
                <div className="mb-5 flex items-start justify-between gap-4">
                  <div className="flex items-center gap-3">
                    <span className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-jaune">
                      <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                        <path d="M12 21s-7-6.3-7-11a7 7 0 1114 0c0 4.7-7 11-7 11z" stroke="#333642" strokeWidth="1.8" strokeLinejoin="round" />
                        <circle cx="12" cy="10" r="2.4" fill="#333642" />
                      </svg>
                    </span>
                    <div>
                      <h2 className="h-title text-xl font-semibold text-encre">{d.ville}</h2>
                      <p className="font-body text-xs text-soft">{d.region} · {d.pays}</p>
                    </div>
                  </div>
                  <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full border border-brume text-encre transition-all group-hover:border-jaune group-hover:bg-jaune">
                    <svg width="15" height="15" viewBox="0 0 24 24" fill="none">
                      <path d="M5 12h14M13 6l6 6-6 6" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round" />
                    </svg>
                  </span>
                </div>

                <p className="font-body leading-relaxed text-soft">{d.intro}</p>

                <dl className="mt-5 space-y-2 border-t border-brume pt-4 font-body text-sm">
                  <div className="flex gap-3">
                    <dt className="w-24 shrink-0 text-soft">Horaires</dt>
                    <dd className="text-encre">{d.horaires[0].jours} · {d.horaires[0].heures}</dd>
                  </div>
                  <div className="flex gap-3">
                    <dt className="w-24 shrink-0 text-soft">Téléphone</dt>
                    <dd className="font-mono text-encre">{d.tel}</dd>
                  </div>
                </dl>

                <ul className="mt-5 flex flex-wrap gap-2">
                  {d.equipements.slice(0, 3).map((e) => (
                    <li key={e} className="rounded-full border border-brume bg-nuage px-3 py-1 font-body text-xs text-encre">
                      {e}
                    </li>
                  ))}
                  {d.equipements.length > 3 && (
                    <li className="rounded-full px-2 py-1 font-body text-xs text-soft">
                      +{d.equipements.length - 3}
                    </li>
                  )}
                </ul>
              </Link>
            </Reveal>
          ))}
        </div>
      </section>

      <CtaBand />
    </main>
  );
}
