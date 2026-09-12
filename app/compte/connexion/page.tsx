import type { Metadata } from "next";
import PageEspace from "@/components/ui/PageEspace";

export const metadata: Metadata = {
  title: "Connexion | Aciers Grosjean",
  description: "Espace client Aciers Grosjean : suivi de commandes, devis et documents.",
  alternates: { canonical: "/compte/connexion" },
  robots: { index: false, follow: true },
};

export default function Page() {
  return (
    <PageEspace
      surtitre="Mon compte"
      titre={<>Espace client</>}
      intro="L’espace client en ligne est en cours de déploiement. Vous n’avez besoin d’aucun compte pour commander."
      maintenant="Aucun compte n’est nécessaire pour acheter chez nous, ni aucun numéro de TVA. Décrivez votre besoin, on chiffre sous 24 h, et vous retirez en dépôt. Les particuliers sont les bienvenus, même pour de petites quantités."
      aVenir={["Retrouver vos devis et vos commandes", "Suivre l’état de préparation d’un enlèvement", "Réutiliser une liste de débit déjà passée", "Télécharger vos factures"]}
    />
  );
}
