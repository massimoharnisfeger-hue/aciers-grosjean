import { depots, site } from "@/lib/content";

export default function Footer() {
  const year = new Date().getFullYear();
  return (
    <footer className="relative overflow-hidden bg-encre text-white">
      <div className="grid-industrie-dark pointer-events-none absolute inset-0" />
      <div className="container-g relative py-16">
        <div className="grid gap-10 md:grid-cols-4">
          <div className="md:col-span-1">
            <div className="flex items-baseline gap-1.5">
              <span className="h-title text-xl font-bold text-white">GROSJEAN</span>
              <span className="h-sub text-xs text-soft-light">aciers</span>
            </div>
            <p className="mt-4 max-w-xs font-body text-sm text-soft-light">
              Négoce et transformation d'acier depuis 40 ans. L'acier de pro,
              accessible à tous.
            </p>
            <span className="mt-4 inline-block h-1 w-12 rounded-full bg-jaune" />
          </div>

          <div>
            <h4 className="h-title mb-4 text-sm font-semibold uppercase tracking-wider text-soft-light">
              Produits
            </h4>
            <ul className="space-y-2 font-body text-sm text-soft-light">
              <li><a href="#produits" className="hover:text-jaune">Poutrelles</a></li>
              <li><a href="#produits" className="hover:text-jaune">Tôles & tubes</a></li>
              <li><a href="#produits" className="hover:text-jaune">Cornières</a></li>
              <li><a href="#produits" className="hover:text-jaune">Acier corten</a></li>
            </ul>
          </div>

          <div>
            <h4 className="h-title mb-4 text-sm font-semibold uppercase tracking-wider text-soft-light">
              Dépôts
            </h4>
            <ul className="space-y-2 font-body text-sm text-soft-light">
              {depots.map((d) => (
                <li key={d.ville}>{d.ville} <span className="text-white/40">· {d.pays}</span></li>
              ))}
            </ul>
          </div>

          <div>
            <h4 className="h-title mb-4 text-sm font-semibold uppercase tracking-wider text-soft-light">
              Contact
            </h4>
            <ul className="space-y-2 font-body text-sm text-soft-light">
              <li><a href={`tel:${site.tel.replace(/\s/g, "")}`} className="hover:text-jaune">{site.tel}</a></li>
              <li><a href={`mailto:${site.email}`} className="hover:text-jaune">{site.email}</a></li>
              <li className="pt-2"><span className="tag-stock">Certifié EN1090-Exc2</span></li>
            </ul>
          </div>
        </div>

        <div className="mt-14 flex flex-col items-center justify-between gap-3 border-t border-white/10 pt-6 md:flex-row">
          <p className="font-body text-xs text-soft-light">
            © {year} Groupe Aciers Grosjean. Tous droits réservés.
          </p>
          <p className="font-body text-xs text-soft-light">
            Mentions légales · Politique de confidentialité
          </p>
        </div>
      </div>
    </footer>
  );
}
