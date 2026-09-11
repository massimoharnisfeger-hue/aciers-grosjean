import type { Metadata } from "next";
import PageHeader from "@/components/ui/PageHeader";
import CtaBand from "@/components/sections/CtaBand";
import Reveal from "@/components/fx/Reveal";
import { depots } from "@/lib/content";

export const metadata: Metadata = {
  title: "Nos dépôts — Charleroi, La Louvière, Tournai, Marville | Aciers Grosjean",
  description:
    "4 dépôts acier : Charleroi, La Louvière, Tournai (Belgique) et Marville (France). Retrait le jour même, horaires et coordonnées.",
};

export default function DepotsPage() {
  return (
    <main>
      <PageHeader
        surtitre="Dépôts"
        titre={<>4 dépôts, <span className="mark-jaune">près de chez vous</span></>}
        intro="Trois en Wallonie, un en France. Le retrait est souvent possible le jour même — vous récupérez vos pièces sans attendre."
      />

      <section className="bg-white py-20 md:py-28">
        <div className="container-g grid gap-6 sm:grid-cols-2">
          {depots.map((d, i) => (
            <Reveal key={d.ville} delay={(i % 2) * 0.08}>
              <div className="flex h-full flex-col rounded-2xl border border-brume bg-white p-7">
                <div className="mb-4 flex items-center gap-3">
                  <span className="flex h-11 w-11 items-center justify-center rounded-xl bg-jaune">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                      <path d="M12 21s-7-6.3-7-11a7 7 0 1114 0c0 4.7-7 11-7 11z" stroke="#333642" strokeWidth="1.8" strokeLinejoin="round" />
                      <circle cx="12" cy="10" r="2.4" fill="#333642" />
                    </svg>
                  </span>
                  <div>
                    <h2 className="h-title text-xl font-semibold text-encre">{d.ville}</h2>
                    <p className="font-body text-xs text-soft">{d.pays}</p>
                  </div>
                </div>
                <dl className="mt-2 space-y-2 border-t border-brume pt-4 font-body text-sm">
                  <div className="flex gap-2"><dt className="w-20 shrink-0 text-soft">Adresse</dt><dd className="text-encre">{d.adresse}</dd></div>
                  <div className="flex gap-2"><dt className="w-20 shrink-0 text-soft">Téléphone</dt><dd><a href={`tel:${d.tel.replace(/\s/g, "")}`} className="text-encre hover:text-jaune">{d.tel}</a></dd></div>
                  <div className="flex gap-2"><dt className="w-20 shrink-0 text-soft">Horaires</dt><dd className="text-encre">{d.horaires}</dd></div>
                </dl>
              </div>
            </Reveal>
          ))}
        </div>
      </section>

      <CtaBand />
    </main>
  );
}
