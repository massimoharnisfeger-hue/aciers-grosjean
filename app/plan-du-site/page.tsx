import type { Metadata } from "next";
import Link from "next/link";
import PageHeader from "@/components/ui/PageHeader";
import CtaBand from "@/components/sections/CtaBand";
import { univers, noeuds, produitsSous, totalProduits } from "@/lib/catalogue";
import { articles, servicesDetail, depotsDetail, pagesAide } from "@/lib/edito";

export const metadata: Metadata = {
  title: "Plan du site | Aciers Grosjean",
  description:
    "Toutes les pages du site : catalogue par univers et par catégorie, services, dépôts, conseils, entreprise et pages légales.",
  alternates: { canonical: "/plan-du-site" },
};

function Bloc({ titre, liens }: { titre: string; liens: { label: string; href: string }[] }) {
  return (
    <div>
      <h2 className="h-title mb-4 text-sm font-semibold uppercase tracking-[0.14em] text-soft">{titre}</h2>
      <ul className="space-y-2">
        {liens.map((l) => (
          <li key={l.href}>
            <Link href={l.href} className="font-body text-sm text-encre hover:text-jaune">
              {l.label}
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default function PlanDuSitePage() {
  return (
    <main>
      <PageHeader
        surtitre="Plan du site"
        titre={<>Tout le site, <span className="mark-jaune">sur une page</span></>}
        intro={`${totalProduits} produits, ${Object.keys(noeuds).length} catégories, ${articles.length} articles, ${servicesDetail.length} services et 4 dépôts. Tout est listé ci-dessous.`}
      />

      <section className="bg-white py-14 md:py-20">
        <div className="container-g">
          {/* catalogue : l'arbre complet */}
          <h2 className="h-display mb-8 text-2xl md:text-3xl">Catalogue</h2>
          <div className="space-y-10">
            {univers.map((u) => (
              <div key={u.slug} className="rounded-2xl border border-brume p-6 md:p-8">
                <div className="flex flex-wrap items-baseline justify-between gap-3 border-b border-brume pb-4">
                  <Link href={`/${u.slug}`} className="h-title text-xl font-semibold text-encre hover:text-jaune">
                    {u.nom}
                  </Link>
                  <span className="font-mono text-xs text-soft">
                    {produitsSous(`/${u.slug}`).length} produits
                  </span>
                </div>

                <div className="mt-5 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
                  {u.enfants.map((fc) => {
                    const f = noeuds[fc];
                    if (!f) return null;
                    const sous = f.enfants.map((c) => noeuds[c]).filter(Boolean);
                    return (
                      <div key={fc}>
                        <Link href={f.chemin} className="h-title font-semibold text-encre hover:text-jaune">
                          {f.nom}
                        </Link>
                        {sous.length > 0 && (
                          <ul className="mt-2 space-y-1.5 border-l border-brume pl-4">
                            {sous.map((s) => (
                              <li key={s.chemin}>
                                <Link href={s.chemin} className="font-body text-sm text-soft hover:text-encre">
                                  {s.nom}
                                  <span className="ml-1.5 font-mono text-[11px]">
                                    {produitsSous(s.chemin).length}
                                  </span>
                                </Link>
                              </li>
                            ))}
                          </ul>
                        )}
                      </div>
                    );
                  })}
                </div>
              </div>
            ))}
          </div>

          {/* le reste */}
          <div className="mt-16 grid gap-10 sm:grid-cols-2 lg:grid-cols-4">
            <Bloc
              titre="Services"
              liens={servicesDetail.map((s) => ({ label: s.nom, href: `/services/${s.slug}` }))}
            />
            <Bloc
              titre="Dépôts"
              liens={[
                { label: "Tous les dépôts", href: "/depots" },
                ...depotsDetail.map((d) => ({ label: d.nomComplet, href: `/depots/${d.slug}` })),
              ]}
            />
            <Bloc
              titre="Entreprise"
              liens={[
                { label: "L'entreprise", href: "/entreprise" },
                { label: "Engagement ESG", href: "/entreprise/engagement-esg" },
                { label: "Certifications", href: "/entreprise/certifications" },
                { label: "À propos", href: "/a-propos" },
                { label: "Réalisations", href: "/realisations" },
                { label: "Contact", href: "/contact" },
              ]}
            />
            <Bloc
              titre="Aide & compte"
              liens={[
                ...pagesAide.map((p) => ({ label: p.titre, href: `/aide/${p.slug}` })),
                { label: "Espace pro", href: "/pro" },
                { label: "Demande de compte pro", href: "/pro/demande-de-compte" },
                { label: "Recherche", href: "/recherche" },
                { label: "Nouveautés", href: "/nouveautes" },
                { label: "Documentation", href: "/documentation" },
              ]}
            />
          </div>

          <div className="mt-14">
            <Bloc
              titre={`Conseils — ${articles.length} articles`}
              liens={[
                { label: "Tous les conseils", href: "/conseils" },
                ...articles.map((a) => ({ label: a.titre, href: `/conseils/${a.slug}` })),
              ]}
            />
          </div>

          <div className="mt-14">
            <Bloc
              titre="Informations légales"
              liens={[
                { label: "Conditions générales de vente", href: "/conditions-generales-de-vente" },
                { label: "Protection des données", href: "/protection-des-donnees" },
                { label: "Cookies", href: "/cookies" },
                { label: "Mentions légales", href: "/mentions-legales" },
              ]}
            />
          </div>
        </div>
      </section>

      <CtaBand />
    </main>
  );
}
