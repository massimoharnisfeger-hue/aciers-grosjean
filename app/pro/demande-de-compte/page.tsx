import type { Metadata } from "next";
import Link from "next/link";
import PageHeader from "@/components/ui/PageHeader";
import CtaBand from "@/components/sections/CtaBand";
import FormulairePro from "@/components/sections/FormulairePro";

export const metadata: Metadata = {
  title: "Demande de compte professionnel | Aciers Grosjean",
  description:
    "Ouvrez un compte pro : tarifs négociés selon vos volumes, paiement différé et interlocuteur dédié. Un numéro de TVA valide suffit.",
  alternates: { canonical: "/pro/demande-de-compte" },
};

export default function DemandeComptePro() {
  return (
    <main>
      <PageHeader
        surtitre="Espace pro"
        titre={
          <>
            Ouvrir un <span className="mark-jaune">compte pro</span>
          </>
        }
        intro="Un numéro de TVA valide suffit pour démarrer. On revient vers vous sous quelques jours ouvrables avec vos conditions."
      />

      <section className="bg-white py-14 md:py-20">
        <div className="container-g grid gap-10 lg:grid-cols-[1fr_20rem] lg:gap-16">
          <FormulairePro />

          <aside className="lg:sticky lg:top-28 lg:self-start">
            <div className="rounded-2xl border border-brume bg-nuage p-6">
              <h2 className="h-title text-sm font-semibold uppercase tracking-[0.14em] text-soft">
                Comment ça se passe
              </h2>
              <ol className="mt-4 space-y-4">
                {[
                  ["Vous envoyez la demande", "Cinq champs obligatoires, deux minutes."],
                  ["On vérifie le numéro de TVA", "Contrôle de validité et d'activité."],
                  ["Un commercial vous appelle", "Pour caler vos conditions sur vos volumes réels."],
                  ["Le compte est ouvert", "Vous commandez avec vos tarifs et vos délais."],
                ].map(([t, d], i) => (
                  <li key={t} className="flex gap-3">
                    <span className="h-title shrink-0 font-mono text-xs text-soft">
                      {String(i + 1).padStart(2, "0")}
                    </span>
                    <span>
                      <span className="h-title block text-sm font-semibold text-encre">{t}</span>
                      <span className="mt-0.5 block font-body text-sm text-soft">{d}</span>
                    </span>
                  </li>
                ))}
              </ol>
            </div>

            <div className="mt-5 rounded-2xl border border-brume p-6">
              <h2 className="h-title text-sm font-semibold uppercase tracking-[0.14em] text-soft">
                Pas encore décidé&nbsp;?
              </h2>
              <p className="mt-3 font-body text-sm leading-relaxed text-soft">
                Vous pouvez commander sans compte, aux prix affichés. Le compte pro sert quand
                les commandes deviennent régulières.
              </p>
              <Link href="/pro" className="btn-ghost mt-5 w-full justify-center">
                Voir les avantages
              </Link>
            </div>
          </aside>
        </div>
      </section>

      <CtaBand />
    </main>
  );
}
