import type { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";
import FilAriane from "@/components/ui/FilAriane";
import Logo from "@/components/ui/Logo";
import CtaBand from "@/components/sections/CtaBand";
import OngletsChapitres from "@/components/catalogue/OngletsChapitres";
import { notFound } from "next/navigation";
import { chapitres, totauxCatalogue, catalogueActif } from "@/lib/catalogue-visuel";
import { titre, description } from "@/lib/seo";

/**
 * Couverture et sommaire du catalogue visuel.
 *
 * Six chapitres (un par univers), chacun sur sa propre page : les 495 planches
 * ne partent pas toutes d'un coup, et cette couverture reste légère même si un
 * lien de l'en-tête la précharge sur chaque page (leçon L-046).
 */

const totaux = totauxCatalogue();

// Date de construction : le catalogue est une édition, pas une page vivante.
const EDITION = new Intl.DateTimeFormat("fr-BE", { month: "long", year: "numeric" }).format(new Date());

export const metadata: Metadata = {
  title: titre(`Catalogue produits — ${totaux.produits} produits en ${totaux.familles} familles`),
  description: description(
    `Le catalogue Aciers Grosjean en images : acier, aluminium, inox, toiture et bardage, ` +
      `jardin et clôture, quincaillerie. ${totaux.visuels} rendus 3D aux cotes, une fiche par produit.`
  ),
  alternates: { canonical: "/catalogue" },
};

export default function CataloguePage() {
  if (!catalogueActif) notFound();
  const tous = chapitres();
  const onglets = tous.map((c) => ({ slug: c.slug, nom: c.nom, numero: c.numero, href: c.href, nbProduits: c.nbProduits }));

  return (
    <main className="catalogue-imprimable">
      <header className="border-b border-brume bg-nuage pt-28 md:pt-32 print:pt-6">
        <div className="container-g pb-12 md:pb-16">
          <div className="print:hidden">
            <FilAriane items={[{ label: "Catalogue produits" }]} />
          </div>

          <div className="mt-8 grid gap-10 lg:grid-cols-2 lg:items-center lg:gap-16">
            <div className="min-w-0">
              <Logo hauteur={44} anime={false} />
              <p className="mt-10 font-sub text-base text-soft">Édition {EDITION}</p>
              <h1 className="h-display mt-2 text-4xl md:text-6xl">Catalogue produits</h1>
              <p className="mt-5 max-w-xl font-body text-lg leading-relaxed text-soft">
                {totaux.produits} produits en {totaux.familles} familles — acier, aluminium, inox, toiture et
                bardage, jardin et clôture, quincaillerie — dont {totaux.visuels} illustrés par leur rendu 3D aux
                cotes. Chaque planche mène à la fiche du site, où le prix se calcule.
              </p>
              <div className="mt-8 flex flex-wrap gap-3 print:hidden">
                <a href="#sommaire" className="btn-cta">Ouvrir le sommaire</a>
                <Link href="/recherche" className="btn-ghost">Chercher un produit</Link>
              </div>
            </div>

            {/* Une photo studio par chapitre, dans l'ordre du catalogue : la couverture ne montre que des produits réels. */}
            <ul className="grid grid-cols-3 gap-2 sm:gap-3">
              {tous.map((c) =>
                c.studios[0] ? (
                  <li key={c.slug} className="relative overflow-hidden rounded-xl border border-brume bg-white">
                    <Image
                      src={c.studios[0].src}
                      alt={c.studios[0].alt}
                      width={c.studios[0].largeur}
                      height={c.studios[0].hauteur}
                      sizes="(min-width: 1024px) 15vw, 30vw"
                      priority={c.numero <= 3}
                      className="h-auto w-full"
                    />
                    <span className="absolute bottom-1.5 left-1.5 rounded-md bg-white/90 px-1.5 py-0.5 font-title text-xs font-semibold text-encre">
                      {c.nom}
                    </span>
                  </li>
                ) : null
              )}
            </ul>
          </div>
        </div>
      </header>

      <section id="sommaire" className="scroll-mt-24 bg-white py-14 md:py-20" aria-labelledby="sommaire-titre">
        <div className="container-g">
          <h2 id="sommaire-titre" className="h-display text-2xl md:text-4xl">Sommaire</h2>
          <p className="mt-3 max-w-xl font-body text-base text-soft">
            Six chapitres, {totaux.familles} familles. Un chapitre s&apos;ouvre sur sa page, une famille sur sa
            section.
          </p>

          <div className="mt-8">
            <OngletsChapitres chapitres={onglets} />
          </div>

          <ol className="mt-10 grid gap-5 md:grid-cols-2 xl:grid-cols-3">
            {tous.map((c) => (
              <li key={c.slug} className="flex min-w-0 flex-col rounded-2xl border border-brume bg-white p-5 md:p-6">
                <div className="flex items-start gap-4">
                  <span
                    className="flex h-12 w-12 shrink-0 items-center justify-center rounded-lg bg-jaune font-title text-xl font-bold tabular-nums text-encre"
                    aria-hidden="true"
                  >
                    {c.numero}
                  </span>
                  <div className="min-w-0">
                    <h3 className="h-title font-title text-xl font-semibold leading-tight text-encre">
                      <Link href={c.href} prefetch={false} className="lien-tactile hover:text-jaune">
                        <span className="sr-only">Chapitre {c.numero} : </span>
                        {c.nom}
                      </Link>
                    </h3>
                    {c.accroche && <p className="mt-1 font-body text-sm text-soft">{c.accroche}</p>}
                    <p className="mt-1.5 font-body text-xs text-soft">
                      {c.nbFamilles} familles, {c.nbProduits} produits, {c.nbVisuels} vues cotées
                    </p>
                  </div>
                </div>

                <ul className="mt-5 grid grid-cols-1 gap-x-4 sm:grid-cols-2">
                  {c.sections.flatMap((s) =>
                    s.familles.map((f) => (
                      <li key={f.chemin} className="min-w-0 border-t border-brume/70">
                        <Link
                          href={`${c.href}#${f.ancre}`}
                          prefetch={false}
                          className="lien-tactile flex w-full items-baseline justify-between gap-3 py-1.5 font-body text-sm text-encre hover:text-jaune"
                        >
                          <span className="min-w-0 truncate">{f.nom}</span>
                          <span className="shrink-0 font-mono text-xs tabular-nums text-soft">{f.variantes.length}</span>
                        </Link>
                      </li>
                    ))
                  )}
                </ul>

                <Link href={c.href} prefetch={false} className="btn-ghost mt-5 justify-center self-start print:hidden">
                  Ouvrir le chapitre {c.numero}
                </Link>
              </li>
            ))}
          </ol>
        </div>
      </section>

      <section className="border-t border-brume bg-nuage py-12 md:py-16" aria-labelledby="lire-titre">
        <div className="container-g">
          <h2 id="lire-titre" className="h-display text-2xl md:text-3xl">Lire ce catalogue</h2>
          <dl className="mt-6 grid gap-6 md:grid-cols-3">
            <div>
              <dt className="font-title text-base font-semibold text-encre">Les images</dt>
              <dd className="mt-1.5 font-body text-sm leading-relaxed text-soft">
                Chaque variante est dessinée en 3D à ses cotes nominales ; la photo studio montre la famille.
                Illustrations non contractuelles.
              </dd>
            </div>
            <div>
              <dt className="font-title text-base font-semibold text-encre">Les caractéristiques</dt>
              <dd className="mt-1.5 font-body text-sm leading-relaxed text-soft">
                Celles des fiches du site aciersgrosjean.be, relevées le 14 septembre 2026. Ce qui vaut pour toute
                une famille se lit en tête de famille ; ce qui distingue une variante se lit sur sa planche.
              </dd>
            </div>
            <div>
              <dt className="font-title text-base font-semibold text-encre">Les prix</dt>
              <dd className="mt-1.5 font-body text-sm leading-relaxed text-soft">
                Sur la fiche de chaque produit, avec le calcul de votre quantité et la demande de devis. Le
                catalogue ne les reprend pas : ils se mettent à jour sur le site.
              </dd>
            </div>
          </dl>
        </div>
      </section>

      <div className="print:hidden">
        <CtaBand />
      </div>
    </main>
  );
}
