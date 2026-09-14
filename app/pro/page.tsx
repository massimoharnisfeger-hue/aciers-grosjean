import type { Metadata } from "next";
import Link from "next/link";
import PageHeader from "@/components/ui/PageHeader";
import CtaBand from "@/components/sections/CtaBand";
import Reveal from "@/components/fx/Reveal";
import { site, lienTel } from "@/lib/content";

export const metadata: Metadata = {
  title: "Espace pro — tarifs négociés et paiement différé",
  description:
    "Tarifs négociés selon vos volumes, paiement différé et interlocuteur dédié. Un numéro de TVA suffit, réponse sous quelques jours ouvrables.",
  alternates: { canonical: "/pro" },
};

const avantages = [
  {
    titre: "Tarifs négociés",
    texte:
      "Le tarif est indexé sur vos volumes réels, pas sur une grille figée. Plus vous consommez régulièrement, plus la remise est structurelle.",
  },
  {
    titre: "Paiement différé",
    texte:
      "Conditions de paiement définies à l'ouverture du compte. Vous commandez au fil du chantier sans repasser par la caisse à chaque enlèvement.",
  },
  {
    titre: "Un interlocuteur qui vous connaît",
    texte:
      "Le même commercial suit vos dossiers. Il sait ce que vous faites, ce que vous commandez d'habitude et ce qui traîne en délai — ça change tout au téléphone.",
  },
  {
    titre: "Commande rapide",
    texte:
      "Vos références habituelles sont mémorisées : vous recommandez une liste de débit complète en quelques lignes, sans tout retaper.",
  },
  {
    titre: "Documents centralisés",
    texte:
      "Factures, bons de livraison et certificats matière regroupés par chantier. De quoi répondre à un contrôle sans chercher dans les mails.",
  },
  {
    titre: "Devis sous 24 h",
    texte:
      "Même délai que pour tout le monde, mais avec un chiffrage qui tient compte de vos conditions et de vos habitudes de découpe.",
  },
];

export default function ProPage() {
  return (
    <main>
      <PageHeader
        surtitre="Espace pro"
        titre={
          <>
            Un compte pro, <span className="mark-jaune">et tout va plus vite</span>
          </>
        }
        intro="Artisan, métallier, ferronnier, entrepreneur : le compte professionnel donne accès à des conditions négociées, au paiement différé et à un interlocuteur qui connaît vos dossiers."
      />

      <section className="bg-white py-16 md:py-24">
        <div className="container-g">
          <div className="grid gap-5 md:grid-cols-2 lg:grid-cols-3">
            {avantages.map((a, i) => (
              <Reveal key={a.titre} delay={(i % 3) * 0.06}>
                <div className="flex h-full flex-col rounded-2xl border border-brume bg-white p-7">
                  <span className="font-mono text-xs text-soft">{String(i + 1).padStart(2, "0")}</span>
                  <h2 className="h-title mt-3 text-lg font-semibold text-encre">{a.titre}</h2>
                  <p className="mt-2 font-body leading-relaxed text-soft">{a.texte}</p>
                </div>
              </Reveal>
            ))}
          </div>

          <div className="mt-12 grid gap-5 md:grid-cols-2">
            <div className="rounded-2xl border border-brume bg-nuage p-8">
              <h2 className="h-title text-lg font-semibold text-encre">Ouvrir un compte</h2>
              <p className="mt-2 font-body text-soft">
                Un numéro de TVA valide suffit pour démarrer. La demande prend cinq minutes et la
                réponse intervient sous quelques jours ouvrables.
              </p>
              <Link href="/pro/demande-de-compte" className="btn-cta mt-6">
                Demander un compte pro
              </Link>
            </div>

            <div className="rounded-2xl border border-brume p-8">
              <h2 className="h-title text-lg font-semibold text-encre">Vous avez déjà un compte</h2>
              <p className="mt-2 font-body text-soft">
                Les commandes se passent aujourd'hui par téléphone ou par e-mail auprès de votre
                interlocuteur habituel — c'est souvent plus rapide qu'un formulaire.
              </p>
              <div className="mt-6 flex flex-wrap gap-3">
                <Link href="/pro/connexion" className="btn-ghost">Accès au compte</Link>
                <a href={lienTel(site.tel)} className="btn-ghost">
                  {site.tel}
                </a>
              </div>
            </div>
          </div>
        </div>
      </section>

      <CtaBand />
    </main>
  );
}
