import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import CtaBand from "@/components/sections/CtaBand";
import Reveal from "@/components/fx/Reveal";
import FilAriane from "@/components/ui/FilAriane";
import TableauProduits from "@/components/catalogue/TableauProduits";
import { productArt, ArtPoutrelle } from "@/components/art/ProductArt";
import {
  noeuds,
  universBySlug,
  produitsSous,
  ancetres,
  prixMini,
  formatPrix,
} from "@/lib/catalogue";
import { artPour } from "@/lib/visuels";
import VisuelFamille from "@/components/catalogue/VisuelFamille";
import { titre, description } from "@/lib/seo";

type Params = { univers: string; segments: string[] };

export const dynamicParams = false;

export function generateStaticParams() {
  return Object.keys(noeuds)
    .filter((c) => c.split("/").length > 2)
    .map((c) => {
      const parts = c.replace(/^\//, "").split("/");
      return { univers: parts[0], segments: parts.slice(1) };
    });
}

export async function generateMetadata({ params }: { params: Promise<Params> }): Promise<Metadata> {
  const { univers, segments } = await params;
  const chemin = `/${univers}/${segments.join("/")}`;
  const n = noeuds[chemin];
  if (!n) return { title: "Page introuvable | Aciers Grosjean" };
  const total = produitsSous(chemin).length;
  const mini = prixMini(chemin);
  return {
    title: titre(n.titreSeo),
    description: description(
      `${total} référence${total > 1 ? "s" : ""} de ${n.nom.toLowerCase()} en stock` +
        (mini !== null ? `, dès ${formatPrix(mini)}` : "") +
        ". Poids et prix affichés, découpe aux cotes, retrait le jour même."
    ),
    alternates: { canonical: chemin },
  };
}

export default async function NoeudPage({ params }: { params: Promise<Params> }) {
  const { univers, segments } = await params;
  const chemin = `/${univers}/${segments.join("/")}`;
  const n = noeuds[chemin];
  if (!n) notFound();

  const u = universBySlug(univers)!;
  const Art = productArt[artPour(chemin, u.art)] ?? ArtPoutrelle;

  const enfants = n.enfants.map((c) => noeuds[c]).filter(Boolean);
  const produits = produitsSous(chemin);
  const mini = prixMini(chemin);

  const chaine = ancetres(chemin);
  const miettes = [
    { label: "Catalogue", href: "/produits" },
    ...chaine.map((a) => ({ label: a.nom, href: a.chemin })),
  ];

  // Groupes de filtrage : les sous-catégories directes qui portent des produits.
  const groupes = enfants
    .filter((e) => e.produits.length > 0)
    .map((e) => ({ chemin: e.chemin, nom: e.nom }));

  return (
    <main>
      <header className="relative overflow-hidden border-b border-brume bg-nuage pt-32 md:pt-40">
        <div className="grid-industrie pointer-events-none absolute inset-0 opacity-60" />
        <div className="container-g relative pb-12 md:pb-16">
          <div className="mb-5">
            <FilAriane items={miettes} />
          </div>
          <h1 className="h-display max-w-3xl text-3xl md:text-5xl">{n.h1}</h1>
          {n.accroche && (
            <p className="mt-4 max-w-2xl font-body text-lg text-soft">{n.accroche}</p>
          )}
        </div>
      </header>

      <section className="bg-white py-12 md:py-16">
        <div className="container-g">
          {/* chiffres + visuel */}
          <div className="mb-12 grid items-center gap-10 md:grid-cols-[1fr_.8fr]">
            <Reveal>
              <dl className="grid grid-cols-2 gap-x-8 gap-y-6 sm:grid-cols-4">
                <div>
                  <dt className="font-body text-xs uppercase tracking-[0.14em] text-soft">Produits</dt>
                  <dd className="h-title mt-1 text-3xl font-bold tabular-nums text-encre">{produits.length}</dd>
                </div>
                {enfants.length > 0 && (
                  <div>
                    <dt className="font-body text-xs uppercase tracking-[0.14em] text-soft">Catégories</dt>
                    <dd className="h-title mt-1 text-3xl font-bold tabular-nums text-encre">{enfants.length}</dd>
                  </div>
                )}
                {mini !== null && (
                  <div>
                    <dt className="font-body text-xs uppercase tracking-[0.14em] text-soft">À partir de</dt>
                    <dd className="h-title mt-1 text-3xl font-bold tabular-nums text-encre">{formatPrix(mini)}</dd>
                  </div>
                )}
                <div>
                  <dt className="font-body text-xs uppercase tracking-[0.14em] text-soft">Retrait</dt>
                  <dd className="h-title mt-1 text-3xl font-bold text-encre">Jour même</dd>
                </div>
              </dl>

              <p className="mt-7 max-w-lg font-body text-soft">
                Tout se débite aux cotes exactes&nbsp;: vous ne payez que la longueur utile. Prix du
                catalogue hors TVA (TVAC sur chaque fiche), découpe en supplément.
              </p>
              <div className="mt-6 flex flex-wrap gap-3">
                <Link href="/devis" className="btn-cta">Demander un devis</Link>
                <Link href="/services/decoupe" className="btn-ghost">La découpe</Link>
              </div>
            </Reveal>

            <Reveal delay={0.08}>
              <div className="group relative aspect-[4/3] overflow-hidden rounded-2xl border border-brume bg-nuage">
                <div className="grid-industrie absolute inset-0 opacity-70" />
                <div className="shine absolute inset-0">
                  <Art className="h-full w-full transition-transform duration-700 group-hover:scale-105" />
                </div>
                <span className="tag-stock absolute left-5 top-5">Stock permanent</span>
              </div>
            </Reveal>
          </div>

          {/* sous-catégories */}
          {enfants.length > 0 && (
            <div className="mb-14">
              <h2 className="h-display mb-6 text-2xl md:text-3xl">Choisir la catégorie</h2>
              <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
                {enfants.map((e, i) => {
                  const EArt = productArt[artPour(e.chemin, u.art)] ?? Art;
                  const ne = produitsSous(e.chemin).length;
                  const me = prixMini(e.chemin);
                  return (
                    <Reveal key={e.chemin} delay={(i % 3) * 0.06}>
                      <Link
                        href={e.chemin}
                        className="group flex h-full gap-4 rounded-2xl border border-brume bg-white p-5 transition-all duration-300 hover:-translate-y-1 hover:border-encre/20 hover:shadow-[0_26px_60px_-34px_rgba(51,54,66,.5)]"
                      >
                        <div className="shine relative h-20 w-20 shrink-0 overflow-hidden rounded-xl bg-nuage">
                          <div className="grid-industrie absolute inset-0 opacity-70" />
                          <VisuelFamille chemin={e.chemin} Art={EArt} />
                        </div>
                        <div className="min-w-0 flex-1">
                          <h3 className="h-title font-semibold leading-snug text-encre">{e.nom}</h3>
                          <p className="mt-1 font-mono text-xs text-soft">
                            {ne} produit{ne > 1 ? "s" : ""}
                            {me !== null && <> · dès {formatPrix(me)}</>}
                          </p>
                        </div>
                        <span className="self-center text-soft transition-transform group-hover:translate-x-1">
                          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                            <path d="M5 12h14M13 6l6 6-6 6" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round" />
                          </svg>
                        </span>
                      </Link>
                    </Reveal>
                  );
                })}
              </div>
            </div>
          )}

          {/* produits */}
          {produits.length > 0 && (
            <>
              <h2 className="h-display mb-2 text-2xl md:text-3xl">
                {produits.length} produit{produits.length > 1 ? "s" : ""} en stock
              </h2>
              <p className="mb-6 max-w-xl font-body text-soft">
                Cherchez une cote, triez par prix ou par poids. Chaque ligne mène à la fiche
                technique, avec le calcul de votre quantité.
              </p>
              <TableauProduits produits={produits} groupes={groupes} id={segments.join("-")} />
            </>
          )}
        </div>
      </section>

      <CtaBand />
    </main>
  );
}
