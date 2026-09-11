import Link from "next/link";
import Logo from "@/components/ui/Logo";
import { site } from "@/lib/content";
import { familles, matieres, totalRefs } from "@/lib/catalogue";
import { servicesDetail, depotsDetail, guides } from "@/lib/edito";

function Colonne({
  titre,
  liens,
}: {
  titre: string;
  liens: { label: string; href: string }[];
}) {
  return (
    <div>
      <h3 className="h-title mb-4 text-xs font-semibold uppercase tracking-[0.14em] text-white/55">
        {titre}
      </h3>
      <ul className="space-y-2">
        {liens.map((l) => (
          <li key={l.href}>
            <Link href={l.href} className="font-body text-sm text-soft-light transition-colors hover:text-jaune">
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

  return (
    <footer className="relative overflow-hidden bg-encre text-white">
      <div className="grid-industrie-dark pointer-events-none absolute inset-0" />

      <div className="container-g relative py-16 md:py-20">
        {/* marque + contact */}
        <div className="grid gap-10 border-b border-white/10 pb-12 md:grid-cols-[1.2fr_1fr]">
          <div>
            <Logo variante="blanc" className="text-2xl" />
            <p className="mt-4 max-w-md font-body text-soft-light">
              Négoce et transformation d'acier depuis 40 ans. {totalRefs} références en stock,
              coupées aux cotes exactes, retirables le jour même dans quatre dépôts.
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
                  <a href={`tel:${site.tel.replace(/[^+\d]/g, "")}`} className="transition-colors hover:text-jaune">
                    {site.tel}
                  </a>
                </li>
                <li>
                  <a href={`mailto:${site.email}`} className="transition-colors hover:text-jaune">
                    {site.email}
                  </a>
                </li>
                <li className="text-white/45">Lun–Ven 7 h – 17 h</li>
              </ul>
            </div>
            <div>
              <h3 className="h-title mb-3 text-xs font-semibold uppercase tracking-[0.14em] text-white/55">
                Certification
              </h3>
              <span className="tag-stock">EN1090-Exc2</span>
              <p className="mt-3 font-body text-xs leading-relaxed text-white/45">
                La norme européenne des structures en acier — que nos concurrents directs
                n'affichent pas.
              </p>
            </div>
          </div>
        </div>

        {/* plan du site */}
        <div className="grid gap-10 py-12 sm:grid-cols-2 lg:grid-cols-5">
          <Colonne
            titre="Catalogue"
            liens={familles.slice(0, 7).map((f) => ({ label: f.nom, href: `/produits/${f.slug}` }))}
          />
          <Colonne
            titre="Matériaux"
            liens={[
              ...matieres.map((m) => ({ label: m.nom, href: `/materiaux/${m.slug}` })),
              ...familles.slice(7).map((f) => ({ label: f.nom, href: `/produits/${f.slug}` })),
            ]}
          />
          <Colonne
            titre="Services"
            liens={servicesDetail.map((s) => ({ label: s.nom, href: `/services/${s.slug}` }))}
          />
          <Colonne
            titre="Guides"
            liens={guides.slice(0, 6).map((g) => ({
              label: g.titre.split(" : ")[0].split(" —")[0],
              href: `/guides/${g.slug}`,
            }))}
          />
          <Colonne
            titre="Dépôts"
            liens={[
              ...depotsDetail.map((d) => ({ label: d.ville, href: `/depots/${d.slug}` })),
              { label: "Contact", href: "/contact" },
              { label: "Réalisations", href: "/realisations" },
              { label: "À propos", href: "/a-propos" },
              { label: "FAQ", href: "/faq" },
            ]}
          />
        </div>

        {/* bas de page */}
        <div className="flex flex-col items-start justify-between gap-4 border-t border-white/10 pt-6 md:flex-row md:items-center">
          <p className="font-body text-xs text-white/45">
            © {year} Groupe Aciers Grosjean. Tous droits réservés.
          </p>
          <ul className="flex flex-wrap gap-x-5 gap-y-2">
            {[
              ["Mentions légales", "/mentions-legales"],
              ["Confidentialité", "/confidentialite"],
              ["Conditions générales", "/conditions-generales"],
            ].map(([l, h]) => (
              <li key={h}>
                <Link href={h} className="font-body text-xs text-white/45 transition-colors hover:text-jaune">
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
