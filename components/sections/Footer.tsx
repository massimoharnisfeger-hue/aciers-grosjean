import Link from "next/link";
import Logo from "@/components/ui/Logo";
import { site, lienTel } from "@/lib/content";
import { univers, noeuds, totalProduits } from "@/lib/catalogue";
import { catalogueActif } from "@/lib/catalogue-visuel";
import { servicesDetail, depotsDetail, articles } from "@/lib/edito";

function Colonne({ titre, liens }: { titre: string; liens: { label: string; href: string }[] }) {
  return (
    <div>
      <h3 className="h-title mb-4 text-xs font-semibold uppercase tracking-[0.14em] text-white/55">
        {titre}
      </h3>
      <ul className="space-y-2">
        {liens.map((l) => (
          <li key={l.href}>
            <Link href={l.href} className="lien-tactile font-body text-sm text-soft-light transition-colors hover:text-jaune">
              {l.label}
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default function Footer() {
  const year = new Date().getFullYear();
  const acier = univers.find((u) => u.slug === "acier");
  const famillesAcier = (acier?.enfants ?? []).map((c) => noeuds[c]).filter(Boolean);

  return (
    <footer className="relative overflow-hidden bg-encre text-white">
      <div className="grid-industrie-dark pointer-events-none absolute inset-0" />

      <div className="container-g relative py-16 md:py-20">
        <div className="grid gap-10 border-b border-white/10 pb-12 md:grid-cols-[1.2fr_1fr]">
          <div>
            <Logo variante="blanc" hauteur={56} />
            <p className="mt-4 max-w-md font-body text-soft-light">
              Négoce et transformation d&apos;acier depuis 40 ans. {totalProduits} produits en stock,
              coupés aux cotes exactes, retirables le jour même dans quatre dépôts.
            </p>
            <span className="mt-5 inline-block h-1 w-12 rounded-full bg-jaune" />
          </div>

          <div className="grid gap-6 sm:grid-cols-2">
            <div>
              <h3 className="h-title mb-3 text-xs font-semibold uppercase tracking-[0.14em] text-white/55">
                Nous joindre
              </h3>
              <ul className="space-y-2 font-body text-sm text-soft-light">
                <li>
                  <a href={lienTel(site.tel)} className="lien-tactile transition-colors hover:text-jaune">
                    {site.tel}
                  </a>
                </li>
                <li>
                  <a href={`mailto:${site.email}`} className="lien-tactile transition-colors hover:text-jaune">
                    {site.email}
                  </a>
                </li>
                <li className="text-white/45">Lun–Jeu 8 h – 17 h · Ven 8 h – 16 h 30</li>
              </ul>
            </div>
            <div>
              <h3 className="h-title mb-3 text-xs font-semibold uppercase tracking-[0.14em] text-white/55">
                Certification
              </h3>
              <Link href="/entreprise/certifications" className="lien-tactile tag-stock">EN 1090-Exc2</Link>
              <p className="mt-3 font-body text-xs leading-relaxed text-white/45">
                La norme européenne des structures en acier, que nos concurrents directs
                n&apos;affichent pas.
              </p>
            </div>
          </div>
        </div>

        <div className="grid gap-10 py-12 sm:grid-cols-2 lg:grid-cols-5">
          <Colonne
            titre="Univers"
            liens={[
              ...univers.map((u) => ({ label: u.nom, href: `/${u.slug}` })),
              ...(catalogueActif ? [{ label: "Catalogue en images", href: "/catalogue" }] : []),
            ]}
          />
          <Colonne
            titre="Acier"
            liens={famillesAcier.map((f) => ({ label: f.nom, href: f.chemin }))}
          />
          <Colonne
            titre="Services"
            liens={servicesDetail.slice(0, 6).map((s) => ({ label: s.nom, href: `/services/${s.slug}` }))}
          />
          <Colonne
            titre="Conseils"
            liens={articles.slice(0, 5).map((a) => ({
              label: a.titre.split(" : ")[0].split(" — ")[0],
              href: `/conseils/${a.slug}`,
            })).concat([{ label: "Tous les conseils", href: "/conseils" }])}
          />
          <Colonne
            titre="Aciers Grosjean"
            liens={[
              ...depotsDetail.map((d) => ({ label: d.ville, href: `/depots/${d.slug}` })),
              { label: "L'entreprise", href: "/entreprise" },
              { label: "Espace pro", href: "/pro" },
              { label: "Contact", href: "/contact" },
              { label: "Plan du site", href: "/plan-du-site" },
            ]}
          />
        </div>

        <div className="flex flex-col items-start justify-between gap-4 border-t border-white/10 pt-6 md:flex-row md:items-center">
          <p className="font-body text-xs text-white/45">
            © {year} Groupe Aciers Grosjean. Tous droits réservés.
          </p>
          <ul className="flex flex-wrap gap-x-5 gap-y-2">
            {[
              ["Conditions générales", "/conditions-generales-de-vente"],
              ["Protection des données", "/protection-des-donnees"],
              ["Cookies", "/cookies"],
              ["Mentions légales", "/mentions-legales"],
            ].map(([l, h]) => (
              <li key={h}>
                <Link href={h} className="lien-tactile font-body text-xs text-white/45 transition-colors hover:text-jaune">
                  {l}
                </Link>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </footer>
  );
}
