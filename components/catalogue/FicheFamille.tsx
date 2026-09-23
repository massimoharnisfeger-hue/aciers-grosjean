import Image from "next/image";
import Link from "next/link";
import type { Famille } from "@/lib/catalogue-visuel";
import PlancheVariante from "@/components/catalogue/PlancheVariante";

const metres = (v: number) => `${v.toLocaleString("fr-BE")} m`;

/**
 * La fiche d'une famille du catalogue : sa photo studio, son nom, ce qui vaut
 * pour toutes ses variantes (nuance, procédé, longueurs, unité de vente,
 * fiche technique), puis les planches de ses variantes, dans l'ordre des cotes.
 *
 * Tout ce qui est affiché vient des données du site. Une donnée absente ne
 * laisse pas de trou et n'est pas remplacée : la ligne n'existe pas.
 */
export default function FicheFamille({
  famille,
  niveau = 3,
  premiere = false,
}: {
  famille: Famille;
  /** Niveau du titre de famille : 2 quand la famille n'a pas de sous-catégorie au-dessus d'elle. */
  niveau?: 2 | 3;
  /** Première famille de la page : ses premières planches se chargent sans attendre. */
  premiere?: boolean;
}) {
  const f = famille;
  const Titre = niveau === 2 ? "h2" : "h3";
  const nb = f.variantes.length;

  return (
    <section
      id={f.ancre}
      data-famille=""
      className="scroll-mt-28 break-inside-avoid border-t border-brume pt-8 md:pt-10"
      aria-labelledby={`${f.ancre}-titre`}
    >
      <div className="grid gap-6 md:grid-cols-[minmax(0,2fr)_minmax(0,3fr)] md:gap-8 lg:gap-12">
        <figure className="min-w-0">
          <div className="relative overflow-hidden rounded-2xl border border-brume bg-nuage">
            <div className="grid-industrie absolute inset-0 opacity-60" aria-hidden="true" />
            {f.studio ? (
              <Image
                src={f.studio.src}
                alt={f.studio.alt}
                width={f.studio.largeur}
                height={f.studio.hauteur}
                sizes="(min-width: 1280px) 30vw, (min-width: 768px) 40vw, 100vw"
                className="relative h-auto w-full"
              />
            ) : (
              <p className="relative flex aspect-[4/3] items-center justify-center p-6 text-center font-body text-sm text-soft">
                Photo studio à compléter
              </p>
            )}
          </div>
          {f.studio && (
            <figcaption className="mt-2 font-body text-xs text-soft">Photo studio, rendu 3D sur fond blanc</figcaption>
          )}
        </figure>

        <div className="min-w-0 break-words">
          <Titre id={`${f.ancre}-titre`} className="h-title font-title text-2xl font-semibold leading-tight text-encre md:text-3xl">
            {f.nom}
          </Titre>
          {f.accroche && (
            <p className="mt-2 max-w-prose font-body text-base leading-relaxed text-soft">{f.accroche}</p>
          )}

          <dl className="mt-5 grid gap-x-8 gap-y-2 sm:grid-cols-2">
            <div className="flex items-baseline justify-between gap-4 border-b border-brume/70 py-1.5">
              <dt className="font-body text-sm text-soft">Variantes</dt>
              <dd className="font-mono text-sm tabular-nums text-encre">{nb}</dd>
            </div>
            {f.communes.map((s) => (
              <div key={s.label} className="flex items-baseline justify-between gap-4 border-b border-brume/70 py-1.5">
                <dt className="font-body text-sm text-soft">{s.label}</dt>
                <dd className="text-right font-mono text-sm tabular-nums text-encre">{s.valeur}</dd>
              </div>
            ))}
            {f.finition && (
              <div className="flex items-baseline justify-between gap-4 border-b border-brume/70 py-1.5">
                <dt className="font-body text-sm text-soft">Finition</dt>
                <dd className="text-right font-mono text-sm text-encre">{f.finition}</dd>
              </div>
            )}
            {f.unite && (
              <div className="flex items-baseline justify-between gap-4 border-b border-brume/70 py-1.5">
                <dt className="font-body text-sm text-soft">Vente</dt>
                <dd className="text-right font-mono text-sm text-encre">{f.unite}</dd>
              </div>
            )}
            {f.longueurs && (
              <div className="border-b border-brume/70 py-1.5 sm:col-span-2">
                <dt className="font-body text-sm text-soft">Longueurs standard</dt>
                <dd className="mt-1.5 flex flex-wrap gap-1.5">
                  {f.longueurs.map((l) => (
                    <span key={l} className="rounded-md border border-brume px-2 py-0.5 font-mono text-xs tabular-nums text-encre">
                      {metres(l)}
                    </span>
                  ))}
                </dd>
              </div>
            )}
          </dl>

          {f.pdfs.length > 0 && (
            <ul className="mt-4 space-y-1">
              {f.pdfs.map((d) => (
                <li key={d.fichier}>
                  <a
                    href={d.fichier}
                    target="_blank"
                    rel="noopener"
                    className="lien-tactile font-body text-sm font-medium text-encre underline decoration-brume underline-offset-4 hover:decoration-jaune"
                  >
                    {d.titre} (PDF)
                  </a>
                </li>
              ))}
            </ul>
          )}

          <p className="mt-4 print:hidden">
            <Link href={f.chemin} className="lien-tactile font-body text-sm text-soft underline decoration-brume underline-offset-4 hover:text-encre">
              Cette famille sur le site, avec les prix
            </Link>
          </p>
        </div>
      </div>

      <p className="mt-6 font-body text-sm text-soft">
        {nb === 1 ? "Une variante" : `${nb} variantes`}
        {f.nbVisuels < nb && ` — ${nb - f.nbVisuels} sans visuel`}
      </p>
      <ul className="mt-3 grid grid-cols-2 gap-3 sm:grid-cols-3 sm:gap-4 xl:grid-cols-4">
        {f.variantes.map((v, i) => (
          <PlancheVariante key={v.slug} variante={v} priorite={premiere && i < 2} />
        ))}
      </ul>
    </section>
  );
}
