import type { Metadata } from "next";
import PageEspace from "@/components/ui/PageEspace";

export const metadata: Metadata = {
  title: "Panier — chiffrage immédiat, prix ferme sous 24 h",
  description: "Estimez votre besoin sur chaque fiche produit : poids, découpe et total HTVA. Vous recevez le prix ferme sous 24 h et vous payez au retrait.",
  alternates: { canonical: "/panier" },
  robots: { index: false, follow: true },
};

export default function Page() {
  return (
    <PageEspace
      surtitre="Panier"
      titre={<>Votre panier</>}
      intro="La commande en ligne avec paiement est en cours de déploiement. Le chiffrage, lui, est déjà immédiat."
      maintenant="Sur chaque fiche produit, le calculateur donne le poids et l’estimation de prix pour votre quantité, puis prépare le message de demande. Vous recevez le prix ferme sous 24 h et vous payez au retrait."
      aVenir={["Ajouter vos références au panier depuis les fiches produits", "Voir le supplément de coupe avant de valider", "Choisir le dépôt et le créneau de retrait", "Payer en ligne ou au comptoir"]}
    />
  );
}
