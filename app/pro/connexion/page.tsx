import type { Metadata } from "next";
import PageEspace from "@/components/ui/PageEspace";

export const metadata: Metadata = {
  title: "Connexion compte professionnel | Aciers Grosjean",
  description: "Accès au compte professionnel Aciers Grosjean : commandes, documents et conditions négociées.",
  alternates: { canonical: "/pro/connexion" },
  robots: { index: false, follow: true },
};

export default function Page() {
  return (
    <PageEspace
      surtitre="Espace pro"
      titre={<>Accès au compte professionnel</>}
      intro="L’espace pro en ligne est en cours de déploiement. Vos conditions négociées, elles, sont déjà actives."
      maintenant="Passez vos commandes par téléphone ou par e-mail auprès de votre interlocuteur habituel. Vos conditions tarifaires et vos délais de paiement s’appliquent exactement de la même façon."
      aVenir={["Consulter vos tarifs négociés en ligne", "Recommander une liste de débit en quelques clics", "Suivre vos commandes et vos enlèvements", "Télécharger factures, bons de livraison et certificats matière", "Gérer plusieurs utilisateurs sur le même compte"]}
    />
  );
}
