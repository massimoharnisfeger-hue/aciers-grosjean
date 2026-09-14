import Link from "next/link";
import PageHeader from "@/components/ui/PageHeader";
import CtaBand from "@/components/sections/CtaBand";
import { site, lienTel } from "@/lib/content";

/**
 * Gabarit des pages d'espace client et de commande.
 *
 * Ce site est généré en statique : il n'y a ni base de données, ni session, ni
 * paiement. Plutôt que d'afficher un formulaire de connexion qui ne connecte à
 * rien — et qui demanderait un mot de passe pour rien — ces pages annoncent
 * clairement l'état du service et donnent le chemin qui fonctionne aujourd'hui.
 */
export default function PageEspace({
  surtitre,
  titre,
  intro,
  aVenir,
  maintenant,
}: {
  surtitre: string;
  titre: React.ReactNode;
  intro: string;
  aVenir: string[];
  maintenant: string;
}) {
  return (
    <main>
      <PageHeader surtitre={surtitre} titre={titre} intro={intro} />

      <section className="bg-white py-16 md:py-20">
        <div className="container-g grid gap-6 md:grid-cols-2">
          <div className="rounded-2xl border-l-4 border-jaune bg-nuage p-8">
            <h2 className="h-title text-lg font-semibold text-encre">
              En attendant, voici ce qui marche
            </h2>
            <p className="mt-2 font-body leading-relaxed text-soft">{maintenant}</p>
            <div className="mt-6 flex flex-wrap gap-3">
              <Link href="/devis" className="btn-cta">Demander un devis</Link>
              <a href={lienTel(site.tel)} className="btn-ghost">
                {site.tel}
              </a>
            </div>
            <p className="mt-4 font-body text-sm text-soft">
              Ou par e-mail à{" "}
              <a href={`mailto:${site.email}`} className="text-encre underline hover:text-jaune">
                {site.email}
              </a>{" "}
              — réponse sous 24&nbsp;h ouvrées.
            </p>
          </div>

          <div className="rounded-2xl border border-brume p-8">
            <h2 className="h-title text-lg font-semibold text-encre">Ce que cet espace fera</h2>
            <ul className="mt-4 space-y-3">
              {aVenir.map((x) => (
                <li key={x} className="flex gap-3 font-body text-soft">
                  <span className="mt-[0.55em] h-1.5 w-1.5 shrink-0 rounded-full bg-jaune" aria-hidden="true" />
                  <span>{x}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </section>

      <CtaBand />
    </main>
  );
}
