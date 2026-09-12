import type { Metadata } from "next";
import PageEspace from "@/components/ui/PageEspace";

export const metadata: Metadata = {
  title: "Créer un compte | Aciers Grosjean",
  description: "Créer un compte n’est pas obligatoire pour commander chez nous : envoyez votre demande, on chiffre sous 24 h et vous retirez en dépôt.",
  alternates: { canonical: "/compte/inscription" },
  robots: { index: false, follow: true },
};

export default function Page() {
  return (
    <PageEspace
      surtitre="Mon compte"
      titre={<>Créer un compte</>}
      intro="La création de compte en ligne arrive avec l’espace client. Bonne nouvelle : elle n’est pas obligatoire pour commander."
      maintenant="Il n’y a aucune obligation d’avoir un compte. Envoyez votre demande de devis, on vous répond sous 24 h avec le prix exact et le dépôt de retrait."
      aVenir={["Enregistrer vos coordonnées une fois pour toutes", "Garder l’historique de vos devis", "Recevoir un rappel quand un devis arrive à échéance"]}
    />
  );
}
