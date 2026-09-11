import Link from "next/link";
import Reveal from "@/components/fx/Reveal";
import { guides } from "@/lib/edito";

export default function Guides() {
  const vedette = guides[0];
  const suite = guides.slice(1, 4);

  return (
    <section className="bg-white py-24 md:py-32">
      <div className="container-g">
        <Reveal className="mb-12 max-w-2xl">
          <span className="font-body text-xs uppercase tracking-[0.2em] text-soft">Guides</span>
          <h2 className="h-display mt-3 text-4xl md:text-5xl">
            On vous explique <span className="mark-jaune">avant</span> de vous vendre
          </h2>
          <p className="mt-4 font-body text-lg text-soft">
            Quarante ans de questions posées au comptoir, écrites noir sur blanc. Y compris
            quand la réponse est « prenez la section en dessous ».
          </p>
        </Reveal>

        <div className="grid gap-5 lg:grid-cols-[1.15fr_1fr]">
          {/* guide mis en avant */}
          <Reveal>
            <Link
              href={`/guides/${vedette.slug}`}
              className="group relative flex h-full flex-col justify-end overflow-hidden rounded-2xl bg-encre p-8 md:p-10"
            >
              <div className="grid-industrie-dark pointer-events-none absolute inset-0" />
              <div className="pointer-events-none absolute -right-10 -top-10 h-56 w-56 rounded-full bg-jaune/15 blur-[90px]" />
              <div className="relative">
                <span className="font-body text-xs uppercase tracking-[0.2em] text-white/50">
                  {vedette.categorie} · {vedette.lecture} min
                </span>
                <h3 className="h-display mt-4 text-3xl leading-tight text-white md:text-4xl">
                  {vedette.titre}
                </h3>
                <p className="mt-4 max-w-md font-body text-soft-light">{vedette.chapo}</p>
                <span className="mt-7 inline-flex items-center gap-2 font-body text-sm font-medium on-encre-jaune">
                  Lire le guide
                  <svg
                    width="16" height="16" viewBox="0 0 24 24" fill="none"
                    className="transition-transform group-hover:translate-x-1"
                  >
                    <path d="M5 12h14M13 6l6 6-6 6" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round" />
                  </svg>
                </span>
              </div>
            </Link>
          </Reveal>

          {/* les suivants */}
          <div className="grid gap-4">
            {suite.map((g, i) => (
              <Reveal key={g.slug} delay={i * 0.07}>
                <Link
                  href={`/guides/${g.slug}`}
                  className="group flex items-center justify-between gap-6 rounded-2xl border border-brume bg-white p-6 transition-all duration-300 hover:-translate-y-0.5 hover:border-encre/20 hover:shadow-[0_22px_50px_-32px_rgba(51,54,66,.5)]"
                >
                  <span className="min-w-0">
                    <span className="block font-mono text-xs text-soft">
                      {g.categorie} · {g.lecture} min
                    </span>
                    <span className="h-title mt-1.5 block font-semibold leading-snug text-encre">
                      {g.titre}
                    </span>
                  </span>
                  <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full border border-brume text-encre transition-all group-hover:border-jaune group-hover:bg-jaune">
                    <svg width="15" height="15" viewBox="0 0 24 24" fill="none">
                      <path d="M5 12h14M13 6l6 6-6 6" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round" />
                    </svg>
                  </span>
                </Link>
              </Reveal>
            ))}
          </div>
        </div>

        <div className="mt-10 flex justify-center">
          <Link href="/guides" className="btn-ghost">
            Les {guides.length} guides
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
              <path d="M5 12h14M13 6l6 6-6 6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
          </Link>
        </div>
      </div>
    </section>
  );
}
