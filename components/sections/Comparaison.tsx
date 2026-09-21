import Reveal from "@/components/fx/Reveal";
import { comparaison } from "@/lib/content";

export default function Comparaison() {
  return (
    <section className="bg-white py-24 md:py-32">
      <div className="container-g">
        <Reveal className="mb-12 max-w-2xl">
          <span className="font-body text-xs uppercase tracking-[0.2em] text-soft">Le bon réflexe</span>
          <h2 className="h-display mt-3 text-4xl md:text-5xl">{comparaison.titre}</h2>
          <p className="mt-4 font-body text-lg text-soft">{comparaison.intro}</p>
        </Reveal>

        <Reveal delay={0.1}>
          <div className="overflow-hidden rounded-2xl border border-brume break-words hyphens-auto">
            {/* En-tête */}
            <div className="grid grid-cols-[0.95fr_1.25fr_1fr] sm:grid-cols-3 bg-nuage">
              <div className="p-3 sm:p-5 font-body text-sm text-soft">Critère</div>
              <div className="flex flex-col items-start gap-1 border-l border-brume bg-encre p-3 sm:flex-row sm:items-center sm:gap-2 sm:p-5">
                <span className="h-title font-bold text-white">Aciers Grosjean</span>
              </div>
              <div className="border-l border-brume p-3 sm:p-5 font-body text-sm text-soft">Grande surface</div>
            </div>
            {comparaison.lignes.map((l, i) => (
              <div key={l.critere} className={`grid grid-cols-[0.95fr_1.25fr_1fr] sm:grid-cols-3 ${i % 2 ? "bg-white" : "bg-nuage/50"}`}>
                <div className="flex items-center p-3 sm:p-5 font-body text-sm font-medium text-encre">{l.critere}</div>
                <div className="flex flex-col items-start gap-1 border-l border-brume bg-encre/[0.03] p-3 sm:flex-row sm:items-center sm:gap-2 sm:p-5">
                  <span className="flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-jaune">
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none"><path d="M5 13l4 4L19 7" stroke="#333642" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" /></svg>
                  </span>
                  <span className="font-body text-sm font-semibold text-encre">{l.grosjean}</span>
                </div>
                <div className="flex items-center border-l border-brume p-3 sm:p-5 font-body text-sm text-soft">{l.autre}</div>
              </div>
            ))}
          </div>
        </Reveal>
      </div>
    </section>
  );
}
