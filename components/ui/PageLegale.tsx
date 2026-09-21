import Link from "next/link";
import FilAriane from "@/components/ui/FilAriane";

export type BlocLegal = { titre: string; paras: string[] };

export default function PageLegale({
  surtitre,
  titre,
  intro,
  blocs,
  aCompleter,
}: {
  surtitre: string;
  titre: string;
  intro: string;
  blocs: BlocLegal[];
  aCompleter?: string[];
}) {
  return (
    <main>
      <header className="border-b border-brume bg-nuage pt-32 md:pt-40">
        <div className="container-g pb-12 md:pb-16">
          <div className="mb-5">
            <FilAriane items={[{ label: surtitre }]} />
          </div>
          <h1 className="h-display max-w-3xl text-3xl md:text-5xl">{titre}</h1>
          <p className="mt-4 max-w-2xl font-body text-lg text-soft">{intro}</p>
        </div>
      </header>

      <section className="bg-white py-14 md:py-20">
        <div className="container-g max-w-[46rem]">
          {aCompleter && aCompleter.length > 0 && (
            <aside className="mb-12 rounded-2xl border-l-4 border-jaune bg-nuage p-6">
              <p className="h-title font-semibold text-encre">
                Informations à compléter avant mise en ligne
              </p>
              <p className="mt-2 font-body text-sm leading-relaxed text-soft">
                Ce texte est une trame conforme au droit belge, mais il contient des données
                d’entreprise que nous n’avons pas encore. Elles doivent être renseignées avant
                toute publication&nbsp;:
              </p>
              <ul className="mt-3 space-y-1.5">
                {aCompleter.map((x) => (
                  <li key={x} className="flex gap-2.5 font-body text-sm text-soft">
                    <span className="mt-[0.5em] h-1.5 w-1.5 shrink-0 rounded-full bg-jaune" />
                    {x}
                  </li>
                ))}
              </ul>
            </aside>
          )}

          {blocs.map((b, i) => (
            <section key={b.titre} className={i > 0 ? "mt-10" : ""}>
              <h2 className="h-title text-xl font-semibold text-encre">{b.titre}</h2>
              <div className="mt-3 space-y-4">
                {b.paras.map((p, j) => (
                  <p key={j} className="font-body leading-[1.7] text-soft">
                    {p}
                  </p>
                ))}
              </div>
            </section>
          ))}

          <p className="mt-14 border-t border-brume pt-6 font-body text-sm text-soft">
            Une question sur ce document&nbsp;?{" "}
            <Link href="/contact" className="lien-tactile text-encre underline hover:text-jaune">
              Contactez-nous
            </Link>
            .
          </p>
        </div>
      </section>
    </main>
  );
}
