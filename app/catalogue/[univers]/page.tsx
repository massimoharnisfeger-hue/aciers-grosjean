import type { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";
import { notFound } from "next/navigation";
import FilAriane from "@/components/ui/FilAriane";
import CtaBand from "@/components/sections/CtaBand";
import OngletsChapitres from "@/components/catalogue/OngletsChapitres";
import FicheFamille from "@/components/catalogue/FicheFamille";
import FiltreCatalogue from "@/components/catalogue/FiltreCatalogue";
import ImprimerChapitre from "@/components/catalogue/ImprimerChapitre";
import { chapitres, chapitreParSlug, type Chapitre } from "@/lib/catalogue-visuel";
import { titre, description } from "@/lib/seo";

type Params = { univers: string };

export const dynamicParams = false;

export function generateStaticParams() {
  return chapitres().map((c) => ({ univers: c.slug }));
}

export async function generateMetadata({ params }: { params: Promise<Params> }): Promise<Metadata> {
  const { univers } = await params;
  const c = chapitreParSlug(univers);
  if (!c) return { title: "Chapitre introuvable | Aciers Grosjean" };
  return {
    title: titre(`Catalogue ${c.nom} — ${c.nbFamilles} familles, ${c.nbProduits} produits`),
    description: description(
      `Chapitre ${c.numero} du catalogue Aciers Grosjean : ${c.nom.toLowerCase()}, ${c.nbProduits} produits en ` +
        `${c.nbFamilles} familles, ${c.nbVisuels} rendus 3D aux cotes. ${c.accroche}.`
    ),
    alternates: { canonical: c.href },
  };
}

/** Le sommaire du chapitre : une liste d'ancres, rendue deux fois (repliée sur mobile, fixe sur grand écran). */
function IndexFamilles({ c, classe }: { c: Chapitre; classe: string }) {
  return (
    <nav aria-label="Familles du chapitre" className={classe}>
      {c.sections.map((s, i) => (
        <div key={s.chemin ?? `direct-${i}`} className={i > 0 ? "mt-4" : ""}>
          {s.nom && <p className="font-title text-xs font-semibold text-soft">{s.nom}</p>}
          <ul className="mt-1">
            {s.familles.map((f) => (
              <li key={f.chemin} className="min-w-0">
                <a
                  href={`#${f.ancre}`}
                  className="lien-tactile flex w-full items-baseline justify-between gap-3 py-1 font-body text-sm text-encre hover:text-jaune"
                >
                  <span className="min-w-0 truncate">{f.nom}</span>
                  <span className="shrink-0 font-mono text-xs tabular-nums text-soft">{f.variantes.length}</span>
                </a>
              </li>
            ))}
          </ul>
        </div>
      ))}
    </nav>
  );
}

export default async function ChapitrePage({ params }: { params: Promise<Params> }) {
  const { univers } = await params;
  const c = chapitreParSlug(univers);
  if (!c) notFound();

  const tous = chapitres();
  const onglets = tous.map((x) => ({ slug: x.slug, nom: x.nom, numero: x.numero, href: x.href, nbProduits: x.nbProduits }));
  const precedent = tous.find((x) => x.numero === c.numero - 1);
  const suivant = tous.find((x) => x.numero === c.numero + 1);
  const familles = c.sections.flatMap((s) => s.familles);
  const exemples = [...familles]
    .sort((a, b) => b.variantes.length - a.variantes.length)
    .slice(0, 4)
    .map((f) => f.nom);
  const portee = `chapitre-${c.slug}`;

  return (
    <main className="catalogue-imprimable">
      <header className="border-b border-brume bg-nuage pt-28 md:pt-32 print:pt-6">
        <div className="container-g pb-10 md:pb-14">
          <div className="print:hidden">
            <FilAriane items={[{ label: "Catalogue produits", href: "/catalogue" }, { label: c.nom }]} />
          </div>
          <div className="mt-6">
            <OngletsChapitres chapitres={onglets} actif={c.slug} />
          </div>

          <div className="mt-10 grid gap-8 lg:grid-cols-[minmax(0,3fr)_minmax(0,2fr)] lg:items-start lg:gap-14">
            <div className="min-w-0 break-words">
              <p className="font-sub text-base text-soft">Chapitre {c.numero}</p>
              <h1 className="h-display mt-1 text-4xl md:text-6xl">{c.nom}</h1>
              {c.accroche && <p className="mt-4 font-sub text-lg leading-snug text-encre">{c.accroche}</p>}
              {c.intro && <p className="mt-4 max-w-2xl font-body text-base leading-relaxed text-soft">{c.intro}</p>}
              <p className="mt-5 font-body text-sm text-soft">
                {c.nbFamilles} familles, {c.nbProduits} produits, {c.nbVisuels} vues cotées.
              </p>
              <div className="mt-6 flex flex-wrap gap-3 print:hidden">
                <ImprimerChapitre />
                <Link href={`/${c.slug}`} className="btn-ghost">
                  {c.nom} sur le site
                </Link>
              </div>
            </div>

            {c.studios.length > 0 && (
              <ul className={`grid gap-2 sm:gap-3 ${c.studios.length === 1 ? "grid-cols-1" : "grid-cols-2"}`}>
                {c.studios.map((s, i) => (
                  <li key={s.src} className="overflow-hidden rounded-xl border border-brume bg-white">
                    <Image
                      src={s.src}
                      alt={s.alt}
                      width={s.largeur}
                      height={s.hauteur}
                      sizes="(min-width: 1024px) 20vw, 45vw"
                      priority={i < 2}
                      className="h-auto w-full"
                    />
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>
      </header>

      <div className="container-g py-10 md:py-14">
        <details className="rounded-xl border border-brume bg-white px-4 py-3 lg:hidden print:hidden">
          <summary className="cursor-pointer font-title text-sm font-semibold text-encre">
            Familles du chapitre ({c.nbFamilles})
          </summary>
          <IndexFamilles c={c} classe="mt-3" />
        </details>

        <div className="lg:grid lg:grid-cols-[14rem_minmax(0,1fr)] lg:gap-12">
          <aside className="hidden lg:block print:hidden">
            <div className="sticky top-28 max-h-[calc(100vh-8rem)] overflow-y-auto pr-2">
              <IndexFamilles c={c} classe="" />
            </div>
          </aside>

          <div id={portee} className="min-w-0">
            <div className="mt-8 lg:mt-0">
              <FiltreCatalogue total={c.nbProduits} portee={portee} exemples={exemples} />
            </div>

            {c.sections.map((s, i) => (
              <section
                key={s.chemin ?? `direct-${i}`}
                data-section=""
                id={s.chemin ? s.chemin.replace(/^\//, "").replace(/\//g, "-") : undefined}
                className="mt-12 scroll-mt-28 md:mt-16"
                aria-label={s.nom ?? undefined}
              >
                {s.nom && (
                  <div className="mb-8">
                    <h2 className="h-display text-2xl md:text-4xl">{s.nom}</h2>
                    {s.accroche && <p className="mt-2 font-sub text-base text-soft">{s.accroche}</p>}
                  </div>
                )}
                <div className="space-y-12 md:space-y-16">
                  {s.familles.map((f, j) => (
                    <FicheFamille key={f.chemin} famille={f} niveau={s.nom ? 3 : 2} premiere={i === 0 && j === 0} />
                  ))}
                </div>
              </section>
            ))}
          </div>
        </div>
      </div>

      <nav aria-label="Chapitre précédent et suivant" className="border-t border-brume bg-nuage print:hidden">
        <div className="container-g flex flex-col gap-3 py-8 sm:flex-row sm:items-center sm:justify-between">
          {precedent ? (
            <Link href={precedent.href} prefetch={false} className="lien-tactile font-body text-sm text-encre hover:text-jaune">
              <span className="text-soft">Chapitre {precedent.numero} : </span>
              {precedent.nom}
            </Link>
          ) : (
            <span />
          )}
          <Link href="/catalogue#sommaire" className="lien-tactile font-body text-sm font-medium text-encre hover:text-jaune">
            Sommaire
          </Link>
          {suivant ? (
            <Link href={suivant.href} prefetch={false} className="lien-tactile font-body text-sm text-encre hover:text-jaune sm:text-right">
              <span className="text-soft">Chapitre {suivant.numero} : </span>
              {suivant.nom}
            </Link>
          ) : (
            <span />
          )}
        </div>
      </nav>

      <div className="print:hidden">
        <CtaBand />
      </div>
    </main>
  );
}
